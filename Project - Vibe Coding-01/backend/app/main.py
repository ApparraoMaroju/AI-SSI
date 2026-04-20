"""Main FastAPI application."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import jira, testcases, templates, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Test Case Generator API",
    description="Generate structured test cases from Jira tickets using LLM",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(jira.router, prefix="/api/jira", tags=["Jira"])
app.include_router(testcases.router, prefix="/api/testcases", tags=["Test Cases"])
app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Test Case Generator API starting up...")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"LLM Model: {settings.llm_model}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Test Case Generator API shutting down...")
