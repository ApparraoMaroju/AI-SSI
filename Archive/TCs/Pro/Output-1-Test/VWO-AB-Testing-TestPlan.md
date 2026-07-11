# Test Plan for A/B Testing Website – App.vwo.com

- **Author:** Apparao Maroju
- **Role:** Test Manager

---

# 1. Objective

This document outlines the test plan for the A/B Testing application available at app.vwo.com.

The objective is to ensure that all features and functionalities of the VWO login dashboard and core platform work as expected for the target audience. This includes digital marketers, product managers, UX designers, and developers. The plan aims to validate the security, intuitiveness, and efficiency of the login experience and the A/B testing functionalities.

---

# 2. Scope

The scope of this test plan includes:

### Features to be Tested
- **Authentication System:**
    - Email and password-based login
    - Session management
    - Multi-Factor Authentication (2FA)
    - Single Sign-On (SSO)
- **User Input Validation:**
    - Real-time validation
    - Email format verification
    - Password strength indicators
    - Error handling
- **Password Management:**
    - Forgot password flow
    - Password recovery
    - Password complexity requirements
- **User Experience Features:**
    - Responsive design for mobile devices
    - Auto-focus on input fields
    - Clickable labels
    - Loading state indicators
- **Accessibility Features:**
    - Screen reader support (ARIA labels)
    - High contrast mode
    - Keyboard navigation
- **Branding and Visual Design:**
    - Brand consistency
    - Light and Dark Mode support
- **Experiment Creation and Management:**
    - A/B tests
    - Traffic allocation
    - Variation creation
    - Campaign activation
- **Reporting and Analytics**
- **User Management**
- **Settings and Configuration**

### Types of Testing
- Manual Testing
- Automated Testing
- Performance Testing
- Security Testing
- Accessibility Testing
- Usability Testing

### Environments
- Different browsers (Chrome, Firefox, Edge, Safari)
- Operating systems (Windows, macOS, Linux)
- Device types (Desktop, Laptop, Tablet, Smartphone)

### Evaluation Criteria
- Number of defects found and their severity
- Test case execution coverage
- Time taken to complete testing cycles
- User satisfaction ratings and feedback
- Performance metrics (e.g., page load time)

### Team Roles and Responsibilities
- **Test Lead:** Overall responsibility for the testing process.
- **Test Engineers:** Test case creation, execution, and defect reporting.
- **Developers:** Defect resolution and unit testing.
- **Product Managers:** Requirement clarification and feature validation.
- **Stakeholders:** Approvals and final sign-off.

---

# 3. Inclusions

## Introduction
This test plan provides a comprehensive overview of the testing activities for the VWO A/B testing platform, covering the purpose, scope, and goals of the testing effort.

## Test Objectives
- Identify and report defects in the application.
- Ensure the stability, reliability, and accuracy of A/B testing features.
- Improve the overall user experience and usability.
- Validate that the experiment execution and data collection are accurate.
- Ensure the system meets security, performance, and accessibility requirements.

---

# 4. Exclusions

The following items are **out of scope** for this test plan:

- Third-party integrations not explicitly mentioned in the requirements.
- Infrastructure-level testing (e.g., server hardware).
- Production deployment verification (to be handled by a separate plan).
- Testing on non-supported browsers or legacy environments.
- Company-specific SSO configurations beyond standard SAML/OAuth support.

---

# 5. Test Environments

### Operating Systems
- Windows 10 / Windows 11
- macOS (latest version)
- Linux (Ubuntu latest LTS)

### Browsers
- Google Chrome (latest version)
- Mozilla Firefox (latest version)
- Microsoft Edge (latest version)
- Safari (latest version)

### Devices
- Desktop Computers (various resolutions)
- Laptops
- Tablets (iOS and Android)
- Smartphones (iOS and Android)

### Network Connectivity
- Wi-Fi (high and low speed)
- Cellular Networks (4G, 5G)
- Wired Connections

### Hardware / Software Requirements
- Standard office hardware configurations.
- No special software required other than the supported browsers.

### Security Protocols
- HTTPS enforcement (SSL/TLS)
- Secure password authentication
- Secure access tokens for sessions

### Access Permissions
Defined roles for:
- Testers (access to test environment and bug tracking tool)
- Developers (access to code repository and development environment)
- Product stakeholders (read-only access to test reports and dashboards)
- Administrators (full access for configuration and user management)

---

# 6. Defect Reporting Procedure

### Criteria for Identifying Defects
- Any deviation from the product requirements document.
- User experience issues that make the application difficult to use.
- Technical errors, including console errors and network failures.
- Incorrect behavior in A/B testing experiments.
- Performance issues, such as slow page loads.

### Steps for Reporting Defects
1. Use the designated defect template in JIRA.
2. Provide a clear and concise title for the defect.
3. Include detailed steps to reproduce the issue.
4. Attach screenshots, videos, or logs as evidence.
5. Assign an initial severity and priority.

### Triage and Prioritization
- **Severity Levels:** Blocker, Critical, Major, Minor, Trivial.
- **Priority Levels:** High, Medium, Low.
- A daily triage meeting will be held with the Test Lead, a developer representative, and the Product Manager to prioritize defects.

### Tracking Tools
- **JIRA:** For defect tracking and project management.

### Roles and Responsibilities
- **Testers:** Log defects with all required information.
- **Developers:** Analyze and fix the defects.
- **Test Lead:** Review, prioritize, and track the defects to closure.

### Communication Channels
- Daily stand-up meetings.
- Slack channel for real-time communication.
- Email updates for major milestones and reports.
- JIRA dashboards for defect status.

### Metrics
- Number of defects identified per feature/module.
- Defect resolution time.
- Percentage of defects fixed and verified.
- Defect density.

---

# 7. Test Strategy

## Step 1: Test Scenario and Test Case Creation

### Techniques Used
- **Equivalence Class Partitioning:** For input fields like email and password.
- **Boundary Value Analysis:** For fields with numerical inputs (e.g., traffic allocation).
- **Decision Table Testing:** For complex business rules and conditions.
- **State Transition Testing:** For user session states (e.g., logged in, logged out).
- **Use Case Testing:** To simulate real user scenarios and workflows.

### Additional Methods
- **Error Guessing:** Based on experience to find common bugs.
- **Exploratory Testing:** To discover defects not covered by formal test cases.

---

## Step 2: Testing Procedure

### Smoke Testing
A set of basic tests will be executed on each new build to verify critical functionalities are working. If the smoke test fails, the build will be rejected.

### In-depth Testing
Once a build passes smoke testing, detailed functional and non-functional test cases will be executed.

### Multiple Environments
Testing will be conducted in parallel on different browsers and devices to ensure cross-platform compatibility.

### Defect Reporting
- All defects will be logged in JIRA.
- A daily testing status report will be sent to all stakeholders.

### Types of Testing
- **Smoke Testing:** To ensure build stability.
- **Sanity Testing:** To check major functionalities after minor changes.
- **Regression Testing:** To ensure new changes have not broken existing functionality.
- **Retesting:** To verify that fixed defects are resolved.
- **Usability Testing:** To evaluate the user-friendliness of the application.
- **Functionality Testing:** To verify all features work as per requirements.
- **UI Testing:** To check for visual and layout issues.

---

## Step 3: Best Practices

### Context-Driven Testing
The testing approach will be adapted based on the context of the application and the specific feature under test.

### Shift Left Testing
Involve testers early in the development cycle to review requirements and provide feedback.

### Exploratory Testing
Allocate dedicated time for exploratory testing to leverage the creativity and experience of the testers.

### End-to-End Flow Testing
Simulate complete user journeys, from login to creating and running an experiment, to viewing the results.

---

# 8. Test Schedule

### Tasks and Time Duration (Example)
- **Test Plan Creation:** 2 days
- **Test Case Creation:** 5 days
- **Test Execution Cycle 1:** 10 days
- **Regression Testing:** 3 days
- **Test Summary Report Submission:** 1 day

### Timeline
A detailed timeline with specific dates and milestones will be created and tracked in the project management tool.

---

# 9. Test Deliverables

- Test Plan Document (this document)
- Test Scenarios and Test Cases
- Test Execution Reports
- Defect Reports from JIRA
- Test Summary Report

---

# 10. Entry and Exit Criteria

## Requirement Analysis
**Entry Criteria**
- Product Requirements Document (PRD) is available and reviewed.

**Exit Criteria**
- All requirements are understood, and any ambiguities are clarified with the Product Manager.

---

## Test Execution

**Entry Criteria**
- Test plan and test cases are reviewed and signed off.
- The application build is deployed to the test environment and has passed smoke tests.

**Exit Criteria**
- All planned test cases are executed.
- All major and critical defects are either fixed and verified, or a deferral is agreed upon.
- Test execution and defect reports are generated.

---

## Test Closure

**Entry Criteria**
- Test execution is completed.
- All defect reports are available and their final status is updated.

**Exit Criteria**
- A final test summary report is prepared and shared with stakeholders.
- Final approval is obtained from the stakeholders for release.

---

# 11. Tools

### Tools Used
- **JIRA:** Bug Tracking and Project Management
- **Confluence:** Documentation
- **BrowserStack/Sauce Labs:** For cross-browser and cross-device testing
- **JMeter/LoadRunner:** For performance testing
- **Axe/WAVE:** For accessibility testing
- **Snipping Tool/Snagit:** For screenshot capture
- **Microsoft Office Suite (Word, Excel):** For documentation and reporting

---

# 12. Risks and Mitigations

### Possible Risks
- **Non-availability of resources:** Key personnel being unavailable.
- **Build URL not working or unstable build:** Delays due to unstable environment.
- **Limited time for testing:** Tight deadlines affecting test coverage.
- **Changes in requirements:** Late changes impacting the test plan and schedule.

### Mitigation Strategies
- **Backup resource planning:** Have backup resources identified.
- **Work on parallel tasks:** Testers can work on other tasks like test case writing if blocked.
- **Prioritize testing:** Focus on critical functionalities if time is limited.
- **Impact analysis:** Conduct a thorough impact analysis for any requirement changes.

---

# 13. Approvals
Documents requiring **client or stakeholder approval**:
- Test Plan
- Test Scenarios and Test Cases
- Test Summary Report

**Approved By:**________________________
**Date:**________________________
