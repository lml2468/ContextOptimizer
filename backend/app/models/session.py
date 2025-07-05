"""
Session-related data models.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class SessionStatus(str, Enum):
    """Session status enumeration."""
    CREATED = "created"
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    OPTIMIZING = "optimizing"
    COMPLETED = "completed"
    ERROR = "error"


class Session(BaseModel):
    """Model for analysis session."""
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
    
    session_id: str = Field(..., description="Unique session identifier")
    status: SessionStatus = Field(default=SessionStatus.CREATED, description="Session status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # File information
    agents_config_filename: Optional[str] = Field(default=None, description="Agents config filename")
    messages_dataset_filename: Optional[str] = Field(default=None, description="Messages dataset filename")
    original_filenames: Optional[Dict[str, str]] = Field(default_factory=dict, description="Original filenames")
    

    
    # Analysis results
    evaluation_report: Optional[Dict[str, Any]] = Field(default=None, description="Evaluation report")
    optimization_result: Optional[Dict[str, Any]] = Field(default=None, description="Optimization result")
    
    # Error information
    error_message: Optional[str] = Field(default=None, description="Error message if any")
    error_details: Optional[Dict[str, Any]] = Field(default=None, description="Detailed error information")
    
    # Metadata
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    
    def update_status(self, status: SessionStatus, error_message: Optional[str] = None):
        """Update session status and timestamp."""
        self.status = status
        self.updated_at = datetime.utcnow()
        if error_message:
            self.error_message = error_message
            if status != SessionStatus.ERROR:
                self.status = SessionStatus.ERROR
    
    def is_completed(self) -> bool:
        """Check if session is completed."""
        return self.status == SessionStatus.COMPLETED
    
    def is_error(self) -> bool:
        """Check if session has error."""
        return self.status == SessionStatus.ERROR
    
    def has_files(self) -> bool:
        """Check if session has uploaded files."""
        return (self.agents_config_filename is not None and 
                self.messages_dataset_filename is not None)
    
    def has_analysis(self) -> bool:
        """Check if session has analysis results."""
        return self.evaluation_report is not None
    
    def has_optimization(self) -> bool:
        """Check if session has optimization results."""
        return self.optimization_result is not None
