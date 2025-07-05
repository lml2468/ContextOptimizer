"""
File processing service.
"""

from pathlib import Path
from typing import Tuple

from ..models.agent import AgentConfig
from ..models.message import MessageDataset
from ..utils.file_utils import FileUtils
from ..utils.validation import ValidationUtils
from ..utils.exceptions import FileProcessingError, ValidationError
from ..utils.logger import get_logger

logger = get_logger()


class FileService:
    """Service for file processing and validation."""
    
    @staticmethod
    async def process_session_files(
        session_dir: Path,
        agents_config_filename: str,
        messages_dataset_filename: str
    ) -> Tuple[AgentConfig, MessageDataset]:
        """Process and validate session files."""
        try:
            logger.info(f"Processing session files in: {session_dir}")
            
            # Load agents config file
            agents_config_path = session_dir / agents_config_filename
            if not agents_config_path.exists():
                raise FileProcessingError(f"Agents config file not found: {agents_config_path}")
            
            agents_config_data = await FileUtils.load_json(agents_config_path)
            agents_config = ValidationUtils.validate_agents_config(agents_config_data)
            logger.info(f"Agents config validated - {len(agents_config.agents)} agents found")
            
            # Load messages dataset file
            messages_dataset_path = session_dir / messages_dataset_filename
            if not messages_dataset_path.exists():
                raise FileProcessingError(f"Messages dataset file not found: {messages_dataset_path}")
            
            messages_dataset_data = await FileUtils.load_json(messages_dataset_path)
            messages_dataset = ValidationUtils.validate_messages_dataset(messages_dataset_data)
            logger.info(f"Messages dataset validated - {len(messages_dataset.messages)} messages found")
            
            # Cross-validate files
            ValidationUtils.validate_session_files(agents_config, messages_dataset)
            
            logger.info("Session files processed successfully")
            return agents_config, messages_dataset
            
        except (FileProcessingError, ValidationError) as e:
            logger.error(f"File processing/validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to process session files: {e}")
            raise FileProcessingError(f"Failed to process session files: {e}")
    
    @staticmethod
    async def validate_uploaded_file(
        file_content: bytes,
        filename: str,
        max_size: int
    ) -> None:
        """Validate uploaded file."""
        try:
            # Check file extension
            if not FileUtils.is_valid_json_file(filename):
                raise ValidationError(f"Invalid file type. Only JSON files are allowed: {filename}")
            
            # Check file size
            file_size = len(file_content)
            ValidationUtils.validate_file_size(file_size, max_size)
            
            # Try to parse JSON content
            try:
                import json
                json.loads(file_content.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON content in file {filename}: {e}")
            except UnicodeDecodeError as e:
                raise ValidationError(f"Invalid file encoding in file {filename}: {e}")
            
            logger.debug(f"File validation passed: {filename}")
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to validate uploaded file {filename}: {e}")
            raise ValidationError(f"File validation failed: {e}")
    
    @staticmethod
    def get_file_info(file_content: bytes, filename: str) -> dict:
        """Get file information."""
        return {
            "filename": filename,
            "size_bytes": len(file_content),
            "size_human": FileService._format_file_size(len(file_content)),
            "is_json": FileUtils.is_valid_json_file(filename)
        }
    
    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
