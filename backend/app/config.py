"""
Application Configuration Module

Manages all configuration settings for the ContextOptimizer backend.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings configuration."""
    
    # Application Info
    app_name: str = Field(default="ContextOptimizer", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[Path] = Field(default=None, env="LOG_FILE")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    
    # File Storage Configuration
    base_data_dir: Path = Field(default=Path("./data"), env="DATA_DIR")
    upload_dir: Path = Field(default=Path("./data/uploads"), env="UPLOAD_DIR")
    session_dir: Path = Field(default=Path("./data/sessions"), env="SESSION_DIR")
    log_dir: Path = Field(default=Path("./logs"), env="LOG_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_base_url: Optional[str] = Field(default=None, env="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    max_tokens: int = Field(default=4000, env="MAX_TOKENS")
    temperature: float = Field(default=0.1, env="TEMPERATURE")
    
    # LLM Cache Configuration
    use_llm_cache: bool = Field(default=True, env="USE_LLM_CACHE")
    llm_cache_ttl: int = Field(default=3600, env="LLM_CACHE_TTL")  # 1 hour in seconds
    
    # CORS Configuration
    override_allowed_origins: bool = Field(default=False, env="OVERRIDE_ALLOWED_ORIGINS")
    allowed_origins_str: Optional[str] = Field(default=None, env="ALLOWED_ORIGINS")
    
    @property
    def allowed_origins(self) -> list[str]:
        """Get the list of allowed origins for CORS."""
        if self.override_allowed_origins:
            # In development mode, allow all origins
            return ["*"]
        elif self.allowed_origins_str:
            # Parse comma-separated string from env var if provided
            return [origin.strip() for origin in self.allowed_origins_str.split(',')]
        # Default origins
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000", 
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set default log file if not provided
        if self.log_file is None and self.log_dir:
            self.log_file = self.log_dir / "app.log"
        elif self.log_file and not self.log_file.is_absolute():
            self.log_file = Path(self.log_file).resolve()
        
        # Ensure directories exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return self.openai_api_key is not None and len(self.openai_api_key.strip()) > 0


# Global settings instance
settings = Settings()
