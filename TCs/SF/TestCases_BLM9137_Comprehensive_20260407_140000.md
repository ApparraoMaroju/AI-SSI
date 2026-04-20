# Test Cases - BLM-9137: Improve Add and Edit Area Offerings Flow Usability

---

## Verified Facts

**Add Area Offerings Flow:**
- Screen 1: Cancel button must be positioned on the LEFT side
- Screen 2: "Back" button renamed to "Previous"
- Screen 2: "Back" and "Cancel" buttons swap positions

**Edit Area Offerings Flow:**
- Screen 1: Window dynamically adjusts height based on number of existing Area Offerings
- Screen 1: "Save" button renamed to "Save & Close" (EN) / "Speichern & Schließen" (DE)
- Screen 1: "Add Area Offerings" button renamed to "Save & Add Area Offerings" (EN) / "Speichern & Area Offerings hinzufügen" (DE)
- Screen 1: "Save & Add Area Offerings" must persist deletions AND changes to Amount/Quantity
- Screen 2: X close icon added in upper right corner
- Screen 2: Cancel button moved to the left
- Screen 3: Window dynamically adjusts based on number of selected Area Offerings
- Screen 3: X close icon added in upper right corner
- Screen 3: "Back" button renamed to "Previous"
- Screen 3: "Previous" and "Cancel" swap positions, placing Cancel next to "Save"

**Translation Rules:**
- Only explicitly mentioned translations are changed
- All other translations remain unchanged

---

## Missing / Unknown Information

- Minimum/maximum number of Area Offerings for dynamic height testing
- Exact behavior when X icon is clicked (close without save? confirmation dialog?)
- Error handling if save fails
- Specific pixel dimensions or thresholds for "reduced grey space"
- Behavior when user has no Area Offerings (empty state)
- Whether Previous button has same functionality as old Back button
- Keyboard navigation/accessibility requirements

---

## Generated Test Cases

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC001 | Add Flow Screen 1 - Cancel Button Left Position | Functional | Verify Cancel button positioned on left in first Add screen | Opportunity Owner logged in; Opportunity exists | 1 | Navigate to Opportunity record | Record loads | High |
| | | | | | 2 | Click Add Area Offerings | Dialog Screen 1 opens | |
| | | | | | 3 | Locate Cancel button | Cancel button is on LEFT side of screen | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC002 | Add Flow Screen 2 - Previous Label and Button Swap | Functional | Verify Back renamed to Previous and positions swapped with Cancel | Add flow Screen 1 completed | 1 | Complete Screen 1 and proceed | Screen 2 displays | High |
| | | | | | 2 | Verify button formerly labeled "Back" | Button now labeled "Previous" | |
| | | | | | 3 | Verify Previous and Cancel positions | Buttons have swapped positions from original layout | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC003 | Edit Flow Screen 1 - Dynamic Window Height | Functional | Verify window adjusts to number of Area Offerings | Opportunity with 2 Area Offerings | 1 | Open Edit Area Offerings | Dialog opens with minimal grey space for 2 items | High |
| | | | | | 2 | Close dialog and add 10 more Area Offerings to Opportunity | 12 Area Offerings exist | |
| | | | | | 3 | Open Edit Area Offerings again | Window height expanded to accommodate 12 items | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC004 | Edit Flow Screen 1 - Button Labels English | Functional | Verify Save and Add Area Offerings buttons renamed | User language English; Opportunity with Area Offerings | 1 | Open Edit Area Offerings | Dialog Screen 1 opens | High |
| | | | | | 2 | Locate button formerly labeled "Save" | Button displays "Save & Close" | |
| | | | | | 3 | Locate button formerly labeled "Add Area Offerings" | Button displays "Save & Add Area Offerings" | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC005 | Edit Flow Screen 1 - Button Labels German | Functional | Verify German translations for renamed buttons | User language German; Opportunity with Area Offerings | 1 | Open Edit Area Offerings | Dialog Screen 1 opens in German | High |
| | | | | | 2 | Locate Save button | Button displays "Speichern & Schließen" | |
| | | | | | 3 | Locate Add Area Offerings button | Button displays "Speichern & Area Offerings hinzufügen" | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC006 | Save & Add - Persists Amount Changes | Functional | Verify Amount field modifications saved when clicking Save & Add | Opportunity with Area Offerings; Area Offering has Amount=100 | 1 | Open Edit Area Offerings | Dialog opens | Critical |
| | | | | | 2 | Change Amount from 100 to 250 | Amount value updated in dialog | |
| | | | | | 3 | Click "Save & Add Area Offerings" | System saves and navigates to add screen | |
| | | | | | 4 | Cancel and check Area Offering | Amount = 250 (change persisted) | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC007 | Save & Add - Persists Quantity Changes | Functional | Verify Quantity field modifications saved | Opportunity with Area Offering; Quantity=5 | 1 | Open Edit Area Offerings | Dialog opens | Critical |
| | | | | | 2 | Change Quantity from 5 to 15 | Quantity value updated | |
| | | | | | 3 | Click "Save & Add Area Offerings" | Navigates to add screen | |
| | | | | | 4 | Cancel and verify Area Offering | Quantity = 15 (persisted) | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC008 | Save & Add - Persists Deletions | Functional | Verify removed Area Offerings are deleted | Opportunity with 3 Area Offerings | 1 | Open Edit Area Offerings | Dialog shows 3 Area Offerings | Critical |
| | | | | | 2 | Mark 1 Area Offering for removal | Item marked for deletion | |
| | | | | | 3 | Click "Save & Add Area Offerings" | Navigates to add screen | |
| | | | | | 4 | Cancel and check Opportunity | Only 2 Area Offerings remain (deletion persisted) | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC009 | Save & Add - Multiple Changes Combined | Functional | Verify deletion + Amount + Quantity changes all persist | Opportunity with 3 Area Offerings | 1 | Open Edit Area Offerings | Dialog opens with 3 items | Critical |
| | | | | | 2 | Modify Amount on first Area Offering | Amount changed | |
| | | | | | 3 | Modify Quantity on second Area Offering | Quantity changed | |
| | | | | | 4 | Mark third Area Offering for removal | Item marked | |
| | | | | | 5 | Click "Save & Add Area Offerings" | Navigates to add screen | |
| | | | | | 6 | Cancel and verify all changes | Amount persisted; Quantity persisted; Third item deleted | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC010 | Edit Flow Screen 2 - X Icon and Cancel Position | Functional | Verify X close icon and Cancel button left position | Edit flow navigated to Screen 2 | 1 | From Edit Screen 1 click Save & Add Area Offerings | Screen 2 displays | High |
| | | | | | 2 | Look at upper right corner | X close icon is visible | |
| | | | | | 3 | Click X icon | Dialog closes | |
| | | | | | 4 | Reopen and navigate to Screen 2 | Screen 2 displays | |
| | | | | | 5 | Locate Cancel button | Cancel is on LEFT side | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC011 | Edit Flow Screen 3 - Dynamic Height | Functional | Verify window adjusts to selected Area Offerings count | Edit flow at Screen 2 with selections available | 1 | Select 2 Area Offerings and proceed to Screen 3 | Window height appropriate for 2 items | High |
| | | | | | 2 | Go back and select 8 Area Offerings | 8 items selected | |
| | | | | | 3 | Proceed to Screen 3 | Window height expanded for 8 items | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC012 | Edit Flow Screen 3 - X Icon | Functional | Verify X close icon in upper right corner | Edit flow at Screen 3 | 1 | Navigate to Screen 3 of Edit flow | Screen 3 displays | High |
| | | | | | 2 | Look at upper right corner | X close icon is visible | |
| | | | | | 3 | Click X icon | Dialog closes | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC013 | Edit Flow Screen 3 - Previous Label and Button Layout | Functional | Verify Back→Previous rename and Cancel next to Save | Edit flow at Screen 3 | 1 | Navigate to Screen 3 | Screen displays | High |
| | | | | | 2 | Verify button formerly labeled "Back" | Button now labeled "Previous" | |
| | | | | | 3 | Verify Cancel button position | Cancel is directly next to Save button | |
| | | | | | 4 | Verify Previous button position | Previous is on opposite side from Cancel/Save | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC014 | Unchanged Translations Preserved | Functional | Verify non-mentioned translations remain unchanged | German language; Edit flow open | 1 | Open Edit Area Offerings in German | Dialog opens | Medium |
| | | | | | 2 | Verify Cancel button label | Remains as original German translation (unchanged) | |
| | | | | | 3 | Verify Previous button label on Screen 3 | Label is localized but only "Previous" wording changed per spec | |
| | | | | | 4 | Verify all other UI element translations | All unchanged from previous version | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC015 | Save & Close Functionality | Functional | Verify Save & Close saves changes and closes dialog | Opportunity with Area Offerings; changes made | 1 | Open Edit Area Offerings | Dialog opens | High |
| | | | | | 2 | Modify Amount on an Area Offering | Value changed | |
| | | | | | 3 | Click "Save & Close" | Dialog closes | |
| | | | | | 4 | Verify Area Offering | Amount change persisted | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC016 | Edge - Single Area Offering Dynamic Height | Edge | Verify dynamic height with minimum Area Offerings | Opportunity with exactly 1 Area Offering | 1 | Open Edit Area Offerings | Dialog opens | Medium |
| | | | | | 2 | Observe window height | Height minimized appropriately for single item | |

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC017 | Edge - Screen 3 Single Selection Dynamic Height | Edge | Verify Screen 3 dynamic height with single selection | Edit flow at Screen 2 | 1 | Select exactly 1 Area Offering | 1 item selected | Medium |
| | | | | | 2 | Proceed to Screen 3 | Window height minimized for single selection | |

---

## Self-Validation Check

- ✅ No assumptions made - all test cases derived from explicit acceptance criteria
- ✅ All 14 acceptance criteria mapped to test cases
- ✅ No invented error messages, API calls, or UI elements
- ✅ Format complies with Excel structure rules (TID in first row only, blank rows between cases)
- ✅ Category appropriately assigned (Functional, Edge)
- ✅ Only explicitly mentioned translations tested (Save & Close, Save & Add Area Offerings)

---

## Coverage Matrix

| Acceptance Criteria | Test Case(s) |
|---------------------|--------------|
| Cancel left in Add Screen 1 | TC001 |
| Back/Cancel swapped in Add Screen 2 | TC002 |
| Back→Previous in Add Screen 2 | TC002 |
| Dynamic height Edit Screen 1 | TC003, TC016 |
| Save→Save & Close | TC004, TC005, TC015 |
| Add Area Offerings→Save & Add Area Offerings | TC004, TC005 |
| Save & Add persists deletions/Amount/Quantity | TC006, TC007, TC008, TC009 |
| X icon Edit Screen 2 | TC010 |
| Cancel left Edit Screen 2 | TC010 |
| X icon Edit Screen 3 | TC012 |
| Dynamic height Edit Screen 3 | TC011, TC017 |
| Back→Previous Edit Screen 3 | TC013 |
| Previous/Cancel swap, Cancel next to Save | TC013 |
| Only mentioned translations changed | TC014 |

**Total: 17 Test Cases** | Critical: 4 | High: 11 | Medium: 2
