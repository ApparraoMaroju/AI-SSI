---

# Output File Format Requirement

The generated migration test cases must be delivered in **Microsoft Excel (.xlsx) format** suitable for importing into enterprise QA management tools.

Create an Excel workbook with the following structure:

## Workbook Name

`Constellation_Atlassian_Migration_Validation_TestCases.xlsx`

---

# Excel Workbook Structure

The workbook should contain multiple worksheets.

## Sheet 1: Test Cases

This is the primary test case repository.

Columns:

| Column Name | Description |
|-------------|-------------|
| Test ID | Unique identifier (Example: MIG-JIRA-001) |
| Test Case Name | Clear and concise test scenario name |
| Test Category | Jira / Confluence / XRAY / Security / Integration / Performance / Reconciliation |
| Module | Specific application area |
| Description | Detailed purpose of the test |
| Preconditions | Conditions required before execution |
| Test Data | Required sample data or validation data |
| Test Steps | Numbered step-by-step execution instructions |
| Expected Results | Expected outcome after each validation |
| Priority | Critical / High / Medium / Low |
| Risk Area | Migration risk addressed |
| Validation Type | Functional / Data / Security / Performance / Integration |
| Source System | On-Premise component being validated |
| Target System | Cloud component being validated |
| Automation Candidate | Yes / No |
| Execution Status | Not Executed / Pass / Fail / Blocked |
| Defect ID | Placeholder for defect reference |
| Tester Comments | Execution notes |

---

## Sheet 2: Test Data Validation Matrix

Include reconciliation validation.

Columns:

| Validation ID | Object Type | Source Count | Target Count | Validation Method | Expected Result | Status |
|---------------|-------------|--------------|--------------|------------------|-----------------|--------|

Examples:

- Jira Projects
- Jira Issues
- Attachments
- Users
- Groups
- Confluence Spaces
- Confluence Pages
- XRAY Tests
- Test Executions
- Test Plans

---

## Sheet 3: Migration Smoke Test Suite

Create a shortened execution suite containing only critical tests required before business handover.

Columns:

| Smoke Test ID | Test Scenario | Reason for Inclusion | Expected Result | Priority |
|---------------|---------------|---------------------|-----------------|----------|

---

## Sheet 4: User Acceptance Test Readiness

Include end-user validation scenarios.

Columns:

| UAT ID | Business Scenario | User Role | Steps | Expected Result | Acceptance Criteria |
|--------|------------------|-----------|-------|-----------------|--------------------|

---

## Sheet 5: Defect Classification

Create a migration defect categorization reference.

Columns:

| Defect Category | Description | Example Issues | Severity |
|-----------------|-------------|----------------|----------|

Categories:

- Data Loss
- Data Corruption
- Permission Failure
- Configuration Mismatch
- Workflow Failure
- XRAY Traceability Issue
- Integration Failure
- Performance Degradation
- User Experience Issue

---

## Sheet 6: Migration Sign-Off Checklist

Columns:

| Checklist ID | Validation Area | Owner | Completion Criteria | Status |
|--------------|-----------------|-------|--------------------|--------|

Include sign-off areas:

- QA Approval
- Jira Administrator Approval
- Confluence Administrator Approval
- XRAY Administrator Approval
- Security Approval
- Business Owner Approval

---

# Excel Formatting Requirements

Apply professional QA documentation formatting:

- Freeze header rows
- Enable filters on all columns
- Apply column width optimization
- Use conditional formatting for:
  - Priority
  - Execution Status
  - Defect Severity
- Use unique Test IDs
- Use consistent naming conventions
- Avoid duplicate test scenarios
- Ensure every test case has measurable expected results

---

# Test Case Volume Expectation

Generate a comprehensive test repository.

Minimum expected coverage:

| Area | Minimum Test Cases |
|------|-------------------|
| Jira Migration | 100+ |
| XRAY Migration | 50+ |
| Confluence Migration | 75+ |
| User & Security Validation | 40+ |
| Integration Validation | 30+ |
| Reporting Validation | 25+ |
| Performance Validation | 20+ |
| Data Reconciliation | 40+ |
| UAT Validation | 30+ |

Total target:
**400+ migration validation test cases**

---

# Final Deliverable

The final output should be:

1. A downloadable `.xlsx` workbook.
2. Enterprise-ready QA test repository.
3. Suitable for:
   - Migration validation execution
   - QA sign-off
   - Business acceptance testing
   - Audit evidence
   - Atlassian Cloud migration governance

Do not provide only markdown tables. Generate the actual Excel workbook structure.