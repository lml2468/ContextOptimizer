'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import AppLayout from '../../components/Layout/AppLayout';
import { SessionInfo } from '../../types';
import { apiClient } from '../../utils/api';
import { 
  ClockIcon, 
  CheckCircleIcon,
  ExclamationCircleIcon,
  CogIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  CloudArrowUpIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { SessionNavigationManager, NavigationActions, PageNavigationManager } from '../../utils/navigation';

// Session Results View Component
const SessionResultsView = ({ 
  session, 
  onViewSession, 
  formatDate, 
  getStatusIcon, 
  getStatusText 
}: {
  session: SessionInfo;
  onViewSession: (session: SessionInfo) => void;
  formatDate: (dateString: string) => string;
  getStatusIcon: (session: SessionInfo) => React.ReactNode;
  getStatusText: (session: SessionInfo) => string;
}) => (
  <div className="space-y-8">
    {/* Session Header */}
    <div className="card-elevated p-8">
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center space-x-4">
          {getStatusIcon(session)}
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">
              {SessionNavigationManager.getDisplayName(session)}
            </h2>
            <p className="text-neutral-600">
              Created: {formatDate(session.created_at)}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <span className={`status-badge ${SessionNavigationManager.getStatusBadgeClass(session)}`}>
            {getStatusText(session)}
          </span>
          <button
            onClick={() => onViewSession(session)}
            className="btn-primary inline-flex items-center"
          >
            View Details
            <ArrowRightIcon className="ml-2 h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="text-center p-4 bg-gradient-to-br from-primary-50 to-primary-100 rounded-xl">
          <div className="text-2xl font-bold text-primary-700 mb-1">
            {session.session_id.slice(0, 8)}
          </div>
          <div className="text-sm font-medium text-primary-600">Session ID</div>
        </div>
        <div className="text-center p-4 bg-gradient-to-br from-accent-50 to-accent-100 rounded-xl">
          <div className="text-2xl font-bold text-accent-700 mb-1">
            {formatDate(session.updated_at).split(' ')[0]}
          </div>
          <div className="text-sm font-medium text-accent-600">Last Updated</div>
        </div>
        <div className="text-center p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-xl">
          <div className="text-2xl font-bold text-green-700 mb-1">
            {session.has_optimization ? 'Complete' : session.has_analysis ? 'Analyzed' : 'Pending'}
          </div>
          <div className="text-sm font-medium text-green-600">Status</div>
        </div>
      </div>

      {session.error_message && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <h4 className="font-medium text-red-800 mb-2">Error Message:</h4>
          <p className="text-red-700">{session.error_message}</p>
        </div>
      )}
    </div>
  </div>
);

// New Session View Component (Upload Interface)
const NewSessionView = ({ onSessionCreated }: { onSessionCreated?: (sessionId: string) => void }) => {
  const router = useRouter();
  const [state, setState] = useState({
    agentsConfig: null as File | null,
    messagesDataset: null as File | null,
    uploading: false,
    error: null as string | null
  });

  const handleFileSelect = useCallback((type: 'agentsConfig' | 'messagesDataset', file: File) => {
    setState(prev => ({
      ...prev,
      [type]: file,
      error: null
    }));
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>, type: 'agentsConfig' | 'messagesDataset') => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    const file = files.find(f => f.name.endsWith('.json'));
    
    if (file) {
      handleFileSelect(type, file);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleSubmit = async () => {
    if (!state.agentsConfig || !state.messagesDataset) {
      setState(prev => ({ ...prev, error: 'Please upload both configuration files' }));
      return;
    }

    setState(prev => ({ ...prev, uploading: true, error: null }));

    try {
      // Upload files and create session
      const uploadResult = await apiClient.uploadFiles(
        state.agentsConfig,
        state.messagesDataset
      );

      const sessionId = uploadResult.session_id;

      // Start analysis
      await apiClient.startAnalysis(sessionId);

      // 如果提供了回调函数，调用它来更新sessions列表
      if (onSessionCreated) {
        onSessionCreated(sessionId);
      } else {
        // 否则跳转到analysis页面
        router.push(`/analysis/${sessionId}`);
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        uploading: false,
        error: error instanceof Error ? error.message : 'An error occurred'
      }));
    }
  };

  const FileUploadZone = ({ 
    type, 
    title, 
    description, 
    file 
  }: { 
    type: 'agentsConfig' | 'messagesDataset';
    title: string;
    description: string;
    file: File | null;
  }) => (
    <div className="card-elevated p-8 hover:shadow-xl transition-all duration-300">
      <div
        className={`upload-zone ${file ? 'border-green-400 bg-green-50/50' : ''}`}
        onDrop={(e) => handleDrop(e, type)}
        onDragOver={handleDragOver}
      >
        <input
          type="file"
          accept=".json"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFileSelect(type, file);
          }}
          className="hidden"
          id={`file-${type}`}
        />
        
        <div className="flex flex-col items-center">
          {file ? (
            <div className="p-4 bg-green-100 rounded-full mb-6">
              <CheckCircleIcon className="h-12 w-12 text-green-600" />
            </div>
          ) : (
            <div className="p-4 bg-gradient-to-br from-primary-100 to-purple-100 rounded-full mb-6">
              <CloudArrowUpIcon className="h-12 w-12 text-primary-600" />
            </div>
          )}
          
          <h3 className="text-xl font-bold text-neutral-900 mb-3">{title}</h3>
          <p className="text-neutral-600 text-center mb-6 leading-relaxed">{description}</p>
          
          {file ? (
            <div className="flex items-center justify-center p-4 bg-green-100 rounded-lg">
              <DocumentTextIcon className="h-5 w-5 text-green-600 mr-2" />
              <span className="font-semibold text-green-800">{file.name}</span>
            </div>
          ) : (
            <label
              htmlFor={`file-${type}`}
              className="btn-primary cursor-pointer"
            >
              Choose File or Drag & Drop
            </label>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-bold text-neutral-900 mb-6">
          Upload Your Multi-Agent System Configuration
        </h2>
        <p className="text-xl text-neutral-600 max-w-3xl mx-auto leading-relaxed">
          Upload your agent configuration and conversation data to get started with AI-powered context optimization
        </p>
      </div>

      {state.error && (
        <div className="mb-12 p-6 bg-red-50 border border-red-200 rounded-xl flex items-center card-elevated">
          <div className="p-2 bg-red-100 rounded-full mr-4">
            <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
          </div>
          <span className="text-red-800 font-medium">{state.error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
        <FileUploadZone
          type="agentsConfig"
          title="Agent Configuration"
          description="Upload your agents_config.json file containing agent definitions, system prompts, and tool configurations"
          file={state.agentsConfig}
        />
        
        <FileUploadZone
          type="messagesDataset"
          title="Messages Dataset"
          description="Upload your messages_dataset.json file containing the complete multi-agent conversation flows"
          file={state.messagesDataset}
        />
      </div>

      {/* Submit Button */}
      <div className="bg-gradient-to-br from-primary-50 to-accent-50 rounded-xl border border-primary-200 p-8 text-center">
        <div className="max-w-2xl mx-auto">
          <h3 className="text-2xl font-bold text-neutral-900 mb-3">Ready to Start Analysis?</h3>
          <p className="text-base text-neutral-600 mb-6 leading-relaxed">
            Our AI will analyze your configuration and provide optimization recommendations
          </p>
          <button
            onClick={handleSubmit}
            disabled={!state.agentsConfig || !state.messagesDataset || state.uploading}
            className="btn-primary inline-flex items-center text-base px-6 py-3"
          >
            {state.uploading ? (
              <>
                <div className="loading-spinner h-4 w-4 mr-2"></div>
                Starting Analysis...
              </>
            ) : (
              'Start Analysis'
            )}
          </button>
        </div>
      </div>

      {/* File Format Info */}
      <div className="mt-16 card-elevated p-8">
        <h3 className="text-2xl font-bold text-neutral-900 mb-8 text-center">File Format Requirements</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="card p-6">
            <h4 className="font-bold text-neutral-900 mb-4 text-lg">agents_config.json</h4>
            <pre className="text-sm text-neutral-600 bg-neutral-50 p-4 rounded-lg overflow-x-auto leading-relaxed">
{`{
  "agents": [
    {
      "agent_id": "agent1",
      "agent_name": "Agent Name",
      "system_prompt": "...",
      "tools": [...]
    }
  ]
}`}
            </pre>
          </div>
          
          <div className="card p-6">
            <h4 className="font-bold text-neutral-900 mb-4 text-lg">messages_dataset.json</h4>
            <pre className="text-sm text-neutral-600 bg-neutral-50 p-4 rounded-lg overflow-x-auto leading-relaxed">
{`{
  "messages": [
    {
      "content": "...",
      "type": "human|ai|tool",
      "name": "agent_name",
      "tool_calls": [...]
    }
  ]
}`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function SessionsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [currentSession, setCurrentSession] = useState<SessionInfo | null>(null);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      await apiClient.getRecentSessions();
      
      // 默认不选择任何session，显示upload界面
      setCurrentSession(null);
    } catch {
      // Handle error silently or show user-friendly message
      setCurrentSession(null);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (session: SessionInfo) => {
    switch (session.status) {
      case 'completed':
        return (
          <div className="p-1.5 bg-green-100 rounded-full">
            <CheckCircleIcon className="h-4 w-4 text-green-600" />
          </div>
        );
      case 'analyzing':
      case 'processing':
        return (
          <div className="p-1.5 bg-blue-100 rounded-full">
            <ClockIcon className="h-4 w-4 text-blue-600 animate-spin" />
          </div>
        );
      case 'error':
      case 'failed':
        return (
          <div className="p-1.5 bg-red-100 rounded-full">
            <ExclamationCircleIcon className="h-4 w-4 text-red-600" />
          </div>
        );
      default:
        return (
          <div className="p-1.5 bg-neutral-100 rounded-full">
            <CogIcon className="h-4 w-4 text-neutral-500" />
          </div>
        );
    }
  };

  const getStatusText = (session: SessionInfo) => {
    return SessionNavigationManager.getStatusText(session);
  };

  const formatDate = (dateString: string) => {
    return SessionNavigationManager.formatDate(dateString, false);
  };

  const handleViewSession = (session: SessionInfo) => {
    NavigationActions.navigateToSession(router, session);
  };

  const handleSessionCreated = async (sessionId: string) => {
    // 重新获取sessions列表
    await fetchSessions();
    
    // 直接跳转到分析页面
    router.push(`/analysis/${sessionId}`);
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="loading-spinner h-12 w-12 mx-auto mb-6"></div>
            <p className="text-neutral-600 text-lg">Loading sessions...</p>
          </div>
        </div>
      </AppLayout>
    );
  }

  // 如果没有sessions，仍然显示正常的sessions页面布局，但右侧显示upload界面
  // 这样用户可以直接创建第一个session

  return (
    <AppLayout currentSessionId={currentSession?.session_id}>
      <div className="min-h-screen">
        {/* Header */}
        <header className="header-blur">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between py-8">
              <div className="flex items-center">
                <button
                  onClick={() => NavigationActions.navigateBack(router, '/sessions')}
                  className="btn-ghost flex items-center mr-8"
                >
                  <ArrowLeftIcon className="h-5 w-5 mr-2" />
                  {PageNavigationManager.getBackLink('/sessions').label}
                </button>
                <h1 className="text-3xl font-bold text-gradient">Recent Sessions</h1>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {currentSession ? (
            <SessionResultsView 
              session={currentSession} 
              onViewSession={handleViewSession}
              formatDate={formatDate}
              getStatusIcon={getStatusIcon}
              getStatusText={getStatusText}
            />
          ) : (
            <NewSessionView onSessionCreated={handleSessionCreated} />
          )}
        </main>
      </div>
    </AppLayout>
  );
} 