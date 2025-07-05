"""
Context optimization engine.
"""

import json
from typing import Dict, Any

from ..models.agent import AgentConfig
from ..models.schemas import OptimizationResult
from ..services.llm_service import LLMService
from ..utils.exceptions import LLMServiceError
from ..utils.logger import get_logger
from .prompts import PromptTemplates

logger = get_logger(__name__)


class ContextOptimizer:
    """Engine for optimizing Multi-Agent System context logic."""
    
    def __init__(self, llm_service: LLMService):
        """Initialize optimizer with LLM service."""
        self.llm_service = llm_service
    
    async def optimize_context(
        self,
        agents_config: AgentConfig,
        evaluation_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate optimized agent configurations and tool recommendations."""
        try:
            logger.info("Starting context optimization")
            
            # Prepare data for optimization
            agents_config_json = self._prepare_agents_config(agents_config)
            evaluation_report_json = self._prepare_evaluation_report(evaluation_report)
            
            # Generate optimization prompt
            optimization_prompt = PromptTemplates.get_optimization_prompt(
                agents_config=agents_config_json,
                evaluation_report=evaluation_report_json
            )
            
            # Call LLM for optimization
            logger.info("Calling LLM for context optimization")
            
            try:
                response = await self.llm_service.call_llm(
                prompt=optimization_prompt,
                system_prompt=PromptTemplates.OPTIMIZATION_SYSTEM_PROMPT,
                max_tokens=4000,
                temperature=0.1
            )
                logger.info("LLM response received")
            except Exception as llm_error:
                logger.error(f"LLM call failed: {llm_error}")
                raise
            
            # Parse response
            try:
                optimization_result = await self.llm_service.parse_json_response(response)
                logger.info("JSON parsing successful")
                
                # Check if result is a dictionary (expected) or needs conversion
                if isinstance(optimization_result, list):
                    if optimization_result and isinstance(optimization_result[0], dict):
                        optimization_result = optimization_result[0]
                    else:
                        raise ValueError("Unexpected list format in optimization result")
                elif not isinstance(optimization_result, dict):
                    raise ValueError(f"Expected dict or list, got {type(optimization_result)}")
                    
            except Exception as parse_error:
                logger.error(f"JSON parsing failed: {parse_error}")
                raise
            
            # Validate and enhance result
            optimization_result = self._enhance_optimization_result(
                optimization_result, agents_config, evaluation_report
            )
            
            logger.info("Context optimization completed successfully")
            return optimization_result
            
        except Exception as e:
            logger.error(f"Context optimization failed: {e}")
            raise LLMServiceError(f"Context optimization failed: {e}")
    
    def _prepare_agents_config(self, agents_config: AgentConfig) -> str:
        """Prepare agents config for LLM optimization."""
        config_dict = agents_config.model_dump()
        return json.dumps(config_dict, indent=2, ensure_ascii=False)
    
    def _prepare_evaluation_report(self, evaluation_report: Dict[str, Any]) -> str:
        """Prepare evaluation report for LLM optimization."""
        return json.dumps(evaluation_report, indent=2, ensure_ascii=False)
    
    def _enhance_optimization_result(
        self,
        optimization_result: Dict[str, Any],
        agents_config: AgentConfig,
        evaluation_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance optimization result with additional metadata and validation."""
        
        # Ensure required fields exist
        required_fields = {
            "optimized_agents": [],
            "tool_format_recommendations": [],
            "implementation_guide": "Apply the optimized configurations to your MAS system.",
            "expected_improvements": [],
            "compatibility_notes": []
        }
        
        for field, default_value in required_fields.items():
            if field not in optimization_result:
                optimization_result[field] = default_value
        
        # Validate optimized agents
        optimization_result["optimized_agents"] = self._validate_optimized_agents(
            optimization_result["optimized_agents"], agents_config
        )
        
        # Add metadata
        optimization_result["metadata"] = {
            "optimization_timestamp": "2024-01-01T00:00:00Z",  # Will be set by caller
            "original_agent_count": len(agents_config.agents),
            "optimized_agent_count": len(optimization_result["optimized_agents"]),
            "tool_recommendations_count": len(optimization_result["tool_format_recommendations"]),
            "based_on_evaluation_score": evaluation_report.get("overall_score", 0.0)
        }
        
        # Generate summary statistics
        optimization_result["summary_stats"] = self._generate_summary_stats(
            optimization_result, evaluation_report
        )
        
        return optimization_result
    
    def _validate_optimized_agents(
        self,
        optimized_agents: list,
        original_config: AgentConfig
    ) -> list:
        """Validate and ensure completeness of optimized agents."""
        
        validated_agents = []
        original_agent_ids = {agent.agent_id for agent in original_config.agents}
        
        for optimized_agent in optimized_agents:
            # Ensure required fields
            if not isinstance(optimized_agent, dict):
                continue
            
            agent_id = optimized_agent.get("agent_id")
            if not agent_id or agent_id not in original_agent_ids:
                continue
            
            # Get original agent for reference
            original_agent = original_config.get_agent_by_id(agent_id)
            if not original_agent:
                continue
            
            # Ensure all required fields are present
            validated_agent = {
                "agent_id": agent_id,
                "agent_name": optimized_agent.get("agent_name", original_agent.agent_name),
                "original_system_prompt": optimized_agent.get("original_system_prompt", original_agent.system_prompt),
                "optimized_system_prompt": optimized_agent.get("optimized_system_prompt", original_agent.system_prompt),
                "changes_summary": optimized_agent.get("changes_summary", "No changes specified"),
                "tools": optimized_agent.get("tools", [tool.model_dump() for tool in original_agent.tools])
            }
            
            validated_agents.append(validated_agent)
        
        # Ensure all original agents are included
        optimized_agent_ids = {agent["agent_id"] for agent in validated_agents}
        for original_agent in original_config.agents:
            if original_agent.agent_id not in optimized_agent_ids:
                # Add original agent as fallback
                validated_agents.append({
                    "agent_id": original_agent.agent_id,
                    "agent_name": original_agent.agent_name,
                    "original_system_prompt": original_agent.system_prompt,
                    "optimized_system_prompt": original_agent.system_prompt,
                    "changes_summary": "No optimization applied",
                    "tools": [tool.model_dump() for tool in original_agent.tools]
                })
        
        return validated_agents
    
    def _generate_summary_stats(
        self,
        optimization_result: Dict[str, Any],
        evaluation_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate summary statistics for the optimization."""
        
        return {
            "agents_optimized": len(optimization_result["optimized_agents"]),
            "tool_recommendations": len(optimization_result["tool_format_recommendations"]),
            "expected_score_improvement": "8.5+",  # Target score
            "original_score": evaluation_report.get("overall_score", 0.0),
            "high_priority_issues_addressed": len([
                issue for issue in evaluation_report.get("priority_issues", [])
                if issue.get("priority") == "high"
            ]),
            "optimization_focus_areas": self._extract_focus_areas(evaluation_report)
        }
    
    def _extract_focus_areas(self, evaluation_report: Dict[str, Any]) -> list:
        """Extract main focus areas from evaluation report."""
        focus_areas = []
        
        # Extract from dimensions with low scores
        for dimension in evaluation_report.get("dimensions", []):
            score = dimension.get("score", 10.0)
            if score < 7.0:
                focus_areas.append(dimension.get("name", "Unknown"))
        
        # Extract from high priority issues
        for issue in evaluation_report.get("priority_issues", []):
            if issue.get("priority") == "high":
                category = issue.get("category", "")
                if category and category not in focus_areas:
                    focus_areas.append(category)
        
        return focus_areas
