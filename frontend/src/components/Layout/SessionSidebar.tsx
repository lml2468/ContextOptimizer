'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  CogIcon,
  PlusIcon,
  TrashIcon,
  EyeIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { SessionInfo } from '../../types';
import { apiClient } from '../../utils/api';
import { SessionNavigationManager, NavigationActions } from '../../utils/navigation';

interface SessionSidebarProps {
  sessions: SessionInfo[];
  currentSessionId?: string;
  loading: boolean;
  collapsed: boolean;
  onToggleCollapse: () => void;
  onSessionUpdate: () => void;
}

export default function SessionSidebar({
  sessions,
  currentSessionId,
  loading,
  collapsed,
  onToggleCollapse,
  onSessionUpdate
}: SessionSidebarProps) {
  const router = useRouter();
  const [deletingSessionId, setDeletingSessionId] = useState<string | null>(null);

  const getStatusIcon = (session: SessionInfo) => {
    switch (session.status) {
      case 'completed':
        return (
          <div className="relative p-2 bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl border border-green-200/50 shadow-sm">
            <CheckCircleIcon className="h-4 w-4 text-green-600" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        );
      case 'analyzing':
      case 'analyzed':
      case 'optimizing':
      case 'processing':
        return (
          <div className="relative p-2 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl border border-blue-200/50 shadow-sm">
            <ClockIcon className="h-4 w-4 text-blue-600 animate-spin" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
          </div>
        );
      case 'error':
      case 'failed':
        return (
          <div className="relative p-2 bg-gradient-to-br from-red-50 to-rose-100 rounded-xl border border-red-200/50 shadow-sm">
            <ExclamationCircleIcon className="h-4 w-4 text-red-600" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
          </div>
        );
      default:
        return (
          <div className="p-2 bg-gradient-to-br from-neutral-50 to-neutral-100 rounded-xl border border-neutral-200/50 shadow-sm">
            <CogIcon className="h-4 w-4 text-neutral-500" />
          </div>
        );
    }
  };

  const getStatusBadge = (session: SessionInfo) => {
    switch (session.status) {
      case 'completed':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
            <SparklesIcon className="h-3 w-3 mr-1" />
            Completed
          </span>
        );
      case 'analyzing':
      case 'analyzed':
      case 'optimizing':
      case 'processing':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse mr-1"></div>
            Processing
          </span>
        );
      case 'error':
      case 'failed':
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200">
            Error
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-neutral-100 text-neutral-600 border border-neutral-200">
            Created
          </span>
        );
    }
  };

  const formatDate = (dateString: string) => {
    return SessionNavigationManager.formatDate(dateString, true);
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
      return;
    }

    setDeletingSessionId(sessionId);
    try {
      await apiClient.deleteSession(sessionId);
      onSessionUpdate();
      
      // If we're currently viewing the deleted session, redirect to sessions
      if (currentSessionId === sessionId) {
        router.push('/sessions');
      }
    } catch {
      // Handle error with user-friendly message
      alert('Failed to delete session. Please try again.');
    } finally {
      setDeletingSessionId(null);
    }
  };

  const handleSessionClick = (session: SessionInfo) => {
    NavigationActions.navigateToSession(router, session);
  };

  return (
    <div className={`fixed left-0 top-0 h-full bg-gradient-to-b from-white via-white to-neutral-50/50 backdrop-blur-xl border-r border-neutral-200/60 shadow-xl transition-all duration-300 ease-in-out z-30 ${
      collapsed ? 'w-20' : 'w-84'
    }`}>
      {/* Header */}
      <div className="sidebar-header">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-accent-500/5"></div>
        <div className="relative flex items-center justify-between w-full">
          {!collapsed && (
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl shadow-lg">
                <SparklesIcon className="h-5 w-5 text-white" />
              </div>
              <h2 className="text-xl font-bold text-gradient">Sessions</h2>
            </div>
          )}
          <button
            onClick={onToggleCollapse}
            className="relative p-2.5 rounded-xl bg-white/80 hover:bg-white border border-neutral-200/60 hover:border-neutral-300 shadow-sm hover:shadow-md transition-all duration-200 ease-in-out text-neutral-600 hover:text-neutral-900 transform hover:scale-105"
          >
            {collapsed ? (
              <ChevronRightIcon className="h-5 w-5" />
            ) : (
              <ChevronLeftIcon className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {/* New Session Button */}
      <div className="p-4 border-b border-neutral-200/60 bg-gradient-to-r from-neutral-50/50 to-white/50">
        <Link
          href="/sessions"
          className={`group relative overflow-hidden bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 ease-in-out transform hover:scale-[1.02] hover:-translate-y-0.5 flex items-center justify-center w-full ${
            collapsed ? 'px-3 py-3' : 'px-4 py-3'
          }`}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 transform translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 ease-in-out"></div>
          <PlusIcon className="h-5 w-5 relative z-10" />
          {!collapsed && <span className="ml-2 relative z-10">New Session</span>}
        </Link>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-neutral-300 scrollbar-track-transparent">
        {loading ? (
          <div className="p-6 text-center">
            <div className="relative">
              <div className="loading-spinner h-10 w-10 mx-auto mb-4 border-4 border-primary-200 border-t-primary-600"></div>
              <div className="absolute inset-0 loading-spinner h-10 w-10 mx-auto mb-4 border-4 border-transparent border-t-accent-400 animate-spin" style={{ animationDuration: '1.5s' }}></div>
            </div>
            {!collapsed && (
              <div className="space-y-2">
                <span className="text-sm font-semibold text-neutral-700">Loading sessions...</span>
                <div className="text-xs text-neutral-500">Please wait while we fetch your data</div>
              </div>
            )}
          </div>
        ) : sessions.length === 0 ? (
          <div className="p-6 text-center">
            {!collapsed && (
              <div className="space-y-4">
                <div className="p-4 bg-gradient-to-br from-neutral-50 to-neutral-100 rounded-2xl border border-neutral-200/60 shadow-sm">
                  <CogIcon className="h-10 w-10 mx-auto text-neutral-400 mb-3" />
                  <span className="text-sm font-semibold text-neutral-700 block">No sessions yet</span>
                  <span className="text-xs text-neutral-500 mt-1 block">Create your first session to get started</span>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="py-3 space-y-2">
            {sessions.map((session) => (
              <div
                key={session.session_id}
                className={`group relative mx-3 rounded-xl border transition-all duration-300 ease-in-out cursor-pointer transform hover:scale-[1.02] hover:-translate-y-0.5 ${
                  currentSessionId === session.session_id 
                    ? 'bg-gradient-to-r from-primary-50 to-accent-50 border-primary-200 shadow-lg shadow-primary-500/10' 
                    : 'bg-white/80 hover:bg-white border-neutral-200/60 hover:border-neutral-300 hover:shadow-lg'
                }`}
                onClick={() => handleSessionClick(session)}
              >
                <div className="p-4">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 mt-0.5">
                      {getStatusIcon(session)}
                    </div>
                    {!collapsed && (
                      <div className="min-w-0 flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <div className="min-w-0 flex-1">
                            <div className={`text-sm font-bold truncate ${
                              currentSessionId === session.session_id 
                                ? 'text-primary-900' 
                                : 'text-neutral-900'
                            }`}>
                              {SessionNavigationManager.getDisplayName(session)}
                            </div>
                            <div className="text-xs text-neutral-500 font-medium mt-1">
                              {formatDate(session.updated_at)}
                            </div>
                          </div>
                          <div className="flex items-center space-x-1 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                            <button
                              onClick={(e) => {
                                e.preventDefault();
                                e.stopPropagation();
                                handleSessionClick(session);
                              }}
                              className="p-1.5 rounded-lg text-neutral-400 hover:text-primary-600 hover:bg-primary-50 transition-all duration-200"
                              title="View session"
                            >
                              <EyeIcon className="h-4 w-4" />
                            </button>
                            <button
                              onClick={(e) => handleDeleteSession(session.session_id, e)}
                              disabled={deletingSessionId === session.session_id}
                              className="p-1.5 rounded-lg text-neutral-400 hover:text-red-600 hover:bg-red-50 disabled:opacity-50 transition-all duration-200"
                              title="Delete session"
                            >
                              {deletingSessionId === session.session_id ? (
                                <div className="loading-spinner h-4 w-4 border-2 border-red-200 border-t-red-500" />
                              ) : (
                                <TrashIcon className="h-4 w-4" />
                              )}
                            </button>
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            {getStatusBadge(session)}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                
                {/* Active session indicator */}
                {currentSessionId === session.session_id && (
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-primary-500 to-accent-500 rounded-r-full shadow-lg"></div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div className="p-4 border-t border-neutral-200/60 bg-gradient-to-r from-neutral-50/50 to-white/50">
        {!collapsed && (
          <div className="text-center">
            <div className="text-xs text-neutral-500 font-medium">
              {sessions.length} session{sessions.length !== 1 ? 's' : ''} total
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 