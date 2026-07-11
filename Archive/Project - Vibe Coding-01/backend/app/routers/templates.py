"""Templates API router."""

import os
import logging
from pathlib import Path
from typing import List
import yaml
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.schemas import TestTemplate, TemplateListResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Templates directory
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


def load_templates() -> List[TestTemplate]:
    """Load all YAML templates from templates directory."""
    templates = []
    
    if not TEMPLATES_DIR.exists():
        logger.warning(f"Templates directory not found: {TEMPLATES_DIR}")
        return templates
    
    for file_path in TEMPLATES_DIR.glob("*.yaml"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                template = TestTemplate(**data)
                templates.append(template)
                logger.debug(f"Loaded template: {template.name}")
        except Exception as e:
            logger.error(f"Error loading template {file_path}: {e}")
    
    return templates


@router.get("/", response_model=TemplateListResponse)
async def list_templates() -> TemplateListResponse:
    """List all available test templates."""
    templates = load_templates()
    return TemplateListResponse(templates=templates)


@router.get("/{template_name}")
async def get_template(template_name: str):
    """Get a specific template by name."""
    templates = load_templates()
    
    for template in templates:
        if template.name.lower() == template_name.lower():
            return template
    
    raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")


@router.post("/upload")
async def upload_custom_template(file: UploadFile = File(...)):
    """
    Upload a custom YAML template.
    
    The template must conform to the TestTemplate schema.
    """
    if not file.filename.endswith(('.yaml', '.yml')):
        raise HTTPException(status_code=400, detail="File must be a YAML file")
    
    try:
        content = await file.read()
        data = yaml.safe_load(content.decode('utf-8'))
        
        # Validate template structure
        template = TestTemplate(**data)
        
        return {
            "success": True,
            "message": f"Template '{template.name}' validated successfully",
            "template": template
        }
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid template structure: {str(e)}")
