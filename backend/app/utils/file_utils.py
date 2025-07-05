"""
File handling utilities.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import aiofiles

from .exceptions import FileProcessingError, ValidationError
from .logger import get_logger

logger = get_logger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    async def save_json(data: Dict[str, Any], file_path: Path) -> None:
        """Save data as JSON file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=2, ensure_ascii=False, cls=DateTimeEncoder))
            logger.info(f"Saved JSON file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save JSON file {file_path}: {e}")
            raise FileProcessingError(f"Failed to save JSON file: {e}")
    
    @staticmethod
    async def load_json(file_path: Path) -> Dict[str, Any]:
        """Load JSON file."""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
            
            logger.info(f"Loaded JSON file: {file_path}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {e}")
            raise ValidationError(f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"Failed to load JSON file {file_path}: {e}")
            raise FileProcessingError(f"Failed to load JSON file: {e}")
    
    @staticmethod
    async def save_uploaded_file(
        file_content: bytes, 
        filename: str, 
        upload_dir: Path
    ) -> Path:
        """Save uploaded file to disk."""
        try:
            # Ensure upload directory exists
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename to avoid conflicts
            file_path = upload_dir / filename
            if file_path.exists():
                name_parts = filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    name, ext = name_parts
                    unique_filename = f"{name}_{uuid.uuid4().hex[:8]}.{ext}"
                else:
                    unique_filename = f"{filename}_{uuid.uuid4().hex[:8]}"
                file_path = upload_dir / unique_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
            
            logger.info(f"Saved uploaded file: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to save uploaded file {filename}: {e}")
            raise FileProcessingError(f"Failed to save uploaded file: {e}")
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any], required_keys: list) -> bool:
        """Validate JSON structure has required keys."""
        try:
            for key in required_keys:
                if key not in data:
                    raise ValidationError(f"Missing required key: {key}")
            return True
        except Exception as e:
            logger.error(f"JSON structure validation failed: {e}")
            raise
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_session_dir(session_id: str, base_dir: Path) -> Path:
        """Get session directory path."""
        return base_dir / session_id
    
    @staticmethod
    async def ensure_session_dir(session_id: str, base_dir: Path) -> Path:
        """Ensure session directory exists."""
        session_dir = FileUtils.get_session_dir(session_id, base_dir)
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir
    
    @staticmethod
    def is_valid_json_file(filename: str) -> bool:
        """Check if filename has valid JSON extension."""
        return filename.lower().endswith('.json')
    
    @staticmethod
    def get_file_size(file_path: Path) -> int:
        """Get file size in bytes."""
        return file_path.stat().st_size if file_path.exists() else 0
    
    @staticmethod
    async def save_bytes_to_file(content: bytes, file_path: Path) -> None:
        """Save bytes content to file."""
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            logger.info(f"Saved file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save file {file_path}: {e}")
            raise FileProcessingError(f"Failed to save file: {e}")
