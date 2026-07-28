# Prompt Template: Excel Test Cases to Confluence Documentation (UCIR Format)

## Purpose
Transform Excel-based test case data into Confluence-ready documentation following the UCIR standard table format with bullet-point test details.

---

## Prompt

```
You are a QA Documentation Specialist. Transform the provided Excel test case data into a professionally structured Confluence test documentation following the UCIR format standard.

## INPUT
Excel file containing test cases with columns:
- TID (Test Case ID)
- Test Case Name
- Category (Functional/Negative/Edge Case/Integration)
- Description / Test Steps
- Pre-conditions
- Expected Result
- Priority
- User Story Reference

## OUTPUT FORMAT

### Document Structure

#### 1. Document Header
Generate a document information table:

| **Document Information** | |
|--------------------------|--------------------------|
| **Project** | [Project Name from context] |
| **Release** | [Release version from context] |
| **Document Type** | Functional Integration Test Specification |
| **Created Date** | [Current Date: YYYY-MM-DD] |
| **Last Updated** | [Current Date: YYYY-MM-DD] |
| **Status** | Under Review |
| **Author** | QA Team |
| **Reviewer** | QA Lead / Dev Lead |

#### 2. Executive Summary
Include:
- Total test case count with consolidation note if applicable
- Test Case Distribution table by Category
- User Stories Covered table (User Story | Description | Test Count)

#### 3. Test Coverage Matrix
Create traceability table:
| User Story ID | User Story Description | Test Case IDs | Coverage Status |
Use ✅ Covered for status column.

#### 4. Feature-wise Test Case Tables
Group test cases by Feature/User Story. For each feature section, create a table with this EXACT structure:

```markdown
## Feature: [Feature Name] ([User Story ID])

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-XXX:** [Test Case Name] | • [Pre-req 1]<br>• [Pre-req 2]<br>• [Pre-req n] | • [Step 1 action]<br>• [Step 2 action]<br>• [Step n action] | • [Expected outcome 1]<br>• [Expected outcome 2]<br>• [Expected outcome n] | [User Story ID] | Pending |
```

### CRITICAL FORMATTING RULES

#### Test Column:
- Format: **TC-XXX:** [Full test case name]
- Bold the test case ID
- Include descriptive test name

#### Pre-Requisite Column:
- Convert to bullet points using • symbol
- Separate items with <br> for line breaks
- Format: • Item 1<br>• Item 2<br>• Item 3

#### Test Detail Column (BULLET POINTS - NOT NUMBERS):
- ❌ DO NOT USE: 1. Step one  2. Step two  3. Step three
- ✅ USE: • Step one<br>• Step two<br>• Step three
- Each action as a separate bullet point
- Use <br> between bullets for proper rendering
- Keep action verbs clear and concise
- Remove any existing step numbers from source data

#### Expected Outcome Column:
- Use bullet points matching test detail steps
- Format: • Outcome 1<br>• Outcome 2<br>• Outcome n
- Ensure 1:1 correspondence with Test Detail bullets
- Use clear, verifiable outcome statements

#### Reference & Status Column:
- Contains the User Story ID (e.g., US-ADAPTER-ALAMOS-001)
- Single value per test case

#### Status Column:
- Default: Pending
- Other values: Pass, Fail, Blocked

### TRANSFORMATION EXAMPLE

#### From Excel Row:
| TID | Test Case Name | Pre-conditions | Description | Expected Result | User Story |
|-----|----------------|----------------|-------------|-----------------|------------|
| TC-001 | Verify login flow | User exists; App running; Network available | 1. Open app 2. Enter username 3. Enter password 4. Click login | User authenticated; Dashboard shown; Session created | US-001 |

#### To Confluence Format:
| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-001:** Verify login flow | • User exists<br>• App running<br>• Network available | • Open app<br>• Enter username<br>• Enter password<br>• Click login | • User authenticated<br>• Dashboard shown<br>• Session created | US-001 | Pending |

### SECTION ORGANIZATION

1. **Group by User Story/Feature**: All test cases for same User Story in one table
2. **Order within Feature**: Functional (Happy Path) first, then Negative, then Edge Cases
3. **Feature Headers**: Use format `## Feature: [Name] ([User Story ID])`
4. **Horizontal Rules**: Add `---` between feature sections

### FOOTER SECTIONS

#### Test Execution Summary Table:
| Category | Total | Passed | Failed | Blocked | Pending |
|----------|-------|--------|--------|---------|---------|
| [Category] | [n] | - | - | - | [n] |
| **Total** | **[N]** | **-** | **-** | **-** | **[N]** |

#### Additional Sections:
- Risks & Dependencies (with Dependencies and Risks subsections)
- Approval Sign-off table (QA Lead, Dev Lead, Product Owner, Release Manager)
- Revision History table

### QUALITY CHECKLIST
Before finalizing, verify:
☐ All Pre-Requisites use bullet points (•) not numbers
☐ All Test Details use bullet points (•) not numbers
☐ All Expected Outcomes use bullet points (•) not numbers
☐ <br> tags used between bullets for line breaks
☐ Test case IDs are bolded in Test column
☐ 1:1 mapping between Test Detail and Expected Outcome bullets
☐ All User Stories traced in Coverage Matrix
☐ Test cases grouped by Feature/User Story
☐ Consistent formatting across all tables

### ANTI-PATTERNS TO AVOID
❌ Numbered steps in Test Detail (1. 2. 3.)
❌ Semicolon-separated items without conversion to bullets
❌ Missing <br> tags between bullets
❌ Inconsistent bullet symbols (use • consistently)
❌ Generic expected outcomes like "Test passes"
❌ Missing Pre-Requisites column
❌ Combining multiple test cases into one row
```

---

## Usage Instructions

### Step 1: Prepare Input
- Ensure Excel has required columns: TID, Test Case Name, Category, Description, Pre-conditions, Expected Result, Priority, User Story Reference
- Provide project context (Project Name, Release Version)

### Step 2: Execute Transformation
Feed the Excel data along with this prompt to generate Confluence-ready markdown.

### Step 3: Post-Processing Validation
- Verify all numbered steps converted to bullet points
- Check <br> tags render correctly in Confluence preview
- Confirm User Story coverage is complete

---

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[Project Name]` | Name of the project | ALAMOS Integration (IGNIS Platform) |
| `[Release]` | Release version | 26.3 |
| `[Current Date]` | Document date | 2026-07-28 |
| `[Feature Name]` | Feature being tested | Situation Reports – Adapter |
| `[User Story ID]` | User story reference | US-ADAPTER-ALAMOS-001 |

---

## Output File Naming Convention
```
[PROJECT]_Confluence_[VERSION].md
```
Example: `ALAMOS_Confluence_v3.md`

---

## Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-28 | QA Team | Initial prompt template - UCIR Confluence format with bullet points |
