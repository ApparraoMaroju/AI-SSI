## Scope
- **In Scope:**
  - Search functionality including:
    - Display of matching results based on valid search criteria
    - Result details (total count, pagination, scrollbars)
    - Persistence of search results after navigation
  - Reset (Zurücksetzen) functionality:
    - Clearing all search inputs and results
  - Sorting functionality:
    - Sorting data across columns
  - Column customization:
    - Enabling/disabling columns
    - Rearranging column order
    - Reset to default column configuration
  - Abbrechen (Cancel) functionality:
    - Returns user to dashboard screen
  - Edit & Create operations based on user roles:
    - Viewer User (View only access)
    - Writer User (Create, Edit, Save, Approve, Reject, Delete)
    - Admin User (Full access including Flow execution)

- **Out of Scope:**
  - Validation rules for input fields (Not specified in requirements)
  - Error handling and error messages (Not specified in requirements)
  - Backend/API behavior (Not specified in requirements)
  - Authentication/authorization mechanisms (Not specified in requirements)

---

## User Role Permissions

### Viewer User
| Permission | Access |
|------------|--------|
| Create data | Not allowed |
| Edit data | Not allowed |
| Access Bearbeiten (Edit) page | View mode only |
| Access Create new page | Not allowed ('+' icon disabled) |
| Edit fields | All fields disabled |
| Buttons enabled | Only Schließen (Close) button |
| View edit_pending icons | Allowed |

### Writer User
| Permission | Access |
|------------|--------|
| Create records | Allowed |
| View records | Allowed |
| Edit records | Allowed |
| Save records | Allowed |
| Approve records | Allowed |
| Reject records | Allowed |
| Delete records | Allowed |
| Execute/Run flow | Not allowed |

### Admin User
| Permission | Access |
|------------|--------|
| Create records | Allowed |
| View records | Allowed |
| Edit records | Allowed |
| Save records | Allowed |
| Approve records | Allowed |
| Reject records | Allowed |
| Delete records | Allowed |
| Execute/Run flow | Allowed (Full access) |

---

## Edit & Create Actions

> **NOTE:** Edit and Create have similar scenarios; only expected results differ for Save and Double Save operations.

### Save (Edit)
| Aspect | Effect on Itself |
|--------|------------------|
| Data | Record holds updated values. In Bearbeiten page: updated data in left column, production data in right column. Updated fields highlighted in green. |
| Icon | Shows save icon |
| Buttons | Delete (L1 & L2), Send for Approval, and Close buttons enabled |
| Timestamp & Users | Update timestamp in UI (insert timestamp in edit pending table) and change user updated. Release user field becomes empty |

**Effect on Parent:**
- If no edit_pending data exists: Change user and Update timestamp updated. Release user becomes empty
- If edit_pending data exists: No change

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: No change

### Save (Create New)
| Aspect | Effect on Itself |
|--------|------------------|
| Data | Record holds new values. In create new page: new data in left column, right column should be empty. Newly added fields highlighted in green. |
| Icon | Shows save icon |
| Buttons | Delete (L1 & L2), Send for Approval, and Close buttons enabled |
| Timestamp & Users | Update timestamp in UI (insert timestamp in edit pending table) and change user updated. Release user field becomes empty |

**Effect on Parent:**
- If no edit_pending data exists: Change user and Update timestamp updated. Release user becomes empty
- If edit_pending data exists: No change

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: No change

### Double Save (Edit)
| Aspect | Effect on Itself |
|--------|------------------|
| Data, Icon, Buttons | Same as Save, but latest changes overwrite previously saved data in the left column. Right column still shows production data. |
| Timestamp & Users | Update timestamp and change user updated when new edit is saved |

**Effect on Parent/Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: No change

### Double Save (Create New)
| Aspect | Effect on Itself |
|--------|------------------|
| Data, Icon, Buttons | Same as Save, but latest changes overwrite previously saved data in the left column. Right column should still be empty. |
| Timestamp & Users | Update timestamp in UI (insert timestamp in edit pending table) and change user updated |

**Effect on Parent/Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: No change

### Send for Approval
| Aspect | Effect on Itself |
|--------|------------------|
| Data | Record sent for approval and becomes non-editable |
| Message | "Record not editable" displayed |
| Icon | Single orange tick icon shown |
| Buttons (Sender) | Only Close button enabled |
| Buttons (Other users) | Approve, Reject, Close enabled |
| Timestamp & Users | Update timestamp and change user updated |

**Effect on Parent:** Update timestamp and change user updated. Entire tree sent for approval.

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change (status reflects sent for approval)
- If edit_pending data exists: Update timestamp and change user updated. Entire tree sent for approval

### Reject
| Aspect | Effect on Itself |
|--------|------------------|
| Data | Rejection comments stored and visible. Previously updated data remains visible. Record becomes editable. Comments persist until record is sent for approval again or deleted. |
| Icon | Shows save icon |
| Timestamp & Users | Update timestamp and change user updated |

**Effect on Parent:** Update timestamp and change user updated. Entire tree is rejected and rejection comments displayed in all edit pending records.

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: Update timestamp and change user updated. Entire tree is rejected and rejection comments displayed in all edit pending records.

> **NOTE:** Rejection comments should disappear only when record is sent again for approval.

### Approve
| Aspect | Effect on Itself |
|--------|------------------|
| Data | No change in data and should be non-editable |
| Message | "Record not editable" displayed |
| Icon | Shows green double tick icon |
| Timestamp & Users | Update timestamp and release user updated |

**Effect on Parent:** Release user and update timestamp updated. Entire tree is approved.

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: Release user and update timestamp updated. Entire tree is approved.

### Delete Level 1 (Top Button)
| Scope | Effect |
|-------|--------|
| Itself | Edits deleted only for the selected record |
| Parent | If last child → parent also deleted. If not last child → no change |
| Sibling | No change |
| Child | All children are deleted |

### Delete Level 2 (Footer Button)
| Scope | Effect |
|-------|--------|
| Itself | Edits deleted for entire tree |
| Parent | Edits deleted for entire tree |
| Sibling | Edits deleted for entire tree |
| Child | Edits deleted for entire tree |

### Flow (Admin Only)
| Aspect | Effect on Itself |
|--------|------------------|
| Data | Record moves to production state and becomes editable if required |
| Icon | Production icon displayed |
| Timestamp & Users | Insert ts and update ts for new production data = timestamp when flow 18 was running. No change in change user and release user |

**Effect on Parent:** Entire tree moved to production. Update ts = timestamp when flow 18 was running. No change in change user and release user.

**Effect on Sibling/Child:**
- If no edit_pending data exists: No change
- If edit_pending data exists: Insert ts and update ts = timestamp when flow 18 was running. No change in change user and release user.

---

## Test Data
| Data Type        | Value           | Purpose        |
|------------------|-----------------|----------------|
| Valid search input | Not specified in requirements | Happy path |
| Invalid search input | Not specified in requirements | Negative test |
| Empty search input | No input provided | Validate no results without search trigger |
| Viewer User | User with view-only access | Verify view mode restrictions |
| Writer User | User with create/edit/save/approve/reject/delete access | Verify write operations (no flow execution) |
| Admin User | User with full access including flow execution | Verify full access operations |

## Test Environment
- **Browser:** Not specified in requirements
- **Device:** Not specified in requirements
- **OS:** Not specified in requirements

## Dependencies
- Application UI for Search, Reset, Sorting, and Column Customization must be available
- User roles (Viewer, Writer, Admin) must be configured
- Data must exist to support search results and pagination
- Edit pending table must be available for timestamp and user tracking
- Parent-Child-Sibling relationships must exist for tree operations

## UI Elements
| Element | Description |
|---------|-------------|
| Bearbeiten (Edit) page | Edit page with left column (updated data) and right column (production data) |
| Create new page | Page for creating new records |
| '+' icon | Create new button (disabled for Viewer) |
| Schließen (Close) button | Close button |
| Abbrechen button | Cancel button - navigates to dashboard screen |
| Zurücksetzen button | Reset button - clears all search parameters and results |
| Delete L1 button | Top delete button (deletes selected record and children) |
| Delete L2 button | Footer delete button (deletes entire tree) |
| Send for Approval button | Sends record for approval |
| Approve button | Approves record |
| Reject button | Rejects record with comments |
| Save icon | Indicates saved state |
| Orange tick icon | Single orange tick - sent for approval |
| Green double tick icon | Approved state |
| Production icon | Production state |
| edit_pending icons | Icons showing pending edit status |

---

## Search Page Functionality

### Search Functionality
1. When valid search criteria are entered and the Search button is clicked, the system should display the corresponding matching results. The results should include:
   - Total count of records retrieved
   - Number of records per page (pagination)
   - Vertical and horizontal scrollbars, if applicable

2. When a user performs a search, navigates away from the screen, and then returns, the previously displayed search results should remain visible.

> **Note:** If the user only enters search criteria but does not click the Search button, no results should be displayed when revisiting the screen.

### Zurücksetzen (Reset)
When the Zurücksetzen button is clicked, all search parameters and search results should be cleared/reset to their default state.

### Sorting
1. When a column is sorted, all corresponding rows should be rearranged based on the selected column.
2. If another column is sorted, the sorting should be applied only to that column, overriding any previous sorting.

### Column Customization
1. The system should allow users to enable or disable the visibility of columns.
2. Users should be able to rearrange the column order as required.
3. The system should provide an option to reset and restore the default column configuration.

### Abbrechen (Cancel)
When the Abbrechen button is clicked, the dashboard screen should be displayed.

---

## Status Icons Reference
| Icon | Status |
|------|--------|
| Save icon | Record saved (editable) |
| Single orange tick | Sent for approval (non-editable for sender) |
| Green double tick | Approved (non-editable) |
| Production icon | In production state |

## Known Issues
- None currently identified (previous clarification queries resolved)