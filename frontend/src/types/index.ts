// API Response Types
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Session Types
export interface SessionInfo {
  session_id: string;
  status: 'created' | 'uploaded' | 'analyzing' | 'analyzed' | 'optimizing' | 'processing' | 'completed' | 'failed' | 'error';
  has_files: boolean;
  has_analysis: boolean;
  has_optimization: boolean;
  created_at: string;
  updated_at: string;
  files?: {
    agents_config: {
      filename: string;
      size_bytes: number;
      size_human: string;
      is_json: boolean;
    };
    messages_dataset: {
      filename: string;
      size_bytes: number;
      size_human: string;
      is_json: boolean;
    };
  };
  error_message?: string;
}

// Upload Types
export interface UploadRequest {
  agents_config: File;
  messages_dataset: File;
}

export interface UploadResponse {
  session_id: string;
  message: string;
}

// Analysis Types
export interface AnalysisRequest {
  session_id: string;
}

export interface EvaluationDimension {
  name: string;
  score: number;
  description: string;
  issues: string[];
  recommendations: string[];
}

export interface PriorityIssue {
  priority: 'high' | 'medium' | 'low';
  category: string;
  description: string;
  impact: string;
  solution: string;
  affected_agents: string[];
}

export interface EvaluationReport {
  session_id: string;
  overall_score: number;
  dimensions: EvaluationDimension[];
  priority_issues: PriorityIssue[];
  summary: string;
  recommendations: string[];
  generated_at: string;
}

// Optimization Types
export interface OptimizationRequest {
  session_id: string;
}

export interface OptimizedAgent {
  agent_id: string;
  agent_name: string;
  original_system_prompt: string;
  optimized_system_prompt: string;
  changes_summary: string;
  tools: AgentTool[];
}

export interface ToolFormatRecommendation {
  tool_name: string;
  current_format?: string;
  recommended_format: string;
  format_example: Record<string, unknown>;
  rationale: string;
}

export interface OptimizationResult {
  session_id: string;
  optimized_agents: OptimizedAgent[];
  tool_format_recommendations: ToolFormatRecommendation[];
  implementation_guide: string;
  expected_improvements: string[];
  compatibility_notes: string[];
  generated_at: string;
}

// Agent Configuration Types
export interface AgentTool {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

export interface AgentConfig {
  id: string;
  name: string;
  system_prompt: string;
  tools: AgentTool[];
}

export interface AgentsConfigFile {
  agents: AgentConfig[];
}

// Message Types
export interface ToolCall {
  id: string;
  type: string;
  function: {
    name: string;
    arguments: string;
  };
}

export interface Message {
  content: string;
  type: 'human' | 'ai' | 'tool';
  name?: string;
  tool_calls?: ToolCall[];
  tool_call_id?: string;
}

export interface MessagesDatasetFile {
  messages: Message[];
}
