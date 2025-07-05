'use client';

import { useState, useEffect } from 'react';
import SessionSidebar from './SessionSidebar';
import { SessionInfo } from '../../types';
import { apiClient } from '../../utils/api';

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

  useEffect(() => {
    if (showSidebar) {
      fetchRecentSessions();
    }
  }, [showSidebar]);

  const fetchRecentSessions = async () => {
    try {
      const recentSessions = await apiClient.getRecentSessions();
      setSessions(recentSessions);
    } catch {
      // Handle error silently or show user-friendly message
      setSessions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSessionUpdate = () => {
    fetchRecentSessions();
  };

  if (!showSidebar) {
    return <div className="min-h-screen">{children}</div>;
  }

  return (
    <div className="flex h-screen">
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
      <div className={`flex-1 flex flex-col transition-all duration-300 ease-in-out ${
        sidebarCollapsed ? 'ml-16' : 'ml-80'
      }`}>
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
} 