"""
FastAPI Application Entry Point
Maps to: Problem Understanding - Define the overall purpose of the API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging

from app.config import get_settings
from app.database import init_db
from app.logging_config import setup_logging
from app.middleware import validation_exception_handler, general_exception_handler
from app.routers import auth, messages, conversations

# Setup logging
logger = setup_logging()

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    # Messaging API - Academic Project
    
    # A production-ready RESTful API for messaging functionality built with FastAPI.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers with API versioning
app.include_router(auth.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(conversations.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup
    Maps to: Deployment - Deployment Workflow (Using GitHub)
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Shutting down application")


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Health check
    Maps to: Hosting - Verify all endpoints are reachable
    """
    return {
        "message": "Messaging API",
        "version": settings.app_version,
        "status": "operational",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Maps to: Deployment - Check logs for errors
    """
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
