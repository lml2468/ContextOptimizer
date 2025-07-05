"""
Application-specific exceptions.
"""

from typing import Optional, Dict, Any


class ContextOptimizerException(Exception):
    """Base exception for ContextOptimizer application."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None, error_code: str = "generic_error"):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.error_code = error_code
    
    def __str__(self):
        return self.message


class ValidationError(ContextOptimizerException):
    """Exception raised for data validation errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "validation_error")


class FileProcessingError(ContextOptimizerException):
    """Exception raised for file processing errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "file_processing_error")


class LLMServiceError(ContextOptimizerException):
    """Exception raised for LLM service errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "llm_service_error")


class SessionNotFoundError(ContextOptimizerException):
    """Exception raised when a session is not found."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "session_not_found")


class ConfigurationError(ContextOptimizerException):
    """Exception raised for configuration errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "configuration_error")


class RateLimitError(ContextOptimizerException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "rate_limit_error")


class DataConsistencyError(ContextOptimizerException):
    """Exception raised for data consistency issues."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "data_consistency_error")


class AnalysisError(ContextOptimizerException):
    """Exception raised for analysis errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "analysis_error")


class OptimizationError(ContextOptimizerException):
    """Exception raised for optimization errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "optimization_error")


class TimeoutError(ContextOptimizerException):
    """Exception raised when an operation times out."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, "timeout_error")
