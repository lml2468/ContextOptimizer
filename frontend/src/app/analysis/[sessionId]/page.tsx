'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { 
  ArrowLeftIcon, 
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  ArrowRightIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { apiClient } from '../../../utils/api';
import { EvaluationReport, SessionInfo } from '../../../types';
import AppLayout from '../../../components/Layout/AppLayout';
import { PageNavigationManager, NavigationActions } from '../../../utils/navigation';

export default function AnalysisPage({ params }: { params: Promise<{ sessionId: string }> }) {
  const router = useRouter();
  const pathname = usePathname();
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [evaluationReport, setEvaluationReport] = useState<EvaluationReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [optimizationStarting, setOptimizationStarting] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const [progressStage, setProgressStage] = useState<'analyzing' | 'optimizing' | 'completed'>('analyzing');
  const [progressPercentage, setProgressPercentage] = useState(0);

  useEffect(() => {
    const initializeParams = async () => {
      const resolvedParams = await params;
      setSessionId(resolvedParams.sessionId);
    };
    initializeParams();
  }, [params]);

  // Fetch session data and evaluation report
  const fetchData = useCallback(async () => {
    if (!sessionId) return;

    try {
      const sessionData = await apiClient.getSessionInfo(sessionId);
      setSessionInfo(sessionData);

      if (sessionData.has_analysis) {
        const reportData = await apiClient.getEvaluationReport(sessionId);
        setEvaluationReport(reportData);
      }

      // Update progress based on session status
      if (sessionData.status === 'analyzing') {
        setProgressStage('analyzing');
        setProgressPercentage(33);
      } else if (sessionData.status === 'analyzed') {
        setProgressStage('optimizing');
        setProgressPercentage(66);
      } else if (sessionData.status === 'completed') {
        setProgressStage('completed');
        setProgressPercentage(100);
      }

      return sessionData;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      return null;
    }
  }, [sessionId]);

  // Initial data fetch
  useEffect(() => {
    if (!sessionId) return;

    const initialFetch = async () => {
      await fetchData();
      setLoading(false);
    };

    initialFetch();
  }, [sessionId, fetchData]);

  // Polling for progress updates
  useEffect(() => {
    if (!sessionId || loading) return;

    const pollInterval = setInterval(async () => {
      const sessionData = await fetchData();
      
      if (sessionData) {
        // Auto-redirect when analysis is complete
        if (sessionData.status === 'completed' && sessionData.has_analysis) {
          // Small delay to show completion state
          setTimeout(() => {
            clearInterval(pollInterval);
            // Stay on the analysis page to show results instead of redirecting
          }, 1000);
        }
        
        // Stop polling if there's an error
        if (sessionData.status === 'error') {
          clearInterval(pollInterval);
        }
      }
    }, 3000); // Poll every 3 seconds

    // Cleanup interval on unmount
    return () => clearInterval(pollInterval);
  }, [sessionId, loading, fetchData]);

  const startOptimization = async () => {
    if (!sessionId) return;
    
    setOptimizationStarting(true);
    try {
      await apiClient.startOptimization(sessionId);
      // Refresh session info to get updated has_optimization status
      const updatedSessionInfo = await apiClient.getSessionInfo(sessionId);
      setSessionInfo(updatedSessionInfo);
      
      // Navigate to optimization page
      router.push(`/optimization/${sessionId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start optimization');
    } finally {
      setOptimizationStarting(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressMessage = () => {
    switch (progressStage) {
      case 'analyzing':
        return 'Analyzing your configuration and conversation data...';
      case 'optimizing':
        return 'Generating optimization recommendations...';
      case 'completed':
        return 'Analysis complete! Loading results...';
      default:
        return 'Processing your data...';
    }
  };

  if (loading) {
    return (
      <AppLayout currentSessionId={sessionId || undefined}>
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analysis...</p>
        </div>
      </div>
      </AppLayout>
    );
  }

  if (error) {
    return (
      <AppLayout currentSessionId={sessionId || undefined}>
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/sessions" className="btn-primary">
            Start New Analysis
          </Link>
        </div>
      </div>
      </AppLayout>
    );
  }

  if (sessionInfo?.status === 'analyzing' || sessionInfo?.status === 'analyzed') {
    return (
      <AppLayout currentSessionId={sessionId || undefined}>
        <div className="min-h-screen">
          <header className="page-header">
          <div className="page-header-content">
              <div className="page-header-inner">
                <h1 className="text-3xl font-bold text-gradient">Analysis in Progress</h1>
            </div>
          </div>
        </header>

          <main className="main-content-with-fixed-header max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
              <div className="card-elevated max-w-2xl mx-auto p-12">
                <div className="mb-8">
                  <div className="p-6 bg-gradient-to-br from-primary-100 to-accent-100 rounded-full w-24 h-24 mx-auto mb-6">
                    <ClockIcon className="h-12 w-12 text-primary-600 mx-auto animate-spin" />
                  </div>
                  <h2 className="text-3xl font-bold text-neutral-900 mb-4">Analyzing Your Multi-Agent System</h2>
                  <p className="text-lg text-neutral-600 mb-8 leading-relaxed">
                    {getProgressMessage()}
                  </p>
                </div>
                <div className="progress-bar mb-4">
                  <div 
                    className="progress-fill transition-all duration-1000 ease-out" 
                    style={{ width: `${progressPercentage}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-sm text-neutral-500 mb-4">
                  <span className={progressStage === 'analyzing' ? 'text-primary-600 font-medium' : ''}>
                    Analysis
                  </span>
                  <span className={progressStage === 'optimizing' ? 'text-primary-600 font-medium' : ''}>
                    Optimization
                  </span>
                  <span className={progressStage === 'completed' ? 'text-primary-600 font-medium' : ''}>
                    Complete
                  </span>
                </div>
                <p className="text-sm text-neutral-500">
                  {progressPercentage}% complete • This typically takes 2-3 minutes
                </p>
              </div>
          </div>
        </main>
      </div>
      </AppLayout>
    );
  }

  if (!evaluationReport) {
    return (
      <AppLayout currentSessionId={sessionId || undefined}>
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <InformationCircleIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Available</h2>
          <p className="text-gray-600 mb-4">The analysis report is not yet available.</p>
            <Link href="/sessions" className="btn-primary">
              New Session
          </Link>
        </div>
      </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout currentSessionId={sessionId || undefined}>
      <div className="min-h-screen">
      {/* Header */}
        <header className="page-header">
        <div className="page-header-content">
            <div className="page-header-inner justify-between">
            <div className="flex items-center">
                <button
                  onClick={() => NavigationActions.navigateBack(router, pathname, sessionId)}
                  className="btn-ghost flex items-center mr-8"
                >
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                  {PageNavigationManager.getBackLink(pathname, sessionId).label}
                </button>
                <h1 className="text-3xl font-bold text-gradient">
                  {PageNavigationManager.getPageTitle(pathname)}
                </h1>
            </div>
            {sessionInfo?.has_optimization && (
              <Link
                href={`/optimization/${sessionId}`}
                className="btn-primary flex items-center"
              >
                View Optimization
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
            )}
          </div>
        </div>
      </header>

      <main className="main-content-with-fixed-header max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overall Score */}
        <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-neutral-900 mb-3">Overall Score</h2>
              <p className="text-base text-neutral-600 leading-relaxed">{evaluationReport.summary}</p>
            </div>
            <div className="text-center ml-8">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-primary-100 to-accent-100 rounded-full flex items-center justify-center mb-2">
                  <div className={`text-2xl font-bold ${getScoreColor(evaluationReport.overall_score)}`}>
                {evaluationReport.overall_score.toFixed(1)}
                  </div>
                </div>
                <div className="text-sm font-medium text-neutral-500">out of 10</div>
              </div>
            </div>
          </div>
        </div>

        {/* Dimension Scores */}
        <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
          <h3 className="text-xl font-bold text-neutral-900 mb-6">Evaluation Dimensions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {evaluationReport.dimensions.map((dimension, index) => (
              <div key={index} className="bg-neutral-50 rounded-lg border border-neutral-200 p-5 hover:bg-neutral-100 transition-colors duration-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-neutral-900 text-base">{dimension.name}</h4>
                  <div className="text-center">
                    <div className={`text-xl font-bold ${getScoreColor(dimension.score)}`}>
                    {dimension.score.toFixed(1)}
                    </div>
                    <div className="text-xs text-neutral-500">/ 10</div>
                  </div>
                </div>
                <p className="text-sm text-neutral-600 mb-3 leading-relaxed">{dimension.description}</p>
                
                {dimension.issues.length > 0 && (
                  <div className="mb-3">
                    <h5 className="text-xs font-semibold text-red-700 mb-2 uppercase tracking-wide">Issues:</h5>
                    <ul className="text-sm text-neutral-600 space-y-1">
                      {dimension.issues.map((issue, i) => (
                        <li key={i} className="flex items-start">
                          <span className="text-red-500 mr-2 mt-1 flex-shrink-0">•</span>
                          <span>{issue}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {dimension.recommendations.length > 0 && (
                  <div>
                    <h5 className="text-xs font-semibold text-green-700 mb-2 uppercase tracking-wide">Recommendations:</h5>
                    <ul className="text-sm text-neutral-600 space-y-1">
                      {dimension.recommendations.map((rec, i) => (
                        <li key={i} className="flex items-start">
                          <span className="text-green-500 mr-2 mt-1 flex-shrink-0">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Priority Issues */}
        {evaluationReport.priority_issues.length > 0 && (
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h3 className="text-xl font-bold text-neutral-900 mb-6">Priority Issues</h3>
            <div className="space-y-4">
              {evaluationReport.priority_issues.map((issue, index) => (
                <div key={index} className="bg-red-50 rounded-lg border border-red-200 border-l-4 border-l-red-400 p-6">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center">
                      <span className={`status-badge ${getPriorityColor(issue.priority)}`}>
                        {issue.priority.toUpperCase()}
                      </span>
                      <span className="ml-3 text-lg font-semibold text-neutral-900">{issue.category}</span>
                    </div>
                  </div>
                  
                  <p className="text-neutral-700 mb-4 leading-relaxed">{issue.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <h5 className="font-semibold text-gray-700 mb-1">Impact:</h5>
                      <p className="text-gray-600">{issue.impact}</p>
                    </div>
                    <div>
                      <h5 className="font-semibold text-gray-700 mb-1">Solution:</h5>
                      <p className="text-gray-600">{issue.solution}</p>
                    </div>
                  </div>
                  
                  {issue.affected_agents.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-red-200">
                      <h5 className="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">Affected Agents:</h5>
                      <div className="flex flex-wrap gap-2">
                        {issue.affected_agents.map((agent, i) => (
                          <span key={i} className="px-2 py-1 bg-white border border-red-200 text-gray-700 rounded text-xs">
                            {agent}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Overall Recommendations */}
        {evaluationReport.recommendations.length > 0 && (
          <div className="bg-white rounded-xl border border-neutral-200 p-8 mb-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Overall Recommendations</h3>
            <ul className="space-y-3">
              {evaluationReport.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Next Steps */}
        <div className="bg-gradient-to-br from-primary-50 to-accent-50 rounded-xl border border-primary-200 p-8 text-center">
          <div className="max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-neutral-900 mb-3">Ready for Optimization?</h3>
            <p className="text-base text-neutral-600 mb-6 leading-relaxed">
              Get detailed optimization recommendations and ready-to-use configurations tailored to your system
          </p>
          {sessionInfo?.has_optimization ? (
            <Link
              href={`/optimization/${sessionId}`}
                className="btn-primary inline-flex items-center text-base px-6 py-3"
            >
                View Optimization Results
                <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          ) : (
            <button
              onClick={startOptimization}
              disabled={optimizationStarting}
                className="btn-primary inline-flex items-center text-base px-6 py-3"
            >
              {optimizationStarting ? (
                <>
                    <div className="loading-spinner h-4 w-4 mr-2"></div>
                  Starting Optimization...
                </>
              ) : (
                <>
                  Generate Optimization
                    <ArrowRightIcon className="ml-2 h-5 w-5" />
                </>
              )}
            </button>
          )}
          </div>
        </div>
      </main>
    </div>
    </AppLayout>
  );
}
