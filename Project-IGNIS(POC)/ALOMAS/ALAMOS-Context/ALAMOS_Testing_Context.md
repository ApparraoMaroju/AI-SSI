# Testing Context

## Scope
- **In Scope:**
  - Alerting flow, including squad information (`<squads>`) — legacy path (IPL → Facade Service (LEGACY) → ALAMOS Gateway → ALAMOS FE2). Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`, `US-INTEGRATION-E2E-001.md`
  - Continuous Mission Updates — legacy path through the ALAMOS Gateway. Source: `US-ALAMOS-GW-002.md`, `US-INTEGRATION-E2E-001.md`
  - Situation Reports — event-driven path (ALAMOS FE2 → Adapter → Domain Event → FacadeService → IPL). Source: `US-ADAPTER-ALAMOS-001.md` – `US-ADAPTER-ALAMOS-004.md`, `US-INTEGRATION-E2E-001.md`
  - Retry, DLQ, error-handling, and recovery behavior across all ALAMOS flows. Source: `US-ADAPTER-RELIABILITY-001.md`
  - Mock-mode functional and integration testing of the ALAMOS Gateway (without live ALAMOS FE2). Source: `US-ALAMOSGW-MOCK-001.md`
  - Build-time automated unit and integration tests for the Adapter and ALAMOS Gateway. Source: `US-PLATFORM-CICD-001.md`
- **Out of Scope:**
  - IPL-to-ALAMOS flow for Situation Reports (explicitly not supported in Release 26.3 per Epic 6.1/Phase-1 scope). Source: `ALAMOS Integration – Phase 1.md`
  - Dispatch correlation logic for Continuous Mission Updates (not introduced in this release). Source: `US-ALAMOS-GW-002.md`
  - Asynchronous infrastructure testing (Inbox, Outbox, Process Tracker, Event Bus, standalone EES) — not implemented in Release 26.3. Source: `ALAMOS Integration – Phase 1.md`

## Test Data
Not Available in Source Documents — no concrete test data values (e.g., sample payloads, specific `external_id`/`incident_number`/`call_sign` values, credentials) are provided in the input files. The following data *fields* are referenced and would require test data to be defined:

| Data Type | Value | Purpose |
|-----------|-------|---------|
| `external_id` | Not Available in Source Documents | Primary incident correlation key (US-ADAPTER-ALAMOS-002) |
| `incident_number` | Not Available in Source Documents | Fallback incident correlation key (US-ADAPTER-ALAMOS-002) |
| `call_sign` | Not Available in Source Documents | Authoring resource identifier, with fallback handling (US-ADAPTER-ALAMOS-002) |
| `<squads>` (squad information) | Not Available in Source Documents | Alerting squad data — single and multiple entries (US-ALAMOS-GW-003) |
| Situation Report payload (`incident.situation_report_received/v1`) | Example structure documented (see below), no concrete sample values | Domain Event minimum payload (`ALAMOS Integration – Phase 1.md`) |

Example documented payload structure (illustrative field names only, not populated test data):
```json
{
  "event_id": "uuid",
  "event_type": "incident.situation_report_received",
  "occurred_at": "2026-01-01T12:00:00Z",
  "source_system": "ALAMOS",
  "tenant_id": "string",
  "incident": { "external_id": "string", "incident_number": "string" },
  "authoring_resource": { "external_resource_id": "string", "call_sign": "string" },
  "situation_report": { "text": "string", "reported_at": "2026-01-01T12:00:00Z" }
}
```
Source: `ALAMOS Integration – Phase 1.md`

## Test Environment
- **Browser:** Not Available in Source Documents (no UI/browser-based testing is documented; this is a backend/system integration).
- **Device:** Not Available in Source Documents.
- **OS:** Not Available in Source Documents.
- **Mock Environment:** The ALAMOS Gateway can run standalone in a configurable mock mode, returning predefined success/error responses, enabling development and testing without live ALAMOS FE2 connectivity. Source: `US-ALAMOSGW-MOCK-001.md`
- **Build/CI Environment:** Automated unit and integration tests run as part of the build pipeline; failed builds/tests prevent artifact generation. Source: `US-PLATFORM-CICD-001.md`

## Dependencies
- ALAMOS Gateway (mock mode) must be available and configured for Alerting and Continuous Mission Update testing without live ALAMOS FE2. Source: `US-ALAMOSGW-MOCK-001.md`
- IPL endpoints (`erzeugeEinsatzmeldung`, and Alerting/Mission Update legacy interfaces) must be reachable for Situation Report and legacy flow testing. Source: `US-ADAPTER-ALAMOS-004.md`, `ALAMOS Integration – Phase 1.md`
- Existing Retry & DLQ mechanisms must be operational/testable across flows. Source: `US-ADAPTER-RELIABILITY-001.md`
- Build/CI pipeline templates updated to support ALAMOS Phase 1 changes. Source: `US-PLATFORM-CICD-001.md`

## Known Issues
- Open architectural clarification: transport protocol between Adapter and EES (REST+JSON vs. SOAP+XML) is not fully finalized in the source document (REST+JSON marked ✅, SOAP+XML marked ❌, but listed under "Clarifications Required"). This could affect future (26.4) test design but does not block 26.3 testing since EES is out of scope for this release. Source: `ALAMOS Integration – Phase 1.md`
- No workaround information documented. Not Available in Source Documents.

---

# Additional Testing Information

## Functional Testing Scope
1. Situation Report ingestion, validation, Domain Event generation, FacadeService routing, and IPL invocation (US-ADAPTER-ALAMOS-001 – 004).
2. Legacy Alerting with and without squad information (US-ALAMOS-GW-001, US-ALAMOS-GW-003).
3. Legacy Continuous Mission Updates for all four triggers: incident status, resource status, keyword, and location changes (US-ALAMOS-GW-002).
4. Mock-mode functional validation of Alerting (with squads) and Continuous Mission Updates (US-ALAMOSGW-MOCK-001).
5. Retry and DLQ behavior across Situation Report, Alerting, and Continuous Mission Update paths (US-ADAPTER-RELIABILITY-001).
6. Full end-to-end validation across Adapter, FacadeService, IPL, ALAMOS Gateway, and ALAMOS FE2 (US-INTEGRATION-E2E-001).

Source: All `US-*.md` files.

## Test Scenarios

### Positive Scenarios
- Valid Situation Report received, validated, transformed into `incident.situation_report_received`, processed successfully by IPL, and acknowledged to ALAMOS FE2. Source: `US-ADAPTER-ALAMOS-001.md` – `US-ADAPTER-ALAMOS-004.md`
- Incident correlation using `external_id`. Source: `US-ADAPTER-ALAMOS-002.md`
- `call_sign` available and mapped directly (no fallback needed). Source: `US-ADAPTER-ALAMOS-002.md`
- Valid Alerting request (with and without `<squads>`) successfully forwarded to ALAMOS FE2 with successful acknowledgement. Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`
- Multiple squads supplied in a single Alerting request. Source: `US-ALAMOS-GW-003.md`
- Each of the four Continuous Mission Update triggers (incident status, resource status, keyword, location) successfully forwarded and acknowledged. Source: `US-ALAMOS-GW-002.md`
- Successful processing after a transient failure is retried. Source: `US-ADAPTER-RELIABILITY-001.md`
- ALAMOS Gateway mock mode returns predefined success responses. Source: `US-ALAMOSGW-MOCK-001.md`

### Negative Scenarios
- Situation Report violates the ALAMOS contract or is missing mandatory fields → rejected. Source: `US-ADAPTER-ALAMOS-001.md`
- Invalid request headers/authentication, unsupported HTTP method, or invalid content type → technical error response. Source: `US-ADAPTER-ALAMOS-001.md`
- Failed IPL processing result → synchronous failure acknowledgment returned to ALAMOS FE2. Source: `US-ADAPTER-ALAMOS-001.md`
- Required event attributes missing/invalid → Domain Event generation fails. Source: `US-ADAPTER-ALAMOS-002.md`
- Incident correlation, resource mapping, or event generation cannot complete → error returned. Source: `US-ADAPTER-ALAMOS-002.md`
- Invalid FacadeService routing configuration or unsupported capability. Source: `US-ADAPTER-ALAMOS-003.md`
- IPL returns business fault or technical fault response; IPL endpoint unavailable/times out. Source: `US-ADAPTER-ALAMOS-004.md`
- ALAMOS FE2 returns a business or technical error for Alerting or Continuous Mission Updates. Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-002.md`, `US-ALAMOS-GW-003.md`
- Invalid or malformed Alerting requests rejected. Source: `US-ALAMOS-GW-001.md`
- Business validation error returned by IPL or ALAMOS → must NOT trigger unnecessary retries. Source: `US-ADAPTER-RELIABILITY-001.md`
- Retry limit exceeded → message routed to existing DLQ. Source: `US-ADAPTER-RELIABILITY-001.md`
- Mock mode configurable error responses for negative testing. Source: `US-ALAMOSGW-MOCK-001.md`

### Boundary Conditions
Not Available in Source Documents (no explicit boundary values — e.g., payload size limits, field length limits, rate limits — are documented in the source files).

### Edge Cases
- `call_sign` missing/invalid on a reporting resource → fallback handling logic applied (fallback rule details not documented). Source: `US-ADAPTER-ALAMOS-002.md`
- `external_id` unavailable → fallback to `incident_number` for incident correlation. Source: `US-ADAPTER-ALAMOS-002.md`
- Alerting request with no squad information (must remain backward compatible). Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`
- Temporary communication failure between ALAMOS Gateway and ALAMOS FE2 followed by successful retry. Source: `US-ADAPTER-RELIABILITY-001.md`

## Integration Testing
- Full Alerting flow: IPL → Facade Service (LEGACY) → ALAMOS Gateway → ALAMOS FE2, including squad information, with responses propagated back to IPL. Source: `US-INTEGRATION-E2E-001.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`
- Full Continuous Mission Update flow through the ALAMOS Gateway. Source: `US-INTEGRATION-E2E-001.md`
- Full Situation Report flow: ALAMOS FE2 → Adapter → Domain Event generation → FacadeService → IPL, including acknowledgement propagation. Source: `US-INTEGRATION-E2E-001.md`, `Situation Reports (EVENT).svg`
- Retry and DLQ mechanisms validated end-to-end using representative failure scenarios, with no unexpected message loss. Source: `US-ADAPTER-RELIABILITY-001.md`, `US-INTEGRATION-E2E-001.md`
- Integration/connectivity testing performed using the ALAMOS Gateway mock mode without requiring ALAMOS FE2 access. Source: `US-ALAMOSGW-MOCK-001.md`

## Regression Scope
- Existing Alerting functionality (without squad information) must remain unaffected and backward compatible. Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`
- Existing Continuous Mission Update functionality must remain backward compatible with the current gateway implementation. Source: `US-ALAMOS-GW-002.md`
- Existing retry, DLQ, logging, and monitoring capabilities must remain functional after changes. Source: `US-ADAPTER-RELIABILITY-001.md`
- Mock-mode configuration must not impact normal (non-mock) gateway operation when disabled. Source: `US-ALAMOSGW-MOCK-001.md`

## Risks (Testing-Related)
- Synchronous coupling between Adapter → FacadeService → IPL means test execution/availability depends on real-time IPL endpoint availability. Source: `ALAMOS Integration – Phase 1.md`
- No Inbox/Outbox/Event Bus/Process Tracker in 26.3 — failure/retry testing must rely on existing (legacy) retry/DLQ mechanisms only, without durable event queuing at the Domain Event level. Source: `ALAMOS Integration – Phase 1.md`
- Domain Events are not persisted in 26.3, which may limit ability to inspect/replay events during test investigation. Source: `ALAMOS Integration – Phase 1.md`

## Test Assumptions
Not Available in Source Documents (no assumptions are explicitly labeled as testing assumptions in the source files).

## Traceability to Requirements
| Test Area | Related Feature / Requirement Source |
|---|---|
| Situation Report receive/validate testing | `US-ADAPTER-ALAMOS-001.md` |
| Domain Event generation testing | `US-ADAPTER-ALAMOS-002.md` |
| FacadeService routing testing | `US-ADAPTER-ALAMOS-003.md` |
| FacadeService IPL processing testing | `US-ADAPTER-ALAMOS-004.md` |
| Retry/DLQ testing | `US-ADAPTER-RELIABILITY-001.md` |
| Legacy Alerting testing | `US-ALAMOS-GW-001.md` |
| Continuous Mission Update testing | `US-ALAMOS-GW-002.md` |
| Squad information testing | `US-ALAMOS-GW-003.md` |
| Mock Gateway testing | `US-ALAMOSGW-MOCK-001.md` |
| End-to-end integration testing | `US-INTEGRATION-E2E-001.md` |
| Build/CI automated test execution | `US-PLATFORM-CICD-001.md` |

## Conflicts / Observations Detected (Testing-Specific)
- `US-INTEGRATION-E2E-001.md` labels the Alerting, Continuous Mission Update, and Situation Report features as "US-ALAMOS-100", "US-ALAMOS-200", and "US-ALAMOS-300" respectively, matching the naming used in `ALAMOS Integration – Phase 1.md` ("US-100", "US-200", "US-300"), but these differ from the Jira-tracked story IDs used elsewhere (`US-ADAPTER-ALAMOS-00x`, `US-ALAMOS-GW-00x`). This is recorded as a naming/traceability observation, not resolved as a single canonical ID scheme in the source documents.
