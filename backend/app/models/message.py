"""
Message-related data models.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """Message type enumeration."""
    HUMAN = "human"
    AI = "ai"
    TOOL = "tool"


class ToolCall(BaseModel):
    """Model for tool call within a message."""
    
    name: str = Field(..., description="Tool name")
    args: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")
    id: str = Field(..., description="Tool call ID")
    type: str = Field(default="tool_call", description="Tool call type")


class Message(BaseModel):
    """Model for individual message in conversation."""
    
    content: str = Field(default="", description="Message content")
    type: MessageType = Field(..., description="Message type")
    name: Optional[str] = Field(default=None, description="Agent or tool name")
    id: str = Field(..., description="Message ID")
    example: bool = Field(default=False, description="Whether this is an example message")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Tool calls in message")
    invalid_tool_calls: List[dict] = Field(default_factory=list, description="Invalid tool calls")
    usage_metadata: Optional[dict] = Field(default=None, description="Usage metadata")
    tool_call_id: Optional[str] = Field(default=None, description="Tool call ID for tool messages")
    artifact: Optional[dict] = Field(default=None, description="Tool response artifact")
    status: Optional[str] = Field(default=None, description="Tool execution status")


class MessageDataset(BaseModel):
    """Model for complete message dataset."""
    
    messages: List[Message] = Field(..., description="List of messages")
    metadata: Optional[dict] = Field(default=None, description="Dataset metadata")
    
    def get_messages_by_type(self, message_type: MessageType) -> List[Message]:
        """Get messages by type."""
        return [msg for msg in self.messages if msg.type == message_type]
    
    def get_messages_by_agent(self, agent_name: str) -> List[Message]:
        """Get messages by agent name."""
        return [msg for msg in self.messages if msg.name == agent_name]
    
    def get_tool_calls(self) -> List[ToolCall]:
        """Get all tool calls from all messages."""
        tool_calls = []
        for message in self.messages:
            tool_calls.extend(message.tool_calls)
        return tool_calls
    
    def get_unique_agents(self) -> List[str]:
        """Get list of unique agent names."""
        agents = set()
        for message in self.messages:
            if message.name and message.type == MessageType.AI:
                agents.add(message.name)
        return list(agents)
    
    def get_unique_tools(self) -> List[str]:
        """Get list of unique tool names."""
        tools = set()
        for message in self.messages:
            for tool_call in message.tool_calls:
                tools.add(tool_call.name)
        return list(tools)
