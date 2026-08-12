# Jira & Confluence Cloud Migration Smoke Test Suite

**Document:** Jira_Confluence_Cloud_Migration_Smoke_Tests.md
**Companion file:** Jira_Confluence_Cloud_Migration_Smoke_Tests.xlsx
**Generated:** 2026-08-12
**Total test cases:** 120

---

## 1. Purpose

This document is a comprehensive, execution-ready smoke-test and handover-validation suite for the migration of Jira and Confluence from **On-Premises to Atlassian Cloud**. It is intended to be used by:

- The **Migration Team**, immediately after completing the Test Environment migration, to perform sanity checks before handover.
- The **Application/Project Team**, during the 1-2 week Test Environment validation window following handover.
- Both teams again during **Production migration validation**, reusing the same critical (Critical/High priority) test cases.

## 2. Scope

### 2.1 Jira Projects
- **SFDC Development**
- **SFDC Operations**

Includes projects, issue types, workflows, screens, custom fields, priorities/resolutions, project settings, versions, components, roles/permissions, notification/permission/issue-security schemes, users/groups, comments, attachments, history/worklogs, issue links/relationships, sprints, Scrum/Kanban boards, filters, dashboards, and audit information where supported.

### 2.2 Jira Issue Types (13, explicitly validated)
Bug, Epic, Feature, Pre-condition, Spike, Sub-test Execution, Sub-task, Task, Test, Test Execution, Test Plan, Test Set, User Story.

### 2.3 Xray
Xray is treated as a **critical, mandatory** component: Test Cases, Test Sets, Test Executions, Test Plans, Preconditions, test steps/data/evidence, and end-to-end Requirement -> Test -> Test Execution -> Defect traceability.

### 2.4 Confluence
Space in scope: **SFSUPPORTDE** - space permissions, all pages, hierarchy, content/formatting/tables, images, macros, attachments, embedded documents, links (Jira, Confluence-internal, SharePoint, external), search, labels, restrictions, and comments where applicable.

## 3. Assumptions

- Actual issue keys, usernames, page names, attachment names, sprint names, and counts are **not fabricated** in this suite. Placeholders (e.g. `<SOURCE_ISSUE_KEY>`, `<TARGET_ISSUE_KEY>`, `<SOURCE_COUNT>`, `<TARGET_COUNT>`, `<SOURCE_PAGE_NAME>`, `<SOURCE_ATTACHMENT_NAME>`, `<SOURCE_SPRINT_NAME>`, `<SOURCE_USER>`, `<CLOUD_USER>`) must be replaced by the tester with real values from the source/target environments and the Migration Team's pre-migration reports before/while executing each test.
- Test Environment migration (Phase 1) has completed and the Migration Team has performed its own initial technical sanity checks before this suite is executed.
- Where a value cannot be compared directly (e.g. legacy On-Premises URLs that are intentionally deprecated), the tester classifies the result as a **documented migration exception** rather than an automatic failure (see Section 9).
- This suite validates functional/data/configuration integrity from a tester's perspective; it does not replace the Migration Team's own technical/infrastructure-level migration logs.
- The same Critical and High priority test cases in this suite are intended to be **re-executed against Production** after the Phase 2 migration.

## 4. Test Execution Guidance

For every test case, the tester must be able to determine:

1. **What** needs to be checked (Test Name / Description).
2. **Where** to check it (Test Step navigation path).
3. **What data** to use (Pre-requisite, and any `<SOURCE_...>` placeholder replaced with real data).
4. **What action** to perform (Test Action).
5. **What constitutes a Pass** (Expected Result).
6. **What constitutes a Fail** (any deviation from the Expected Result not covered by a documented exception).

Where a test requires comparing Cloud data against the source, the tester must explicitly **compare the Cloud value against the corresponding On-Premises/source value** before marking the result.

Record execution results (Test Result, Actual Result, Defect ID, Executed By, Execution Date, Comments) in the companion Excel workbook, `Jira_Confluence_Cloud_Migration_Smoke_Tests.xlsx`, which contains identical test cases to this document plus execution-tracking columns.

## 5. Priority Definitions

| Priority | Meaning |
|---|---|
| **Critical** | Failure could indicate data loss, major migration failure, security failure, project/space unavailability, Xray unavailability, major traceability loss, or severe data corruption. Must be resolved before handover. |
| **High** | Important functional or data validation. Should be resolved or explicitly risk-accepted before handover. |
| **Medium** | Important but non-blocking validation. May be tracked for resolution during the validation window. |
| **Low** | Secondary/non-blocking validation. May be deferred with agreement from both teams. |

## 6. Required Test Case Format

```text
TestID|Test Name|Description|Pre-requisite|testStep|TestAction|Expected Result|Priority|
```

`TestID`, `Test Name`, `Description`, `Pre-requisite`, and `Priority` appear only once, on the first line. `Test Step`, `Test Action`, and `Expected Result` may span multiple lines and are separated from each other only by the pipe (`|`) character; continuation lines do not repeat the single-occurrence fields. Exactly one blank line separates two test cases.

---

## 7. Test Cases

### 1. Environment & Access

```text
ENV-001|Verify Jira Cloud URL and login|Verify that the migrated Jira Cloud site is reachable and that a valid migrated user can log in.|Test Environment migration is complete; tester has a migrated Jira Cloud user account and the Cloud site URL|1. Open the migrated Jira Cloud URL in a supported browser.
2. Enter the credentials of a migrated user (or authenticate via SSO if configured).
3. Observe the landing page after successful authentication.|Confirm the URL resolves to the correct Jira Cloud tenant (not the old On-Premises URL).
Confirm login succeeds without certificate, redirect, or authentication errors.
Confirm the user lands on the Jira Cloud dashboard/home screen.|The Jira Cloud URL loads without error and displays the correct Cloud tenant.
The migrated user authenticates successfully and reaches the Jira home/dashboard screen without being redirected to the legacy On-Premises URL.|Critical|

ENV-002|Verify Confluence Cloud URL and login|Verify that the migrated Confluence Cloud site is reachable and that a valid migrated user can log in.|Test Environment migration is complete; tester has a migrated Confluence Cloud user account and the Cloud site URL|1. Open the migrated Confluence Cloud URL in a supported browser.
2. Enter the credentials of a migrated user (or authenticate via SSO if configured).
3. Observe the landing page after successful authentication.|Confirm the URL resolves to the correct Confluence Cloud tenant.
Confirm login succeeds without certificate, redirect, or authentication errors.
Confirm the user lands on the Confluence Cloud home screen.|The Confluence Cloud URL loads without error and displays the correct Cloud tenant.
The migrated user authenticates successfully and reaches the Confluence home screen without errors.|Critical|

ENV-003|Verify SSO/authentication for migrated users|Verify that Single Sign-On (or the configured authentication method) works correctly for migrated user accounts on both Jira Cloud and Confluence Cloud.|SSO/authentication has been configured for the Cloud tenant; at least one migrated user account is available for testing|1. Navigate to the Jira Cloud login page and initiate SSO login (or standard login if SSO is not in scope).
2. Complete authentication using a migrated user identity.
3. Repeat steps 1-2 for the Confluence Cloud login page.|Verify the user is redirected to the correct identity provider (if SSO is used).
Verify the same migrated identity works for both Jira Cloud and Confluence Cloud.
Verify no duplicate/orphaned account prompts appear.|The migrated user authenticates successfully on both Jira Cloud and Confluence Cloud using a single identity.
No authentication errors, account-linking prompts, or duplicate-account warnings occur.|Critical|

ENV-004|Verify project and space level access for authorized users|Verify that migrated users retain access to the Jira projects and Confluence space they were authorized for prior to migration.|A test user known to have had access to SFDC Development, SFDC Operations and the SFSUPPORTDE space in the source environment is available|1. Log in to Jira Cloud as the test user.
2. Navigate to the SFDC Development and SFDC Operations projects.
3. Log in to Confluence Cloud as the same test user.
4. Navigate to the SFSUPPORTDE space.|Confirm the user can open both Jira projects without an authorization error.
Confirm the user can open the SFSUPPORTDE space without an authorization error.
Compare the resulting access level against the corresponding On-Premises/source access (<SOURCE_USER> access level).|The test user can access SFDC Development, SFDC Operations, and SFSUPPORTDE without permission errors.
The user's access level in Cloud matches the access level recorded for <SOURCE_USER> in the source environment.|Critical|

ENV-005|Verify basic navigation and browser compatibility|Verify that core Jira Cloud and Confluence Cloud navigation elements render and function correctly across the supported browser(s).|Test Environment migration is complete; tester has access to the supported browser(s) used by the organization|1. Log in to Jira Cloud and navigate through the top navigation bar, project sidebar, and issue navigator.
2. Log in to Confluence Cloud and navigate through the space sidebar, page tree, and top navigation bar.
3. Repeat on any additional officially supported browser.|Confirm all primary navigation menus render and respond to clicks.
Confirm no layout/rendering errors are present.
Confirm no JavaScript console errors block core navigation (where tester tooling allows).|All primary Jira Cloud and Confluence Cloud navigation elements load and function correctly in the supported browser(s).
No blocking rendering or navigation errors are observed.|Medium|
```

### 2. Jira Project Validation

```text
JIRA-001|Verify both migrated Jira projects are listed|Verify that both in-scope Jira projects, SFDC Development and SFDC Operations, appear in the Jira Cloud Projects directory.|Test Environment migration is completed; tester has valid Jira Cloud access|1. Log in to Jira Cloud.
2. Navigate to Projects > View all projects.
3. Locate SFDC Development and SFDC Operations in the list.|Verify both project names appear exactly as in the source environment.
Verify both project keys are displayed alongside the project names.
Verify both projects can be opened from the directory.|SFDC Development and SFDC Operations are both listed in the Projects directory with the expected project names and keys.
Both projects open successfully when selected.|Critical|

JIRA-002|Verify issue creation works in migrated projects|Verify that a new issue can be created in each migrated project after migration, confirming the project configuration supports normal operation.|Tester has Create Issue permission in SFDC Development and SFDC Operations|1. Open SFDC Development and select Create issue.
2. Select an available issue type (e.g. Task) and populate the mandatory fields.
3. Submit the issue and note the generated issue key.
4. Repeat steps 1-3 for SFDC Operations.|Verify the issue type list matches the expected migrated issue type scheme.
Verify mandatory fields are enforced as expected.
Verify the new issue is created and opens successfully in each project.|A new issue can be created successfully in both SFDC Development and SFDC Operations without configuration errors.
Each new issue receives a valid issue key using the project's expected key prefix.|High|

JIRA-003|Verify issue editing, viewing, and transitions work in migrated projects|Verify that existing migrated issues can be viewed, edited, and transitioned through their workflow in both projects.|A known migrated issue key is available in each project; tester has Edit/Transition permissions|1. Open <SOURCE_ISSUE_KEY> in SFDC Development.
2. Edit a non-critical field (e.g. add a label) and save.
3. Perform an available workflow transition and confirm the new status.
4. Repeat steps 1-3 using an equivalent issue in SFDC Operations.|Verify the edit is saved without error.
Verify the workflow transition options match the expected migrated workflow.
Verify the issue status updates correctly after the transition.|Issues in both projects can be viewed, edited, and transitioned without errors.
The workflow transitions offered match the expected source workflow for the issue type.|High|

DEV-001|Verify SFDC Development project identity and configuration|Verify that the SFDC Development project retains its correct project key, name, project type, lead, and general configuration after migration.|Test Environment migration is completed; tester has access to SFDC Development|1. Navigate to the SFDC Development project.
2. Open Project settings > Details.
3. Compare the Project key, Project name, Project type, and Project lead against the source environment.|Compare the Cloud value against the corresponding On-Premises/source value for project key, name, type, and lead.
Verify the project category (if used) is preserved.|SFDC Development displays the same project key, name, project type, and lead as the source environment.
No configuration discrepancies are found when compared to <SOURCE_COUNT>/source configuration records.|Critical|

DEV-002|Verify SFDC Development project roles and permissions|Verify that project roles (e.g. Administrators, Developers, Testers) and their permission scheme assignments are preserved for SFDC Development.|Tester has Project Administrator access to SFDC Development|1. Open SFDC Development > Project settings > People.
2. Review the members assigned to each project role.
3. Open Project settings > Permissions and review the associated permission scheme.|Compare project role membership against the source environment's role assignments (<SOURCE_USER> mappings).
Verify the permission scheme name and key permission grants match the source configuration.|Project roles in SFDC Development contain the expected migrated members.
The permission scheme applied matches the source environment's permission scheme and grants.|High|

DEV-003|Verify SFDC Development versions, components, and issue type scheme|Verify that Versions/Releases, Components (including component leads), and the Issue Type Scheme configured for SFDC Development were migrated correctly.|Tester has access to SFDC Development project settings|1. Open Project settings > Versions and review the list of versions/releases.
2. Open Project settings > Components and review components and their leads.
3. Open Project settings > Issue types and review the associated issue type scheme.|Compare the versions list, release/status flags, and dates against the source environment.
Compare each component name and component lead against the source environment.
Compare the issue types available to the project against the expected 13 issue types in scope.|Versions, components (with correct leads), and the issue type scheme in SFDC Development match the source environment.
All expected issue types remain associated with the project.|High|

OPS-001|Verify SFDC Operations project identity and configuration|Verify that the SFDC Operations project retains its correct project key, name, project type, lead, and general configuration after migration.|Test Environment migration is completed; tester has access to SFDC Operations|1. Navigate to the SFDC Operations project.
2. Open Project settings > Details.
3. Compare the Project key, Project name, Project type, and Project lead against the source environment.|Compare the Cloud value against the corresponding On-Premises/source value for project key, name, type, and lead.
Verify the project category (if used) is preserved.|SFDC Operations displays the same project key, name, project type, and lead as the source environment.
No configuration discrepancies are found when compared to the source configuration records.|Critical|

OPS-002|Verify SFDC Operations project roles and permissions|Verify that project roles and their permission scheme assignments are preserved for SFDC Operations.|Tester has Project Administrator access to SFDC Operations|1. Open SFDC Operations > Project settings > People.
2. Review the members assigned to each project role.
3. Open Project settings > Permissions and review the associated permission scheme.|Compare project role membership against the source environment's role assignments (<SOURCE_USER> mappings).
Verify the permission scheme name and key permission grants match the source configuration.|Project roles in SFDC Operations contain the expected migrated members.
The permission scheme applied matches the source environment's permission scheme and grants.|High|

OPS-003|Verify SFDC Operations versions, components, and issue type scheme|Verify that Versions/Releases, Components (including component leads), and the Issue Type Scheme configured for SFDC Operations were migrated correctly.|Tester has access to SFDC Operations project settings|1. Open Project settings > Versions and review the list of versions/releases.
2. Open Project settings > Components and review components and their leads.
3. Open Project settings > Issue types and review the associated issue type scheme.|Compare the versions list, release/status flags, and dates against the source environment.
Compare each component name and component lead against the source environment.
Compare the issue types available to the project against the expected issue types in scope.|Versions, components (with correct leads), and the issue type scheme in SFDC Operations match the source environment.
All expected issue types remain associated with the project.|High|
```

### 3. Jira Issue Types

```text
JIRA-004|Verify migrated Bug issue type retains core data|Verify that a representative Bug issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Bug issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Bug using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Bug and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Bug issue is retrievable by its expected issue key and displays Bug as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|Critical|

JIRA-005|Verify migrated Epic issue type retains core data|Verify that a representative Epic issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Epic issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Epic using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Epic and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Epic issue is retrievable by its expected issue key and displays Epic as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|Critical|

JIRA-006|Verify migrated Feature issue type retains core data|Verify that a representative Feature issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Feature issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Feature using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Feature and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Feature issue is retrievable by its expected issue key and displays Feature as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-007|Verify migrated Pre-condition issue type retains core data|Verify that a representative Pre-condition issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Pre-condition issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Pre-condition using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Pre-condition and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Pre-condition issue is retrievable by its expected issue key and displays Pre-condition as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-008|Verify migrated Spike issue type retains core data|Verify that a representative Spike issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Spike issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Spike using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Spike and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Spike issue is retrievable by its expected issue key and displays Spike as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|Medium|

JIRA-009|Verify migrated Sub-test Execution issue type retains core data|Verify that a representative Sub-test Execution issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Sub-test Execution issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Sub-test Execution using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Sub-test Execution and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Sub-test Execution issue is retrievable by its expected issue key and displays Sub-test Execution as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-010|Verify migrated Sub-task issue type retains core data|Verify that a representative Sub-task issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Sub-task issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Sub-task using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Sub-task and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Sub-task issue is retrievable by its expected issue key and displays Sub-task as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-011|Verify migrated Task issue type retains core data|Verify that a representative Task issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Task issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Task using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Task and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Task issue is retrievable by its expected issue key and displays Task as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-012|Verify migrated Test issue type retains core data|Verify that a representative Test issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Test issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Test using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Test and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Test issue is retrievable by its expected issue key and displays Test as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|Critical|

JIRA-013|Verify migrated Test Execution issue type retains core data|Verify that a representative Test Execution issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Test Execution issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Test Execution using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Test Execution and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Test Execution issue is retrievable by its expected issue key and displays Test Execution as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|Critical|

JIRA-014|Verify migrated Test Plan issue type retains core data|Verify that a representative Test Plan issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Test Plan issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Test Plan using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Test Plan and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Test Plan issue is retrievable by its expected issue key and displays Test Plan as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-015|Verify migrated Test Set issue type retains core data|Verify that a representative Test Set issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source Test Set issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated Test Set using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as Test Set and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated Test Set issue is retrievable by its expected issue key and displays Test Set as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|

JIRA-016|Verify migrated User Story issue type retains core data|Verify that a representative User Story issue migrated from SFDC Development or SFDC Operations retains its core field data, relationships, and history.|A known source User Story issue key (<SOURCE_ISSUE_KEY>) is available; tester has access to the migrated project|1. Search for the migrated User Story using its issue key <SOURCE_ISSUE_KEY>.
2. Open the issue and confirm the Issue Type field shows the correct type.
3. Review Summary, Description, Status, Priority, Reporter, Assignee, Components, Versions, Labels and custom fields.
4. Review comments, attachments, issue links, parent/child relationships (where applicable), and issue history.|Verify the issue type is displayed as User Story and matches the source issue type.
Compare each field value against the corresponding source issue.
Verify comments, attachments, links, and history are present and complete.|The migrated User Story issue is retrievable by its expected issue key and displays User Story as its issue type.
All core field values, comments, attachments, links, and history match the corresponding source issue with no data loss.|High|
```

### 4. Jira Configuration

```text
CFG-001|Verify workflow statuses and transitions|Verify that the workflow(s) associated with migrated issue types retain their expected statuses and transitions, including conditions, validators, and post-functions where testable.|Tester has access to a migrated issue in each key workflow (e.g. Bug, Task, Test Execution)|1. Open a migrated issue and review the available status.
2. Attempt each available workflow transition in turn (in a non-production-impacting manner).
3. Where configured, attempt a transition that should be blocked by a condition/validator.|Compare the list of statuses and available transitions against the source workflow diagram/configuration.
Verify transitions restricted by conditions/validators behave the same as in the source environment.
Verify post-function side effects (e.g. auto-assign, field updates) occur as expected.|The workflow statuses and transitions available on the migrated issue match the source workflow definition.
Conditions, validators, and post-functions behave consistently with the source environment.|High|

CFG-002|Verify screens and screen schemes|Verify that Create/Edit/View screens and their screen scheme associations were migrated correctly for each issue type.|Tester has access to create and edit issues of multiple issue types in both projects|1. Open the Create Issue screen for a given issue type and review the fields presented.
2. Open an existing issue and review the fields on the View/Edit screen.
3. Repeat for at least 3 different issue types (e.g. Bug, Test, User Story).|Compare the fields shown on each screen against the expected screen scheme configuration from the source environment.
Verify field order and required/optional indicators match expectations.|Create, Edit, and View screens display the expected fields for each issue type, consistent with the source screen scheme configuration.
No fields are unexpectedly missing or duplicated.|Medium|

CFG-003|Verify custom fields and field configurations|Verify that custom fields used across SFDC Development and SFDC Operations were migrated with correct field type, options, and field configuration behavior.|A list of key custom fields in scope is available; tester has access to a representative migrated issue using those fields|1. Open a migrated issue that uses several custom fields.
2. Review each custom field's label, type (e.g. select list, text, date), and populated value.
3. Open the field configuration (where accessible) and confirm required/optional and field description settings.|Compare each custom field's label, type, options, and value against the source issue.
Verify field configuration behavior (required/hidden/optional) matches the source environment.|All reviewed custom fields display the correct label, type, options, and value consistent with the source issue.
Field configuration behavior matches the source environment.|High|

CFG-004|Verify priorities and resolutions|Verify that the full list of Priorities and Resolutions configured in the source environment is available in Jira Cloud.|Tester has access to Jira Cloud administration or can view priority/resolution values on migrated issues|1. Open a migrated issue and review the Priority field options.
2. Open a migrated closed issue and review the Resolution field value.
3. Where admin access is available, review the full Priorities and Resolutions configuration lists.|Compare the list of available priorities against the source environment's priority scheme.
Compare the list of available resolutions against the source environment's resolution scheme.|All priorities and resolutions from the source environment are present and selectable/displayed correctly in Jira Cloud.
No priority or resolution values are missing or renamed unexpectedly.|Medium|

CFG-005|Verify notification schemes and permission schemes|Verify that the notification scheme and permission scheme associated with each project were migrated and function as expected.|Tester has Project Administrator access and can trigger a test notification event (e.g. issue creation/comment)|1. Open Project settings > Notifications for SFDC Development and SFDC Operations and review the configured events/recipients.
2. Create or comment on a test issue to trigger a notification event.
3. Confirm the expected recipient(s) receive the notification (or verify the configuration matches expectations if live email testing is out of scope).|Compare the notification scheme configuration against the source environment.
Verify the permission scheme referenced by Project settings > Permissions matches the source scheme name and grants.|Notification scheme events and recipients match the source configuration, and a test event generates the expected notification.
The permission scheme in use matches the source environment.|Medium|

CFG-006|Verify issue security schemes and project settings|Verify that Issue Security Schemes and general project settings (e.g. default assignee, request types where applicable) were migrated correctly.|A migrated issue with issue-level security applied is available; tester has Project Administrator access|1. Open a migrated issue configured with an Issue Security Level.
2. Confirm the security level shown and the users/roles able to view it.
3. Open Project settings > general settings and review remaining configuration values.|Compare the issue security level and its associated visibility rules against the source environment.
Compare general project settings values against the source configuration.|The issue security scheme is preserved and restricts visibility consistent with the source environment.
General project settings match the expected source configuration.|High|
```

### 5. Jira Data Integrity

```text
DATA-001|Verify representative recent and historical issues migrated correctly|Verify that both recently created issues and old/historical issues from each project migrated with complete data, confirming migration was not limited to recent records only.|A recent source issue key and an old source issue key are available for each project|1. Open a recently created issue (<SOURCE_ISSUE_KEY>) in SFDC Development.
2. Open an old/historical issue (<SOURCE_ISSUE_KEY>) in SFDC Development.
3. Repeat steps 1-2 for SFDC Operations.|Compare all core fields of the recent issue against the source record.
Compare all core fields of the old/historical issue against the source record.|Both recent and historical issues in each project display complete and accurate data matching the source environment.
No data degradation is observed for older records.|Critical|

DATA-002|Verify open and closed issue status preservation|Verify that both open and closed/resolved issues retain their correct status and resolution after migration.|A known open issue key and a known closed issue key are available in each project|1. Open a known open issue and confirm its Status field.
2. Open a known closed/resolved issue and confirm its Status and Resolution fields.|Compare the Status of the open issue against the source environment.
Compare the Status and Resolution of the closed issue against the source environment.|The open issue displays the same status as in the source environment.
The closed issue displays the same status and resolution as in the source environment.|High|

DATA-003|Verify high-priority issue data integrity|Verify that issues flagged with high/critical priority in the source environment retain their priority, status, and related field data after migration.|A list of known high-priority source issue keys is available|1. Open each high-priority issue (<SOURCE_ISSUE_KEY>) in the migrated project.
2. Review Priority, Status, Assignee, Reporter, and any escalation-related custom fields.|Compare Priority and related field values against the source record for each issue.
Confirm no high-priority issue is missing from the migrated project.|All sampled high-priority issues are present in Cloud with Priority and related fields matching the source environment.
No high-priority issue is found to be missing.|Critical|

DATA-004|Verify issues with comments, attachments, and multiple links preserved|Verify that issues containing comments, attachments, and multiple issue links retain all associated data after migration.|A known source issue key containing comments, attachments, and multiple links is available|1. Open <SOURCE_ISSUE_KEY> and count the number of comments, attachments, and issue links.
2. Open each comment and confirm author, timestamp, and content.
3. Open each attachment and confirm it opens correctly.
4. Open each linked issue and confirm the link type and target.|Compare comment count, author, timestamp, and content against the source issue.
Compare attachment count and integrity against the source issue.
Compare link count, link type, and link target against the source issue.|The migrated issue shows the same number of comments, attachments, and links as the source, with matching content, authorship, and timestamps.
All attachments open without corruption and all links resolve to the correct migrated targets.|High|

DATA-005|Verify issues with subtasks, Epic links, versions, and component associations preserved|Verify that parent/subtask relationships, Epic associations, and Version/Component assignments are preserved for representative issues.|A known source issue key with subtasks and Epic/Version/Component associations is available|1. Open <SOURCE_ISSUE_KEY> and review its subtasks (if any).
2. Review the Epic Link (or parent Epic) field.
3. Review the Fix Version(s), Affects Version(s), and Component(s) fields.|Compare subtask list and status against the source issue.
Compare the Epic association against the source issue.
Compare Version and Component assignments against the source issue.|Subtasks, Epic association, Versions, and Components on the migrated issue match the source issue exactly.
No subtask, Epic link, version, or component assignment is missing.|High|
```

### 6. Jira Links & Relationships

```text
LINK-001|Verify 'Blocks/is blocked by' issue links|Verify that Blocks and is blocked by relationships between migrated issues are preserved and navigable.|A known pair of source issues with a Blocks/is blocked by relationship is available|1. Open the blocking issue (<SOURCE_ISSUE_KEY>) and locate the Blocks link in the Linked Issues section.
2. Click through to the blocked issue.
3. Open the blocked issue and confirm the reciprocal 'is blocked by' link back to the first issue.|Verify the link type label matches 'blocks'/'is blocked by' as in the source.
Verify clicking the link navigates to the correct migrated Cloud issue (not a broken/legacy URL).|The Blocks/is blocked by relationship is present on both issues and navigates correctly between the migrated Cloud issues.
The link type and direction match the source environment.|High|

LINK-002|Verify 'Relates to' and 'Duplicates/is duplicated by' issue links|Verify that Relates to and Duplicate relationships between migrated issues are preserved and navigable.|Known source issue pairs with 'Relates to' and 'Duplicates' relationships are available|1. Open an issue (<SOURCE_ISSUE_KEY>) with a 'Relates to' link and confirm the linked issue.
2. Open an issue (<SOURCE_ISSUE_KEY>) with a 'Duplicates'/'is duplicated by' link and confirm the linked issue.|Verify the link type and target match the source environment for both relationship types.
Verify both links navigate to the correct migrated Cloud issue.|'Relates to' and 'Duplicates/is duplicated by' links are present with the correct type and target, and navigate correctly to migrated Cloud issues.
No relationship data is lost.|Medium|

LINK-003|Verify parent/child, Epic/child-issue, and subtask/parent relationships|Verify that hierarchical relationships (Epic to child issues, parent issue to Sub-task) are preserved after migration.|A known Epic with child issues and a known parent issue with subtasks are available|1. Open the Epic (<SOURCE_ISSUE_KEY>) and review its list of child issues.
2. Open one child issue and confirm the Epic Link field points back to the correct Epic.
3. Open a parent issue with subtasks and confirm each subtask is listed and correctly linked.|Compare the child issue list on the Epic against the source environment.
Compare the subtask list and status against the source environment.|The Epic displays the correct, complete list of child issues, and each child correctly references its Epic.
Subtasks remain correctly associated with their parent issue.|High|

LINK-004|Verify remote links and cross-project links between SFDC Development and SFDC Operations|Verify that remote links (e.g. to external systems) and issue links spanning SFDC Development and SFDC Operations are preserved and resolve correctly.|A known issue with a remote link and a known cross-project link between the two projects are available|1. Open an issue (<SOURCE_ISSUE_KEY>) containing a remote link and click through to the destination.
2. Open an issue in SFDC Development that is linked to an issue in SFDC Operations and click through to it.|Verify the remote link destination is correct and reachable (or documented as an expected exception if the destination system is out of migration scope).
Verify the cross-project link opens the correct migrated Cloud issue in SFDC Operations.|The remote link resolves to the expected destination (or is documented as an expected exception).
The cross-project link successfully opens the corresponding migrated issue in the target project.|Medium|

LINK-005|Verify Xray test-to-requirement relationships (issue link level)|Verify that Jira issue links representing Xray 'Tests'/'is tested by' relationships between requirement issues and Test issues are preserved.|A known requirement issue (e.g. User Story) linked to one or more Test issues via Xray is available|1. Open the requirement issue (<SOURCE_ISSUE_KEY>) and locate the 'Tests'/'is tested by' link section.
2. Click through to each linked Test issue.
3. Confirm the Test issue's reciprocal link back to the requirement.|Verify the number and identity of linked Test issues matches the source environment.
Verify the reciprocal link is present and correctly typed on the Test issue.|The requirement issue shows the correct set of linked Test issues, and each Test issue reciprocally links back to the requirement.
No test-to-requirement relationship is lost.|Critical|
```

### 7. Attachments (Jira)

```text
ATT-001|Verify attachment presence and count on a representative issue|Verify that all attachments on a representative migrated issue are present and the count matches the source environment.|A known source issue key with multiple attachments (<SOURCE_ATTACHMENT_NAME> list) is available|1. Open <SOURCE_ISSUE_KEY> and open the Attachments panel.
2. Count the number of attachments and list their filenames.|Compare the attachment count against the source issue.
Compare each attachment filename against the source issue's attachment list.|The migrated issue displays the same number of attachments as the source issue, with matching filenames.
No attachment is missing or renamed.|High|

ATT-002|Verify attachments can be opened and downloaded without corruption|Verify that migrated attachments can be opened in-browser and downloaded, and that file contents are not corrupted.|A known source issue with at least one downloadable attachment is available|1. Open <SOURCE_ISSUE_KEY> and select an attachment to preview (if supported) and to download.
2. Open the downloaded file locally.
3. Compare the file size/content against the equivalent source file where available.|Verify the file opens without a corruption or format error.
Verify the downloaded file size and content are consistent with <SOURCE_ATTACHMENT_NAME>.|The attachment opens and downloads successfully, and the file content is intact and matches the source file.
No corruption, truncation, or format error is observed.|High|

ATT-003|Verify image attachments render correctly|Verify that image attachments (e.g. screenshots) on migrated issues render correctly as thumbnails and in full view.|A known source issue with an image attachment is available|1. Open <SOURCE_ISSUE_KEY> and locate an image attachment.
2. View the thumbnail preview.
3. Open the full-size image view.|Verify the thumbnail renders without a broken-image icon.
Verify the full-size image displays correctly with no distortion, truncation, or missing content.|The image attachment renders correctly as both a thumbnail and in full view, matching the expected source image.
No broken image indicators are present.|Medium|

ATT-004|Verify document attachments open correctly|Verify that document-type attachments (e.g. Office documents, PDFs) present in the source environment open correctly after migration.|A known source issue with a document attachment of a type actually present in the source environment is available|1. Open <SOURCE_ISSUE_KEY> and locate the document attachment.
2. Open/download the document using the appropriate application.
3. Review the document content for completeness.|Verify the document opens without an application/format error.
Verify the document content matches the expected source content (page count, key sections, embedded objects).|The document attachment opens correctly and its content is complete and unmodified compared to the source file.
No corruption or missing content is observed.|Medium|

ATT-005|Verify representative large attachments are accessible|Verify that large attachments (approaching the maximum file size used in the source environment) migrated successfully and remain accessible.|A known source issue containing a large attachment (<SOURCE_ATTACHMENT_NAME>) is available|1. Open the issue containing the large attachment.
2. Attempt to preview (if supported) and download the attachment.
3. Confirm the download completes and the file opens correctly.|Verify the download completes without timeout or truncation.
Verify the file size matches the source file size.|The large attachment downloads completely and opens without corruption, with a file size matching the source.
No timeout, truncation, or size mismatch is observed.|Medium|
```

### 8. Search & Reporting (Jira)

```text
SEARCH-001|Verify basic issue search returns migrated issues|Verify that basic Jira search (quick search / text search) returns expected migrated issues.|A known migrated issue key and a known keyword from its summary are available|1. Use the Jira Cloud quick search bar to search for <SOURCE_ISSUE_KEY>.
2. Use the quick search bar to search for a known keyword from the issue's summary.|Verify the issue key search returns the correct issue directly.
Verify the keyword search returns the expected issue in the result list.|Searching by issue key returns the correct migrated issue.
Searching by keyword returns the expected issue among the results.|High|

SEARCH-002|Verify advanced JQL search across projects, issue types, and fields|Verify that JQL (Advanced search) correctly filters migrated issues by project, issue type, status, assignee, priority, version, component, and custom fields.|Tester has access to the Advanced issue search (JQL) screen|1. Run a JQL query filtering by project = SFDC Development.
2. Run a JQL query filtering by issue type, status, assignee, priority, version, and component individually.
3. Run a JQL query filtering by a known custom field value.|Verify each JQL query returns results consistent with the expected filter criteria.
Verify known migrated issues appear in the results when they meet the filter criteria.|All JQL queries return accurate, filtered results consistent with the criteria used, and known migrated issues are found as expected.
No JQL query errors occur due to missing/misconfigured fields.|High|

SEARCH-003|Verify saved filters and dashboard gadgets display migrated data|Verify that saved filters carried over from the source environment execute correctly and that dashboard gadgets referencing them display migrated data.|A known saved filter name and a dashboard using that filter are available|1. Open Issues > Saved filters and locate the known saved filter.
2. Run the saved filter and review the results.
3. Open the dashboard containing a gadget based on this filter and review the gadget output.|Verify the saved filter's JQL and results match expectations from the source environment.
Verify the dashboard gadget renders results consistent with the underlying filter.|The saved filter runs successfully and returns the expected migrated issues.
The dashboard gadget referencing the filter displays consistent, accurate data.|Medium|

SEARCH-004|Verify historical issue search across sprints and versions|Verify that issues associated with past (closed) sprints and past versions can still be located via search, confirming search is not limited to current/active data.|A known closed sprint name (<SOURCE_SPRINT_NAME>) and a known past version are available|1. Run a JQL search filtering by the closed sprint name.
2. Run a JQL search filtering by a past/released version.|Verify the issues returned match the expected set of issues from the source environment for that sprint/version.
Verify no unexpected issues are missing from the historical result set.|Historical searches by closed sprint and past version return the complete, correct set of migrated issues.
No historical data is found to be missing from search results.|Medium|
```

### 9. Scrum Boards

```text
BOARD-001|Verify Scrum board availability, name, and filter|Verify that the migrated Scrum board for SFDC Development (or SFDC Operations, as applicable) is available with the correct name and board filter.|A known Scrum board name is available for the in-scope project|1. Navigate to the project's Boards section.
2. Open the Scrum board and confirm its name.
3. Open the board's configuration and review the board filter (saved JQL filter).|Compare the board name against the source environment.
Compare the board filter JQL against the source environment.|The Scrum board is available with the expected name and its underlying filter matches the source configuration.
The board opens without errors.|High|

BOARD-002|Verify Scrum board columns and status mapping|Verify that Scrum board columns and their mapped statuses match the source board configuration.|Tester has access to the migrated Scrum board configuration|1. Open the Scrum board configuration > Columns.
2. Review each column name and the statuses mapped to it.|Compare the column names and status mappings against the source board configuration.|Scrum board columns and status mappings match the source environment exactly.
No status is left unmapped or mapped to the wrong column.|Medium|

BOARD-003|Verify Scrum board quick filters and swimlanes|Verify that quick filters and swimlane configuration on the Scrum board were preserved after migration.|Tester has access to the migrated Scrum board|1. Open the Scrum board and review the available quick filters.
2. Apply each quick filter and confirm the board updates accordingly.
3. Review the swimlane configuration (e.g. by Epic, by Assignee, or custom JQL swimlanes).|Compare quick filter names/JQL against the source configuration.
Compare swimlane configuration against the source configuration.|Quick filters and swimlanes match the source board configuration and function correctly when applied.
No quick filter or swimlane is missing.|Medium|

BOARD-004|Verify Scrum board backlog, active sprint, and future sprint visibility|Verify that the board's Backlog view correctly displays active sprint, future sprints, and unassigned backlog issues.|Tester has access to the migrated Scrum board with at least one active and one future sprint|1. Open the Backlog view for the Scrum board.
2. Review the active sprint section and its issue list.
3. Review future sprint sections and the backlog (unscheduled) section.|Compare the active sprint's issue list against the source environment.
Compare future sprint contents and backlog issue order/ranking against the source environment.|The Backlog view correctly displays the active sprint, future sprints, and backlog issues consistent with the source environment.
Issue ranking/order is preserved.|High|
```

### 10. Kanban Boards

```text
BOARD-005|Verify Kanban board availability and filter|Verify that the migrated Kanban board (where applicable) is available with the correct name and board filter.|A known Kanban board name is available for the in-scope project|1. Navigate to the project's Boards section.
2. Open the Kanban board and confirm its name.
3. Review the board's underlying filter.|Compare the board name and filter JQL against the source environment.|The Kanban board is available with the expected name and its filter matches the source configuration.
The board opens without errors.|Medium|

BOARD-006|Verify Kanban board columns, status mapping, and swimlanes|Verify that Kanban board columns, status mapping, and swimlane configuration match the source board configuration.|Tester has access to the migrated Kanban board configuration|1. Open the Kanban board configuration > Columns and review column/status mapping.
2. Review the swimlane configuration.
3. Review any configured quick filters.|Compare columns, status mapping, swimlanes, and quick filters against the source configuration.|Kanban board columns, status mapping, swimlanes, and quick filters match the source environment.
No status is left unmapped.|Medium|

BOARD-007|Verify Kanban board ranking and historical data|Verify that issue ranking/order on the Kanban board and historical (completed) issue data are preserved.|Tester has access to the migrated Kanban board with historical completed issues|1. Open the Kanban board and review the current issue ranking/order in each column.
2. Review the 'Done'/completed issues history (if the board retains historical data).|Compare issue ranking/order against the expected source order.
Compare historical completed issue data against the source environment.|Kanban issue ranking and historical completed issue data are preserved and consistent with the source environment.|Low|
```

### 11. Sprint & Historical Data

```text
SPRINT-001|Verify sprint names, dates, and status preserved|Verify that sprint name, start date, end date, and sprint status (active/closed/future) are preserved after migration.|A known sprint name (<SOURCE_SPRINT_NAME>) is available for comparison|1. Open the board's Backlog or Reports view and locate the sprint <SOURCE_SPRINT_NAME>.
2. Review the sprint's start date, end date, and status.|Compare the sprint name, dates, and status against the source environment.|The sprint name, start/end dates, and status match the source environment exactly.|High|

SPRINT-002|Verify completed sprint history and issue membership|Verify that completed (closed) sprints retain their full list of associated issues and outcome (completed/incomplete/removed).|A known closed sprint name (<SOURCE_SPRINT_NAME>) with a known issue list is available|1. Open the Reports section for the board and select the closed sprint.
2. Review the list of issues that were completed, not completed, and added/removed during the sprint.|Compare the completed/incomplete/removed issue lists against the source environment's sprint report.|The closed sprint's issue membership and completion outcome match the source environment.
No issue is missing from the sprint history.|High|

SPRINT-003|Verify active sprint validation|Verify that the currently active sprint (if one exists at time of migration) displays the correct issues, dates, and progress.|An active sprint exists in the migrated project|1. Open the board and locate the active sprint.
2. Review the sprint's issue list, dates, and progress indicators.|Compare the active sprint's issue list and dates against the source environment.|The active sprint displays the correct issues and dates consistent with the source environment.|High|

SPRINT-004|Verify future/planned sprints|Verify that future (not yet started) sprints and their planned issue assignments are preserved after migration.|A known future sprint name is available in the source environment|1. Open the Backlog view and locate the future sprint.
2. Review the issues planned/assigned to the future sprint.|Compare the future sprint's planned issue list against the source environment.|The future sprint and its planned issues are present and match the source environment.|Medium|

SPRINT-005|Verify burndown and velocity reports where applicable|Verify that Scrum reporting gadgets such as Burndown Chart and Velocity Chart render historical data correctly, where these reports are in scope.|Tester has access to the board Reports section with historical sprint data|1. Open the board's Reports section.
2. Open the Burndown Chart for a completed sprint.
3. Open the Velocity Chart and review historical sprint velocity.|Verify the Burndown Chart renders data consistent with the sprint's known scope/completion.
Verify the Velocity Chart displays historical sprints with plausible completed-vs-committed values.|Burndown and Velocity reports render without error and reflect data consistent with the source environment's historical sprints.|Low|
```

### 12. Xray

```text
XRAY-001|Verify Xray is installed and accessible in Jira Cloud|Verify that the Xray app is installed, licensed, and accessible within the migrated Jira Cloud instance, since Xray is a critical component of this migration.|Tester has an authorized Xray user account on Jira Cloud|1. Log in to Jira Cloud as an authorized user.
2. Navigate to the Xray menu/app section (e.g. via the top navigation or app switcher).
3. Confirm the Xray license/app status.|Verify Xray appears as an installed and active app.
Verify the authorized user can open Xray screens without a licensing or access error.|Xray is installed, licensed, and accessible in Jira Cloud without errors.
Authorized users can open Xray functionality successfully.|Critical|

XRAY-002|Verify migrated Test issue retains steps, data, and expected results|Verify that a representative Test issue migrated via Xray retains its test steps, test data, and expected results.|A known source Test issue key (<SOURCE_ISSUE_KEY>) is available|1. Open the migrated Test issue <SOURCE_ISSUE_KEY>.
2. Open the Test Details/Steps panel and review each step, its test data, and expected result.
3. Review any associated preconditions and evidence/attachments.|Compare the number of steps and their action/data/expected result content against the source Test.
Compare linked preconditions and evidence against the source Test.|The migrated Test issue displays the same steps, test data, and expected results as the source Test, in the same order.
Linked preconditions and evidence are present and unchanged.|Critical|

XRAY-003|Verify migrated Precondition issue type|Verify that a representative Pre-condition issue and its association with dependent Test issues were migrated correctly.|A known source Precondition issue key (<SOURCE_ISSUE_KEY>) linked to one or more Tests is available|1. Open the migrated Precondition issue <SOURCE_ISSUE_KEY>.
2. Review the precondition definition/details.
3. Review the list of associated Test issues.|Compare the precondition content against the source issue.
Compare the list of associated Tests against the source issue.|The Precondition issue's content and its associated Test issues match the source environment exactly.|High|

XRAY-004|Verify Xray Test Set migration|Verify that a Test Set exists in Cloud with the correct associated Tests and Test Set metadata preserved.|A known source Test Set issue key (<SOURCE_ISSUE_KEY>) is available|1. Open the migrated Test Set <SOURCE_ISSUE_KEY>.
2. Review the list of Tests associated with the Test Set.
3. Review the Test Set's summary, description, and any custom fields.|Compare the associated Test list (count and identity) against the source Test Set.
Compare Test Set metadata against the source Test Set.|The Test Set contains the correct, complete list of associated Tests and preserves its metadata, matching the source environment.|High|

XRAY-005|Verify Xray Test Execution migration|Verify that a Test Execution retains its associated Tests, execution status, test run results, and execution history.|A known source Test Execution issue key (<SOURCE_ISSUE_KEY>) is available|1. Open the migrated Test Execution <SOURCE_ISSUE_KEY>.
2. Review the list of associated Tests and their individual run status (Pass/Fail/Executing/Todo).
3. Open one test run's execution details and review recorded evidence/comments.
4. Review the execution's environment/version fields and execution date/history.|Compare associated Tests and their run status against the source Test Execution.
Compare execution evidence, comments, and environment/version fields against the source.|The Test Execution shows the correct associated Tests with matching run status, evidence, and metadata consistent with the source environment.
Execution history is preserved.|Critical|

XRAY-006|Verify Xray Test Plan migration|Verify that a Test Plan retains its linked Test Executions and associated Tests after migration.|A known source Test Plan issue key (<SOURCE_ISSUE_KEY>) is available|1. Open the migrated Test Plan <SOURCE_ISSUE_KEY>.
2. Review the list of linked Test Executions.
3. Review the list of Tests associated with the Test Plan and their overall status.|Compare linked Test Executions against the source Test Plan.
Compare associated Tests and overall status against the source Test Plan.|The Test Plan's linked Test Executions and associated Tests match the source environment, including overall test status.|High|

XRAY-007|Verify end-to-end Xray traceability: Requirement to Test to Test Execution to Defect|Verify that the full traceability chain from a Requirement issue through its Test(s), Test Execution(s), and any linked Defect is preserved and navigable.|A known Requirement issue (<SOURCE_ISSUE_KEY>) linked to a Test, a Test Execution, and a Defect is available|1. Open the Requirement issue and navigate to its linked Test(s) via the Tests panel.
2. From the Test, navigate to its Test Execution(s).
3. From the failed test run (if applicable), navigate to the linked Defect issue.
4. Confirm the Defect links back to the originating Test/Test Execution.|Verify each link in the chain (Requirement -> Test -> Test Execution -> Defect) resolves to the correct migrated Cloud issue.
Verify the traceability report/coverage view (if available) reflects the full chain.|The full Requirement -> Test -> Test Execution -> Defect chain is navigable and each relationship matches the source environment.
No link in the traceability chain is broken or missing.|Critical|

XRAY-008|Verify Xray reporting and test coverage functions|Verify that Xray reporting features (e.g. Test Coverage, Requirement coverage, Traceability report/matrix) render correctly using migrated data.|Tester has access to Xray reporting for SFDC Development and/or SFDC Operations|1. Open the Xray Test Coverage (or equivalent) report for a Requirement issue or a set of Requirements.
2. Review coverage percentages and status breakdown.
3. Open the Traceability Matrix/report (if available) and review the Requirement-to-Test mapping.|Verify coverage figures are consistent with the number and status of migrated Tests/Test Executions.
Verify the traceability report reflects the correct Requirement-to-Test relationships.|Xray reporting functions render successfully and reflect data consistent with the migrated Tests, Test Executions, and Requirements.|Medium|

XRAY-009|Verify Xray test evidence and attachments|Verify that evidence/attachments captured during test execution (e.g. screenshots, logs) are preserved and accessible on migrated Test Executions.|A known Test Execution/test run with attached evidence is available|1. Open the Test Execution and locate the specific test run containing evidence.
2. Open the Evidence section and review each attached file.
3. Download/open each evidence file to confirm it is not corrupted.|Compare the evidence file list and names against the source Test Execution.
Verify each evidence file opens correctly without corruption.|All evidence/attachments on the migrated Test Execution are present, correctly named, and open without corruption, matching the source environment.|High|
```

### 13. Integrations

```text
INT-001|Verify configured development tool integration panel is visible on issues|Verify that the configured development tool integration panel (e.g. source control/build/deployment information) is visible and functional on migrated issues, as included in the migration scope.|A known migrated issue with development tool integration data is available|1. Open the migrated issue and locate the Development panel/section.
2. Review the summary counts shown (e.g. commits, branches, pull/merge requests, builds, deployments) as applicable to the configured development tool integration within the migration scope.|Compare the development panel summary information against the source environment where comparable data is available.|The development tool integration panel is visible on the migrated issue and reflects information consistent with the configured integration in scope.
No integration panel errors are displayed.|Medium|

INT-002|Verify commit/pull-request links open correctly from Jira issues|Verify that commit links and pull/merge request links surfaced on migrated issues via the development tool integration open the correct destination.|A known migrated issue with at least one commit or pull/merge request link is available|1. Open the migrated issue's Development panel.
2. Select a listed commit or pull/merge request link.
3. Confirm the destination page loads correctly.|Verify the link opens the correct commit/PR record in the configured development tool integration within the migration scope.|Commit and pull/merge request links open the correct destination without errors.
No link results in a broken or unauthorized-access page.|Medium|

INT-003|Verify build and deployment information displays correctly|Verify that build and deployment information surfaced via the configured development tool integration displays correctly on migrated issues.|A known migrated issue with associated build/deployment information is available|1. Open the migrated issue's Development panel.
2. Review the Builds and Deployments sections (if present).
3. Confirm build/deployment status indicators render correctly.|Compare the build/deployment status and identifiers against the source environment where comparable data is available.|Build and deployment information displays correctly on the migrated issue, consistent with the configured integration in scope.|Low|
```

### 14. Security & Permissions

```text
SEC-001|Verify Administrator role access|Verify that a user assigned the Jira Administrator role retains full administrative access after migration.|A test account provisioned with the Jira Administrator role is available|1. Log in as the Administrator test account.
2. Navigate to Jira Settings > System/Global settings.
3. Confirm access to user management, scheme configuration, and app management.|Verify all expected administration areas are accessible without permission errors.|The Administrator account has full access to Jira Cloud administration areas consistent with its role in the source environment.|Critical|

SEC-002|Verify Project Administrator role access|Verify that a user assigned the Project Administrator role for SFDC Development or SFDC Operations can manage project-level configuration but not global settings.|A test account provisioned with the Project Administrator role for one of the in-scope projects is available|1. Log in as the Project Administrator test account.
2. Open Project settings for the assigned project and confirm access to configuration screens.
3. Attempt to access Jira Settings > System/Global settings.|Verify project-level configuration access is granted.
Verify global administration settings remain restricted (unless the user also holds global admin rights in the source environment).|The Project Administrator can manage project-level settings for their assigned project and is correctly restricted from unrelated global settings, consistent with the source environment.|High|

SEC-003|Verify Developer/Tester standard role access|Verify that a user assigned a Developer or Tester role can perform expected day-to-day actions (create/edit/transition issues, execute Tests) within their authorized project(s).|A test account provisioned with a Developer or Tester role in SFDC Development or SFDC Operations is available|1. Log in as the Developer/Tester test account.
2. Create, edit, and transition an issue in the authorized project.
3. Open and execute a Test issue in Xray (for Tester role).|Verify all expected day-to-day actions succeed without unexpected permission errors.
Verify the user cannot perform actions restricted to higher-privileged roles (e.g. project configuration changes).|The Developer/Tester account can perform expected standard actions and is correctly restricted from administrative actions, consistent with the source environment.|High|

SEC-004|Verify Viewer/read-only user access restrictions|Verify that a user assigned a Viewer/read-only role can view but not modify issues or configuration.|A test account provisioned with a Viewer/read-only role is available|1. Log in as the Viewer test account.
2. Open an issue and confirm it can be viewed.
3. Attempt to edit, transition, or delete the issue.|Verify view access succeeds.
Verify edit/transition/delete actions are blocked or the corresponding controls are not available.|The Viewer account can view issue content but is correctly prevented from editing, transitioning, or deleting issues, consistent with the source environment.|High|

SEC-005|Verify restricted/issue-security-level user access is enforced|Verify that a user without the required role/permission for an issue-level security scheme cannot view issues protected by that security level.|A test account known to be excluded from a specific Issue Security Level, and an issue using that security level, are available|1. Log in as the restricted test account.
2. Attempt to open the issue protected by the issue security level (via direct URL/issue key search).
3. Attempt to locate the issue via search/JQL.|Verify the restricted account receives an appropriate access-denied response and cannot view the issue's content.
Verify the issue does not appear in the restricted account's search results.|The restricted user cannot view or find the issue protected by the issue security level, consistent with the source environment's security configuration.|Critical|
```

### 15. Confluence Space

```text
CONF-001|Verify SFSUPPORTDE space exists with correct key and name|Verify that the SFSUPPORTDE Confluence space is available in Cloud with the correct space key and space name.|Test Environment migration is completed; tester has valid Confluence Cloud access|1. Log in to Confluence Cloud.
2. Navigate to Spaces > View all spaces.
3. Locate and open the SFSUPPORTDE space.|Compare the space key and space name against the source environment.|The SFSUPPORTDE space is present with the expected space key and name, and opens successfully.|Critical|

CONF-002|Verify authorized users can access the SFSUPPORTDE space|Verify that users authorized to access SFSUPPORTDE in the source environment retain that access after migration.|A test account known to have had access to SFSUPPORTDE is available|1. Log in as the authorized test account.
2. Navigate to the SFSUPPORTDE space and open a representative page.|Verify the space and page open without an authorization error.
Compare the access level against the source environment (<SOURCE_USER> access level).|The authorized user can access the SFSUPPORTDE space and its content without permission errors, consistent with the source environment.|Critical|

CONF-003|Verify unauthorized users cannot access restricted SFSUPPORTDE content|Verify that users who were not authorized to access SFSUPPORTDE (or specific restricted pages within it) in the source environment remain restricted after migration.|A test account known to lack access to SFSUPPORTDE (or a specific restricted page) is available|1. Log in as the unauthorized test account.
2. Attempt to navigate to the SFSUPPORTDE space or the specific restricted page.|Verify access is denied or the space/page is not visible, consistent with the source environment's permission configuration.|The unauthorized user is correctly prevented from accessing the SFSUPPORTDE space/restricted page, consistent with the source environment.|Critical|
```

### 16. Confluence Pages

```text
CONF-004|Verify page hierarchy for top-level and nested pages|Verify that the parent/child page hierarchy within SFSUPPORTDE is preserved after migration.|A known page hierarchy structure (parent page and nested child pages, <SOURCE_PAGE_NAME>) is available|1. Open the SFSUPPORTDE space page tree.
2. Locate the known parent page <SOURCE_PAGE_NAME> and expand its child pages.
3. Compare the resulting tree structure against the source environment.|Verify each child page appears under the correct parent, matching the source hierarchy.
Verify no page is missing or nested incorrectly.|The page hierarchy in Cloud matches the source environment exactly, with all parent/child relationships preserved.|High|

CONF-005|Verify page content, formatting, and tables render correctly|Verify that a representative page's text content, formatting, and embedded tables render correctly after migration.|A known source page (<SOURCE_PAGE_NAME>) containing formatted text and at least one table is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Review text formatting (headings, bold/italic, lists, code blocks).
3. Review any embedded tables for correct structure and data.|Compare formatting and table structure/content against the source page.|The page's content, formatting, and tables render correctly and match the source page's structure and data.|High|

CONF-006|Verify pages containing images and macros render correctly|Verify that pages containing embedded images and Confluence macros display correctly after migration.|A known source page (<SOURCE_PAGE_NAME>) containing images and macros (e.g. Table of Contents, Status, Info panel) is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Review each embedded image for correct rendering.
3. Review each macro for correct rendering and functional behavior (e.g. Table of Contents links, Status lozenge color).|Compare image rendering and macro output against the source page.|Images and macros on the migrated page render correctly and function consistent with the source page.|High|

CONF-007|Verify page labels and page restrictions are preserved|Verify that labels applied to a page and any page-level view/edit restrictions are preserved after migration.|A known source page (<SOURCE_PAGE_NAME>) with labels and a restriction is available|1. Open the page <SOURCE_PAGE_NAME> and review its labels.
2. Review the page's restriction settings (Restrictions > view/edit).|Compare the label list against the source page.
Compare the restriction configuration (restricted users/groups) against the source page.|Page labels and restrictions on the migrated page match the source page exactly.|Medium|

CONF-008|Verify page version/history is available where supported|Verify that page version history is retained (where supported by the migration approach) for a representative page.|A known source page (<SOURCE_PAGE_NAME>) with multiple historical versions is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Open Page History and review the list of versions.
3. Open an older version and compare its content to the expected historical content.|Compare the number of versions and their authorship/timestamps against the source page (where version history migration is supported).|Page version history is available and consistent with the source environment, or is documented as a known migration exception if not supported by the migration approach.|Low|
```

### 17. Confluence Attachments

```text
CONF-009|Verify Confluence attachments exist with preserved names|Verify that attachments on a representative page are present after migration with filenames preserved.|A known source page (<SOURCE_PAGE_NAME>) with attachments (<SOURCE_ATTACHMENT_NAME> list) is available|1. Open the page <SOURCE_PAGE_NAME> and open the Attachments list.
2. Compare the attachment count and filenames against the source page.|Verify each attachment filename matches the source exactly.|All attachments from the source page are present in Cloud with matching filenames and count.|High|

CONF-010|Verify Confluence attachments open and download without corruption|Verify that attachments can be opened/downloaded from the migrated page and that file contents are not corrupted.|A known source page attachment (<SOURCE_ATTACHMENT_NAME>) is available|1. Open the attachment from the page.
2. Download the file and open it locally.
3. Compare file size/content against the source file.|Verify the file opens without corruption and matches the expected source file.|The attachment opens and downloads successfully with content matching the source file, with no corruption.|High|

CONF-011|Verify embedded documents open correctly|Verify that documents embedded/displayed inline on a page (e.g. via the Office/PDF preview macro) open and render correctly.|A known source page containing an embedded document is available|1. Open the page containing the embedded document.
2. View the inline preview (if supported).
3. Open the document in full view/download it.|Verify the embedded document renders/opens correctly and its content matches the source document.|The embedded document opens correctly with content matching the source, with no corruption.|Medium|

CONF-012|Verify embedded images render correctly|Verify that images embedded directly within page content (not as standalone attachments) render correctly after migration.|A known source page with inline embedded images is available|1. Open the page and review each inline embedded image.
2. Confirm image resolution, placement, and captions (if used) are preserved.|Compare embedded image rendering against the source page.|Embedded images render correctly, in the correct placement and resolution, consistent with the source page.|Medium|
```

### 18. Confluence Links

```text
LINK-006|Verify Confluence page links to Jira issues resolve correctly|Verify that links from a Confluence page to Jira issues (including Jira issue macros) resolve to the correct migrated Cloud issue.|A known source page (<SOURCE_PAGE_NAME>) containing a Jira issue link/macro referencing <SOURCE_ISSUE_KEY> is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Locate the Jira issue link or Jira issue macro.
3. Click through to the referenced issue.|Verify the link/macro renders the correct issue key, summary, and status.
Verify clicking navigates to the correct migrated Jira Cloud issue, not a broken/legacy URL.|The Jira issue link/macro on the Confluence page correctly displays and navigates to the corresponding migrated Jira Cloud issue.|High|

LINK-007|Verify internal Confluence links (parent/child and cross-page) resolve correctly|Verify that internal links between SFSUPPORTDE pages, including parent/child navigation links, resolve correctly after migration.|A known source page (<SOURCE_PAGE_NAME>) containing links to other SFSUPPORTDE pages is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Click each internal link to another SFSUPPORTDE page.
3. Use the page tree/breadcrumbs to navigate to the parent page.|Verify each internal link opens the correct destination page.
Verify parent/child breadcrumb navigation is accurate.|All internal Confluence links and parent/child navigation correctly resolve to the expected migrated pages.|Medium|

LINK-008|Verify SharePoint links behavior after migration|Verify links from Confluence pages to SharePoint locations, distinguishing genuine migration defects from expected/legacy-only link exceptions.|A known source page (<SOURCE_PAGE_NAME>) containing a SharePoint link is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Click the SharePoint link.
3. If the link fails, confirm whether the failure is due to the migration or an intentionally deprecated/expected exception.|Verify the link opens the expected SharePoint destination.
If the destination is intentionally no longer valid, confirm it is documented as an expected migration exception rather than a defect.|The SharePoint link resolves correctly, or, if it does not, is documented as an expected migration exception rather than logged as an unexplained defect.|Medium|

LINK-009|Verify external website/document links resolve correctly|Verify that links from Confluence pages to external websites or external documents remain functional after migration.|A known source page (<SOURCE_PAGE_NAME>) containing an external link is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Click each external link.
3. Confirm the destination loads as expected.|Verify the external destination loads correctly and is unaffected by the migration.|External website/document links continue to resolve correctly after migration, with no unexpected breakage introduced by the migration.|Low|
```

### 19. Confluence Search

```text
SEARCH-005|Verify Confluence page and keyword search returns migrated content|Verify that Confluence search returns expected migrated pages when searching by page title and by keyword content.|A known source page name (<SOURCE_PAGE_NAME>) and a known keyword from its content are available|1. Use Confluence Cloud search to search for the exact page title <SOURCE_PAGE_NAME>.
2. Use Confluence Cloud search to search for a known keyword from the page's content.|Verify the title search returns the expected page as a top result.
Verify the keyword search returns the expected page in the results.|Both title-based and keyword-based searches return the expected migrated page.|High|

SEARCH-006|Verify Confluence search by label|Verify that pages can be found via label-based search where labels are used in the source environment.|A known label applied to one or more source pages is available|1. Use Confluence search filters (or the label browser) to search by the known label.
2. Review the returned list of pages.|Compare the returned page list against the expected set of labeled pages from the source environment.|Label-based search returns the complete, correct set of pages consistent with the source environment.|Medium|

SEARCH-007|Verify Confluence attachment search where supported|Verify that attachments can be located via Confluence search (where attachment search is supported) using a known attachment filename.|A known attachment filename (<SOURCE_ATTACHMENT_NAME>) is available|1. Use Confluence search to search for the attachment filename <SOURCE_ATTACHMENT_NAME>.|Verify the search returns the page containing the attachment (where this search capability is supported by the environment).|The attachment search returns the expected page containing the attachment, where this capability is supported.|Low|
```

### 20. Jira-Confluence Cross Validation

```text
LINK-010|Verify Jira issues linking to Confluence pages resolve correctly|Verify that Confluence page links added to Jira issues (e.g. in the description, comments, or the Confluence pages panel) resolve correctly.|A known migrated Jira issue (<SOURCE_ISSUE_KEY>) linked to a Confluence page (<SOURCE_PAGE_NAME>) is available|1. Open the Jira issue <SOURCE_ISSUE_KEY>.
2. Locate the Confluence page link (in description, comment, or the Confluence pages panel/remote link).
3. Click through to the Confluence page.|Verify the link opens the correct migrated Confluence Cloud page, not a broken/legacy URL.|The link from the Jira issue correctly opens the corresponding migrated Confluence Cloud page.|High|

LINK-011|Verify Confluence macros embedding Jira issues/filters function correctly|Verify that Confluence macros displaying live Jira data (single issue macro or Jira issues/filter macro) render correctly and reflect current Jira Cloud data.|A known source page (<SOURCE_PAGE_NAME>) containing a Jira issue or Jira filter macro is available|1. Open the page <SOURCE_PAGE_NAME>.
2. Review the Jira macro output (single issue details or filter result table).
3. Confirm the macro is correctly connected to the migrated Jira Cloud instance (not the old On-Premises instance).|Verify the macro output matches the current state of the referenced Jira Cloud issue(s)/filter.|The Jira macro renders correctly, is connected to the migrated Jira Cloud instance, and reflects accurate, current issue data.|High|

LINK-012|Verify navigation between Jira Cloud and Confluence Cloud|Verify general cross-application navigation between Jira Cloud and Confluence Cloud (e.g. via the app switcher and cross-links) functions correctly for a migrated user.|Tester has access to both migrated Jira Cloud and Confluence Cloud|1. Log in to Jira Cloud.
2. Use the app switcher (or a cross-link) to navigate to Confluence Cloud.
3. Navigate back to Jira Cloud using the app switcher.|Verify navigation between the two applications is seamless and does not require re-authentication (if SSO is configured).|The user can navigate between Jira Cloud and Confluence Cloud without errors or unexpected re-authentication prompts.|Medium|
```

### 21. Data Reconciliation

```text
DATA-006|Verify total Jira issue count reconciliation overall and by project|Verify that the total number of migrated Jira issues, overall and broken down by project, matches the source environment counts.|Source issue counts (<SOURCE_COUNT>) overall and per project are available from the Migration Team's pre-migration report|1. Run a JQL query for all issues in scope (both projects) and note the total count.
2. Run separate JQL queries for project = SFDC Development and project = SFDC Operations and note each count.|Compare the Cloud value <TARGET_COUNT> against the corresponding source value <SOURCE_COUNT> for the overall total and for each project.|The total migrated issue count and per-project counts match the corresponding source counts exactly, or any variance is documented and explained.|Critical|

DATA-007|Verify issue counts by issue type reconciliation|Verify that the count of migrated issues for each of the 13 in-scope issue types matches the source environment.|Source issue counts by issue type (<SOURCE_COUNT>) are available from the Migration Team's pre-migration report|1. Run a JQL query filtered by issuetype for each of the 13 in-scope issue types and note each count.|Compare each issue type's Cloud count <TARGET_COUNT> against the corresponding source count <SOURCE_COUNT>.|Issue counts for all 13 issue types match the source environment exactly, or any variance is documented and explained.|Critical|

DATA-008|Verify issue counts by status, priority, version, and component|Verify that migrated issue counts broken down by status, priority, version, and component match the source environment.|Source issue counts by status/priority/version/component (<SOURCE_COUNT>) are available|1. Run JQL queries filtered by each key status, priority, version, and component and note the counts.|Compare each Cloud count <TARGET_COUNT> against the corresponding source count <SOURCE_COUNT>.|Issue counts by status, priority, version, and component match the source environment exactly, or any variance is documented and explained.|High|

DATA-009|Verify Xray artifact count reconciliation|Verify that the counts of migrated Test, Test Set, Test Execution, and Test Plan issues match the source environment.|Source Xray artifact counts (<SOURCE_COUNT>) are available from the Migration Team's pre-migration report|1. Run JQL queries filtered by issuetype = Test, Test Set, Test Execution, and Test Plan and note each count.|Compare each Cloud count <TARGET_COUNT> against the corresponding source count <SOURCE_COUNT>.|Xray artifact counts (Tests, Test Sets, Test Executions, Test Plans) match the source environment exactly, or any variance is documented and explained.|Critical|

DATA-010|Verify Confluence page count reconciliation|Verify that the total number of migrated pages within SFSUPPORTDE matches the source environment's page count.|Source page count (<SOURCE_COUNT>) for SFSUPPORTDE is available from the Migration Team's pre-migration report|1. Open SFSUPPORTDE space details/analytics (or export the page tree) and note the total page count.|Compare the Cloud page count <TARGET_COUNT> against the source count <SOURCE_COUNT>.|The total migrated page count for SFSUPPORTDE matches the source environment exactly, or any variance is documented and explained.|Critical|

DATA-011|Verify attachment count reconciliation for Jira and Confluence|Verify that the total number of migrated attachments across the in-scope Jira projects and the SFSUPPORTDE space matches the source environment, where counts are available.|Source attachment counts (<SOURCE_COUNT>) for Jira and Confluence are available from the Migration Team's pre-migration report|1. Use available reporting/export capability to obtain the total attachment count for SFDC Development and SFDC Operations.
2. Use available reporting/export capability to obtain the total attachment count for SFSUPPORTDE.|Compare each Cloud attachment count <TARGET_COUNT> against the corresponding source count <SOURCE_COUNT>.|Attachment counts for Jira and Confluence match the source environment exactly, or any variance is documented and explained.|High|
```

### 22. Migration Exceptions

```text
EXC-001|Identify missing or duplicate Jira issues|Verify that no issues are missing and no issues were duplicated during migration by comparing sample sets and reconciliation counts.|Reconciliation counts from DATA-006/DATA-007 and a sample list of source issue keys are available|1. Cross-check the reconciliation counts from DATA-006 and DATA-007 for discrepancies.
2. Spot-check a sample of source issue keys (<SOURCE_ISSUE_KEY>) to confirm each exists exactly once in Cloud.|Log any missing issue as a migration defect with the source issue key.
Log any duplicate issue as a migration defect with both Cloud issue keys involved.|No missing or duplicate issues are found; any discrepancy identified is logged as a migration defect with supporting evidence (issue keys, counts).|Critical|

EXC-002|Identify broken links and missing attachments|Verify whether any issue links, Confluence links, or attachments identified during testing were found broken or missing, and consolidate findings.|Results from LINK-001 to LINK-012 and ATT-001 to ATT-005 / CONF-009 to CONF-012 test executions are available|1. Review results from all link and attachment test cases executed so far.
2. Classify each failure as either a genuine migration defect or an expected/documented exception (e.g. intentionally deprecated On-Premises URL).|Log each unresolved broken link or missing attachment as a migration defect with reproduction details.|All broken links and missing attachments identified during testing are either resolved, or classified and logged as migration defects/expected exceptions.|High|

EXC-003|Identify incorrect user mapping or permission discrepancies|Verify whether any users were incorrectly mapped, omitted, or granted incorrect permissions during migration.|Results from ENV-004, SEC-001 to SEC-005, CONF-002, and CONF-003 test executions are available|1. Review results from environment, security, and Confluence permission test cases.
2. Cross-check a sample of <SOURCE_USER> to <CLOUD_USER> mappings against the Migration Team's user mapping document.|Log any user missing from Cloud, mapped to the wrong account, or granted incorrect permissions as a migration defect.|No unresolved user mapping or permission discrepancies remain; any issue found is logged as a migration defect with the affected user and expected vs. actual access.|Critical|

EXC-004|Identify missing history, incorrect custom-field values, or workflow/status mapping issues|Verify whether any issue history, comments, custom-field values, or workflow status mappings were found incorrect or missing during data integrity and configuration testing.|Results from DATA-001 to DATA-005 and CFG-001 to CFG-006 test executions are available|1. Review results from data integrity and configuration test cases.
2. Confirm each identified discrepancy has been reproduced and documented with the affected issue key/field.|Log each confirmed discrepancy (missing history, incorrect custom field value, incorrect workflow/status mapping) as a migration defect.|No unresolved history, custom-field, or workflow mapping discrepancies remain; any issue found is logged as a migration defect with reproduction evidence.|High|

EXC-005|Identify missing Xray data or Confluence page/hierarchy issues|Verify whether any Xray artifacts (Tests, Test Sets, Test Executions, Test Plans, Preconditions) or Confluence pages/hierarchy were found missing or incorrect.|Results from XRAY-001 to XRAY-009, DATA-009, CONF-001 to CONF-008, and DATA-010 test executions are available|1. Review results from Xray and Confluence test cases and reconciliation counts.
2. Confirm each identified discrepancy has been reproduced and documented.|Log each confirmed missing Xray artifact or Confluence page/hierarchy defect with supporting evidence (issue key/page name, expected vs. actual).|No unresolved missing Xray data or Confluence page/hierarchy issues remain; any issue found is logged as a migration defect with supporting evidence.|Critical|
```

### 23. Handover Readiness

```text
HAND-001|Verify critical Jira functions checklist for handover|Confirm that all Critical-priority Jira test cases in this suite (ENV, JIRA, DEV, OPS, issue types, CFG, DATA, LINK, SEARCH, BOARD) have been executed and passed prior to handover.|All Critical-priority Jira-related test cases in this suite have been executed|1. Compile the execution results for all Critical-priority test cases with prefixes ENV, JIRA, DEV, OPS, CFG, DATA, LINK, SEARCH, and BOARD.
2. Confirm each has a Pass result or a documented, accepted exception.|Verify no Critical-priority Jira test case has a Fail status without a documented resolution or accepted risk.|All Critical-priority Jira test cases are passed or have a documented, accepted exception, supporting readiness for handover.|Critical|

HAND-002|Verify critical Xray functions checklist for handover|Confirm that all Critical-priority Xray test cases (XRAY-001, XRAY-002, XRAY-005, XRAY-007, and related DATA-009) have been executed and passed prior to handover.|All Critical-priority Xray-related test cases in this suite have been executed|1. Compile the execution results for all Critical-priority test cases with prefix XRAY, plus DATA-009.
2. Confirm each has a Pass result or a documented, accepted exception.|Verify no Critical-priority Xray test case has a Fail status without a documented resolution or accepted risk.|All Critical-priority Xray test cases are passed or have a documented, accepted exception, confirming Xray is usable and traceable for handover.|Critical|

HAND-003|Verify critical Confluence functions checklist for handover|Confirm that all Critical-priority Confluence test cases (CONF-001 to CONF-003, DATA-010) have been executed and passed prior to handover.|All Critical-priority Confluence-related test cases in this suite have been executed|1. Compile the execution results for all Critical-priority test cases with prefix CONF, plus DATA-010.
2. Confirm each has a Pass result or a documented, accepted exception.|Verify no Critical-priority Confluence test case has a Fail status without a documented resolution or accepted risk.|All Critical-priority Confluence test cases are passed or have a documented, accepted exception, supporting readiness for handover.|Critical|

HAND-004|Verify user access and permissions sign-off checklist|Confirm that user access, group access, and permission validation across Jira and Confluence (ENV-003, ENV-004, SEC-001 to SEC-005, CONF-002, CONF-003, EXC-003) is complete and accepted.|All relevant environment, security, and permission test cases have been executed|1. Compile the execution results for ENV-003, ENV-004, SEC-001 to SEC-005, CONF-002, CONF-003, and EXC-003.
2. Confirm each has a Pass result or a documented, accepted exception.|Verify no unresolved permission or access discrepancy remains open.|User access and permission validation is complete, with all Critical/High findings resolved or formally accepted, supporting handover sign-off.|Critical|

HAND-005|Verify no unresolved Severity 1/Critical migration defects or data-loss issues remain|Confirm that the migration defect log contains no open Severity 1/Critical defects and no unresolved data-loss issues identified through EXC-001 to EXC-005.|The consolidated migration defect log and results of EXC-001 to EXC-005 are available|1. Review the migration defect log for any open Severity 1/Critical entries.
2. Cross-check against the findings from EXC-001 to EXC-005 for unresolved data-loss issues.|Verify all Severity 1/Critical defects are either resolved and re-verified, or explicitly accepted by the Application/Project Team with sign-off.|No open Severity 1/Critical migration defects or unresolved data-loss issues remain; any exceptions are explicitly accepted and documented.|Critical|

HAND-006|Verify Migration Team sign-off readiness and documented exceptions|Confirm that all known migration exceptions are documented, all required test evidence has been captured, and the Migration Team is ready to formally hand over the Test Environment.|All test cases in this suite have been executed and results/evidence recorded|1. Compile a summary of overall pass/fail results across all test categories in this suite.
2. Compile the list of documented/accepted migration exceptions.
3. Obtain formal Migration Team sign-off confirming handover readiness.|Verify the summary report is complete, all exceptions are documented with business/technical justification, and sign-off has been recorded.|A complete summary report and documented exception list are available, and the Migration Team has formally signed off on handover readiness to the Application/Project Team.|Critical|
```

---

## 8. Handover Acceptance Criteria

The migrated Test Environment is considered **ready for handover** from the Migration Team to the Application/Project Team when:

- [ ] All **Critical**-priority test cases across every category (Environment, Jira projects, issue types, configuration, data, links, Xray, security, Confluence, reconciliation) have a Pass result, or a documented and formally accepted exception.
- [ ] No open Severity 1/Critical migration defect remains unresolved (see HAND-005).
- [ ] No unresolved data-loss issue has been identified (see EXC-001 to EXC-005).
- [ ] Xray is confirmed installed, licensed, accessible, and its data/traceability intact (XRAY-001 to XRAY-009, DATA-009).
- [ ] SFSUPPORTDE space, page hierarchy, and Confluence-Jira cross-links are confirmed intact (CONF-001 to CONF-012, LINK-006 to LINK-012, DATA-010).
- [ ] Data reconciliation counts (DATA-006 to DATA-011) match the source environment, or variances are explained.
- [ ] All known migration exceptions are documented with business/technical justification (see Section 9).
- [ ] The Migration Team has formally signed off on handover readiness (HAND-006).

Once these criteria are met, the Migration Team hands over the Test Environment to the Application/Project Team for the 1-2 week validation window. The same Critical/High priority test cases must be re-executed against Production after Phase 2.

## 9. Migration Defect / Exception Guidance

- Log every Fail result as a migration defect referencing the TestID, the affected object (issue key/page name/user), the expected value, and the actual value.
- Before logging a Fail, confirm whether the discrepancy is a **genuine migration defect** or an **expected migration exception** (e.g. an On-Premises-only URL that is intentionally no longer valid, or unsupported legacy page version history). Document expected exceptions explicitly rather than logging them as open defects.
- Assign defect severity aligned to the test case Priority (Critical priority test failures should generally be raised as Severity 1/2 defects).
- Route all confirmed defects to the Migration Team for investigation and correction during the 1-2 week validation window (Phase 1) or immediately after Production migration (Phase 2).
- Maintain a single consolidated defect/exception log referenced by HAND-005 and HAND-006 for sign-off.

---

*This suite contains 120 distinct test cases. See the companion workbook `Jira_Confluence_Cloud_Migration_Smoke_Tests.xlsx` for the identical test cases with execution-tracking columns (Test Result, Actual Result, Defect ID, Executed By, Execution Date, Comments).*
