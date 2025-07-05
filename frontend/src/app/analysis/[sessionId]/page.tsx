'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
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
import LoadingSpinner from '../../../components/LoadingSpinner';

export default function AnalysisPage({ params }: { params: { sessionId: string } }) {
  const router = useRouter();
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [evaluationReport, setEvaluationReport] = useState<EvaluationReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [optimizationStarting, setOptimizationStarting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get session info
        const sessionData = await apiClient.getSessionInfo(params.sessionId);
        setSessionInfo(sessionData);

        // If analysis is completed, get the report
        if (sessionData.has_analysis) {
          const reportData = await apiClient.getEvaluationReport(params.sessionId);
          setEvaluationReport(reportData);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Poll for updates if analysis is in progress
    const interval = setInterval(() => {
      if (sessionInfo?.status === 'analyzing' || sessionInfo?.status === 'processing') {
        fetchData();
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [params.sessionId, sessionInfo?.status]);

  const startOptimization = async () => {
    setOptimizationStarting(true);
    try {
      const result = await apiClient.startOptimization(params.sessionId);
      router.push(`/optimization/${params.sessionId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start optimization');
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analysis...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/upload" className="btn-primary">
            Start New Analysis
          </Link>
        </div>
      </div>
    );
  }

  if (sessionInfo?.status === 'analyzing') {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center py-6">
              <Link href="/upload" className="flex items-center text-gray-600 hover:text-primary-600 mr-8">
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                Back to Upload
              </Link>
              <h1 className="text-2xl font-bold text-gradient">Analysis in Progress</h1>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <ClockIcon className="h-16 w-16 text-primary-600 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analyzing Your Multi-Agent System</h2>
            <p className="text-lg text-gray-600 mb-8">
              Our AI is analyzing your configuration and conversation data. This typically takes 5-8 minutes.
            </p>
            <div className="animate-pulse bg-gray-200 h-2 rounded-full max-w-md mx-auto"></div>
          </div>
        </main>
      </div>
    );
  }

  if (!evaluationReport) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <InformationCircleIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Available</h2>
          <p className="text-gray-600 mb-4">The analysis report is not yet available.</p>
          <Link href="/upload" className="btn-primary">
            Start New Analysis
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center">
              <Link href="/upload" className="flex items-center text-gray-600 hover:text-primary-600 mr-8">
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                Back to Upload
              </Link>
              <h1 className="text-2xl font-bold text-gradient">Analysis Report</h1>
            </div>
            {sessionInfo?.has_optimization && (
              <Link
                href={`/optimization/${params.sessionId}`}
                className="btn-primary flex items-center"
              >
                View Optimization
                <ArrowRightIcon className="ml-2 h-4 w-4" />
              </Link>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Overall Score */}
        <div className="card mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Overall Score</h2>
              <p className="text-gray-600">{evaluationReport.summary}</p>
            </div>
            <div className="text-right">
              <div className={`text-4xl font-bold ${getScoreColor(evaluationReport.overall_score)}`}>
                {evaluationReport.overall_score.toFixed(1)}
              </div>
              <div className="text-gray-500">out of 10</div>
            </div>
          </div>
        </div>

        {/* Dimension Scores */}
        <div className="card mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-6">Evaluation Dimensions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {evaluationReport.dimensions.map((dimension, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{dimension.name}</h4>
                  <span className={`text-lg font-bold ${getScoreColor(dimension.score)}`}>
                    {dimension.score.toFixed(1)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{dimension.description}</p>
                
                {dimension.issues.length > 0 && (
                  <div className="mb-3">
                    <h5 className="text-xs font-medium text-gray-700 mb-1">Issues:</h5>
                    <ul className="text-xs text-gray-600 space-y-1">
                      {dimension.issues.map((issue, i) => (
                        <li key={i} className="flex items-start">
                          <span className="text-red-400 mr-1">•</span>
                          {issue}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {dimension.recommendations.length > 0 && (
                  <div>
                    <h5 className="text-xs font-medium text-gray-700 mb-1">Recommendations:</h5>
                    <ul className="text-xs text-gray-600 space-y-1">
                      {dimension.recommendations.map((rec, i) => (
                        <li key={i} className="flex items-start">
                          <span className="text-green-400 mr-1">•</span>
                          {rec}
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
          <div className="card mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-6">Priority Issues</h3>
            <div className="space-y-4">
              {evaluationReport.priority_issues.map((issue, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(issue.priority)}`}>
                        {issue.priority.toUpperCase()}
                      </span>
                      <span className="ml-3 font-medium text-gray-900">{issue.category}</span>
                    </div>
                  </div>
                  
                  <p className="text-gray-700 mb-3">{issue.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <h5 className="font-medium text-gray-700 mb-1">Impact:</h5>
                      <p className="text-gray-600">{issue.impact}</p>
                    </div>
                    <div>
                      <h5 className="font-medium text-gray-700 mb-1">Solution:</h5>
                      <p className="text-gray-600">{issue.solution}</p>
                    </div>
                  </div>
                  
                  {issue.affected_agents.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <h5 className="text-xs font-medium text-gray-700 mb-2">Affected Agents:</h5>
                      <div className="flex flex-wrap gap-2">
                        {issue.affected_agents.map((agent, i) => (
                          <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
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
          <div className="card mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Overall Recommendations</h3>
            <ul className="space-y-2">
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
        <div className="text-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Ready for Optimization?</h3>
          <p className="text-gray-600 mb-6">
            Get detailed optimization recommendations and ready-to-use configurations
          </p>
          {sessionInfo?.has_optimization ? (
            <Link
              href={`/optimization/${params.sessionId}`}
              className="btn-primary inline-flex items-center"
            >
              View Optimization
              <ArrowRightIcon className="ml-2 h-4 w-4" />
            </Link>
          ) : (
            <button
              onClick={startOptimization}
              disabled={optimizationStarting}
              className="btn-primary inline-flex items-center"
            >
              {optimizationStarting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Starting Optimization...
                </>
              ) : (
                <>
                  Generate Optimization
                  <ArrowRightIcon className="ml-2 h-4 w-4" />
                </>
              )}
            </button>
          )}
        </div>
      </main>
    </div>
  );
}
