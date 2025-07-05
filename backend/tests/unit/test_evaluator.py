"""
Unit tests for context evaluator.
"""

import pytest
from unittest.mock import patch, MagicMock
import json

from app.core.evaluator import ContextEvaluator
from app.services.llm_service import LLMService
from app.utils.exceptions import LLMServiceError
from app.models.agent import AgentConfig
from app.models.message import MessageDataset


class TestContextEvaluator:
    """Tests for ContextEvaluator class."""
    
    @pytest.fixture
    def evaluator(self, mock_llm_service):
        """Create a context evaluator for testing."""
        return ContextEvaluator(llm_service=mock_llm_service)
    
    @pytest.fixture
    def sample_evaluation_result(self):
        """Create a sample evaluation result."""
        return {
            "overall_score": 7.5,
            "dimensions": [
                {
                    "name": "Prompt Clarity",
                    "score": 8.0,
                    "description": "Assessment of system prompt quality",
                    "issues": ["Test issue"],
                    "recommendations": ["Test recommendation"]
                },
                {
                    "name": "Context Flow",
                    "score": 7.0,
                    "description": "Assessment of information flow between agents",
                    "issues": ["Test issue"],
                    "recommendations": ["Test recommendation"]
                }
            ],
            "priority_issues": [
                {
                    "priority": "high",
                    "category": "Context Flow",
                    "description": "Test issue description",
                    "impact": "Test impact",
                    "solution": "Test solution",
                    "affected_agents": ["agent1", "agent2"]
                }
            ],
            "summary": "Test summary",
            "recommendations": ["Test recommendation"]
        }
    
    @pytest.mark.asyncio
    async def test_evaluate_context(self, evaluator, sample_agents_config_model, 
                                   sample_messages_dataset_model, sample_evaluation_result):
        """Test evaluating context."""
        # Mock LLM service to return sample evaluation result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_evaluation_result
        evaluator.llm_service = mock_llm
        
        # Evaluate context
        result = await evaluator.evaluate_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model
        )
        
        # Verify result
        assert result == sample_evaluation_result
        assert result["overall_score"] == 7.5
        assert len(result["dimensions"]) == 2
        assert len(result["priority_issues"]) == 1
        
        # Verify LLM was called
        mock_llm.call_llm.assert_called_once()
        mock_llm.parse_json_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_evaluate_context_standard_analysis(self, evaluator, sample_agents_config_model, 
                                                sample_messages_dataset_model, sample_evaluation_result):
        """Test evaluating context with standard analysis."""
        # Mock LLM service to return sample evaluation result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_evaluation_result
        evaluator.llm_service = mock_llm
        
        # Evaluate context with standard analysis
        result = await evaluator.evaluate_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model
        )
        
        # Verify result
        assert result == sample_evaluation_result
        
        # Verify LLM was called with appropriate parameters
        call_args = mock_llm.call_llm.call_args[1]
        assert "temperature" in call_args
        assert call_args["temperature"] == 0.1  # Standard analysis temperature
    
    @pytest.mark.asyncio
    async def test_evaluate_context_with_focus_areas(self, evaluator, sample_agents_config_model, 
                                                   sample_messages_dataset_model, sample_evaluation_result):
        """Test evaluating context with specific focus areas."""
        # Mock LLM service to return sample evaluation result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_evaluation_result
        evaluator.llm_service = mock_llm
        
        # Evaluate context with specific focus areas
        focus_areas = ["prompt_clarity"]
        result = await evaluator.evaluate_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model
        )
        
        # Verify result
        assert result == sample_evaluation_result
        
        # Verify focus areas were included in prompt
        prompt = mock_llm.call_llm.call_args[1]["prompt"]
        assert "prompt_clarity" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_evaluate_context_llm_error(self, evaluator, sample_agents_config_model, 
                                            sample_messages_dataset_model):
        """Test handling LLM errors during evaluation."""
        # Mock LLM service to raise exception
        mock_llm = MagicMock()
        mock_llm.call_llm.side_effect = Exception("LLM Error")
        evaluator.llm_service = mock_llm
        
        # Evaluate context and expect error
        with pytest.raises(LLMServiceError):
            await evaluator.evaluate_context(
                agents_config=sample_agents_config_model,
                messages_dataset=sample_messages_dataset_model
            )
    
    @pytest.mark.asyncio
    async def test_evaluate_context_parsing_error(self, evaluator, sample_agents_config_model, 
                                                sample_messages_dataset_model):
        """Test handling parsing errors during evaluation."""
        # Mock LLM service to return response but fail parsing
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.side_effect = Exception("Parsing Error")
        evaluator.llm_service = mock_llm
        
        # Evaluate context and expect error
        with pytest.raises(LLMServiceError):
            await evaluator.evaluate_context(
                agents_config=sample_agents_config_model,
                messages_dataset=sample_messages_dataset_model
            )
    
    @pytest.mark.asyncio
    async def test_generate_evaluation_prompt(self, evaluator, sample_agents_config_model, 
                                            sample_messages_dataset_model):
        """Test generating evaluation prompt."""
        # Generate prompt
        prompt = evaluator._generate_evaluation_prompt(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model
        )
        
        # Verify prompt contains necessary information
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "agents" in prompt.lower()
        assert "messages" in prompt.lower()
        assert "prompt_clarity" in prompt.lower()
        assert "context_flow" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_validate_evaluation_result(self, evaluator, sample_evaluation_result):
        """Test validating evaluation result."""
        # Valid result should not raise exception
        evaluator._validate_evaluation_result(sample_evaluation_result)
        
        # Test with missing fields
        incomplete_result = {
            "overall_score": 7.5,
            "dimensions": []
            # Missing other required fields
        }
        
        with pytest.raises(LLMServiceError):
            evaluator._validate_evaluation_result(incomplete_result)
        
        # Test with invalid score
        invalid_score_result = dict(sample_evaluation_result)
        invalid_score_result["overall_score"] = 11  # Score out of range
        
        with pytest.raises(LLMServiceError):
            evaluator._validate_evaluation_result(invalid_score_result) 