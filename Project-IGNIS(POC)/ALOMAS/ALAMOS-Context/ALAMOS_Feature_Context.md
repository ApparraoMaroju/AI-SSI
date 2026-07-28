# Feature Context: ALAMOS Integration – Release 26.3

## Overview
This document covers all ALAMOS Release 26.3 features: Situation Report handling (Adapter + FacadeService), legacy Alerting and Continuous Mission Updates (ALAMOS Gateway), the ALAMOS Gateway mock service, end-to-end integration testing, and the CI/CD build pipeline. Each feature below follows the template structure (Overview, User Stories, Acceptance Criteria, API Endpoints, UI Elements, Validation Rules, Error Messages).
Source: `ALAMOS Integration – Phase 1.md`, all `US-*.md` files.

---

## Feature: Situation Reports – Adapter Receive & Validate (US-ADAPTER-ALAMOS-001)

### Overview
The Adapter receives Situation Reports from ALAMOS FE2, validates them per the ALAMOS contract, and returns a synchronous acknowledgment reflecting the final IPL processing result. Jira: IPL-26909 (In Progress).
Source: `US-ADAPTER-ALAMOS-001.md`

### User Stories
- As an Adapter Integration system, I want to receive and validate Situation Reports submitted by ALAMOS FE2, so that compliant requests can be accepted for further processing and ALAMOS FE2 receives a synchronous acknowledgment reflecting the final IPL processing outcome.

### Acceptance Criteria
- [ ] The Adapter exposes REST endpoint(s) capable of receiving Situation Reports from ALAMOS FE2.
- [ ] The Adapter validates incoming requests against the ALAMOS contract and rejects non-compliant requests with a clear validation error.
- [ ] The Adapter performs initial payload validation before further processing.
- [ ] The Adapter verifies required request headers and technical prerequisites before processing.
- [ ] The Adapter rejects unsupported HTTP methods and invalid content types with appropriate technical error responses.
- [ ] The Adapter accepts valid Situation Reports and forwards them for downstream processing, waiting for the final IPL processing result.
- [ ] The Adapter returns a synchronous success acknowledgment when IPL processing completes successfully.
- [ ] The Adapter returns a synchronous failure acknowledgment when IPL processing fails or returns an error, accurately reflecting the final IPL processing result.

### API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| REST (exact method/path not specified) | Adapter inbound Situation Report endpoint | Receives Situation Reports from ALAMOS FE2 ("Situation Report (REST)" per sequence diagram) |

Source: `US-ADAPTER-ALAMOS-001.md`, `Situation Reports (EVENT).svg`

### UI Elements
Not Available in Source Documents (backend integration feature; no UI documented).

### Validation Rules
| Field/Aspect | Rule |
|---|---|
| ALAMOS contract compliance | Request must comply with the ALAMOS contract; non-compliant requests rejected |
| Mandatory fields | Missing mandatory fields cause rejection |
| Request headers/authentication | Must be present and valid before processing |
| HTTP method | Unsupported methods rejected |
| Content type | Invalid content types rejected |

### Error Messages
Not Available in Source Documents (specific error codes/message text not documented). Documented error *categories*: contract violation, missing mandatory fields, invalid headers/authentication, unsupported HTTP method, invalid content type, failed IPL processing result.

---

## Feature: Situation Reports – Domain Event Generation (US-ADAPTER-ALAMOS-002)

### Overview
Transforms validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event, with incident correlation and resource mapping. Jira: IPL-26910 (Open).
Source: `US-ADAPTER-ALAMOS-002.md`

### User Stories
- As an Adapter Integration system, I want to transform validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event, so that Situation Reports can be consumed consistently by downstream systems using a standardized event model with accurate incident correlation and resource mapping.

### Acceptance Criteria
- [ ] The Adapter transforms validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event, containing all required attributes and metadata.
- [ ] Incident correlation uses `external_id` when available.
- [ ] Incident correlation uses `incident_number` as a fallback when `external_id` is not available.
- [ ] Reporting resources are mapped from the ALAMOS payload into the canonical event structure.
- [ ] `call_sign` fallback handling is applied when a reporting resource does not provide a valid `call_sign`.
- [ ] The generated event is validated prior to publication or downstream processing.
- [ ] An appropriate error is returned when incident correlation, resource mapping, or event generation cannot be completed successfully.
- [ ] The generated event conforms to the `incident.situation_report_received/v1` contract and is ready for downstream consumption.

### API Endpoints (if applicable)
Not Available in Source Documents (this feature operates on data internally transformed after ingestion by US-ADAPTER-ALAMOS-001; no separate endpoint documented).

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Field | Rule |
|---|---|
| `external_id` | Primary key for incident correlation |
| `incident_number` | Fallback key for incident correlation when `external_id` unavailable |
| `call_sign` | Fallback handling applied when missing/invalid (fallback logic details: Not Available in Source Documents) |
| Event payload | Must contain all required attributes/metadata of `incident.situation_report_received/v1` before publication |

### Error Messages
Not Available in Source Documents (specific codes/messages not documented). Documented error *categories*: missing/invalid required event attributes; mapping or validation failures during canonical event payload generation.

---

## Feature: FacadeService – Routing Layer (US-ADAPTER-ALAMOS-003)

### Overview
A standalone, extractable FacadeService inside the ALAMOS Adapter routes requests/events to LEGACY or EVENT processing paths and coordinates synchronous processing. Jira: IPL-26911 (Open).
Source: `US-ADAPTER-ALAMOS-003.md`

### User Stories
- As a FacadeService within the ALAMOS Adapter, I want to provide a synchronous routing and processing layer for ALAMOS capabilities, so that requests can be routed through the appropriate processing path and integrated with existing IPL interfaces without introducing additional infrastructure components.

### Acceptance Criteria
- [ ] The FacadeService is implemented inside the ALAMOS Adapter as a standalone and extractable component.
- [ ] The FacadeService receives requests and Domain Events generated within the Adapter.
- [ ] The FacadeService determines the appropriate processing path using capability-specific routing configuration.
- [ ] The FacadeService supports both LEGACY and EVENT processing modes where applicable.
- [ ] The FacadeService coordinates synchronous processing and returns the result to the calling component.
- [ ] The FacadeService propagates success and failure responses back to the Adapter.
- [ ] The FacadeService is implemented without an Inbox, Outbox, Event Bus, Process Tracker, or persistence mechanism.
- [ ] The FacadeService remains fully extractable to EES as part of Release 26.4.

### API Endpoints (if applicable)
Not Available in Source Documents (internal routing component, not directly externally exposed).

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Aspect | Rule |
|---|---|
| Routing configuration | Must resolve capability to LEGACY or EVENT path; invalid/unsupported configuration is an error condition |

### Error Messages
Not Available in Source Documents. Documented error *categories*: invalid routing configuration, unsupported capability, processing failure propagated to caller.

---

## Feature: FacadeService – IPL Processing (US-ADAPTER-ALAMOS-004)

### Overview
Transforms `incident.situation_report_received` Domain Events into IPL-compatible requests and invokes IPL synchronously, propagating results back to ALAMOS FE2. Jira: IPL-26912 (Open).
Source: `US-ADAPTER-ALAMOS-004.md`

### User Stories
- As a FacadeService within the ALAMOS Adapter, I want to transform `incident.situation_report_received` Domain Events into IPL-compatible requests and invoke IPL synchronously, so that Situation Reports can be processed by IPL and the resulting business outcome can be returned to ALAMOS FE2.

### Acceptance Criteria
- [ ] The FacadeService receives `incident.situation_report_received` events for IPL processing.
- [ ] The FacadeService validates that all required data for IPL request generation is available before invoking IPL.
- [ ] The FacadeService maps Situation Report event data to the corresponding IPL request structure.
- [ ] The FacadeService invokes the IPL `POST /einsatztransfer/erzeugeEinsatzmeldung` endpoint synchronously.
- [ ] The FacadeService processes successful, business fault, and technical fault responses returned by IPL.
- [ ] The FacadeService handles communication failures (connectivity issues, timeouts, unavailable IPL endpoint).
- [ ] Successful IPL processing results are propagated back through the Adapter to ALAMOS FE2.
- [ ] IPL fault and technical error responses are propagated back through the Adapter to ALAMOS FE2, accurately reflecting the final processing result.
- [ ] Only successfully validated and mapped events are submitted to IPL for processing.

### API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/einsatztransfer/erzeugeEinsatzmeldung` (IPL, SOAP) | Processes the Situation Report / creates the mission report ("Einsatzmeldung") in IPL |

Source: `US-ADAPTER-ALAMOS-004.md`, `Situation Reports (EVENT).svg`

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Aspect | Rule |
|---|---|
| Required IPL request data | Must be validated as available before invoking IPL |
| Event-to-request mapping | Situation Report event data must be mapped to the IPL request structure |

### Error Messages
Not Available in Source Documents. Documented error *categories*: missing/invalid required event data, IPL business fault, IPL technical fault, IPL endpoint unavailable/timeout.

---

## Feature: Reliability – Retry & DLQ Validation (US-ADAPTER-RELIABILITY-001)

### Overview
Validates existing retry, DLQ, error-handling, logging, and recovery mechanisms across Situation Report, Alerting, and Continuous Mission Update flows. Jira: IPL-26914 (Open).
Source: `US-ADAPTER-RELIABILITY-001.md`

### User Stories
- As an Adapter Integration system, I want to validate retry, DLQ, error-handling, and recovery behavior across ALAMOS integration flows, so that communication failures, processing errors, and external system unavailability are handled consistently, recoverable failures are retried appropriately, and unrecoverable failures are traceable through the existing DLQ mechanism.

### Acceptance Criteria
- [ ] Existing retry, error-handling, and DLQ mechanisms are validated for Situation Report, Alerting, and Continuous Mission Update flows.
- [ ] Recoverable communication failures are processed according to existing retry policies.
- [ ] Messages process successfully when transient failures resolve within configured retry limits.
- [ ] Messages route to the existing DLQ when retry limits are exceeded.
- [ ] Business validation errors do not trigger unnecessary retries.
- [ ] Technical failures (connectivity, unavailable endpoints, timeouts) are handled consistently.
- [ ] Retry attempts, DLQ events, and processing failures are logged with sufficient diagnostic information.
- [ ] Existing monitoring/operational logging capabilities remain functional.
- [ ] Success and fault responses are propagated correctly to the originating caller.
- [ ] End-to-end failure scenarios demonstrate correct retry and DLQ behavior across all supported ALAMOS capabilities.

### API Endpoints (if applicable)
Not Available in Source Documents (this is a cross-cutting reliability validation feature, not a new endpoint).

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Aspect | Rule |
|---|---|
| Retry limits | Configured retry limits determine whether a message is retried or routed to DLQ (exact limit values: Not Available in Source Documents) |
| Business validation errors | Must not trigger retries |

### Error Messages
Not Available in Source Documents. Documented error *categories*: temporary communication failure, communication timeout, unavailable endpoint, business validation error, technical fault, retry-limit-exceeded (→ DLQ).

---

## Feature: ALAMOS Gateway – Legacy Alerting (US-ALAMOS-GW-001)

### Overview
The existing ALAMOS Gateway continues processing Alerting requests, extended to support squad information (`<squads>`), preserving IPL compatibility. Jira: IPL-26913 (In Progress).
Source: `US-ALAMOS-GW-001.md`

### User Stories
- As an ALAMOS Gateway, I want to receive Alerting requests from IPL and process them using the existing ALAMOS integration path, so that Alerting messages, including squad information, can be delivered to ALAMOS FE2 while maintaining full backward compatibility with the current implementation.

### Acceptance Criteria
- [ ] The ALAMOS Gateway receives Alerting requests from IPL using the existing integration path.
- [ ] The ALAMOS Gateway supports processing of Alerting requests containing squad information (`<squads>`).
- [ ] The ALAMOS Gateway correctly maps squad information to the ALAMOS request format.
- [ ] The ALAMOS Gateway preserves compatibility with existing Alerting requests without squad information.
- [ ] The ALAMOS Gateway forwards Alerting requests to ALAMOS FE2 successfully.
- [ ] The ALAMOS Gateway processes success, business fault, and technical fault responses returned by ALAMOS FE2.
- [ ] The ALAMOS Gateway handles communication failures (connectivity, unavailable endpoints, timeouts).
- [ ] The ALAMOS Gateway propagates the final processing result back to IPL, accurately reflecting the ALAMOS FE2 response.

### API Endpoints (if applicable)
| Method | Endpoint | Description |
|--------|----------|-------------|
| SOAP | `AlarmRequest` (IPL → ALAMOS Gateway) | Legacy Alerting request, including `<squads>` |
| REST | ALARM API (ALAMOS Gateway → ALAMOS FE2) | Forwards Alerting request to ALAMOS FE2 |

Source: `ALAMOS Integration – Phase 1.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Field | Rule |
|---|---|
| `<squads>` | Must be correctly mapped to the ALAMOS request format when present |
| Alerting request without squads | Must continue to be processed successfully (backward compatibility) |

### Error Messages
Not Available in Source Documents. Documented error *categories*: business error, technical error, communication timeout/connectivity failure, invalid/malformed Alerting request (rejected).

---

## Feature: ALAMOS Gateway – Continuous Mission Updates (US-ALAMOS-GW-002)

### Overview
Processes and forwards Continuous Mission Updates from IPL to ALAMOS via the existing gateway, without new event-driven infrastructure or dispatch correlation. Jira: IPL-26934 (Open).
Source: `US-ALAMOS-GW-002.md`

### User Stories
- As an ALAMOS Gateway, I want to process and forward Continuous Mission Updates received from IPL, so that ALAMOS receives ongoing mission changes and remains synchronized with operational updates occurring within IGNIS.

### Acceptance Criteria
- [ ] The ALAMOS Gateway processes Continuous Mission Update requests originating from IPL.
- [ ] The ALAMOS Gateway supports configured update triggers: incident status changes, resource status changes, keyword changes, location changes.
- [ ] The ALAMOS Gateway transforms and forwards update requests to ALAMOS using the existing integration path.
- [ ] The ALAMOS Gateway processes successful, business fault, and technical fault responses returned by ALAMOS.
- [ ] The ALAMOS Gateway handles communication failures (timeouts, unavailable endpoints, connectivity issues).
- [ ] The ALAMOS Gateway propagates the final processing result back to IPL, accurately reflecting the ALAMOS response.
- [ ] Existing Continuous Mission Update functionality remains backward compatible with the current gateway implementation.

### API Endpoints (if applicable)
Not Available in Source Documents (specific endpoint path/method for Continuous Mission Updates not documented; only that it uses "the existing gateway implementation").

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Trigger | Rule |
|---|---|
| Incident status change | Triggers a Continuous Mission Update |
| Resource status change | Triggers a Continuous Mission Update |
| Keyword change | Triggers a Continuous Mission Update |
| Location change | Triggers a Continuous Mission Update |

### Error Messages
Not Available in Source Documents. Documented error *categories*: business error, technical error, communication timeout/connectivity failure.

---

## Feature: ALAMOS Gateway – Squad Information Extension (US-ALAMOS-GW-003)

### Overview
Enables the ALAMOS Gateway to process and forward squad information within Alerting requests. Jira: IPL-26936 (Open).
Source: `US-ALAMOS-GW-003.md`

### User Stories
- As an ALAMOS Gateway, I want to process squad information included in Alerting requests, so that ALAMOS receives complete alerting messages containing both alarm details and associated squad information.

### Acceptance Criteria
- [ ] The ALAMOS Gateway supports processing of squad information included in Alerting requests.
- [ ] Squad information is extracted from the IPL Alerting request and mapped to the ALAMOS message structure.
- [ ] Multiple squad entries are supported where provided by IPL.
- [ ] Alerting requests without squad information continue to be processed successfully.
- [ ] Existing Alerting functionality remains backward compatible.
- [ ] The ALAMOS Gateway forwards the enriched Alerting request to ALAMOS FE2 using the existing integration path.
- [ ] Success, business fault, and technical fault responses returned by ALAMOS FE2 are processed correctly.
- [ ] Acknowledgements are propagated back to IPL without loss of information.
- [ ] End-to-end testing verifies squad information is correctly transmitted to ALAMOS FE2.

### API Endpoints (if applicable)
Same as US-ALAMOS-GW-001 (SOAP `AlarmRequest` inbound; REST ALARM API outbound to ALAMOS FE2). Source: `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Field | Rule |
|---|---|
| Squad information | Extracted and mapped to ALAMOS message structure; multiple entries supported |
| No squad information | Request must still process successfully |

### Error Messages
Not Available in Source Documents. Documented error *categories*: business error, technical error returned by ALAMOS FE2.

---

## Feature: ALAMOS Gateway – Mock Service (US-ALAMOSGW-MOCK-001)

### Overview
The ALAMOS Gateway supports a configurable mock mode for development, integration testing, and validation without live ALAMOS FE2 connectivity. Jira: IPL-26908 (In Progress).
Source: `US-ALAMOSGW-MOCK-001.md`

### User Stories
- As an integration team, I want the existing ALAMOS Gateway to run as a standalone application in mock mode, so that ALAMOS integration flows can be developed, validated, and tested independently of external ALAMOS FE2 infrastructure.

### Acceptance Criteria
- [ ] The ALAMOS Gateway supports execution in a configurable mock mode.
- [ ] The ALAMOS Gateway is executable as a standalone application for development/testing.
- [ ] Mock mode allows predefined success responses without requiring a connection to ALAMOS FE2.
- [ ] Mock mode supports configurable error responses for negative test scenarios.
- [ ] Alerting requests, including squad information (`<squads>`), are executable/testable in mock mode.
- [ ] Continuous Mission Update requests are executable/testable in mock mode.
- [ ] Mock-mode configuration does not impact normal gateway operation when disabled.
- [ ] Mock-mode setup supports integration and end-to-end testing for Release 26.3.

### API Endpoints (if applicable)
Not Available in Source Documents (mock mode reuses the same Gateway endpoints as production; no separate documented mock endpoint).

### UI Elements
Not Available in Source Documents.

### Validation Rules
| Aspect | Rule |
|---|---|
| Mock mode toggle | Must not affect normal gateway operation when disabled |

### Error Messages
Not Available in Source Documents. Documented capability: mock mode supports "configurable error responses" for negative testing, but specific error codes/messages are not documented.

---

## Feature: End-to-End Integration Testing (US-INTEGRATION-E2E-001)

### Overview
Validates all ALAMOS Release 26.3 integration capabilities across the Adapter, FacadeService, IPL, ALAMOS Gateway, and ALAMOS FE2. Jira: IPL-26915 (Open).
Source: `US-INTEGRATION-E2E-001.md`

### User Stories
- As an Adapter Integration team, I want to execute end-to-end testing of all ALAMOS Release 26.3 integration flows, so that I can verify that Alerting, Continuous Mission Updates, and Situation Report processing behave correctly across all integrated components under both success and failure scenarios.

### Acceptance Criteria
- [ ] End-to-end testing validates the complete Alerting with Squad Information (referred to as "US-ALAMOS-100") flow, including squad transmission and acknowledgement propagation.
- [ ] End-to-end testing validates the complete Continuous Mission Update ("US-ALAMOS-200") flow through the ALAMOS Gateway.
- [ ] End-to-end testing validates the complete Situation Report ("US-ALAMOS-300") flow from ALAMOS FE2 through the Adapter, Domain Event creation, FacadeService, and IPL.
- [ ] Domain Event generation, request mapping, IPL processing, and acknowledgement propagation are verified for successful scenarios.
- [ ] Business validation failures, technical faults, and communication failures propagate correctly to the originating system.
- [ ] Existing retry and DLQ mechanisms are validated using representative failure scenarios; no unexpected message loss occurs.
- [ ] Logging, monitoring, and traceability information are available across all tested integration flows.
- [ ] All ALAMOS Release 26.3 capabilities demonstrate expected behavior under positive and negative test conditions.

### API Endpoints (if applicable)
Covers the same endpoints referenced in the individual features above (SOAP `AlarmRequest`, REST ALARM API, Situation Report REST endpoint, `POST /einsatztransfer/erzeugeEinsatzmeldung`).

### UI Elements
Not Available in Source Documents.

### Validation Rules
Not Available in Source Documents beyond the acceptance criteria above (no field-level validation rules are specific to this feature; it validates the rules defined by the other features).

### Error Messages
Not Available in Source Documents (specific codes/messages not documented for this feature).

---

## Feature: CI/CD Build Pipeline (US-PLATFORM-CICD-001)

### Overview
Configures build, automated testing, and packaging pipelines for the Adapter and ALAMOS Gateway. Jira: IPL-26916 (Open).
Source: `US-PLATFORM-CICD-001.md`

### User Stories
- As an Adapter Integration Team, I want build jobs and pipeline templates to be configured for the ALAMOS Adapter and ALAMOS Gateway components, so that project artifacts can be built, validated, and packaged consistently for Release 26.3.

### Acceptance Criteria
- [ ] Build jobs are configured for the ALAMOS Adapter and ALAMOS Gateway components.
- [ ] Automated unit and integration tests execute as part of the build process where applicable.
- [ ] Failed builds or test executions prevent artifact generation.
- [ ] Build artifacts are generated in the required packaging format.
- [ ] Required pipeline template changes for Release 26.3 are implemented and validated.
- [ ] Build execution provides visibility into build, test, and packaging results.
- [ ] Build failures are logged with sufficient information for troubleshooting.
- [ ] Build and packaging procedures are repeatable and executable without manual build steps.

### API Endpoints (if applicable)
Not Available in Source Documents (not applicable — this is a build/CI feature).

### UI Elements
Not Available in Source Documents.

### Validation Rules
Not Available in Source Documents (no field-level validation rules; this feature concerns build/test/packaging automation).

### Error Messages
Not Available in Source Documents. Documented behavior: failed builds/tests prevent artifact generation and are logged for troubleshooting; no specific error code/message text documented.

---

## Cross-Feature Workflows (from Sequence Diagrams)

### Alerting (LEGACY) Flow
IPL Server → FacadeService (Adapter, LEGACY capability routing: "Route capability", "Forward request", "Preserve compatibility") → ALAMOS Gateway (SOAP `AlarmRequest`) → ALAMOS Gateway processes Alerting + Squad Information + ALAMOS mapping + legacy integration → ALAMOS FE2 (REST ALARM API) → Acknowledgement/Response returned back through the chain (Response → SOAP Response to IPL).
Source: `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`

### Situation Reports (EVENT) Flow
ALAMOS FE2 → ALAMOS Adapter: "Situation Report (REST)" → Adapter: "Validate Payload" → "Correlate Incident (external_id / incident_number)" → "Create Domain Event: incident.situation_report_received" (Internal Domain Event) → FacadeService (Adapter): "Map Domain Event to IPL Request" → IPL Server: `erzeugeEinsatzmeldung` (SOAP Request) → IPL: "Success / Fault Response" → back through FacadeService/Adapter → ALAMOS FE2: "Success / Error Acknowledgement".
Source: `Situation Reports (EVENT).svg`

## Dependencies (Cross-Feature)
- Situation Report features (US-ADAPTER-ALAMOS-001 → 004) depend on each other sequentially: receive/validate → generate Domain Event → route via FacadeService → invoke IPL.
- US-ADAPTER-RELIABILITY-001 depends on all Alerting, Continuous Mission Update, and Situation Report flows being implemented, to validate retry/DLQ behavior across them.
- US-INTEGRATION-E2E-001 depends on all other features (Adapter, FacadeService, Gateway, Mock Service) being available for end-to-end validation.
- US-ALAMOSGW-MOCK-001 is a testing dependency/enabler for US-ALAMOS-GW-001, US-ALAMOS-GW-002, US-ALAMOS-GW-003, and US-INTEGRATION-E2E-001.
- US-PLATFORM-CICD-001 is a build/delivery dependency for all Adapter and Gateway components.

## Traceability
| Feature | Source File(s) |
|---|---|
| Situation Reports – Receive & Validate | `US-ADAPTER-ALAMOS-001.md`, `Situation Reports (EVENT).svg` |
| Situation Reports – Domain Event Generation | `US-ADAPTER-ALAMOS-002.md`, `ALAMOS Integration – Phase 1.md` |
| FacadeService – Routing | `US-ADAPTER-ALAMOS-003.md`, `ALAMOS Integration – Phase 1.md` |
| FacadeService – IPL Processing | `US-ADAPTER-ALAMOS-004.md`, `Situation Reports (EVENT).svg` |
| Reliability – Retry & DLQ | `US-ADAPTER-RELIABILITY-001.md` |
| Gateway – Legacy Alerting | `US-ALAMOS-GW-001.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg` |
| Gateway – Continuous Mission Updates | `US-ALAMOS-GW-002.md` |
| Gateway – Squad Information | `US-ALAMOS-GW-003.md` |
| Gateway – Mock Service | `US-ALAMOSGW-MOCK-001.md` |
| End-to-End Integration Testing | `US-INTEGRATION-E2E-001.md` |
| CI/CD Build Pipeline | `US-PLATFORM-CICD-001.md` |
