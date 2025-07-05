'use client';

import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
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
import AppLayout from '../../../components/Layout/AppLayout';
import { PageNavigationManager, NavigationActions } from '../../../utils/navigation';

// Common UI Components
const PageHeader = ({ children }: { children: React.ReactNode }) => (
  <header className="page-header">
    <div className="page-header-content">
      <div className="page-header-inner">
        {children}
      </div>
    </div>
  </header>
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
          <main className="main-content-with-fixed-header max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div className="text-center">
      <Icon className="h-16 w-16 text-primary-600 mx-auto mb-6" />
      <h2 className="text-2xl font-bold text-gray-900 mb-4">{title}</h2>
      <p className="text-lg text-gray-600 mb-8">{message}</p>
      <div className="animate-pulse bg-gray-200 h-2 rounded-full max-w-md mx-auto"></div>
    </div>
  </main>
);

export default function OptimizationPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const router = useRouter();
  const pathname = usePathname();
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);

  useEffect(() => {
    const initializeParams = async () => {
      const resolvedParams = await params;
      setSessionId(resolvedParams.sessionId);
    };
    initializeParams();
  }, [params]);

  useEffect(() => {
    if (!sessionId) return;

    const fetchData = async () => {
      try {
        const sessionData = await apiClient.getSessionInfo(sessionId);
        setSessionInfo(sessionData);

        if (sessionData.has_optimization) {
          const optimizationData = await apiClient.getOptimizationResult(sessionId);
          setOptimizationResult(optimizationData);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [sessionId]);

  const generateOptimization = async () => {
    if (!sessionId) return;
    try {
      setGenerating(true);
      const result = await apiClient.startOptimization(sessionId);
      setOptimizationResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate optimization');
    } finally {
      setGenerating(false);
    }
  };

  const downloadOptimization = async () => {
    if (!sessionId) return;
    try {
      const blob = await apiClient.downloadOptimizationResult(sessionId);
      downloadFile(blob, 'optimization_result.json');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to download optimization');
    }
  };

  if (loading) {
    return (
      <AppLayout currentSessionId={sessionId}>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading optimization...</p>
          </div>
        </div>
      </AppLayout>
    );
  }

  if (error) {
    return (
      <AppLayout currentSessionId={sessionId}>
        <CenteredMessage
          icon={ExclamationTriangleIcon}
          title="Error"
          message={error}
          action={
          <Link href={`/analysis/${sessionId}`} className="btn-primary">
            Back to Analysis
          </Link>
          }
        />
      </AppLayout>
    );
  }

  if (!sessionInfo?.has_analysis) {
    return (
      <AppLayout currentSessionId={sessionId}>
        <CenteredMessage
          icon={InformationCircleIcon}
          title="Analysis Required"
          message="Please complete the analysis first before generating optimization."
          action={
          <Link href={`/analysis/${sessionId}`} className="btn-primary">
            View Analysis
          </Link>
          }
        />
      </AppLayout>
    );
  }

  if (!optimizationResult && !generating) {
    return (
      <AppLayout currentSessionId={sessionId}>
      <div className="min-h-screen bg-gray-50">
          <PageHeader>
            <button
              onClick={() => NavigationActions.navigateBack(router, pathname, sessionId)}
              className="btn-ghost flex items-center mr-8"
            >
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
              {PageNavigationManager.getBackLink(pathname, sessionId).label}
            </button>
            <h1 className="text-2xl font-bold text-gradient">
              {PageNavigationManager.getPageTitle(pathname)}
            </h1>
          </PageHeader>

        <main className="main-content-with-fixed-header max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
      </AppLayout>
    );
  }

  if (generating) {
    return (
      <AppLayout currentSessionId={sessionId}>
      <div className="min-h-screen bg-gray-50">
          <PageHeader>
            <button
              onClick={() => NavigationActions.navigateBack(router, pathname, sessionId)}
              className="btn-ghost flex items-center mr-8"
            >
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
              {PageNavigationManager.getBackLink(pathname, sessionId).label}
            </button>
            <h1 className="text-2xl font-bold text-gradient">
              {PageNavigationManager.getPageTitle(pathname)}
            </h1>
          </PageHeader>

          <GeneratingMessage
            icon={ClockIcon}
            title="Generating Your Optimization"
            message="Creating optimized configurations and implementation guides. This may take a few minutes."
          />
          </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout currentSessionId={sessionId}>
    <div className="min-h-screen bg-gray-50">
        <PageHeader>
            <button
            onClick={() => NavigationActions.navigateBack(router, pathname, sessionId)}
            className="btn-ghost flex items-center mr-8"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-2" />
            {PageNavigationManager.getBackLink(pathname, sessionId).label}
          </button>
          <h1 className="text-2xl font-bold text-gradient">
            {PageNavigationManager.getPageTitle(pathname)}
          </h1>
          <div className="ml-auto">
            <button onClick={downloadOptimization} className="btn-secondary inline-flex items-center">
              <ArrowDownTrayIcon className="h-4 w-4 mr-2" />
              Download Results
            </button>
          </div>
        </PageHeader>

      <main className="main-content-with-fixed-header max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Expected Improvements */}
        {optimizationResult?.expected_improvements && optimizationResult.expected_improvements.length > 0 && (
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Expected Improvements</h2>
            <ul className="space-y-3">
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
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Optimized Agent Configurations</h2>
            <div className="space-y-6">
              {optimizationResult.optimized_agents.map((agent, index) => (
                <div key={index} className="bg-neutral-50 rounded-lg border border-neutral-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">{agent.agent_name}</h3>
                  
                  {/* Changes Summary */}
                  {agent.changes_summary && (
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-700 mb-3">Changes Summary:</h4>
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <p className="text-gray-700 text-sm whitespace-pre-wrap leading-relaxed">{agent.changes_summary}</p>
                      </div>
                    </div>
                  )}

                  {/* System Prompt Comparison */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <span className="w-3 h-3 bg-red-400 rounded-full mr-2"></span>
                        Original System Prompt:
                      </h4>
                      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">{agent.original_system_prompt}</pre>
                      </div>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <span className="w-3 h-3 bg-green-400 rounded-full mr-2"></span>
                        Optimized System Prompt:
                      </h4>
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">{agent.optimized_system_prompt}</pre>
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
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Tool Format Recommendations</h2>
            <div className="space-y-6">
              {optimizationResult.tool_format_recommendations.map((recommendation, index) => (
                <div key={index} className="bg-neutral-50 rounded-lg border border-neutral-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{recommendation.tool_name}</h3>
                  <p className="text-gray-600 mb-4 leading-relaxed">{recommendation.rationale}</p>
                  
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {recommendation.current_format && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                          <span className="w-3 h-3 bg-red-400 rounded-full mr-2"></span>
                          Current Format:
                        </h4>
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                          <pre className="text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap leading-relaxed">
                            {recommendation.current_format}
                              </pre>
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                        <span className="w-3 h-3 bg-green-400 rounded-full mr-2"></span>
                        Recommended Format:
                      </h4>
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <pre className="text-sm text-gray-700 overflow-x-auto whitespace-pre-wrap leading-relaxed">
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
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Implementation Guide</h2>
            <div className="prose max-w-none">
              <div className="bg-neutral-50 rounded-lg border border-neutral-200 p-6">
                <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{optimizationResult.implementation_guide}</p>
              </div>
            </div>
          </div>
        )}

        {/* Compatibility Notes */}
        {optimizationResult?.compatibility_notes && optimizationResult.compatibility_notes.length > 0 && (
          <div className="bg-white rounded-xl border border-neutral-200 p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Compatibility Notes</h2>
            <ul className="space-y-3">
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
    </AppLayout>
  );
}
