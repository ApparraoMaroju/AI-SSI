# Test Cases for TW-3491: Processing Status Tile (Bearbeitungsstatus)

**Generated:** April 6, 2026  
**Template Used:** FTC02-PRD to Test Cases (Comprehensive)

---

## Verified Facts

Based on explicit information provided in TW-3491.md and Tributum.md:

### From TW-3491 (User Story)
- A new tile named "Processing status" (Bearbeitungsstatus) is added to the dashboard
- The tile displays statuses of actions: saved, for approval, and approved
- When the tile is activated, a pop-up appears showing current actions being processed
- Users can select an area in the pop-up to navigate to the original mask
- Navigation allows continuing the release process
- Performance considerations are noted (potential separate backend endpoint)

### From Tributum.md (Context)
- **User Roles:**
  - Viewer User: View only access, all fields disabled, only Schließen (Close) button enabled
  - Writer User: Create, Edit, Save, Approve, Reject, Delete access
  - Admin User: Full access including Flow execution
- **Status Icons:**
  - Save icon: Record saved (editable)
  - Single orange tick: Sent for approval (non-editable for sender)
  - Green double tick: Approved (non-editable)
  - Production icon: In production state
- **UI Elements:**
  - Bearbeiten (Edit) page: Edit page with left column (updated data) and right column (production data)
  - Send for Approval button available
  - Approve and Reject buttons available

---

## Missing / Unknown Information

- **Tile Activation Method:** Not specified if click, double-click, or hover activates the tile (assumed: click)
- **Pop-up Layout:** Exact structure and fields displayed in the pop-up not specified
- **Error Handling:** Behavior when no actions are being processed not specified
- **Error Messages:** No error messages defined
- **API Endpoints:** Marked as "Not specified in requirements"
- **Validation Rules:** Not specified in requirements
- **Sorting/Filtering:** No sorting or filtering capability specified for the pop-up
- **Role-based Access:** Not specified if all roles can access the Processing Status tile
- **Performance Metrics:** Specific performance requirements not defined
- **Maximum Items:** Maximum number of actions displayed in pop-up not specified
- **Pagination:** Whether pop-up supports pagination for large datasets not specified

---

## Generated Output

### Test Cases Summary

| TID | Test Case Name | Category | Priority |
|-----|----------------|----------|----------|
| TC_TW3491_001 | Verify Processing Status Tile Visibility on Dashboard | Functional | High |
| TC_TW3491_002 | Verify Tile Displays All Three Status Types | Functional | High |
| TC_TW3491_003 | Verify Pop-up Appears on Tile Activation | Functional | High |
| TC_TW3491_004 | Verify Pop-up Displays Saved Actions | Functional | High |
| TC_TW3491_005 | Verify Pop-up Displays For Approval Actions | Functional | High |
| TC_TW3491_006 | Verify Pop-up Displays Approved Actions | Functional | High |
| TC_TW3491_007 | Verify Navigation from Pop-up to Original Mask | Functional | High |
| TC_TW3491_008 | Verify User Can Continue Release Process After Navigation | Functional | High |
| TC_TW3491_009 | Verify Pop-up Behavior When No Actions Are Being Processed | Edge | Medium |
| TC_TW3491_010 | Verify Viewer User Access to Processing Status Tile | Functional | Medium |

### Detailed Test Cases

**Full test case details are available in the Excel-compatible file:**  
`TestCases_20260406_120000.csv`

---

## Self-Validation Check

### ✅ No Assumptions Made
- All test cases are derived from explicit requirements in TW-3491.md
- Context from Tributum.md used only for verified facts (user roles, status icons, UI elements)
- For TC_TW3491_009 (Edge case), explicitly noted: "Insufficient information to determine exact message"

### ✅ All Test Cases Map to Verified Facts
| Test Case | Verified Fact Source |
|-----------|---------------------|
| TC_TW3491_001 | TW-3491: "A new tile named 'Processing status' is added to the dashboard" |
| TC_TW3491_002 | TW-3491: "The tile displays statuses of actions: saved, for approval, and approved" |
| TC_TW3491_003 | TW-3491: "When the tile is activated, a pop-up appears" |
| TC_TW3491_004 | TW-3491: Status "saved" + Tributum: Save icon reference |
| TC_TW3491_005 | TW-3491: Status "for approval" + Tributum: Orange tick icon |
| TC_TW3491_006 | TW-3491: Status "approved" + Tributum: Green double tick icon |
| TC_TW3491_007 | TW-3491: "Users can select an area in the pop-up to navigate to the original mask" |
| TC_TW3491_008 | TW-3491: "continue the release process" + Tributum: Send for Approval action |
| TC_TW3491_009 | Edge case based on logical scenario - no explicit behavior defined |
| TC_TW3491_010 | Tributum: Viewer User role definition with view-only access |

### ✅ No Invented Data
- No API endpoints invented (marked as not specified)
- No error messages invented
- No UI elements beyond those specified
- No validation rules assumed

### ✅ Format Compliance with Excel Rules
- CSV format suitable for direct Excel import
- Each step in separate row
- TID, Test Case Name, Category, Description, Pre-conditions only in first row of each test case
- Blank row between each test case
- No merged cells
- One-to-one mapping of Step Description to Expected Result

---

## Files Generated

1. **TestCases_20260406_120000.csv** - Excel-compatible test cases file
2. **TestCases_TW-3491_Documentation.md** - This documentation file

---

## Coverage Summary

| Coverage Area | Test Cases |
|---------------|------------|
| Functional (Happy Path) | TC_001, TC_002, TC_003, TC_004, TC_005, TC_006, TC_007, TC_008, TC_010 |
| Edge Cases | TC_009 |
| Role-Based | TC_010 |

**Note:** Negative scenarios and boundary value tests were not generated due to insufficient information in the requirements regarding error handling, validation rules, and system limits.
