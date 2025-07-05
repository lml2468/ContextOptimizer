'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  ArrowLeftIcon, 
  ArrowDownTrayIcon,
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CogIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { apiClient, downloadFile } from '../../../utils/api';
import { OptimizationResult, SessionInfo } from '../../../types';
import LoadingSpinner from '../../../components/LoadingSpinner';

// Common UI Components
const PageHeader = ({ children }: { children: React.ReactNode }) => (
  <header className="bg-white shadow-sm border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center py-6">
        {children}
      </div>
    </div>
  </header>
);

const BackButton = ({ href, label = "Back" }: { href: string; label?: string }) => (
  <Link href={href} className="flex items-center text-gray-600 hover:text-primary-600 mr-8">
    <ArrowLeftIcon className="h-5 w-5 mr-2" />
    {label}
  </Link>
);

const CenteredMessage = ({ icon: Icon, title, message, action }: {
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  title: string;
  message: string;
  action?: React.ReactNode;
}) => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="text-center">
      <Icon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <h2 className="text-xl font-semibold text-gray-900 mb-2">{title}</h2>
      <p className="text-gray-600 mb-4">{message}</p>
      {action}
    </div>
  </div>
);

const GeneratingMessage = ({ icon: Icon, title, message }: {
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  title: string;
  message: string;
}) => (
  <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div className="text-center">
      <Icon className="h-16 w-16 text-primary-600 mx-auto mb-6" />
      <h2 className="text-2xl font-bold text-gray-900 mb-4">{title}</h2>
      <p className="text-lg text-gray-600 mb-8">{message}</p>
      <div className="animate-pulse bg-gray-200 h-2 rounded-full max-w-md mx-auto"></div>
    </div>
  </main>
);

export default function OptimizationPage({ params }: { params: { sessionId: string } }) {
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const sessionData = await apiClient.getSessionInfo(params.sessionId);
        setSessionInfo(sessionData);

        if (sessionData.has_optimization) {
          const optimizationData = await apiClient.getOptimizationResult(params.sessionId);
          setOptimizationResult(optimizationData);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params.sessionId]);

  const generateOptimization = async () => {
    try {
      setGenerating(true);
      const result = await apiClient.startOptimization(params.sessionId);
      setOptimizationResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate optimization');
    } finally {
      setGenerating(false);
    }
  };

  const downloadOptimization = async () => {
    try {
      const blob = await apiClient.downloadOptimizationResult(params.sessionId);
      downloadFile(blob, 'optimization_result.json');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to download optimization');
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <CenteredMessage
        icon={ExclamationTriangleIcon}
        title="Error"
        message={error}
        action={
          <Link href={`/analysis/${params.sessionId}`} className="btn-primary">
            Back to Analysis
          </Link>
        }
      />
    );
  }

  if (!sessionInfo?.has_analysis) {
    return (
      <CenteredMessage
        icon={InformationCircleIcon}
        title="Analysis Required"
        message="Please complete the analysis first before generating optimization."
        action={
          <Link href={`/analysis/${params.sessionId}`} className="btn-primary">
            View Analysis
          </Link>
        }
      />
    );
  }

  if (!optimizationResult && !generating) {
    return (
      <div className="min-h-screen bg-gray-50">
        <PageHeader>
          <BackButton href={`/analysis/${params.sessionId}`} label="Back to Analysis" />
          <h1 className="text-2xl font-bold text-gradient">Generate Optimization</h1>
        </PageHeader>

        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <CogIcon className="h-16 w-16 text-primary-600 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to Generate Optimization</h2>
            <p className="text-lg text-gray-600 mb-8">
              Based on your analysis results, we'll generate optimized configurations and implementation guides.
            </p>
            <button onClick={generateOptimization} className="btn-primary">
              Generate Optimization
            </button>
          </div>
        </main>
      </div>
    );
  }

  if (generating) {
    return (
      <div className="min-h-screen bg-gray-50">
        <PageHeader>
          <BackButton href={`/analysis/${params.sessionId}`} label="Back to Analysis" />
          <h1 className="text-2xl font-bold text-gradient">Generating Optimization</h1>
        </PageHeader>

        <GeneratingMessage
          icon={ClockIcon}
          title="Generating Your Optimization"
          message="Creating optimized configurations and implementation guides. This may take a few minutes."
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <PageHeader>
        <BackButton href={`/analysis/${params.sessionId}`} label="Back to Analysis" />
        <h1 className="text-2xl font-bold text-gradient">Optimization Results</h1>
        <div className="ml-auto">
          <button onClick={downloadOptimization} className="btn-secondary inline-flex items-center">
            <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
            Download Results
          </button>
        </div>
      </PageHeader>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Expected Improvements */}
        {optimizationResult?.expected_improvements && optimizationResult.expected_improvements.length > 0 && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Expected Improvements</h2>
            <ul className="space-y-2">
              {optimizationResult.expected_improvements.map((improvement, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{improvement}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Optimized Agents */}
        {optimizationResult?.optimized_agents && optimizationResult.optimized_agents.length > 0 && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Optimized Agent Configurations</h2>
            <div className="space-y-6">
              {optimizationResult.optimized_agents.map((agent, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">{agent.agent_name}</h3>
                  
                  {/* Changes Summary */}
                  {agent.changes_summary && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-700 mb-2">Changes Summary:</h4>
                      <div className="bg-blue-50 border border-blue-200 rounded p-3">
                        <p className="text-gray-700 text-sm whitespace-pre-wrap">{agent.changes_summary}</p>
                      </div>
                    </div>
                  )}

                  {/* System Prompt Comparison */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Original System Prompt:</h4>
                      <div className="bg-red-50 border border-red-200 rounded p-3 text-sm">
                        <pre className="whitespace-pre-wrap text-gray-700">{agent.original_system_prompt}</pre>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Optimized System Prompt:</h4>
                      <div className="bg-green-50 border border-green-200 rounded p-3 text-sm">
                        <pre className="whitespace-pre-wrap text-gray-700">{agent.optimized_system_prompt}</pre>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tool Format Recommendations */}
        {optimizationResult?.tool_format_recommendations && optimizationResult.tool_format_recommendations.length > 0 && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Tool Format Recommendations</h2>
            <div className="space-y-6">
              {optimizationResult.tool_format_recommendations.map((recommendation, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{recommendation.tool_name}</h3>
                  <p className="text-gray-600 mb-4">{recommendation.rationale}</p>
                  
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {recommendation.current_format && (
                      <div>
                        <h4 className="font-medium text-gray-700 mb-2">Current Format:</h4>
                        <div className="bg-red-50 border border-red-200 rounded p-3">
                          <pre className="text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap">
                            {recommendation.current_format}
                          </pre>
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Recommended Format:</h4>
                      <div className="bg-green-50 border border-green-200 rounded p-3">
                        <pre className="text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap">
                          {recommendation.recommended_format}
                        </pre>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Implementation Guide */}
        {optimizationResult?.implementation_guide && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Implementation Guide</h2>
            <div className="prose max-w-none">
              <p className="text-gray-700 whitespace-pre-wrap">{optimizationResult.implementation_guide}</p>
            </div>
          </div>
        )}

        {/* Compatibility Notes */}
        {optimizationResult?.compatibility_notes && optimizationResult.compatibility_notes.length > 0 && (
          <div className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Compatibility Notes</h2>
            <ul className="space-y-2">
              {optimizationResult.compatibility_notes.map((note, index) => (
                <li key={index} className="flex items-start">
                  <InformationCircleIcon className="h-5 w-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{note}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
