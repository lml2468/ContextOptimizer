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
  EyeIcon
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
    <div className={`fixed left-0 top-0 h-full glass-effect-strong transition-all duration-300 z-30 ${
      collapsed ? 'w-16' : 'w-80'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-white/20">
        {!collapsed && (
          <h2 className="text-xl font-bold text-gradient">Sessions</h2>
        )}
        <button
          onClick={onToggleCollapse}
          className="btn-icon text-neutral-600 hover:text-neutral-900"
        >
          {collapsed ? (
            <ChevronRightIcon className="h-5 w-5" />
          ) : (
            <ChevronLeftIcon className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* New Session Button */}
      <div className="p-4 border-b border-white/20">
        <Link
          href="/sessions"
          className={`btn-primary flex items-center justify-center w-full ${
            collapsed ? 'px-3' : ''
          }`}
        >
          <PlusIcon className="h-4 w-4" />
          {!collapsed && <span className="ml-2">New Session</span>}
        </Link>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-6 text-center text-neutral-500">
            <div className="loading-spinner h-8 w-8 mx-auto mb-4"></div>
            {!collapsed && <span className="text-sm font-medium">Loading sessions...</span>}
          </div>
        ) : sessions.length === 0 ? (
          <div className="p-6 text-center text-neutral-500">
            {!collapsed && (
              <div className="space-y-2">
                <CogIcon className="h-8 w-8 mx-auto text-neutral-400" />
                <span className="text-sm font-medium">No sessions yet</span>
              </div>
            )}
          </div>
        ) : (
          <div className="py-2 space-y-2">
            {sessions.map((session) => (
              <div
                key={session.session_id}
                className={`sidebar-item mx-3 ${
                  currentSessionId === session.session_id ? 'active' : ''
                }`}
                onClick={() => handleSessionClick(session)}
              >
                <div className="flex items-center space-x-3 min-w-0 flex-1">
                  <div className="flex-shrink-0">
                    {getStatusIcon(session)}
                  </div>
                  {!collapsed && (
                    <div className="min-w-0 flex-1">
                      <div className="text-sm font-semibold text-neutral-900 truncate">
                        {SessionNavigationManager.getDisplayName(session)}
                      </div>
                      <div className="text-xs text-neutral-500 font-medium">
                        {getStatusText(session)}
                      </div>
                    </div>
                  )}
                </div>
                
                {!collapsed && (
                  <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        handleSessionClick(session);
                      }}
                      className="btn-icon p-1.5 text-neutral-400 hover:text-neutral-600"
                      title="View session"
                    >
                      <EyeIcon className="h-3.5 w-3.5" />
                    </button>
                    <button
                      onClick={(e) => handleDeleteSession(session.session_id, e)}
                      disabled={deletingSessionId === session.session_id}
                      className="btn-icon p-1.5 text-neutral-400 hover:text-red-600 disabled:opacity-50"
                      title="Delete session"
                    >
                      {deletingSessionId === session.session_id ? (
                        <div className="loading-spinner h-3.5 w-3.5" />
                      ) : (
                        <TrashIcon className="h-3.5 w-3.5" />
                      )}
                    </button>
                  </div>
                )}
                
                {!collapsed && (
                  <div className="mt-2 text-xs text-neutral-400 font-medium">
                    {formatDate(session.updated_at)}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 