import { useState } from 'react';
import { Link, CheckCircle2, XCircle, Loader2, Eye, EyeOff, Key } from 'lucide-react';
import { JiraCredentials, ConnectionState } from '../types';

interface ConnectionPanelProps {
  credentials: JiraCredentials;
  onCredentialsChange: (credentials: JiraCredentials) => void;
  connectionState: ConnectionState;
  onTestConnection: () => void;
  anthropicKey: string;
  onAnthropicKeyChange: (key: string) => void;
}

export default function ConnectionPanel({
  credentials,
  onCredentialsChange,
  connectionState,
  onTestConnection,
  anthropicKey,
  onAnthropicKeyChange,
}: ConnectionPanelProps) {
  const [showToken, setShowToken] = useState(false);
  const [showAnthropicKey, setShowAnthropicKey] = useState(false);

  const updateCredential = (field: keyof JiraCredentials, value: string) => {
    onCredentialsChange({ ...credentials, [field]: value });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Link className="w-5 h-5 text-primary-600" />
        <h2 className="text-lg font-semibold text-gray-900">Connection Settings</h2>
      </div>

      <div className="space-y-4">
        {/* Jira Base URL */}
        <div>
          <label htmlFor="baseUrl" className="block text-sm font-medium text-gray-700 mb-1">
            Jira Base URL
          </label>
          <input
            type="url"
            id="baseUrl"
            placeholder="https://company.atlassian.net"
            value={credentials.base_url}
            onChange={(e) => updateCredential('base_url', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
          />
        </div>

        {/* Email */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address
          </label>
          <input
            type="email"
            id="email"
            placeholder="you@company.com"
            value={credentials.email}
            onChange={(e) => updateCredential('email', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
          />
        </div>

        {/* API Token */}
        <div>
          <label htmlFor="apiToken" className="block text-sm font-medium text-gray-700 mb-1">
            Jira API Token
          </label>
          <div className="relative">
            <input
              type={showToken ? 'text' : 'password'}
              id="apiToken"
              placeholder="Enter your Jira API token"
              value={credentials.api_token}
              onChange={(e) => updateCredential('api_token', e.target.value)}
              className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
            />
            <button
              type="button"
              onClick={() => setShowToken(!showToken)}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {showToken ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Test Connection Button */}
        <button
          onClick={onTestConnection}
          disabled={connectionState.isConnecting || !credentials.base_url || !credentials.email || !credentials.api_token}
          className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
        >
          {connectionState.isConnecting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Testing...
            </>
          ) : (
            'Test Connection'
          )}
        </button>

        {/* Connection Status */}
        {connectionState.isConnected && (
          <div className="flex items-center gap-2 text-green-600 bg-green-50 px-3 py-2 rounded-lg">
            <CheckCircle2 className="w-4 h-4" />
            <span className="text-sm">Connected as {connectionState.userName}</span>
          </div>
        )}
        
        {connectionState.error && (
          <div className="flex items-start gap-2 text-red-600 bg-red-50 px-3 py-2 rounded-lg">
            <XCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span className="text-sm">{connectionState.error}</span>
          </div>
        )}

        {/* Divider */}
        <div className="border-t border-gray-200 my-4" />

        {/* Anthropic API Key */}
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Key className="w-4 h-4 text-primary-600" />
            <label htmlFor="anthropicKey" className="block text-sm font-medium text-gray-700">
              Anthropic API Key
            </label>
          </div>
          <div className="relative">
            <input
              type={showAnthropicKey ? 'text' : 'password'}
              id="anthropicKey"
              placeholder="sk-ant-..."
              value={anthropicKey}
              onChange={(e) => onAnthropicKeyChange(e.target.value)}
              className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
            />
            <button
              type="button"
              onClick={() => setShowAnthropicKey(!showAnthropicKey)}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              {showAnthropicKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">Required for test case generation</p>
        </div>
      </div>
    </div>
  );
}
