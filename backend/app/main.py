"""
ContextOptimizer FastAPI application.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from .config import settings
from .api.routes import router
from .utils.logger import setup_logger, get_logger
from .utils.exceptions import (
    ContextOptimizerException, 
    ValidationError, 
    FileProcessingError,
    LLMServiceError,
    SessionNotFoundError,
    ConfigurationError,
    RateLimitError,
    DataConsistencyError,
    AnalysisError,
    OptimizationError,
    TimeoutError
)

# Setup logging
logger = get_logger()

# Create FastAPI app
app = FastAPI(
    title="ContextOptimizer API",
    description="""
    # ContextOptimizer API

    Intelligent context engineering assistant for Multi-Agent Systems.
    
    ## Overview
    
    ContextOptimizer helps you analyze and optimize your multi-agent system's context flow
    by evaluating your agent configurations and conversation data, then providing actionable
    recommendations to improve system performance.
    
    ## Key Features
    
    - **Context Logic Diagnosis**: Automatically identify context breakage issues
    - **Coordinated Optimization**: Optimize prompts and tool information together
    - **Actionable Solutions**: Get ready-to-use optimized configurations
    
    ## Workflow
    
    1. Upload agent configuration and message data files
    2. Analyze the data to identify issues
    3. Generate optimized configurations
    4. Apply the optimizations to your system
    
    ## Authentication
    
    This API currently does not require authentication.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoints"
        },
        {
            "name": "upload",
            "description": "File upload endpoints"
        },
        {
            "name": "analysis",
            "description": "Context analysis endpoints"
        },
        {
            "name": "sessions",
            "description": "Session management endpoints"
        },
        {
            "name": "optimization",
            "description": "Context optimization endpoints"
        }
    ],
    contact={
        "name": "ContextOptimizer Team",
        "url": "https://github.com/yourusername/ContextOptimizer",
        "email": "example@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting ContextOptimizer API")
    logger.info(f"App: {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Upload directory: {settings.upload_dir}")
    logger.info(f"Session directory: {settings.session_dir}")
    
    # Ensure directories exist
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.session_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("ContextOptimizer API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down ContextOptimizer API")


@app.get("/", tags=["health"])
async def root():
    """Root endpoint."""
    return {
        "name": "ContextOptimizer API",
        "version": "1.0.0",
        "description": "Intelligent context engineering assistant for Multi-Agent Systems",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )


@app.exception_handler(FileProcessingError)
async def file_processing_error_handler(request: Request, exc: FileProcessingError):
    """Handle file processing errors."""
    logger.error(f"File processing error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )


@app.exception_handler(SessionNotFoundError)
async def session_not_found_error_handler(request: Request, exc: SessionNotFoundError):
    """Handle session not found errors."""
    logger.warning(f"Session not found: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=404,
        content=exc.to_dict()
    )


@app.exception_handler(LLMServiceError)
async def llm_service_error_handler(request: Request, exc: LLMServiceError):
    """Handle LLM service errors."""
    logger.error(f"LLM service error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=502,
        content=exc.to_dict()
    )


@app.exception_handler(ConfigurationError)
async def configuration_error_handler(request: Request, exc: ConfigurationError):
    """Handle configuration errors."""
    logger.error(f"Configuration error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


@app.exception_handler(RateLimitError)
async def rate_limit_error_handler(request: Request, exc: RateLimitError):
    """Handle rate limit errors."""
    logger.warning(f"Rate limit exceeded: {exc.message}", exc_info=settings.debug)
    headers = {}
    if "retry_after" in exc.details:
        headers["Retry-After"] = str(exc.details["retry_after"])
    return JSONResponse(
        status_code=429,
        headers=headers,
        content=exc.to_dict()
    )


@app.exception_handler(DataConsistencyError)
async def data_consistency_error_handler(request: Request, exc: DataConsistencyError):
    """Handle data consistency errors."""
    logger.error(f"Data consistency error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=400,
        content=exc.to_dict()
    )


@app.exception_handler(AnalysisError)
async def analysis_error_handler(request: Request, exc: AnalysisError):
    """Handle analysis errors."""
    logger.error(f"Analysis error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


@app.exception_handler(OptimizationError)
async def optimization_error_handler(request: Request, exc: OptimizationError):
    """Handle optimization errors."""
    logger.error(f"Optimization error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


@app.exception_handler(TimeoutError)
async def timeout_error_handler(request: Request, exc: TimeoutError):
    """Handle timeout errors."""
    logger.error(f"Timeout error: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=504,
        content=exc.to_dict()
    )


@app.exception_handler(ContextOptimizerException)
async def context_optimizer_exception_handler(request: Request, exc: ContextOptimizerException):
    """Handle general ContextOptimizer exceptions."""
    logger.error(f"ContextOptimizer exception: {exc.message}", exc_info=settings.debug)
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An internal server error occurred",
            "details": {"type": str(type(exc).__name__)}
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
