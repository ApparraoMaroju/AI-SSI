import { useState } from 'react';
import { Search, Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { TemplateType } from '../types';

interface InputPanelProps {
  isConnected: boolean;
  isLoading: boolean;
  onFetchIssue: (issueId: string) => void;
  onGenerate: (templateType: TemplateType) => void;
  isGenerating: boolean;
  hasIssue: boolean;
  hasAnthropicKey: boolean;
  error: string | null;
}

const TEMPLATE_OPTIONS: { value: TemplateType; label: string; description: string }[] = [
  { value: 'Functional', label: 'Functional', description: 'Comprehensive functional test coverage' },
  { value: 'Regression', label: 'Regression', description: 'Ensure existing features still work' },
  { value: 'Smoke', label: 'Smoke', description: 'Quick sanity checks' },
  { value: 'Edge', label: 'Edge Cases', description: 'Boundary and edge scenarios' },
  { value: 'Security', label: 'Security', description: 'Security vulnerability testing' },
];

export default function InputPanel({
  isConnected,
  isLoading,
  onFetchIssue,
  onGenerate,
  isGenerating,
  hasIssue,
  hasAnthropicKey,
  error,
}: InputPanelProps) {
  const [issueId, setIssueId] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateType>('Functional');

  const handleFetch = () => {
    if (issueId.trim()) {
      onFetchIssue(issueId.trim().toUpperCase());
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && issueId.trim() && isConnected) {
      handleFetch();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Search className="w-5 h-5 text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">Fetch & Generate</h2>
      </div>

      <div className="space-y-4">
        {/* Issue ID Input */}
        <div>
          <label htmlFor="issueId" className="block text-sm font-medium text-gray-700 mb-1">
            Jira Issue ID
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              id="issueId"
              placeholder="PROJ-123"
              value={issueId}
              onChange={(e) => setIssueId(e.target.value.toUpperCase())}
              onKeyDown={handleKeyDown}
              disabled={!isConnected}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm disabled:bg-gray-50 disabled:cursor-not-allowed uppercase"
            />
            <button
              onClick={handleFetch}
              disabled={!isConnected || !issueId.trim() || isLoading}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Search className="w-4 h-4" />
              )}
              Fetch
            </button>
          </div>
          {!isConnected && (
            <p className="text-xs text-gray-500 mt-1">Connect to Jira first</p>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="flex items-start gap-2 text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
            <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {/* Template Selector */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Test Template
          </label>
          <div className="grid grid-cols-2 gap-2">
            {TEMPLATE_OPTIONS.map((template) => (
              <button
                key={template.value}
                onClick={() => setSelectedTemplate(template.value)}
                className={`px-3 py-2 rounded-lg text-left transition-colors ${
                  selectedTemplate === template.value
                    ? 'bg-primary-100 border-2 border-primary-500 text-primary-700'
                    : 'bg-gray-50 border-2 border-transparent text-gray-700 hover:bg-gray-100'
                }`}
              >
                <span className="text-sm font-medium block">{template.label}</span>
                <span className="text-xs text-gray-500">{template.description}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Generate Button */}
        <button
          onClick={() => onGenerate(selectedTemplate)}
          disabled={!hasIssue || !hasAnthropicKey || isGenerating}
          className="w-full px-4 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-lg hover:from-primary-700 hover:to-primary-800 disabled:from-gray-300 disabled:to-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-all font-medium shadow-sm"
        >
          {isGenerating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Test Cases...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Generate Test Cases
            </>
          )}
        </button>

        {!hasIssue && isConnected && (
          <p className="text-xs text-gray-500 text-center">Fetch an issue to generate test cases</p>
        )}
        {!hasAnthropicKey && hasIssue && (
          <p className="text-xs text-amber-600 text-center">Enter your Anthropic API key to generate</p>
        )}
      </div>
    </div>
  );
}
