'use client';

import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';
import Link from 'next/link';
import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowLeftIcon 
} from '@heroicons/react/24/outline';
import { apiClient } from '../../utils/api';
import LoadingSpinner from '../../components/LoadingSpinner';

interface UploadState {
  agentsConfig: File | null;
  messagesDataset: File | null;
  uploading: boolean;
  error: string | null;
}

export default function UploadPage() {
  const router = useRouter();
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
      const analysisResult = await apiClient.startAnalysis(
        sessionId
      );

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
    <div
      className={`upload-zone ${file ? 'border-green-300 bg-green-50' : ''}`}
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
          <CheckCircleIcon className="h-12 w-12 text-green-500 mb-4" />
        ) : (
          <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mb-4" />
        )}
        
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-center mb-4">{description}</p>
        
        {file ? (
          <div className="flex items-center text-green-600">
            <DocumentTextIcon className="h-5 w-5 mr-2" />
            <span className="font-medium">{file.name}</span>
          </div>
        ) : (
          <label
            htmlFor={`file-${type}`}
            className="btn-primary cursor-pointer"
          >
            Choose File
          </label>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <Link href="/" className="flex items-center text-gray-600 hover:text-primary-600 mr-8">
              <ArrowLeftIcon className="h-5 w-5 mr-2" />
              Back to Home
            </Link>
            <h1 className="text-2xl font-bold text-gradient">Upload Configuration</h1>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Upload Your Multi-Agent System Configuration
          </h2>
          <p className="text-lg text-gray-600">
            Upload your agent configuration and conversation data to get started with context optimization
          </p>
        </div>

        {state.error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mr-3" />
            <span className="text-red-700">{state.error}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
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
        <div className="text-center">
          <Button
            onClick={handleSubmit}
            disabled={!state.agentsConfig || !state.messagesDataset || state.uploading}
            className={`px-8 py-3 ${
              !state.agentsConfig || !state.messagesDataset || state.uploading
                ? 'opacity-50 cursor-not-allowed'
                : ''
            }`}
          >
            {state.uploading ? (
              <div className="flex items-center">
                <LoadingSpinner size="sm" color="white" className="mr-2" />
                Starting Analysis...
              </div>
            ) : (
              'Start Analysis'
            )}
          </Button>
        </div>

        {/* File Format Info */}
        <div className="mt-12 card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">File Format Requirements</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">agents_config.json</h4>
              <pre className="text-sm text-gray-600 bg-gray-50 p-3 rounded overflow-x-auto">
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
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">messages_dataset.json</h4>
              <pre className="text-sm text-gray-600 bg-gray-50 p-3 rounded overflow-x-auto">
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
