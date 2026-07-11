# Test Strategy
## SCS Core – Sopra Crypto Solutions

| **Document Information** | |
|--------------------------|---|
| **Project Name:** | SCS Core (Sopra Crypto Solutions) |
| **Document Type:** | Test Strategy |
| **Version:** | 0.1 |
| **Status:** | Draft |
| **Author:** | Test Team |
| **Date:** | June 1, 2026 |

---

## Document Control

### Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 0.1 | June 1, 2026 | Test Team | Initial Draft |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Product Owner | | | |
| Business Representative | | | |

### Distribution List

| Name | Role | Organization |
|------|------|--------------|
| | Test Lead | Sopra Steria |
| | Product Owner | Bank |
| | Development Lead | Sopra Steria |
| | Security Lead | Sopra Steria |

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Intended Audience](#2-intended-audience)
3. [Project Overview](#3-project-overview)
4. [Project Scope](#4-project-scope)
5. [Testing Approach](#5-testing-approach)
6. [Test Deliverables](#6-test-deliverables)
7. [Entry and Exit Criteria](#7-entry-and-exit-criteria)
8. [Defect Management](#8-defect-management)
9. [Roles and Responsibilities](#9-roles-and-responsibilities)
10. [Test Environment](#10-test-environment)
11. [Test Data](#11-test-data)
12. [Test Tools](#12-test-tools)
13. [Test Suspension and Resumption](#13-test-suspension-and-resumption)
14. [Risk Management](#14-risk-management)
15. [Reporting and Communication](#15-reporting-and-communication)
16. [Appendices](#16-appendices)

---

## 1. Purpose

This document is the Test Strategy for the SCS Core (Sopra Crypto Solutions) project. It contains the testing requirements and the high-level approach of testing planned for the project. The test strategy helps to ensure that testing is carried out systematically based on the agreed testing approach.

The purpose of this Test Strategy document is to:
- Define overall testing approach that will be taken by the SCS testing team, referenced as Quality Assurance teams (QA)
- Document and achieve agreement to the high-level testing approach to be followed for the testing of SCS Core
- Clarify the testing activities, roles and responsibilities, Defect Management, Risk Management, Stakeholder Management, and Reporting mechanism

This document is meant to outline the testing standards and best practices for the cryptocurrency/digital asset banking platform while ensuring compliance with banking regulations (KYT, AML, Travel Rule).

---

## 2. Intended Audience

This document will be circulated for use by various stakeholders who are as follows:

| Role | Description |
|------|-------------|
| **Test Manager / Test Lead** | Manage testing activities, ensure compliance with test strategy and processes |
| **Test Engineers / QA Team** | Execute test cases and test governance according to processes |
| **Business Analysts** | Provide requirements, validate test scenarios, review test cases |
| **Developers** | Support testing, fix defects, provide technical guidance |
| **Product Owner** | Review and approve testing approach, accept deliverables |
| **Project Manager** | Oversee project delivery, manage risks and escalations |
| **Bank Representatives** | Business users to execute and validate the implemented processes (UAT) |
| **Security Team** | Security testing oversight, compliance validation |
| **Compliance Team** | KYT/AML/Travel Rule validation |

---

## 3. Project Overview

### 3.1 Business Description

SCS Core (Sopra Crypto Solutions) is a banking solution developed by Sopra Steria that enables banks to deploy a crypto-account offering for their customers. It provides end-to-end management of digital asset accounts, orders (buy/sell), transactions (deposits/withdrawals), and integration with custodians, order management systems, and exchange venues.

### 3.2 User Stories

- As a bank customer, I want to create a crypto-account so that I can hold and manage digital assets
- As a bank customer, I want to buy digital assets so that I can invest in cryptocurrencies
- As a bank customer, I want to sell digital assets so that I can convert them to fiat currency
- As a bank customer, I want to deposit digital assets so that I can transfer them to my account
- As a bank customer, I want to withdraw digital assets so that I can transfer them to external addresses
- As a bank user, I want to manage customer accounts so that I can provide support and oversight
- As a bank user, I want to view dashboards so that I can monitor bank positions and operations

### 3.3 Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Web UI (customer and bank user interfaces) |
| Backend | AWS EKS (Kubernetes microservices architecture) |
| Database | AWS DocumentDB, S3, EFS |
| API Type | REST API |
| Cloud Infrastructure | AWS (EKS, Cognito, API Gateway, WAF, GuardDuty, Secrets Manager, CloudWatch) |
| Container Orchestration | Kubernetes with Cluster Autoscaler and Horizontal Pod Autoscaler (HPA) |
| Authentication | AWS Cognito with OAuth2, MFA, enterprise SSO integration |
| Encryption | TLS 1.3 for data in transit, AWS KMS for data at rest |

### 3.4 External Integrations

| System | Provider | Purpose |
|--------|----------|---------|
| Custodians | Fireblocks, Taurus | Blockchain interactions, wallet management, security |
| Order Management System | Wyden | Order routing and execution |
| Exchange Venues | Kraken, Coinbase | Order execution |
| KYT/AML Provider | Chainalysis | Transaction screening, compliance |
| Core Banking System | Bank CBS | Account information, fiat operations |

### 3.5 Architecture Reference

The following diagrams are available for testing reference:

| Figure | Description |
|--------|-------------|
| Figure 1 | Overview of the Solution |
| Figure 2 | Capability Map |
| Figure 3 | Subledger Concepts |
| Figure 4 | Application Architecture |
| Figure 5 | Deployment |
| Figure 36 | Architecture Principles |
| Figure 37 | Technology Stack |
| Figure 38 | Current Infrastructure |
| Figure 39 | Target Infrastructure |
| Figure 40 | Cluster Autoscaler |
| Figure 41 | Horizontal Pod Autoscaler |

---

## 4. Project Scope

### 4.1 In Scope

The following items are in scope for SCS testing:

#### 4.1.1 Account Management
| Test Area | Process Flow Reference |
|-----------|------------------------|
| Customer request to open digital asset account | Figure 7 |
| Customer accesses digital asset dashboard | Figure 8 |
| Customer login | Figure 9 |
| One account per customer limit validation | Acceptance Criteria |

#### 4.1.2 Order Management
| Test Area | Process Flow Reference |
|-----------|------------------------|
| Initiation of buying order | Figure 10 |
| Execution of buying order | Figure 11 |
| Initiation of selling order | Figure 12 |
| Execution of selling order | Figure 13 |
| Customer request cancellation of order | Figure 22 |
| Order Integration Module | Figure 27 |
| Order status transitions | Figure 33 |

#### 4.1.3 Transaction Management
| Test Area | Process Flow Reference |
|-----------|------------------------|
| New deposit address request | Figure 14 |
| Deposit receipt | Figure 15 |
| Whitelisted address creation | Figure 16 |
| Customer initiates withdrawal | Figure 17 |
| Withdrawal execution | Figure 18 |
| Internal withdrawal execution | Figure 19 |
| Account-based withdrawal execution | Figure 20 |
| Batch execution for UTXO assets (BTC) | Figure 21 |
| Withdrawal status transitions | Figure 34 |
| Deposit status transitions | Figure 35 |

#### 4.1.4 Compliance & Monitoring
| Test Area | Process Flow Reference |
|-----------|------------------------|
| Continuous monitoring | Figure 23 |
| Travel Rule data management | Figure 24 |
| KYT Task Management | Figure 25 |
| Document upload for KYT issue | Figure 32 |

#### 4.1.5 Additional Features
| Test Area | Process Flow Reference |
|-----------|------------------------|
| Price management | Figure 26 |
| Limit update management | Figure 28 |
| Tax-related data computation | Figure 29 |
| Tax reports / Statement report generation | Figure 30 |
| Create bank position | Figure 31 |

#### 4.1.6 Security Testing
- TLS 1.3 enforcement validation
- JWT token validation (structure, claims, expiration, signature)
- SQL injection and XSS attack prevention (WAF rules)
- CORS policy enforcement
- Rate limiting effectiveness
- Unauthorized access attempts (cross-customer access)
- Role-Based Access Control (RBAC)
- Asset-link based access control

#### 4.1.7 API Testing
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /accounts | Create account opening request |
| GET | /accounts | Retrieve account details |
| POST | /orders | Create buy/sell order |
| GET | /orders | Retrieve orders |
| POST | /transactions | Create deposit/withdrawal transaction |
| GET | /transactions | Retrieve transactions |
| POST | /bank-user-access-controls | Verify bank user access to customer |

### 4.2 Out of Scope

Any item not mentioned in section 4.1 will be out of scope of the SCS testing, including:

- Core Banking System (CBS) implementation and internal testing
- Bank-specific authentication provider implementation
- Exchange venue internal logic and testing
- Custodian internal security mechanisms
- Production infrastructure deployment and verification
- Third-party systems not owned by Sopra Steria
- Non-supported browsers or legacy environments
- Mobile application testing (if any)

### 4.3 Assumptions

- Requirements are documented in the SCS Reference Document and context files
- Test environments will be available as per schedule with AWS infrastructure
- Test data will be prepared including JWT tokens with all required claims
- Custodian sandbox/test environments (Fireblocks, Taurus) will be available
- OMS test environment (Wyden) will be accessible
- Mock services for CBS API endpoints will be provided for testing
- Chainalysis test environment will be available for KYT testing
- Digital assets (BTC, ETH, SHIB) will be configured in test environment

### 4.4 Dependencies

| Dependency | Owner | Impact if Not Met |
|------------|-------|-------------------|
| AWS Environment (EKS, Cognito, API Gateway) | DevOps Team | Testing cannot proceed |
| Custodian Test Environment (Fireblocks/Taurus) | External Vendor | Integration testing blocked |
| OMS Test Environment (Wyden) | External Vendor | Order execution testing blocked |
| Chainalysis Test Environment | External Vendor | KYT/AML testing blocked |
| DocumentDB with seed data | DevOps Team | Test data unavailable |
| JWT Token generation capability | Security Team | Authentication testing blocked |
| CBS Mock Services | Development Team | CBS integration testing blocked |
| Digital Asset Configuration | DevOps Team | Order/Transaction testing blocked |

---

## 5. Testing Approach

### 5.1 Testing Methodology

SCS project is being run in **Agile SCRUM methodology**. The project is divided into sprints of 2-3 weeks each. Below testing framework is being followed:

#### Sprint Testing Process
1. **Scope Freeze** – Pre-condition phase to have better quality
2. **Sprint Planning** – Sprint plans are created for completing product backlog items
3. **Test Case Creation + BA Review** – Detailed test cases are created and reviewed by Business Analyst
4. **Test Execution and Bug Fixing** – Execution is performed and corresponding fixing is done
5. **Sprint Retrospective** – Lessons learned are captured

#### Testing Phases
| Phase | Description | Entry Criteria | Exit Criteria |
|-------|-------------|----------------|---------------|
| Unit Testing | Developer testing | Code complete | All unit tests pass |
| API Testing | REST API validation | UT complete | All API contracts verified |
| Integration Testing | External service integration | API testing complete | All integrations verified |
| System Testing | End-to-end functional testing | SIT complete | All test cases executed |
| Security Testing | JWT, RBAC, encryption validation | ST in progress | Security requirements met |
| Performance Testing | Load and stress testing | Core functionality stable | Performance targets met |
| Compliance Testing | KYT, AML, Travel Rule validation | ST complete | Compliance requirements met |
| UAT | Bank user acceptance testing | All testing complete | Business sign-off |

### 5.2 Types of Testing

#### 5.2.1 Functional Testing

| Testing Type | Description | Coverage |
|--------------|-------------|----------|
| Smoke Testing | Verify critical functionalities after each build | Login, Account creation, Order placement |
| Sanity Testing | Quick validation after bug fixes | Affected functionality |
| Regression Testing | Ensure existing functionality is not impacted | Full regression suite |
| Integration Testing | Verify integrations with external systems | Custodians, OMS, CBS, Chainalysis |
| End-to-End Testing | Validate complete business workflows | All user stories |
| User Acceptance Testing | Bank validation of business requirements | All acceptance criteria |
| API Testing | REST API contract validation | All endpoints |
| State Transition Testing | Validate status flow transitions | Order, Withdrawal, Deposit statuses |

#### 5.2.2 Non-Functional Testing

| Testing Type | Description | Coverage |
|--------------|-------------|----------|
| Performance Testing | Validate API response times, concurrent users | All critical APIs |
| Security Testing | JWT, TLS, injection prevention | All security requirements |
| Accessibility Testing | WCAG compliance | Customer and Bank User UI |
| Usability Testing | User experience evaluation | Key user journeys |
| Compatibility Testing | Cross-browser testing | Chrome, Firefox, Safari, Edge |
| Compliance Testing | KYT/AML/Travel Rule validation | All compliance workflows |

### 5.3 Test Design Techniques

| Technique | Application |
|-----------|-------------|
| Equivalence Class Partitioning | Valid/invalid JWT tokens, digital assets, amounts |
| Boundary Value Analysis | Trade limits (min, max), withdrawal limits, precision |
| Decision Table Testing | Role-based access combinations, order status transitions |
| State Transition Testing | Order statuses (Fig 33), Withdrawal (Fig 34), Deposit (Fig 35) |
| Use Case Testing | All user stories, end-to-end workflows |
| Error Guessing | Edge cases based on domain knowledge |
| Exploratory Testing | Unscripted testing for defect discovery |
| API Contract Testing | OpenAPI specification validation |

---

## 6. Test Deliverables

The following testing deliverables will be produced for both functional and non-functional testing:

| Deliverable | Description | Owner | Timeline |
|-------------|-------------|-------|----------|
| Test Strategy | High-level testing approach (this document) | Test Manager | Project Start |
| Test Plan | Detailed test planning document per sprint | Test Lead | Before Test Design |
| Test Scenarios | High-level scenarios for each process flow | Test Analyst | Test Design Phase |
| Test Cases/Scripts | Detailed test steps with expected results | Test Engineer | Test Design Phase |
| Test Data | JWT tokens, customer data, digital asset data | Test Analyst | Before Execution |
| API Test Collections | Postman/REST client collections for all endpoints | Test Engineer | Test Design Phase |
| Security Test Scripts | Security testing automation scripts | Security Tester | Test Design Phase |
| Performance Test Scripts | JMeter/Gatling scripts | Performance Tester | Test Design Phase |
| Defect Reports | Logged defects with full details | Test Engineer | During Execution |
| Test Execution Report | Daily/Weekly status reports | Test Lead | During Execution |
| Test Completion Report | Final testing summary with metrics | Test Manager | End of Testing |
| Compliance Test Report | KYT/AML/Travel Rule test results | Compliance Tester | End of Testing |

---

## 7. Entry and Exit Criteria

### 7.1 Entry Criteria

The entry criteria for both functional and non-functional test execution will be:

| Category | Criteria | Verification |
|----------|----------|--------------|
| Environment | AWS EKS environment stable and available | Health check |
| Environment | AWS Cognito configured for authentication | Login test |
| Environment | AWS API Gateway deployed and accessible | API health check |
| Environment | DocumentDB has seed data loaded | Data verification |
| Test Data | JWT tokens (valid, invalid, expired) prepared | Token generation test |
| Test Data | Customer and Bank User accounts created | Account verification |
| Test Data | Digital assets configured (BTC, ETH, SHIB) | Configuration check |
| Test Cases | Test cases reviewed and approved | Sign-off |
| Build | Build deployed and smoke tested | Smoke test pass |
| Defects | All Severity 1 or 2 defects from previous phase resolved | Defect report |
| Integrations | Custodian sandbox accessible | Integration test |
| Integrations | OMS test environment accessible | Integration test |
| Documentation | Requirements and design documents available | Document review |

### 7.2 Exit Criteria

| Category | Criteria | Target |
|----------|----------|--------|
| Execution | All planned test cases executed | 100% |
| Pass Rate | Test pass rate meets threshold | ≥95% |
| Critical Defects | No open Critical (S1) defects | 0 |
| High Defects | Open High (S2) defects | ≤2 (with workarounds) |
| Security | All security test cases passed | 100% |
| Integration | All integration test cases passed | 100% |
| Compliance | All KYT/AML/Travel Rule tests passed | 100% |
| Documentation | Test completion report prepared | Approved |
| Sign-off | Stakeholder sign-off obtained | Signed |

---

## 8. Defect Management

### 8.1 Defect Management Process

The standard Sopra Steria defect management process will be followed during the project. The Test Lead will perform the role of Defect Manager. The Defect Management process involves compiling and processing information on defects found during testing and analyzing that information so that trends and significant events can be recognized and acted upon.

The purpose of Defect Management is to implement the processes to manage the recording, tracking, progression and fixing of defects found during testing.

#### Defect Workflow
1. **Identification** – Defect identified during test execution
2. **Logging** – Defect logged in JIRA with all required details
3. **Triage** – Defect reviewed and prioritized in triage meeting
4. **Assignment** – Defect assigned to developer
5. **Resolution** – Developer fixes the defect
6. **Retest** – Tester verifies the fix
7. **Regression** – Verify no side effects
8. **Closure** – Defect closed upon successful verification

### 8.2 Defect Logging Standards

All defects must include:
- **Title:** Clear, concise description
- **Description:** Detailed steps to reproduce
- **Expected Result:** What should happen
- **Actual Result:** What actually happened
- **Environment:** Environment name, browser, API endpoint
- **Attachments:** Screenshots, API responses, logs
- **Severity:** As per definitions below
- **Priority:** As per definitions below
- **Linked User Story:** Reference to requirement
- **Component:** Affected module/service

### 8.3 Defect Triage

A defect triage meeting will be scheduled twice weekly to discuss the progress of defects, identify which defects should be fixed first and also to discuss if there are any blockers.

Participants: Test Lead, Dev Lead, BA, Product Owner

---

## 9. Roles and Responsibilities

The roles and responsibilities for the relevant stakeholders for testing are mentioned below:

| Role | Responsibilities |
|------|------------------|
| **Test Manager** | Provides project oversight to ensure compliance with Sopra Steria Testing Practices. Manages and ensures compliance with the Test Strategy, including the testing schedule. |
| **Test Lead** | Manages and ensures compliance with the Test Plan. Performs defect management and monitors defect resolution. Ensures that any testing related issues are resolved internally. Conducts close-down of testing activities for each release, ensuring that lessons learnt are captured. |
| **Test Analyst** | Agreement on testing scope, provide test estimates for releases, conduct testing activities. Develop and maintain high level test cases (scenarios) and test scripts including expected results. |
| **Test Engineer** | Execute test cases, report defects, collect test evidence. Support and execute all levels of testing by actively coordinating with other parties involved. |
| **Automation Engineer** | Identify the relevant automation framework to be used in project. Customize the framework as per project needs. Create and maintain automation scripts. |
| **Performance Tester** | Conduct feasibility study to decide on the tool for performance testing. Create performance testing scenarios/test cases as per user story requirements. Create test reports and conduct results analysis. |
| **Security Tester** | Security test design, JWT validation, penetration testing, WAF validation. |
| **Business Analyst** | Requirements clarification, test scenario review, expectation sheets. |
| **Developer** | Defect resolution, test support, technical guidance, unit testing. |
| **Product Owner** | Acceptance criteria, UAT execution, sign-off, priority decisions. |
| **DevOps Engineer** | Environment setup, deployment, infrastructure support. Ensures that test environment is made available to testing team as per sprint requirement. |

---

## 10. Test Environment

### 10.1 Environment Overview

| Environment | Purpose | Infrastructure | Integrations | Refresh Schedule |
|-------------|---------|----------------|--------------|------------------|
| DEV | Development testing | AWS EKS (Dev) | Mocks only | On-demand |
| TEST | System testing | AWS EKS (Test) | Custodian sandbox, OMS test | Weekly |
| STAGING | Pre-production/Integration | AWS EKS (Staging) | All external integrations | Per release |
| UAT | User acceptance testing | AWS EKS (UAT) | All external integrations | Per release |

### 10.2 AWS Infrastructure Requirements

| Component | Specification | Purpose |
|-----------|---------------|---------|
| AWS EKS | Kubernetes cluster | Application hosting |
| AWS Cognito | Identity provider | Authentication, JWT generation |
| AWS API Gateway | API management | Rate limiting, WAF integration |
| AWS WAF | Web application firewall | Security rules |
| AWS DocumentDB | NoSQL database | Data persistence |
| AWS S3 | Object storage | Document storage |
| AWS CloudWatch | Monitoring | Logging, metrics |
| AWS GuardDuty | Threat detection | Security monitoring |
| AWS Secrets Manager | Secrets management | API keys, credentials |
| AWS KMS | Key management | Encryption keys |

### 10.3 Browser/Client Requirements

| Browser | Version | Primary/Secondary |
|---------|---------|-------------------|
| Chrome | Latest | Primary |
| Firefox | Latest | Secondary |
| Safari | Latest | Secondary (Mac) |
| Edge | Latest | Secondary (Windows) |

### 10.4 External Integration Environments

| System | Environment | Connectivity | Purpose |
|--------|-------------|--------------|---------|
| Fireblocks | Sandbox | HTTPS/API | Custodian integration |
| Taurus | Sandbox | HTTPS/API | Custodian integration |
| Wyden | Test | HTTPS/API | OMS integration |
| Chainalysis | Test | HTTPS/API | KYT/AML screening |
| CBS Mock | Test | Internal | Core Banking simulation |

### 10.5 Environment Issues and Escalation

| Issue Type | First Response | Escalation | Timeline |
|------------|----------------|------------|----------|
| Environment down | Notify DevOps | Project Manager | 4 hours |
| External integration failure | Contact vendor | Project Manager | 8 hours |
| Data corruption | Restore from backup | DevOps Lead | 4 hours |
| Security incident | Security Team | CISO | Immediate |

---

## 11. Test Data

### 11.1 Test Data Strategy

Test data will be prepared by the Test Team in coordination with Development:
- Sensitive data will be anonymized as per GDPR requirements
- JWT tokens will be generated with all required claims
- Digital assets (BTC, ETH, SHIB) will be configured
- Test customer and bank user accounts will be pre-created

### 11.2 Test Data Requirements

#### Authentication Test Data

| Data Type | Value/Format | Purpose |
|-----------|--------------|---------|
| Valid JWT Token | Token with claims: sub, iat, exp, client, customer, role | Happy path authentication |
| Expired JWT Token | Token with past exp timestamp | Token expiration test |
| Invalid JWT Token | Malformed/corrupted token | Security test |
| Missing Claims JWT | Token without customer claim | Validation test |
| Invalid Signature JWT | Token with wrong signature | Security test |
| Customer Role Token | role = "CUSTOMER" | Customer access test |
| Bank User Role Token | role = "BANK_USER" | Bank user access test |

#### Business Test Data

| Data Type | Value/Format | Purpose |
|-----------|--------------|---------|
| Valid Customer ID | UUID format | Account operations |
| Valid Account ID | UUID format | Transaction/Order operations |
| Valid Idempotency-Key | UUID format | Idempotency test |
| Duplicate Idempotency-Key | Same UUID as previous request | Idempotency validation |
| Valid Digital Asset | BTC, ETH, SHIB | Order creation tests |
| Invalid Digital Asset | XYZ (unsupported) | Negative - validation test |
| Amount within limits | Based on configured limits | Happy path |
| Amount exceeding limits | Above configured limits | Limit validation |
| Amount with high precision | 0.00001 SHIB | Precision handling |
| simulationIndicator=true | Query parameter | Simulation mode test |
| simulationIndicator=false | Query parameter | Normal execution test |
| Valid whitelisted address | Blockchain address | Withdrawal test |
| Invalid blockchain address | Malformed address | Validation test |

### 11.3 Test Data Refresh

- Test data refresh frequency: Per Sprint
- Refresh process: DocumentDB restore from baseline snapshot
- JWT tokens regenerated as needed
- External system test data coordinated with vendors

---

## 12. Test Tools

### 12.1 Test Management Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| JIRA | User story management, defect tracking, sprint management | Daily |
| Confluence | Documentation repository, test evidence storage | Daily |
| Xray for JIRA | Test case management, test execution tracking, traceability | Daily |

### 12.2 Testing Tools

| Tool | Purpose | Test Type |
|------|---------|-----------|
| Postman | API testing, JWT validation, collection runner | API Testing |
| REST Assured | API automation | API Automation |
| Selenium / Cypress | UI automation | UI Automation |
| JMeter | Performance testing, load testing | Performance |
| Gatling | Performance testing, stress testing | Performance |
| OWASP ZAP | Security scanning, vulnerability detection | Security |
| Burp Suite | Security testing, request interception | Security |
| AWS CloudWatch | Log analysis, monitoring verification | Monitoring |
| Browser DevTools | Network analysis, JWT inspection, debugging | Debugging |

### 12.3 Environment Tools

| Tool | Purpose |
|------|---------|
| AWS Console | Environment monitoring, service management |
| kubectl | Kubernetes cluster management |
| Docker | Container management |
| Terraform | Infrastructure as code |

---

## 13. Test Suspension and Resumption

### 13.1 Suspension Criteria

Testing will be suspended if:
- Any eventuality which results in the Test environment becoming unstable or unusable
- Test execution will be suspended if there are issues in the deployment of the build
- Test execution will be suspended if more than 30% of test cases fail in smoke testing
- Critical defects block further testing progress
- External integration services unavailable for >4 hours
- Security vulnerabilities discovered requiring immediate attention
- Data breach or compliance violation detected

### 13.2 Resumption Criteria

When the issues triggering the suspension are rectified, testing will resume:
- The test environment would need to be rolled back to the previous acceptable state
- Issues causing suspension are resolved
- Sanity testing passes on fixed build (100% pass)
- External integrations are restored
- Security issues are remediated and verified
- Approval received from Test Lead/Manager
- Root cause documented and communicated
- Implementation of a patch may result in a requirement for a further "Smoke Test"
- A series of Sanity tests to be carried out before resuming test phase test execution

---

## 14. Risk Management

### 14.1 Risk Identification and Mitigation

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy | Owner |
|---------|------------------|-------------|--------|---------------------|-------|
| R001 | AWS environment unavailability | Medium | High | Backup environment, early escalation | DevOps Lead |
| R002 | Delayed requirement delivery | Medium | High | Buffer in schedule, parallel activities | Test Lead |
| R003 | Custodian sandbox unavailability (Fireblocks/Taurus) | Medium | High | Mock services, escalation to vendor | Project Manager |
| R004 | OMS integration issues (Wyden) | Medium | High | Early integration testing, mock services | Test Lead |
| R005 | Test data unavailability | Medium | High | Early data preparation, synthetic data | Test Analyst |
| R006 | Resource unavailability | Medium | Medium | Cross-training, backup resources | Test Manager |
| R007 | Scope changes | Medium | High | Change control process, impact analysis | Project Manager |
| R008 | Security vulnerabilities discovered | Low | Critical | Early security testing, rapid response | Security Lead |
| R009 | Performance issues in API | Medium | High | Early performance testing, optimization | Performance Tester |
| R010 | KYT/AML compliance failure | Low | Critical | Early compliance testing, Chainalysis support | Compliance Tester |
| R011 | JWT token generation issues | Low | High | Pre-generate tokens, Cognito support | Security Team |
| R012 | External vendor response delays | Medium | Medium | SLA agreements, escalation path | Project Manager |

### 14.2 Risk Monitoring

- All project related risks will be maintained in Risk Register
- Risks reviewed in weekly testing progress meetings
- Risk status updated weekly
- Escalation path: Test Lead → Test Manager → Project Manager → Steering Committee

---

## 15. Reporting and Communication

### 15.1 Communication Plan

| Communication | Frequency | Participants | Medium | Purpose |
|---------------|-----------|--------------|--------|---------|
| Daily Standup | Daily | Test Team, Dev Team | Teams/In-person | Status, blockers |
| Test Status Report | Weekly | All stakeholders | Email + Confluence | Progress, metrics |
| Defect Triage | Twice Weekly | Test Lead, Dev Lead, BA, PO | Meeting | Defect review |
| Sprint Review | End of Sprint | All stakeholders | Meeting | Demo, feedback |
| Risk Review | Weekly | Test Lead, PM | Meeting | Risk updates |
| Steering Committee | Bi-weekly | Leadership | Meeting | Escalations, decisions |

### 15.2 Reporting

#### Daily Reports
- Test execution progress (cases executed, passed, failed, blocked)
- Defects raised/closed/reopened
- Blockers and issues
- Environment status

#### Weekly Reports
- Test metrics summary
- Defect analysis (by severity, priority, component, trend)
- Risk and issues update
- Upcoming activities and milestones
- Resource utilization

#### Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| Test Execution Progress | % tests executed vs. planned | 100% |
| Test Pass Rate | % tests passed vs. executed | ≥95% |
| Defect Density | Defects per test case | ≤0.1 |
| Defect Resolution Time | Average time to fix defects | ≤2 days (P1/P2) |
| Test Coverage | % requirements covered | ≥100% |
| Automation Coverage | % regression tests automated | ≥70% |
| Defect Leakage | Defects found in UAT/Prod | 0 |
| Blocked Test Ratio | % tests blocked | ≤5% |

---

## 16. Appendices

### Appendix A – Defect Priority Definitions

Priority is about how important it is to the business to fix the problem. Priority is assigned to a defect to help designate the order in which defects should be fixed.

| Priority | Definition | Response Time | Fix Timeline |
|----------|------------|---------------|--------------|
| **P1 - Critical** | The system/release cannot "go live" with this defect outstanding as it would cause significant impact. Many test cases are blocked. | Immediate | Within 4 hours |
| **P2 - High** | Significant impact. Material impact on customer service, that could cause attrition. Breakdown in function causing client attrition in short term. | Within 4 hours | Within 24-48 hours |
| **P3 - Medium** | Only moderate or slight impact to plan. Single test case affected. Not necessarily enough to prevent "going live", but impacts non-core system functionality. | Within 24 hours | Within current release |
| **P4 - Low** | No significant impact on the customer. No impact on business processes. Minor or no impact to plan. Fix could be left until next release. | Within 48 hours | Future release |

### Appendix B – Defect Severity Definitions

Severity is a measure of the technical impact on the system if the defect was introduced.

| Severity | Definition | Examples |
|----------|------------|----------|
| **S1 - Critical** | Show-stopper. System unavailable / workaround unavailable / the function is inoperable. | System crash, unauthorized access, payment failure, data corruption |
| **S2 - High** | Unacceptable. Not a fatal problem, but severe enough to cause substantial loss of function or business. System is available, but the function is inoperable for the majority of cases (or no workaround available). | Order execution fails, withdrawal blocked, JWT bypass, KYT screening failure |
| **S3 - Medium** | Survivable. Minor loss of functionality in a non-critical area or would cause some inconvenience. The function is inoperable for the majority of cases but a reasonable workaround is available. | Non-core functionality issue, UI display issues, minor calculation errors |
| **S4 - Low** | Easy workaround available. Also covers cosmetic problems. Wrong font or text size; minor spelling or grammatical mistake; incorrect positioning on screen. | Cosmetic issues, spelling errors, minor UI alignment |

### Appendix C – Test Case Life Cycle

JIRA/Xray provides us the facility to maintain life cycle of a test case. A test case will have 6 states:

| Status | Description |
|--------|-------------|
| **Unexecuted** | By default, test cases are marked as 'Unexecuted', so when a test case is added it has this status |
| **WIP** | When a tester picks up a test case for execution it is marked as "WIP" meaning it is in progress |
| **Passed** | If the expected result matches the actual result, the test case is marked as Passed |
| **Failed** | If the expected result does not match the actual result, the test case is marked as Failed |
| **Blocked** | If the test case cannot be executed due to a defect or functionality not available, it is marked as Blocked |
| **De-Scoped** | If any functionality gets obsolete or is removed for some reason, the test case is marked as "De-Scoped" |

### Appendix D – API Error Codes Reference

| HTTP Code | Message | Description |
|-----------|---------|-------------|
| 200 | OK | Successful request |
| 206 | Partial Content | Results limited due to pagination cap |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Invalid or missing JWT token |
| 403 | Forbidden | Access denied based on role or asset-link control |
| 404 | Not Found | Resource does not exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Technical issues |
| 502 | Bad Gateway | External service unavailable |
| 503 | Service Unavailable | Service temporarily unavailable |

### Appendix E – Business Error Codes

| Return Code | Description | HTTP Status |
|-------------|-------------|-------------|
| ACCOUNT_ALREADY_EXIST | Customer already has an account | 400 |
| CUSTODIAN_NOT_AVAILABLE | Fireblocks/Taurus API call failed | 502 |
| INVALID_DIGITAL_ASSET | Unsupported digital asset code | 400 |
| LIMIT_EXCEEDED | Trade or withdrawal limit exceeded | 400 |
| INSUFFICIENT_BALANCE | Insufficient funds for operation | 400 |
| KYT_SCREENING_FAILED | Transaction failed KYT screening | 403 |
| INVALID_ADDRESS | Invalid blockchain address format | 400 |
| ADDRESS_NOT_WHITELISTED | Withdrawal address not whitelisted | 403 |

### Appendix F – Validation Rules

| Field | Rule | Error if Invalid |
|-------|------|------------------|
| JWT Token | Required for all API calls with valid signature | 401 Unauthorized |
| Idempotency-Key | Required for POST operations, UUID format | 400 Bad Request |
| simulationIndicator | Optional, boolean (true/false) | 400 Bad Request |
| Customer ID | Must match JWT customer claim | 403 Forbidden |
| Account ID | Must belong to authenticated customer | 403 Forbidden |
| Trade Amount | Must be within configured limits | LIMIT_EXCEEDED |
| Withdrawal Amount | Must be within configured limits | LIMIT_EXCEEDED |
| Digital Asset | Must be in enabled assets list | INVALID_DIGITAL_ASSET |
| Blockchain Address | Must be valid format for asset type | INVALID_ADDRESS |

### Appendix G – Glossary

| Term | Definition |
|------|------------|
| SCS | Sopra Crypto Solutions |
| JWT | JSON Web Token - authentication token format |
| RBAC | Role-Based Access Control |
| KYT | Know Your Transaction - compliance checking |
| AML | Anti-Money Laundering |
| OMS | Order Management System |
| CBS | Core Banking System |
| EKS | Elastic Kubernetes Service (AWS) |
| HPA | Horizontal Pod Autoscaler |
| UAT | User Acceptance Testing |
| SIT | System Integration Testing |
| NFR | Non-Functional Requirements |
| UTXO | Unspent Transaction Output (Bitcoin model) |
| MFA | Multi-Factor Authentication |
| TLS | Transport Layer Security |
| WAF | Web Application Firewall |
| PII | Personally Identifiable Information |
| GDPR | General Data Protection Regulation |
| Fiat | Traditional government-issued currency (EUR, USD) |
| Custodian | Entity managing blockchain interactions and wallet security |
| Whitelisted Address | Pre-approved withdrawal destination address |
| Travel Rule | Regulatory requirement for transaction information sharing |

---

### Appendix H – Process Flow Diagrams

#### Architecture Diagrams

**Figure 1 - Overview of the Solution**
![Overview of the Solution](../SCS-Context/images/image_1.png)

**Figure 2 - Capability Map**
![Capability Map](../SCS-Context/images/image_2.png)

**Figure 3 - Subledger Concepts**
![Subledger Concepts](../SCS-Context/images/image_3.png)

**Figure 4 - Application Architecture**
![Application Architecture](../SCS-Context/images/image_4.png)

**Figure 5 - Deployment**
![Deployment](../SCS-Context/images/image_5.png)

**Figure 6 - Link Components vs Capabilities**
![Link Components vs Capabilities](../SCS-Context/images/image_6.png)

---

#### Account Management Process Flows

**Figure 7 - Customer Request to Open a Digital Asset Account**
![Account Opening Request](../SCS-Context/images/image_7.png)

**Figure 8 - Customer Accesses a Digital Asset Dashboard**
![Digital Asset Dashboard](../SCS-Context/images/image_8.png)

**Figure 9 - Customer Logs In**
![Customer Login](../SCS-Context/images/image_9.png)

---

#### Order Management Process Flows

**Figure 10 - Initiation of the Buying Order**
![Buying Order Initiation](../SCS-Context/images/image_10.png)

**Figure 11 - Execution of a Buying Order**
![Buying Order Execution](../SCS-Context/images/image_12.png)

**Figure 12 - Initiation of a Selling Order**
![Selling Order Initiation](../SCS-Context/images/image_13.png)

**Figure 13 - Execution of a Selling Order**
![Selling Order Execution](../SCS-Context/images/image_14.png)

**Figure 22 - Customer Request Cancellation of an Order**
![Order Cancellation](../SCS-Context/images/image_22.png)

**Figure 27 - Order Integration Module**
![Order Integration Module](../SCS-Context/images/image_27.png)

---

#### Transaction Management Process Flows

**Figure 14 - New Deposit Address Request**
![Deposit Address Request](../SCS-Context/images/image_15.png)

**Figure 15 - Deposit Receipt**
![Deposit Receipt](../SCS-Context/images/image_16.png)

**Figure 16 - Whitelisted Address Creation**
![Whitelisted Address Creation](../SCS-Context/images/image_17.png)

**Figure 17 - Customer Initiates Withdrawal**
![Withdrawal Initiation](../SCS-Context/images/image_18.png)

**Figure 18 - Withdrawal Execution**
![Withdrawal Execution](../SCS-Context/images/image_19.png)

**Figure 19 - Internal Withdrawal Execution**
![Internal Withdrawal Execution](../SCS-Context/images/image_20.png)

**Figure 20 - Account-based Withdrawal Execution**
![Account-based Withdrawal](../SCS-Context/images/image_21.png)

**Figure 21 - Batch Execution for UTXO Assets**
![UTXO Batch Execution](../SCS-Context/images/image_22.png)

---

#### Compliance & Monitoring Process Flows

**Figure 23 - Continuous Monitoring**
![Continuous Monitoring](../SCS-Context/images/image_23.png)

**Figure 24 - Travel Rule Data Management**
![Travel Rule Management](../SCS-Context/images/image_24.png)

**Figure 25 - KYT Task Management**
![KYT Task Management](../SCS-Context/images/image_25.png)

**Figure 32 - Document Upload for KYT Issue**
![KYT Document Upload](../SCS-Context/images/image_32.png)

---

#### Additional Feature Process Flows

**Figure 26 - Price Management**
![Price Management](../SCS-Context/images/image_26.png)

**Figure 28 - Limit Update Management**
![Limit Update Management](../SCS-Context/images/image_28.png)

**Figure 29 - Tax-related Data Computation**
![Tax Data Computation](../SCS-Context/images/image_29.png)

**Figure 30 - Retrieve Tax Reports / Statement Report Generation**
![Tax Reports](../SCS-Context/images/image_30.png)

**Figure 31 - Create Bank Position**
![Create Bank Position](../SCS-Context/images/image_31.png)

---

#### Status Flow Diagrams

**Figure 33 - Buy/Sell Order Statuses**
![Order Statuses](../SCS-Context/images/image_45.png)

**Figure 34 - Withdrawal Statuses**
![Withdrawal Statuses](../SCS-Context/images/image_46.png)

**Figure 35 - Deposit Statuses**
![Deposit Statuses](../SCS-Context/images/image_54.png)

---

#### Infrastructure Diagrams

**Figure 36 - Architecture Principles**
![Architecture Principles](../SCS-Context/images/image_48.png)

**Figure 37 - Technology Stack**
![Technology Stack](../SCS-Context/images/image_49.png)

**Figure 38 - Current Infrastructure**
![Current Infrastructure](../SCS-Context/images/image_50.png)

**Figure 39 - Target Infrastructure**
![Target Infrastructure](../SCS-Context/images/image_51.png)

**Figure 40 - Cluster Autoscaler**
![Cluster Autoscaler](../SCS-Context/images/image_52.png)

**Figure 41 - Horizontal Pod Autoscaler**
![Horizontal Pod Autoscaler](../SCS-Context/images/image_53.png)

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Product Owner | | | |
| Business Representative | | | |
| Security Lead | | | |

---

*This Test Strategy document is subject to change based on project requirements and stakeholder feedback.*

**Document Version:** 0.1  
**Generated on:** June 1, 2026
