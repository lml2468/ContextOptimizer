'use client';

import Link from 'next/link';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gradient">ContextOptimizer</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold text-gray-900 mb-4 sm:text-5xl">
              Intelligent Context Engineering Assistant
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Optimize your Multi-Agent System's context flow with data-driven analysis and recommendations
            </p>
            <Link href="/upload" passHref>
              <Button size="lg" className="px-8">Get Started</Button>
            </Link>
          </div>

          {/* Features Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <Card>
              <CardHeader>
                <CardTitle>Context Logic Diagnosis</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Automatically identify context breakage issues in your multi-agent conversations
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Coordinated Optimization</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Optimize prompts and tool information together for better coherence
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Actionable Solutions</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Get ready-to-use optimized configurations and implementation guides
                </CardDescription>
              </CardContent>
            </Card>
          </div>

          {/* CTA Section */}
          <div className="text-center">
            <Link href="/upload" passHref>
              <Button variant="secondary" className="mr-4">Learn More</Button>
            </Link>
            <Link href="/upload" passHref>
              <Button>Start Analysis</Button>
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} ContextOptimizer. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
