"""
Integration tests for API endpoints.
"""

import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app


class TestAPIEndpoints:
    """Tests for API endpoints."""
    
    def test_health_check(self, test_client):
        """Test health check endpoint."""
        response = test_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "health_check" in data
    
    def test_list_sessions_empty(self, test_client, test_session_dir):
        """Test listing sessions when none exist."""
        response = test_client.get("/api/v1/sessions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_upload_files(self, test_client, test_data_dir):
        """Test uploading files."""
        # Prepare test files
        agents_config_path = test_data_dir / "agents_config.json"
        messages_dataset_path = test_data_dir / "messages_dataset.json"
        
        with open(agents_config_path, "rb") as agents_file, \
             open(messages_dataset_path, "rb") as messages_file:
            
            files = {
                "agents_config": ("agents_config.json", agents_file, "application/json"),
                "messages_dataset": ("messages_dataset.json", messages_file, "application/json")
            }
            
            response = test_client.post("/api/v1/upload", files=files)
            assert response.status_code == 200
            
            result = response.json()
            assert "session_id" in result
            assert result["status"] == "uploaded"
            assert "files" in result
            assert "agents_config" in result["files"]
            assert "messages_dataset" in result["files"]
            
            # Store session ID for subsequent tests
            session_id = result["session_id"]
            return session_id
    
    def test_upload_invalid_file(self, test_client, temp_test_dir):
        """Test uploading invalid file."""
        # Create an invalid JSON file
        invalid_file_path = temp_test_dir / "invalid.json"
        with open(invalid_file_path, "w") as f:
            f.write("not valid json")
        
        # Create a valid JSON file
        valid_file_path = temp_test_dir / "valid.json"
        with open(valid_file_path, "w") as f:
            json.dump({"test": "data"}, f)
        
        with open(invalid_file_path, "rb") as invalid_file, \
             open(valid_file_path, "rb") as valid_file:
            
            files = {
                "agents_config": ("invalid.json", invalid_file, "application/json"),
                "messages_dataset": ("valid.json", valid_file, "application/json")
            }
            
            response = test_client.post("/api/v1/upload", files=files)
            assert response.status_code == 400
    
    def test_get_session(self, test_client):
        """Test getting session info."""
        # First upload files to create a session
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        
        # Get session info
        response = test_client.get(f"/api/v1/session/{session_id}")
        assert response.status_code == 200
        
        result = response.json()
        assert result["session_id"] == session_id
        assert "files" in result
        assert "created_at" in result
    
    def test_get_nonexistent_session(self, test_client):
        """Test getting nonexistent session."""
        response = test_client.get("/api/v1/session/nonexistent")
        assert response.status_code == 404
    
    def test_analyze_session(self, test_client):
        """Test analyzing a session."""
        # First upload files to create a session
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        
        # Analyze session
        request_data = {
            "focus_areas": ["prompt_clarity", "context_flow"]
        }
        
        response = test_client.post(
            f"/api/v1/analyze/{session_id}",
            json=request_data
        )
        
        assert response.status_code == 200
        
        result = response.json()
        assert result["session_id"] == session_id
        assert "overall_score" in result
        assert "dimensions" in result
        assert "priority_issues" in result
        assert "recommendations" in result
    
    def test_analyze_nonexistent_session(self, test_client):
        """Test analyzing nonexistent session."""
        request_data = {
            "focus_areas": ["prompt_clarity", "context_flow"]
        }
        
        response = test_client.post(
            "/api/v1/analyze/nonexistent",
            json=request_data
        )
        
        assert response.status_code == 404
    
    def test_get_analysis(self, test_client):
        """Test getting analysis results."""
        # First upload files and analyze
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        self.test_analyze_session(test_client)
        
        # Get analysis results
        response = test_client.get(f"/api/v1/analysis/{session_id}")
        assert response.status_code == 200
        
        result = response.json()
        assert result["session_id"] == session_id
        assert "overall_score" in result
        assert "dimensions" in result
        assert "priority_issues" in result
    
    def test_optimize_session(self, test_client):
        """Test optimizing a session."""
        # First upload files and analyze
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        self.test_analyze_session(test_client)
        
        # Optimize session
        request_data = {
            "focus_areas": ["prompt_clarity", "context_flow"],
            "optimization_level": "balanced"
        }
        
        response = test_client.post(
            f"/api/v1/optimize/{session_id}",
            json=request_data
        )
        
        assert response.status_code == 200
        
        result = response.json()
        assert result["session_id"] == session_id
        assert "optimized_agents" in result
        assert "tool_format_recommendations" in result
        assert "implementation_guide" in result
    
    def test_get_optimization(self, test_client):
        """Test getting optimization results."""
        # First upload files, analyze, and optimize
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        self.test_analyze_session(test_client)
        self.test_optimize_session(test_client)
        
        # Get optimization results
        response = test_client.get(f"/api/v1/optimization/{session_id}")
        assert response.status_code == 200
        
        result = response.json()
        assert result["session_id"] == session_id
        assert "optimized_agents" in result
        assert "tool_format_recommendations" in result
    
    def test_delete_session(self, test_client):
        """Test deleting a session."""
        # First upload files to create a session
        session_id = self.test_upload_files(test_client, test_client.app.state.test_data_dir)
        
        # Delete session
        response = test_client.delete(f"/api/v1/session/{session_id}")
        assert response.status_code == 200
        
        result = response.json()
        assert result["success"] is True
        assert result["session_id"] == session_id
        
        # Verify session is deleted
        response = test_client.get(f"/api/v1/session/{session_id}")
        assert response.status_code == 404
    
    def test_delete_nonexistent_session(self, test_client):
        """Test deleting nonexistent session."""
        response = test_client.delete("/api/v1/session/nonexistent")
        assert response.status_code == 404


# Add app state for tests
@pytest.fixture(autouse=True)
def setup_app_state(test_client, test_data_dir):
    """Set up app state for tests."""
    test_client.app.state.test_data_dir = test_data_dir 