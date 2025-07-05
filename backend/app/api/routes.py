"""
API routes for ContextOptimizer backend.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, Body, BackgroundTasks
from fastapi.responses import JSONResponse

from ..config import settings
from ..models.schemas import (
    UploadResponse, AnalysisRequest, SessionInfo, ErrorResponse,
    EvaluationReport, OptimizationResult, AnalysisResult, OptimizationRequest,
    FileInfo, HealthResponse
)
from ..services.session_service import SessionService
from ..services.file_service import FileService
from ..services.llm_service import LLMService
from ..core.evaluator import ContextEvaluator
from ..core.optimizer import ContextOptimizer
from ..utils.exceptions import (
    ValidationError, FileProcessingError, SessionNotFoundError, 
    LLMServiceError, ConfigurationError
)
from ..utils.logger import get_logger
from ..utils.file_utils import FileUtils
from ..models.schemas import SessionStatus

logger = get_logger(__name__)

# Initialize services
session_service = SessionService()
llm_service = LLMService()
evaluator = ContextEvaluator(llm_service)
optimizer = ContextOptimizer(llm_service)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status information about the API.
    
    Example response:
    ```json
    {
        "status": "ok",
        "version": "1.0.0",
        "environment": "production"
    }
    ```
    """
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production"
    }


@router.post("/upload", response_model=SessionInfo, tags=["upload"], summary="Upload agent configuration and message data files", description="Upload agent configuration and message data files to create a new analysis session.")
async def upload_files(
    agents_config: UploadFile = File(..., description="Agent configuration JSON file"),
    messages_dataset: UploadFile = File(..., description="Messages dataset JSON file"),

):
    """
    Upload agent configuration and message data files.
    
    Args:
        agents_config: Agent configuration JSON file
        messages_dataset: Messages dataset JSON file
    
    Returns:
        Session information including session ID
    
    Raises:
        400: Invalid file format or content
        500: Server error
    
    Example response:
    ```json
    {
        "session_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_at": "2023-04-01T12:34:56.789Z",
        "files": {
            "agents_config": {
                "filename": "agents_config.json",
                "size_bytes": 1024,
                "size_human": "1.0 KB"
            },
            "messages_dataset": {
                "filename": "messages_dataset.json",
                "size_bytes": 2048,
                "size_human": "2.0 KB"
            }
        },
        "status": "created"
    }
    ```
    """
    try:
        logger.info(f"Uploading files: {agents_config.filename}, {messages_dataset.filename}")
        
        # Validate file types and sizes
        agents_config_content = await agents_config.read()
        await FileService.validate_uploaded_file(
            agents_config_content,
            agents_config.filename,
            settings.max_file_size
        )
        
        messages_dataset_content = await messages_dataset.read()
        await FileService.validate_uploaded_file(
            messages_dataset_content,
            messages_dataset.filename,
            settings.max_file_size
        )
        
        # Create new session with uploaded files
        session = await session_service.create_session(
            agents_config_content=agents_config_content,
            agents_config_filename=agents_config.filename,
            messages_dataset_content=messages_dataset_content,
            messages_dataset_filename=messages_dataset.filename
        )
        
        # Get file info for response
        file_info = {
            "agents_config": FileInfo(**FileService.get_file_info(agents_config_content, agents_config.filename)),
            "messages_dataset": FileInfo(**FileService.get_file_info(messages_dataset_content, messages_dataset.filename))
        }
        
        logger.info(f"Files uploaded successfully for session: {session.session_id}")
        
        # Return session info with file details
        return {
            "session_id": session.session_id,
            "status": session.status,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "files": file_info,
            "has_files": session.has_files(),
            "has_analysis": session.has_analysis(),
            "has_optimization": session.has_optimization()
        }
        
    except ValidationError as e:
        logger.error(f"File validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except FileProcessingError as e:
        logger.error(f"File processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")


@router.post("/analyze", response_model=dict)
async def analyze_context(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Start context analysis for a session."""
    try:
        logger.info(f"🚀 Analysis request received for session: {request.session_id}")
        logger.debug(f"📋 Request details: {request}")
        
        # Get session
        logger.debug(f"📋 Retrieving session: {request.session_id}")
        session = await session_service.get_session(request.session_id)
        logger.debug(f"📊 Session status: {session.status}, has_files: {session.has_files()}, has_analysis: {session.has_analysis()}")
        
        if not session.has_files():
            logger.warning(f"❌ Session files not uploaded for: {request.session_id}")
            raise HTTPException(status_code=400, detail="Session files not uploaded")
        
        # Check if analysis is already in progress or completed
        if session.status == SessionStatus.ANALYZING:
            logger.info(f"⏳ Analysis already in progress for session: {request.session_id}")
            return {
                "session_id": request.session_id,
                "status": "processing",
                "message": "Analysis already in progress",
                "estimated_time": "2-5 minutes"
            }
        
        if session.has_analysis() and session.status != SessionStatus.ERROR:
            logger.info(f"✅ Analysis already completed for session: {request.session_id}")
            return {
                "session_id": request.session_id,
                "status": "completed",
                "message": "Analysis already completed",
                "has_evaluation_report": True,
                "has_optimization_result": session.has_optimization()
            }
        
        # Update session status
        logger.debug(f"🔄 Updating session status to ANALYZING for: {request.session_id}")
        session.update_status(SessionStatus.ANALYZING, "Analysis started")
        await session_service.update_session(session)
        
        # Start background analysis
        logger.info(f"🎬 Starting background analysis task for session: {request.session_id}")
        background_tasks.add_task(
            _perform_analysis,
            request.session_id
        )
        
        logger.info(f"✅ Analysis started successfully for session: {request.session_id}")
        return {
            "session_id": request.session_id,
            "status": "processing",
            "message": "Analysis started",
            "estimated_time": "2-5 minutes"
        }
        
    except SessionNotFoundError as e:
        logger.error(f"❌ Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"💥 Analysis start failed: {e}")
        import traceback
        logger.error(f"🔍 Analysis start error traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Analysis start failed")


@router.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """Get session information and status."""
    try:
        session = await session_service.get_session(session_id)
        
        return SessionInfo(
            session_id=session.session_id,
            status=session.status,
            created_at=session.created_at,
            updated_at=session.updated_at,
            has_files=session.has_files(),
            has_analysis=session.has_analysis(),
            has_optimization=session.has_optimization(),
            error_message=session.error_message
        )
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get session failed: {e}")
        raise HTTPException(status_code=500, detail="Get session failed")


@router.get("/session/{session_id}/evaluation", response_model=dict)
async def get_evaluation_report(session_id: str):
    """Get evaluation report for a session."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.evaluation_report:
            raise HTTPException(status_code=404, detail="Evaluation report not found")
        
        return session.evaluation_report
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get evaluation report failed: {e}")
        raise HTTPException(status_code=500, detail="Get evaluation report failed")


@router.get("/session/{session_id}/optimization", response_model=dict)
async def get_optimization_result(session_id: str):
    """Get optimization result for a session."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.optimization_result:
            raise HTTPException(status_code=404, detail="Optimization result not found")
        
        return session.optimization_result
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get optimization result failed: {e}")
        raise HTTPException(status_code=500, detail="Get optimization result failed")


# Frontend compatibility endpoints
@router.get("/analysis/{session_id}", response_model=dict)
async def get_analysis_report(session_id: str):
    """Get analysis report for a session (frontend compatibility endpoint)."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.evaluation_report:
            raise HTTPException(status_code=404, detail="Analysis report not found")
        
        return session.evaluation_report
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get analysis report failed: {e}")
        raise HTTPException(status_code=500, detail="Get analysis report failed")


@router.get("/optimization/{session_id}", response_model=dict)
async def get_optimization_report(session_id: str):
    """Get optimization report for a session (frontend compatibility endpoint)."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.optimization_result:
            raise HTTPException(status_code=404, detail="Optimization result not found")
        
        return session.optimization_result
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Get optimization report failed: {e}")
        raise HTTPException(status_code=500, detail="Get optimization report failed")


@router.post("/optimize/{session_id}", response_model=dict)
async def start_optimization(
    session_id: str,
    optimization_level: str = Body("balanced", description="Optimization level"),
    focus_areas: List[str] = Body(default_factory=list, description="Focus areas")
):
    """Start optimization for a session (frontend compatibility endpoint)."""
    try:
        logger.info(f"Starting optimization for session: {session_id}")
        
        # Get session
        session = await session_service.get_session(session_id)
        
        if not session.evaluation_report:
            raise HTTPException(status_code=400, detail="Analysis must be completed before optimization")
        
        # Check if optimization is already completed
        if session.optimization_result:
            logger.info(f"Optimization already completed for session: {session_id}")
            return session.optimization_result
        
        # Get agents config and evaluation report
        session_dir = session_service.session_dir / session_id
        agents_config, _ = await FileService.process_session_files(
            session_dir,
            session.agents_config_filename,
            session.messages_dataset_filename
        )
        
        # Perform optimization
        logger.info(f"Starting context optimization for session: {session_id}")
        optimization_result = await optimizer.optimize_context(
            agents_config, session.evaluation_report
        )
        logger.info("Context optimization completed successfully")
        
        # Add timestamp
        optimization_result["metadata"]["optimization_timestamp"] = datetime.utcnow().isoformat()
        
        # Save optimization result
        analysis_dir = session_dir / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        optimization_file = analysis_dir / "optimization_result.json"
        await FileUtils.save_json(optimization_result, optimization_file)
        
        # Update session
        session.optimization_result = optimization_result
        session.update_status(SessionStatus.COMPLETED)
        await session_service.update_session(session)
        
        logger.info(f"Optimization completed successfully for session: {session_id}")
        return optimization_result
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Start optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Start optimization failed")


@router.get("/sessions", response_model=List[SessionInfo], tags=["sessions"], summary="List all sessions", description="Get a list of all analysis sessions.")
async def list_sessions(
    limit: int = Query(10, description="Maximum number of sessions to return"),
    offset: int = Query(0, description="Number of sessions to skip")
):
    """
    List all analysis sessions.
    
    Args:
        limit: Maximum number of sessions to return
        offset: Number of sessions to skip
    
    Returns:
        List of session information
    
    Example response:
    ```json
    [
        {
            "session_id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2023-04-01T12:34:56.789Z",
            "files": {
                "agents_config": {
                    "filename": "agents_config.json",
                    "size_bytes": 1024,
                    "size_human": "1.0 KB"
                },
                "messages_dataset": {
                    "filename": "messages_dataset.json",
                    "size_bytes": 2048,
                    "size_human": "2.0 KB"
                }
            },
            "status": "analyzed"
        }
    ]
    ```
    """
    try:
        sessions = await session_service.list_sessions(limit, offset)
        
        return [
            SessionInfo(
                session_id=session.session_id,
                status=session.status,
                created_at=session.created_at,
                updated_at=session.updated_at,
                has_files=session.has_files(),
                has_analysis=session.has_analysis(),
                has_optimization=session.has_optimization(),
                error_message=session.error_message
            )
            for session in sessions
        ]
        
    except Exception as e:
        logger.error(f"List sessions failed: {e}")
        raise HTTPException(status_code=500, detail="List sessions failed")


@router.delete("/session/{session_id}", response_model=Dict[str, Any], tags=["sessions"], summary="Delete a session", description="Delete a session and all associated data.")
async def delete_session(session_id: str):
    """
    Delete a session and all associated data.
    
    Args:
        session_id: Session ID
    
    Returns:
        Deletion confirmation
    
    Raises:
        404: Session not found
    
    Example response:
    ```json
    {
        "success": true,
        "message": "Session deleted successfully",
        "session_id": "550e8400-e29b-41d4-a716-446655440000"
    }
    ```
    """
    try:
        success = await session_service.delete_session(session_id)
        
        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
    except Exception as e:
        logger.error(f"Delete session failed: {e}")
        raise HTTPException(status_code=500, detail="Delete session failed")


@router.get("/sessions/{session_id}/evaluation/download")
async def download_evaluation_report(session_id: str):
    """Download evaluation report as JSON file."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.evaluation_report:
            raise HTTPException(status_code=404, detail="Evaluation report not found")
        
        # Create JSON response for download
        from fastapi.responses import Response
        import json
        
        json_content = json.dumps(session.evaluation_report, indent=2, ensure_ascii=False)
        
        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=evaluation_report_{session_id}.json"
            }
        )
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Download evaluation report failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")


@router.get("/sessions/{session_id}/optimization/download")
async def download_optimization_result(session_id: str):
    """Download optimization result as JSON file."""
    try:
        session = await session_service.get_session(session_id)
        
        if not session.optimization_result:
            raise HTTPException(status_code=404, detail="Optimization result not found")
        
        # Create JSON response for download
        from fastapi.responses import Response
        import json
        
        json_content = json.dumps(session.optimization_result, indent=2, ensure_ascii=False)
        
        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=optimization_result_{session_id}.json"
            }
        )
        
    except SessionNotFoundError as e:
        logger.error(f"Session not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Download optimization result failed: {e}")
        raise HTTPException(status_code=500, detail="Download failed")


async def _perform_analysis(session_id: str):
    """Perform context analysis in background."""
    try:
        logger.info(f"Starting analysis for session: {session_id}")
        
        # Get session
        session = await session_service.get_session(session_id)
        session_dir = session_service.session_dir / session_id
        
        # Process session files
        agents_config, messages_dataset = await FileService.process_session_files(
            session_dir,
            session.agents_config_filename,
            session.messages_dataset_filename
        )
        
        # Update session status
        session.update_status(SessionStatus.ANALYZING)
        await session_service.update_session(session)
        
        # Perform evaluation
        logger.info(f"Starting context evaluation for session: {session_id}")
        evaluation_report = await evaluator.evaluate_context(
            agents_config, messages_dataset
        )
        logger.info("Context evaluation completed successfully")
        
        # Add timestamp
        evaluation_report["metadata"]["analysis_timestamp"] = datetime.utcnow().isoformat()
        
        # Create analysis directory
        analysis_dir = session_dir / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Save evaluation report
        evaluation_file = analysis_dir / "evaluation_report.json"
        await FileUtils.save_json(evaluation_report, evaluation_file)
        
        # Update session status
        session.update_status(SessionStatus.ANALYZED)
        session.evaluation_report = evaluation_report
        await session_service.update_session(session)
        
        # Perform optimization
        logger.info(f"Starting context optimization for session: {session_id}")
        optimization_result = await optimizer.optimize_context(
            agents_config, evaluation_report
        )
        logger.info("Context optimization completed successfully")
        
        # Add timestamp
        optimization_result["metadata"]["optimization_timestamp"] = datetime.utcnow().isoformat()
        
        # Save optimization result
        optimization_file = analysis_dir / "optimization_result.json"
        await FileUtils.save_json(optimization_result, optimization_file)
        
        # Update session
        session.optimization_result = optimization_result
        session.update_status(SessionStatus.COMPLETED)
        await session_service.update_session(session)
        
        logger.info(f"Analysis completed successfully for session: {session_id}")
        
    except Exception as e:
        logger.error(f"Analysis failed for session {session_id}: {e}")
        
        # Update session with error
        try:
            session = await session_service.get_session(session_id)
            session.update_status(SessionStatus.ERROR, str(e))
            await session_service.update_session(session)
        except Exception as update_error:
            logger.error(f"Failed to update session error status: {update_error}")



