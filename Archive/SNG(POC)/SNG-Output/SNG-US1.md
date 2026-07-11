# User Stories: Enable User Assignment to Duty Schedules

- **Feature:** Enable User Assignment to Duty Schedules
- **Application:** UeLS-zentras On-call System (Pikettsystem 2)
- **Author:** Apparao Maroju
- **Role:** Test Manager
- **Date:** May 7, 2026
- **Source Document:** 6.3 Pikettsystem 2 en-US.pdf (v0.2)

---

## User Stories

| SID | Module / Feature | Scenario Description | Scenario Type | Priority | Reference Requirement |
|-----|------------------|---------------------|---------------|----------|-----------------------|
| SNG-US1-001 | On-call Participant Configuration | An administrator assigns an LDAP user as an on-call participant by linking their login to one or more alarm media (SMS/pager) | Functional | High | Section 6.8 – On-call participants |
| SNG-US1-002 | On-call Participant Configuration | An administrator assigns multiple alarm media (cell phone and pager) to a single on-call participant | Functional | High | Section 6.8 – On-call participants |
| SNG-US1-003 | On-call Participant Configuration | An administrator activates or deactivates a specific alarm medium for an on-call participant | Functional | High | Section 6.8 – On-call participants |
| SNG-US1-004 | Period Planning | An on-call planner assigns an on-call participant to an on-call period within a basic plan for a specific region | Functional | High | Section 5.2 – Period planning |
| SNG-US1-005 | Period Planning | The system displays a warning when the assigned on-call participant differs from the originally planned participant for the period | Functional | High | Section 5.2.1 – Merge period |
| SNG-US1-006 | Period Planning – Split | An on-call planner splits a period and assigns on-call participants to both newly created periods | Functional | Medium | Section 5.2.2 – Split period |
| SNG-US1-007 | Period Planning – Merge | An on-call planner merges two adjacent periods and selects the on-call participant for the merged period | Functional | Medium | Section 5.2.1 – Merge period |
| SNG-US1-008 | Period Planning – Handover | An on-call planner adjusts the handover time between two periods and selects the responsible on-call participants | Functional | Medium | Section 5.2.3 – Adjust transfer date |
| SNG-US1-009 | Escalation Assignment – Period | An on-call planner assigns an escalation on-call participant at the period level who is alerted if the regular participant cannot be reached | Functional | High | Section 2.2.10 – Escalation rules |
| SNG-US1-010 | Escalation Assignment – Region | An administrator assigns an escalation on-call participant at the region level as a fallback when both regular and period-level escalation fail | Functional | High | Section 6.1 – On-call region / Section 2.2.10 |
| SNG-US1-011 | Escalation Chain | The system follows the escalation chain (regular → period escalation → region escalation) when the on-call participant cannot be reached | Functional | High | Section 2.2.10 – Escalation rules |
| SNG-US1-012 | Info Box | The system displays the assigned on-call participant details in the info box when a period is selected | Functional | Medium | Section 5.2 – Period planning (Info box) |
| SNG-US1-013 | Absence Planning | An on-call planner records an absence (Vacation, Sickness, Compensation, Military/Civilian Service, Cleaning, Unpaid, Other) for an on-call participant | Functional | Medium | Section 7.1 – Planning an absence |
| SNG-US1-014 | Absence Warning | The system displays a visual indicator when an on-call participant assigned to a period has a recorded absence during that period | Functional | Medium | Section 7.1 – Planning an absence |
| SNG-US1-015 | Holiday Warning | The system displays a warning when an on-call period that includes a public holiday is assigned to a participant | Functional | Medium | Section 7.2 – Configuration of public holidays |
| SNG-US1-016 | Overall Planning Report | A user generates an overall planning evaluation showing all regions and assigned on-call participants in a day-based view | Functional | Medium | Section 9.1 – Overall planning |
| SNG-US1-017 | On-call Region Report | A user generates a region-specific duty roster showing assigned on-call participants for a selected region and date range | Functional | Medium | Section 9.2 – On-call region |
| SNG-US1-018 | On-call Participant Report | A user generates a participant-specific report showing all on-call assignments for a selected participant | Functional | Medium | Section 9.3 – On-call participants |
| SNG-US1-019 | Conflict Detection | The system highlights scheduling conflicts in red and multiple on-call shifts in orange in evaluation reports | Functional | Medium | Section 9.1 – Overall planning |
| SNG-US1-020 | Report Export | A user exports the on-call assignment evaluation as CSV or XML | Functional | Low | Section 9.1 – Overall planning |
| SNG-US1-021 | Negative – No Alarm Media | An administrator attempts to assign an LDAP user as an on-call participant without linking any alarm medium | Negative | High | Section 2.2.3 – On-call participant |
| SNG-US1-022 | Negative – Deactivated Alarm Media | All alarm media for an assigned on-call participant are deactivated, resulting in no alarms being forwarded | Negative | High | Section 6.8 – On-call participants |
| SNG-US1-023 | Negative – Paused Region | An on-call participant is assigned to a period in a paused region; SMS/pager messages are not sent | Negative | Medium | Section 6.2 – Pause |
| SNG-US1-024 | Negative – Inactive System | An alarm occurs for an inactive system; the assigned on-call participant does not receive a notification | Negative | Medium | Section 6.7 – System activation |
| SNG-US1-025 | Negative – Invalid Phone Number | An alarm medium is configured with an invalid phone number; F24 eCall returns error 5112 | Negative | High | Section 8.4 – eCall error codes |
| SNG-US1-026 | Negative – Unassigned Period | An on-call period exists without an assigned participant; the system does not forward alarms for that period | Negative | High | Section 5.2 – Period planning |
| SNG-US1-027 | Boundary – Single Day Period | An on-call planner assigns a participant to a period of exactly one day duration | Boundary | Medium | Section 5.2.2 – Split period |
| SNG-US1-028 | Boundary – Max Alarm Media | An on-call participant is assigned the maximum number of alarm media supported by the system | Boundary | Low | Section 6.8 – On-call participants |
| SNG-US1-029 | Boundary – Period at Plan Start/End | An on-call participant is assigned to the first and last periods of a basic plan | Boundary | Medium | Section 5.1 – Basic planning |
| SNG-US1-030 | Edge Case – Midnight Handover | An on-call planner assigns a participant with a handover time crossing midnight | Edge Case | Medium | Section 5.2.3 – Adjust transfer date |
| SNG-US1-031 | Edge Case – Same Participant Consecutive | The same on-call participant is assigned to consecutive periods in the same region | Edge Case | Low | Section 5.2 – Period planning |
| SNG-US1-032 | Edge Case – Participant in Multiple Regions | An on-call participant is assigned to periods in multiple on-call regions simultaneously | Edge Case | Medium | Section 5.2 – Period planning / Section 9.1 |
| SNG-US1-033 | Edge Case – Absence Does Not Block | An on-call participant with a recorded absence can still be assigned to a period (warning only, no prevention) | Edge Case | Medium | Section 7.1 – Planning an absence |
| SNG-US1-034 | Edge Case – Escalation Same as Regular | The escalation participant is set to the same person as the regular on-call participant | Edge Case | Low | Section 2.2.10 – Escalation rules |
| SNG-US1-035 | Edge Case – Failover Duplicate | During a cluster communication interruption, an assigned participant may receive duplicate alarm messages from both locations | Edge Case | Low | Section 2 – Application architecture |
| SNG-US1-036 | Security – Authorization Check | A user without sufficient authorization cannot assign on-call participants to duty periods | Security | High | Section 1.3 – Delimitation / Section 2.1 – User roles |
| SNG-US1-037 | Security – LDAP Authentication | Only authenticated LDAP users or SSO-authenticated users can be assigned as on-call participants | Security | High | Section 2.2.2 – LDAP user |
| SNG-US1-038 | Integration – UeLS-zentras Sync | When a new system is added in UeLS-zentras, it is automatically synchronized to the on-call system and available for region assignment | Integration | Medium | Section 6.7 – System activation |
| SNG-US1-039 | Integration – F24 eCall Delivery | When an alarm occurs, the system sends SMS/pager to the assigned on-call participant via F24 eCall and tracks delivery status | Integration | High | Section 8.3 – SMS/Pager / Section 1.4 |
| SNG-US1-040 | Integration – Escalation via eCall | When the F24 eCall response indicates the regular participant was unreachable, the system escalates to the next participant in the chain | Integration | High | Section 2.2.10 – Escalation rules |
| SNG-US1-041 | Usability – Participant Selection UI | The on-call participant selection dropdown/list is available during period creation, split, merge, and handover adjustment | Usability | Medium | Section 5.2 – Period planning |
| SNG-US1-042 | Usability – Conflict Visualization | Scheduling conflicts and multiple assignments are clearly visible using red and orange color coding in evaluation views | Usability | Medium | Section 9.1 – Overall planning |

---

**Notes:**
- Specific REST/SOAP API endpoint details are not specified in the requirements document.
- Browser and OS requirements for the test environment are **"Needs Clarification"**.
- Maximum number of alarm media per participant is not explicitly stated in the requirements — marked as a boundary scenario for validation.
