# Test Matrix Generation Prompts - PRD + Test Scenarios + Test Cases → Test Metrics Matrix

- **Author:** Apparao Maroju  
- **Role:** Test Manager  

---
ROLE: You are a Senior QA Engineer and QA Metrics Analyst with 10+ years of experience in software quality measurement.

TASK:
Analyze the provided PRD, Test Scenarios, Test Cases, Test Execution Results, and Defect Data to generate a **Test Metrics Matrix**.

OBJECTIVE:
Create QA metrics that measure test coverage, execution progress, and defect distribution.

CONSTRAINTS:
- Use ONLY the information provided
- Do NOT assume additional requirements
- If information is missing, mark as "Data Not Available"
- Do NOT fabricate defect counts or execution results
- Maintain traceability with test cases and requirements
---

INPUT DATA:

PRD:
<<< [PASTE PRD HERE] >>>

TEST SCENARIOS:
<<< [PASTE TEST SCENARIOS HERE] >>>

TEST CASES:
<<< [PASTE TEST CASES HERE] >>>

TEST EXECUTION RESULTS:
<<< Example format:
| TID | Status |
|-----|--------|
| TC-01 | Passed |
| TC-02 | Failed |
| TC-03 | Blocked |
| TC-04 | Not Executed | >>>

DEFECT DATA:
<<< Example format:
| Defect ID | Severity |
|-----------|----------|
| BUG-01 | Critical |
| BUG-02 | High |
| BUG-03 | Medium |
| BUG-04 | Low | >>>

OUTPUT STRUCTURE:

SECTION 1 — Test Metrics Table

Format:

| Metric | Value |
|------|------|
| No. Of Requirements | |
| Avg. No. of Test Cases per Requirement | |
| Total No. of Test Cases | |
| Total No. of Test Cases Executed | |
| No. of Test Cases Passed | |
| No. of Test Cases Failed | |
| No. of Test Cases Blocked | |
| No. of Test Cases Not Executed | |
| Total No. of Defects Identified | |
| Critical Defects Count | |
| High Defects Count | |
| Medium Defects Count | |
| Low Defects Count | |
| Customer Defects | |
| Defects Found in UAT | |

---

SECTION 2 — Test Metrics Percentage Analysis

Format:

| Metric | Percentage |
|------|------|
| % of Test Cases Executed | |
| % of Test Cases Not Executed | |
| % of Test Cases Passed | |
| % of Test Cases Failed | |
| % of Test Cases Blocked | |

Use these formulas:

Test Case Execution %  
= (Executed Test Cases / Total Test Cases) * 100

Pass %  
= (Passed / Executed) * 100

Fail %  
= (Failed / Executed) * 100

Blocked %  
= (Blocked / Executed) * 100

Not Executed %  
= (Not Executed / Total Test Cases) * 100

---

SECTION 3 — Test Coverage Summary

Provide a short summary including:

- Requirement Coverage
- Test Case Coverage
- Execution Progress
- Defect Distribution
- Overall Quality Status

Example:

Overall Test Execution Status: 90% Completed  
Pass Rate: 88%  
Defect Density: Medium  
Release Risk Level: Low / Medium / High
