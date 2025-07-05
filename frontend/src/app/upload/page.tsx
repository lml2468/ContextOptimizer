'use client';

import { useState, useCallback } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowLeftIcon 
} from '@heroicons/react/24/outline';
import { apiClient } from '../../utils/api';
import { PageNavigationManager, NavigationActions } from '../../utils/navigation';

interface UploadState {
  agentsConfig: File | null;
  messagesDataset: File | null;
  uploading: boolean;
  error: string | null;
}

export default function UploadPage() {
  const router = useRouter();
  const pathname = usePathname();
  const [state, setState] = useState<UploadState>({
    agentsConfig: null,
    messagesDataset: null,
    uploading: false,
    error: null
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

      // Redirect to analysis page
      router.push(`/analysis/${sessionId}`);
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
    <div className="bg-white rounded-xl border border-neutral-200 p-6 hover:border-neutral-300 transition-all duration-300">
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
            <div className="p-3 bg-green-100 rounded-full mb-4">
              <CheckCircleIcon className="h-10 w-10 text-green-600" />
            </div>
          ) : (
            <div className="p-3 bg-gradient-to-br from-primary-100 to-purple-100 rounded-full mb-4">
              <CloudArrowUpIcon className="h-10 w-10 text-primary-600" />
            </div>
          )}
          
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">{title}</h3>
          <p className="text-neutral-600 text-center mb-4 text-sm leading-relaxed">{description}</p>
          
          {file ? (
            <div className="flex items-center justify-center p-3 bg-green-100 rounded-lg">
              <DocumentTextIcon className="h-4 w-4 text-green-600 mr-2" />
              <span className="font-medium text-green-800 text-sm">{file.name}</span>
            </div>
          ) : (
            <label
              htmlFor={`file-${type}`}
              className="btn-primary cursor-pointer text-sm px-4 py-2"
            >
              Choose File or Drag & Drop
            </label>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="header-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <button
              onClick={() => NavigationActions.navigateBack(router, pathname)}
              className="btn-ghost flex items-center mr-6"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-2" />
              {PageNavigationManager.getBackLink(pathname).label}
            </button>
            <h1 className="text-2xl font-bold text-gradient">
              {PageNavigationManager.getPageTitle(pathname)}
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-neutral-900 mb-4">
            Upload Your Multi-Agent System Configuration
          </h2>
          <p className="text-lg text-neutral-600 max-w-3xl mx-auto leading-relaxed">
            Upload your agent configuration and conversation data to get started with AI-powered context optimization
          </p>
        </div>

        {state.error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center">
            <div className="p-2 bg-red-100 rounded-full mr-3">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-600" />
            </div>
            <span className="text-red-800 font-medium">{state.error}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
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
        <div 
          className="relative overflow-hidden rounded-xl p-8 text-center mb-12"
          style={{
            background: 'linear-gradient(135deg, #bfdbfe 0%, #c7d2fe 50%, #e9d5ff 100%)',
            border: '2px solid #8b5cf6',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
          }}
        >
          {/* Background decoration */}
          <div 
            className="absolute inset-0"
            style={{
              background: 'linear-gradient(135deg, rgba(219, 234, 254, 0.5) 0%, rgba(243, 232, 255, 0.5) 100%)'
            }}
          ></div>
          <div 
            className="absolute top-0 right-0 w-32 h-32 rounded-full -translate-y-16 translate-x-16"
            style={{
              background: 'linear-gradient(135deg, rgba(165, 180, 252, 0.3) 0%, rgba(196, 181, 253, 0.3) 100%)'
            }}
          ></div>
          <div 
            className="absolute bottom-0 left-0 w-24 h-24 rounded-full translate-y-12 -translate-x-12"
            style={{
              background: 'linear-gradient(135deg, rgba(147, 197, 253, 0.3) 0%, rgba(165, 180, 252, 0.3) 100%)'
            }}
          ></div>
          
          <div className="relative max-w-2xl mx-auto">
            <div 
              className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-4"
              style={{
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
              }}
            >
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-neutral-900 mb-3">Ready to Start Analysis?</h3>
            <p className="text-base text-neutral-600 mb-6 leading-relaxed">
              Our AI will analyze your configuration and provide optimization recommendations
            </p>
            <button
              onClick={handleSubmit}
              disabled={!state.agentsConfig || !state.messagesDataset || state.uploading}
              className="btn-primary inline-flex items-center text-base px-6 py-3"
              style={{
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                transition: 'box-shadow 0.2s ease-in-out'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
              }}
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
        <div className="bg-white rounded-xl border border-neutral-200 p-6">
          <h3 className="text-xl font-semibold text-neutral-900 mb-6 text-center">File Format Requirements</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-neutral-50 rounded-lg p-4">
              <h4 className="font-semibold text-neutral-900 mb-3">agents_config.json</h4>
              <pre className="text-sm text-neutral-600 bg-white p-3 rounded-lg overflow-x-auto leading-relaxed">
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
            
            <div className="bg-neutral-50 rounded-lg p-4">
              <h4 className="font-semibold text-neutral-900 mb-3">messages_dataset.json</h4>
              <pre className="text-sm text-neutral-600 bg-white p-3 rounded-lg overflow-x-auto leading-relaxed">
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
      </main>
    </div>
  );
}
