from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

def add_table(doc, data, bold_header=True):
    """Helper function to add a table with data"""
    if not data:
        return
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.style = 'Table Grid'
    for i, row_data in enumerate(data):
        for j, cell_data in enumerate(row_data):
            table.rows[i].cells[j].text = str(cell_data)
            if bold_header and i == 0:
                for run in table.rows[i].cells[j].paragraphs[0].runs:
                    run.bold = True
    doc.add_paragraph()

def create_scs_test_strategy_v02():
    doc = Document()
    
    # Title
    title = doc.add_heading('Test Strategy for SCS Core (Sopra Crypto Solutions)', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Document info
    doc.add_paragraph()
    add_table(doc, [
        ['Document Version:', '0.2'],
        ['Author:', 'Test Team'],
        ['Role:', 'Test Manager / QA Lead'],
        ['Date:', 'June 1, 2026'],
        ['Status:', 'Draft - Revised']
    ], bold_header=False)
    
    doc.add_paragraph('─' * 60)
    
    # Document Control
    doc.add_heading('Document Control', 1)
    
    doc.add_heading('Revision History', 2)
    add_table(doc, [
        ['Version', 'Date', 'Author', 'Description of Changes'],
        ['0.1', 'June 1, 2026', 'Test Team', 'Initial Draft'],
        ['0.2', 'June 1, 2026', 'Test Team', 'Revised with complete context - added all process flows, validation rules, security features, acceptance criteria']
    ])
    
    doc.add_heading('Document Approval', 2)
    add_table(doc, [
        ['Role', 'Name', 'Signature', 'Date'],
        ['Test Manager', '', '', ''],
        ['Project Manager', '', '', ''],
        ['Product Owner', '', '', ''],
        ['Security Lead', '', '', '']
    ])
    
    # Section 1: Introduction
    doc.add_page_break()
    doc.add_heading('1. Introduction', 1)
    
    doc.add_heading('1.1 Purpose', 2)
    doc.add_paragraph(
        'This document defines the overall testing approach for the SCS Core (Sopra Crypto Solutions) project. '
        'It outlines the testing activities, methodologies, roles and responsibilities, defect management processes, '
        'risk management, stakeholder engagement, and reporting mechanisms.'
    )
    
    doc.add_paragraph('The purpose of this Test Strategy is to:')
    for item in [
        'Document and achieve agreement on the high-level testing approach for SCS Core',
        'Define testing standards and best practices for cryptocurrency/digital asset banking platform',
        'Clarify testing activities and quality assurance processes',
        'Establish clear roles and responsibilities for testing the platform',
        'Ensure compliance with banking regulations (KYT, AML, Travel Rule)'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('1.2 Scope', 2)
    doc.add_paragraph('This Test Strategy covers:')
    for item in [
        'Account Management (creation, retrieval, status updates, one-account-per-customer limit)',
        'Order Management (buy, sell, convert digital assets, order cancellation)',
        'Transaction Management (deposit, withdrawal, internal withdrawal, batch execution for UTXO)',
        'API Security (JWT validation, authentication, authorization, non-repudiation)',
        'Role-Based Access Control (RBAC) and Asset-link based access control',
        'Integration with external services (Custodians, OMS, Exchange venues, KYT/AML providers)',
        'Customer and Bank User Web Interfaces',
        'Compliance features (KYT screening, Travel Rule, AML)',
        'Price Management and Tax Reporting',
        'Bank Position Management and Limit Management'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('1.3 Intended Audience', 2)
    add_table(doc, [
        ['Role', 'Responsibilities'],
        ['Test Lead / Manager', 'Manage testing activities, ensure compliance with strategy'],
        ['Test Engineers', 'Execute test cases, report defects according to defined processes'],
        ['Business Analysts', 'Provide requirements, validate test scenarios'],
        ['Developers', 'Support testing, fix defects, provide technical guidance'],
        ['Product Owner', 'Review and approve testing approach, accept deliverables'],
        ['Project Manager', 'Oversee project delivery, manage risks and escalations'],
        ['Bank Representatives', 'UAT execution and sign-off'],
        ['Security Team', 'Security testing oversight, compliance validation'],
        ['Compliance Team', 'KYT/AML/Travel Rule validation']
    ])
    
    # Section 2: Project Overview
    doc.add_page_break()
    doc.add_heading('2. Project Overview', 1)
    
    doc.add_heading('2.1 Project Background', 2)
    doc.add_paragraph(
        'SCS Core (Sopra Crypto Solutions) is a banking solution that enables banks to deploy a crypto-account '
        'offering for their customers. It provides end-to-end management of digital asset accounts, orders (buy/sell), '
        'transactions (deposits/withdrawals), and integration with custodians, order management systems, and exchange venues.'
    )
    
    doc.add_heading('User Stories Covered', 3)
    add_table(doc, [
        ['User Type', 'User Story'],
        ['Bank Customer', 'Create a crypto-account to hold and manage digital assets'],
        ['Bank Customer', 'Buy digital assets to invest in cryptocurrencies'],
        ['Bank Customer', 'Sell digital assets to convert them to fiat currency'],
        ['Bank Customer', 'Deposit digital assets to transfer them to my account'],
        ['Bank Customer', 'Withdraw digital assets to transfer them to external addresses'],
        ['Bank User', 'Manage customer accounts for support and oversight'],
        ['Bank User', 'View dashboards to monitor bank positions and operations']
    ])
    
    doc.add_heading('2.2 Technology Stack', 2)
    add_table(doc, [
        ['Component', 'Technology', 'Details'],
        ['Frontend', 'Web UI', 'Customer and bank user interfaces'],
        ['Backend', 'AWS EKS', 'Kubernetes microservices architecture'],
        ['Database', 'AWS DocumentDB, S3, EFS', 'Data persistence'],
        ['API Type', 'REST API', 'JSON-based communication'],
        ['Cloud Infrastructure', 'AWS', 'EKS, Cognito, API Gateway, WAF, GuardDuty'],
        ['Container Orchestration', 'Kubernetes', 'Cluster Autoscaler and HPA'],
        ['Authentication', 'AWS Cognito', 'OAuth2, MFA, enterprise SSO'],
        ['Encryption', 'TLS 1.3 / AWS KMS', 'Data in transit and at rest']
    ])
    
    doc.add_heading('2.3 External Integrations', 2)
    add_table(doc, [
        ['Integration Type', 'Provider', 'Purpose'],
        ['Custodians', 'Fireblocks, Taurus', 'Blockchain interactions, wallet management'],
        ['Order Management System', 'Wyden', 'Order routing and execution'],
        ['Exchange Venues', 'Kraken, Coinbase', 'Order execution'],
        ['KYT/AML Provider', 'Chainalysis', 'Transaction screening, compliance'],
        ['Core Banking System', 'Bank CBS', 'Account information, fiat operations']
    ])
    
    # Section 3: Test Scope
    doc.add_page_break()
    doc.add_heading('3. Test Scope', 1)
    
    doc.add_heading('3.1 In Scope - Functional Areas', 2)
    
    doc.add_heading('3.1.1 Account Management', 3)
    add_table(doc, [
        ['Test Area', 'Description', 'Process Flow Reference'],
        ['Account Opening', 'Customer request to open digital asset account', 'Figure 7'],
        ['Dashboard Access', 'Customer accesses digital asset dashboard', 'Figure 8'],
        ['Customer Login', 'Authentication and session management', 'Figure 9'],
        ['One Account Limit', 'Validation of single account per customer', 'Acceptance Criteria']
    ])
    
    doc.add_heading('3.1.2 Order Management', 3)
    add_table(doc, [
        ['Test Area', 'Description', 'Process Flow Reference'],
        ['Buy Order Initiation', 'Customer initiates buying order', 'Figure 10'],
        ['Buy Order Execution', 'End-to-end buy order processing', 'Figure 11'],
        ['Sell Order Initiation', 'Customer initiates selling order', 'Figure 12'],
        ['Sell Order Execution', 'End-to-end sell order processing', 'Figure 13'],
        ['Order Cancellation', 'Customer cancels pending order', 'Figure 22'],
        ['Order Status Transitions', 'All order status states', 'Figure 33'],
        ['Order Integration Module', 'OMS integration testing', 'Figure 27']
    ])
    
    doc.add_heading('3.1.3 Transaction Management', 3)
    add_table(doc, [
        ['Test Area', 'Description', 'Process Flow Reference'],
        ['Deposit Address Request', 'Customer requests new deposit address', 'Figure 14'],
        ['Deposit Receipt', 'Processing incoming deposits', 'Figure 15'],
        ['Whitelisted Address Creation', 'Customer creates whitelisted address', 'Figure 16'],
        ['Withdrawal Initiation', 'Customer initiates withdrawal', 'Figure 17'],
        ['Withdrawal Execution', 'Standard withdrawal processing', 'Figure 18'],
        ['Internal Withdrawal', 'Internal transfer execution', 'Figure 19'],
        ['Account-based Withdrawal', 'Account-based withdrawal execution', 'Figure 20'],
        ['UTXO Batch Execution', 'Batch processing for UTXO assets (BTC)', 'Figure 21'],
        ['Withdrawal Status Transitions', 'All withdrawal status states', 'Figure 34'],
        ['Deposit Status Transitions', 'All deposit status states', 'Figure 35']
    ])
    
    doc.add_heading('3.1.4 Compliance & Monitoring', 3)
    add_table(doc, [
        ['Test Area', 'Description', 'Process Flow Reference'],
        ['Continuous Monitoring', 'Real-time transaction monitoring', 'Figure 23'],
        ['Travel Rule Management', 'Travel Rule data handling', 'Figure 24'],
        ['KYT Task Management', 'KYT screening and task workflows', 'Figure 25'],
        ['KYT Document Upload', 'Document submission for KYT issues', 'Figure 32']
    ])
    
    doc.add_heading('3.1.5 Additional Features', 3)
    add_table(doc, [
        ['Test Area', 'Description', 'Process Flow Reference'],
        ['Price Management', 'Digital asset price retrieval and display', 'Figure 26'],
        ['Limit Management', 'Trade and withdrawal limit updates', 'Figure 28'],
        ['Tax Data Computation', 'Tax-related calculations', 'Figure 29'],
        ['Tax Report Generation', 'Statement and tax report retrieval', 'Figure 30'],
        ['Bank Position Management', 'Bank position creation and monitoring', 'Figure 31']
    ])
    
    doc.add_heading('3.1.6 API Testing Scope', 3)
    add_table(doc, [
        ['Method', 'Endpoint', 'Description', 'Test Focus'],
        ['POST', '/accounts', 'Create account opening request', 'Validation, idempotency, simulation'],
        ['GET', '/accounts', 'Retrieve account details', 'Authorization, pagination'],
        ['POST', '/orders', 'Create buy/sell order', 'Pre-trade validation, limits'],
        ['GET', '/orders', 'Retrieve orders', 'Filtering, pagination'],
        ['POST', '/transactions', 'Create deposit/withdrawal', 'KYT screening, limits'],
        ['GET', '/transactions', 'Retrieve transactions', 'Authorization, filtering'],
        ['POST', '/bank-user-access-controls', 'Verify bank user access', 'RBAC, asset-link control']
    ])
    
    doc.add_heading('3.1.7 Security Testing Scope', 3)
    add_table(doc, [
        ['Security Feature', 'Test Focus'],
        ['JWT Token Validation', 'Token structure, expiration, signature, claims'],
        ['Multi-Factor Authentication', 'MFA flow, bypass attempts'],
        ['OAuth2-based Access', 'Token flow, refresh tokens'],
        ['Role-Based Access Control', 'Role enforcement at UI and API levels'],
        ['Asset-link Based Access', 'Customer can only access own assets'],
        ['Non-repudiation', 'Authorization-Reference header validation'],
        ['TLS 1.3 Encryption', 'Protocol enforcement, certificate validation'],
        ['Rate Limiting', 'Request throttling, burst handling'],
        ['SQL Injection Prevention', 'WAF rules effectiveness'],
        ['XSS Prevention', 'Input sanitization, WAF rules'],
        ['CORS Policy', 'Cross-origin request handling']
    ])
    
    doc.add_heading('3.2 Out of Scope', 2)
    for item in [
        'Core Banking System (CBS) implementation and internal testing',
        'Bank-specific authentication provider implementation',
        'Exchange venue internal logic and testing',
        'Custodian internal security mechanisms',
        'Production infrastructure deployment and verification',
        'Third-party systems not owned by Sopra Steria',
        'Non-supported browsers or legacy environments'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    # Section 4: Test Approach
    doc.add_page_break()
    doc.add_heading('4. Test Approach', 1)
    
    doc.add_heading('4.1 Testing Methodology', 2)
    doc.add_paragraph('The project follows Agile methodology with Sprint-based testing.')
    
    doc.add_heading('Testing Phases', 3)
    add_table(doc, [
        ['Phase', 'Description', 'Entry Criteria', 'Exit Criteria'],
        ['Unit Testing', 'Developer testing', 'Code complete', 'All unit tests pass'],
        ['API Testing', 'REST API validation', 'UT complete', 'All API contracts verified'],
        ['Integration Testing', 'External service integration', 'API testing complete', 'All integrations verified'],
        ['System Testing', 'End-to-end functional testing', 'SIT complete', 'All test cases executed'],
        ['Security Testing', 'JWT, RBAC, encryption validation', 'ST in progress', 'Security requirements met'],
        ['Performance Testing', 'Load and stress testing', 'Core functionality stable', 'Performance targets met'],
        ['Compliance Testing', 'KYT, AML, Travel Rule validation', 'ST complete', 'Compliance requirements met'],
        ['UAT', 'Bank user acceptance testing', 'All testing complete', 'Business sign-off']
    ])
    
    doc.add_heading('4.2 Types of Testing', 2)
    
    doc.add_heading('4.2.1 Functional Testing', 3)
    add_table(doc, [
        ['Testing Type', 'Description', 'Applicable', 'Coverage'],
        ['Smoke Testing', 'Verify critical functionalities after each build', 'Yes', 'Login, Account, Order'],
        ['Sanity Testing', 'Quick validation after bug fixes', 'Yes', 'Affected functionality'],
        ['Regression Testing', 'Ensure existing functionality not impacted', 'Yes', 'Full regression suite'],
        ['Integration Testing', 'Verify integrations with external systems', 'Yes', 'Custodians, OMS, CBS'],
        ['End-to-End Testing', 'Validate complete business workflows', 'Yes', 'All user stories'],
        ['User Acceptance Testing', 'Bank validation of requirements', 'Yes', 'All acceptance criteria'],
        ['API Testing', 'REST API contract validation', 'Yes', 'All endpoints'],
        ['State Transition Testing', 'Validate status flow transitions', 'Yes', 'Order, Withdrawal, Deposit']
    ])
    
    doc.add_heading('4.2.2 Non-Functional Testing', 3)
    add_table(doc, [
        ['Testing Type', 'Description', 'Applicable', 'Coverage'],
        ['Performance Testing', 'Validate API response times', 'Yes', 'All critical APIs'],
        ['Security Testing', 'JWT, TLS, injection prevention', 'Yes', 'All security requirements'],
        ['Accessibility Testing', 'WCAG compliance', 'Yes', 'Customer and Bank User UI'],
        ['Usability Testing', 'User experience evaluation', 'Yes', 'Key user journeys'],
        ['Compatibility Testing', 'Cross-browser testing', 'Yes', 'Chrome, Firefox, Safari, Edge'],
        ['Compliance Testing', 'KYT/AML/Travel Rule validation', 'Yes', 'All compliance workflows']
    ])
    
    doc.add_heading('4.3 Test Design Techniques', 2)
    add_table(doc, [
        ['Technique', 'Application'],
        ['Equivalence Class Partitioning', 'Valid/invalid JWT tokens, digital assets, amounts'],
        ['Boundary Value Analysis', 'Trade limits (min, max), withdrawal limits, precision'],
        ['Decision Table Testing', 'Role-based access combinations, order status transitions'],
        ['State Transition Testing', 'Order statuses (Fig 33), Withdrawal (Fig 34), Deposit (Fig 35)'],
        ['Use Case Testing', 'All user stories, end-to-end workflows'],
        ['Error Guessing', 'Edge cases based on domain knowledge'],
        ['Exploratory Testing', 'Unscripted testing for defect discovery'],
        ['API Contract Testing', 'OpenAPI specification validation']
    ])
    
    # Section 5: Test Deliverables
    doc.add_page_break()
    doc.add_heading('5. Test Deliverables', 1)
    add_table(doc, [
        ['Deliverable', 'Description', 'Owner', 'Timeline'],
        ['Test Strategy', 'High-level testing approach', 'Test Manager', 'Project Start'],
        ['Test Plan', 'Detailed test planning per sprint', 'Test Lead', 'Before Test Design'],
        ['Test Scenarios', 'High-level scenarios for each flow', 'Test Analyst', 'Test Design Phase'],
        ['Test Cases/Scripts', 'Detailed test steps', 'Test Engineer', 'Test Design Phase'],
        ['Test Data', 'JWT tokens, customer data', 'Test Analyst', 'Before Execution'],
        ['API Test Collections', 'Postman collections', 'Test Engineer', 'Test Design Phase'],
        ['Security Test Scripts', 'Security automation scripts', 'Security Tester', 'Test Design Phase'],
        ['Performance Test Scripts', 'JMeter/Gatling scripts', 'Performance Tester', 'Test Design Phase'],
        ['Defect Reports', 'Logged defects', 'Test Engineer', 'During Execution'],
        ['Test Execution Report', 'Daily/Weekly status', 'Test Lead', 'During Execution'],
        ['Test Completion Report', 'Final summary with metrics', 'Test Manager', 'End of Testing'],
        ['Compliance Test Report', 'KYT/AML/Travel Rule results', 'Compliance Tester', 'End of Testing']
    ])
    
    # Section 6: Test Environment
    doc.add_heading('6. Test Environment', 1)
    
    doc.add_heading('6.1 Environment Overview', 2)
    add_table(doc, [
        ['Environment', 'Purpose', 'Infrastructure', 'Integrations', 'Refresh'],
        ['DEV', 'Development testing', 'AWS EKS (Dev)', 'Mocks only', 'On-demand'],
        ['TEST', 'System testing', 'AWS EKS (Test)', 'Custodian sandbox, OMS test', 'Weekly'],
        ['STAGING', 'Pre-production', 'AWS EKS (Staging)', 'All external integrations', 'Per release'],
        ['UAT', 'User acceptance', 'AWS EKS (UAT)', 'All external integrations', 'Per release']
    ])
    
    doc.add_heading('6.2 AWS Infrastructure Requirements', 2)
    add_table(doc, [
        ['Component', 'Specification', 'Purpose'],
        ['AWS EKS', 'Kubernetes cluster', 'Application hosting'],
        ['AWS Cognito', 'Identity provider', 'Authentication, JWT generation'],
        ['AWS API Gateway', 'API management', 'Rate limiting, WAF integration'],
        ['AWS WAF', 'Web application firewall', 'Security rules'],
        ['AWS DocumentDB', 'NoSQL database', 'Data persistence'],
        ['AWS S3', 'Object storage', 'Document storage'],
        ['AWS CloudWatch', 'Monitoring', 'Logging, metrics'],
        ['AWS GuardDuty', 'Threat detection', 'Security monitoring'],
        ['AWS Secrets Manager', 'Secrets management', 'API keys, credentials'],
        ['AWS KMS', 'Key management', 'Encryption keys']
    ])
    
    # Section 7: Test Data Management
    doc.add_page_break()
    doc.add_heading('7. Test Data Management', 1)
    
    doc.add_heading('7.1 Authentication Test Data', 2)
    add_table(doc, [
        ['Data Type', 'Value/Format', 'Purpose'],
        ['Valid JWT Token', 'Token with claims: sub, iat, exp, client, customer, role', 'Happy path'],
        ['Expired JWT Token', 'Token with past exp timestamp', 'Token expiration test'],
        ['Invalid JWT Token', 'Malformed/corrupted token', 'Security test'],
        ['Missing Claims JWT', 'Token without customer claim', 'Validation test'],
        ['Invalid Signature JWT', 'Token with wrong signature', 'Security test'],
        ['Customer Role Token', 'role = "CUSTOMER"', 'Customer access test'],
        ['Bank User Role Token', 'role = "BANK_USER"', 'Bank user access test']
    ])
    
    doc.add_heading('7.2 Business Test Data', 2)
    add_table(doc, [
        ['Data Type', 'Value/Format', 'Purpose'],
        ['Valid Customer ID', 'UUID format', 'Account operations'],
        ['Valid Account ID', 'UUID format', 'Transaction/Order operations'],
        ['Valid Idempotency-Key', 'UUID format', 'Idempotency test'],
        ['Duplicate Idempotency-Key', 'Same UUID as previous', 'Idempotency validation'],
        ['Valid Digital Asset', 'BTC, ETH, SHIB', 'Order creation tests'],
        ['Invalid Digital Asset', 'XYZ (unsupported)', 'Validation test'],
        ['Amount within limits', 'Based on configured limits', 'Happy path'],
        ['Amount exceeding limits', 'Above configured limits', 'Limit validation'],
        ['Amount high precision', '0.00001 SHIB', 'Precision handling'],
        ['simulationIndicator=true', 'Query parameter', 'Simulation mode'],
        ['simulationIndicator=false', 'Query parameter', 'Normal execution'],
        ['Valid whitelisted address', 'Blockchain address', 'Withdrawal test'],
        ['Invalid blockchain address', 'Malformed address', 'Validation test']
    ])
    
    # Section 8: Defect Management
    doc.add_heading('8. Defect Management', 1)
    
    doc.add_heading('8.1 Defect Severity Definitions', 2)
    add_table(doc, [
        ['Severity', 'Definition', 'Examples', 'SLA'],
        ['Critical (S1)', 'System unavailable, security breach', 'System crash, unauthorized access', 'Immediate'],
        ['High (S2)', 'Major functionality impacted', 'Order fails, JWT bypass', '4 hours'],
        ['Medium (S3)', 'Moderate impact, workaround available', 'Non-core issue, UI display', '24 hours'],
        ['Low (S4)', 'Minor issue, easy workaround', 'Cosmetic issues, spelling', 'Next sprint']
    ])
    
    doc.add_heading('8.2 Defect Priority Definitions', 2)
    add_table(doc, [
        ['Priority', 'Definition', 'Response Time', 'Fix Timeline'],
        ['P1 - Critical', 'Must be fixed immediately', 'Immediate', 'Within 4 hours'],
        ['P2 - High', 'Must be fixed in current sprint', 'Within 4 hours', 'Within 24-48 hours'],
        ['P3 - Medium', 'Should be fixed, can be deferred', 'Within 24 hours', 'Within current release'],
        ['P4 - Low', 'Can be fixed in future release', 'Within 48 hours', 'Future release']
    ])
    
    # Section 9: Entry and Exit Criteria
    doc.add_page_break()
    doc.add_heading('9. Entry and Exit Criteria', 1)
    
    doc.add_heading('9.1 Entry Criteria', 2)
    add_table(doc, [
        ['Category', 'Criteria', 'Verification'],
        ['Environment', 'AWS EKS environment stable', 'Health check'],
        ['Environment', 'AWS Cognito configured', 'Login test'],
        ['Environment', 'AWS API Gateway accessible', 'API health check'],
        ['Environment', 'DocumentDB has seed data', 'Data verification'],
        ['Test Data', 'JWT tokens prepared', 'Token generation test'],
        ['Test Data', 'Customer accounts created', 'Account verification'],
        ['Test Data', 'Digital assets configured', 'Configuration check'],
        ['Test Cases', 'Test cases reviewed and approved', 'Sign-off'],
        ['Build', 'Build deployed and smoke tested', 'Smoke test pass'],
        ['Defects', 'Critical/High defects resolved', 'Defect report'],
        ['Integrations', 'Custodian sandbox accessible', 'Integration test'],
        ['Integrations', 'OMS test environment accessible', 'Integration test']
    ])
    
    doc.add_heading('9.2 Exit Criteria', 2)
    add_table(doc, [
        ['Category', 'Criteria', 'Target'],
        ['Execution', 'All planned test cases executed', '100%'],
        ['Pass Rate', 'Test pass rate meets threshold', '≥95%'],
        ['Critical Defects', 'No open Critical (S1) defects', '0'],
        ['High Defects', 'Open High (S2) defects', '≤2 (with workarounds)'],
        ['Security', 'All security test cases passed', '100%'],
        ['Integration', 'All integration tests passed', '100%'],
        ['Compliance', 'All KYT/AML/Travel Rule tests passed', '100%'],
        ['Documentation', 'Test completion report prepared', 'Approved'],
        ['Sign-off', 'Stakeholder sign-off obtained', 'Signed']
    ])
    
    # Section 10: Roles and Responsibilities
    doc.add_heading('10. Roles and Responsibilities', 1)
    add_table(doc, [
        ['Role', 'Responsibilities'],
        ['Test Manager', 'Overall governance, stakeholder management, risk management'],
        ['Test Lead', 'Test planning, estimation, coordination, defect management'],
        ['Test Analyst', 'Test scenario/case design, test data preparation'],
        ['Test Engineer', 'Test execution, defect logging, evidence collection'],
        ['Automation Engineer', 'Automation framework, regression scripts, CI/CD'],
        ['Performance Tester', 'Performance test design, execution, analysis'],
        ['Security Tester', 'Security test design, JWT validation, penetration testing'],
        ['Compliance Tester', 'KYT/AML/Travel Rule testing, regulatory compliance'],
        ['Business Analyst', 'Requirements clarification, test scenario review'],
        ['Developer', 'Defect resolution, test support, technical guidance'],
        ['Product Owner', 'Acceptance criteria, UAT execution, sign-off'],
        ['DevOps Engineer', 'Environment setup, deployment, infrastructure support']
    ])
    
    # Section 11: Tools
    doc.add_page_break()
    doc.add_heading('11. Tools and Infrastructure', 1)
    
    doc.add_heading('11.1 Test Management Tools', 2)
    add_table(doc, [
        ['Tool', 'Purpose', 'Usage'],
        ['JIRA', 'User story management, defect tracking', 'Daily'],
        ['Confluence', 'Documentation repository', 'Daily'],
        ['Xray for JIRA', 'Test case management, execution tracking', 'Daily']
    ])
    
    doc.add_heading('11.2 Testing Tools', 2)
    add_table(doc, [
        ['Tool', 'Purpose', 'Test Type'],
        ['Postman', 'API testing, JWT validation', 'API Testing'],
        ['REST Assured', 'API automation', 'API Automation'],
        ['Selenium / Cypress', 'UI automation', 'UI Automation'],
        ['JMeter', 'Performance testing, load testing', 'Performance'],
        ['Gatling', 'Performance testing, stress testing', 'Performance'],
        ['OWASP ZAP', 'Security scanning', 'Security'],
        ['Burp Suite', 'Security testing, request interception', 'Security'],
        ['AWS CloudWatch', 'Log analysis, monitoring', 'Monitoring']
    ])
    
    # Section 12: Risk Management
    doc.add_heading('12. Risk Management', 1)
    add_table(doc, [
        ['Risk ID', 'Risk Description', 'Probability', 'Impact', 'Mitigation'],
        ['R001', 'AWS environment unavailability', 'Medium', 'High', 'Backup environment, escalation'],
        ['R002', 'Delayed requirement delivery', 'Medium', 'High', 'Buffer in schedule'],
        ['R003', 'Custodian sandbox unavailability', 'Medium', 'High', 'Mock services, vendor escalation'],
        ['R004', 'OMS integration issues', 'Medium', 'High', 'Early integration testing'],
        ['R005', 'Test data unavailability', 'Medium', 'High', 'Early data preparation'],
        ['R006', 'Resource unavailability', 'Medium', 'Medium', 'Cross-training, backup'],
        ['R007', 'Scope changes', 'Medium', 'High', 'Change control process'],
        ['R008', 'Security vulnerabilities', 'Low', 'Critical', 'Early security testing'],
        ['R009', 'Performance issues', 'Medium', 'High', 'Early performance testing'],
        ['R010', 'KYT/AML compliance failure', 'Low', 'Critical', 'Early compliance testing'],
        ['R011', 'JWT token generation issues', 'Low', 'High', 'Pre-generate tokens'],
        ['R012', 'Vendor response delays', 'Medium', 'Medium', 'SLA agreements']
    ])
    
    # Section 13: Communication
    doc.add_heading('13. Communication and Reporting', 1)
    
    doc.add_heading('13.1 Communication Plan', 2)
    add_table(doc, [
        ['Communication', 'Frequency', 'Participants', 'Medium'],
        ['Daily Standup', 'Daily', 'Test Team, Dev Team', 'Teams/In-person'],
        ['Test Status Report', 'Weekly', 'All stakeholders', 'Email + Confluence'],
        ['Defect Triage', 'Daily/Twice Weekly', 'Test Lead, Dev Lead, BA, PO', 'Meeting'],
        ['Sprint Review', 'End of Sprint', 'All stakeholders', 'Meeting'],
        ['Risk Review', 'Weekly', 'Test Lead, PM', 'Meeting'],
        ['Steering Committee', 'Bi-weekly', 'Leadership', 'Meeting']
    ])
    
    doc.add_heading('13.2 Metrics Tracked', 2)
    add_table(doc, [
        ['Metric', 'Description', 'Target', 'Calculation'],
        ['Test Execution Progress', '% tests executed vs. planned', '100%', 'Executed / Planned × 100'],
        ['Test Pass Rate', '% tests passed vs. executed', '≥95%', 'Passed / Executed × 100'],
        ['Defect Density', 'Defects per test case', '≤0.1', 'Defects / Total TCs'],
        ['Defect Resolution Time', 'Average time to fix', '≤2 days', 'Sum(Fix Time) / Count'],
        ['Test Coverage', '% requirements covered', '≥100%', 'Covered / Total × 100'],
        ['Automation Coverage', '% regression automated', '≥70%', 'Automated / Total Reg × 100'],
        ['Defect Leakage', 'Defects found in UAT/Prod', '0', 'UAT Defects / Total'],
        ['Blocked Test Ratio', '% tests blocked', '≤5%', 'Blocked / Total × 100']
    ])
    
    # Section 14: Acceptance Criteria Verification
    doc.add_page_break()
    doc.add_heading('14. Acceptance Criteria Verification', 1)
    add_table(doc, [
        ['ID', 'Acceptance Criteria', 'Test Type', 'Priority'],
        ['AC01', 'Customers can create only one crypto-account', 'Functional', 'High'],
        ['AC02', 'All orders must pass pre-trade validation', 'Functional', 'High'],
        ['AC03', 'Transactions must be screened for KYT/AML', 'Compliance', 'Critical'],
        ['AC04', 'API calls must include valid JWT tokens', 'Security', 'Critical'],
        ['AC05', 'Simulation mode available for state-changing ops', 'Functional', 'High'],
        ['AC06', 'Idempotency enforced using Idempotency-Key', 'Functional', 'High'],
        ['AC07', 'Role-based access control enforced', 'Security', 'Critical'],
        ['AC08', 'Asset-link based access control', 'Security', 'Critical'],
        ['AC09', 'Logs must not contain PII', 'Compliance', 'High'],
        ['AC10', 'Amount formatting: 2 significant digits min', 'Functional', 'Medium'],
        ['AC11', 'All API communications use HTTPS/TLS 1.3', 'Security', 'Critical'],
        ['AC12', 'Rate limiting and throttling enforced', 'Security', 'High']
    ])
    
    # Appendices
    doc.add_page_break()
    doc.add_heading('Appendices', 1)
    
    doc.add_heading('Appendix A – Glossary', 2)
    add_table(doc, [
        ['Term', 'Definition'],
        ['SCS', 'Sopra Crypto Solutions'],
        ['JWT', 'JSON Web Token - authentication token format'],
        ['RBAC', 'Role-Based Access Control'],
        ['KYT', 'Know Your Transaction - compliance checking'],
        ['AML', 'Anti-Money Laundering'],
        ['OMS', 'Order Management System'],
        ['CBS', 'Core Banking System'],
        ['EKS', 'Elastic Kubernetes Service (AWS)'],
        ['HPA', 'Horizontal Pod Autoscaler'],
        ['UAT', 'User Acceptance Testing'],
        ['SIT', 'System Integration Testing'],
        ['NFR', 'Non-Functional Requirements'],
        ['UTXO', 'Unspent Transaction Output (Bitcoin model)'],
        ['MFA', 'Multi-Factor Authentication'],
        ['TLS', 'Transport Layer Security'],
        ['WAF', 'Web Application Firewall'],
        ['PII', 'Personally Identifiable Information'],
        ['GDPR', 'General Data Protection Regulation'],
        ['Fiat', 'Traditional government-issued currency'],
        ['Custodian', 'Entity managing blockchain interactions'],
        ['Whitelisted Address', 'Pre-approved withdrawal destination'],
        ['Travel Rule', 'Regulatory requirement for transaction info sharing']
    ])
    
    doc.add_heading('Appendix B – Test Case Life Cycle', 2)
    add_table(doc, [
        ['Status', 'Description'],
        ['Unexecuted', 'Test case not yet executed (default state)'],
        ['WIP', 'Test case execution in progress'],
        ['Passed', 'Test case executed successfully'],
        ['Failed', 'Test case execution failed, defect raised'],
        ['Blocked', 'Cannot be executed due to defect or missing functionality'],
        ['De-Scoped', 'Test case removed from scope']
    ])
    
    doc.add_heading('Appendix C – API Endpoints Reference', 2)
    add_table(doc, [
        ['Method', 'Endpoint', 'Description', 'Auth Required', 'Idempotent'],
        ['POST', '/accounts', 'Create account opening request', 'Yes (Customer)', 'Yes'],
        ['GET', '/accounts', 'Retrieve account details', 'Yes', 'No'],
        ['POST', '/orders', 'Create buy/sell order', 'Yes (Customer)', 'Yes'],
        ['GET', '/orders', 'Retrieve orders', 'Yes', 'No'],
        ['POST', '/transactions', 'Create deposit/withdrawal', 'Yes (Customer)', 'Yes'],
        ['GET', '/transactions', 'Retrieve transactions', 'Yes', 'No'],
        ['POST', '/bank-user-access-controls', 'Verify bank user access', 'Yes (Bank User)', 'No']
    ])
    
    doc.add_heading('Appendix D – Error Codes Reference', 2)
    add_table(doc, [
        ['HTTP Code', 'Message', 'Description'],
        ['200', 'OK', 'Successful request'],
        ['206', 'Partial Content', 'Results limited due to pagination'],
        ['400', 'Bad Request', 'Invalid input data'],
        ['401', 'Unauthorized', 'Invalid or missing JWT token'],
        ['403', 'Forbidden', 'Access denied'],
        ['404', 'Not Found', 'Resource does not exist'],
        ['429', 'Too Many Requests', 'Rate limit exceeded'],
        ['500', 'Internal Server Error', 'Technical issues'],
        ['502', 'Bad Gateway', 'External service unavailable'],
        ['503', 'Service Unavailable', 'Temporarily unavailable']
    ])
    
    doc.add_heading('Appendix E – Business Error Codes', 2)
    add_table(doc, [
        ['Return Code', 'Description', 'HTTP Status'],
        ['ACCOUNT_ALREADY_EXIST', 'Customer already has an account', '400'],
        ['CUSTODIAN_NOT_AVAILABLE', 'Fireblocks/Taurus API failed', '502'],
        ['INVALID_DIGITAL_ASSET', 'Unsupported digital asset', '400'],
        ['LIMIT_EXCEEDED', 'Trade or withdrawal limit exceeded', '400'],
        ['INSUFFICIENT_BALANCE', 'Insufficient funds', '400'],
        ['KYT_SCREENING_FAILED', 'Transaction failed KYT screening', '403'],
        ['INVALID_ADDRESS', 'Invalid blockchain address', '400'],
        ['ADDRESS_NOT_WHITELISTED', 'Address not whitelisted', '403']
    ])
    
    doc.add_heading('Appendix F – Validation Rules', 2)
    add_table(doc, [
        ['Field', 'Rule', 'Error if Invalid'],
        ['JWT Token', 'Required with valid signature', '401 Unauthorized'],
        ['Idempotency-Key', 'Required for POST, UUID format', '400 Bad Request'],
        ['simulationIndicator', 'Optional, boolean', '400 Bad Request'],
        ['Customer ID', 'Must match JWT claim', '403 Forbidden'],
        ['Account ID', 'Must belong to customer', '403 Forbidden'],
        ['Trade Amount', 'Must be within limits', 'LIMIT_EXCEEDED'],
        ['Withdrawal Amount', 'Must be within limits', 'LIMIT_EXCEEDED'],
        ['Digital Asset', 'Must be in enabled list', 'INVALID_DIGITAL_ASSET'],
        ['Blockchain Address', 'Valid format for asset', 'INVALID_ADDRESS']
    ])
    
    # Sign-Off
    doc.add_page_break()
    doc.add_heading('Sign-Off', 1)
    add_table(doc, [
        ['Role', 'Name', 'Signature', 'Date'],
        ['Test Manager', '', '', ''],
        ['Project Manager', '', '', ''],
        ['Product Owner', '', '', ''],
        ['Business Representative', '', '', ''],
        ['Security Lead', '', '', '']
    ])
    
    doc.add_paragraph()
    doc.add_paragraph('─' * 60)
    para = doc.add_paragraph()
    para.add_run('This Test Strategy document is subject to change based on project requirements and stakeholder feedback.').italic = True
    doc.add_paragraph()
    doc.add_paragraph('Document Version: 0.2 (Revised)')
    doc.add_paragraph('Generated on: June 1, 2026')
    
    # Save the document
    output_path = r'c:\Apparao Maroju\AI-SSI\SCS\SCS-Output\SCS_TestStrategy_v0.2.docx'
    doc.save(output_path)
    print(f'Document saved successfully to: {output_path}')

if __name__ == '__main__':
    create_scs_test_strategy_v02()
