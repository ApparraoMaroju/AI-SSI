# Story: ALAMOS Phase 1 – Implement FacadeService for IPL Integration

| Field | Value |
|--------|-------|
| **Story ID** | US-ADAPTER-ALAMOS-003 |
| **Story Name** | ALAMOS Phase 1 – Implement FacadeService for IPL Integration |
| **Actor** | FacadeService (ALAMOS Adapter) |
| **Goal** | Process Situation Report Domain Events and invoke IPL |
| **Business Value** | Enables the ALAMOS Adapter to centralize capability routing and processing through a standalone FacadeService, providing a migration layer between Adapter-generated requests/events and existing IPL interfaces while remaining extractable to EES in a future release. |
| **Jira Ticket** | IPL-26911 – Implement FacadeService for IPL Integration *(Open)* |

---

## User Story

**As** a FacadeService within the ALAMOS Adapter,  
**I want** to provide a synchronous routing and processing layer for ALAMOS capabilities,  
**So that** requests can be routed through the appropriate processing path and integrated with existing IPL interfaces without introducing additional infrastructure components.

---

## Key Scenarios & Variations

### Happy Path
- Valid `incident.situation_report_received` event received.
- Valid request/event is received and routed successfully.
- Routing resolves the capability to **LEGACY** or **EVENT** processing.
- Processing is executed synchronously through the configured integration path.
- Processing succeeds and a response is returned.

### Routing & Configuration Failures
- Invalid routing configuration is detected.
- Unsupported capability is detected.

### Processing Failures
- Processing fails and an error response is propagated to the caller.

---

## Acceptance Criteria

### FacadeService Implementation
- The FacadeService shall be implemented inside the ALAMOS Adapter as a standalone and extractable component.
- The FacadeService shall receive requests and Domain Events generated within the Adapter.

### Routing
- The FacadeService shall determine the appropriate processing path using capability-specific routing configuration.
- The FacadeService shall support both **LEGACY** and **EVENT** processing modes where applicable.

### Processing
- The FacadeService shall coordinate synchronous processing and return the result to the calling component.
- The FacadeService shall propagate success and failure responses back to the Adapter.

### Architecture Constraints
- The FacadeService shall be implemented without introducing an Inbox, Outbox, Event Bus, Process Tracker, or persistence mechanism.
- The FacadeService shall remain fully extractable to EES as part of the planned **Release 26.4** migration.