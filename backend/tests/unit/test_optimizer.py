"""
Unit tests for context optimizer.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.core.optimizer import ContextOptimizer
from app.utils.exceptions import OptimizationError
from app.models.agent import AgentConfig
from app.models.message import MessageDataset


class TestContextOptimizer:
    """Tests for ContextOptimizer class."""
    
    @pytest.fixture
    def optimizer(self, mock_llm_service):
        """Create a context optimizer for testing."""
        return ContextOptimizer(llm_service=mock_llm_service)
    
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
    
    @pytest.fixture
    def sample_optimization_result(self):
        """Create a sample optimization result."""
        return {
            "optimized_agents": [
                {
                    "agent_id": "agent1",
                    "agent_name": "Research Agent",
                    "original_system_prompt": "Original prompt",
                    "optimized_system_prompt": "Optimized prompt",
                    "changes_summary": "Test changes",
                    "tools": [{"name": "search_web", "description": "Search tool"}]
                },
                {
                    "agent_id": "agent2",
                    "agent_name": "Coding Agent",
                    "original_system_prompt": "Original prompt",
                    "optimized_system_prompt": "Optimized prompt",
                    "changes_summary": "Test changes",
                    "tools": [{"name": "code_editor", "description": "Code tool"}]
                }
            ],
            "tool_format_recommendations": [
                {
                    "tool_name": "search_web",
                    "current_format": "Current format",
                    "recommended_format": "Recommended format",
                    "format_example": {"key": "value"},
                    "rationale": "Test rationale"
                }
            ],
            "implementation_guide": "Test guide",
            "expected_improvements": ["Test improvement"],
            "compatibility_notes": ["Test note"]
        }
    
    @pytest.mark.asyncio
    async def test_optimize_context(self, optimizer, sample_agents_config_model, 
                                   sample_messages_dataset_model, sample_evaluation_result,
                                   sample_optimization_result):
        """Test optimizing context."""
        # Mock LLM service to return sample optimization result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_optimization_result
        optimizer.llm_service = mock_llm
        
        # Optimize context
        result = await optimizer.optimize_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model,
            evaluation_result=sample_evaluation_result,
            focus_areas=["prompt_clarity", "context_flow"],
            optimization_level="balanced"
        )
        
        # Verify result
        assert result == sample_optimization_result
        assert len(result["optimized_agents"]) == 2
        assert len(result["tool_format_recommendations"]) == 1
        
        # Verify LLM was called
        mock_llm.call_llm.assert_called_once()
        mock_llm.parse_json_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_optimize_context_conservative(self, optimizer, sample_agents_config_model, 
                                               sample_messages_dataset_model, sample_evaluation_result,
                                               sample_optimization_result):
        """Test optimizing context with conservative level."""
        # Mock LLM service to return sample optimization result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_optimization_result
        optimizer.llm_service = mock_llm
        
        # Optimize context with conservative level
        result = await optimizer.optimize_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model,
            evaluation_result=sample_evaluation_result,
            focus_areas=["prompt_clarity"],
            optimization_level="conservative"
        )
        
        # Verify result
        assert result == sample_optimization_result
        
        # Verify LLM was called with appropriate parameters
        prompt = mock_llm.call_llm.call_args[1]["prompt"]
        assert "conservative" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_optimize_context_aggressive(self, optimizer, sample_agents_config_model, 
                                             sample_messages_dataset_model, sample_evaluation_result,
                                             sample_optimization_result):
        """Test optimizing context with aggressive level."""
        # Mock LLM service to return sample optimization result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_optimization_result
        optimizer.llm_service = mock_llm
        
        # Optimize context with aggressive level
        result = await optimizer.optimize_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model,
            evaluation_result=sample_evaluation_result,
            focus_areas=["context_flow"],
            optimization_level="aggressive"
        )
        
        # Verify result
        assert result == sample_optimization_result
        
        # Verify LLM was called with appropriate parameters
        prompt = mock_llm.call_llm.call_args[1]["prompt"]
        assert "aggressive" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_optimize_context_with_focus_areas(self, optimizer, sample_agents_config_model, 
                                                   sample_messages_dataset_model, sample_evaluation_result,
                                                   sample_optimization_result):
        """Test optimizing context with specific focus areas."""
        # Mock LLM service to return sample optimization result
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.return_value = sample_optimization_result
        optimizer.llm_service = mock_llm
        
        # Optimize context with specific focus areas
        focus_areas = ["prompt_clarity"]
        result = await optimizer.optimize_context(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model,
            evaluation_result=sample_evaluation_result,
            focus_areas=focus_areas
        )
        
        # Verify result
        assert result == sample_optimization_result
        
        # Verify focus areas were included in prompt
        prompt = mock_llm.call_llm.call_args[1]["prompt"]
        assert "prompt_clarity" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_optimize_context_llm_error(self, optimizer, sample_agents_config_model, 
                                            sample_messages_dataset_model, sample_evaluation_result):
        """Test handling LLM errors during optimization."""
        # Mock LLM service to raise exception
        mock_llm = MagicMock()
        mock_llm.call_llm.side_effect = Exception("LLM Error")
        optimizer.llm_service = mock_llm
        
        # Optimize context and expect error
        with pytest.raises(OptimizationError):
            await optimizer.optimize_context(
                agents_config=sample_agents_config_model,
                messages_dataset=sample_messages_dataset_model,
                evaluation_result=sample_evaluation_result
            )
    
    @pytest.mark.asyncio
    async def test_optimize_context_parsing_error(self, optimizer, sample_agents_config_model, 
                                                sample_messages_dataset_model, sample_evaluation_result):
        """Test handling parsing errors during optimization."""
        # Mock LLM service to return response but fail parsing
        mock_llm = MagicMock()
        mock_llm.call_llm.return_value = "Test LLM response"
        mock_llm.parse_json_response.side_effect = Exception("Parsing Error")
        optimizer.llm_service = mock_llm
        
        # Optimize context and expect error
        with pytest.raises(OptimizationError):
            await optimizer.optimize_context(
                agents_config=sample_agents_config_model,
                messages_dataset=sample_messages_dataset_model,
                evaluation_result=sample_evaluation_result
            )
    
    @pytest.mark.asyncio
    async def test_generate_optimization_prompt(self, optimizer, sample_agents_config_model, 
                                              sample_messages_dataset_model, sample_evaluation_result):
        """Test generating optimization prompt."""
        # Generate prompt
        prompt = optimizer._generate_optimization_prompt(
            agents_config=sample_agents_config_model,
            messages_dataset=sample_messages_dataset_model,
            evaluation_result=sample_evaluation_result,
            focus_areas=["prompt_clarity", "context_flow"],
            optimization_level="balanced"
        )
        
        # Verify prompt contains necessary information
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "agents" in prompt.lower()
        assert "messages" in prompt.lower()
        assert "prompt_clarity" in prompt.lower()
        assert "context_flow" in prompt.lower()
        assert "balanced" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_validate_optimization_result(self, optimizer, sample_optimization_result):
        """Test validating optimization result."""
        # Valid result should not raise exception
        optimizer._validate_optimization_result(sample_optimization_result)
        
        # Test with missing fields
        incomplete_result = {
            "optimized_agents": []
            # Missing other required fields
        }
        
        with pytest.raises(OptimizationError):
            optimizer._validate_optimization_result(incomplete_result)
        
        # Test with empty optimized agents
        empty_agents_result = dict(sample_optimization_result)
        empty_agents_result["optimized_agents"] = []
        
        with pytest.raises(OptimizationError):
            optimizer._validate_optimization_result(empty_agents_result) 