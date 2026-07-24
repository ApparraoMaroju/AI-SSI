# Story: ALAMOS Phase 1 – Process Situation Reports Through IPL

| Field | Value |
|--------|-------|
| **Story ID** | US-ADAPTER-ALAMOS-004 |
| **Story Name** | ALAMOS Phase 1 – Process Situation Reports Through IPL |
| **Actor** | FacadeService (ALAMOS Adapter) |
| **Goal** | Process Situation Report events through synchronous IPL integration |
| **Business Value** | Enables incoming ALAMOS Situation Reports to be transformed into the corresponding IPL request format, processed through existing IPL interfaces, and acknowledged synchronously back to ALAMOS FE2 without requiring changes to IPL. |
| **Jira Ticket** | IPL-26912 – Process Situation Reports Through IPL *(Open)* |

---

## User Story

**As** a FacadeService within the ALAMOS Adapter,  
**I want** to transform `incident.situation_report_received` Domain Events into IPL-compatible requests and invoke IPL synchronously,  
**So that** Situation Reports can be processed by IPL and the resulting business outcome can be returned to ALAMOS FE2.

---

## Key Scenarios & Variations

### Happy Path
- Valid `incident.situation_report_received` event received.
- Event successfully mapped to the corresponding IPL request structure.
- IPL `POST /einsatztransfer/erzeugeEinsatzmeldung` endpoint is reachable and processes the request successfully.
- IPL returns a successful response.
- Successful IPL response is propagated back to ALAMOS FE2 through the Adapter.

### Validation & Mapping Failures
- Required event data is missing or invalid for IPL request generation.

### IPL Business & Technical Failures
- IPL returns a business fault response.
- IPL returns a technical fault response.
- IPL endpoint is unavailable or times out.
- Fault or technical error response is propagated back to ALAMOS FE2 through the Adapter.

---

## Acceptance Criteria

### Event Processing
- The FacadeService must receive `incident.situation_report_received` events for IPL processing.
- The FacadeService must validate that all required data for IPL request generation is available before invoking IPL.
- The FacadeService must map Situation Report event data to the corresponding IPL request structure.

### IPL Integration
- The FacadeService must invoke the IPL `POST /einsatztransfer/erzeugeEinsatzmeldung` endpoint synchronously.
- The FacadeService must process successful responses returned by IPL.
- The FacadeService must process business fault responses returned by IPL.
- The FacadeService must process technical fault responses returned by IPL.
- The FacadeService must handle communication failures such as connectivity issues, timeouts, or unavailable IPL endpoints.

### Response Handling
- The FacadeService must propagate successful IPL processing results back through the Adapter to ALAMOS FE2.
- The FacadeService must propagate IPL fault and technical error responses back through the Adapter to ALAMOS FE2.
- The response returned to ALAMOS FE2 must accurately reflect the final processing result received from IPL.

### Validation Rules
- Only successfully validated and mapped events must be submitted to IPL for processing.