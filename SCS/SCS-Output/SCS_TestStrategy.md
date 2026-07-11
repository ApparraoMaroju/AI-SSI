# Test Strategy for SCS Core (Sopra Crypto Solutions)

- **Document Version:** 1.0  
- **Author:** Test Team  
- **Role:** Test Manager / QA Lead  
- **Date:** June 1, 2026  
- **Status:** Draft  

---

# Document Control

## Revision History

| Version | Date | Author | Description of Changes |
|---------|------|--------|------------------------|
| 1.0 | June 1, 2026 | Test Team | Initial Draft |
| | | | |

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Product Owner | | | |

## Distribution List

| Name | Role | Organization |
|------|------|--------------|
| | Test Lead | Sopra Steria |
| | Product Owner | Bank |
| | Development Lead | Sopra Steria |

---

# 1. Introduction

## 1.1 Purpose

This document defines the overall testing approach for the **SCS Core (Sopra Crypto Solutions)** project. It outlines the testing activities, methodologies, roles and responsibilities, defect management processes, risk management, stakeholder engagement, and reporting mechanisms.

The purpose of this Test Strategy is to:
- Document and achieve agreement on the high-level testing approach for SCS Core
- Define testing standards and best practices for cryptocurrency/digital asset banking platform
- Clarify testing activities and quality assurance processes
- Establish clear roles and responsibilities for testing the platform

## 1.2 Scope

This Test Strategy covers:
- Account Management (creation, retrieval, status updates)
- Order Management (buy, sell, convert digital assets)
- Transaction Management (deposit, withdrawal)
- API Security (JWT validation, authentication, authorization)
- Role-Based Access Control (RBAC)
- Integration with external services (Custodians, OMS, Exchange venues)
- Customer and Bank User Web Interfaces

## 1.3 Intended Audience

This document is intended for the following stakeholders:

| Role | Responsibilities |
|------|------------------|
| **Test Lead / Manager** | Manage testing activities, ensure compliance with strategy |
| **Test Engineers** | Execute test cases, report defects according to defined processes |
| **Business Analysts** | Provide requirements, validate test scenarios |
| **Developers** | Support testing, fix defects, provide technical guidance |
| **Product Owner** | Review and approve testing approach, accept deliverables |
| **Project Manager** | Oversee project delivery, manage risks and escalations |
| **Bank Representatives** | UAT execution and sign-off |

## 1.4 References

| Document Name | Version | Location |
|---------------|---------|----------|
| SCS Project Context | 1.0 | SCS-Context/SCS_ProjectContext.md |
| SCS Feature Context | 1.0 | SCS-Context/SCS_FeatureContext.md |
| SCS Test Context | 1.0 | SCS-Context/SCS_TestContext.md |
| SCS Reference Document | v26 | SCS-Input |

---

# 2. Project Overview

## 2.1 Project Background

SCS Core (Sopra Crypto Solutions) is a banking solution that enables banks to deploy a crypto-account offering for their customers. It provides end-to-end management of digital asset accounts, orders (buy/sell), transactions (deposits/withdrawals), and integration with custodians, order management systems, and exchange venues.

The platform supports:
- **Bank Customers:** Create crypto-accounts, buy/sell digital assets, deposit/withdraw cryptocurrencies
- **Bank Users:** Manage customer accounts, monitor bank positions, provide support and oversight

## 2.2 System Architecture Overview

### Technology Stack
- **Frontend:** Web UI (customer and bank user interfaces)
- **Backend:** AWS EKS (Kubernetes microservices architecture)
- **Database:** AWS DocumentDB, S3, EFS
- **API Type:** REST API
- **Cloud Infrastructure:** AWS (EKS, Cognito, API Gateway, WAF, GuardDuty, Secrets Manager, CloudWatch)
- **Container Orchestration:** Kubernetes with Cluster Autoscaler and Horizontal Pod Autoscaler (HPA)

### Architecture Diagram
![Application Architecture](SCS-Context/images/image_4.png)

### External Integrations
- **Custodians:** Fireblocks, Taurus (for blockchain interactions and security)
- **Order Management System (OMS):** Wyden
- **Exchange Venues:** Kraken, Coinbase
- **KYT/AML Provider:** Chainalysis
- **Core Banking System (CBS):** Integration via defined API endpoints

## 2.3 Key Stakeholders

| Stakeholder | Role | Contact |
|-------------|------|---------|
| Bank Product Owner | Business requirements, UAT sign-off | |
| Sopra Steria Test Lead | Test planning and execution | |
| Development Lead | Technical support, defect resolution | |
| Security Team | Security testing oversight | |

---

# 3. Test Scope

## 3.1 In Scope

The following items are **in scope** for testing:

| Category | Items |
|----------|-------|
| **Functional Areas** | Account management, Order management, Transaction management |
| **Integrations** | Custodians (Fireblocks, Taurus), OMS (Wyden), Exchange venues, Chainalysis KYT |
| **User Interfaces** | Customer Web Interface, Bank User Web Interface |
| **APIs** | /accounts, /orders, /transactions, /bank-user-access-controls |
| **Workflows** | Buy order execution, Sell order execution, Deposit receipt, Withdrawal execution |
| **Security** | JWT validation, RBAC, Asset-link based access control, TLS 1.3 |

### Detailed Functional Areas

| Functional Area | Test Coverage |
|-----------------|---------------|
| Account Opening | Customer account creation, one account per customer limit |
| Buy Orders | Order initiation, pre-trade validation, execution, post-trade settlement |
| Sell Orders | Order initiation, validation, execution, fiat currency conversion |
| Deposits | Deposit address creation, deposit receipt, KYT screening |
| Withdrawals | Whitelisted address creation, withdrawal initiation, KYT/AML checks, execution |
| Order Cancellation | Customer-initiated cancellation workflow |
| Limit Management | Trade limits, withdrawal limits validation |
| Price Management | Price retrieval and display |
| Tax Reports | Tax-related data computation and retrieval |
| Bank Positions | Bank position creation and management |

## 3.2 Out of Scope

The following items are **out of scope** for this testing engagement:

- Core Banking System (CBS) implementation and internal testing
- Bank-specific authentication provider implementation
- Exchange venue internal logic and testing
- Custodian internal security mechanisms
- Production infrastructure deployment and verification
- Third-party systems not owned by Sopra Steria
- Non-supported browsers or legacy environments

## 3.3 Assumptions

- Requirements are documented in the SCS Reference Document and context files
- Test environments will be available as per schedule with AWS infrastructure
- Test data will be prepared including JWT tokens, customer data, and digital asset configurations
- Custodian sandbox/test environments (Fireblocks, Taurus) will be available
- OMS test environment (Wyden) will be accessible
- Mock services for CBS API endpoints will be provided for testing

## 3.4 Dependencies

| Dependency | Owner | Impact if Not Met |
|------------|-------|-------------------|
| AWS Environment (EKS, Cognito, API Gateway) | DevOps Team | Testing cannot proceed |
| Custodian Test Environment | External (Fireblocks/Taurus) | Integration testing blocked |
| OMS Test Environment | External (Wyden) | Order execution testing blocked |
| DocumentDB with seed data | DevOps Team | Test data unavailable |
| JWT Token generation capability | Security Team | Authentication testing blocked |

---

# 4. Test Approach

## 4.1 Testing Methodology

The project follows **Agile** methodology with Sprint-based testing. Testing activities are organized as follows:

### Sprint-Based Testing Process:
- **Sprint Planning** – Test scope and estimates defined based on user stories
- **Test Case Creation + BA Review** – Test cases created and reviewed by Business Analyst/Product Owner
- **Test Execution and Bug Fixing** – Execution performed with defect tracking
- **Sprint Retrospective** – Lessons learned captured

### Testing Phases:

| Phase | Description | Entry Criteria | Exit Criteria |
|-------|-------------|----------------|---------------|
| Unit Testing | Developer testing | Code complete | All unit tests pass |
| Integration Testing | API and service integration testing | UT complete | All integrations verified |
| System Testing | End-to-end functional testing | SIT complete | All test cases executed |
| Security Testing | JWT, RBAC, encryption validation | ST in progress | Security requirements met |
| Performance Testing | Load and stress testing | Core functionality stable | Performance targets met |
| UAT | Bank user acceptance testing | ST complete | Business sign-off |

### Process Flow Diagrams

#### Buying Order Execution Flow
![Buying Order Execution](SCS-Context/images/image_11.png)

#### Selling Order Execution Flow
![Selling Order Execution](SCS-Context/images/image_13.png)

#### Withdrawal Execution Flow
![Withdrawal Execution](SCS-Context/images/image_18.png)

## 4.2 Types of Testing

### 4.2.1 Functional Testing

| Testing Type | Description | Applicable |
|--------------|-------------|------------|
| **Smoke Testing** | Verify critical functionalities (login, account creation, order placement) after each build | Yes |
| **Sanity Testing** | Quick validation of specific functionality after bug fixes | Yes |
| **Regression Testing** | Ensure existing functionality is not impacted by new changes | Yes |
| **Integration Testing** | Verify integrations with Custodians, OMS, Exchange venues, CBS | Yes |
| **End-to-End Testing** | Validate complete workflows (account opening → buy order → withdrawal) | Yes |
| **User Acceptance Testing** | Bank validation of business requirements | Yes |

### 4.2.2 Non-Functional Testing

| Testing Type | Description | Applicable |
|--------------|-------------|------------|
| **Performance Testing** | Validate API response times, concurrent user handling | Yes |
| **Security Testing** | JWT validation, TLS 1.3, SQL injection, XSS prevention | Yes |
| **Accessibility Testing** | Ensure compliance with accessibility standards (WCAG) | Yes |
| **Usability Testing** | Evaluate customer and bank user experience | Yes |
| **Compatibility Testing** | Verify cross-browser (Chrome, Firefox, Safari, Edge) compatibility | Yes |

### Security Testing Focus Areas
- TLS 1.3 enforcement validation
- JWT token manipulation attempts (expired, invalid, malformed tokens)
- SQL injection and XSS attack prevention (WAF rules)
- CORS policy enforcement
- Rate limiting effectiveness
- Unauthorized access attempts (cross-customer access)
- Role-Based Access Control validation
- Asset-link based access control verification

## 4.3 Test Design Techniques

The following test design techniques will be applied:

- **Equivalence Class Partitioning** – Valid/invalid JWT tokens, valid/invalid digital assets
- **Boundary Value Analysis** – Trade limits, withdrawal limits, amount boundaries
- **Decision Table Testing** – Role-based access combinations, order status transitions
- **State Transition Testing** – Order statuses (Buy/Sell), Withdrawal statuses, Deposit statuses
- **Use Case Testing** – Customer workflows, Bank user workflows
- **Error Guessing** – Experience-based testing for edge cases
- **Exploratory Testing** – Unscripted testing to discover defects

### Status Flow Testing Reference

#### Order Status Transitions
![Order Statuses](SCS-Context/images/image_45.png)

#### Withdrawal Status Transitions
![Withdrawal Statuses](SCS-Context/images/image_46.png)

#### Deposit Status Transitions
![Deposit Statuses](SCS-Context/images/image_47.png)

---

# 5. Test Deliverables

The following deliverables will be produced:

| Deliverable | Description | Owner | Timeline |
|-------------|-------------|-------|----------|
| Test Strategy | High-level testing approach (this document) | Test Manager | Project Start |
| Test Plan | Detailed test planning document per sprint | Test Lead | Before Test Design |
| Test Scenarios | High-level test scenarios for each feature | Test Analyst | Test Design Phase |
| Test Cases/Scripts | Detailed test steps with expected results | Test Engineer | Test Design Phase |
| Test Data | JWT tokens, customer data, digital asset configurations | Test Analyst | Before Execution |
| API Test Collections | Postman/REST client collections | Test Engineer | Test Design Phase |
| Defect Reports | Logged defects with severity and priority | Test Engineer | During Execution |
| Test Execution Report | Daily/Weekly status reports | Test Lead | During Execution |
| Test Completion Report | Final testing summary with metrics | Test Manager | End of Testing |

---

# 6. Test Environment

## 6.1 Environment Overview

| Environment | Purpose | Infrastructure | Refresh Schedule |
|-------------|---------|----------------|------------------|
| DEV | Development testing | AWS EKS (Dev) | On-demand |
| TEST | System testing | AWS EKS (Test) | Weekly |
| STAGING | Pre-production/Integration testing | AWS EKS (Staging) | Per release |
| UAT | User acceptance testing | AWS EKS (UAT) | Per release |

## 6.2 Environment Requirements

### Infrastructure Requirements
| Component | Specification | Notes |
|-----------|---------------|-------|
| Cloud Platform | AWS | EKS-based Kubernetes |
| Authentication | AWS Cognito | OAuth2, MFA support |
| API Gateway | AWS API Gateway | Rate limiting, WAF integration |
| Database | AWS DocumentDB | With seed data |
| Container Orchestration | Kubernetes | HPA and Cluster Autoscaler |

### Browser/Client Requirements
| Component | Version | Notes |
|-----------|---------|-------|
| Chrome | Latest | Primary browser |
| Firefox | Latest | Secondary browser |
| Safari | Latest | Mac testing |
| Edge | Latest | Windows testing |
| Postman/REST Client | Latest | API Testing |

### External Integration Requirements
| System | Environment | Purpose |
|--------|-------------|---------|
| Fireblocks | Sandbox | Custodian integration testing |
| Taurus | Sandbox | Custodian integration testing |
| Wyden | Test | OMS integration testing |
| CBS Mock | Test | Core Banking System simulation |

### Access Requirements
- AWS Cognito credentials for test users
- JWT token generation capability
- Role-based access for Customer and Bank User personas
- API Gateway access with valid API keys

## 6.3 Environment Issues and Escalation

In case of environment issues:
1. Log the issue in JIRA with Environment label
2. Notify DevOps team immediately
3. Escalate to Project Manager if not resolved within 4 hours
4. Document impact on testing schedule

---

# 7. Test Data Management

## 7.1 Test Data Strategy

- Test data will be prepared by the Test Team in coordination with Development
- Sensitive data will be anonymized as per data protection requirements (GDPR)
- JWT tokens will be generated with appropriate claims (sub, iat, exp, client, customer, role)
- Test data will be stored in DocumentDB test instance

## 7.2 Test Data Requirements

| Data Type | Source | Preparation Method | Owner |
|-----------|--------|-------------------|-------|
| JWT Tokens (Valid) | AWS Cognito | Generated with valid claims | Test Team |
| JWT Tokens (Invalid) | Manual creation | Expired, malformed, missing claims | Test Team |
| Customer Data | Seed data | Pre-loaded in DocumentDB | DevOps |
| Digital Assets | Configuration | BTC, ETH, SHIB configured | DevOps |
| Order Data | Test execution | Created during testing | Test Team |
| Transaction Data | Test execution | Created during testing | Test Team |

### Test Data Values

| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid JWT Token | Token with valid sub, iat, exp, client, customer, role | Happy path authentication |
| Expired JWT Token | Token with past exp timestamp | Negative - token expiration test |
| Invalid JWT Token | Malformed/corrupted token | Negative - security test |
| Valid Idempotency-Key | UUID format | Idempotency test |
| Duplicate Idempotency-Key | Same UUID as previous request | Idempotency validation |
| Valid Digital Asset | BTC, ETH, SHIB | Order creation tests |
| Invalid Digital Asset | Unsupported asset code | Negative - validation test |
| Amount within limits | Based on configured trade/withdrawal limits | Happy path |
| Amount exceeding limits | Above configured limits | Negative - limit validation |
| simulationIndicator=true | Query parameter | Simulation mode test |
| simulationIndicator=false | Query parameter | Normal execution test |

## 7.3 Test Data Refresh

- Test data refresh frequency: Per Sprint
- Refresh process: DocumentDB restore from baseline snapshot
- JWT tokens regenerated as needed

---

# 8. Defect Management

## 8.1 Defect Management Process

1. **Identification** – Defect identified during test execution
2. **Logging** – Defect logged in JIRA with required details
3. **Triage** – Defect reviewed and prioritized in triage meeting
4. **Assignment** – Defect assigned to developer
5. **Resolution** – Developer fixes the defect
6. **Retest** – Tester verifies the fix
7. **Closure** – Defect closed upon successful verification

## 8.2 Defect Logging Standards

All defects must include:
- **Title:** Clear, concise description (e.g., "JWT validation fails for expired token")
- **Description:** Detailed steps to reproduce
- **Expected vs. Actual Result:** Clear comparison
- **Environment details:** Environment name, browser, API endpoint
- **Screenshots/logs:** API responses, error messages
- **Severity and Priority:** As per definitions below
- **Linked User Story:** Reference to related requirement

## 8.3 Defect Severity Definitions

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical (S1)** | System unavailable, no workaround available, security breach | System crash, data loss, unauthorized access, payment processing failure |
| **High (S2)** | Major functionality impacted, limited workaround | Order execution fails, withdrawal blocked, JWT validation bypass |
| **Medium (S3)** | Moderate impact, workaround available | Non-core functionality issue, UI display issues, minor calculation errors |
| **Low (S4)** | Minor issue, easy workaround | Cosmetic issues, spelling errors, minor UI alignment |

## 8.4 Defect Priority Definitions

| Priority | Definition | Response Time |
|----------|------------|---------------|
| **P1 - Critical** | Must be fixed immediately, blocking release | Immediate (within 4 hours) |
| **P2 - High** | Must be fixed in current sprint | Within 24-48 hours |
| **P3 - Medium** | Should be fixed, can be deferred if necessary | Within current release |
| **P4 - Low** | Can be fixed in future release | Future release |

## 8.5 Defect Triage Process

- **Triage Frequency:** Daily during active testing, twice weekly otherwise
- **Participants:** Test Lead, Dev Lead, BA, Product Owner
- **Purpose:** Review new defects, validate severity/priority, assign owners, discuss blockers

---

# 9. Entry and Exit Criteria

## 9.1 Entry Criteria

### Test Execution Entry Criteria
- [ ] AWS EKS environment is stable and available
- [ ] AWS Cognito configured for authentication
- [ ] AWS API Gateway deployed and accessible
- [ ] DocumentDB has seed data loaded
- [ ] Test data (JWT tokens, customer data) is prepared
- [ ] Test cases are reviewed and approved
- [ ] Build is deployed and smoke tested
- [ ] All Critical/High severity defects from previous phase are resolved
- [ ] External integrations (Custodian sandbox, OMS test) are accessible
- [ ] Required documentation is available

## 9.2 Exit Criteria

### Test Execution Exit Criteria
- [ ] All planned test cases executed
- [ ] Test pass rate meets threshold (≥95%)
- [ ] No open Critical (S1) severity defects
- [ ] No more than 2 open High (S2) severity defects (with approved workarounds)
- [ ] All security test cases passed
- [ ] All integration test cases with external systems passed
- [ ] Test completion report is prepared and approved
- [ ] Sign-off obtained from Product Owner and stakeholders

---

# 10. Test Suspension and Resumption

## 10.1 Suspension Criteria

Testing will be suspended if:
- AWS environment becomes unstable or unavailable
- Build deployment fails or introduces blocking issues
- More than 30% of test cases fail in smoke testing
- Critical defects block further testing progress
- External integration services (Custodian, OMS) become unavailable
- Security vulnerabilities discovered requiring immediate attention

## 10.2 Resumption Criteria

Testing will resume when:
- Issues causing suspension are resolved
- Environment is restored to stable state
- Sanity testing passes on fixed build
- External integrations are restored
- Approval received from Test Lead/Manager
- Security issues are remediated and verified

---

# 11. Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Test Manager** | Overall test governance, stakeholder management, risk management, resource allocation |
| **Test Lead** | Test planning, estimation, daily coordination, defect management, reporting, compliance with strategy |
| **Test Analyst** | Test scenario/case design, test data preparation, requirement analysis, walkthrough with BA/PO |
| **Test Engineer** | Test execution, defect logging, test evidence collection, API testing |
| **Automation Engineer** | Automation framework development, regression script creation, maintenance |
| **Performance Tester** | Performance test design, execution, analysis, NFR validation |
| **Security Tester** | Security test design, JWT validation tests, penetration testing support |
| **Business Analyst** | Requirements clarification, test scenario review, expectation sheets |
| **Developer** | Defect resolution, test support, technical guidance, unit testing |
| **Product Owner** | Acceptance criteria definition, UAT execution, sign-off |
| **DevOps Engineer** | Environment setup, deployment support, infrastructure issues |

---

# 12. Tools and Infrastructure

## 12.1 Test Management Tools

| Tool | Purpose | Access |
|------|---------|--------|
| JIRA | User story management, defect tracking, sprint management | Project JIRA instance |
| Confluence | Documentation repository, test evidence storage | Project Confluence space |
| Xray for JIRA | Test case management, test execution tracking | Integrated with JIRA |

## 12.2 Testing Tools

| Tool | Purpose | Applicable |
|------|---------|------------|
| Postman / REST Assured | API Testing, JWT validation testing | Yes |
| Selenium / Cypress | UI Automation (Customer and Bank User interfaces) | Yes |
| JMeter / Gatling | Performance Testing (API load testing) | Yes |
| OWASP ZAP | Security Testing (vulnerability scanning) | Yes |
| AWS CloudWatch | Log analysis, monitoring verification | Yes |
| Browser DevTools | Network analysis, JWT inspection | Yes |

## 12.3 Environment Tools

| Tool | Purpose |
|------|---------|
| AWS Console | Environment monitoring, CloudWatch logs |
| kubectl | Kubernetes cluster management |
| Docker | Container management |

---

# 13. Risk Management

## 13.1 Risk Identification and Mitigation

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy | Owner |
|---------|------------------|-------------|--------|---------------------|-------|
| R001 | AWS environment unavailability | Medium | High | Backup environment, early escalation to DevOps | DevOps Lead |
| R002 | Delayed requirement delivery | Medium | High | Buffer in schedule, parallel test design activities | Test Lead |
| R003 | Custodian sandbox unavailability | Medium | High | Mock services for initial testing, escalation to vendor | Project Manager |
| R004 | OMS integration issues | Medium | High | Early integration testing, mock services | Test Lead |
| R005 | Test data unavailability | Medium | High | Early data preparation, synthetic data generation | Test Analyst |
| R006 | Resource unavailability | Medium | Medium | Cross-training, backup resources | Test Manager |
| R007 | Scope changes | Medium | High | Change control process, impact analysis | Project Manager |
| R008 | Security vulnerabilities discovered | Low | Critical | Early security testing, rapid response team | Security Lead |
| R009 | Performance issues in API | Medium | High | Early performance testing, optimization sprints | Performance Tester |

## 13.2 Risk Monitoring

- Risks will be reviewed in daily standup and weekly status meetings
- Risk register maintained in JIRA/Confluence
- Escalation path: Test Lead → Test Manager → Project Manager → Steering Committee

---

# 14. Communication and Reporting

## 14.1 Communication Plan

| Communication | Frequency | Participants | Medium |
|---------------|-----------|--------------|--------|
| Daily Standup | Daily | Test Team, Dev Team | Teams/In-person |
| Test Status Report | Weekly | All stakeholders | Email + Confluence |
| Defect Triage | Daily/Twice Weekly | Test Lead, Dev Lead, BA, PO | Meeting |
| Sprint Review | End of Sprint | All stakeholders | Meeting |
| Risk Review | Weekly | Test Lead, PM | Meeting |

## 14.2 Reporting

### Daily Reports
- Test execution progress (cases executed, passed, failed, blocked)
- Defects raised/closed
- Blockers and issues

### Weekly Reports
- Test metrics summary (coverage, pass rate, defect density)
- Defect analysis (by severity, priority, component)
- Risk and issues update
- Upcoming activities and milestones

### Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| Test Execution Progress | % tests executed vs. planned | 100% |
| Test Pass Rate | % tests passed vs. executed | ≥95% |
| Defect Density | Defects per test case | ≤0.1 |
| Defect Resolution Time | Average time to fix defects | ≤2 days (P1/P2) |
| Test Coverage | % requirements covered by tests | ≥100% |
| Automation Coverage | % of regression tests automated | ≥70% |

---

# 15. Appendices

## Appendix A – Glossary

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
| UTXO | Unspent Transaction Output |
| MFA | Multi-Factor Authentication |
| TLS | Transport Layer Security |
| WAF | Web Application Firewall |

## Appendix B – Test Case Life Cycle

| Status | Description |
|--------|-------------|
| **Unexecuted** | Test case not yet executed (default state) |
| **WIP** | Test case execution in progress |
| **Passed** | Test case executed successfully, actual matches expected |
| **Failed** | Test case execution failed, defect raised |
| **Blocked** | Test case cannot be executed due to defect or missing functionality |
| **De-Scoped** | Test case removed from scope |

## Appendix C – API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /accounts | Create account opening request |
| GET | /accounts | Retrieve account details |
| POST | /orders | Create buy/sell order |
| GET | /orders | Retrieve orders |
| POST | /transactions | Create deposit/withdrawal transaction |
| GET | /transactions | Retrieve transactions |
| POST | /bank-user-access-controls | Verify bank user access to customer |

## Appendix D – Error Codes Reference

| Code | Message |
|------|---------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing JWT token |
| 403 | Forbidden - Access denied based on role or asset-link control |
| 404 | Not Found - Resource does not exist |
| 206 | Partial Content - Results limited due to pagination cap |
| 5xx | Server Error - Technical issues (DB unavailable, external service error) |

## Appendix E – Business Error Codes

| Return Code | Description |
|-------------|-------------|
| ACCOUNT_ALREADY_EXIST | Customer already has an account |
| CUSTODIAN_NOT_AVAILABLE | Fireblocks/Taurus API call failed |

---

# Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Product Owner | | | |
| Business Representative | | | |

---

*This Test Strategy document is subject to change based on project requirements and stakeholder feedback.*

**Document generated on:** June 1, 2026
