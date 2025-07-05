"""
Data validation utilities.
"""

import json
from typing import Dict, Any, List, Union, Tuple
from ..models.agent import AgentConfig
from ..models.message import MessageDataset, MessageType
from .exceptions import ValidationError, DataConsistencyError
from .logger import get_logger

logger = get_logger(__name__)


class ValidationUtils:
    """Utility class for data validation."""
    
    @staticmethod
    def validate_agents_config(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> AgentConfig:
        """Validate and parse agents configuration."""
        try:
            # Normalize input format
            config_data = ValidationUtils._normalize_agents_config_format(data)
            
            # Normalize agent data
            agents = config_data.get("agents", [])
            normalized_agents = []
            
            for i, agent in enumerate(agents):
                if not isinstance(agent, dict):
                    raise ValidationError(f"Agent {i} is not a valid object")
                
                normalized_agent = ValidationUtils._normalize_agent_fields(agent, i)
                normalized_agents.append(normalized_agent)
            
            # Create final configuration
            final_config = {"agents": normalized_agents}
            
            # Validate using Pydantic model
            return AgentConfig(**final_config)
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to validate agents config: {e}")
            raise ValidationError(f"Invalid agents configuration: {e}")
    
    @staticmethod
    def _normalize_agents_config_format(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Normalize agents configuration format."""
        if isinstance(data, list):
            logger.debug("Processing agents config in direct list format")
            return {"agents": data}
        elif isinstance(data, dict):
            if "agents" in data:
                logger.debug("Processing agents config in standard format")
                return data
            elif "agent_id" in data:
                logger.debug("Processing agents config in single agent format")
                return {"agents": [data]}
            elif any(key in data for key in ["id", "name", "agent_name"]):
                logger.debug("Inferred single agent format from keys")
                return {"agents": [data]}
            else:
                # Check if values are agent-like objects
                agent_like_values = [
                    v for v in data.values() 
                    if isinstance(v, dict) and ("agent_id" in v or "id" in v)
                ]
                if agent_like_values:
                    logger.debug("Inferred agent dictionary format")
                    return {"agents": agent_like_values}
                else:
                    raise ValidationError("Could not infer agents configuration format")
        else:
            raise ValidationError("Invalid agents configuration format")
    
    @staticmethod
    def _normalize_agent_fields(agent: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Normalize agent fields with fallback handling."""
        normalized_agent = {}
        
        # Handle ID field with fallbacks
        field_mappings = {
            "agent_id": ["agent_id", "id"],
            "agent_name": ["agent_name", "name"],
            "system_prompt": ["system_prompt", "prompt", "system"]
        }
        
        for target_field, source_fields in field_mappings.items():
            value = None
            for source_field in source_fields:
                if source_field in agent:
                    value = agent[source_field]
                    if source_field != target_field:
                        logger.debug(f"Normalized '{source_field}' to '{target_field}' for agent {index}")
                    break
            
            if value is not None:
                normalized_agent[target_field] = value
            elif target_field == "agent_id":
                raise ValidationError(f"Agent {index} missing required field: agent_id")
            elif target_field == "agent_name":
                # Use ID as fallback for name
                normalized_agent["agent_name"] = normalized_agent.get("agent_id", f"agent_{index}")
                logger.debug(f"Using agent_id as agent_name for agent {index}")
            elif target_field == "system_prompt":
                raise ValidationError(f"Agent {index} missing required field: system_prompt")
        
        # Handle tools field
        normalized_agent["tools"] = agent.get("tools", [])
        
        return normalized_agent
    
    @staticmethod
    def validate_messages_dataset(data: Dict[str, Any]) -> MessageDataset:
        """Validate and parse messages dataset."""
        try:
            # Normalize input format
            messages_data = ValidationUtils._normalize_messages_format(data)
            
            # Validate and normalize messages
            messages = messages_data.get("messages", [])
            if not isinstance(messages, list):
                raise ValidationError("Messages must be a list")
            if not messages:
                raise ValidationError("Messages dataset is empty")
            
            normalized_messages = []
            for i, message in enumerate(messages):
                if not isinstance(message, dict):
                    raise ValidationError(f"Message {i} is not a valid object")
                
                normalized_message = ValidationUtils._normalize_message_fields(message, i)
                normalized_messages.append(normalized_message)
            
            # Create final dataset
            final_dataset = {"messages": normalized_messages}
            
            # Validate using Pydantic model
            return MessageDataset(**final_dataset)
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Failed to validate messages dataset: {e}")
            raise ValidationError(f"Invalid messages dataset: {e}")
    
    @staticmethod
    def _normalize_messages_format(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Normalize messages dataset format."""
        if isinstance(data, list):
            logger.debug("Processing messages in direct list format")
            return {"messages": data}
        elif isinstance(data, dict):
            if "messages" in data:
                logger.debug("Processing messages in standard format")
                return data
            elif "conversations" in data:
                # Conversation format - flatten conversations
                conversations = data.get("conversations", [])
                all_messages = []
                for conv in conversations:
                    if isinstance(conv, dict) and "messages" in conv:
                        all_messages.extend(conv["messages"])
                logger.debug(f"Flattened {len(conversations)} conversations into {len(all_messages)} messages")
                return {"messages": all_messages}
            else:
                raise ValidationError("Messages dataset missing 'messages' or 'conversations' key")
        else:
            raise ValidationError("Messages dataset must be a JSON object or array")
    
    @staticmethod
    def _normalize_message_fields(message: Dict[str, Any], index: int) -> Dict[str, Any]:
        """Normalize message fields with type mapping."""
        normalized_message = {}
                
        # Handle ID field
        normalized_message["id"] = message.get("id", f"msg_{index}")
                
        # Handle content field
        normalized_message["content"] = message.get("content", "")
                
        # Handle type field with role mapping
        if "type" in message:
            normalized_message["type"] = message["type"]
        elif "role" in message:
            role_mapping = {
                "user": "human",
                "assistant": "ai",
                "ai": "ai",
                "system": "system",
                "tool": "tool",
                "function": "tool"
            }
            role = message["role"]
            normalized_message["type"] = role_mapping.get(role, "ai")
            logger.debug(f"Mapped role '{role}' to type '{normalized_message['type']}' for message {index}")
        else:
            raise ValidationError(f"Message {index} missing required field: type or role")
                
        # Validate message type
        valid_types = ["human", "ai", "tool", "system"]
        if normalized_message["type"] not in valid_types:
            raise ValidationError(f"Message {index} has invalid type: {normalized_message['type']}")
                
        # Handle optional fields
        optional_fields = ["name", "example", "tool_call_id"]
        for field in optional_fields:
            if field in message:
                normalized_message[field] = message[field]
        
        # Handle special name field logic
        if "name" not in normalized_message:
            if normalized_message["type"] == "ai" and "role" in message and message["role"] != "assistant":
                normalized_message["name"] = message["role"]
            elif normalized_message["type"] == "tool" and "tool_name" in message:
                normalized_message["name"] = message["tool_name"]
                
        # Handle tool calls
        if "tool_calls" in message:
            normalized_message["tool_calls"] = ValidationUtils._normalize_tool_calls(message["tool_calls"])
        
        # Set default values
        normalized_message.setdefault("example", False)
        normalized_message.setdefault("tool_calls", [])
        
        return normalized_message
    
    @staticmethod
    def _normalize_tool_calls(tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize tool calls format."""
        normalized_tool_calls = []
                    
        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                continue
            
            normalized_tool_call = {}
            
            # Handle tool name
            if "name" in tool_call:
                normalized_tool_call["name"] = tool_call["name"]
            elif "function" in tool_call and "name" in tool_call["function"]:
                normalized_tool_call["name"] = tool_call["function"]["name"]
            else:
                continue  # Skip invalid tool call
            
            # Handle tool args
            if "args" in tool_call:
                normalized_tool_call["args"] = tool_call["args"]
            elif "arguments" in tool_call:
                normalized_tool_call["args"] = tool_call["arguments"]
            elif "function" in tool_call and "arguments" in tool_call["function"]:
                # Try to parse arguments string if it's JSON
                args_str = tool_call["function"]["arguments"]
                try:
                    if isinstance(args_str, str):
                        normalized_tool_call["args"] = json.loads(args_str)
                    else:
                        normalized_tool_call["args"] = args_str
                except json.JSONDecodeError:
                    normalized_tool_call["args"] = {"raw_arguments": args_str}
            else:
                normalized_tool_call["args"] = {}
                        
            # Handle tool call ID
            if "id" in tool_call:
                normalized_tool_call["id"] = tool_call["id"]
            elif "function" in tool_call and "id" in tool_call["function"]:
                normalized_tool_call["id"] = tool_call["function"]["id"]
            else:
                normalized_tool_call["id"] = f"call_{len(normalized_tool_calls)}"
                        
            normalized_tool_calls.append(normalized_tool_call)
                    
        return normalized_tool_calls
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """Validate file size."""
        if file_size > max_size:
            raise ValidationError(
                f"File size {file_size} exceeds maximum {max_size} bytes",
                details={"file_size": file_size, "max_size": max_size}
            )
        return True
    
    @staticmethod
    def validate_session_files(
        agents_config: AgentConfig, 
        messages_dataset: MessageDataset
    ) -> Dict[str, Any]:
        """Cross-validate agents config and messages dataset."""
        try:
            validation_results = {
                "agents_count": len(agents_config.agents),
                "messages_count": len(messages_dataset.messages),
                "unique_agents_in_messages": len(messages_dataset.get_unique_agents()),
                "unique_tools_in_messages": len(messages_dataset.get_unique_tools()),
                "warnings": [],
                "recommendations": [],
                "errors": []
            }
            
            # Get agent and tool sets for comparison
            config_agent_names = set(agents_config.get_agent_names())
            message_agent_names = set(messages_dataset.get_unique_agents())
            message_tools = set(messages_dataset.get_unique_tools())
            config_tools = set()
            for agent in agents_config.agents:
                for tool in agent.tools:
                    config_tools.add(tool.name)
            
            # Check for missing agents
            ValidationUtils._check_missing_agents(
                config_agent_names, message_agent_names, validation_results
            )
            
            # Check for missing tools
            ValidationUtils._check_missing_tools(
                config_tools, message_tools, validation_results
                )
            
            # Check conversation flow
            flow_issues = ValidationUtils._check_conversation_flow(messages_dataset)
            validation_results["warnings"].extend(flow_issues)
            
            # Check for critical errors
            if validation_results["errors"]:
                error_msg = "; ".join(validation_results["errors"])
                raise DataConsistencyError(
                    f"Critical data consistency errors: {error_msg}",
                    details={"errors": validation_results["errors"]}
                )
            
            logger.info(f"Cross-validation completed with {len(validation_results['warnings'])} warnings")
            return validation_results
            
        except DataConsistencyError:
            raise
        except Exception as e:
            logger.error(f"Failed to cross-validate session files: {e}")
            raise ValidationError(f"Cross-validation failed: {e}")
    
    @staticmethod
    def _check_missing_agents(config_agents: set, message_agents: set, results: Dict[str, Any]) -> None:
        """Check for missing agents between config and messages."""
        missing_in_config = message_agents - config_agents
        if missing_in_config:
            results["warnings"].append(f"Agents found in messages but not in config: {list(missing_in_config)}")
            results["recommendations"].append("Add missing agents to configuration or correct agent names in messages")
        
        missing_in_messages = config_agents - message_agents
        if missing_in_messages:
            results["warnings"].append(f"Agents in config but not found in messages: {list(missing_in_messages)}")
    
    @staticmethod
    def _check_missing_tools(config_tools: set, message_tools: set, results: Dict[str, Any]) -> None:
        """Check for missing tools between config and messages."""
        undefined_tools = message_tools - config_tools
        if undefined_tools:
            results["warnings"].append(f"Tools used in messages but not defined in config: {list(undefined_tools)}")
            results["recommendations"].append("Add missing tool definitions to agent configurations")
    
    @staticmethod
    def _check_conversation_flow(messages_dataset: MessageDataset) -> List[str]:
        """Check for conversation flow issues."""
        issues = []
        messages = messages_dataset.messages
            
            # Check for tool responses without tool calls
        for i, curr_msg in enumerate(messages):
            if curr_msg.type == MessageType.TOOL and curr_msg.tool_call_id:
                # Find corresponding tool call
                tool_call_found = False
                for j in range(max(0, i-5), i):  # Look back up to 5 messages
                    if messages[j].type == MessageType.AI and any(
                        tc.id == curr_msg.tool_call_id for tc in messages[j].tool_calls
                    ):
                        tool_call_found = True
                        break
                
                if not tool_call_found:
                    issues.append(
                        f"Tool message (ID: {curr_msg.id}) references non-existent tool call ID: {curr_msg.tool_call_id}"
                    )
        
        return issues

