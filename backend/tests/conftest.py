"""
Test configuration and fixtures.
"""

import pytest
import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

from app.core.evaluator import ContextEvaluator
from app.core.optimizer import ContextOptimizer
from app.services.llm_service import LLMService
from app.models.agent import AgentConfig
from app.models.message import MessageDataset

# Test directories
backend_dir = Path(__file__).parent.parent
test_data_dir = backend_dir / "test_data"


@pytest.fixture
def temp_test_dir():
    """Create a temporary directory for test files."""
    temp_dir = backend_dir / "tests" / "temp"
    temp_dir.mkdir(exist_ok=True)
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def test_data_dir():
    """Get the test data directory."""
    return test_data_dir


@pytest.fixture
def sample_agents_config():
    """Create sample agents configuration."""
    return {
        "agents": [
            {
                "agent_id": "agent1",
                "agent_name": "Research Agent",
                "system_prompt": "You are a research agent.",
                "tools": [{"name": "search_web", "description": "Search the web"}]
            },
            {
                "agent_id": "agent2",
                "agent_name": "Coding Agent",
                "system_prompt": "You are a coding agent.",
                "tools": [{"name": "code_editor", "description": "Edit code"}]
            }
        ]
    }


@pytest.fixture
def sample_agents_config_model(sample_agents_config):
    """Create AgentConfig model from sample data."""
    return AgentConfig(**sample_agents_config)


@pytest.fixture
def sample_messages_dataset():
    """Create sample messages dataset."""
    return {
        "messages": [
            {"type": "human", "id": "msg1", "content": "Hello"},
            {"type": "ai", "name": "agent1", "id": "msg2", "content": "Hi there!"},
            {"type": "human", "id": "msg3", "content": "How are you?"},
            {"type": "ai", "name": "agent2", "id": "msg4", "content": "I'm doing well!"}
        ]
    }


@pytest.fixture
def sample_messages_dataset_model(sample_messages_dataset):
    """Create MessageDataset model from sample data."""
    return MessageDataset(**sample_messages_dataset)


@pytest.fixture
def sample_evaluation_result():
    """Create sample evaluation result."""
    return {
        "overall_score": 7.5,
        "dimensions": [
            {"name": "prompt_clarity", "score": 8.0, "feedback": "Good clarity"},
            {"name": "context_flow", "score": 7.0, "feedback": "Needs improvement"}
        ],
        "priority_issues": [
            {"category": "prompt_clarity", "priority": "medium", "description": "Test issue"}
                ],
        "summary": "Overall good performance",
        "recommendations": ["Improve context flow"]
    }


@pytest.fixture
def sample_optimization_result():
    """Create sample optimization result."""
    return {
        "optimized_agents": [
            {
                "agent_id": "agent1",
                "agent_name": "Research Agent",
                "original_system_prompt": "Original prompt",
                "optimized_system_prompt": "Optimized prompt",
                "changes_summary": "Improved clarity",
                "tools": [{"name": "search_web", "description": "Search tool"}]
            }
        ],
        "tool_format_recommendations": [
            {
                "tool_name": "search_web",
                "current_format": "Current format",
                "recommended_format": "Recommended format",
                "rationale": "Better structure"
            }
        ],
        "implementation_guide": "Apply the changes as described",
        "expected_improvements": ["Better performance"],
        "compatibility_notes": ["No breaking changes"]
    }


@pytest.fixture
def mock_llm_service():
    """Create a mock LLM service."""
    mock = MagicMock(spec=LLMService)
    mock.call_llm.return_value = "Mock LLM response"
    mock.parse_json_response.return_value = {"test": "response"}
    return mock


@pytest.fixture
def evaluator(mock_llm_service):
    """Create ContextEvaluator with mock LLM service."""
    return ContextEvaluator(mock_llm_service)


@pytest.fixture
def optimizer(mock_llm_service):
    """Create ContextOptimizer with mock LLM service."""
    return ContextOptimizer(mock_llm_service) 