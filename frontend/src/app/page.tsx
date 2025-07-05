'use client';

import Link from 'next/link';
import { 
  PlusIcon
} from '@heroicons/react/24/outline';

export default function HomePage() {

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-accent-50/30">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(79,70,229,0.1),transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(192,38,211,0.1),transparent_50%)]"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="mb-8">
              <h1 className="text-5xl sm:text-6xl font-bold mb-6">
                <span className="text-gradient">ContextOptimizer</span>
            </h1>
              <div className="w-24 h-1 bg-gradient-to-r from-primary-500 to-accent-500 mx-auto rounded-full"></div>
            </div>
            
            <p className="text-xl text-neutral-600 mb-12 max-w-4xl mx-auto leading-relaxed">
              Intelligent context engineering assistant for Multi-Agent Systems. 
              Analyze and optimize your agent configurations for better performance with AI-powered insights.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link href="/sessions" className="btn-primary inline-flex items-center text-lg px-8 py-4">
                <PlusIcon className="h-5 w-5 mr-2" />
                Try it now!
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="relative py-20">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-white via-primary-50/30 to-white"></div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gradient mb-6">How It Works</h2>
            <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
              Simple three-step process to optimize your Multi-Agent System with AI-powered analysis
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center group">
              <div className="relative mb-8">
                <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:scale-110">
                  <span className="text-2xl font-bold text-white">1</span>
                </div>
                <div className="absolute top-10 left-1/2 transform -translate-x-1/2 w-px h-8 bg-gradient-to-b from-primary-300 to-transparent hidden md:block"></div>
              </div>
              <h3 className="text-2xl font-bold text-neutral-900 mb-4">Upload Configuration</h3>
              <p className="text-neutral-600 leading-relaxed">
                Upload your agent configuration and conversation data files. Our system supports various formats and validates your data automatically.
              </p>
            </div>
            
            <div className="text-center group">
              <div className="relative mb-8">
                <div className="bg-gradient-to-br from-accent-500 to-accent-600 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:scale-110">
                  <span className="text-2xl font-bold text-white">2</span>
                </div>
                <div className="absolute top-10 left-1/2 transform -translate-x-1/2 w-px h-8 bg-gradient-to-b from-accent-300 to-transparent hidden md:block"></div>
              </div>
              <h3 className="text-2xl font-bold text-neutral-900 mb-4">AI Analysis</h3>
              <p className="text-neutral-600 leading-relaxed">
                Our advanced AI analyzes your system architecture, identifies bottlenecks, and discovers optimization opportunities across all agents.
              </p>
            </div>
            
            <div className="text-center group">
              <div className="mb-8">
                <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:scale-110">
                  <span className="text-2xl font-bold text-white">3</span>
                </div>
              </div>
              <h3 className="text-2xl font-bold text-neutral-900 mb-4">Get Optimizations</h3>
              <p className="text-neutral-600 leading-relaxed">
                Receive detailed recommendations, optimized configurations, and ready-to-implement solutions with clear implementation guides.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="relative bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(79,70,229,0.1),transparent_50%)]"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(192,38,211,0.1),transparent_50%)]"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
            {/* Project Info */}
            <div className="md:col-span-2">
              <div className="flex items-center mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center mr-3">
                  <span className="text-white font-bold text-lg">C</span>
                </div>
                <h3 className="text-2xl font-bold text-white">ContextOptimizer</h3>
              </div>
              <p className="text-neutral-300 leading-relaxed mb-6 max-w-md">
                Open-source intelligent context engineering assistant for Multi-Agent Systems. 
                Optimize your AI agents with data-driven insights and automated recommendations.
              </p>
              <div className="flex items-center space-x-4">
                <a
                  href="https://github.com/lml2468/ContextOptimizer"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center px-4 py-2 bg-white text-neutral-900 rounded-lg font-medium hover:bg-neutral-100 transition-colors duration-200"
                >
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                  </svg>
                  View on GitHub
                </a>
                <span className="text-neutral-400 text-sm">⭐ Star us on GitHub</span>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
              <ul className="space-y-3">
                <li>
                  <Link href="/sessions" className="text-neutral-300 hover:text-white transition-colors duration-200">
                    Get Started
                  </Link>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer#readme"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/releases"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Releases
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/issues"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Report Issues
                  </a>
                </li>
              </ul>
            </div>

            {/* Community */}
            <div>
              <h4 className="text-lg font-semibold text-white mb-4">Community</h4>
              <ul className="space-y-3">
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/discussions"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Discussions
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/blob/main/CONTRIBUTING.md"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Contributing
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/blob/main/CODE_OF_CONDUCT.md"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    Code of Conduct
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/lml2468/ContextOptimizer/blob/main/LICENSE"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-neutral-300 hover:text-white transition-colors duration-200"
                  >
                    License
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-neutral-700 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="flex items-center space-x-6 mb-4 md:mb-0">
                <p className="text-neutral-400 text-sm">
                  © {new Date().getFullYear()} ContextOptimizer. Open source under MIT License.
                </p>
              </div>
              <div className="flex items-center space-x-6">
                <a
                  href="https://github.com/lml2468"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-neutral-400 hover:text-white transition-colors duration-200 text-sm"
                >
                  Built by @lml2468
                </a>
                <span className="text-neutral-600">•</span>
                <span className="text-neutral-400 text-sm">
                  Made with ❤️ for the AI community
                </span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
