import axios from 'axios';
import {
  JiraCredentials,
  JiraConnectionResponse,
  JiraIssueResponse,
  JiraIssue,
  TestCaseGenerateRequest,
  TestCaseGenerateResponse,
  TestCase,
  ExportFormat,
  ExportResponse,
  TemplateType
} from './types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Jira API

export async function testJiraConnection(credentials: JiraCredentials): Promise<JiraConnectionResponse> {
  const response = await api.post<JiraConnectionResponse>('/jira/test-connection', {
    credentials,
  });
  return response.data;
}

export async function fetchJiraIssue(
  credentials: JiraCredentials,
  issueId: string
): Promise<JiraIssueResponse> {
  const response = await api.post<JiraIssueResponse>('/jira/fetch-issue', {
    credentials,
    issue_id: issueId,
  });
  return response.data;
}

// Test Case API

export async function generateTestCases(
  issue: JiraIssue,
  templateType: TemplateType,
  anthropicApiKey: string,
  minCases: number = 5,
  customTemplate: string | null = null
): Promise<TestCaseGenerateResponse> {
  const request: TestCaseGenerateRequest = {
    issue,
    template_type: templateType,
    custom_template: customTemplate,
    min_test_cases: minCases,
    anthropic_api_key: anthropicApiKey,
  };
  
  const response = await api.post<TestCaseGenerateResponse>('/testcases/generate', request);
  return response.data;
}

export async function exportTestCases(
  testCases: TestCase[],
  format: ExportFormat,
  includeHeader: boolean = true
): Promise<ExportResponse> {
  const response = await api.post<ExportResponse>('/testcases/export', {
    test_cases: testCases,
    format,
    include_header: includeHeader,
  });
  return response.data;
}

// Health Check

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
}
