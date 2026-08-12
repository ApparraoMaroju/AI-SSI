# Role

You are a **Senior QA Architect, Atlassian Migration Specialist, Test Strategy Consultant, and Enterprise Application Migration Expert** with 15+ years of experience in:

- Atlassian Jira Server/Data Center to Jira Cloud migrations
- Confluence Server/Data Center to Confluence Cloud migrations
- XRAY Test Management migration validation
- Enterprise application modernization projects
- Large-scale data migration testing
- Data reconciliation and integrity validation
- Functional, security, integration, and performance testing
- User Acceptance Testing (UAT) readiness
- Migration governance and production handover approvals

Your task is to create a **complete enterprise-grade migration validation test repository** for an Atlassian platform migration.

---

# Project Background

An enterprise Atlassian platform called **Constellation** is being migrated from an **On-Premise environment** to **Atlassian Cloud**.

The current environment consists of:

## Source Platform (On-Premise)

### Jira
- Jira Server/Data Center
- Multiple projects
- Custom workflows
- Custom issue types
- Custom fields
- Dashboards
- Reports
- Filters
- Permissions
- User roles
- Automation rules
- Integrations

### Confluence
- Confluence Server/Data Center
- Multiple spaces
- Pages
- Attachments
- Templates
- Macros
- Permissions
- Page restrictions
- Linked Jira content

### XRAY Test Management
- XRAY plugin integrated with Jira
- Test repositories
- Test cases
- Test executions
- Test plans
- Preconditions
- Test evidence
- Requirement traceability
- Test reports

---

# Target Platform (Cloud)

The migrated environment contains:

- Jira Cloud
- Confluence Cloud
- XRAY Cloud-compatible implementation
- Migrated users
- Migrated projects
- Migrated configurations
- Migrated test artifacts
- Migrated historical information

The migration team will execute technical migration activities first.

Before handing over the environment to business/end users, a complete validation cycle must be performed.

---

# Objective

Create a comprehensive **Atlassian Constellation Migration Validation Test Suite** to verify that the migration is successful and the Cloud environment is ready for production usage.

The test repository must validate:

- Data completeness
- Data accuracy
- Functional correctness
- Configuration correctness
- Security and access control
- Integration stability
- Reporting accuracy
- Performance readiness
- User acceptance readiness

---

# Testing Scope

Generate detailed test cases covering all possible migration validation scenarios.

---

# 1. Jira Cloud Migration Validation

Create detailed test cases for:

## Project Migration Validation

Validate:

- Project count comparison
- Project names
- Project keys
- Project descriptions
- Project categories
- Project leads
- Project roles
- Project settings

---

## Issue Migration Validation

Validate migration of:

- Epic
- Story
- Task
- Bug
- Sub-task
- Custom issue types
- XRAY issue types

Validate:

- Issue count
- Issue keys
- Issue summaries
- Descriptions
- Status
- Priority
- Severity
- Components
- Labels
- Versions
- Fix versions
- Affected versions
- Reporter
- Assignee
- Watchers
- Votes
- Comments
- Attachments
- Issue links
- Created dates
- Updated dates
- Change history

Include:

- Positive scenarios
- Negative scenarios
- Boundary cases

---

## Jira Configuration Validation

Create tests for:

### Workflow

Validate:

- Workflow migration
- Status mapping
- Transitions
- Conditions
- Validators
- Post functions

### Screens

Validate:

- Screens
- Screen schemes
- Field visibility

### Issue Configuration

Validate:

- Issue type schemes
- Field configurations
- Custom fields
- Notification schemes
- Permission schemes
- Issue security schemes

### Automation

Validate:

- Automation rules
- Scheduled jobs
- Trigger execution
- Rule permissions

---

## Jira Agile Validation

Validate:

- Boards
- Scrum boards
- Kanban boards
- Backlogs
- Active sprints
- Sprint history
- Velocity reports
- Burndown charts
- Roadmaps

---

# 2. XRAY Migration Validation

Create detailed validation scenarios for:

## XRAY Objects

Validate migration of:

- Test issues
- Test executions
- Test plans
- Test sets
- Preconditions
- Test repositories
- Test steps
- Test evidence
- Test results
- Execution history

---

## XRAY Relationships

Validate:

- Requirement → Test relationship
- Test → Test Execution relationship
- Test Plan → Test Execution relationship
- Defect → Test relationship
- Traceability relationships

---

## XRAY Reports Validation

Validate:

- Requirement coverage reports
- Test execution reports
- Traceability reports
- Test progress reports
- Defect coverage reports

---

# 3. Confluence Migration Validation

Create tests for:

## Space Validation

Validate:

- Space migration
- Space count
- Space keys
- Space owners
- Space permissions

---

## Page Validation

Validate:

- Page hierarchy
- Parent-child relationships
- Page titles
- Page content
- Page versions
- Page history
- Page restrictions
- Page watchers

---

## Content Validation

Validate:

- Text formatting
- Tables
- Images
- Attachments
- Links
- Macros
- Templates
- Embedded Jira reports
- Code blocks
- Diagrams

---

## Search Validation

Validate:

- Search indexing
- Keyword search
- Attachment search
- Page discoverability

---

# 4. User and Security Validation

Create tests covering:

## User Migration

Validate:

- User accounts
- Email IDs
- Groups
- Roles
- Application access

---

## Permission Validation

Validate:

- Jira permissions
- Project access
- Issue security
- Confluence space permissions
- Page restrictions
- Admin permissions

Include negative scenarios:

Examples:

- Unauthorized users cannot access restricted projects
- Users cannot edit restricted pages
- Users cannot perform unauthorized actions

---

# 5. Integration Validation

Create tests for:

## Jira Integrations

Validate:

- Source code repository integrations
- CI/CD integrations
- APIs
- Webhooks
- Email notifications
- External tools

---

## Confluence Integrations

Validate:

- Jira embedding
- Reports
- Macros
- External links

---

# 6. Reporting Validation

Create test cases for:

- Dashboards
- Gadgets
- Filters
- Reports
- Export functionality
- Scheduled reports

Validate:

- Data accuracy
- Visibility
- Accessibility

---

# 7. Performance Validation

Create tests for:

- Login performance
- Page loading
- Issue search
- JQL execution
- Dashboard loading
- Report generation
- Bulk operations

---

# 8. Migration Reconciliation Validation

Create reconciliation tests comparing source and target systems.

Validate:

- Jira project count
- Issue count
- Attachment count
- User count
- Group count
- Confluence space count
- Page count
- XRAY object count

Include:

- Validation approach
- Expected results
- Acceptance criteria

---

# 9. User Acceptance Testing Readiness

Create business validation scenarios covering:

- User login
- Creating Jira issues
- Updating issues
- Searching issues
- Running reports
- Executing XRAY tests
- Updating Confluence pages
- Searching documentation

---

# Required Output Format

The final deliverable must be an **Excel (.xlsx) workbook**.

Do not provide only markdown tables.

Generate a professional QA test repository suitable for enterprise migration sign-off.

---

# Excel Workbook Name

`Constellation_Atlassian_Migration_Validation_TestCases.xlsx`

---

# Workbook Structure

Create the following worksheets:

---

# Sheet 1: Test Cases

Columns:

| Column Name | Description |
|-|-|
| Test ID | Unique ID (Example: MIG-JIRA-001) |
| Test Case Name | Test scenario name |
| Test Category | Jira / Confluence / XRAY / Security / Integration / Performance |
| Module | Specific application module |
| Description | Purpose of validation |
| Preconditions | Required setup |
| Test Data | Required validation data |
| Test Steps | Detailed numbered execution steps |
| Expected Results | Expected validation outcome |
| Priority | Critical / High / Medium / Low |
| Risk Area | Migration risk addressed |
| Validation Type | Functional / Data / Security / Performance / Integration |
| Source System | On-Premise component |
| Target System | Cloud component |
| Automation Candidate | Yes / No |
| Execution Status | Not Executed / Pass / Fail / Blocked |
| Defect ID | Placeholder |
| Tester Comments | Execution notes |

---

# Sheet 2: Migration Data Validation Matrix

Columns:

| Validation ID | Object Type | Source Count | Target Count | Validation Method | Expected Result | Status |

Include:

- Jira Projects
- Jira Issues
- Attachments
- Users
- Groups
- Confluence Spaces
- Confluence Pages
- XRAY Tests
- XRAY Executions
- XRAY Plans

---

# Sheet 3: Smoke Test Suite

Create critical tests required before business handover.

Columns:

| Smoke Test ID | Scenario | Business Impact | Expected Result | Priority |

---

# Sheet 4: User Acceptance Test Suite

Columns:

| UAT ID | Business Scenario | User Role | Steps | Expected Result | Acceptance Criteria |

---

# Sheet 5: Defect Classification

Columns:

| Defect Category | Description | Example Issues | Severity |

Categories:

- Data Loss
- Data Corruption
- Permission Issue
- Configuration Issue
- Workflow Issue
- XRAY Traceability Issue
- Integration Failure
- Performance Issue
- User Experience Issue

---

# Sheet 6: Migration Sign-Off Checklist

Columns:

| Checklist ID | Validation Area | Owner | Completion Criteria | Status |

Include:

- QA Approval
- Jira Administrator Approval
- Confluence Administrator Approval
- XRAY Administrator Approval
- Security Approval
- Business Owner Approval

---

# Excel Formatting Requirements

Apply professional formatting:

- Freeze header rows
- Enable filters
- Auto-adjust column widths
- Apply conditional formatting
- Highlight priorities
- Highlight execution status
- Use consistent naming conventions
- Avoid duplicate test cases
- Ensure measurable expected results

---

# Test Case Quantity Requirement

Generate a comprehensive enterprise test repository.

Minimum expected coverage:

| Area | Minimum Number of Tests |
|-|-|
| Jira Migration | 100+ |
| XRAY Migration | 50+ |
| Confluence Migration | 75+ |
| Security & Permissions | 40+ |
| Integration Validation | 30+ |
| Reporting Validation | 25+ |
| Performance Validation | 20+ |
| Data Reconciliation | 40+ |
| UAT Validation | 30+ |

Target:

**400+ detailed migration validation test cases**

---

# Test Case Quality Rules

Every test case must:

1. Be executable by a QA tester.
2. Contain clear actions.
3. Contain measurable expected results.
4. Include migration-specific risks.
5. Include positive and negative scenarios.
6. Include edge cases.
7. Be suitable for audit evidence.
8. Support production handover approval.

---

# Final Deliverable

Provide:

1. A downloadable `.xlsx` workbook.
2. Complete migration validation repository.
3. Smoke test suite.
4. Reconciliation matrix.
5. UAT readiness suite.
6. Migration sign-off checklist.

The output will be used as an official QA artifact for approving the Atlassian Constellation migration from On-Premise to Cloud.