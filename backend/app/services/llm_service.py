"""
LLM service for calling OpenAI and Anthropic APIs using LangChain.
"""

import json
import hashlib
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from json_repair import repair_json

from ..config import settings
from ..utils.exceptions import LLMServiceError, ConfigurationError
from ..utils.logger import get_logger
from ..utils.cache import cache_manager

logger = get_logger()


class LLMService:
    """Service for LLM API calls using LangChain."""
    
    def __init__(self):
        """Initialize LLM service."""
        self.openai_client = None
        
        if not settings.has_openai_key:
            raise ConfigurationError("No LLM API keys configured")
        
        self.openai_client = ChatOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            model=settings.openai_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )
        logger.info("LLM service initialized")
        
        # Cache configuration
        self.use_cache = settings.use_llm_cache
        self.cache_ttl = settings.llm_cache_ttl
    
    async def call_llm(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        skip_cache: bool = False
    ) -> str:
        """Call LLM with the given prompt."""
        
        max_tokens = max_tokens or settings.max_tokens
        temperature = temperature or settings.temperature
        
        # Check cache first
        cache_key = None
        if self.use_cache and not skip_cache:
            cache_key = self._generate_cache_key(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            cached_response = cache_manager.get(cache_key)
            if cached_response:
                logger.debug("Using cached LLM response")
                return cached_response
        
        try:
            # Call Model
            if self.openai_client:
                response = await self._call_openai(prompt, system_prompt, max_tokens, temperature)
                logger.info("LLM API call successful")
            else:
                raise LLMServiceError("No LLM providers available")
            
            # Cache the response if caching is enabled
            if self.use_cache and cache_key and not skip_cache:
                cache_manager.set(cache_key, response, self.cache_ttl)
            
            return response
        
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise LLMServiceError(f"LLM call failed: {e}")
    
    async def _call_openai(
        self, 
        prompt: str, 
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call OpenAI API using LangChain."""
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            # Use custom client if parameters differ
            client = self.openai_client
            if max_tokens != settings.max_tokens or temperature != settings.temperature:
                client = ChatOpenAI(
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url,
                    model=settings.openai_model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            # Make API call
            logger.debug(f"Calling LLM API: {settings.openai_model}")
            response = await client.ainvoke(messages)
            
            result = response.content
            logger.info("LLM API call successful")
            
            return result
            
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise LLMServiceError(f"LLM API call failed: {e}")
    
    async def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM using json-repair for enhanced robustness."""
        try:
            # First, try standard JSON parsing on the raw response
            try:
                result = json.loads(response.strip())
                logger.debug("JSON parsing successful")
                return result
                
            except json.JSONDecodeError:
                # If standard parsing fails, use json-repair directly on the original response
                logger.debug("Standard JSON parsing failed, attempting repair")
                repaired_json = repair_json(response)
                result = json.loads(repaired_json)
                logger.debug("JSON parsing successful after repair")
                return result
                
        except Exception as e:
            logger.error(f"Failed to parse JSON response: {e}")
            raise LLMServiceError(f"Invalid JSON response from LLM: {e}")
    
    def _generate_cache_key(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Generate a cache key for LLM request."""
        # Create a dictionary of all parameters that affect the response
        cache_data = {
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "model": settings.openai_model
        }
        
        # Convert to a stable string representation
        cache_str = json.dumps(cache_data, sort_keys=True)
        
        # Generate hash
        return f"llm:{hashlib.md5(cache_str.encode()).hexdigest()}"
    
    def clear_cache(self) -> None:
        """Clear the LLM response cache."""
        cache_manager.clear()
        logger.info("LLM response cache cleared")
