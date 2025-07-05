"""
Session management service.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..config import settings
from ..models.session import Session, SessionStatus
from ..utils.file_utils import FileUtils
from ..utils.exceptions import SessionNotFoundError, FileProcessingError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SessionService:
    """Service for managing analysis sessions."""
    
    def __init__(self):
        """Initialize session service."""
        self.session_dir = settings.session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_session(
        self,
        agents_config_content: bytes,
        agents_config_filename: str,
        messages_dataset_content: bytes,
        messages_dataset_filename: str
    ) -> Session:
        """Create a new session with uploaded files."""
        session_id = FileUtils.generate_session_id()
        
        # Create session
        session = Session(
            session_id=session_id
        )
        
        # Create session directory
        session_path = await FileUtils.ensure_session_dir(session_id, self.session_dir)
        
        try:
            # Save agents config file
            agents_config_path = session_path / "input"
            agents_config_path.mkdir(parents=True, exist_ok=True)
            agents_config_file = agents_config_path / "agents_config.json"
            await FileUtils.save_bytes_to_file(agents_config_content, agents_config_file)
            
            # Save messages dataset file
            messages_dataset_file = agents_config_path / "messages_dataset.json"
            await FileUtils.save_bytes_to_file(messages_dataset_content, messages_dataset_file)
            
            # Update session
            session.agents_config_filename = "input/agents_config.json"
            session.messages_dataset_filename = "input/messages_dataset.json"
            session.status = SessionStatus.UPLOADED
            session.original_filenames = {
                "agents_config": agents_config_filename,
                "messages_dataset": messages_dataset_filename
            }
            
            # Save session metadata
            await self._save_session(session)
            
            logger.info(f"Created new session with uploaded files: {session_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to create session with uploaded files: {e}")
            # Clean up session directory on failure
            await self.delete_session(session_id)
            raise FileProcessingError(f"Failed to create session: {e}")
    
    async def get_session(self, session_id: str) -> Session:
        """Get session by ID."""
        session_file = self._get_session_file_path(session_id)
        
        if not session_file.exists():
            raise SessionNotFoundError(f"Session not found: {session_id}")
        
        try:
            session_data = await FileUtils.load_json(session_file)
            session = Session(**session_data)
            logger.debug(f"Retrieved session: {session_id}")
            return session
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {e}")
            raise FileProcessingError(f"Failed to load session: {e}")
    
    async def update_session(self, session: Session) -> Session:
        """Update session."""
        session.updated_at = datetime.utcnow()
        await self._save_session(session)
        logger.debug(f"Updated session: {session.session_id}")
        return session
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete session and all associated files."""
        try:
            session_dir = FileUtils.get_session_dir(session_id, self.session_dir)
            
            if session_dir.exists():
                # Remove all files in session directory
                for file_path in session_dir.rglob("*"):
                    if file_path.is_file():
                        file_path.unlink()
                
                # Remove directory
                session_dir.rmdir()
                
                logger.info(f"Deleted session: {session_id}")
                return True
            else:
                logger.warning(f"Session directory not found: {session_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise FileProcessingError(f"Failed to delete session: {e}")
    
    async def list_sessions(self, limit: int = 50) -> List[Session]:
        """List all sessions."""
        sessions = []
        
        try:
            for session_dir in self.session_dir.iterdir():
                if session_dir.is_dir():
                    session_file = session_dir / "session.json"
                    if session_file.exists():
                        try:
                            session_data = await FileUtils.load_json(session_file)
                            session = Session(**session_data)
                            sessions.append(session)
                        except Exception as e:
                            logger.warning(f"Failed to load session from {session_dir}: {e}")
            
            # Sort by creation time (newest first)
            sessions.sort(key=lambda s: s.created_at, reverse=True)
            
            # Apply limit
            if limit > 0:
                sessions = sessions[:limit]
            
            logger.info(f"Listed {len(sessions)} sessions")
            return sessions
            
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            raise FileProcessingError(f"Failed to list sessions: {e}")
    
    async def get_session_file_path(self, session_id: str, filename: str) -> Path:
        """Get path to session file."""
        session_dir = FileUtils.get_session_dir(session_id, self.session_dir)
        return session_dir / filename
    
    def _get_session_file_path(self, session_id: str) -> Path:
        """Get path to session metadata file."""
        session_dir = FileUtils.get_session_dir(session_id, self.session_dir)
        return session_dir / "session.json"
    
    async def _save_session(self, session: Session) -> None:
        """Save session metadata to file."""
        session_file = self._get_session_file_path(session.session_id)
        # Convert to dict and handle datetime serialization
        session_data = session.model_dump()
        await FileUtils.save_json(session_data, session_file)
