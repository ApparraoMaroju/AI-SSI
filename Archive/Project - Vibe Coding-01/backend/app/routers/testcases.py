"""Test cases API router."""

import logging
from fastapi import APIRouter, HTTPException

from app.schemas import (
    TestCaseGenerateRequest,
    TestCaseGenerateResponse,
    ExportRequest,
    ExportResponse
)
from app.services.llm_service import LLMService
from app.services.export_service import ExportService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate", response_model=TestCaseGenerateResponse)
async def generate_test_cases(request: TestCaseGenerateRequest) -> TestCaseGenerateResponse:
    """
    Generate test cases from a Jira issue using LLM.
    
    The request must include:
    - Parsed Jira issue
    - Template type or custom template
    - Anthropic API key for LLM
    - Minimum number of test cases (default 5)
    """
    logger.info(f"Generating test cases for {request.issue.key} with template {request.template_type}")
    
    # Validate API key
    if not request.anthropic_api_key or not request.anthropic_api_key.strip():
        return TestCaseGenerateResponse(
            success=False,
            message="Anthropic API key is required",
            test_cases=[],
            generation_time_ms=0,
            tokens_used=0
        )
    
    # Validate issue has content
    if not request.issue.description and not request.issue.acceptance_criteria:
        logger.warning(f"Issue {request.issue.key} has no description or acceptance criteria")
    
    # Initialize LLM service
    llm_service = LLMService(request.anthropic_api_key.strip())
    
    # Generate test cases
    success, message, test_cases, generation_time_ms, tokens_used = await llm_service.generate_test_cases(
        issue=request.issue,
        template_type=request.template_type,
        custom_template=request.custom_template,
        min_cases=request.min_test_cases
    )
    
    return TestCaseGenerateResponse(
        success=success,
        message=message,
        test_cases=test_cases,
        generation_time_ms=generation_time_ms,
        tokens_used=tokens_used
    )


@router.post("/export", response_model=ExportResponse)
async def export_test_cases(request: ExportRequest) -> ExportResponse:
    """
    Export test cases to specified format (Markdown, CSV, or TSV).
    
    TSV format is optimized for direct paste into Jira, Xray, or TestRail.
    """
    logger.info(f"Exporting {len(request.test_cases)} test cases to {request.format}")
    
    if not request.test_cases:
        return ExportResponse(
            success=False,
            content="",
            filename="",
            content_type=""
        )
    
    try:
        content, filename, content_type = ExportService.export(
            test_cases=request.test_cases,
            format=request.format,
            include_header=request.include_header
        )
        
        return ExportResponse(
            success=True,
            content=content,
            filename=filename,
            content_type=content_type
        )
    except Exception as e:
        logger.exception("Error exporting test cases")
        return ExportResponse(
            success=False,
            content=str(e),
            filename="",
            content_type=""
        )
