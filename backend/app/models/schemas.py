"""
API request/response schemas.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from .session import SessionStatus


class UploadRequest(BaseModel):
    """Request model for file upload."""
    
    session_id: Optional[str] = Field(default=None, description="Existing session ID")


class UploadResponse(BaseModel):
    """Response model for file upload."""
    
    session_id: str = Field(..., description="Session ID")
    status: SessionStatus = Field(..., description="Session status")
    message: str = Field(..., description="Response message")
    uploaded_files: List[str] = Field(default_factory=list, description="List of uploaded filenames")


class AnalysisRequest(BaseModel):
    """Request model for analysis."""
    
    session_id: str = Field(..., description="Session ID")


class EvaluationDimension(BaseModel):
    """Model for evaluation dimension."""
    
    name: str = Field(..., description="Dimension name")
    score: float = Field(..., ge=0, le=10, description="Score from 0 to 10")
    description: str = Field(..., description="Dimension description")
    issues: List[str] = Field(default_factory=list, description="Identified issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


class PriorityIssue(BaseModel):
    """Model for priority issue."""
    
    priority: str = Field(..., description="Priority level: high, medium, low")
    category: str = Field(..., description="Issue category")
    description: str = Field(..., description="Issue description")
    impact: str = Field(..., description="Impact description")
    solution: str = Field(..., description="Recommended solution")
    affected_agents: List[str] = Field(default_factory=list, description="Affected agent IDs")


class EvaluationReport(BaseModel):
    """Model for evaluation report."""
    
    session_id: str = Field(..., description="Session ID")
    overall_score: float = Field(..., ge=0, le=10, description="Overall score")
    dimensions: List[EvaluationDimension] = Field(..., description="Evaluation dimensions")
    priority_issues: List[PriorityIssue] = Field(default_factory=list, description="Priority issues")
    summary: str = Field(..., description="Executive summary")
    recommendations: List[str] = Field(default_factory=list, description="Overall recommendations")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")


class OptimizedAgent(BaseModel):
    """Model for optimized agent configuration."""
    
    agent_id: str = Field(..., description="Agent ID")
    agent_name: str = Field(..., description="Agent name")
    original_system_prompt: str = Field(..., description="Original system prompt")
    optimized_system_prompt: str = Field(..., description="Optimized system prompt")
    changes_summary: str = Field(..., description="Summary of changes made")
    tools: List[Dict[str, Any]] = Field(default_factory=list, description="Tool configurations")


class ToolFormatRecommendation(BaseModel):
    """Model for tool format recommendation."""
    
    tool_name: str = Field(..., description="Tool name")
    current_format: Optional[str] = Field(default=None, description="Current format description")
    recommended_format: str = Field(..., description="Recommended format")
    format_example: Dict[str, Any] = Field(..., description="Format example")
    rationale: str = Field(..., description="Rationale for recommendation")


class OptimizationResult(BaseModel):
    """Model for optimization result."""
    
    session_id: str = Field(..., description="Session ID")
    optimized_agents: List[OptimizedAgent] = Field(..., description="Optimized agent configurations")
    tool_format_recommendations: List[ToolFormatRecommendation] = Field(
        default_factory=list, description="Tool format recommendations"
    )
    implementation_guide: str = Field(..., description="Implementation guide")
    expected_improvements: List[str] = Field(default_factory=list, description="Expected improvements")
    compatibility_notes: List[str] = Field(default_factory=list, description="Compatibility notes")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")


class AnalysisResponse(BaseModel):
    """Response model for analysis."""
    
    session_id: str = Field(..., description="Session ID")
    status: SessionStatus = Field(..., description="Session status")
    evaluation_report: Optional[EvaluationReport] = Field(default=None, description="Evaluation report")
    optimization_result: Optional[OptimizationResult] = Field(default=None, description="Optimization result")
    message: str = Field(..., description="Response message")


class FileInfo(BaseModel):
    """File information model."""
    
    filename: str = Field(..., description="File name")
    size_bytes: int = Field(..., description="File size in bytes")
    size_human: str = Field(..., description="Human-readable file size")
    is_json: bool = Field(..., description="Whether the file is a JSON file")


class SessionInfo(BaseModel):
    """Model for session information."""
    
    session_id: str = Field(..., description="Session ID")
    status: SessionStatus = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    has_files: bool = Field(..., description="Whether files are uploaded")
    has_analysis: bool = Field(..., description="Whether analysis is completed")
    has_optimization: bool = Field(..., description="Whether optimization is completed")
    files: Optional[Dict[str, FileInfo]] = Field(default=None, description="File information")
    error_message: Optional[str] = Field(default=None, description="Error message if any")


class ErrorResponse(BaseModel):
    """Model for error response."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Error details")
    session_id: Optional[str] = Field(default=None, description="Session ID if applicable")


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment (development/production)")


class AnalysisResult(BaseModel):
    """Model for analysis result."""
    
    session_id: str = Field(..., description="Session ID")
    status: str = Field(..., description="Analysis status")
    message: str = Field(..., description="Result message")
    completed_at: datetime = Field(default_factory=datetime.utcnow, description="Completion timestamp")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional details")


class OptimizationRequest(BaseModel):
    """Request model for optimization."""
    
    session_id: str = Field(..., description="Session ID")
    optimization_level: str = Field(default="standard", description="Optimization level: basic or advanced")
    focus_areas: List[str] = Field(default_factory=list, description="Areas to focus optimization on")
