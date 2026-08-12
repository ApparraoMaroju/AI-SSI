# Prompt: Jira & Confluence On-Premises to Cloud Migration Smoke-Test Suite

## Role

Act as a **Senior Scrum Master, Project Manager, Jira/Confluence Administrator, QA Test Lead, and Migration Validation Specialist** with extensive experience in Atlassian Jira, Confluence, Xray, Cloud migrations, data validation, application smoke testing, and post-migration verification.

Your task is to create a **comprehensive, execution-ready migration smoke-test and handover-validation test suite** for a Jira and Confluence migration from **On-Premises to Atlassian Cloud**.

The test suite will be used by the **Migration Team before handing over the migrated Test Environment** and by the **Application/Project Team during the subsequent 1–2 week validation period**.

---

## 1. Migration Background

The migration will be completed in two phases.

### Phase 1 – Test Environment Migration

The Migration Team will:

1. Complete the migration of Jira and Confluence from On-Premises to Cloud.
2. Perform their initial technical sanity checks.
3. Hand over the migrated Test Environment to the Application/Project Team.
4. The Application/Project Team will validate the environment for approximately **1–2 weeks**.
5. Migration defects identified during this period will be investigated and corrected by the Migration Team.

### Phase 2 – Production Migration

After successful validation of the Test Environment:

1. Jira and Confluence Production will be migrated to Cloud.
2. Post-migration activities will be completed.
3. Production will be handed over to the Application/Project Team.
4. The same critical smoke tests should be repeated against Production.

---

# 2. Systems in Scope

## 2.1 Jira Projects

The following Jira projects are in scope:

* **SFDC Development**
* **SFDC Operations**

The complete project data and configuration are expected to be migrated.

Validate the migration of:

* Projects
* Project keys and names
* Project details
* Issue types
* Workflows
* Workflow statuses
* Workflow transitions
* Workflow conditions
* Workflow validators
* Workflow post-functions
* Screens
* Screen schemes
* Issue type screen schemes
* Custom fields
* Field configurations
* Field configuration schemes
* Priorities
* Resolutions
* Project settings
* Versions/Releases
* Components
* Component leads
* Project roles
* Project permissions
* Permission schemes
* Notification schemes
* Issue security schemes
* Users
* User mappings
* Groups
* Group memberships
* Assignees
* Reporters
* Watchers where applicable
* Comments
* Attachments
* Issue history
* Change history
* Worklogs
* Issue links
* Issue relationships
* Parent/child relationships
* Subtasks
* Epic relationships
* Linked tickets
* Remote links
* Development tool integrations
* Sprint information
* Active sprints
* Completed sprints
* Future sprints
* Sprint history
* Scrum boards
* Kanban boards
* Board filters
* Board configuration
* Quick filters
* Columns
* Swimlanes
* Card configuration
* Previous Sprint reports/history
* Dashboards where applicable
* Filters
* Saved searches
* Notifications
* Audit information where supported

---

# 3. Jira Issue Types

Explicitly validate the following issue types:

* Bug
* Epic
* Feature
* Pre-condition
* Spike
* Sub-test Execution
* Sub-task
* Task
* Test
* Test Execution
* Test Plan
* Test Set
* User Story

Do not assume that validating one issue type proves that all issue types migrated successfully.

Where practical, create representative validation tests for each issue type.

---

# 4. Xray Plugin

**Xray is a critical component of the Jira environment and must be available in Jira Cloud.**

Xray is used as the primary Test Management solution.

It supports:

* Test Cases
* Test Sets
* Test Executions
* Test Plans
* Preconditions
* Test steps
* Test data
* Test evidence
* Requirements traceability
* Defect traceability
* Test coverage
* Test execution status
* Test reporting

The migration validation must explicitly verify that **Xray is available, correctly configured, usable, and that migrated Xray data remains intact and traceable**.

Do not treat Xray as an optional or secondary plugin.

---

# 5. Confluence

The Confluence space in scope is:

**SFSUPPORTDE**

All content within this space is expected to migrate to Cloud.

Validate:

* Space availability
* Space key
* Space name
* Space permissions
* All pages
* Page hierarchy
* Parent/child relationships
* Page titles
* Page content
* Page formatting
* Tables
* Images
* Macros
* Page properties
* Page metadata
* Page history/version history where supported
* Attachments
* Embedded documents
* Embedded images
* Links to SharePoint
* Links to external documents
* Links to Jira issues
* Links to Jira projects
* Links to other Confluence pages
* Internal Confluence links
* Page restrictions
* User/group permissions
* Search
* Page labels
* Comments where applicable

Pay particular attention to **broken links and remapping of Jira/Confluence references after migration**.

---

# 6. Primary Objective

Create a **detailed, practical, execution-ready smoke-test suite** that the Migration Team can execute immediately after completing the Jira and Confluence Test Environment migration.

The tests must determine whether the migrated environment is sufficiently healthy to be handed over to the Application/Project Team.

The test suite must cover:

1. Migration completeness
2. Data integrity
3. Configuration integrity
4. Functional integrity
5. User access
6. Jira project functionality
7. Xray functionality
8. Sprint and board functionality
9. Link and relationship integrity
10. Attachments
11. History and audit information
12. Confluence content integrity
13. Confluence navigation
14. Integrations
15. Search and reporting
16. Permissions and security
17. Regression/smoke validation
18. Handover readiness

---

# 7. Test Design Principles

Create tests that are:

* Specific
* Repeatable
* Unambiguous
* Actionable
* Execution-ready
* Suitable for Jira/Confluence administrators
* Suitable for Scrum Masters/Project Managers
* Suitable for QA/Test Leads
* Suitable for application/business teams
* Traceable to the migration scope

Avoid vague tests such as:

> Check whether Jira works.

Instead, create actionable tests such as:

> Open a migrated Bug from the SFDC Development project and verify the issue key, summary, description, priority, status, assignee, reporter, labels, components, fix version, custom fields, comments, attachments, linked issues, and change history.

---

# 8. Required Test Coverage

## 8.1 Environment and Accessibility

Validate:

* Jira Cloud URL
* Confluence Cloud URL
* Login
* SSO
* User authentication
* User access
* Group access
* Project access
* Space access
* Basic navigation
* Browser access
* Cloud environment availability

---

## 8.2 Jira Project Validation

For both:

* SFDC Development
* SFDC Operations

Validate:

* Project existence
* Project key
* Project name
* Project type
* Project configuration
* Project settings
* Project roles
* Project permissions
* Issue creation
* Issue editing
* Issue viewing
* Issue searching
* Issue transitions

---

## 8.3 Jira Issue-Type Validation

Explicitly cover all of the following:

* Bug
* Epic
* Feature
* Pre-condition
* Spike
* Sub-test Execution
* Sub-task
* Task
* Test
* Test Execution
* Test Plan
* Test Set
* User Story

For representative migrated records, validate:

* Issue key
* Issue type
* Summary
* Description
* Status
* Priority
* Reporter
* Assignee
* Components
* Versions
* Labels
* Custom fields
* Comments
* Attachments
* Links
* Parent/child relationships
* History

---

## 8.4 Jira Configuration

Validate:

* Workflows
* Workflow statuses
* Workflow transitions
* Screens
* Screen schemes
* Custom fields
* Field configurations
* Priorities
* Resolutions
* Versions
* Components
* Project roles
* Permission schemes
* Notification schemes
* Issue security
* Project settings

Where configuration cannot be validated through direct comparison, provide a practical functional validation approach.

---

# 9. Jira Data Integrity

Validate representative records from:

* Recent issues
* Old issues
* Open issues
* Closed issues
* High-priority issues
* Issues with comments
* Issues with attachments
* Issues with multiple links
* Issues with custom fields
* Issues with subtasks
* Issues associated with Epics
* Issues associated with Versions
* Issues associated with Components

Verify:

* Issue count
* Missing issues
* Duplicate issues
* Issue key preservation
* Comment preservation
* Attachment preservation
* History preservation
* Worklog preservation
* Link preservation

---

# 10. Jira Relationships and Links

Explicitly test:

* Blocks / is blocked by
* Relates to
* Duplicates / is duplicated by
* Parent / child
* Epic / child issues
* Subtask / parent issue
* Xray relationships
* Jira issue links
* Remote links
* Cross-project links
* Links between SFDC Development and SFDC Operations

Verify that links navigate to the correct Cloud destination.

---

# 11. Attachments

Validate:

* Existing attachments are present
* Attachment names are correct
* Attachment counts are correct
* Attachments can be opened
* Attachments can be downloaded
* File contents are not corrupted
* Images render correctly
* Documents open correctly
* Representative large attachments are accessible

---

# 12. Jira Search and Reporting

Validate:

* Basic search
* Advanced/JQL search
* Project filtering
* Issue-type filtering
* Status filtering
* Assignee filtering
* Priority filtering
* Version filtering
* Component filtering
* Custom-field filtering
* Historical issue searches
* Saved filters
* Reports
* Dashboard gadgets where applicable

Verify that migrated issues can be found using expected search criteria.

---

# 13. Scrum Boards

Validate:

* Board availability
* Board name
* Board filter
* Columns
* Status mapping
* Quick filters
* Swimlanes
* Issue visibility
* Sprint association
* Backlog
* Active sprint
* Completed sprint
* Future sprint
* Sprint history

---

# 14. Kanban Boards

Validate:

* Board availability
* Board filter
* Columns
* Status mapping
* Quick filters
* Swimlanes
* Issue visibility
* Ranking
* Backlog where applicable
* Historical data

---

# 15. Sprint and Historical Data

Validate:

* Sprint names
* Sprint dates
* Sprint status
* Sprint membership
* Completed sprints
* Previous sprint history
* Future sprints
* Active sprint
* Issues associated with sprints
* Burndown reports where applicable
* Velocity reports where applicable
* Historical reporting

Do not limit validation to the current sprint.

---

# 16. Xray Validation

Create dedicated Xray tests.

## Xray Availability

Validate:

* Xray is installed/available
* Xray functionality is accessible
* Authorized users can access Xray

## Xray Test Cases

Validate:

* Test issue type
* Test steps
* Test data
* Expected results
* Preconditions
* Attachments/evidence
* Test status

## Xray Test Sets

Validate:

* Test Set exists
* Tests are associated correctly
* Test Set information is preserved

## Xray Test Executions

Validate:

* Test Execution exists
* Associated tests are correct
* Execution status is correct
* Test results are available
* Execution history is preserved

## Xray Test Plans

Validate:

* Test Plan exists
* Test Executions are linked
* Tests are associated correctly

## Xray Traceability

Validate the end-to-end relationship:

**Requirement → Test → Test Execution → Defect**

Verify that each relationship is preserved and navigable.

## Xray Reporting

Validate relevant Xray test management and reporting functions.

Do not assume that successful migration of standard Jira issues proves successful Xray migration.

---

# 17. Jira Integrations

Validate all integrations explicitly included in the migration scope.

Examples may include:

* Development tools
* Source control integrations
* CI/CD integrations
* Build integrations
* Deployment integrations
* Jira development panels
* Commit links
* Pull/merge request links
* Build information

If specific third-party tools are not provided, use:

> Configured development tool integration within the migration scope

Do not invent specific integration names.

---

# 18. Jira Permissions and Security

Validate using appropriate test accounts/roles:

* Administrator
* Project Administrator
* Developer
* Tester
* Viewer/Read-only user
* Restricted user

Verify:

* Authorized users can access required projects
* Unauthorized users cannot access restricted projects
* Users can perform expected actions
* Restricted issues remain restricted
* Project permissions are preserved
* Issue security is preserved

---

# 19. Confluence Space Validation

Validate:

* SFSUPPORTDE space exists
* Space key is preserved
* Space name is correct
* Space permissions are correct
* Authorized users can access the space
* Unauthorized users cannot access restricted content

---

# 20. Confluence Page Validation

Validate representative:

* Top-level pages
* Nested pages
* Old pages
* Recently updated pages
* Large pages
* Pages containing tables
* Pages containing images
* Pages containing macros
* Pages containing attachments
* Pages containing Jira references

Validate:

* Page title
* Page content
* Formatting
* Page hierarchy
* Tables
* Images
* Macros
* Attachments
* Labels
* Restrictions
* Comments where applicable

---

# 21. Confluence Attachments and Embedded Documents

Validate:

* Attachments exist
* Attachment names are preserved
* Attachments open
* Attachments download
* Embedded documents open
* Embedded images render
* Files are not corrupted

Use representative document types where available.

Do not invent document types that are not present in the source environment.

---

# 22. Confluence Links

Explicitly validate:

### Jira Links

* Jira issue links
* Jira project links
* Jira filters where applicable

### Confluence Links

* Links to other SFSUPPORTDE pages
* Parent/child navigation
* Internal links

### External Links

* SharePoint links
* External websites
* External documents

Verify that links are not unexpectedly broken after migration.

If an On-Premises URL is intentionally no longer valid after migration, classify it as an **expected migration exception** rather than automatically marking the test as failed.

---

# 23. Confluence Search

Validate:

* Page search
* Keyword search
* Page title search
* Attachment search where supported
* Search for known migrated content
* Search by label where applicable

Verify that expected migrated pages can be found.

---

# 24. Jira-Confluence Cross-Platform Validation

Validate:

* Confluence pages linking to Jira issues
* Jira issues linking to Confluence pages
* Jira macros embedded in Confluence
* Jira issue references
* Jira project references
* Navigation between Jira Cloud and Confluence Cloud

Verify that migrated references point to the correct Cloud locations.

---

# 25. Data Reconciliation

Create explicit tests for source-to-target reconciliation.

Where source counts/reports are available, validate:

* Total Jira issues
* Issues by project
* Issues by issue type
* Issues by status
* Issues by priority
* Issues by version
* Issues by component
* Xray issue counts
* Test Sets
* Test Executions
* Test Plans
* Test Cases
* Confluence page counts
* Attachment counts where available

Do not invent actual counts.

Use placeholders such as:

* `<SOURCE_COUNT>`
* `<TARGET_COUNT>`
* `<SOURCE_ISSUE_KEY>`
* `<TARGET_ISSUE_KEY>`
* `<SOURCE_PAGE_NAME>`
* `<SOURCE_ATTACHMENT_NAME>`

---

# 26. Migration Exceptions

Create tests to identify:

* Missing records
* Duplicate records
* Broken links
* Missing attachments
* Incorrect permissions
* Missing users
* Incorrect user mapping
* Missing comments
* Missing history
* Incorrect statuses
* Incorrect workflow mappings
* Missing custom fields
* Incorrect custom-field values
* Missing Xray data
* Missing Confluence pages
* Incorrect page hierarchy
* Broken embedded content

---

# 27. Handover Readiness

Create final handover tests/checks covering:

* Critical Jira functions
* Critical Xray functions
* Critical Confluence functions
* User access
* Permissions
* Data integrity
* Attachments
* Links
* Boards
* Sprint history
* Search
* Integrations
* No Severity 1/Critical migration defects
* No unresolved data-loss issues
* Known migration exceptions documented
* Migration Team sign-off readiness

---

# 28. Required Test Case Format

Every test case must follow this format:

```text
TestID|Test Name|Description|Pre-requisite|testStep|TestAction|Expected Result|Priority|
```

## Formatting Rules

The following fields must appear **only on the first line of each test case**:

* TestID
* Test Name
* Description
* Pre-requisite
* Priority

The following fields may contain multiple lines:

* Test Step
* Test Action
* Expected Result

Continuation lines must **not repeat**:

* TestID
* Test Name
* Description
* Pre-requisite
* Priority

There must be **exactly one blank line between two test cases**.

---

# 29. Example Test Case

```text
JIRA-001|Verify SFDC Development project exists|Verify that the migrated SFDC Development Jira project is available in Cloud with the expected project identity and basic configuration.|Test Environment migration is completed; tester has valid Jira Cloud access|1. Log in to Jira Cloud.
2. Navigate to Projects.
3. Search for SFDC Development.
4. Open the project.
5. Verify the project key and project name.|The SFDC Development project is displayed and can be opened successfully.
The project key and project name match the expected source environment values.
Project navigation is available without errors.|Critical|

JIRA-002|Verify migrated Bug issue|Verify that a representative Bug migrated from the SFDC Development project retains its core data and relationships.|A known source Bug issue key is available; tester has access to the migrated project|1. Search for the migrated Bug using its issue key.
2. Open the issue.
3. Verify Summary, Description, Status, Priority, Reporter and Assignee.
4. Verify Components, Fix Version, Labels and custom fields.
5. Verify comments.
6. Verify attachments.
7. Verify issue links.
8. Open the issue history.|The migrated Bug is available using the expected issue key.
Core field values match the corresponding source issue.
Comments and attachments are available.
Issue links point to the expected migrated records.
History is available and consistent with the source.|High|
```

Do not use the example as the complete output.

---

# 30. Test ID Convention

Use unique Test IDs.

Recommended prefixes:

| Prefix | Purpose                       |
| ------ | ----------------------------- |
| ENV    | Environment/access            |
| JIRA   | General Jira                  |
| DEV    | SFDC Development              |
| OPS    | SFDC Operations               |
| CFG    | Jira configuration            |
| DATA   | Data integrity/reconciliation |
| BOARD  | Scrum/Kanban boards           |
| SPRINT | Sprint/history                |
| XRAY   | Xray                          |
| INT    | Integrations                  |
| SEC    | Security/permissions          |
| CONF   | Confluence                    |
| LINK   | Links/navigation              |
| ATT    | Attachments                   |
| SEARCH | Search/reporting              |
| HAND   | Handover readiness            |

Example:

```text
ENV-001
JIRA-001
DEV-001
OPS-001
CFG-001
DATA-001
BOARD-001
SPRINT-001
XRAY-001
INT-001
SEC-001
CONF-001
LINK-001
ATT-001
SEARCH-001
HAND-001
```

Every Test ID must be unique.

---

# 31. Priority

Use only:

* Critical
* High
* Medium
* Low

### Critical

Use for tests where failure could indicate:

* Data loss
* Major migration failure
* Security failure
* Project unavailability
* Xray unavailability
* Major traceability loss
* Severe data corruption

### High

Use for important functional or data validation.

### Medium

Use for important but non-critical validation.

### Low

Use for secondary/non-blocking validation.

---

# 32. Number of Tests

Create a **comprehensive test suite containing approximately 80–120 distinct test cases**.

Do not create duplicate tests simply to increase the test count.

Ensure meaningful coverage across:

* Both Jira projects
* All Jira issue types
* Jira configuration
* Data
* Boards
* Sprints
* Xray
* Integrations
* Security
* Confluence
* Attachments
* Links
* Search
* Reconciliation
* Handover

---

# 33. Source-to-Target Validation

For tests requiring comparison between On-Premises and Cloud, explicitly state:

> Compare the Cloud value against the corresponding On-Premises/source value.

Use placeholders rather than fabricated information:

```text
<SOURCE_ISSUE_KEY>
<TARGET_ISSUE_KEY>
<SOURCE_COUNT>
<TARGET_COUNT>
<SOURCE_PAGE_NAME>
<SOURCE_ATTACHMENT_NAME>
<SOURCE_SPRINT_NAME>
<SOURCE_USER>
<CLOUD_USER>
```

Never fabricate:

* Jira issue keys
* Usernames
* Page names
* Counts
* URLs
* Sprint names
* Migration statistics

---

# 34. Test Execution Guidance

Each test must provide enough information for a tester to determine:

1. What needs to be checked
2. Where to check it
3. What data should be used
4. What action should be performed
5. What constitutes a pass
6. What constitutes a failure

Where source comparison is required, explicitly instruct the tester to compare against the source On-Premises environment.

---

# 35. Expected Result Quality

Avoid vague expected results such as:

* "It works."
* "Data is correct."
* "Migration is successful."

Instead use measurable results such as:

> The project is displayed using the expected project key and name, and the tester can open the project without an authorization or application error.

Or:

> The issue contains the same Summary, Description, Status, Priority, Assignee, Reporter, Components, Versions, and custom-field values as the source issue.

Or:

> The attachment is present with the expected filename and can be opened/downloaded without corruption.

Or:

> The Jira issue link opens the corresponding Cloud issue rather than an obsolete On-Premises URL.

---

# 36. Test Suite Organization

Generate tests in the following order:

1. Environment & Access
2. Jira Project Validation
3. Jira Issue Types
4. Jira Configuration
5. Jira Data Integrity
6. Jira Links & Relationships
7. Attachments
8. Search & Reporting
9. Scrum Boards
10. Kanban Boards
11. Sprint & Historical Data
12. Xray
13. Integrations
14. Security & Permissions
15. Confluence Space
16. Confluence Pages
17. Confluence Attachments
18. Confluence Links
19. Confluence Search
20. Jira-Confluence Cross Validation
21. Data Reconciliation
22. Migration Exceptions
23. Handover Readiness

---

# 37. Deliverable 1 – Markdown

Create:

`Jira_Confluence_Cloud_Migration_Smoke_Tests.md`

The Markdown deliverable must contain:

1. Title
2. Purpose
3. Scope
4. Assumptions
5. Test execution guidance
6. Priority definitions
7. Complete test cases
8. Handover acceptance criteria
9. Migration defect/exception guidance

The test cases must follow the exact pipe-delimited format specified above.

---

# 38. Deliverable 2 – Excel

Create:

`Jira_Confluence_Cloud_Migration_Smoke_Tests.xls`

Use the following columns:

| Column | Name            |
| ------ | --------------- |
| A      | TestID          |
| B      | Test Name       |
| C      | Description     |
| D      | Pre-requisite   |
| E      | Test Step       |
| F      | Test Action     |
| G      | Expected Result |
| H      | Priority        |
| I      | Test Result     |
| J      | Actual Result   |
| K      | Defect ID       |
| L      | Executed By     |
| M      | Execution Date  |
| N      | Comments        |

For the Excel output:

* Each test must have a unique TestID.
* Preserve all test information.
* Leave execution fields blank.
* Apply filters to the header.
* Freeze the header row.
* Use readable column widths.
* Enable text wrapping.
* Preserve multiline actions/results.
* Do not merge cells in a way that prevents filtering/sorting.
* Make the workbook suitable for actual test execution.

If the environment cannot generate a binary `.xls` file, provide an **Excel-compatible tabular representation** that can be saved/imported as `.xls`.

Do not falsely claim that a binary `.xls` file was generated if the environment does not support binary Excel generation.

---

# 39. Consistency Between Deliverables

The Markdown and Excel outputs must contain exactly the same test cases.

Before finalizing, verify:

* Same number of tests
* Same Test IDs
* Same Test Names
* Same Descriptions
* Same Pre-requisites
* Same Test Steps
* Same Test Actions
* Same Expected Results
* Same Priorities

No test may exist in only one deliverable.

---

# 40. Final Quality Review

Before producing the final output, verify that:

* [ ] Both SFDC Development and SFDC Operations are covered.
* [ ] All 13 Jira issue types are covered.
* [ ] Workflows are covered.
* [ ] Screens are covered.
* [ ] Custom fields are covered.
* [ ] Priorities are covered.
* [ ] Project settings are covered.
* [ ] Versions are covered.
* [ ] Components are covered.
* [ ] Roles and permissions are covered.
* [ ] Notification schemes are covered.
* [ ] Development integrations are covered.
* [ ] Scrum boards are covered.
* [ ] Kanban boards are covered.
* [ ] Previous sprint history is covered.
* [ ] Attachments are covered.
* [ ] Jira links are covered.
* [ ] Issue relationships are covered.
* [ ] Linked tickets are covered.
* [ ] Comments are covered.
* [ ] History is covered.
* [ ] Audit information is covered where supported.
* [ ] Xray availability is covered.
* [ ] Xray Test Cases are covered.
* [ ] Xray Test Sets are covered.
* [ ] Xray Test Executions are covered.
* [ ] Xray Test Plans are covered.
* [ ] Xray Preconditions are covered.
* [ ] Xray traceability is covered.
* [ ] Confluence SFSUPPORTDE is covered.
* [ ] Confluence pages are covered.
* [ ] Page hierarchy is covered.
* [ ] Page content is covered.
* [ ] Attachments are covered.
* [ ] Embedded documents are covered.
* [ ] Jira links are covered.
* [ ] SharePoint/external links are covered.
* [ ] Internal Confluence links are covered.
* [ ] Search is covered.
* [ ] Permissions are covered.
* [ ] Jira-Confluence navigation is covered.
* [ ] Data reconciliation is covered.
* [ ] Migration exceptions are covered.
* [ ] Handover readiness is covered.
* [ ] Tests are actionable.
* [ ] Expected results are measurable.
* [ ] No real migration data has been fabricated.
* [ ] Test IDs are unique.
* [ ] Markdown and Excel contain identical test cases.

---

# 41. Final Response

Return the following two deliverables:

1. `Jira_Confluence_Cloud_Migration_Smoke_Tests.md`
2. `Jira_Confluence_Cloud_Migration_Smoke_Tests.xls`

Do not return only a sample.

Generate the **complete 80–120 test case suite**.

The final test suite must be detailed enough for the Migration Team to execute during **Test Environment handover** and reusable for **Production migration validation**.
