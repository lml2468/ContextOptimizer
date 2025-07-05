'use client';

import { useState, useEffect, useCallback } from 'react';
import { SessionInfo } from '../../types';
import { apiClient } from '../../utils/api';
import SessionSidebar from './SessionSidebar';

interface AppLayoutProps {
  children: React.ReactNode;
  currentSessionId?: string;
}

export default function AppLayout({ children, currentSessionId }: AppLayoutProps) {
  const [sessions, setSessions] = useState<SessionInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Show sidebar on all pages except standalone upload page (which no longer exists)
  const showSidebar = true;

  // Fetch sessions function
  const fetchRecentSessions = useCallback(async () => {
    try {
      const recentSessions = await apiClient.getRecentSessions();
      setSessions(recentSessions);
    } catch {
      // Handle error silently or show user-friendly message
      setSessions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial fetch
  useEffect(() => {
    if (showSidebar) {
      fetchRecentSessions();
    }
  }, [showSidebar, fetchRecentSessions]);

  // Polling for session updates
  useEffect(() => {
    if (!showSidebar) return;

    const pollInterval = setInterval(async () => {
      // Only poll if there are sessions that might be in progress
      const hasActiveSession = sessions.some(session => 
        session.status === 'analyzing' || 
        session.status === 'analyzed' || 
        session.status === 'optimizing' ||
        session.status === 'processing'
      );

      if (hasActiveSession) {
        await fetchRecentSessions();
      }
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(pollInterval);
  }, [showSidebar, sessions, fetchRecentSessions]);

  // Update page header class based on sidebar state
  useEffect(() => {
    const pageHeaders = document.querySelectorAll('.page-header');
    pageHeaders.forEach(header => {
      if (sidebarCollapsed) {
        header.classList.add('sidebar-collapsed');
      } else {
        header.classList.remove('sidebar-collapsed');
      }
    });
  }, [sidebarCollapsed]);

  const handleSessionUpdate = () => {
    fetchRecentSessions();
  };

  if (!showSidebar) {
    return <div className="min-h-screen">{children}</div>;
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-neutral-50 via-white to-primary-50/30">
      {/* Sidebar */}
      <SessionSidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        loading={loading}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        onSessionUpdate={handleSessionUpdate}
      />

      {/* Main content */}
      <div className={`flex-1 flex flex-col transition-all duration-300 ease-in-out layout-transition ${
        sidebarCollapsed ? 'ml-20' : 'ml-84'
      }`}>
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
} 