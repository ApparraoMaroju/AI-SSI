// API Types matching backend schemas

export interface JiraCredentials {
  base_url: string;
  email: string;
  api_token: string;
}

export interface JiraIssue {
  id: string;
  key: string;
  summary: string;
  description: string | null;
  acceptance_criteria: string | null;
  issue_type: string;
  priority: string;
  status: string;
  components: string[];
  labels: string[];
  reporter: string | null;
  assignee: string | null;
}

export type TestType = 'Positive' | 'Negative' | 'Edge' | 'Boundary' | 'Security';
export type Priority = 'P0' | 'P1' | 'P2';
export type TemplateType = 'Functional' | 'Regression' | 'Smoke' | 'Edge' | 'Security' | 'Custom';
export type ExportFormat = 'markdown' | 'csv' | 'tsv';

export interface TestCase {
  id: string;
  title: string;
  type: TestType;
  priority: Priority;
  preconditions: string;
  steps: string[];
  test_data: string;
  expected_result: string;
  linked_jira_id: string;
}

// API Request/Response types

export interface JiraConnectionResponse {
  success: boolean;
  message: string;
  user_display_name: string | null;
}

export interface JiraIssueResponse {
  success: boolean;
  message: string;
  issue: JiraIssue | null;
}

export interface TestCaseGenerateRequest {
  issue: JiraIssue;
  template_type: TemplateType;
  custom_template: string | null;
  min_test_cases: number;
  anthropic_api_key: string;
}

export interface TestCaseGenerateResponse {
  success: boolean;
  message: string;
  test_cases: TestCase[];
  generation_time_ms: number;
  tokens_used: number;
}

export interface ExportResponse {
  success: boolean;
  content: string;
  filename: string;
  content_type: string;
}

// UI State types

export interface ConnectionState {
  isConnected: boolean;
  isConnecting: boolean;
  userName: string | null;
  error: string | null;
}

export interface GenerationState {
  isGenerating: boolean;
  progress: string;
  error: string | null;
}
