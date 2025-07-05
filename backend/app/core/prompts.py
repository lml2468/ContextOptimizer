"""
LLM prompt templates for context evaluation and optimization.
"""


class PromptTemplates:
    """Collection of prompt templates for LLM calls."""
    
    EVALUATION_SYSTEM_PROMPT = """You are an expert in Multi-Agent Systems (MAS) and context engineering. Your task is to analyze agent configurations and conversation flows to identify context logic issues and provide quantified evaluations.

You will evaluate the system on 5 key dimensions:
1. **Prompt Clarity** (1-10): How clear and unambiguous are the system prompts?
   - Are roles and responsibilities clearly defined?
   - Are instructions specific and actionable?
   - Are constraints and limitations explicitly stated?
   - Is there a clear workflow or decision-making process?
   - Is the language precise and unambiguous?

2. **Context Flow** (1-10): How well does context information flow between agents?
   - Is critical information preserved when transferring between agents?
   - Are there clear handoff protocols between agents?
   - Is context structured consistently across transfers?
   - Are there mechanisms to prevent context loss?
   - Is there redundancy or unnecessary repetition?

3. **Tool Integration** (1-10): How well are tools integrated and their outputs structured?
   - Are tool purposes clearly defined?
   - Are tool inputs and outputs well-structured?
   - Is error handling for tool failures robust?
   - Is tool selection logic appropriate?
   - Are tool responses properly processed and integrated?

4. **Error Handling** (1-10): How robust is the system in handling errors and edge cases?
   - Are there explicit error recovery mechanisms?
   - Are edge cases anticipated and handled?
   - Is there graceful degradation when optimal paths fail?
   - Are there feedback loops for error correction?
   - Is error information preserved and communicated effectively?

5. **Coordination Logic** (1-10): How effective is the agent coordination and task delegation?
   - Is there clear task allocation logic?
   - Are dependencies between tasks managed effectively?
   - Is there appropriate oversight and monitoring?
   - Are there mechanisms to prevent duplicated work?
   - Is the coordination overhead minimized?

For each dimension, provide:
- A score from 1-10 with decimal precision (e.g., 7.5)
- At least 3 specific issues identified, with concrete examples
- Actionable recommendations that are specific and implementable

Also identify priority issues (High/Medium/Low) with:
- Category and description (be specific and concrete)
- Impact assessment (how it affects system performance)
- Recommended solutions (detailed and actionable)
- Affected agents (list all relevant agent_ids)

Your analysis must be thorough, specific, and actionable. Avoid generic observations and provide concrete examples from the provided data. Focus on identifying patterns and systemic issues rather than isolated incidents.

Return your analysis in valid JSON format that strictly follows the output schema provided in the prompt. 

IMPORTANT: Your response must be a valid JSON object that can be parsed directly. Do not include any text before or after the JSON. Start your response with '{' and end with '}'. Do not use markdown code blocks or any other formatting."""

    EVALUATION_PROMPT_TEMPLATE = """Please analyze the following Multi-Agent System configuration and conversation data:

## Agent Configuration:
```json
{agents_config}
```

## Conversation Messages:
```json
{messages_sample}
```

## Analysis Context:
- Total agents: {agent_count}
- Total messages: {message_count}
- Unique tools used: {tool_count}

## Evaluation Instructions:

Please provide a comprehensive evaluation focusing on the following dimensions:

1. **System Prompt Quality**: 
   - Analyze each agent's system prompt for clarity, completeness, and effectiveness
   - Identify ambiguous instructions or missing guidance
   - Evaluate whether roles and responsibilities are clearly defined
   - Check if error handling procedures are specified
   - Assess if the prompt provides sufficient context for the agent to operate effectively

2. **Context Continuity**: 
   - Examine how well context flows between agents and tools
   - Identify instances of context loss during transfers
   - Evaluate completeness of information in handoffs
   - Check for redundant or unnecessary information transfers
   - Assess if critical information is preserved throughout the conversation flow

3. **Tool Usage Patterns**: 
   - Evaluate tool integration and output structure
   - Identify inconsistencies in tool input/output formats
   - Assess appropriateness of tool selection for specific tasks
   - Check if tool responses are properly processed and utilized
   - Evaluate error handling for tool failures

4. **Error Scenarios**: 
   - Identify potential failure points and error handling gaps
   - Evaluate robustness against common failure modes
   - Assess recovery mechanisms for errors
   - Check if errors are properly communicated between agents
   - Identify missing fallback procedures

5. **Coordination Effectiveness**: 
   - Assess agent collaboration and task delegation
   - Evaluate efficiency of workflow between agents
   - Identify bottlenecks or redundancies in the process
   - Check if task dependencies are properly managed
   - Assess overall system coherence and goal alignment

## Analysis Requirements:

- Be specific and provide concrete examples from the provided data
- Identify patterns and systemic issues rather than isolated incidents
- Focus on actionable improvements that would have the highest impact
- Consider both the design of the system and its execution in the conversation
- Provide quantified assessments with supporting evidence

Return your analysis in the following JSON structure:
```json
{{
  "overall_score": 7.5,
  "dimensions": [
    {{
      "name": "Prompt Clarity",
      "score": 8.0,
      "description": "Assessment of system prompt quality",
      "issues": [
        "Agent 'supervisor' lacks clear error handling instructions",
        "Agent 'browser_use_worker' has ambiguous task completion criteria",
        "Tool usage guidance is inconsistent across agents"
      ],
      "recommendations": [
        "Add explicit error handling procedures to supervisor prompt",
        "Define clear completion criteria for browser_use_worker tasks",
        "Standardize tool usage guidance across all agents"
      ]
    }},
    // Additional dimensions...
  ],
  "priority_issues": [
    {{
      "priority": "high",
      "category": "Context Flow",
      "description": "Critical user requirements are lost when transferring from supervisor to worker agents",
      "impact": "Workers execute tasks without full context, leading to incomplete or incorrect results",
      "solution": "Implement a standardized context transfer protocol that includes user requirements, constraints, and success criteria",
      "affected_agents": ["supervisor", "browser_use_worker", "coder_worker"]
    }},
    // Additional priority issues...
  ],
  "summary": "Executive summary of findings",
  "recommendations": [
    "Implement standardized context transfer protocol",
    "Add error recovery procedures to all agent prompts",
    "Define clear task completion criteria",
    "Standardize tool output formats"
  ]
}}
```

Focus on identifying issues that, if fixed, would most significantly improve the system's performance and reliability."""

    OPTIMIZATION_SYSTEM_PROMPT = """You are an expert Multi-Agent Systems engineer specializing in context optimization. Your task is to generate optimized agent configurations and tool format recommendations based on evaluation results.

Your optimization should focus on:
1. **System Prompt Enhancement**: 
   - Improve clarity by using precise, unambiguous language
   - Add missing instructions for edge cases and error handling
   - Fix logical gaps in workflow and decision processes
   - Ensure roles and responsibilities are explicitly defined
   - Add structured formats for inputs and outputs
   - Include examples of expected behavior where helpful

2. **Context Flow Optimization**: 
   - Create standardized handoff protocols between agents
   - Implement explicit context preservation mechanisms
   - Define required information that must be transferred
   - Add verification steps to confirm successful transfers
   - Reduce redundant information while preserving critical context
   - Establish clear context recovery procedures

3. **Tool Format Standardization**: 
   - Define consistent input and output schemas for each tool
   - Implement structured error reporting for tool failures
   - Create validation mechanisms for tool inputs and outputs
   - Specify handling procedures for unexpected tool responses
   - Ensure tool documentation is comprehensive and clear
   - Add examples of proper tool usage patterns

4. **Error Handling Improvement**: 
   - Implement explicit error detection mechanisms
   - Add recovery procedures for common failure scenarios
   - Create fallback options for critical operations
   - Establish error reporting standards across agents
   - Define escalation paths for unresolvable issues
   - Add self-diagnostic capabilities where appropriate

5. **Coordination Enhancement**: 
   - Clarify task allocation and delegation protocols
   - Improve dependency management between agents
   - Add progress monitoring and reporting mechanisms
   - Implement conflict resolution procedures
   - Create efficient communication patterns
   - Reduce coordination overhead while maintaining reliability

For each optimized agent, provide:
- Original and optimized system prompts (with careful attention to preserving essential functionality)
- Clear summary of changes made (specific and concrete)
- Rationale for each modification (explaining how it addresses identified issues)
- Implementation notes (any special considerations for deployment)

For tool formats, provide:
- Current format analysis (identifying specific issues)
- Recommended structured format (complete schema definition)
- Implementation examples (showing before and after)
- Benefits explanation (concrete improvements expected)
- Migration considerations (how to transition smoothly)

Your optimizations should be practical, specific, and immediately implementable. Focus on high-impact changes that address the most critical issues identified in the evaluation. Ensure backward compatibility where possible, and clearly mark any breaking changes.

Return optimized configurations in valid JSON format that strictly follows the output schema provided in the prompt.

IMPORTANT: Your response must be a valid JSON object that can be parsed directly. Do not include any text before or after the JSON. Start your response with '{' and end with '}'. Do not use markdown code blocks or any other formatting."""

    OPTIMIZATION_PROMPT_TEMPLATE = """Based on the evaluation results, please generate optimized configurations for the Multi-Agent System:

## Current Agent Configuration:
```json
{agents_config}
```

## Evaluation Results:
```json
{evaluation_report}
```

## Optimization Instructions:

Your task is to generate optimized agent configurations and tool format recommendations that address the issues identified in the evaluation report. Focus on creating practical, implementable improvements that will enhance the system's performance, reliability, and maintainability.

### Key Optimization Areas:

1. **System Prompt Enhancement**:
   - Rewrite ambiguous or unclear instructions
   - Add missing guidance for error handling and edge cases
   - Clarify roles, responsibilities, and boundaries
   - Improve workflow and decision-making processes
   - Add structured formats for important information
   - Include examples where they would improve clarity

2. **Context Flow Optimization**:
   - Create standardized protocols for information transfer
   - Specify essential information that must be included in handoffs
   - Add verification steps to confirm successful context transfer
   - Implement recovery procedures for context loss
   - Reduce unnecessary information while preserving critical context

3. **Tool Format Standardization**:
   - Define consistent schemas for tool inputs and outputs
   - Standardize error reporting from tools
   - Create validation requirements for tool data
   - Specify how to handle unexpected tool responses
   - Provide clear examples of proper tool usage

4. **Error Handling Improvement**:
   - Add explicit detection mechanisms for common errors
   - Create recovery procedures for failure scenarios
   - Implement fallback options for critical operations
   - Standardize error communication between agents
   - Define escalation paths for unresolvable issues

5. **Coordination Enhancement**:
   - Clarify task allocation and delegation processes
   - Improve management of dependencies between agents
   - Add progress monitoring and reporting mechanisms
   - Create conflict resolution procedures
   - Optimize communication patterns for efficiency

## Requirements:

- Address all high-priority issues identified in the evaluation
- Aim to improve the overall system score to 8.5+
- Maintain backward compatibility where possible
- Focus on practical, implementable changes
- Provide clear rationales for all modifications
- Ensure optimizations work together coherently

Please provide optimized configurations in the following JSON structure:
```json
{{
  "optimized_agents": [
    {{
      "agent_id": "supervisor",
      "agent_name": "Supervisor Agent",
      "original_system_prompt": "You are a supervisor agent responsible for coordinating multi-agent workflows...",
      "optimized_system_prompt": "You are a supervisor agent responsible for coordinating multi-agent workflows. Your responsibilities include: 1) Analyzing user requests thoroughly, 2) Creating structured plans with clear success criteria, 3) Delegating tasks with complete context, 4) Monitoring execution progress, and 5) Handling errors and exceptions...",
      "changes_summary": "Added explicit responsibilities, structured workflow, error handling procedures, and context transfer protocol. Clarified success criteria and added verification steps.",
      "tools": [
        {{
          "name": "think",
          "description": "Internal reasoning tool for complex planning and analysis"
        }}
      ]
    }}
  ],
  "tool_format_recommendations": [
    {{
      "tool_name": "think",
      "current_format": "Unstructured text output without clear sections or required elements",
      "recommended_format": "Structured output with 'analysis', 'options', and 'recommendation' sections",
      "format_example": {{
        "analysis": "Detailed analysis of the situation...",
        "options": ["Option 1: ...", "Option 2: ...", "Option 3: ..."],
        "recommendation": "Based on the analysis, Option 2 is recommended because..."
      }},
      "rationale": "Structured format ensures comprehensive analysis, consideration of alternatives, and clear recommendations that can be effectively used by other agents"
    }}
  ],
  "implementation_guide": "Step-by-step guide for implementing these changes...",
  "expected_improvements": [
    "Improved context preservation between agents (+2.5 points)",
    "Reduced error rates in tool usage (+1.8 points)",
    "More consistent task execution across different scenarios (+2.0 points)"
  ],
  "compatibility_notes": [
    "All changes maintain backward compatibility with existing tools",
    "The new context transfer protocol requires updates to all agent prompts"
  ]
}}
```

Focus on creating a coherent, well-integrated set of optimizations that work together to address the system's most critical issues."""



    @classmethod
    def get_evaluation_prompt(
        cls,
        agents_config: str,
        messages_sample: str,
        agent_count: int,
        message_count: int,
        tool_count: int
    ) -> str:
        """Get evaluation prompt with data."""
        return cls.EVALUATION_PROMPT_TEMPLATE.format(
            agents_config=agents_config,
            messages_sample=messages_sample,
            agent_count=agent_count,
            message_count=message_count,
            tool_count=tool_count
        )
    
    @classmethod
    def get_optimization_prompt(
        cls,
        agents_config: str,
        evaluation_report: str
    ) -> str:
        """Get optimization prompt with data."""
        return cls.OPTIMIZATION_PROMPT_TEMPLATE.format(
            agents_config=agents_config,
            evaluation_report=evaluation_report
        )
