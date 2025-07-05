import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ContextOptimizer',
  description: 'Intelligent context engineering assistant for Multi-Agent Systems',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="font-sans antialiased h-full">
        <div className="min-h-screen bg-gray-50 flex flex-col">
          {children}
        </div>
      </body>
    </html>
  );
}
