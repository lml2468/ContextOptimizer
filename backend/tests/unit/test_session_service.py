"""
Unit tests for session service.
"""

import pytest
import json
import uuid
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.session_service import SessionService
from app.utils.exceptions import (
    SessionNotFoundError,
    FileProcessingError,
    ValidationError
)


class TestSessionService:
    """Tests for SessionService class."""
    
    @pytest.fixture
    def session_service(self, test_session_dir, test_upload_dir, mock_llm_service):
        """Create a session service for testing."""
        return SessionService()
    
    @pytest.mark.asyncio
    async def test_create_session(self, session_service):
        """Test creating a new session."""
        # Create session
        session_id = await session_service.create_session()
        
        # Verify session ID format
        assert isinstance(session_id, str)
        try:
            uuid.UUID(session_id)
        except ValueError:
            pytest.fail("Session ID is not a valid UUID")
        
        # Verify session directory was created
        session_dir = Path(session_service.session_dir) / session_id
        assert session_dir.exists()
        assert session_dir.is_dir()
        
        # Verify session metadata file was created
        metadata_file = session_dir / "metadata.json"
        assert metadata_file.exists()
        
        # Verify metadata content
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        assert metadata["session_id"] == session_id
        assert "created_at" in metadata
        assert "status" in metadata
