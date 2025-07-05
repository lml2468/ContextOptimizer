"""
Context evaluation engine.
"""

import json
from typing import Dict, Any

from ..models.agent import AgentConfig
from ..models.message import MessageDataset
from ..services.llm_service import LLMService
from ..utils.exceptions import LLMServiceError
from ..utils.logger import get_logger
from .prompts import PromptTemplates

logger = get_logger(__name__)


class ContextEvaluator:
    """Engine for evaluating Multi-Agent System context quality."""
    
    def __init__(self, llm_service: LLMService):
        """Initialize evaluator with LLM service."""
        self.llm_service = llm_service
    
    async def evaluate_context(
        self,
        agents_config: AgentConfig,
        messages_dataset: MessageDataset
    ) -> Dict[str, Any]:
        """Evaluate context quality and provide detailed analysis."""
        try:
            logger.info("Starting context evaluation")
            
            # Prepare data for evaluation
            agents_config_json = self._prepare_agents_config(agents_config)
            messages_dataset_json = self._prepare_messages_dataset(messages_dataset)
            
            # Generate evaluation prompt
            evaluation_prompt = PromptTemplates.get_evaluation_prompt(
                agents_config=agents_config_json,
                messages_sample=messages_dataset_json,
                agent_count=len(agents_config.agents),
                message_count=len(messages_dataset.messages),
                tool_count=len(messages_dataset.get_unique_tools())
            )
            
            # Call LLM for evaluation
            logger.info("Calling LLM for context evaluation")
            
            try:
                response = await self.llm_service.call_llm(
                    prompt=evaluation_prompt,
                    system_prompt=PromptTemplates.EVALUATION_SYSTEM_PROMPT,
                    max_tokens=4000,
                    temperature=0.1
                )
                logger.info("LLM response received")
            except Exception as llm_error:
                logger.error(f"LLM call failed: {llm_error}")
                raise
            
            # Parse response
            try:
                evaluation_result = await self.llm_service.parse_json_response(response)
                logger.info("JSON parsing successful")
            except Exception as parse_error:
                logger.error(f"JSON parsing failed: {parse_error}")
                raise
            
            # Validate and enhance result
            evaluation_result = self._enhance_evaluation_result(
                evaluation_result, agents_config, messages_dataset
            )
            
            logger.info("Context evaluation completed successfully")
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Context evaluation failed: {e}")
            raise LLMServiceError(f"Context evaluation failed: {e}")
    
    def _prepare_agents_config(self, agents_config: AgentConfig) -> str:
        """Prepare agents config for LLM evaluation."""
        config_dict = agents_config.model_dump()
        return json.dumps(config_dict, indent=2, ensure_ascii=False)
    
    def _prepare_messages_dataset(self, messages_dataset: MessageDataset) -> str:
        """Prepare messages dataset for LLM evaluation."""
        dataset_dict = messages_dataset.model_dump()
        return json.dumps(dataset_dict, indent=2, ensure_ascii=False)
    
    def _enhance_evaluation_result(
        self,
        evaluation_result: Dict[str, Any],
        agents_config: AgentConfig,
        messages_dataset: MessageDataset
    ) -> Dict[str, Any]:
        """Enhance evaluation result with additional metadata."""
        
        # Ensure required fields exist
        required_fields = {
            "overall_score": 5.0,
            "dimensions": [],
            "priority_issues": [],
            "summary": "Analysis completed",
            "recommendations": []
        }
        
        for field, default_value in required_fields.items():
            if field not in evaluation_result:
                evaluation_result[field] = default_value
        
        # Add metadata
        evaluation_result["metadata"] = {
            "analysis_timestamp": "2024-01-01T00:00:00Z",  # Will be set by caller
            "agent_count": len(agents_config.agents),
            "message_count": len(messages_dataset.messages),
            "unique_tools": len(messages_dataset.get_unique_tools()),
            "agent_names": agents_config.get_agent_names(),
            "tool_names": messages_dataset.get_unique_tools()
        }
        
        # Validate scores
        evaluation_result["overall_score"] = max(0.0, min(10.0, float(evaluation_result["overall_score"])))
        
        for dimension in evaluation_result["dimensions"]:
            if "score" in dimension:
                dimension["score"] = max(0.0, min(10.0, float(dimension["score"])))
        
        return evaluation_result
