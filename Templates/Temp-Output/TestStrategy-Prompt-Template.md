# Test Strategy Generation Prompt Template

Use this prompt template to generate a comprehensive Test Strategy document for any project. Replace the placeholders `{{...}}` with your project-specific information.

---

## Prompt

```
Generate a comprehensive Test Strategy document for {{PROJECT_NAME}} following enterprise testing standards.

## Project Context

**Project Name:** {{PROJECT_NAME}}
**Project Description:** {{BRIEF_PROJECT_DESCRIPTION}}
**Domain:** {{DOMAIN}} (e.g., Banking, Healthcare, E-commerce, Insurance)
**Technology Stack:** {{TECHNOLOGY_STACK}}
**Deployment Platform:** {{DEPLOYMENT_PLATFORM}} (e.g., AWS, Azure, On-premise)

## Key Features to Test

{{LIST_OF_FEATURES}}
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## External Integrations

{{LIST_OF_INTEGRATIONS}}
- Integration 1: Purpose
- Integration 2: Purpose

## Compliance & Regulatory Requirements

{{COMPLIANCE_REQUIREMENTS}}
- Requirement 1
- Requirement 2

## Test Strategy Document Requirements

Generate a Test Strategy document with the following sections:

### 1. Document Control
- Version history table
- Document purpose and scope
- References to related documents
- Distribution list

### 2. Introduction
- Project overview
- Business context
- Testing objectives
- Success criteria

### 3. Scope of Testing
- **In Scope:** Features, integrations, and functionalities to be tested
- **Out of Scope:** Items explicitly excluded from testing
- **Assumptions:** Testing assumptions
- **Constraints:** Testing constraints and limitations

### 4. Test Approach
- Testing methodology (Agile/Waterfall/Hybrid)
- Test levels (Unit, Integration, System, UAT)
- Testing techniques (Black-box, White-box, Gray-box)

### 5. Types of Testing
For each applicable testing type, provide:
- Purpose and scope
- Tools to be used
- Entry/Exit criteria
- Deliverables

Include these testing types as applicable:
- [ ] Functional Testing
- [ ] Integration Testing
- [ ] API Testing
- [ ] Security Testing
- [ ] Performance Testing
- [ ] Regression Testing
- [ ] User Acceptance Testing (UAT)
- [ ] Accessibility Testing
- [ ] Compliance Testing
- [ ] End-to-End Testing

### 6. Test Data Strategy
- Test data requirements
- Data sources (synthetic, anonymized production, mocked)
- Data management approach
- Data refresh strategy

### 7. Entry and Exit Criteria
#### Entry Criteria
- Environment readiness
- Test data availability
- Code deployment status
- Documentation status

#### Exit Criteria
- Test execution completion percentage
- Pass rate thresholds
- Defect resolution requirements
- Sign-off requirements

### 8. Defect Management
- Defect lifecycle workflow
- Defect logging standards
- Severity definitions (S1-S4)
- Priority definitions (P1-P4)
- Triage process

### 9. Roles and Responsibilities
Define responsibilities for:
- Test Manager
- Test Lead
- Test Analyst/Engineer
- Automation Engineer
- Performance Tester
- Security Tester
- Business Analyst
- Developer
- Product Owner

### 10. Test Environment
- Environment architecture
- Environment-specific configurations
- Access requirements
- Refresh schedules

### 11. Test Automation Strategy
- Automation scope and objectives
- Tool selection
- Framework approach
- Automation coverage targets
- CI/CD integration

### 12. Tools and Infrastructure
- Test management tools
- Automation tools
- Performance testing tools
- Security testing tools
- Defect tracking tools
- CI/CD tools

### 13. Risk Management
- Risk identification process
- Risk assessment matrix
- Mitigation strategies
- Contingency planning

### 14. Dependencies
- External system dependencies
- Team dependencies
- Environment dependencies
- Third-party dependencies

### 15. Reporting and Communication
- Status reporting frequency
- Report templates
- Communication channels
- Escalation matrix
- Key metrics to track

### 16. Appendices
Include relevant appendices:
- Appendix A: Defect Priority Definitions
- Appendix B: Defect Severity Definitions
- Appendix C: Test Case Lifecycle
- Appendix D: Error Codes Reference
- Appendix E: Validation Rules
- Appendix F: Glossary
- Appendix G: Process Flow Diagrams (if available)

### Sign-Off Section
Include a sign-off table with columns:
| Role | Name | Signature | Date |

## Output Format

- Generate the document in {{OUTPUT_FORMAT}} format (Markdown / Word / Both)
- Use tables for structured data
- Include clear section numbering
- Maintain professional formatting
```

---

## Example Usage

```
Generate a comprehensive Test Strategy document for SCS Core (Sopra Crypto Solutions) following enterprise testing standards.

## Project Context

**Project Name:** SCS Core
**Project Description:** A cryptocurrency banking solution enabling banks to offer digital asset services to their customers
**Domain:** Banking / FinTech / Cryptocurrency
**Technology Stack:** Java/Spring Boot microservices, REST APIs, AWS EKS, DocumentDB, Redis
**Deployment Platform:** AWS (EKS, Cognito, API Gateway, WAF, CloudWatch, KMS)

## Key Features to Test

- Account Management: Open/close digital asset accounts, KYC verification
- Order Management: Buy/sell digital assets, order lifecycle
- Transaction Management: Deposits, withdrawals, blockchain integration
- Compliance: KYT screening, AML checks, Travel Rule compliance
- Reporting: Tax reports, statements, audit trails

## External Integrations

- Fireblocks/Taurus: Custodian services for blockchain operations
- Wyden: Order Management System
- Chainalysis: KYT and AML compliance screening
- Kraken/Coinbase: Cryptocurrency exchanges

## Compliance & Regulatory Requirements

- KYT (Know Your Transaction) screening
- AML (Anti-Money Laundering) compliance
- Travel Rule data exchange
- GDPR data protection
- MiCA regulations

## Output Format

Generate the document in both Markdown and Word format
```

---

## Tips for Best Results

1. **Be Specific:** Provide detailed project context for more relevant output
2. **List All Features:** Include all features that need testing coverage
3. **Include Integrations:** External systems significantly impact test strategy
4. **Mention Compliance:** Regulatory requirements shape testing approach
5. **Specify Tools:** If you have preferred tools, mention them
6. **Reference Existing Documents:** Point to feature specs, architecture docs if available

---

## Context Files to Attach

For best results, provide these context files along with the prompt:

| File Type | Purpose |
|-----------|---------|
| Project Context | Overall project background, stakeholders, timeline |
| Feature Context | Detailed feature specifications, user stories |
| Testing Context | Existing testing standards, constraints, preferences |
| Architecture Diagram | System architecture and integrations |
| Reference Template | Sample test strategy document to follow |

---

## Customization Options

Add any of these optional sections based on project needs:

- **Localization Testing:** For multi-language support
- **Mobile Testing:** For mobile applications
- **Database Testing:** For data-heavy applications
- **Migration Testing:** For system migrations
- **Disaster Recovery Testing:** For critical systems
- **Load/Stress Testing:** For high-traffic systems
- **Chaos Engineering:** For resilience testing

---

*Template Version: 1.0*  
*Created: June 2026*
