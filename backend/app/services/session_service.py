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
    
    async def list_sessions(
        self, 
        limit: int = 50, 
        offset: int = 0,
        status_filter: Optional[str] = None,
        search_query: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        simple_format: bool = False
    ) -> Dict[str, Any]:
        """List sessions with filtering, searching, and pagination."""
        sessions = []
        
        try:
            # Load all sessions
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
            
            # Apply filters
            filtered_sessions = sessions
            
            # Status filter
            if status_filter:
                filtered_sessions = [s for s in filtered_sessions if s.status.value == status_filter]
            
            # Search query filter
            if search_query:
                query_lower = search_query.lower()
                filtered_sessions = [
                    s for s in filtered_sessions 
                    if (query_lower in s.session_id.lower() or
                        (s.original_filenames and any(
                            query_lower in filename.lower() 
                            for filename in s.original_filenames.values()
                        )) or
                        (s.error_message and query_lower in s.error_message.lower()))
                ]
            
            # Sort sessions
            reverse_order = sort_order.lower() == "desc"
            if sort_by == "created_at":
                filtered_sessions.sort(key=lambda s: s.created_at, reverse=reverse_order)
            elif sort_by == "updated_at":
                filtered_sessions.sort(key=lambda s: s.updated_at, reverse=reverse_order)
            elif sort_by == "status":
                filtered_sessions.sort(key=lambda s: s.status.value, reverse=reverse_order)
            
            # Calculate pagination
            total_count = len(filtered_sessions)
            total_pages = (total_count + limit - 1) // limit if limit > 0 else 1
            current_page = (offset // limit) + 1 if limit > 0 else 1
            
            # Apply pagination
            if limit > 0:
                paginated_sessions = filtered_sessions[offset:offset + limit]
            else:
                paginated_sessions = filtered_sessions
            
            logger.info(f"Listed {len(paginated_sessions)} sessions (total: {total_count})")
            
            # Return simple format for backward compatibility
            if simple_format or (not status_filter and not search_query):
                return paginated_sessions
            
            return {
                "sessions": paginated_sessions,
                "pagination": {
                    "total_count": total_count,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "page_size": limit,
                    "has_next": offset + limit < total_count,
                    "has_previous": offset > 0
                },
                "filters": {
                    "status_filter": status_filter,
                    "search_query": search_query,
                    "sort_by": sort_by,
                    "sort_order": sort_order
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            raise FileProcessingError(f"Failed to list sessions: {e}")
    
    async def get_session_statistics(self) -> Dict[str, Any]:
        """Get session statistics."""
        try:
            sessions = []
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
            
            # Calculate statistics
            total_sessions = len(sessions)
            status_counts = {}
            
            for session in sessions:
                status = session.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Calculate success rate
            completed_sessions = status_counts.get("completed", 0)
            success_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Recent activity (last 7 days)
            from datetime import datetime, timedelta
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_sessions = [s for s in sessions if s.created_at >= seven_days_ago]
            
            stats = {
                "total_sessions": total_sessions,
                "status_counts": status_counts,
                "success_rate": round(success_rate, 1),
                "recent_sessions_count": len(recent_sessions),
                "has_analysis_count": len([s for s in sessions if s.has_analysis()]),
                "has_optimization_count": len([s for s in sessions if s.has_optimization()])
            }
            
            logger.info(f"Generated session statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            raise FileProcessingError(f"Failed to get session statistics: {e}")
    
    async def bulk_delete_sessions(self, session_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple sessions."""
        results = {
            "deleted": [],
            "failed": [],
            "total": len(session_ids)
        }
        
        for session_id in session_ids:
            try:
                success = await self.delete_session(session_id)
                if success:
                    results["deleted"].append(session_id)
                else:
                    results["failed"].append({"session_id": session_id, "error": "Session not found"})
            except Exception as e:
                results["failed"].append({"session_id": session_id, "error": str(e)})
        
        logger.info(f"Bulk delete completed: {len(results['deleted'])} deleted, {len(results['failed'])} failed")
        return results
    
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
