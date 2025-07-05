"""
Unit tests for validation utilities.
"""

import pytest
import json
from pathlib import Path

from app.utils.validation import ValidationUtils
from app.utils.exceptions import ValidationError, DataConsistencyError
from app.models.agent import AgentConfig
from app.models.message import MessageDataset


class TestValidationUtils:
    """Tests for ValidationUtils class."""
    
    def test_validate_agents_config_standard_format(self, sample_agents_config):
        """Test validating agents config in standard format."""
        # Standard format with agents list
        result = ValidationUtils.validate_agents_config(sample_agents_config)
        assert isinstance(result, AgentConfig)
        assert len(result.agents) == 2
        assert result.agents[0].agent_id == "agent1"
        assert result.agents[1].agent_id == "agent2"
    
    def test_validate_agents_config_direct_list(self):
        """Test validating agents config as direct list."""
        # Direct list format
        agents_list = [
            {
                "agent_id": "test_agent",
                "agent_name": "Test Agent",
                "system_prompt": "You are a test agent."
            }
        ]
        
        result = ValidationUtils.validate_agents_config(agents_list)
        assert isinstance(result, AgentConfig)
        assert len(result.agents) == 1
        assert result.agents[0].agent_id == "test_agent"
    
    def test_validate_agents_config_single_agent(self):
        """Test validating agents config as single agent."""
        # Single agent format
        single_agent = {
            "agent_id": "test_agent",
            "agent_name": "Test Agent",
            "system_prompt": "You are a test agent."
        }
        
        result = ValidationUtils.validate_agents_config(single_agent)
        assert isinstance(result, AgentConfig)
        assert len(result.agents) == 1
        assert result.agents[0].agent_id == "test_agent"
    
    def test_validate_agents_config_legacy_format(self):
        """Test validating agents config with legacy field names."""
        # Legacy format with id/name instead of agent_id/agent_name
        legacy_format = {
            "agents": [
                {
                    "id": "legacy_agent",
                    "name": "Legacy Agent",
                    "system_prompt": "You are a legacy agent."
                }
            ]
        }
        
        result = ValidationUtils.validate_agents_config(legacy_format)
        assert isinstance(result, AgentConfig)
        assert len(result.agents) == 1
        assert result.agents[0].agent_id == "legacy_agent"
        assert result.agents[0].agent_name == "Legacy Agent"
    
    def test_validate_agents_config_invalid_format(self):
        """Test validating agents config with invalid format."""
        # Invalid format (not a dict or list)
        with pytest.raises(ValidationError):
            ValidationUtils.validate_agents_config("not a dict or list")
        
        # Empty agents list
        with pytest.raises(ValidationError):
            ValidationUtils.validate_agents_config({"agents": []})
        
        # Missing required fields
        with pytest.raises(ValidationError):
            ValidationUtils.validate_agents_config([{"agent_id": "missing_fields"}])
    
    def test_validate_messages_dataset_standard_format(self, sample_messages_dataset):
        """Test validating messages dataset in standard format."""
        # Standard format with messages list
        result = ValidationUtils.validate_messages_dataset(sample_messages_dataset)
        assert isinstance(result, MessageDataset)
        assert len(result.messages) == 4
    
    def test_validate_messages_dataset_direct_list(self):
        """Test validating messages dataset as direct list."""
        # Direct list format
        messages_list = [
            {
                "type": "human",
                "id": "msg1",
                "content": "Test message"
            }
        ]
        
        result = ValidationUtils.validate_messages_dataset(messages_list)
        assert isinstance(result, MessageDataset)
        assert len(result.messages) == 1
        assert result.messages[0].type == "human"
    
    def test_validate_messages_dataset_conversation_format(self):
        """Test validating messages dataset in conversation format."""
        # Conversation format
        conv_format = {
            "conversations": [
                {
                    "messages": [
                        {
                            "type": "human",
                            "id": "msg1",
                            "content": "Test message"
                        }
                    ]
                }
            ]
        }
        
        result = ValidationUtils.validate_messages_dataset(conv_format)
        assert isinstance(result, MessageDataset)
        assert len(result.messages) == 1
        assert result.messages[0].type == "human"
    
    def test_validate_messages_dataset_role_format(self):
        """Test validating messages dataset with role instead of type."""
        # Role format instead of type
        role_format = {
            "messages": [
                {
                    "role": "user",
                    "id": "msg1",
                    "content": "Test message"
                },
                {
                    "role": "assistant",
                    "id": "msg2",
                    "content": "Test response"
                }
            ]
        }
        
        result = ValidationUtils.validate_messages_dataset(role_format)
        assert isinstance(result, MessageDataset)
        assert len(result.messages) == 2
        assert result.messages[0].type == "human"  # user -> human
        assert result.messages[1].type == "ai"     # assistant -> ai
    
    def test_validate_messages_dataset_invalid_format(self):
        """Test validating messages dataset with invalid format."""
        # Invalid format (not a dict or list)
        with pytest.raises(ValidationError):
            ValidationUtils.validate_messages_dataset("not a dict or list")
        
        # Empty messages list
        with pytest.raises(ValidationError):
            ValidationUtils.validate_messages_dataset({"messages": []})
        
        # Missing required fields
        with pytest.raises(ValidationError):
            ValidationUtils.validate_messages_dataset({"messages": [{"content": "missing fields"}]})
    
    def test_validate_file_size(self):
        """Test validating file size."""
        # Valid file size
        assert ValidationUtils.validate_file_size(1000, 2000) is True
        
        # Invalid file size
        with pytest.raises(ValidationError):
            ValidationUtils.validate_file_size(2000, 1000)
    
    def test_validate_session_files(self, sample_agents_config_model, sample_messages_dataset_model):
        """Test cross-validating session files."""
        # Valid session files
        result = ValidationUtils.validate_session_files(
            sample_agents_config_model,
            sample_messages_dataset_model
        )
        
        assert "warnings" in result
        assert "recommendations" in result
        assert isinstance(result["agents_count"], int)
        assert isinstance(result["messages_count"], int)
    
    def test_validate_session_files_with_inconsistencies(self, sample_agents_config_model):
        """Test cross-validating session files with inconsistencies."""
        # Create messages dataset with agent not in config
        inconsistent_messages = MessageDataset(
            messages=[
                {
                    "type": "human",
                    "id": "msg1",
                    "content": "Test message"
                },
                {
                    "type": "ai",
                    "name": "unknown_agent",  # Agent not in config
                    "id": "msg2",
                    "content": "Test response"
                }
            ]
        )
        
        result = ValidationUtils.validate_session_files(
            sample_agents_config_model,
            inconsistent_messages
        )
        
        # Should have warnings about inconsistencies
        assert len(result["warnings"]) > 0
        assert any("unknown_agent" in warning for warning in result["warnings"])
        assert len(result["recommendations"]) > 0 