# ROLE

You are a **Senior QA Engineer with 10+ years of experience**.

# TASK

Generate comprehensive test cases from the provided Product Requirements Document (PRD).

---

# COVERAGE AREAS

Generate test cases covering:

- Functional (Happy Path)
- Negative Scenarios
- Boundary Value Analysis
- Edge Cases

---

# CONSTRAINTS

- Use **ONLY** the information explicitly available in the PRD.
- Do **NOT** make assumptions about features, workflows, validations, business rules, or system behavior that are not documented.
- If any requirement is ambiguous or incomplete, clearly mark it as **Needs clarification**.
- Do **NOT** invent:
  - Error messages
  - Error codes
  - Business rules
  - Validation logic
  - API behavior
  - UI elements
  - System responses

---

# OUTPUT REQUIREMENTS

Generate the output as a **Microsoft Excel (.xlsx)** workbook.

### File Name

Use the following naming convention:

`TestCases_<YYYYMMDD_HHMMSS>.xlsx`

Example:

`TestCases_20260723_143015.xlsx`

---

# WORKSHEET

Create a single worksheet named:

**Test Cases**

---

# COLUMN STRUCTURE

Use the following columns in the exact order:

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |User Story Referance|

---

# FORMATTING RULES

For each test case:

1. Populate the following columns **ONLY in the first row** of the test case:
   - TID
   - Test Case Name
   - Category
   - Description
   - Pre-conditions
   - User Story Referance

2. For every subsequent step of the same test case, leave the following columns blank:
   - TID
   - Test Case Name
   - Category
   - Description
   - Pre-conditions

3. Each test step must be written on a **separate row**.

4. Every step must contain:
   - Step No
   - Step Description
   - Expected Result

5. Maintain a **1:1 mapping** between each step and its expected result.

6. Insert **exactly one blank row** after the last step of every test case.

7. Do **NOT** merge cells.

8. Preserve the generated row structure exactly as produced.

9. Apply basic Excel formatting:
   - Bold header row.
   - Freeze the header row.
   - Enable text wrapping for all cells.
   - Auto-adjust column widths based on content.
   - Apply filters to the header row.

10. Ensure the workbook is immediately usable without requiring manual formatting or transformation.

---

# PRIORITY

Assign one of the following priorities based solely on the PRD:

- High
- Medium
- Low

---

# QUALITY EXPECTATIONS

- Generate comprehensive coverage using only the PRD.
- Create atomic, independent test cases.
- Avoid duplicate scenarios.
- Cover:
  - Functional scenarios
  - Negative scenarios
  - Boundary values
  - Edge cases
- If any requirement is incomplete or ambiguous, mark it as **Needs clarification** rather than making assumptions.

---

# PRD

```text
[PASTE PRD HERE]
```