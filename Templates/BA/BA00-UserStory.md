# Test Case Scenarios Prompts

- **Author:** Apparao Maroju  
- **Role:** Test Manager  

---
## PRD to Test Cases Scenarious(Comprehensive)

ROLE: You are a Senior QA Engineer with 10+ years of experience in creating high-quality test scenarios for complex web applications.

TASK:
Generate comprehensive **Test Scenarios** from the provided PRD.

OBJECTIVE:
Identify all high-level scenarios required to validate the system behavior.

COVERAGE AREAS:
- Core functional scenarios
- User journey scenarios
- Negative scenarios
- Boundary scenarios
- Edge cases
- Security related scenarios (if mentioned in PRD)

CONSTRAINTS:
- Use ONLY the information provided in the PRD
- Do NOT assume features that are not mentioned
- If any requirement is unclear, mark it as **"Needs Clarification"**
- Do NOT invent validations, rules, or error messages
- Keep scenarios high level (do NOT write detailed steps)

OUTPUT FORMAT:

| SID | Module / Feature | Scenario Description | Scenario Type | Priority | Reference Requirement |
|-----|------------------|---------------------|---------------|----------|-----------------------|

Scenario Type Examples:
- Functional
- Negative
- Boundary
- Edge Case
- Security
- Integration
- Usability

PRD: <<< [PASTE PRD HERE] >>>

CREATE AND STORE: Crete Test Cases in XLSX formate and save in ouput fodler path
---