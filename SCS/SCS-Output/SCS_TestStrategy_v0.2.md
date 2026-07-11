# Test Strategy for SCS Core (Sopra Crypto Solutions)

- **Document Version:** 0.2  
- **Author:** Test Team  
- **Role:** Test Manager / QA Lead  
- **Date:** June 1, 2026  
- **Status:** Draft - Revised  

---

# Document Control

## Revision History

| Version | Date | Author | Description of Changes |
|---------|------|--------|------------------------|
| 0.1 | June 1, 2026 | Test Team | Initial Draft |
| 0.2 | June 1, 2026 | Test Team | Revised with complete context - added all process flows, validation rules, security features, acceptance criteria |

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
| | Security Lead | Sopra Steria |

---

# 1. Introduction

## 1.1 Purpose

This document defines the overall testing approach for the **SCS Core (Sopra Crypto Solutions)** project. It outlines the testing activities, methodologies, roles and responsibilities, defect management processes, risk management, stakeholder engagement, and reporting mechanisms.

The purpose of this Test Strategy is to:
- Document and achieve agreement on the high-level testing approach for SCS Core
- Define testing standards and best practices for cryptocurrency/digital asset banking platform
- Clarify testing activities and quality assurance processes
- Establish clear roles and responsibilities for testing the platform
- Ensure compliance with banking regulations (KYT, AML, Travel Rule)

## 1.2 Scope

This Test Strategy covers:
- Account Management (creation, retrieval, status updates, one-account-per-customer limit)
- Order Management (buy, sell, convert digital assets, order cancellation)
- Transaction Management (deposit, withdrawal, internal withdrawal, batch execution for UTXO)
- API Security (JWT validation, authentication, authorization, non-repudiation)
- Role-Based Access Control (RBAC) and Asset-link based access control
- Integration with external services (Custodians, OMS, Exchange venues, KYT/AML providers)
- Customer and Bank User Web Interfaces
- Compliance features (KYT screening, Travel Rule, AML)
- Price Management and Tax Reporting
- Bank Position Management and Limit Management

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
| **Security Team** | Security testing oversight, compliance validation |
| **Compliance Team** | KYT/AML/Travel Rule validation |

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

### User Stories Covered

| User Type | User Story |
|-----------|------------|
| Bank Customer | Create a crypto-account to hold and manage digital assets |
| Bank Customer | Buy digital assets to invest in cryptocurrencies |
| Bank Customer | Sell digital assets to convert them to fiat currency |
| Bank Customer | Deposit digital assets to transfer them to my account |
| Bank Customer | Withdraw digital assets to transfer them to external addresses |
| Bank User | Manage customer accounts for support and oversight |
| Bank User | View dashboards to monitor bank positions and operations |

## 2.2 System Architecture Overview

### Technology Stack

| Component | Technology | Details |
|-----------|------------|---------|
| **Frontend** | Web UI | Customer and bank user interfaces |
| **Backend** | AWS EKS | Kubernetes microservices architecture |
| **Database** | AWS DocumentDB, S3, EFS | Data persistence |
| **API Type** | REST API | JSON-based communication |
| **Cloud Infrastructure** | AWS | EKS, Cognito, API Gateway, WAF, GuardDuty, Secrets Manager, CloudWatch |
| **Container Orchestration** | Kubernetes | Cluster Autoscaler and Horizontal Pod Autoscaler (HPA) |
| **Authentication** | AWS Cognito | OAuth2, MFA, enterprise SSO integration |
| **Encryption** | TLS 1.3 / AWS KMS | Data in transit and at rest |

### Architecture Diagram Reference
- Figure 1 - Overview of the Solution
- Figure 2 - Capability Map
- Figure 3 - Subledger Concepts
- Figure 4 - Application Architecture
- Figure 5 - Deployment Architecture
- Figure 36 - Architecture Principles
- Figure 37 - Technology Stack
- Figure 38 - Current Infrastructure
- Figure 39 - Target Infrastructure
- Figure 40 - Cluster Autoscaler
- Figure 41 - Horizontal Pod Autoscaler

### Infrastructure Details
- **Deployment:** Private subnets within AWS VPC with EKS workloads
- **Security:** Multi-layered approach including Security Groups, NACLs, AWS Network Firewall, Kubernetes Network Policies, Service Mesh (Istio)

### External Integrations

| Integration Type | Provider | Purpose |
|------------------|----------|---------|
| **Custodians** | Fireblocks, Taurus | Blockchain interactions, wallet management, security |
| **Order Management System** | Wyden | Order routing and execution |
| **Exchange Venues** | Kraken, Coinbase | Order execution |
| **KYT/AML Provider** | Chainalysis | Transaction screening, compliance |
| **Core Banking System** | Bank CBS | Account information, fiat operations |

## 2.3 Key Stakeholders

| Stakeholder | Role | Responsibility |
|-------------|------|----------------|
| Bank Product Owner | Business requirements | UAT sign-off, acceptance criteria |
| Sopra Steria Test Lead | Test planning | Test execution oversight |
| Development Lead | Technical support | Defect resolution |
| Security Team | Security oversight | Compliance validation |
| Compliance Team | Regulatory compliance | KYT/AML/Travel Rule validation |

---

# 3. Test Scope

## 3.1 In Scope - Detailed Functional Areas

### 3.1.1 Account Management

| Test Area | Description | Process Flow Reference |
|-----------|-------------|------------------------|
| Account Opening | Customer request to open digital asset account | Figure 7 |
| Dashboard Access | Customer accesses digital asset dashboard | Figure 8 |
| Customer Login | Authentication and session management | Figure 9 |
| One Account Limit | Validation of single account per customer | Acceptance Criteria |

### 3.1.2 Order Management

| Test Area | Description | Process Flow Reference |
|-----------|-------------|------------------------|
| Buy Order Initiation | Customer initiates buying order | Figure 10 |
| Buy Order Execution | End-to-end buy order processing | Figure 11 |
| Sell Order Initiation | Customer initiates selling order | Figure 12 |
| Sell Order Execution | End-to-end sell order processing | Figure 13 |
| Order Cancellation | Customer cancels pending order | Figure 22 |
| Order Status Transitions | All order status states | Figure 33 |
| Order Integration Module | OMS integration testing | Figure 27 |

### 3.1.3 Transaction Management

| Test Area | Description | Process Flow Reference |
|-----------|-------------|------------------------|
| Deposit Address Request | Customer requests new deposit address | Figure 14 |
| Deposit Receipt | Processing incoming deposits | Figure 15 |
| Whitelisted Address Creation | Customer creates whitelisted withdrawal address | Figure 16 |
| Withdrawal Initiation | Customer initiates withdrawal | Figure 17 |
| Withdrawal Execution | Standard withdrawal processing | Figure 18 |
| Internal Withdrawal | Internal transfer execution | Figure 19 |
| Account-based Withdrawal | Account-based withdrawal execution | Figure 20 |
| UTXO Batch Execution | Batch processing for UTXO assets (BTC) | Figure 21 |
| Withdrawal Status Transitions | All withdrawal status states | Figure 34 |
| Deposit Status Transitions | All deposit status states | Figure 35 |

### 3.1.4 Compliance & Monitoring

| Test Area | Description | Process Flow Reference |
|-----------|-------------|------------------------|
| Continuous Monitoring | Real-time transaction monitoring | Figure 23 |
| Travel Rule Management | Travel Rule data handling | Figure 24 |
| KYT Task Management | KYT screening and task workflows | Figure 25 |
| KYT Document Upload | Document submission for KYT issues | Figure 32 |

### 3.1.5 Additional Features

| Test Area | Description | Process Flow Reference |
|-----------|-------------|------------------------|
| Price Management | Digital asset price retrieval and display | Figure 26 |
| Limit Management | Trade and withdrawal limit updates | Figure 28 |
| Tax Data Computation | Tax-related calculations | Figure 29 |
| Tax Report Generation | Statement and tax report retrieval | Figure 30 |
| Bank Position Management | Bank position creation and monitoring | Figure 31 |

### 3.1.6 API Testing Scope

| Method | Endpoint | Description | Test Focus |
|--------|----------|-------------|------------|
| POST | /accounts | Create account opening request | Validation, idempotency, simulation mode |
| GET | /accounts | Retrieve account details | Authorization, pagination |
| POST | /orders | Create buy/sell order | Pre-trade validation, limits, simulation |
| GET | /orders | Retrieve orders | Filtering, pagination |
| POST | /transactions | Create deposit/withdrawal | KYT screening, limits, simulation |
| GET | /transactions | Retrieve transactions | Authorization, filtering |
| POST | /bank-user-access-controls | Verify bank user access | RBAC, asset-link control |

### 3.1.7 Security Testing Scope

| Security Feature | Test Focus |
|------------------|------------|
| JWT Token Validation | Token structure, expiration, signature, claims (sub, iat, exp, client, customer, role) |
| Multi-Factor Authentication (MFA) | MFA flow, bypass attempts |
| OAuth2-based Access | Token flow, refresh tokens |
| Role-Based Access Control (RBAC) | Role enforcement at UI and API levels |
| Asset-link Based Access Control | Customer can only access own assets |
| Non-repudiation | Authorization-Reference header validation |
| TLS 1.3 Encryption | Protocol enforcement, certificate validation |
| Rate Limiting | Request throttling, burst handling |
| SQL Injection Prevention | WAF rules effectiveness |
| XSS Prevention | Input sanitization, WAF rules |
| CORS Policy | Cross-origin request handling |

## 3.2 Out of Scope

The following items are **out of scope** for this testing engagement:

- Core Banking System (CBS) implementation and internal testing
- Bank-specific authentication provider implementation (will use mock/default)
- Exchange venue internal logic and testing
- Custodian internal security mechanisms
- Production infrastructure deployment and verification
- Third-party systems not owned by Sopra Steria
- Non-supported browsers or legacy environments
- Mobile application testing (if any)

## 3.3 Assumptions

- Requirements are documented in the SCS Reference Document and context files
- Test environments will be available as per schedule with AWS infrastructure
- Test data will be prepared including JWT tokens with all required claims
- Custodian sandbox/test environments (Fireblocks, Taurus) will be available
- OMS test environment (Wyden) will be accessible
- Mock services for CBS API endpoints will be provided for testing
- Chainalysis test environment will be available for KYT testing
- Digital assets (BTC, ETH, SHIB) will be configured in test environment

## 3.4 Dependencies

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

# 4. Test Approach

## 4.1 Testing Methodology

The project follows **Agile** methodology with Sprint-based testing. Testing activities are organized as follows:

### Sprint-Based Testing Process
1. **Sprint Planning** – Test scope and estimates defined based on user stories
2. **Test Case Creation + BA Review** – Test cases created and reviewed by Business Analyst/Product Owner
3. **Test Execution and Bug Fixing** – Execution performed with defect tracking
4. **Sprint Retrospective** – Lessons learned captured

### Testing Phases

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

## 4.2 Types of Testing

### 4.2.1 Functional Testing

| Testing Type | Description | Applicable | Coverage |
|--------------|-------------|------------|----------|
| **Smoke Testing** | Verify critical functionalities after each build | Yes | Login, Account creation, Order placement |
| **Sanity Testing** | Quick validation after bug fixes | Yes | Affected functionality |
| **Regression Testing** | Ensure existing functionality is not impacted | Yes | Full regression suite |
| **Integration Testing** | Verify integrations with external systems | Yes | Custodians, OMS, CBS, Chainalysis |
| **End-to-End Testing** | Validate complete business workflows | Yes | All user stories |
| **User Acceptance Testing** | Bank validation of business requirements | Yes | All acceptance criteria |
| **API Testing** | REST API contract validation | Yes | All endpoints |
| **State Transition Testing** | Validate status flow transitions | Yes | Order, Withdrawal, Deposit statuses |

### 4.2.2 Non-Functional Testing

| Testing Type | Description | Applicable | Coverage |
|--------------|-------------|------------|----------|
| **Performance Testing** | Validate API response times, concurrent users | Yes | All critical APIs |
| **Security Testing** | JWT, TLS, injection prevention | Yes | All security requirements |
| **Accessibility Testing** | WCAG compliance | Yes | Customer and Bank User UI |
| **Usability Testing** | User experience evaluation | Yes | Key user journeys |
| **Compatibility Testing** | Cross-browser testing | Yes | Chrome, Firefox, Safari, Edge |
| **Compliance Testing** | KYT/AML/Travel Rule validation | Yes | All compliance workflows |

### Security Testing Details

| Security Test Area | Test Scenarios |
|--------------------|----------------|
| **TLS 1.3 Enforcement** | Verify TLS 1.3 only, reject lower versions |
| **JWT Token Validation** | Valid token, expired token, malformed token, missing claims, invalid signature |
| **RBAC Testing** | Customer role restrictions, Bank user role restrictions, role escalation attempts |
| **Asset-link Control** | Cross-customer access attempts, unauthorized asset access |
| **SQL Injection** | Common injection patterns against all inputs |
| **XSS Prevention** | Script injection in all input fields |
| **CORS Policy** | Cross-origin requests from unauthorized domains |
| **Rate Limiting** | Exceed rate limits, verify throttling behavior |
| **Sensitive Data** | PII not in logs, error masking in responses |

## 4.3 Test Design Techniques

| Technique | Application |
|-----------|-------------|
| **Equivalence Class Partitioning** | Valid/invalid JWT tokens, valid/invalid digital assets, valid/invalid amounts |
| **Boundary Value Analysis** | Trade limits (min, max, boundary), withdrawal limits, amount precision |
| **Decision Table Testing** | Role-based access combinations, order status transitions |
| **State Transition Testing** | Order statuses (Figure 33), Withdrawal statuses (Figure 34), Deposit statuses (Figure 35) |
| **Use Case Testing** | All user stories, end-to-end workflows |
| **Error Guessing** | Edge cases based on domain knowledge |
| **Exploratory Testing** | Unscripted testing for defect discovery |
| **API Contract Testing** | OpenAPI specification validation |

### State Transition Test Coverage

#### Order Status Transitions (Figure 33)
- PENDING → EXECUTED
- PENDING → CANCELLED
- PENDING → FAILED
- All valid and invalid transitions

#### Withdrawal Status Transitions (Figure 34)
- INITIATED → PENDING_KYT
- PENDING_KYT → APPROVED
- PENDING_KYT → REJECTED
- APPROVED → PROCESSING
- PROCESSING → COMPLETED
- PROCESSING → FAILED
- All valid and invalid transitions

#### Deposit Status Transitions (Figure 35)
- DETECTED → PENDING_KYT
- PENDING_KYT → CONFIRMED
- PENDING_KYT → REJECTED
- All valid and invalid transitions

---

# 5. Test Deliverables

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

# 6. Test Environment

## 6.1 Environment Overview

| Environment | Purpose | Infrastructure | Integrations | Refresh Schedule |
|-------------|---------|----------------|--------------|------------------|
| DEV | Development testing | AWS EKS (Dev) | Mocks only | On-demand |
| TEST | System testing | AWS EKS (Test) | Custodian sandbox, OMS test | Weekly |
| STAGING | Pre-production/Integration | AWS EKS (Staging) | All external integrations | Per release |
| UAT | User acceptance testing | AWS EKS (UAT) | All external integrations | Per release |

## 6.2 Environment Requirements

### AWS Infrastructure Requirements

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

### Browser/Client Requirements

| Browser | Version | Primary/Secondary |
|---------|---------|-------------------|
| Chrome | Latest | Primary |
| Firefox | Latest | Secondary |
| Safari | Latest | Secondary (Mac) |
| Edge | Latest | Secondary (Windows) |

### External Integration Requirements

| System | Environment | Connectivity | Purpose |
|--------|-------------|--------------|---------|
| Fireblocks | Sandbox | HTTPS/API | Custodian integration |
| Taurus | Sandbox | HTTPS/API | Custodian integration |
| Wyden | Test | HTTPS/API | OMS integration |
| Chainalysis | Test | HTTPS/API | KYT/AML screening |
| CBS Mock | Test | Internal | Core Banking simulation |

### Access Requirements
- AWS Cognito credentials for test users (Customer and Bank User roles)
- JWT token generation capability with all required claims
- API Gateway access with valid API keys
- Role-based access for different personas

## 6.3 Environment Issues and Escalation

| Issue Type | First Response | Escalation | Timeline |
|------------|----------------|------------|----------|
| Environment down | Notify DevOps | Project Manager | 4 hours |
| External integration failure | Contact vendor | Project Manager | 8 hours |
| Data corruption | Restore from backup | DevOps Lead | 4 hours |
| Security incident | Security Team | CISO | Immediate |

---

# 7. Test Data Management

## 7.1 Test Data Strategy

- Test data will be prepared by the Test Team in coordination with Development
- Sensitive data will be anonymized as per GDPR requirements
- JWT tokens will be generated with all required claims
- Digital assets (BTC, ETH, SHIB) will be configured
- Test customer and bank user accounts will be pre-created

## 7.2 Test Data Requirements

### Authentication Test Data

| Data Type | Value/Format | Purpose |
|-----------|--------------|---------|
| Valid JWT Token | Token with claims: sub, iat, exp, client, customer, role | Happy path authentication |
| Expired JWT Token | Token with past exp timestamp | Token expiration test |
| Invalid JWT Token | Malformed/corrupted token | Security test |
| Missing Claims JWT | Token without customer claim | Validation test |
| Invalid Signature JWT | Token with wrong signature | Security test |
| Customer Role Token | role = "CUSTOMER" | Customer access test |
| Bank User Role Token | role = "BANK_USER" | Bank user access test |

### Business Test Data

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

### Limit Test Data

| Limit Type | Min Value | Max Value | Purpose |
|------------|-----------|-----------|---------|
| Trade Limit (Buy) | 10 EUR | 10,000 EUR | Limit validation |
| Trade Limit (Sell) | 0.001 BTC | 1 BTC | Limit validation |
| Withdrawal Limit | 0.001 ETH | 5 ETH | Limit validation |
| Daily Limit | N/A | 50,000 EUR | Aggregate limit test |

## 7.3 Test Data Refresh

- Test data refresh frequency: Per Sprint
- Refresh process: DocumentDB restore from baseline snapshot
- JWT tokens regenerated as needed
- External system test data coordinated with vendors

---

# 8. Defect Management

## 8.1 Defect Management Process

1. **Identification** – Defect identified during test execution
2. **Logging** – Defect logged in JIRA with all required details
3. **Triage** – Defect reviewed and prioritized in triage meeting
4. **Assignment** – Defect assigned to developer
5. **Resolution** – Developer fixes the defect
6. **Retest** – Tester verifies the fix
7. **Regression** – Verify no side effects
8. **Closure** – Defect closed upon successful verification

## 8.2 Defect Logging Standards

All defects must include:
- **Title:** Clear, concise description (e.g., "JWT validation fails for expired token")
- **Description:** Detailed steps to reproduce
- **Expected Result:** What should happen
- **Actual Result:** What actually happened
- **Environment:** Environment name, browser, API endpoint
- **Attachments:** Screenshots, API responses, logs
- **Severity:** As per definitions below
- **Priority:** As per definitions below
- **Linked User Story:** Reference to requirement
- **Component:** Affected module/service

## 8.3 Defect Severity Definitions

| Severity | Definition | Examples | SLA |
|----------|------------|----------|-----|
| **Critical (S1)** | System unavailable, security breach, data loss | System crash, unauthorized access, payment failure, data corruption | Immediate |
| **High (S2)** | Major functionality impacted, limited workaround | Order execution fails, withdrawal blocked, JWT bypass, KYT screening failure | 4 hours |
| **Medium (S3)** | Moderate impact, workaround available | Non-core functionality issue, UI display issues, minor calculation errors | 24 hours |
| **Low (S4)** | Minor issue, easy workaround | Cosmetic issues, spelling errors, minor UI alignment | Next sprint |

## 8.4 Defect Priority Definitions

| Priority | Definition | Response Time | Fix Timeline |
|----------|------------|---------------|--------------|
| **P1 - Critical** | Must be fixed immediately, blocking release | Immediate | Within 4 hours |
| **P2 - High** | Must be fixed in current sprint | Within 4 hours | Within 24-48 hours |
| **P3 - Medium** | Should be fixed, can be deferred if necessary | Within 24 hours | Within current release |
| **P4 - Low** | Can be fixed in future release | Within 48 hours | Future release |

## 8.5 Defect Triage Process

- **Triage Frequency:** Daily during active testing, twice weekly otherwise
- **Participants:** Test Lead, Dev Lead, BA, Product Owner
- **Agenda:**
  1. Review new defects
  2. Validate severity/priority
  3. Assign owners
  4. Discuss blockers
  5. Review aged defects
  6. Update risk register if needed

---

# 9. Entry and Exit Criteria

## 9.1 Entry Criteria

### Test Execution Entry Criteria

| Category | Criteria | Verification |
|----------|----------|--------------|
| **Environment** | AWS EKS environment stable and available | Health check |
| **Environment** | AWS Cognito configured for authentication | Login test |
| **Environment** | AWS API Gateway deployed and accessible | API health check |
| **Environment** | DocumentDB has seed data loaded | Data verification |
| **Test Data** | JWT tokens (valid, invalid, expired) prepared | Token generation test |
| **Test Data** | Customer and Bank User accounts created | Account verification |
| **Test Data** | Digital assets configured (BTC, ETH, SHIB) | Configuration check |
| **Test Cases** | Test cases reviewed and approved | Sign-off |
| **Build** | Build deployed and smoke tested | Smoke test pass |
| **Defects** | All Critical/High defects from previous phase resolved | Defect report |
| **Integrations** | Custodian sandbox accessible | Integration test |
| **Integrations** | OMS test environment accessible | Integration test |
| **Documentation** | Requirements and design documents available | Document review |

## 9.2 Exit Criteria

### Test Execution Exit Criteria

| Category | Criteria | Target |
|----------|----------|--------|
| **Execution** | All planned test cases executed | 100% |
| **Pass Rate** | Test pass rate meets threshold | ≥95% |
| **Critical Defects** | No open Critical (S1) defects | 0 |
| **High Defects** | Open High (S2) defects | ≤2 (with workarounds) |
| **Security** | All security test cases passed | 100% |
| **Integration** | All integration test cases passed | 100% |
| **Compliance** | All KYT/AML/Travel Rule tests passed | 100% |
| **Documentation** | Test completion report prepared | Approved |
| **Sign-off** | Stakeholder sign-off obtained | Signed |

---

# 10. Test Suspension and Resumption

## 10.1 Suspension Criteria

Testing will be suspended if:
- AWS environment becomes unstable or unavailable (>2 hours)
- Build deployment fails or introduces blocking issues
- More than 30% of test cases fail in smoke testing
- Critical defects block further testing progress
- External integration services unavailable for >4 hours
- Security vulnerabilities discovered requiring immediate attention
- Data breach or compliance violation detected

## 10.2 Resumption Criteria

Testing will resume when:
- Issues causing suspension are resolved
- Environment is restored to stable state
- Sanity testing passes on fixed build (100% pass)
- External integrations are restored
- Security issues are remediated and verified
- Approval received from Test Lead/Manager
- Root cause documented and communicated

---

# 11. Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Test Manager** | Overall test governance, stakeholder management, risk management, resource allocation, compliance oversight |
| **Test Lead** | Test planning, estimation, daily coordination, defect management, reporting, strategy compliance |
| **Test Analyst** | Test scenario/case design, test data preparation, requirement analysis, BA walkthrough |
| **Test Engineer** | Test execution, defect logging, test evidence collection, API testing |
| **Automation Engineer** | Automation framework, regression scripts, CI/CD integration |
| **Performance Tester** | Performance test design, execution, analysis, NFR validation |
| **Security Tester** | Security test design, JWT validation, penetration testing, WAF validation |
| **Compliance Tester** | KYT/AML/Travel Rule testing, regulatory compliance validation |
| **Business Analyst** | Requirements clarification, test scenario review, expectation sheets |
| **Developer** | Defect resolution, test support, technical guidance, unit testing |
| **Product Owner** | Acceptance criteria, UAT execution, sign-off, priority decisions |
| **DevOps Engineer** | Environment setup, deployment, infrastructure support |

---

# 12. Tools and Infrastructure

## 12.1 Test Management Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| JIRA | User story management, defect tracking, sprint management | Daily |
| Confluence | Documentation repository, test evidence storage | Daily |
| Xray for JIRA | Test case management, test execution tracking, traceability | Daily |

## 12.2 Testing Tools

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

## 12.3 Environment Tools

| Tool | Purpose |
|------|---------|
| AWS Console | Environment monitoring, service management |
| kubectl | Kubernetes cluster management |
| Docker | Container management |
| Terraform | Infrastructure as code |

---

# 13. Risk Management

## 13.1 Risk Identification and Mitigation

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy | Owner | Status |
|---------|------------------|-------------|--------|---------------------|-------|--------|
| R001 | AWS environment unavailability | Medium | High | Backup environment, early escalation | DevOps Lead | Open |
| R002 | Delayed requirement delivery | Medium | High | Buffer in schedule, parallel activities | Test Lead | Open |
| R003 | Custodian sandbox unavailability (Fireblocks/Taurus) | Medium | High | Mock services, escalation to vendor | Project Manager | Open |
| R004 | OMS integration issues (Wyden) | Medium | High | Early integration testing, mock services | Test Lead | Open |
| R005 | Test data unavailability | Medium | High | Early data preparation, synthetic data | Test Analyst | Open |
| R006 | Resource unavailability | Medium | Medium | Cross-training, backup resources | Test Manager | Open |
| R007 | Scope changes | Medium | High | Change control process, impact analysis | Project Manager | Open |
| R008 | Security vulnerabilities discovered | Low | Critical | Early security testing, rapid response | Security Lead | Open |
| R009 | Performance issues in API | Medium | High | Early performance testing, optimization | Performance Tester | Open |
| R010 | KYT/AML compliance failure | Low | Critical | Early compliance testing, Chainalysis support | Compliance Tester | Open |
| R011 | JWT token generation issues | Low | High | Pre-generate tokens, Cognito support | Security Team | Open |
| R012 | External vendor response delays | Medium | Medium | SLA agreements, escalation path | Project Manager | Open |

## 13.2 Risk Monitoring

- Risks reviewed in daily standup and weekly status meetings
- Risk register maintained in JIRA/Confluence
- Risk status updated weekly
- Escalation path: Test Lead → Test Manager → Project Manager → Steering Committee

---

# 14. Communication and Reporting

## 14.1 Communication Plan

| Communication | Frequency | Participants | Medium | Purpose |
|---------------|-----------|--------------|--------|---------|
| Daily Standup | Daily | Test Team, Dev Team | Teams/In-person | Status, blockers |
| Test Status Report | Weekly | All stakeholders | Email + Confluence | Progress, metrics |
| Defect Triage | Daily/Twice Weekly | Test Lead, Dev Lead, BA, PO | Meeting | Defect review |
| Sprint Review | End of Sprint | All stakeholders | Meeting | Demo, feedback |
| Risk Review | Weekly | Test Lead, PM | Meeting | Risk updates |
| Steering Committee | Bi-weekly | Leadership | Meeting | Escalations, decisions |

## 14.2 Reporting

### Daily Reports
- Test execution progress (cases executed, passed, failed, blocked)
- Defects raised/closed/reopened
- Blockers and issues
- Environment status

### Weekly Reports
- Test metrics summary
- Defect analysis (by severity, priority, component, trend)
- Risk and issues update
- Upcoming activities and milestones
- Resource utilization

### Metrics Tracked

| Metric | Description | Target | Calculation |
|--------|-------------|--------|-------------|
| Test Execution Progress | % tests executed vs. planned | 100% | Executed / Planned × 100 |
| Test Pass Rate | % tests passed vs. executed | ≥95% | Passed / Executed × 100 |
| Defect Density | Defects per test case | ≤0.1 | Total Defects / Total TCs |
| Defect Resolution Time | Average time to fix defects | ≤2 days (P1/P2) | Sum(Fix Time) / Defect Count |
| Test Coverage | % requirements covered | ≥100% | Covered Reqs / Total Reqs × 100 |
| Automation Coverage | % regression tests automated | ≥70% | Automated / Total Regression × 100 |
| Defect Leakage | Defects found in UAT/Prod | 0 | UAT Defects / Total Defects |
| Blocked Test Ratio | % tests blocked | ≤5% | Blocked / Total × 100 |

---

# 15. Acceptance Criteria Verification

The following acceptance criteria from requirements must be verified:

| ID | Acceptance Criteria | Test Type | Priority |
|----|---------------------|-----------|----------|
| AC01 | Customers can create only one crypto-account per customer | Functional | High |
| AC02 | All orders must pass pre-trade validation (limits, eligibility, balance checks) | Functional | High |
| AC03 | Transactions must be screened for KYT/AML compliance | Compliance | Critical |
| AC04 | API calls must include valid JWT tokens with required attributes | Security | Critical |
| AC05 | Simulation mode available for all state-changing operations | Functional | High |
| AC06 | Idempotency enforced using Idempotency-Key header | Functional | High |
| AC07 | Role-based access control enforced for all operations | Security | Critical |
| AC08 | Asset-link based access control for customer resources | Security | Critical |
| AC09 | Logs must not contain PII - only technical IDs | Compliance | High |
| AC10 | Amount formatting: 2 significant digits minimum | Functional | Medium |
| AC11 | All API communications must use HTTPS with TLS 1.3 | Security | Critical |
| AC12 | Rate limiting and throttling enforced | Security | High |

---

# 16. Appendices

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

## Appendix B – Test Case Life Cycle

| Status | Description |
|--------|-------------|
| **Unexecuted** | Test case not yet executed (default state) |
| **WIP** | Test case execution in progress |
| **Passed** | Test case executed successfully |
| **Failed** | Test case execution failed, defect raised |
| **Blocked** | Cannot be executed due to defect or missing functionality |
| **De-Scoped** | Test case removed from scope |

## Appendix C – API Endpoints Reference

| Method | Endpoint | Description | Auth Required | Idempotent |
|--------|----------|-------------|---------------|------------|
| POST | /accounts | Create account opening request | Yes (Customer) | Yes |
| GET | /accounts | Retrieve account details | Yes | No |
| POST | /orders | Create buy/sell order | Yes (Customer) | Yes |
| GET | /orders | Retrieve orders | Yes | No |
| POST | /transactions | Create deposit/withdrawal | Yes (Customer) | Yes |
| GET | /transactions | Retrieve transactions | Yes | No |
| POST | /bank-user-access-controls | Verify bank user access | Yes (Bank User) | No |

## Appendix D – Error Codes Reference

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

## Appendix E – Business Error Codes

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

## Appendix F – Validation Rules

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

---

# Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Product Owner | | | |
| Business Representative | | | |
| Security Lead | | | |

---

*This Test Strategy document is subject to change based on project requirements and stakeholder feedback.*

**Document Version:** 0.2 (Revised)  
**Generated on:** June 1, 2026
