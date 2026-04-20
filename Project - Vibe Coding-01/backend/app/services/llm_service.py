"""LLM service for test case generation using Claude."""

import json
import logging
import time
from typing import List, Tuple, Optional
import anthropic

from app.schemas import JiraIssue, TestCase, TestTemplate, TemplateType
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMService:
    """Service for generating test cases using Claude LLM."""
    
    SYSTEM_PROMPT = """You are an expert QA engineer specializing in test case design. Your task is to generate comprehensive, structured test cases based on Jira user stories.

STRICT REQUIREMENTS:
1. Generate at least {min_cases} test cases
2. Output ONLY valid JSON matching the exact schema provided
3. Include a mix of test types: Positive, Negative, Edge, Boundary, and Security
4. Each test case must have clear, actionable steps
5. All test cases must trace back to the provided user story

TEST CASE SCHEMA (each test case must match this exactly):
{{
    "id": "TC_XXX",
    "title": "Descriptive test title",
    "type": "Positive | Negative | Edge | Boundary | Security",
    "priority": "P0 | P1 | P2",
    "preconditions": "Setup requirements before test execution",
    "steps": ["Step 1", "Step 2", "Step 3"],
    "test_data": "Required test data specifications",
    "expected_result": "Expected outcome after test execution",
    "linked_jira_id": "{jira_id}"
}}

OUTPUT FORMAT:
Return ONLY a JSON object with this structure:
{{
    "test_cases": [<array of test cases>]
}}

No explanations, no markdown code blocks, just pure JSON."""

    def __init__(self, api_key: str):
        """Initialize LLM service with API key."""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = settings.llm_model
        self.max_tokens = settings.llm_max_tokens
        self.temperature = settings.llm_temperature
    
    def _get_template_context(self, template_type: TemplateType, custom_template: Optional[str] = None) -> str:
        """Get template-specific context for the prompt."""
        template_contexts = {
            TemplateType.FUNCTIONAL: """
FOCUS: Functional Testing
- Verify all functional requirements work as specified
- Cover happy path and primary use cases
- Validate input/output behavior
- Test data validation and error handling
- Priority: P0 for critical flows, P1 for secondary""",
            
            TemplateType.REGRESSION: """
FOCUS: Regression Testing
- Ensure existing functionality is not broken
- Cover integration points
- Test backward compatibility
- Validate data integrity
- Include tests for previously reported bugs
- Priority: P1 for core features, P2 for edge cases""",
            
            TemplateType.SMOKE: """
FOCUS: Smoke Testing
- Critical path verification only
- Quick sanity checks for main functionality
- Minimal but essential test coverage
- All tests should be P0 priority
- Focus on "does it work at all" scenarios""",
            
            TemplateType.EDGE: """
FOCUS: Edge Case Testing
- Boundary value analysis
- Extreme input values
- Empty/null/undefined scenarios
- Maximum/minimum limits
- Race conditions and timing issues
- Priority: P1 for likely scenarios, P2 for unlikely""",
            
            TemplateType.SECURITY: """
FOCUS: Security Testing
- Input validation and sanitization
- Authentication/authorization checks
- SQL injection prevention
- XSS vulnerability checks  
- CSRF protection
- Data exposure risks
- Priority: P0 for critical vulnerabilities, P1 for medium""",
            
            TemplateType.CUSTOM: f"""
CUSTOM TEMPLATE REQUIREMENTS:
{custom_template if custom_template else "No custom requirements specified. Use balanced coverage."}"""
        }
        
        return template_contexts.get(template_type, template_contexts[TemplateType.FUNCTIONAL])
    
    def _build_user_prompt(
        self,
        issue: JiraIssue,
        template_type: TemplateType,
        custom_template: Optional[str],
        min_cases: int
    ) -> str:
        """Build the user prompt for test case generation."""
        template_context = self._get_template_context(template_type, custom_template)
        
        prompt = f"""Generate test cases for the following Jira user story:

=== JIRA ISSUE: {issue.key} ===

SUMMARY: {issue.summary}

ISSUE TYPE: {issue.issue_type}
PRIORITY: {issue.priority}
STATUS: {issue.status}
COMPONENTS: {', '.join(issue.components) if issue.components else 'None'}
LABELS: {', '.join(issue.labels) if issue.labels else 'None'}

DESCRIPTION:
{issue.description or 'No description provided'}

ACCEPTANCE CRITERIA:
{issue.acceptance_criteria or 'No explicit acceptance criteria. Derive from description.'}

=== TEST TEMPLATE ===
{template_context}

=== REQUIREMENTS ===
1. Generate at least {min_cases} test cases
2. Ensure diverse coverage: include Positive, Negative, and at least one Edge or Boundary case
3. Make steps specific and actionable
4. Link all test cases to {issue.key}
5. Prioritize based on business impact

Generate the test cases now as JSON."""
        
        return prompt
    
    async def generate_test_cases(
        self,
        issue: JiraIssue,
        template_type: TemplateType = TemplateType.FUNCTIONAL,
        custom_template: Optional[str] = None,
        min_cases: int = 5
    ) -> Tuple[bool, str, List[TestCase], int, int]:
        """
        Generate test cases for a Jira issue using Claude.
        
        Returns:
            Tuple of (success, message, test_cases, generation_time_ms, tokens_used)
        """
        start_time = time.time()
        
        try:
            system_prompt = self.SYSTEM_PROMPT.format(
                min_cases=min_cases,
                jira_id=issue.key
            )
            
            user_prompt = self._build_user_prompt(
                issue=issue,
                template_type=template_type,
                custom_template=custom_template,
                min_cases=min_cases
            )
            
            logger.info(f"Sending request to Claude for {issue.key}")
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Calculate metrics
            generation_time_ms = int((time.time() - start_time) * 1000)
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            logger.info(f"Claude response received in {generation_time_ms}ms, {tokens_used} tokens used")
            
            # Parse response
            content = response.content[0].text
            
            # Try to extract JSON from response
            try:
                # Handle potential markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                data = json.loads(content.strip())
                
                if "test_cases" not in data:
                    # If root is already an array
                    if isinstance(data, list):
                        data = {"test_cases": data}
                    else:
                        raise ValueError("Response missing 'test_cases' key")
                
                test_cases = []
                for i, tc_data in enumerate(data["test_cases"]):
                    # Ensure ID is properly formatted
                    if "id" not in tc_data or not tc_data["id"]:
                        tc_data["id"] = f"TC_{str(i+1).zfill(3)}"
                    
                    # Set linked_jira_id if missing
                    if "linked_jira_id" not in tc_data or not tc_data["linked_jira_id"]:
                        tc_data["linked_jira_id"] = issue.key
                    
                    test_case = TestCase(**tc_data)
                    test_cases.append(test_case)
                
                logger.info(f"Successfully parsed {len(test_cases)} test cases")
                
                # Validate minimum count
                if len(test_cases) < min_cases:
                    logger.warning(f"Only {len(test_cases)} test cases generated, minimum is {min_cases}")
                    return (
                        False,
                        f"Only {len(test_cases)} test cases generated. Please regenerate.",
                        test_cases,
                        generation_time_ms,
                        tokens_used
                    )
                
                return True, "Test cases generated successfully", test_cases, generation_time_ms, tokens_used
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Raw response: {content}")
                return False, f"Failed to parse LLM response as JSON: {str(e)}", [], generation_time_ms, tokens_used
            except ValueError as e:
                logger.error(f"Invalid response structure: {e}")
                return False, str(e), [], generation_time_ms, tokens_used
                
        except anthropic.AuthenticationError:
            logger.error("Anthropic authentication failed")
            return False, "Invalid Anthropic API key. Please check your configuration.", [], 0, 0
        except anthropic.RateLimitError:
            logger.error("Anthropic rate limit exceeded")
            return False, "API rate limit exceeded. Please wait and try again.", [], 0, 0
        except anthropic.APITimeoutError:
            logger.error("Anthropic API timeout")
            return False, "LLM request timed out. Please try again.", [], 0, 0
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            return False, f"LLM API error: {str(e)}", [], 0, 0
        except Exception as e:
            logger.exception("Unexpected error during test case generation")
            return False, f"Unexpected error: {str(e)}", [], 0, 0
