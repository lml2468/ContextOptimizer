"""
Unit tests for LLM service.
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock, AsyncMock

from app.services.llm_service import LLMService
from app.utils.exceptions import LLMServiceError
from app.utils.cache import cache_manager


class TestLLMService:
    """Tests for LLMService class."""
    
    @pytest.fixture
    def llm_service(self):
        """Create an LLM service for testing."""
        with patch('langchain_openai.ChatOpenAI'):
            service = LLMService()
            # Set use_cache to True for testing
            service.use_cache = True
            service.cache_ttl = 3600
            return service
    
    @pytest.fixture
    def mock_langchain_response(self):
        """Create a mock LangChain response."""
        mock_response = MagicMock()
        mock_response.content = "This is a test response"
        return mock_response
    
    # Anthropic fixture removed
    
    @pytest.mark.asyncio
    async def test_call_llm_openai(self, llm_service, mock_langchain_response):
        """Test calling LangChain OpenAI LLM."""
        # Replace the openai_client with our mock
        with patch.object(llm_service, 'openai_client') as mock_client:
            mock_client.ainvoke = AsyncMock(return_value=mock_langchain_response)
            
            # Call LLM
            response = await llm_service.call_llm(
                prompt="Test prompt"
            )
            
            # Verify response
            assert response == "This is a test response"
            
            # Verify LangChain was called correctly
            mock_client.ainvoke.assert_called_once()
            call_args = mock_client.ainvoke.call_args[0]
            messages = call_args[0]
            assert len(messages) == 1
            assert messages[0].content == "Test prompt"
    
    # Anthropic test removed
    
    @pytest.mark.asyncio
    async def test_call_llm_with_system_prompt(self, llm_service, mock_langchain_response):
        """Test calling LLM with system prompt."""
        # Replace the openai_client with our mock
        with patch.object(llm_service, 'openai_client') as mock_client:
            mock_client.ainvoke = AsyncMock(return_value=mock_langchain_response)
            
            # Call LLM with system prompt
            response = await llm_service.call_llm(
                prompt="Test prompt",
                system_prompt="You are a helpful assistant"
            )
            
            # Verify response
            assert response == "This is a test response"
            
            # Verify system prompt was included
            call_args = mock_client.ainvoke.call_args[0]
            messages = call_args[0]
            assert len(messages) == 2
            assert messages[0].content == "You are a helpful assistant"
            assert messages[1].content == "Test prompt"
    
    @pytest.mark.asyncio
    async def test_call_llm_with_parameters(self, llm_service, mock_langchain_response):
        """Test calling LLM with custom parameters."""
        # Mock ChatOpenAI constructor to capture parameters
        with patch('app.services.llm_service.ChatOpenAI') as mock_chat_openai:
            mock_client = MagicMock()
            mock_client.ainvoke = AsyncMock(return_value=mock_langchain_response)
            mock_chat_openai.return_value = mock_client
            
            # Call LLM with custom parameters
            response = await llm_service.call_llm(
                prompt="Test prompt",
                max_tokens=100,
                temperature=0.7
            )
            
            # Verify response
            assert response == "This is a test response"
            
            # Verify a new client was created with custom parameters
            mock_chat_openai.assert_called()
            call_args = mock_chat_openai.call_args[1]
            assert call_args["max_tokens"] == 100
            assert call_args["temperature"] == 0.7
    
    # Invalid provider test removed - no longer applicable with single provider
    
    @pytest.mark.asyncio
    async def test_call_llm_api_error(self, llm_service):
        """Test handling API errors."""
        # Clear cache first
        cache_manager.clear()
        
        # Replace the _call_openai method directly to ensure the exception is raised
        with patch.object(llm_service, '_call_openai') as mock_call:
            # Setup mock to raise exception
            mock_call.side_effect = Exception("API Error")
            
            # Call LLM with skip_cache to ensure the API is called
            with pytest.raises(LLMServiceError):
                await llm_service.call_llm(
                    prompt="Test prompt",
                    skip_cache=True
                )
    
    @pytest.mark.asyncio
    async def test_call_llm_with_cache(self, llm_service, mock_langchain_response):
        """Test LLM caching."""
        # Clear cache first
        cache_manager.clear()
        
        # Replace the openai_client with our mock
        with patch.object(llm_service, 'openai_client') as mock_client:
            mock_client.ainvoke = AsyncMock(return_value=mock_langchain_response)
            
            # First call should use the API
            response1 = await llm_service.call_llm(
                prompt="Test prompt"
            )
            
            # Second call with same parameters should use cache
            response2 = await llm_service.call_llm(
                prompt="Test prompt"
            )
            
            # Both responses should be the same
            assert response1 == response2
            
            # API should only be called once
            mock_client.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_call_llm_skip_cache(self, llm_service, mock_langchain_response):
        """Test skipping LLM cache."""
        # Clear cache first
        cache_manager.clear()
        
        # Replace the openai_client with our mock
        with patch.object(llm_service, 'openai_client') as mock_client:
            mock_client.ainvoke = AsyncMock(return_value=mock_langchain_response)
            
            # First call should use the API
            response1 = await llm_service.call_llm(
                prompt="Test prompt"
            )
            
            # Second call with skip_cache should use API again
            response2 = await llm_service.call_llm(
                prompt="Test prompt",
                skip_cache=True
            )
            
            # Both responses should be the same
            assert response1 == response2
            
            # API should be called twice
            assert mock_client.ainvoke.call_count == 2
    
    @pytest.mark.asyncio
    async def test_parse_json_response_valid(self, llm_service):
        """Test parsing valid JSON response."""
        # Valid JSON string
        json_response = '{"key": "value", "number": 42}'
        
        result = await llm_service.parse_json_response(json_response)
        assert result == {"key": "value", "number": 42}
    
    @pytest.mark.asyncio
    async def test_parse_json_response_with_markdown(self, llm_service):
        """Test parsing JSON response with markdown code blocks."""
        # JSON string with markdown code blocks
        markdown_response = """
        Here's the JSON:
        
        ```json
        {
            "key": "value",
            "number": 42
        }
        ```
        
        Hope that helps!
        """
        
        result = await llm_service.parse_json_response(markdown_response)
        assert result == {"key": "value", "number": 42}
    
    @pytest.mark.asyncio
    async def test_parse_json_response_invalid(self, llm_service):
        """Test parsing invalid JSON response."""
        # Truly invalid JSON that even json-repair can't fix
        invalid_response = "This is not JSON at all, just plain text"
        
        with pytest.raises(LLMServiceError):
            await llm_service.parse_json_response(invalid_response)
    
    @pytest.mark.asyncio
    async def test_parse_json_response_repair_features(self, llm_service):
        """Test json-repair enhanced features."""
        # Test cases that json-repair can fix
        test_cases = [
            # Missing quotes around keys
            ('{key: "value", number: 42}', {"key": "value", "number": 42}),
            
            # Trailing comma
            ('{"key": "value", "number": 42,}', {"key": "value", "number": 42}),
            
            # Single quotes
            ("{'key': 'value', 'number': 42}", {"key": "value", "number": 42}),
            
            # Missing closing brace (json-repair can fix this)
            ('{"key": "value", "number": 42', {"key": "value", "number": 42}),
            
            # Comments in JSON
            ('{"key": "value", /* comment */ "number": 42}', {"key": "value", "number": 42}),
        ]
        
        for input_json, expected in test_cases:
            result = await llm_service.parse_json_response(input_json)
            assert result == expected
    
    # test_get_available_providers removed - no longer applicable with single provider