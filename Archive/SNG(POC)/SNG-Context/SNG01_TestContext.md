# Testing Context

## Scope
- **In Scope:**
  - Planning View: Basic plan creation, editing, copying, deleting, extending/shortening; period split, merge, handover time adjustment
  - Configuration View: On-call region CRUD, pause/unpause, auto-pause schedules, alarm delay, shipping delay, group-to-region assignment, system activation, on-call participant management, alarm media management
  - Appointment View: Absence planning (all types), public holiday configuration, i-Cal import
  - Message View: On-call alarm list, delayed alarms, SMS/pager message list, shipping list, internal alarms, measurements, suppressed data points, test message sending
  - Evaluation View: Overall planning report, on-call region report, on-call participant report, CSV/XML export
  - Escalation: Escalation chain (regular → period → region), eCall response handling
  - System Configuration View: Objects, system computers, assets, data point groups, data points, communication
  - Navigation & UI: Meta area icons, view/tab selection, login/logout, settings, context menus, alarm frame
  - F24 eCall Integration: SMS/pager message sending, delivery status tracking, error handling

- **Out of Scope:**
  - UeLS-zentras core functionality (alarms, data points, measured values – covered by separate UeLS-zentras documentation)
  - LDAP/SSO authentication infrastructure (managed externally)
  - F24 eCall backend service (third-party system)
  - Network/infrastructure failover mechanics between Stans and Senti locations
  - Authorization/role configuration within UeLS-zentras

## Test Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid region name | "RegionAlpha01" | Happy path – region creation (≤20 alphanumeric chars) |
| Invalid region name | "Region With Spaces!@#" | Negative test – special characters and spaces |
| Region name > 20 chars | "RegionAlphaBetaGamma99" | Boundary test – exceeds max length |
| Valid phone number | "0791234567" | Happy path – alarm medium creation |
| Invalid phone number | "079-ABC-1234" | Negative test – non-numeric characters |
| Valid SMS text | "UeLS-Z Test alarm message" (≤154 chars) | Happy path – test message sending |
| SMS text > 154 chars | 155+ character string | Boundary test – exceeds max SMS length |
| Valid time format | "08:00" | Happy path – auto-pause time entry |
| Invalid time format | "25:99" | Negative test – invalid time |
| Valid alarm delay | 300 (seconds) | Happy path – alarm delay configuration |
| Valid absence type | "Vacation" | Happy path – absence planning |
| Valid holiday date | "2026-12-25" | Happy path – public holiday entry |
| Midnight-spanning time | From "20:00" To "07:00" | Edge case – alarm delay crossing midnight |
| On-call participant (LDAP) | Valid LDAP login | Happy path – participant assignment |
| i-Cal file | Standard .ics file | Happy path – holiday import |
| eCall error code | 5112 | Error handling – invalid phone number response |
| eCall success status | 8 (receipt confirmed) | Happy path – successful SMS delivery |

## Test Environment
- **Browser:** Web browser (SA-CH compliant application) [NEEDS CLARIFICATION – specific browser versions]
- **Device:** Desktop
- **OS:** Not specified in requirements – [NEEDS CLARIFICATION]
- **Application:** UeLS-zentras On-call System (Pikettsystem 2) v0.2
- **Cluster:** Active-passive cluster (Stans and Senti locations)

## Dependencies
- UeLS-zentras application must be running and accessible
- LDAP service must be available for user authentication
- F24 eCall interface must be accessible for SMS/pager message sending
- UeLS-zentras system assets must be synchronized to the on-call system database
- At least one on-call region must be configured and active
- At least one on-call participant with active alarm media must exist
- At least one on-call basic plan with assigned periods must be configured
- System computers and data point lists must be loaded from UeLS-zentras

## Known Issues
- In a communication interruption between Stans and Senti, duplicate messages may be sent (documented as unlikely but possible; manual deactivation of regions at one location is the workaround)
- Absence planning does not prevent scheduling an on-call participant for duty (warning only)
- Delayed alarms view is runtime-only (not persisted) – contents lost on application restart
- If a region is paused, test messages will silently fail to send (no SMS/pager entry created)
