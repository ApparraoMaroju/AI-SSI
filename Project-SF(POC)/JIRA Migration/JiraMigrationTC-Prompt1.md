# Role

You are a Senior QA Architect, Atlassian Migration Specialist, and Test Strategy Consultant with 15+ years of experience in validating enterprise migrations involving:

- Atlassian Jira Server/Data Center to Jira Cloud migrations
- Confluence Server/Data Center to Confluence Cloud migrations
- XRAY Test Management migration validation
- Large-scale enterprise application migrations
- Data integrity validation
- User acceptance readiness testing
- Post-migration quality assurance

Your task is to design a complete migration validation test suite for an enterprise Atlassian platform migration.

---

# Project Context

An enterprise Atlassian environment named **Constellation** is being migrated from:

## Current Environment
- Confluence On-Premise
- Jira On-Premise
- XRAY Test Management plugin integrated with Jira
- Existing users, groups, permissions, workflows, projects, spaces, dashboards, reports, attachments, and historical data

## Target Environment
- Confluence Cloud
- Jira Cloud
- XRAY Cloud-compatible environment
- Migrated users, projects, configurations, test artifacts, and historical records

The migration will be handed over to business/end users after technical migration completion.

Before handover, a detailed validation cycle must be executed to ensure:

- Data completeness
- Data accuracy
- Functional correctness
- Integration stability
- Security and access correctness
- User readiness
- Business continuity

---

# Objective

Create a comprehensive migration testing catalogue that validates the complete migration lifecycle.

The test cases should cover:

1. Migration readiness validation
2. Migration execution validation
3. Post-migration validation
4. Functional validation
5. Data validation
6. Security validation
7. Integration validation
8. User acceptance readiness validation

---

# Scope of Testing

Generate test cases covering all possible validation areas for:

## 1. Jira Cloud Migration Validation

Include tests for:

### Projects
- Project migration
- Project count comparison
- Project keys
- Project names
- Project descriptions
- Project categories
- Project leads
- Project roles

### Issues
Validate migration of:

- Epic
- Story
- Task
- Bug
- Sub-task
- Test issue types
- Custom issue types

Validate:

- Issue count comparison
- Issue IDs
- Issue keys
- Summary
- Description
- Status
- Priority
- Severity
- Labels
- Components
- Versions
- Fix versions
- Affected versions
- Reporter
- Assignee
- Watchers
- Votes
- Comments
- Attachments
- History
- Created date
- Updated date

### Jira Configuration

Validate:

- Workflows
- Workflow transitions
- Screens
- Screen schemes
- Issue type schemes
- Field configurations
- Custom fields
- Validators
- Conditions
- Post functions
- Notification schemes
- Permission schemes
- Security schemes
- Automation rules

### Jira Agile

Validate:

- Boards
- Filters
- Scrum boards
- Kanban boards
- Backlogs
- Sprints
- Sprint history
- Velocity reports
- Burndown reports
- Roadmaps

---

# 2. XRAY Migration Validation

Create detailed tests for:

## XRAY Objects

Validate:

- Test issues
- Test executions
- Test plans
- Test sets
- Precondition objects
- Test repositories
- Test steps
- Test evidence
- Test results
- Test status
- Test history

## XRAY Relationships

Validate:

- Requirement ↔ Test linkage
- Test ↔ Test Execution linkage
- Test Plan ↔ Test Execution linkage
- Defect ↔ Test linkage
- Coverage reports

## XRAY Reports

Validate:

- Requirement coverage report
- Test execution report
- Traceability report
- Test progress reports
- Defect traceability

---

# 3. Confluence Migration Validation

Create tests covering:

## Spaces

Validate:

- Space migration
- Space count
- Space keys
- Space permissions
- Space owners

## Pages

Validate:

- Page hierarchy
- Parent-child relationships
- Page titles
- Page content
- Page versions
- Page history
- Page restrictions
- Page watchers

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

## Search Validation

Validate:

- Page indexing
- Search results
- Keywords
- Attachments search

---

# 4. User and Security Validation

Include tests for:

## User Migration

Validate:

- User accounts
- Usernames
- Email IDs
- Groups
- Roles
- Application access

## Permissions

Validate:

- Jira project permissions
- Issue security
- Confluence space permissions
- Page restrictions
- Admin permissions
- Read/write permissions

Include negative testing:

Example:
- Unauthorized user cannot access restricted project
- User cannot modify restricted pages

---

# 5. Integration Validation

Create tests for integrations:

## Jira Integrations

Validate:

- CI/CD integrations
- Repository integrations
- Automation integrations
- Email notifications
- Webhooks
- APIs

## Confluence Integrations

Validate:

- Jira links
- Embedded reports
- External links
- Macros

---

# 6. Reporting Validation

Include tests for:

- Dashboards
- Gadgets
- Filters
- Reports
- Export functionality
- Scheduled reports

Validate:

- Data accuracy
- Visibility
- Performance

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

# 8. Migration Reconciliation Testing

Create detailed reconciliation tests:

Examples:

- Source Jira issue count vs target Jira issue count
- Source Confluence pages vs target Confluence pages
- Attachment count comparison
- User count comparison
- Project count comparison
- XRAY object count comparison

Include:

- Validation method
- Expected tolerance
- Pass/fail criteria

---

# 9. User Acceptance Testing Preparation

Include tests for:

- End-user login
- Common business workflows
- Creating issues
- Updating issues
- Running reports
- Executing tests
- Updating Confluence pages
- Searching information

---

# Required Output Format

Generate the output as a markdown table.

Each test case must contain:

| Test ID | Test Case Name | Category | Description | Preconditions | Test Data | Actions | Expected Results | Priority | Validation Type |
|---------|----------------|----------|-------------|---------------|------------|---------|------------------|----------|----------------|

---

# Test Case Writing Rules

Follow these rules:

1. Generate detailed enterprise-level test cases.
2. Each test case must be executable by a QA tester.
3. Avoid generic statements.
4. Include exact validation points.
5. Include positive and negative scenarios.
6. Include edge cases.
7. Include migration-specific risks.
8. Include expected outcomes.
9. Prioritize critical migration validations.
10. Assume the environment contains thousands of Jira issues, Confluence pages, users, and XRAY objects.

---

# Additional Deliverables

After generating test cases, provide:

## 1. Migration Validation Coverage Matrix

Include:

| Area | Validation Coverage | Risk Level | Priority |

## 2. Critical Smoke Test Suite

Provide the minimum tests required before business handover.

## 3. Migration Defect Classification

Provide categories:

- Data Loss
- Data Corruption
- Permission Issue
- Configuration Issue
- Functional Issue
- Performance Issue
- Integration Issue

## 4. Migration Sign-Off Checklist

Create a checklist for:

- QA approval
- Business approval
- Admin approval
- Security approval

---

# Final Instruction

Generate the most exhaustive migration validation test suite possible. Assume this document will be used as an official QA artifact for approving production handover after migration.