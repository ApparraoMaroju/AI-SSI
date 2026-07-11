import { FileText, Tag, User, AlertCircle, CheckCircle } from 'lucide-react';
import { JiraIssue } from '../types';

interface ContextCardProps {
  issue: JiraIssue | null;
  isLoading: boolean;
}

export default function ContextCard({ issue, isLoading }: ContextCardProps) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3" />
          <div className="h-4 bg-gray-200 rounded w-full" />
          <div className="h-4 bg-gray-200 rounded w-2/3" />
          <div className="h-20 bg-gray-200 rounded w-full" />
        </div>
      </div>
    );
  }

  if (!issue) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-gray-400" />
          <h2 className="text-lg font-semibold text-gray-400">Issue Context</h2>
        </div>
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <FileText className="w-12 h-12 mb-2" />
          <p className="text-sm">No issue loaded</p>
          <p className="text-xs">Fetch a Jira issue to see details here</p>
        </div>
      </div>
    );
  }

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'highest':
      case 'critical':
        return 'bg-red-100 text-red-700';
      case 'high':
        return 'bg-orange-100 text-orange-700';
      case 'medium':
        return 'bg-yellow-100 text-yellow-700';
      case 'low':
        return 'bg-green-100 text-green-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getStatusColor = (status: string) => {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('done') || statusLower.includes('closed')) {
      return 'bg-green-100 text-green-700';
    }
    if (statusLower.includes('progress')) {
      return 'bg-blue-100 text-blue-700';
    }
    return 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 h-full">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="w-5 h-5 text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">Issue Context</h2>
      </div>

      <div className="space-y-4">
        {/* Issue Key & Summary */}
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-sm font-mono bg-primary-100 text-primary-700 px-2 py-0.5 rounded">
              {issue.key}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded ${getStatusColor(issue.status)}`}>
              {issue.status}
            </span>
          </div>
          <h3 className="text-base font-medium text-gray-900">{issue.summary}</h3>
        </div>

        {/* Meta Info */}
        <div className="flex flex-wrap gap-2">
          <span className="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
            <Tag className="w-3 h-3" />
            {issue.issue_type}
          </span>
          <span className={`inline-flex items-center gap-1 text-xs px-2 py-1 rounded ${getPriorityColor(issue.priority)}`}>
            {issue.priority}
          </span>
          {issue.reporter && (
            <span className="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
              <User className="w-3 h-3" />
              {issue.reporter}
            </span>
          )}
        </div>

        {/* Components & Labels */}
        {(issue.components.length > 0 || issue.labels.length > 0) && (
          <div className="flex flex-wrap gap-1">
            {issue.components.map((comp) => (
              <span key={comp} className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">
                {comp}
              </span>
            ))}
            {issue.labels.map((label) => (
              <span key={label} className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
                {label}
              </span>
            ))}
          </div>
        )}

        {/* Description */}
        {issue.description && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1 flex items-center gap-1">
              <FileText className="w-3 h-3" />
              Description
            </h4>
            <div className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3 max-h-40 overflow-y-auto whitespace-pre-wrap">
              {issue.description}
            </div>
          </div>
        )}

        {/* Acceptance Criteria */}
        {issue.acceptance_criteria ? (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-1 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-600" />
              Acceptance Criteria
            </h4>
            <div className="text-sm text-gray-600 bg-green-50 rounded-lg p-3 max-h-40 overflow-y-auto whitespace-pre-wrap">
              {issue.acceptance_criteria}
            </div>
          </div>
        ) : (
          <div className="flex items-start gap-2 text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
            <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span className="text-xs">No explicit acceptance criteria found. Test cases will be derived from the description.</span>
          </div>
        )}
      </div>
    </div>
  );
}
