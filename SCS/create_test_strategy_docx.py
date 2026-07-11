from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import os

# Image paths
IMAGES_DIR = r'c:\Apparao Maroju\AI-SSI\SCS\SCS-Context\images'

def add_image_if_exists(doc, image_name, caption, width=5.5):
    """Add an image to the document if it exists"""
    image_path = os.path.join(IMAGES_DIR, image_name)
    if os.path.exists(image_path):
        try:
            doc.add_picture(image_path, width=Inches(width))
            last_paragraph = doc.paragraphs[-1]
            last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap = doc.add_paragraph(caption)
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.runs[0].italic = True
            doc.add_paragraph()
            return True
        except Exception as e:
            doc.add_paragraph(f'[Image not available: {image_name}]')
            return False
    else:
        doc.add_paragraph(f'[Image not found: {image_name}]')
        return False

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

def create_scs_test_strategy():
    doc = Document()
    
    # Title
    title = doc.add_heading('Test Strategy', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_heading('SCS Core – Sopra Crypto Solutions', 1)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Document info table
    doc.add_paragraph()
    add_table(doc, [
        ['Document Information', ''],
        ['Project Name:', 'SCS Core (Sopra Crypto Solutions)'],
        ['Document Type:', 'Test Strategy'],
        ['Version:', '0.1'],
        ['Status:', 'Draft'],
        ['Author:', 'Test Team'],
        ['Date:', 'June 1, 2026']
    ], bold_header=False)
    
    doc.add_paragraph('─' * 60)
    
    # Document Control
    doc.add_heading('Document Control', 1)
    
    doc.add_heading('Revision History', 2)
    add_table(doc, [
        ['Version', 'Date', 'Author', 'Description'],
        ['0.1', 'June 1, 2026', 'Test Team', 'Initial Draft']
    ])
    
    doc.add_heading('Document Approval', 2)
    add_table(doc, [
        ['Role', 'Name', 'Signature', 'Date'],
        ['Test Manager', '', '', ''],
        ['Project Manager', '', '', ''],
        ['Product Owner', '', '', ''],
        ['Business Representative', '', '', '']
    ])
    
    doc.add_heading('Distribution List', 2)
    add_table(doc, [
        ['Name', 'Role', 'Organization'],
        ['', 'Test Lead', 'Sopra Steria'],
        ['', 'Product Owner', 'Bank'],
        ['', 'Development Lead', 'Sopra Steria'],
        ['', 'Security Lead', 'Sopra Steria']
    ])
    
    # Section 1: Purpose
    doc.add_page_break()
    doc.add_heading('1. Purpose', 1)
    doc.add_paragraph(
        'This document is the Test Strategy for the SCS Core (Sopra Crypto Solutions) project. '
        'It contains the testing requirements and the high-level approach of testing planned for the project. '
        'The test strategy helps to ensure that testing is carried out systematically based on the agreed testing approach.'
    )
    
    doc.add_paragraph('The purpose of this Test Strategy document is to:')
    for item in [
        'Define overall testing approach that will be taken by the SCS testing team',
        'Document and achieve agreement to the high-level testing approach for testing of SCS Core',
        'Clarify the testing activities, roles and responsibilities, Defect Management, Risk Management',
        'Ensure compliance with banking regulations (KYT, AML, Travel Rule)'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    # Section 2: Intended Audience
    doc.add_heading('2. Intended Audience', 1)
    doc.add_paragraph('This document will be circulated for use by various stakeholders:')
    add_table(doc, [
        ['Role', 'Description'],
        ['Test Manager / Test Lead', 'Manage testing activities, ensure compliance with strategy'],
        ['Test Engineers / QA Team', 'Execute test cases and test governance'],
        ['Business Analysts', 'Provide requirements, validate test scenarios'],
        ['Developers', 'Support testing, fix defects, provide technical guidance'],
        ['Product Owner', 'Review and approve testing approach, accept deliverables'],
        ['Project Manager', 'Oversee project delivery, manage risks and escalations'],
        ['Bank Representatives', 'UAT execution and validation'],
        ['Security Team', 'Security testing oversight, compliance validation'],
        ['Compliance Team', 'KYT/AML/Travel Rule validation']
    ])
    
    # Section 3: Project Overview
    doc.add_page_break()
    doc.add_heading('3. Project Overview', 1)
    
    doc.add_heading('3.1 Business Description', 2)
    doc.add_paragraph(
        'SCS Core (Sopra Crypto Solutions) is a banking solution developed by Sopra Steria that enables banks '
        'to deploy a crypto-account offering for their customers. It provides end-to-end management of digital '
        'asset accounts, orders (buy/sell), transactions (deposits/withdrawals), and integration with custodians, '
        'order management systems, and exchange venues.'
    )
    
    doc.add_heading('3.2 User Stories', 2)
    for story in [
        'As a bank customer, I want to create a crypto-account so that I can hold and manage digital assets',
        'As a bank customer, I want to buy digital assets so that I can invest in cryptocurrencies',
        'As a bank customer, I want to sell digital assets so that I can convert them to fiat currency',
        'As a bank customer, I want to deposit digital assets so that I can transfer them to my account',
        'As a bank customer, I want to withdraw digital assets so that I can transfer them to external addresses',
        'As a bank user, I want to manage customer accounts so that I can provide support and oversight',
        'As a bank user, I want to view dashboards so that I can monitor bank positions and operations'
    ]:
        doc.add_paragraph(story, style='List Bullet')
    
    doc.add_heading('3.3 Technology Stack', 2)
    add_table(doc, [
        ['Component', 'Technology'],
        ['Frontend', 'Web UI (customer and bank user interfaces)'],
        ['Backend', 'AWS EKS (Kubernetes microservices architecture)'],
        ['Database', 'AWS DocumentDB, S3, EFS'],
        ['API Type', 'REST API'],
        ['Cloud Infrastructure', 'AWS (EKS, Cognito, API Gateway, WAF, GuardDuty)'],
        ['Container Orchestration', 'Kubernetes with Cluster Autoscaler and HPA'],
        ['Authentication', 'AWS Cognito with OAuth2, MFA, enterprise SSO'],
        ['Encryption', 'TLS 1.3 for data in transit, AWS KMS for data at rest']
    ])
    
    doc.add_heading('3.4 External Integrations', 2)
    add_table(doc, [
        ['System', 'Provider', 'Purpose'],
        ['Custodians', 'Fireblocks, Taurus', 'Blockchain interactions, wallet management'],
        ['Order Management System', 'Wyden', 'Order routing and execution'],
        ['Exchange Venues', 'Kraken, Coinbase', 'Order execution'],
        ['KYT/AML Provider', 'Chainalysis', 'Transaction screening, compliance'],
        ['Core Banking System', 'Bank CBS', 'Account information, fiat operations']
    ])
    
    # Section 4: Project Scope
    doc.add_page_break()
    doc.add_heading('4. Project Scope', 1)
    
    doc.add_heading('4.1 In Scope', 2)
    
    doc.add_heading('4.1.1 Account Management', 3)
    add_table(doc, [
        ['Test Area', 'Process Flow Reference'],
        ['Customer request to open digital asset account', 'Figure 7'],
        ['Customer accesses digital asset dashboard', 'Figure 8'],
        ['Customer login', 'Figure 9'],
        ['One account per customer limit validation', 'Acceptance Criteria']
    ])
    
    doc.add_heading('4.1.2 Order Management', 3)
    add_table(doc, [
        ['Test Area', 'Process Flow Reference'],
        ['Initiation of buying order', 'Figure 10'],
        ['Execution of buying order', 'Figure 11'],
        ['Initiation of selling order', 'Figure 12'],
        ['Execution of selling order', 'Figure 13'],
        ['Customer request cancellation of order', 'Figure 22'],
        ['Order Integration Module', 'Figure 27'],
        ['Order status transitions', 'Figure 33']
    ])
    
    doc.add_heading('4.1.3 Transaction Management', 3)
    add_table(doc, [
        ['Test Area', 'Process Flow Reference'],
        ['New deposit address request', 'Figure 14'],
        ['Deposit receipt', 'Figure 15'],
        ['Whitelisted address creation', 'Figure 16'],
        ['Customer initiates withdrawal', 'Figure 17'],
        ['Withdrawal execution', 'Figure 18'],
        ['Internal withdrawal execution', 'Figure 19'],
        ['Account-based withdrawal execution', 'Figure 20'],
        ['Batch execution for UTXO assets (BTC)', 'Figure 21'],
        ['Withdrawal status transitions', 'Figure 34'],
        ['Deposit status transitions', 'Figure 35']
    ])
    
    doc.add_heading('4.1.4 Compliance & Monitoring', 3)
    add_table(doc, [
        ['Test Area', 'Process Flow Reference'],
        ['Continuous monitoring', 'Figure 23'],
        ['Travel Rule data management', 'Figure 24'],
        ['KYT Task Management', 'Figure 25'],
        ['Document upload for KYT issue', 'Figure 32']
    ])
    
    doc.add_heading('4.1.5 Additional Features', 3)
    add_table(doc, [
        ['Test Area', 'Process Flow Reference'],
        ['Price management', 'Figure 26'],
        ['Limit update management', 'Figure 28'],
        ['Tax-related data computation', 'Figure 29'],
        ['Tax reports / Statement report generation', 'Figure 30'],
        ['Create bank position', 'Figure 31']
    ])
    
    doc.add_heading('4.1.6 Security Testing', 3)
    for item in [
        'TLS 1.3 enforcement validation',
        'JWT token validation (structure, claims, expiration, signature)',
        'SQL injection and XSS attack prevention (WAF rules)',
        'CORS policy enforcement',
        'Rate limiting effectiveness',
        'Unauthorized access attempts (cross-customer access)',
        'Role-Based Access Control (RBAC)',
        'Asset-link based access control'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('4.1.7 API Testing', 3)
    add_table(doc, [
        ['Method', 'Endpoint', 'Description'],
        ['POST', '/accounts', 'Create account opening request'],
        ['GET', '/accounts', 'Retrieve account details'],
        ['POST', '/orders', 'Create buy/sell order'],
        ['GET', '/orders', 'Retrieve orders'],
        ['POST', '/transactions', 'Create deposit/withdrawal transaction'],
        ['GET', '/transactions', 'Retrieve transactions'],
        ['POST', '/bank-user-access-controls', 'Verify bank user access']
    ])
    
    doc.add_heading('4.2 Out of Scope', 2)
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
    
    doc.add_heading('4.3 Assumptions', 2)
    for item in [
        'Requirements are documented in the SCS Reference Document',
        'Test environments will be available as per schedule with AWS infrastructure',
        'Test data will be prepared including JWT tokens with all required claims',
        'Custodian sandbox/test environments (Fireblocks, Taurus) will be available',
        'OMS test environment (Wyden) will be accessible',
        'Mock services for CBS API endpoints will be provided',
        'Chainalysis test environment will be available for KYT testing',
        'Digital assets (BTC, ETH, SHIB) will be configured in test environment'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('4.4 Dependencies', 2)
    add_table(doc, [
        ['Dependency', 'Owner', 'Impact if Not Met'],
        ['AWS Environment (EKS, Cognito, API Gateway)', 'DevOps Team', 'Testing cannot proceed'],
        ['Custodian Test Environment', 'External Vendor', 'Integration testing blocked'],
        ['OMS Test Environment (Wyden)', 'External Vendor', 'Order execution testing blocked'],
        ['Chainalysis Test Environment', 'External Vendor', 'KYT/AML testing blocked'],
        ['DocumentDB with seed data', 'DevOps Team', 'Test data unavailable'],
        ['JWT Token generation capability', 'Security Team', 'Authentication testing blocked'],
        ['CBS Mock Services', 'Development Team', 'CBS integration testing blocked']
    ])
    
    # Section 5: Testing Approach
    doc.add_page_break()
    doc.add_heading('5. Testing Approach', 1)
    
    doc.add_heading('5.1 Testing Methodology', 2)
    doc.add_paragraph(
        'SCS project is being run in Agile SCRUM methodology. The project is divided into sprints of 2-3 weeks each.'
    )
    
    doc.add_heading('Sprint Testing Process', 3)
    for item in [
        'Scope Freeze – Pre-condition phase to have better quality',
        'Sprint Planning – Sprint plans are created for completing product backlog items',
        'Test Case Creation + BA Review – Detailed test cases are created and reviewed',
        'Test Execution and Bug Fixing – Execution is performed and fixing is done',
        'Sprint Retrospective – Lessons learned are captured'
    ]:
        doc.add_paragraph(item, style='List Number')
    
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
    
    doc.add_heading('5.2 Types of Testing', 2)
    
    doc.add_heading('5.2.1 Functional Testing', 3)
    add_table(doc, [
        ['Testing Type', 'Description', 'Coverage'],
        ['Smoke Testing', 'Verify critical functionalities after each build', 'Login, Account, Order'],
        ['Sanity Testing', 'Quick validation after bug fixes', 'Affected functionality'],
        ['Regression Testing', 'Ensure existing functionality is not impacted', 'Full regression suite'],
        ['Integration Testing', 'Verify integrations with external systems', 'Custodians, OMS, CBS'],
        ['End-to-End Testing', 'Validate complete business workflows', 'All user stories'],
        ['User Acceptance Testing', 'Bank validation of business requirements', 'All acceptance criteria'],
        ['API Testing', 'REST API contract validation', 'All endpoints'],
        ['State Transition Testing', 'Validate status flow transitions', 'Order, Withdrawal, Deposit']
    ])
    
    doc.add_heading('5.2.2 Non-Functional Testing', 3)
    add_table(doc, [
        ['Testing Type', 'Description', 'Coverage'],
        ['Performance Testing', 'Validate API response times', 'All critical APIs'],
        ['Security Testing', 'JWT, TLS, injection prevention', 'All security requirements'],
        ['Accessibility Testing', 'WCAG compliance', 'Customer and Bank User UI'],
        ['Usability Testing', 'User experience evaluation', 'Key user journeys'],
        ['Compatibility Testing', 'Cross-browser testing', 'Chrome, Firefox, Safari, Edge'],
        ['Compliance Testing', 'KYT/AML/Travel Rule validation', 'All compliance workflows']
    ])
    
    doc.add_heading('5.3 Test Design Techniques', 2)
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
    
    # Section 6: Test Deliverables
    doc.add_page_break()
    doc.add_heading('6. Test Deliverables', 1)
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
    
    # Section 7: Entry and Exit Criteria
    doc.add_heading('7. Entry and Exit Criteria', 1)
    
    doc.add_heading('7.1 Entry Criteria', 2)
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
        ['Defects', 'Severity 1/2 defects resolved', 'Defect report'],
        ['Integrations', 'Custodian sandbox accessible', 'Integration test'],
        ['Integrations', 'OMS test environment accessible', 'Integration test']
    ])
    
    doc.add_heading('7.2 Exit Criteria', 2)
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
    
    # Section 8: Defect Management
    doc.add_page_break()
    doc.add_heading('8. Defect Management', 1)
    
    doc.add_heading('8.1 Defect Management Process', 2)
    doc.add_paragraph(
        'The standard Sopra Steria defect management process will be followed. The Test Lead will perform '
        'the role of Defect Manager. The purpose is to manage recording, tracking, progression and fixing '
        'of defects found during testing.'
    )
    
    doc.add_heading('Defect Workflow', 3)
    for item in [
        'Identification – Defect identified during test execution',
        'Logging – Defect logged in JIRA with all required details',
        'Triage – Defect reviewed and prioritized in triage meeting',
        'Assignment – Defect assigned to developer',
        'Resolution – Developer fixes the defect',
        'Retest – Tester verifies the fix',
        'Regression – Verify no side effects',
        'Closure – Defect closed upon successful verification'
    ]:
        doc.add_paragraph(item, style='List Number')
    
    doc.add_heading('8.2 Defect Logging Standards', 2)
    doc.add_paragraph('All defects must include:')
    for item in [
        'Title: Clear, concise description',
        'Description: Detailed steps to reproduce',
        'Expected Result: What should happen',
        'Actual Result: What actually happened',
        'Environment: Environment name, browser, API endpoint',
        'Attachments: Screenshots, API responses, logs',
        'Severity: As per definitions',
        'Priority: As per definitions',
        'Linked User Story: Reference to requirement'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('8.3 Defect Triage', 2)
    doc.add_paragraph(
        'A defect triage meeting will be scheduled twice weekly to discuss progress of defects, '
        'identify which defects should be fixed first and discuss blockers.'
    )
    doc.add_paragraph('Participants: Test Lead, Dev Lead, BA, Product Owner')
    
    # Section 9: Roles and Responsibilities
    doc.add_heading('9. Roles and Responsibilities', 1)
    add_table(doc, [
        ['Role', 'Responsibilities'],
        ['Test Manager', 'Project oversight, compliance with Test Strategy, testing schedule'],
        ['Test Lead', 'Compliance with Test Plan, defect management, issue resolution'],
        ['Test Analyst', 'Testing scope agreement, estimates, test case development'],
        ['Test Engineer', 'Test execution, defect logging, evidence collection'],
        ['Automation Engineer', 'Automation framework, script development and maintenance'],
        ['Performance Tester', 'Performance test design, execution, analysis'],
        ['Security Tester', 'Security test design, JWT validation, penetration testing'],
        ['Business Analyst', 'Requirements clarification, test scenario review'],
        ['Developer', 'Defect resolution, test support, technical guidance'],
        ['Product Owner', 'Acceptance criteria, UAT execution, sign-off'],
        ['DevOps Engineer', 'Environment setup, deployment, infrastructure support']
    ])
    
    # Section 10: Test Environment
    doc.add_page_break()
    doc.add_heading('10. Test Environment', 1)
    
    doc.add_heading('10.1 Environment Overview', 2)
    add_table(doc, [
        ['Environment', 'Purpose', 'Infrastructure', 'Integrations', 'Refresh'],
        ['DEV', 'Development testing', 'AWS EKS (Dev)', 'Mocks only', 'On-demand'],
        ['TEST', 'System testing', 'AWS EKS (Test)', 'Custodian sandbox, OMS test', 'Weekly'],
        ['STAGING', 'Pre-production', 'AWS EKS (Staging)', 'All external integrations', 'Per release'],
        ['UAT', 'User acceptance', 'AWS EKS (UAT)', 'All external integrations', 'Per release']
    ])
    
    doc.add_heading('10.2 AWS Infrastructure Requirements', 2)
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
    
    doc.add_heading('10.3 Browser/Client Requirements', 2)
    add_table(doc, [
        ['Browser', 'Version', 'Primary/Secondary'],
        ['Chrome', 'Latest', 'Primary'],
        ['Firefox', 'Latest', 'Secondary'],
        ['Safari', 'Latest', 'Secondary (Mac)'],
        ['Edge', 'Latest', 'Secondary (Windows)']
    ])
    
    doc.add_heading('10.4 External Integration Environments', 2)
    add_table(doc, [
        ['System', 'Environment', 'Connectivity', 'Purpose'],
        ['Fireblocks', 'Sandbox', 'HTTPS/API', 'Custodian integration'],
        ['Taurus', 'Sandbox', 'HTTPS/API', 'Custodian integration'],
        ['Wyden', 'Test', 'HTTPS/API', 'OMS integration'],
        ['Chainalysis', 'Test', 'HTTPS/API', 'KYT/AML screening'],
        ['CBS Mock', 'Test', 'Internal', 'Core Banking simulation']
    ])
    
    # Section 11: Test Data
    doc.add_heading('11. Test Data', 1)
    
    doc.add_heading('11.1 Test Data Strategy', 2)
    for item in [
        'Sensitive data will be anonymized as per GDPR requirements',
        'JWT tokens will be generated with all required claims',
        'Digital assets (BTC, ETH, SHIB) will be configured',
        'Test customer and bank user accounts will be pre-created'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('11.2 Authentication Test Data', 2)
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
    
    doc.add_heading('11.3 Business Test Data', 2)
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
        ['simulationIndicator=true', 'Query parameter', 'Simulation mode'],
        ['simulationIndicator=false', 'Query parameter', 'Normal execution'],
        ['Valid whitelisted address', 'Blockchain address', 'Withdrawal test'],
        ['Invalid blockchain address', 'Malformed address', 'Validation test']
    ])
    
    # Section 12: Test Tools
    doc.add_page_break()
    doc.add_heading('12. Test Tools', 1)
    
    doc.add_heading('12.1 Test Management Tools', 2)
    add_table(doc, [
        ['Tool', 'Purpose', 'Usage'],
        ['JIRA', 'User story management, defect tracking', 'Daily'],
        ['Confluence', 'Documentation repository', 'Daily'],
        ['Xray for JIRA', 'Test case management, execution tracking', 'Daily']
    ])
    
    doc.add_heading('12.2 Testing Tools', 2)
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
    
    # Section 13: Test Suspension and Resumption
    doc.add_heading('13. Test Suspension and Resumption', 1)
    
    doc.add_heading('13.1 Suspension Criteria', 2)
    doc.add_paragraph('Testing will be suspended if:')
    for item in [
        'Any eventuality which results in the Test environment becoming unstable',
        'There are issues in the deployment of the build',
        'More than 30% of test cases fail in smoke testing',
        'Critical defects block further testing progress',
        'External integration services unavailable for >4 hours',
        'Security vulnerabilities discovered requiring immediate attention',
        'Data breach or compliance violation detected'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('13.2 Resumption Criteria', 2)
    doc.add_paragraph('Testing will resume when:')
    for item in [
        'Issues causing suspension are resolved',
        'Environment is rolled back to previous acceptable state',
        'Sanity testing passes on fixed build (100% pass)',
        'External integrations are restored',
        'Security issues are remediated and verified',
        'Approval received from Test Lead/Manager',
        'Root cause documented and communicated'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    # Section 14: Risk Management
    doc.add_heading('14. Risk Management', 1)
    
    doc.add_heading('14.1 Risk Identification and Mitigation', 2)
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
    
    doc.add_heading('14.2 Risk Monitoring', 2)
    for item in [
        'All project related risks will be maintained in Risk Register',
        'Risks reviewed in weekly testing progress meetings',
        'Risk status updated weekly',
        'Escalation path: Test Lead → Test Manager → Project Manager → Steering Committee'
    ]:
        doc.add_paragraph(item, style='List Bullet')
    
    # Section 15: Reporting and Communication
    doc.add_page_break()
    doc.add_heading('15. Reporting and Communication', 1)
    
    doc.add_heading('15.1 Communication Plan', 2)
    add_table(doc, [
        ['Communication', 'Frequency', 'Participants', 'Medium'],
        ['Daily Standup', 'Daily', 'Test Team, Dev Team', 'Teams/In-person'],
        ['Test Status Report', 'Weekly', 'All stakeholders', 'Email + Confluence'],
        ['Defect Triage', 'Twice Weekly', 'Test Lead, Dev Lead, BA, PO', 'Meeting'],
        ['Sprint Review', 'End of Sprint', 'All stakeholders', 'Meeting'],
        ['Risk Review', 'Weekly', 'Test Lead, PM', 'Meeting'],
        ['Steering Committee', 'Bi-weekly', 'Leadership', 'Meeting']
    ])
    
    doc.add_heading('15.2 Metrics Tracked', 2)
    add_table(doc, [
        ['Metric', 'Description', 'Target'],
        ['Test Execution Progress', '% tests executed vs. planned', '100%'],
        ['Test Pass Rate', '% tests passed vs. executed', '≥95%'],
        ['Defect Density', 'Defects per test case', '≤0.1'],
        ['Defect Resolution Time', 'Average time to fix defects', '≤2 days (P1/P2)'],
        ['Test Coverage', '% requirements covered', '≥100%'],
        ['Automation Coverage', '% regression tests automated', '≥70%'],
        ['Defect Leakage', 'Defects found in UAT/Prod', '0'],
        ['Blocked Test Ratio', '% tests blocked', '≤5%']
    ])
    
    # Appendices
    doc.add_page_break()
    doc.add_heading('16. Appendices', 1)
    
    doc.add_heading('Appendix A – Defect Priority Definitions', 2)
    doc.add_paragraph(
        'Priority is about how important it is to the business to fix the problem. Priority is assigned '
        'to a defect to help designate the order in which defects should be fixed.'
    )
    add_table(doc, [
        ['Priority', 'Definition', 'Response Time', 'Fix Timeline'],
        ['P1 - Critical', 'System cannot go live. Many test cases blocked.', 'Immediate', 'Within 4 hours'],
        ['P2 - High', 'Significant impact. Material impact on customer service.', 'Within 4 hours', 'Within 24-48 hours'],
        ['P3 - Medium', 'Moderate impact. Not enough to prevent going live.', 'Within 24 hours', 'Within current release'],
        ['P4 - Low', 'No significant impact. Minor or no impact to plan.', 'Within 48 hours', 'Future release']
    ])
    
    doc.add_heading('Appendix B – Defect Severity Definitions', 2)
    doc.add_paragraph('Severity is a measure of the technical impact on the system if the defect was introduced.')
    add_table(doc, [
        ['Severity', 'Definition', 'Examples'],
        ['S1 - Critical', 'Show-stopper. System unavailable. No workaround.', 'System crash, unauthorized access'],
        ['S2 - High', 'Substantial loss of function. Inoperable for majority cases.', 'Order fails, JWT bypass'],
        ['S3 - Medium', 'Minor loss of functionality. Reasonable workaround available.', 'Non-core issues, UI display'],
        ['S4 - Low', 'Easy workaround. Cosmetic problems.', 'Spelling errors, minor alignment']
    ])
    
    doc.add_heading('Appendix C – Test Case Life Cycle', 2)
    add_table(doc, [
        ['Status', 'Description'],
        ['Unexecuted', 'Default status when test case is added'],
        ['WIP', 'Tester has picked up test case for execution'],
        ['Passed', 'Expected result matches actual result'],
        ['Failed', 'Expected result does not match actual result'],
        ['Blocked', 'Cannot execute due to defect or missing functionality'],
        ['De-Scoped', 'Functionality obsolete or removed']
    ])
    
    doc.add_heading('Appendix D – API Error Codes Reference', 2)
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
    
    doc.add_heading('Appendix G – Glossary', 2)
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
    
    # Appendix H - Process Flow Diagrams with Images
    doc.add_page_break()
    doc.add_heading('Appendix H – Process Flow Diagrams', 2)
    
    # Architecture Diagrams
    doc.add_heading('Architecture Diagrams', 3)
    add_image_if_exists(doc, 'image_1.png', 'Figure 1 - Overview of the Solution')
    add_image_if_exists(doc, 'image_2.png', 'Figure 2 - Capability Map')
    add_image_if_exists(doc, 'image_3.png', 'Figure 3 - Subledger Concepts')
    add_image_if_exists(doc, 'image_4.png', 'Figure 4 - Application Architecture')
    add_image_if_exists(doc, 'image_5.png', 'Figure 5 - Deployment')
    add_image_if_exists(doc, 'image_6.png', 'Figure 6 - Link Components vs Capabilities')
    
    # Account Management Process Flows
    doc.add_page_break()
    doc.add_heading('Account Management Process Flows', 3)
    add_image_if_exists(doc, 'image_7.png', 'Figure 7 - Customer Request to Open a Digital Asset Account')
    add_image_if_exists(doc, 'image_8.png', 'Figure 8 - Customer Accesses a Digital Asset Dashboard')
    add_image_if_exists(doc, 'image_9.png', 'Figure 9 - Customer Logs In')
    
    # Order Management Process Flows
    doc.add_page_break()
    doc.add_heading('Order Management Process Flows', 3)
    add_image_if_exists(doc, 'image_10.png', 'Figure 10 - Initiation of the Buying Order')
    add_image_if_exists(doc, 'image_12.png', 'Figure 11 - Execution of a Buying Order')
    add_image_if_exists(doc, 'image_13.png', 'Figure 12 - Initiation of a Selling Order')
    add_image_if_exists(doc, 'image_14.png', 'Figure 13 - Execution of a Selling Order')
    add_image_if_exists(doc, 'image_22.png', 'Figure 22 - Customer Request Cancellation of an Order')
    add_image_if_exists(doc, 'image_27.png', 'Figure 27 - Order Integration Module')
    
    # Transaction Management Process Flows
    doc.add_page_break()
    doc.add_heading('Transaction Management Process Flows', 3)
    add_image_if_exists(doc, 'image_15.png', 'Figure 14 - New Deposit Address Request')
    add_image_if_exists(doc, 'image_16.png', 'Figure 15 - Deposit Receipt')
    add_image_if_exists(doc, 'image_17.png', 'Figure 16 - Whitelisted Address Creation')
    add_image_if_exists(doc, 'image_18.png', 'Figure 17 - Customer Initiates Withdrawal')
    add_image_if_exists(doc, 'image_19.png', 'Figure 18 - Withdrawal Execution')
    add_image_if_exists(doc, 'image_20.png', 'Figure 19 - Internal Withdrawal Execution')
    add_image_if_exists(doc, 'image_21.png', 'Figure 20 - Account-based Withdrawal Execution')
    
    # Compliance & Monitoring Process Flows
    doc.add_page_break()
    doc.add_heading('Compliance & Monitoring Process Flows', 3)
    add_image_if_exists(doc, 'image_23.png', 'Figure 23 - Continuous Monitoring')
    add_image_if_exists(doc, 'image_24.png', 'Figure 24 - Travel Rule Data Management')
    add_image_if_exists(doc, 'image_25.png', 'Figure 25 - KYT Task Management')
    add_image_if_exists(doc, 'image_32.png', 'Figure 32 - Document Upload for KYT Issue')
    
    # Additional Feature Process Flows
    doc.add_page_break()
    doc.add_heading('Additional Feature Process Flows', 3)
    add_image_if_exists(doc, 'image_26.png', 'Figure 26 - Price Management')
    add_image_if_exists(doc, 'image_28.png', 'Figure 28 - Limit Update Management')
    add_image_if_exists(doc, 'image_29.png', 'Figure 29 - Tax-related Data Computation')
    add_image_if_exists(doc, 'image_30.png', 'Figure 30 - Retrieve Tax Reports / Statement Report Generation')
    add_image_if_exists(doc, 'image_31.png', 'Figure 31 - Create Bank Position')
    
    # Status Flow Diagrams
    doc.add_page_break()
    doc.add_heading('Status Flow Diagrams', 3)
    add_image_if_exists(doc, 'image_45.png', 'Figure 33 - Buy/Sell Order Statuses')
    add_image_if_exists(doc, 'image_46.png', 'Figure 34 - Withdrawal Statuses')
    add_image_if_exists(doc, 'image_54.png', 'Figure 35 - Deposit Statuses')
    
    # Infrastructure Diagrams
    doc.add_page_break()
    doc.add_heading('Infrastructure Diagrams', 3)
    add_image_if_exists(doc, 'image_48.png', 'Figure 36 - Architecture Principles')
    add_image_if_exists(doc, 'image_49.png', 'Figure 37 - Technology Stack')
    add_image_if_exists(doc, 'image_50.png', 'Figure 38 - Current Infrastructure')
    add_image_if_exists(doc, 'image_51.png', 'Figure 39 - Target Infrastructure')
    add_image_if_exists(doc, 'image_52.png', 'Figure 40 - Cluster Autoscaler')
    add_image_if_exists(doc, 'image_53.png', 'Figure 41 - Horizontal Pod Autoscaler')
    
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
    doc.add_paragraph('Document Version: 0.1')
    doc.add_paragraph('Generated on: June 1, 2026')
    
    # Save the document
    output_path = r'c:\Apparao Maroju\AI-SSI\SCS\SCS-Output\SCS_Test_Strategy_F_v0.2.docx'
    doc.save(output_path)
    print(f'Document saved successfully to: {output_path}')

if __name__ == '__main__':
    create_scs_test_strategy()
