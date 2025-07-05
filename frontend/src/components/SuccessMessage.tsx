import React from 'react';
import { CheckCircleIcon } from '@heroicons/react/24/outline';

interface SuccessMessageProps {
  title?: string;
  message: string;
  className?: string;
}

const SuccessMessage: React.FC<SuccessMessageProps> = ({ 
  title = 'Success', 
  message, 
  className = '' 
}) => {
  return (
    <div className={`p-4 bg-green-50 border border-green-200 rounded-lg ${className}`}>
      <div className="flex items-start">
        <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
        <div>
          {title && <h4 className="text-sm font-medium text-green-800 mb-1">{title}</h4>}
          <p className="text-sm text-green-700">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default SuccessMessage;
