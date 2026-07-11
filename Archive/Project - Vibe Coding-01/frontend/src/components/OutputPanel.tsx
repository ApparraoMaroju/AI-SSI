import { useState } from 'react';
import { 
  ClipboardCopy, 
  Download, 
  FileText, 
  RefreshCw, 
  Clock, 
  Zap,
  CheckCircle,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Edit3,
  Save,
  X
} from 'lucide-react';
import { TestCase, GenerationState, ExportFormat } from '../types';
import { exportTestCases } from '../api';

interface OutputPanelProps {
  testCases: TestCase[];
  generationState: GenerationState;
  generationMetrics: { time_ms: number; tokens: number } | null;
  onEditTestCase: (index: number, testCase: TestCase) => void;
  onRegenerate: () => void;
}

export default function OutputPanel({
  testCases,
  generationState,
  generationMetrics,
  onEditTestCase,
  onRegenerate,
}: OutputPanelProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<TestCase | null>(null);

  const handleCopyAll = async () => {
    try {
      const response = await exportTestCases(testCases, 'tsv');
      if (response.success) {
        await navigator.clipboard.writeText(response.content);
        setCopiedIndex(-1);
        setTimeout(() => setCopiedIndex(null), 2000);
      }
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  const handleExport = async (format: ExportFormat) => {
    try {
      const response = await exportTestCases(testCases, format);
      if (response.success) {
        const blob = new Blob([response.content], { type: response.content_type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Failed to export:', error);
    }
  };

  const handleStartEdit = (index: number) => {
    setEditingIndex(index);
    setEditForm({ ...testCases[index] });
    setExpandedIndex(index);
  };

  const handleSaveEdit = () => {
    if (editingIndex !== null && editForm) {
      onEditTestCase(editingIndex, editForm);
      setEditingIndex(null);
      setEditForm(null);
    }
  };

  const handleCancelEdit = () => {
    setEditingIndex(null);
    setEditForm(null);
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Positive':
        return 'bg-green-100 text-green-700';
      case 'Negative':
        return 'bg-red-100 text-red-700';
      case 'Edge':
        return 'bg-orange-100 text-orange-700';
      case 'Boundary':
        return 'bg-purple-100 text-purple-700';
      case 'Security':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P0':
        return 'bg-red-500 text-white';
      case 'P1':
        return 'bg-orange-500 text-white';
      case 'P2':
        return 'bg-blue-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  // Loading State
  if (generationState.isGenerating) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col items-center justify-center py-12">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-primary-200 rounded-full"></div>
            <div className="w-16 h-16 border-4 border-primary-600 rounded-full absolute top-0 left-0 animate-spin border-t-transparent"></div>
          </div>
          <p className="mt-4 text-lg font-medium text-gray-900">{generationState.progress}</p>
          <p className="text-sm text-gray-500">This may take a few seconds...</p>
        </div>
      </div>
    );
  }

  // Error State
  if (generationState.error && testCases.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col items-center justify-center py-12">
          <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
          <p className="text-lg font-medium text-gray-900">Generation Failed</p>
          <p className="text-sm text-gray-500 mb-4">{generationState.error}</p>
          <button
            onClick={onRegenerate}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
          >
            <RefreshCw className="w-4 h-4" />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Empty State
  if (testCases.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col items-center justify-center py-12 text-gray-400">
          <FileText className="w-12 h-12 mb-2" />
          <p className="text-sm">No test cases generated yet</p>
          <p className="text-xs">Fetch a Jira issue and generate test cases</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Generated Test Cases ({testCases.length})
            </h2>
            {generationMetrics && (
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {(generationMetrics.time_ms / 1000).toFixed(2)}s
                </span>
                <span className="flex items-center gap-1">
                  <Zap className="w-4 h-4" />
                  {generationMetrics.tokens.toLocaleString()} tokens
                </span>
              </div>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopyAll}
              className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2 text-sm transition-colors"
            >
              {copiedIndex === -1 ? (
                <>
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  Copied!
                </>
              ) : (
                <>
                  <ClipboardCopy className="w-4 h-4" />
                  Copy TSV
                </>
              )}
            </button>
            
            <button
              onClick={() => handleExport('markdown')}
              className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2 text-sm transition-colors"
            >
              <Download className="w-4 h-4" />
              Export MD
            </button>
            
            <button
              onClick={() => handleExport('csv')}
              className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-2 text-sm transition-colors"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
            
            <button
              onClick={onRegenerate}
              className="px-3 py-1.5 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 flex items-center gap-2 text-sm transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Regenerate
            </button>
          </div>
        </div>
        
        {generationState.error && (
          <div className="mt-2 flex items-center gap-2 text-amber-700 bg-amber-50 px-3 py-2 rounded-lg">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">{generationState.error}</span>
          </div>
        )}
      </div>

      {/* Test Cases Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">ID</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Type</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-16">Pri</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {testCases.map((tc, index) => (
              <>
                <tr 
                  key={tc.id}
                  className={`hover:bg-gray-50 cursor-pointer ${expandedIndex === index ? 'bg-gray-50' : ''}`}
                  onClick={() => editingIndex !== index && setExpandedIndex(expandedIndex === index ? null : index)}
                >
                  <td className="px-4 py-3">
                    <span className="font-mono text-sm text-gray-600">{tc.id}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm text-gray-900">{tc.title}</span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${getTypeColor(tc.type)}`}>
                      {tc.type}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(tc.priority)}`}>
                      {tc.priority}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleStartEdit(index);
                        }}
                        className="p-1 text-gray-400 hover:text-primary-600 transition-colors"
                        title="Edit"
                      >
                        <Edit3 className="w-4 h-4" />
                      </button>
                      {expandedIndex === index ? (
                        <ChevronUp className="w-4 h-4 text-gray-400" />
                      ) : (
                        <ChevronDown className="w-4 h-4 text-gray-400" />
                      )}
                    </div>
                  </td>
                </tr>
                
                {/* Expanded Row */}
                {expandedIndex === index && (
                  <tr>
                    <td colSpan={5} className="px-4 py-4 bg-gray-50">
                      {editingIndex === index && editForm ? (
                        // Edit Mode
                        <div className="space-y-4">
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <label className="block text-xs font-medium text-gray-700 mb-1">Title</label>
                              <input
                                type="text"
                                value={editForm.title}
                                onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                              />
                            </div>
                            <div className="flex gap-4">
                              <div className="flex-1">
                                <label className="block text-xs font-medium text-gray-700 mb-1">Type</label>
                                <select
                                  value={editForm.type}
                                  onChange={(e) => setEditForm({ ...editForm, type: e.target.value as TestCase['type'] })}
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                                >
                                  <option value="Positive">Positive</option>
                                  <option value="Negative">Negative</option>
                                  <option value="Edge">Edge</option>
                                  <option value="Boundary">Boundary</option>
                                  <option value="Security">Security</option>
                                </select>
                              </div>
                              <div className="flex-1">
                                <label className="block text-xs font-medium text-gray-700 mb-1">Priority</label>
                                <select
                                  value={editForm.priority}
                                  onChange={(e) => setEditForm({ ...editForm, priority: e.target.value as TestCase['priority'] })}
                                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                                >
                                  <option value="P0">P0</option>
                                  <option value="P1">P1</option>
                                  <option value="P2">P2</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Preconditions</label>
                            <textarea
                              value={editForm.preconditions}
                              onChange={(e) => setEditForm({ ...editForm, preconditions: e.target.value })}
                              rows={2}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                            />
                          </div>
                          
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Steps (one per line)</label>
                            <textarea
                              value={editForm.steps.join('\n')}
                              onChange={(e) => setEditForm({ ...editForm, steps: e.target.value.split('\n').filter(s => s.trim()) })}
                              rows={4}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono"
                            />
                          </div>
                          
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Test Data</label>
                            <textarea
                              value={editForm.test_data}
                              onChange={(e) => setEditForm({ ...editForm, test_data: e.target.value })}
                              rows={2}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                            />
                          </div>
                          
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">Expected Result</label>
                            <textarea
                              value={editForm.expected_result}
                              onChange={(e) => setEditForm({ ...editForm, expected_result: e.target.value })}
                              rows={2}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                            />
                          </div>
                          
                          <div className="flex justify-end gap-2">
                            <button
                              onClick={handleCancelEdit}
                              className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center gap-1 text-sm"
                            >
                              <X className="w-4 h-4" />
                              Cancel
                            </button>
                            <button
                              onClick={handleSaveEdit}
                              className="px-3 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-1 text-sm"
                            >
                              <Save className="w-4 h-4" />
                              Save
                            </button>
                          </div>
                        </div>
                      ) : (
                        // View Mode
                        <div className="space-y-3">
                          <div>
                            <h4 className="text-xs font-medium text-gray-500 uppercase mb-1">Preconditions</h4>
                            <p className="text-sm text-gray-700">{tc.preconditions}</p>
                          </div>
                          
                          <div>
                            <h4 className="text-xs font-medium text-gray-500 uppercase mb-1">Steps</h4>
                            <ol className="list-decimal list-inside space-y-1">
                              {tc.steps.map((step, i) => (
                                <li key={i} className="text-sm text-gray-700">{step}</li>
                              ))}
                            </ol>
                          </div>
                          
                          <div>
                            <h4 className="text-xs font-medium text-gray-500 uppercase mb-1">Test Data</h4>
                            <p className="text-sm text-gray-700 font-mono bg-gray-100 px-2 py-1 rounded">{tc.test_data}</p>
                          </div>
                          
                          <div>
                            <h4 className="text-xs font-medium text-gray-500 uppercase mb-1">Expected Result</h4>
                            <p className="text-sm text-gray-700">{tc.expected_result}</p>
                          </div>
                          
                          <div className="text-xs text-gray-500">
                            Linked to: <span className="font-mono">{tc.linked_jira_id}</span>
                          </div>
                        </div>
                      )}
                    </td>
                  </tr>
                )}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
