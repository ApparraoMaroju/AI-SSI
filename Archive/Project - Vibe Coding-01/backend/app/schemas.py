"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


# ============= Enums =============

class TestType(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    EDGE = "Edge"
    BOUNDARY = "Boundary"
    SECURITY = "Security"


class Priority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"


class TemplateType(str, Enum):
    FUNCTIONAL = "Functional"
    REGRESSION = "Regression"
    SMOKE = "Smoke"
    EDGE = "Edge"
    SECURITY = "Security"
    CUSTOM = "Custom"


# ============= Jira Models =============

class JiraCredentials(BaseModel):
    """Jira authentication credentials."""
    base_url: str = Field(..., description="Jira instance base URL", example="https://company.atlassian.net")
    email: str = Field(..., description="Jira user email", example="user@company.com")
    api_token: str = Field(..., description="Jira API token")


class JiraConnectionRequest(BaseModel):
    """Request to test Jira connection."""
    credentials: JiraCredentials


class JiraConnectionResponse(BaseModel):
    """Response for connection test."""
    success: bool
    message: str
    user_display_name: Optional[str] = None


class JiraIssueRequest(BaseModel):
    """Request to fetch a Jira issue."""
    credentials: JiraCredentials
    issue_id: str = Field(..., description="Jira issue ID", example="PROJ-123")


class JiraIssue(BaseModel):
    """Parsed Jira issue data."""
    id: str
    key: str
    summary: str
    description: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    issue_type: str
    priority: str
    status: str
    components: List[str] = []
    labels: List[str] = []
    reporter: Optional[str] = None
    assignee: Optional[str] = None


class JiraIssueResponse(BaseModel):
    """Response containing parsed Jira issue."""
    success: bool
    message: str
    issue: Optional[JiraIssue] = None


# ============= Test Case Models =============

class TestCase(BaseModel):
    """Single test case following the strict schema."""
    id: str = Field(..., description="Test case ID", example="TC_001")
    title: str = Field(..., description="Test case title")
    type: TestType = Field(..., description="Type of test case")
    priority: Priority = Field(..., description="Test priority")
    preconditions: str = Field(..., description="Setup requirements")
    steps: List[str] = Field(..., description="Test steps", min_length=1)
    test_data: str = Field(..., description="Required test data")
    expected_result: str = Field(..., description="Expected outcome")
    linked_jira_id: str = Field(..., description="Linked Jira ticket ID")


class TestCaseGenerateRequest(BaseModel):
    """Request to generate test cases."""
    issue: JiraIssue
    template_type: TemplateType = TemplateType.FUNCTIONAL
    custom_template: Optional[str] = None
    min_test_cases: int = Field(default=5, ge=5, description="Minimum number of test cases")
    anthropic_api_key: str = Field(..., description="Anthropic API key for LLM")


class TestCaseGenerateResponse(BaseModel):
    """Response containing generated test cases."""
    success: bool
    message: str
    test_cases: List[TestCase] = []
    generation_time_ms: int = 0
    tokens_used: int = 0


# ============= Export Models =============

class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    CSV = "csv"
    TSV = "tsv"


class ExportRequest(BaseModel):
    """Request to export test cases."""
    test_cases: List[TestCase]
    format: ExportFormat
    include_header: bool = True


class ExportResponse(BaseModel):
    """Response with exported content."""
    success: bool
    content: str
    filename: str
    content_type: str


# ============= Template Models =============

class TestTemplate(BaseModel):
    """Test template configuration."""
    name: str
    description: str
    coverage_categories: List[str]
    depth: Literal["shallow", "standard", "deep"]
    tone: Literal["formal", "casual", "technical"]
    focus_areas: List[str] = []
    exclude_areas: List[str] = []


class TemplateListResponse(BaseModel):
    """Response listing available templates."""
    templates: List[TestTemplate]
