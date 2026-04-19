
# Test Case Generation Prompts

- **Author:** Apparao Maroju  
- **Role:** Test Manager  

---

## PRD to Test Cases (Comprehensive)


ROLE: You are a Senior QA Engineer with 10+ years of experience.

TASK:
Generate comprehensive test cases from the provided PRD and also produce a Test Matrix summary report.

OBJECTIVE:
Ensure complete functional validation of the system based only on the provided requirements.

COVERAGE AREAS:
- Functional (happy path)
- Negative scenarios
- Boundary values
- Edge cases

CONSTRAINTS:
- Use ONLY PRD content
- Do NOT assume functionality not mentioned
- Mark unclear requirements as "Needs clarification"
- Do NOT invent error messages, status codes, or validation rules
- If a requirement is missing expected behavior, mention "Expected result needs clarification"

OUTPUT STRUCTURE:

SECTION 1 — Test Case Summary
Provide a summary count of generated test cases.

Format:
Total Test Cases Generated: <number>

Breakdown:
- Functional:
- Negative:
- Boundary:
- Edge Cases:

---

SECTION 2 — Test Case Table

FORMAT:
| TID | Category | Description | Pre-conditions | Steps | Expected Result | Priority |

---

SECTION 3 — Requirement Coverage Matrix

FORMAT:
| Requirement ID | Requirement Description | Covered Test Cases |

---

SECTION 4 — HTML Test Matrix Report

Generate an HTML report that visualizes the test coverage.

HTML FORMAT:

<!DOCTYPE html>
<html>
<head>
<title>Test Matrix Report</title>
<style>
body {
  font-family: Arial;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background-color: #f2f2f2;
}
.summary {
  background-color: #eef;
  padding: 10px;
  margin-bottom: 20px;
}
</style>
</head>

<body>

<h1>Test Coverage Report</h1>

<div class="summary">
<h2>Test Case Summary</h2>
<p>Total Test Cases Generated: X</p>
<p>Functional: X</p>
<p>Negative: X</p>
<p>Boundary: X</p>
<p>Edge Cases: X</p>
</div>

<h2>Test Case Matrix</h2>

<table>
<tr>
<th>TID</th>
<th>Category</th>
<th>Description</th>
<th>Priority</th>
</tr>

<!-- Generated Rows -->

</table>

<h2>Requirement Traceability Matrix</h2>

<table>
<tr>
<th>Requirement</th>
<th>Covered Test Cases</th>
</tr>

<!-- Generated Rows -->

</table>

</body>
</html>

---

PRD: <<< [PASTE PRD HERE] >>>

---