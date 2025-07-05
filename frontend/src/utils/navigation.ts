import { SessionInfo } from '../types';

/**
 * 统一的Session导航管理工具
 */
export class SessionNavigationManager {
  /**
   * 获取session的最佳跳转链接
   * 优先级：optimization > analysis > analysis (默认)
   */
  static getSessionLink(session: SessionInfo): string {
    if (session.has_optimization) {
      return `/optimization/${session.session_id}`;
    } else if (session.has_analysis) {
      return `/analysis/${session.session_id}`;
    } else {
      // 对于正在处理或失败的session，也跳转到analysis页面
      return `/analysis/${session.session_id}`;
    }
  }

  /**
   * 获取session的状态文本
   */
  static getStatusText(session: SessionInfo): string {
    if (session.has_optimization) return 'Optimized';
    if (session.has_analysis) return 'Analyzed';
    if (session.status === 'analyzing' || session.status === 'processing') return 'Processing';
    if (session.status === 'error' || session.status === 'failed') return 'Failed';
    return 'Uploaded';
  }

  /**
   * 获取session的状态样式类
   */
  static getStatusBadgeClass(session: SessionInfo): string {
    if (session.has_optimization) return 'status-badge-success';
    if (session.has_analysis) return 'status-badge-info';
    if (session.status === 'analyzing' || session.status === 'processing') return 'status-badge-warning';
    if (session.status === 'error' || session.status === 'failed') return 'status-badge-error';
    return 'status-badge-neutral';
  }

  /**
   * 判断session是否可以进行优化
   */
  static canOptimize(session: SessionInfo): boolean {
    return session.has_analysis && !session.has_optimization;
  }

  /**
   * 判断session是否正在处理中
   */
  static isProcessing(session: SessionInfo): boolean {
    return session.status === 'analyzing' || session.status === 'processing';
  }

  /**
   * 判断session是否有错误
   */
  static hasError(session: SessionInfo): boolean {
    return session.status === 'error' || session.status === 'failed';
  }

  /**
   * 获取session的显示名称
   */
  static getDisplayName(session: SessionInfo): string {
    return `Session ${session.session_id.slice(0, 8)}`;
  }

  /**
   * 格式化日期显示
   */
  static formatDate(dateString: string, relative: boolean = false): string {
    const date = new Date(dateString);
    
    if (relative) {
      const now = new Date();
      const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

      if (diffInHours < 1) {
        return 'Just now';
      } else if (diffInHours < 24) {
        return `${Math.floor(diffInHours)}h ago`;
      } else if (diffInHours < 48) {
        return 'Yesterday';
      } else {
        return date.toLocaleDateString();
      }
    }
    
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
}

/**
 * 页面导航管理
 */
export class PageNavigationManager {
  /**
   * 获取当前页面的返回链接
   */
  static getBackLink(currentPath: string, sessionId?: string): { href: string; label: string } {
    // 分析页面 -> 回到sessions页面
    if (currentPath.startsWith('/analysis/')) {
      return { href: '/sessions', label: 'Back to Sessions' };
    }
    
    // 优化页面 -> 回到对应的分析页面
    if (currentPath.startsWith('/optimization/')) {
      return { href: `/analysis/${sessionId}`, label: 'Back to Analysis' };
    }
    
    // sessions页面 -> 回到首页
    if (currentPath === '/sessions') {
      return { href: '/', label: 'Back to Home' };
    }
    
    // 上传页面 -> 回到首页
    if (currentPath === '/upload') {
      return { href: '/', label: 'Back to Home' };
    }
    
    // 默认回到首页
    return { href: '/', label: 'Back to Home' };
  }

  /**
   * 获取页面标题
   */
  static getPageTitle(currentPath: string, sessionId?: string): string {
    if (currentPath.startsWith('/analysis/')) {
      return 'Analysis Report';
    }
    
    if (currentPath.startsWith('/optimization/')) {
      return 'Optimization Results';
    }
    
    if (currentPath === '/sessions') {
      return 'Recent Sessions';
    }
    
    if (currentPath === '/upload') {
      return 'Upload Configuration';
    }
    
    return 'ContextOptimizer';
  }

  /**
   * 获取面包屑导航
   */
  static getBreadcrumbs(currentPath: string, sessionId?: string): Array<{ label: string; href?: string }> {
    const breadcrumbs: Array<{ label: string; href?: string }> = [{ label: 'Home', href: '/' }];
    
    if (currentPath.startsWith('/analysis/')) {
      breadcrumbs.push({ label: 'Sessions', href: '/sessions' });
      breadcrumbs.push({ label: 'Analysis' });
    } else if (currentPath.startsWith('/optimization/')) {
      breadcrumbs.push({ label: 'Sessions', href: '/sessions' });
      if (sessionId) {
        breadcrumbs.push({ label: 'Analysis', href: `/analysis/${sessionId}` });
      }
      breadcrumbs.push({ label: 'Optimization' });
    } else if (currentPath === '/sessions') {
      breadcrumbs.push({ label: 'Sessions' });
    } else if (currentPath === '/upload') {
      breadcrumbs.push({ label: 'Upload' });
    }
    
    return breadcrumbs;
  }
}

/**
 * 导航操作管理
 */
export class NavigationActions {
  /**
   * 导航到session的最佳页面
   */
  static navigateToSession(router: any, session: SessionInfo): void {
    const link = SessionNavigationManager.getSessionLink(session);
    router.push(link);
  }

  /**
   * 导航到上一页
   */
  static navigateBack(router: any, currentPath: string, sessionId?: string): void {
    const { href } = PageNavigationManager.getBackLink(currentPath, sessionId);
    router.push(href);
  }

  /**
   * 导航到新建session
   */
  static navigateToNewSession(router: any): void {
    router.push('/upload');
  }

  /**
   * 导航到sessions列表
   */
  static navigateToSessions(router: any): void {
    router.push('/sessions');
  }

  /**
   * 导航到首页
   */
  static navigateToHome(router: any): void {
    router.push('/');
  }
} 