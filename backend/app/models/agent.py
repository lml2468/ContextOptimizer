"""
Agent-related data models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AgentTool(BaseModel):
    """Model for agent tool configuration."""
    
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: Optional[dict] = Field(default=None, description="Tool parameters schema")


class Agent(BaseModel):
    """Model for individual agent configuration."""
    
    agent_id: str = Field(..., description="Unique agent identifier")
    agent_name: str = Field(..., description="Human-readable agent name")
    version: str = Field(default="1.0", description="Agent version")
    system_prompt: str = Field(..., description="System prompt for the agent")
    tools: List[AgentTool] = Field(default_factory=list, description="Available tools")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")


class AgentConfig(BaseModel):
    """Model for complete agent configuration file."""
    
    agents: List[Agent] = Field(..., description="List of agent configurations")
    version: Optional[str] = Field(default="1.0", description="Configuration version")
    metadata: Optional[dict] = Field(default=None, description="Configuration metadata")
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None
    
    def get_agent_names(self) -> List[str]:
        """Get list of all agent names."""
        return [agent.agent_name for agent in self.agents]
    
    def get_agent_ids(self) -> List[str]:
        """Get list of all agent IDs."""
        return [agent.agent_id for agent in self.agents]
