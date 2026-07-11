# Feature Context: UeLS-zentras On-call System (Pikettsystem 2)

## Overview
The On-call System (Pikettsystem 2) is a web-based application for managing on-call duty schedules, alarm forwarding, and SMS/pager notifications for the Swiss Federal Roads Office (FEDRO). It integrates with UeLS-zentras to receive alarms from infrastructure systems and forwards them to on-call personnel via SMS and pager using the F24 eCall interface.

## User Stories
- As an **on-call planner**, I want to create and manage on-call basic plans so that on-call duty is scheduled for specific regions and time intervals
- As an **on-call planner**, I want to split, merge, and adjust on-call periods so that duty schedules can be flexibly managed
- As an **administrator**, I want to configure on-call regions so that alarm messages are routed to the correct on-call personnel
- As an **administrator**, I want to configure auto-pause schedules so that SMS/pager forwarding is suppressed during working hours
- As an **administrator**, I want to set alarm delays so that transient alarms do not trigger unnecessary notifications
- As an **administrator**, I want to configure shipping delays so that less important alarms are collected and sent later
- As an **administrator**, I want to manage on-call participants and their alarm media (phones/pagers) so that alerts reach the right devices
- As an **on-call participant**, I want to view on-call alarms and SMS/pager message lists so that I can monitor alert status
- As an **on-call planner**, I want to record absences (vacation, sickness, etc.) so that on-call planning accounts for unavailability
- As an **on-call planner**, I want to configure public holidays so that on-call scheduling displays appropriate warnings
- As a **user**, I want to send test messages to verify that alerting is working correctly
- As a **user**, I want to generate evaluation reports (overall plan, region-based, participant-based) so that on-call schedules can be reviewed and exported

## Acceptance Criteria

### Planning View
- [ ] Basic on-call plans can be created for a specific region and time interval
- [ ] On-call periods can be assigned to on-call participants
- [ ] Periods can be split into two parts with configurable day count
- [ ] Periods can be merged with previous or subsequent periods
- [ ] Handover times can be adjusted for periods
- [ ] Basic plans can be extended, shortened, copied, and deleted
- [ ] Warning displayed when on-call participant differs from planned participant
- [ ] Info box shows participant details for each period

### Configuration View
- [ ] On-call regions can be created with unique name (max 20 alphanumeric chars)
- [ ] Regions can be paused/unpaused manually
- [ ] Auto-pause schedules can be configured per weekday with activate/pause actions
- [ ] Alarm delays can be configured per region, weekday, time range, priority, AKS code, and system
- [ ] Shipping delays can be configured to collect and defer message delivery
- [ ] UeLS-zentras groups can be assigned to on-call regions
- [ ] Systems can be activated/deactivated for alarm forwarding
- [ ] On-call participants can be created by assigning LDAP users to alarm media
- [ ] Alarm media (SMS/pager) can be created with identification, number, and type
- [ ] Multiple alarm media can be assigned to a single participant

### Appointment View
- [ ] Absences can be recorded with type (Vacation, Compensation, Sickness, Military/Civilian Service, Cleaning, Unpaid, Other)
- [ ] Public holidays can be entered per region or for all regions
- [ ] Holidays can be imported via i-Cal file
- [ ] Warning messages displayed during planning when periods include holidays

### Message View
- [ ] On-call alarm list displays last 1000 alarms (most recent first)
- [ ] Delayed alarms list shows alarms with active alarm or shipping delay
- [ ] SMS/pager message list displays last 1000 messages with delivery status
- [ ] Shipping list displays last 1000 dispatch attempts with eCall response status
- [ ] Internal alarms list shows priority 1, 2, and 3 messages
- [ ] Measurements list shows current data point values
- [ ] Suppressed data points can be viewed and reactivated
- [ ] Test messages can be sent to a selected region's active on-call participant

### Evaluation View
- [ ] Overall planning report shows day-based view of all regions and participants
- [ ] On-call region report shows duty roster for a selected region
- [ ] On-call participant report shows assignments for a selected participant
- [ ] Conflicts shown in red, multiple on-call shifts shown in orange
- [ ] Reports exportable as CSV and XML

### Escalation
- [ ] Escalation chain follows order: regular participant → period escalation → region escalation
- [ ] Escalation triggered when regular on-call participant cannot be reached (based on eCall response status)

## API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| - | UeLS-zentras interface | Receives alarm data from UeLS-zentras systems |
| - | F24 eCall HTTP/HTTPS | Sends SMS/pager messages via F24 Schweiz AG |

*Note: Specific REST/SOAP API endpoint details are not specified in requirements.*

## UI Elements
- **Meta Area** – Application icons (Alarms, Suppressed DP, Current on-call schedule, Detach, Dispatcher), navigation buttons (Start, Back, Forward), user info, logout, settings, print, help, system info
- **Navigation Area** – View selection (Planning, Configuration, Appointment, Message, Evaluation, System Configuration, Document) and tab selection within views
- **Process Frame** – Main content area displaying selected masks/screens
- **Alarm Frame** – Collapsible bottom bar showing active internal alarms (priority 1) and faults (priority 2)
- **Quick Access Icons** – Toolbar icons for common actions
- **Context Menus** – Right-click menus on alarm lists and message lists for navigation between related views

## Validation Rules
| Field | Rule |
|-------|------|
| Region Name | Unique, max 20 alphanumeric characters, not editable after creation |
| Alarm Medium Identification | Unique, not editable after creation |
| Alarm Medium Number | Only numbers allowed |
| System Identification | Unique, not editable after creation |
| SMS/Pager Message Text | Max 154 characters (160 with timestamp) |
| Auto-Pause Time | Format hh:mm |
| Alarm Delay Time | Format hh:mm (from/to), delay in seconds |
| Shipping Delay Time | Format hh:mm (from/to), delay in seconds |
| Absence Date | From/To date range required |
| Holiday Date | Valid date required |
| On-call Period | Must be part of an on-call basic plan |

## Error Messages
| Code / Scenario | Message |
|-----------------|---------|
| Different on-call participant | Warning displayed when saving a period if participant differs from planned |
| Holiday overlap | Warning when on-call period includes a public holiday |
| Paused region | "Pager activated?" note when attempting to send a test message to a paused region |
| eCall error 5112 | Invalid phone number |
| eCall error 5111 | Text too long |
| eCall error 1000 | Connection interrupted |
| eCall error 1001 | Timeout: The page could not be sent successfully |
| eCall error 5155 | Traffic too heavy |
| eCall error 5510 | Too many messages to the same recipient |
| eCall error 5511 | Too many messages to the same recipient with the same text |
| eCall error 5512 | Job ID already assigned by this sender |
| eCall error 5513 | Callback, address, or parts of message text on blacklist |
| eCall error 5514 | Blocked by outgoing filter rules |
| Plausibility error | Symbol (⚠) displayed next to input field with pop-up describing the error |

## Key Object Model
| Object Type | Description |
|-------------|-------------|
| Alarm Medium | Cell phone or pager with number and type (SMS/Pager) |
| LDAP User | User authenticated via LDAP or SSO |
| On-call Participant | LDAP user assigned to one or more alarm media |
| Absence Planning | Recorded absences per participant |
| On-call Region | Grouping of UeLS-zentras systems for alarm routing |
| On-call Period | A duty period (typically one week) within a basic plan |
| On-call Basic Plan | Defines on-call duty for a time interval and region |
| Switch-on/off Times | Auto-pause activation/deactivation schedules |
| Public Holidays | Holiday dates per region for planning warnings |
| Escalation Policy | Backup on-call chain (period-level and region-level) |
| Alarm Delay | Configuration to suppress transient alarms |
| Shipping Delay | Configuration to collect and defer alarm delivery |
