import { useState } from 'react';
import { TestSquare } from 'lucide-react';
import ConnectionPanel from './components/ConnectionPanel';
import InputPanel from './components/InputPanel';
import ContextCard from './components/ContextCard';
import OutputPanel from './components/OutputPanel';
import { JiraCredentials, JiraIssue, TestCase, TemplateType, ConnectionState, GenerationState } from './types';
import { testJiraConnection, fetchJiraIssue, generateTestCases } from './api';

function App() {
  // Connection state
  const [credentials, setCredentials] = useState<JiraCredentials>({
    base_url: '',
    email: '',
    api_token: '',
  });
  const [connectionState, setConnectionState] = useState<ConnectionState>({
    isConnected: false,
    isConnecting: false,
    userName: null,
    error: null,
  });
  
  // Anthropic API key
  const [anthropicKey, setAnthropicKey] = useState('');
  
  // Issue state
  const [issue, setIssue] = useState<JiraIssue | null>(null);
  const [isLoadingIssue, setIsLoadingIssue] = useState(false);
  const [issueError, setIssueError] = useState<string | null>(null);
  
  // Generation state
  const [testCases, setTestCases] = useState<TestCase[]>([]);
  const [generationState, setGenerationState] = useState<GenerationState>({
    isGenerating: false,
    progress: '',
    error: null,
  });
  const [generationMetrics, setGenerationMetrics] = useState<{
    time_ms: number;
    tokens: number;
  } | null>(null);

  // Handle connection test
  const handleTestConnection = async () => {
    setConnectionState({
      isConnected: false,
      isConnecting: true,
      userName: null,
      error: null,
    });

    try {
      const response = await testJiraConnection(credentials);
      
      if (response.success) {
        setConnectionState({
          isConnected: true,
          isConnecting: false,
          userName: response.user_display_name,
          error: null,
        });
      } else {
        setConnectionState({
          isConnected: false,
          isConnecting: false,
          userName: null,
          error: response.message,
        });
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Connection failed';
      setConnectionState({
        isConnected: false,
        isConnecting: false,
        userName: null,
        error: message,
      });
    }
  };

  // Handle issue fetch
  const handleFetchIssue = async (issueId: string) => {
    setIsLoadingIssue(true);
    setIssueError(null);
    setIssue(null);
    setTestCases([]);
    
    try {
      const response = await fetchJiraIssue(credentials, issueId);
      
      if (response.success && response.issue) {
        setIssue(response.issue);
        if (response.message.includes('Warning')) {
          setIssueError(response.message);
        }
      } else {
        setIssueError(response.message);
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to fetch issue';
      setIssueError(message);
    } finally {
      setIsLoadingIssue(false);
    }
  };

  // Handle test case generation
  const handleGenerate = async (templateType: TemplateType) => {
    if (!issue) return;
    
    setGenerationState({
      isGenerating: true,
      progress: 'Sending request to Claude...',
      error: null,
    });
    setTestCases([]);
    setGenerationMetrics(null);

    try {
      setGenerationState(prev => ({ ...prev, progress: 'Generating test cases...' }));
      
      const response = await generateTestCases(issue, templateType, anthropicKey);
      
      if (response.success) {
        setTestCases(response.test_cases);
        setGenerationMetrics({
          time_ms: response.generation_time_ms,
          tokens: response.tokens_used,
        });
        setGenerationState({
          isGenerating: false,
          progress: '',
          error: null,
        });
      } else {
        // If we got some test cases but not enough, still show them
        if (response.test_cases.length > 0) {
          setTestCases(response.test_cases);
          setGenerationMetrics({
            time_ms: response.generation_time_ms,
            tokens: response.tokens_used,
          });
        }
        setGenerationState({
          isGenerating: false,
          progress: '',
          error: response.message,
        });
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Generation failed';
      setGenerationState({
        isGenerating: false,
        progress: '',
        error: message,
      });
    }
  };

  // Handle test case edit
  const handleEditTestCase = (index: number, updatedTestCase: TestCase) => {
    const newTestCases = [...testCases];
    newTestCases[index] = updatedTestCase;
    setTestCases(newTestCases);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-600 rounded-lg">
              <TestSquare className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Test Case Generator</h1>
              <p className="text-sm text-gray-500">Generate structured test cases from Jira tickets</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Connection & Input */}
          <div className="space-y-6">
            <ConnectionPanel
              credentials={credentials}
              onCredentialsChange={setCredentials}
              connectionState={connectionState}
              onTestConnection={handleTestConnection}
              anthropicKey={anthropicKey}
              onAnthropicKeyChange={setAnthropicKey}
            />
            
            <InputPanel
              isConnected={connectionState.isConnected}
              isLoading={isLoadingIssue}
              onFetchIssue={handleFetchIssue}
              onGenerate={handleGenerate}
              isGenerating={generationState.isGenerating}
              hasIssue={!!issue}
              hasAnthropicKey={!!anthropicKey.trim()}
              error={issueError}
            />
          </div>

          {/* Middle Column - Context Card */}
          <div>
            <ContextCard
              issue={issue}
              isLoading={isLoadingIssue}
            />
          </div>

          {/* Right Column - Output Panel (spans full width on generation) */}
          <div className="lg:col-span-1">
            {/* Placeholder for layout */}
          </div>
        </div>

        {/* Output Panel - Full Width Below */}
        <div className="mt-6">
          <OutputPanel
            testCases={testCases}
            generationState={generationState}
            generationMetrics={generationMetrics}
            onEditTestCase={handleEditTestCase}
            onRegenerate={() => issue && handleGenerate('Functional')}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-sm text-gray-500 text-center">
            Test Case Generator • Powered by Claude AI
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
