'use client';

import Link from 'next/link';
import { 
  PlusIcon, 
  InformationCircleIcon
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
    </div>
  );
}
