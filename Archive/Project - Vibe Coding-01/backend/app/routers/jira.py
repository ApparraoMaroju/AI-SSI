"""Jira API router."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas import (
    JiraConnectionRequest,
    JiraConnectionResponse,
    JiraIssueRequest,
    JiraIssueResponse
)
from app.services.jira_service import JiraService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/test-connection", response_model=JiraConnectionResponse)
async def test_connection(request: JiraConnectionRequest) -> JiraConnectionResponse:
    """
    Test Jira connection with provided credentials.
    Validates that the credentials are correct and the user has access.
    """
    logger.info(f"Testing connection to {request.credentials.base_url}")
    
    service = JiraService(request.credentials)
    success, message, user_name = await service.test_connection()
    
    return JiraConnectionResponse(
        success=success,
        message=message,
        user_display_name=user_name
    )


@router.post("/fetch-issue", response_model=JiraIssueResponse)
async def fetch_issue(request: JiraIssueRequest) -> JiraIssueResponse:
    """
    Fetch and parse a Jira issue by ID.
    Returns the parsed issue including summary, description, acceptance criteria, etc.
    """
    logger.info(f"Fetching issue {request.issue_id}")
    
    # Validate issue ID format
    if not request.issue_id or not request.issue_id.strip():
        return JiraIssueResponse(
            success=False,
            message="Issue ID is required",
            issue=None
        )
    
    service = JiraService(request.credentials)
    success, message, issue = await service.fetch_issue(request.issue_id.strip().upper())
    
    if not success:
        return JiraIssueResponse(
            success=False,
            message=message,
            issue=None
        )
    
    # Validate that issue has enough content for test generation
    if issue and not issue.description and not issue.acceptance_criteria:
        logger.warning(f"Issue {request.issue_id} has no description or acceptance criteria")
        return JiraIssueResponse(
            success=True,
            message="Warning: Issue has no description or acceptance criteria. Test case quality may be limited.",
            issue=issue
        )
    
    return JiraIssueResponse(
        success=success,
        message=message,
        issue=issue
    )
