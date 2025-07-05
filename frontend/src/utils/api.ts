import { 
  ApiResponse, 
  SessionInfo, 
  EvaluationReport, 
  OptimizationResult 
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  private async downloadRequest(endpoint: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}${endpoint}`);
    if (!response.ok) {
      throw new Error(`Download failed: HTTP ${response.status}`);
    }
    return response.blob();
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request('/api/v1/health');
  }

  // Session management
  async getSessionInfo(sessionId: string): Promise<SessionInfo> {
    return this.request(`/api/v1/session/${sessionId}`);
  }

  async listSessions(): Promise<SessionInfo[]> {
    return this.request('/api/v1/sessions');
  }

  async getRecentSessions(limit: number = 20): Promise<SessionInfo[]> {
    return this.request(`/api/v1/sessions/recent?limit=${limit}`);
  }

  async deleteSession(sessionId: string): Promise<{ success: boolean }> {
    return this.request(`/api/v1/session/${sessionId}`, { method: 'DELETE' });
  }

  // File upload
  async uploadFiles(agentsConfig: File, messagesDataset: File): Promise<SessionInfo> {
    const formData = new FormData();
    formData.append('agents_config', agentsConfig);
    formData.append('messages_dataset', messagesDataset);

    const response = await fetch(`${this.baseUrl}/api/v1/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || `Upload failed: HTTP ${response.status}`);
    }

    return response.json();
  }

  // Analysis
  async startAnalysis(sessionId: string, focusAreas: string[] = []): Promise<ApiResponse<unknown>> {
    return this.request(`/api/v1/analyze`, {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, focus_areas: focusAreas }),
    });
  }

  async getEvaluationReport(sessionId: string): Promise<EvaluationReport> {
    return this.request(`/api/v1/analysis/${sessionId}`);
  }

  // Optimization
  async startOptimization(
    sessionId: string,
    focusAreas: string[] = [],
    optimizationLevel: 'conservative' | 'balanced' | 'aggressive' = 'balanced'
  ): Promise<OptimizationResult> {
    return this.request(`/api/v1/optimize/${sessionId}`, {
      method: 'POST',
      body: JSON.stringify({ focus_areas: focusAreas, optimization_level: optimizationLevel }),
    });
  }

  async getOptimizationResult(sessionId: string): Promise<OptimizationResult> {
    return this.request(`/api/v1/optimization/${sessionId}`);
  }

  // File downloads
  async downloadEvaluationReport(sessionId: string): Promise<Blob> {
    return this.downloadRequest(`/api/v1/sessions/${sessionId}/evaluation/download`);
  }

  async downloadOptimizationResult(sessionId: string): Promise<Blob> {
    return this.downloadRequest(`/api/v1/sessions/${sessionId}/optimization/download`);
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Utility functions
export const downloadFile = (blob: Blob, filename: string) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export const validateJsonFile = (file: File): Promise<boolean> => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        JSON.parse(e.target?.result as string);
        resolve(true);
      } catch {
        resolve(false);
      }
    };
    reader.onerror = () => resolve(false);
    reader.readAsText(file);
  });
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
};
