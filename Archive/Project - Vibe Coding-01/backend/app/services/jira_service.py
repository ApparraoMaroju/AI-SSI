"""Jira integration service."""

import logging
import re
import httpx
from typing import Optional, Tuple
from app.schemas import JiraCredentials, JiraIssue

logger = logging.getLogger(__name__)


class JiraService:
    """Service for interacting with Jira REST API."""
    
    def __init__(self, credentials: JiraCredentials):
        """Initialize Jira service with credentials."""
        self.base_url = credentials.base_url.rstrip("/")
        self.email = credentials.email
        self.api_token = credentials.api_token
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                auth=(self.email, self.api_token),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def test_connection(self) -> Tuple[bool, str, Optional[str]]:
        """
        Test Jira connection and return status.
        
        Returns:
            Tuple of (success, message, user_display_name)
        """
        try:
            client = await self._get_client()
            response = await client.get("/rest/api/3/myself")
            
            if response.status_code == 200:
                user_data = response.json()
                display_name = user_data.get("displayName", "Unknown User")
                logger.info(f"Jira connection successful for user: {display_name}")
                return True, "Connection successful", display_name
            elif response.status_code == 401:
                logger.warning("Jira authentication failed")
                return False, "Authentication failed. Check your email and API token.", None
            elif response.status_code == 403:
                logger.warning("Jira access forbidden")
                return False, "Access forbidden. Check your permissions.", None
            else:
                logger.error(f"Jira connection failed: {response.status_code}")
                return False, f"Connection failed with status {response.status_code}", None
                
        except httpx.ConnectError:
            logger.error(f"Cannot connect to Jira at {self.base_url}")
            return False, f"Cannot connect to Jira at {self.base_url}. Check the URL.", None
        except httpx.TimeoutException:
            logger.error("Jira connection timed out")
            return False, "Connection timed out. Please try again.", None
        except Exception as e:
            logger.exception("Unexpected error testing Jira connection")
            return False, f"Unexpected error: {str(e)}", None
        finally:
            await self.close()
    
    def _extract_acceptance_criteria(self, description: str) -> Optional[str]:
        """Extract acceptance criteria from description."""
        if not description:
            return None
        
        # Common patterns for acceptance criteria
        patterns = [
            r"(?i)acceptance\s+criteria[:\s]*\n?(.*?)(?=\n\n|\Z)",
            r"(?i)ac[:\s]*\n?(.*?)(?=\n\n|\Z)",
            r"(?i)given\s+.*?when\s+.*?then\s+.*",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description, re.DOTALL)
            if match:
                return match.group(0).strip()
        
        return None
    
    def _convert_adf_to_text(self, adf_content: dict) -> str:
        """Convert Atlassian Document Format to plain text."""
        if not adf_content or not isinstance(adf_content, dict):
            return ""
        
        def extract_text(node):
            if isinstance(node, str):
                return node
            if isinstance(node, dict):
                text_parts = []
                if node.get("type") == "text":
                    return node.get("text", "")
                if node.get("type") == "hardBreak":
                    return "\n"
                if "content" in node:
                    for child in node["content"]:
                        text_parts.append(extract_text(child))
                # Add newlines for block elements
                if node.get("type") in ["paragraph", "heading", "bulletList", "orderedList", "listItem"]:
                    text_parts.append("\n")
                return "".join(text_parts)
            if isinstance(node, list):
                return "".join(extract_text(item) for item in node)
            return ""
        
        return extract_text(adf_content).strip()
    
    async def fetch_issue(self, issue_id: str) -> Tuple[bool, str, Optional[JiraIssue]]:
        """
        Fetch and parse a Jira issue.
        
        Args:
            issue_id: Jira issue key (e.g., PROJ-123)
            
        Returns:
            Tuple of (success, message, parsed_issue)
        """
        try:
            client = await self._get_client()
            
            # Fetch issue with all required fields
            fields = "summary,description,issuetype,priority,status,components,labels,reporter,assignee"
            response = await client.get(
                f"/rest/api/3/issue/{issue_id}",
                params={"fields": fields}
            )
            
            if response.status_code == 200:
                data = response.json()
                fields_data = data.get("fields", {})
                
                # Parse description (may be ADF format in Jira Cloud)
                description_raw = fields_data.get("description")
                if isinstance(description_raw, dict):
                    description = self._convert_adf_to_text(description_raw)
                else:
                    description = description_raw or ""
                
                # Extract acceptance criteria
                acceptance_criteria = self._extract_acceptance_criteria(description)
                
                # Parse components
                components = [c.get("name", "") for c in fields_data.get("components", []) if c.get("name")]
                
                # Parse labels
                labels = fields_data.get("labels", [])
                
                issue = JiraIssue(
                    id=data.get("id", ""),
                    key=data.get("key", issue_id),
                    summary=fields_data.get("summary", "No summary"),
                    description=description,
                    acceptance_criteria=acceptance_criteria,
                    issue_type=fields_data.get("issuetype", {}).get("name", "Unknown"),
                    priority=fields_data.get("priority", {}).get("name", "None"),
                    status=fields_data.get("status", {}).get("name", "Unknown"),
                    components=components,
                    labels=labels,
                    reporter=fields_data.get("reporter", {}).get("displayName") if fields_data.get("reporter") else None,
                    assignee=fields_data.get("assignee", {}).get("displayName") if fields_data.get("assignee") else None
                )
                
                logger.info(f"Successfully fetched issue {issue_id}")
                return True, "Issue fetched successfully", issue
                
            elif response.status_code == 404:
                logger.warning(f"Issue {issue_id} not found")
                return False, f"Issue {issue_id} not found. Check the issue ID.", None
            elif response.status_code == 401:
                return False, "Authentication failed. Please reconnect to Jira.", None
            elif response.status_code == 403:
                return False, f"Access denied to issue {issue_id}.", None
            else:
                return False, f"Failed to fetch issue: HTTP {response.status_code}", None
                
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching issue {issue_id}")
            return False, "Request timed out. Please try again.", None
        except Exception as e:
            logger.exception(f"Error fetching issue {issue_id}")
            return False, f"Error fetching issue: {str(e)}", None
        finally:
            await self.close()
