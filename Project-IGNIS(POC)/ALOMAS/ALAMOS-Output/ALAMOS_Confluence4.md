# ALAMOS Integration – Release 26.3 Test Documentation

| **Document Information** | |
|--------------------------|--------------------------|
| **Project** | ALAMOS Integration (IGNIS Platform) |
| **Release** | 26.3 |
| **Document Type** | Functional Integration Test Specification |
| **Created Date** | 2026-07-28 |
| **Last Updated** | 2026-07-28 |
| **Status** | Under Review |
| **Author** | QA Team |
| **Reviewer** | QA Lead / Dev Lead |

---

## Executive Summary

This document contains **19 optimized functional integration test cases** for the ALAMOS Integration Release 26.3. These test cases have been consolidated from an original set of 50+ test cases, achieving a **62% reduction** while maintaining **100% requirement coverage**.

### Test Case Distribution

| Category | Count |
|----------|-------|
| Functional (Happy Path) | 9 |
| Negative Scenario | 7 |
| Edge Case / Negative | 1 |
| Integration (E2E) | 3 |
| **Total** | **19** |

### User Stories Covered

| User Story | Description | Test Count |
|------------|-------------|------------|
| US-ADAPTER-ALAMOS-001 | Situation Report Receive & Validate | 3 |
| US-ADAPTER-ALAMOS-002 | Domain Event Generation | 2 |
| US-ADAPTER-ALAMOS-003 | FacadeService Routing Layer | 2 |
| US-ADAPTER-ALAMOS-004 | FacadeService IPL Processing | 2 |
| US-ADAPTER-RELIABILITY-001 | Retry & DLQ Validation | 1 |
| US-ALAMOS-GW-001 | Legacy Alerting | 2 |
| US-ALAMOS-GW-002 | Continuous Mission Updates | 2 |
| US-ALAMOS-GW-003 | Squad Information Extension | 1 |
| US-ALAMOSGW-MOCK-001 | Mock Gateway Service | 1 |
| US-INTEGRATION-E2E-001 | End-to-End Integration Testing | 3 |

---

## Test Coverage Matrix

| User Story ID | User Story Description | Test Case IDs | Coverage Status |
|---------------|------------------------|---------------|-----------------|
| US-ADAPTER-ALAMOS-001 | Adapter receives and validates Situation Reports from ALAMOS FE2 | TC-001, TC-002, TC-003 | ✅ Covered |
| US-ADAPTER-ALAMOS-002 | Domain Event generation with incident correlation | TC-004, TC-005 | ✅ Covered |
| US-ADAPTER-ALAMOS-003 | FacadeService routing and response propagation | TC-006, TC-007 | ✅ Covered |
| US-ADAPTER-ALAMOS-004 | FacadeService IPL processing and error handling | TC-008, TC-009 | ✅ Covered |
| US-ADAPTER-RELIABILITY-001 | Retry, DLQ, and logging validation | TC-015 | ✅ Covered |
| US-ALAMOS-GW-001 | Legacy Alerting via ALAMOS Gateway | TC-010, TC-011 | ✅ Covered |
| US-ALAMOS-GW-002 | Continuous Mission Updates processing | TC-012, TC-013 | ✅ Covered |
| US-ALAMOS-GW-003 | Squad Information in Alerting requests | TC-014 | ✅ Covered |
| US-ALAMOSGW-MOCK-001 | ALAMOS Gateway Mock Service | TC-016 | ✅ Covered |
| US-INTEGRATION-E2E-001 | End-to-End Integration flows | TC-017, TC-018, TC-019 | ✅ Covered |

---

## Feature: Situation Reports – Adapter (US-ADAPTER-ALAMOS-001)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-001:** Verify complete Situation Report receive, validate, and acknowledge flow | • Adapter REST endpoint is available<br>• ALAMOS FE2 is configured and connected<br>• Valid authentication credentials are available<br>• IPL endpoint is available | • Prepare a valid Situation Report payload with all mandatory fields (external_id, incident_number, call_sign, situation_report.text, reported_at)<br>• Send the Situation Report to the Adapter REST endpoint with valid headers (Content-Type: application/json) and authentication<br>• Verify the Adapter validates request headers, authentication, and content-type before payload processing<br>• Verify the Adapter validates the payload against the ALAMOS contract including all mandatory fields<br>• Verify the Adapter accepts the request and forwards to FacadeService for IPL processing<br>• Verify IPL processes the request successfully<br>• Verify the Adapter returns a synchronous success acknowledgment to ALAMOS FE2 | • Valid payload is prepared with all required fields<br>• Request is transmitted successfully<br>• Technical prerequisites validation passes<br>• Payload validation passes without errors<br>• Situation Report is accepted and forwarded for processing<br>• IPL returns success response<br>• HTTP 200 response with success acknowledgment is returned | US-ADAPTER-ALAMOS-001 | Pending |
| **TC-002:** Verify Adapter rejects invalid requests (missing fields, invalid headers/auth/content-type, unsupported methods) | • Adapter REST endpoint is available<br>• Authentication mechanism is enabled | • Send a Situation Report with missing mandatory field (external_id empty)<br>• Send a request without authentication headers<br>• Send a request with invalid Content-Type (text/plain instead of application/json)<br>• Send a request using GET method instead of POST<br>• Verify all rejected requests do not proceed to downstream processing | • HTTP 400 with validation error indicating missing field<br>• HTTP 401 Unauthorized response<br>• HTTP 415 Unsupported Media Type response<br>• HTTP 405 Method Not Allowed response<br>• No Domain Event created for invalid requests | US-ADAPTER-ALAMOS-001 | Pending |
| **TC-003:** Verify Adapter returns failure acknowledgment when IPL processing fails | • Adapter REST endpoint is available<br>• IPL endpoint is configured to return a fault response | • Configure IPL endpoint to return a business fault for the test scenario<br>• Send a valid Situation Report to the Adapter<br>• Verify the Adapter forwards the request and waits for IPL response<br>• Verify the Adapter returns synchronous failure acknowledgment to ALAMOS FE2 | • IPL mock/stub is configured to return fault<br>• Request is received and validated by Adapter<br>• Adapter processes the request synchronously<br>• HTTP response with failure acknowledgment accurately reflecting IPL fault is returned | US-ADAPTER-ALAMOS-001 | Pending |

---

## Feature: Domain Event Generation (US-ADAPTER-ALAMOS-002)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-004:** Verify Domain Event generation with incident correlation (external_id primary, incident_number fallback) | • Adapter is running<br>• Valid Situation Report payloads are available | • Submit a valid Situation Report with external_id populated<br>• Verify the Adapter creates incident.situation_report_received/v1 Domain Event with correct event_type<br>• Verify incident correlation uses external_id from the payload (primary key)<br>• Verify all required Domain Event attributes are populated: event_id (UUID), event_type, occurred_at (ISO 8601), source_system (ALAMOS), tenant_id, authoring_resource, situation_report<br>• Submit a Situation Report with external_id empty/null and incident_number populated<br>• Verify incident correlation falls back to incident_number when external_id unavailable<br>• Verify the Domain Event is validated prior to downstream processing | • Situation Report is received and validated<br>• Domain Event is created with correct type<br>• incident.external_id in Domain Event matches submitted external_id<br>• All mandatory attributes present and correctly formatted<br>• Request is received by Adapter<br>• incident.incident_number is used for correlation<br>• Domain Event passes contract validation | US-ADAPTER-ALAMOS-002 | Pending |
| **TC-005:** Verify call_sign fallback and error handling for incomplete correlation data | • Adapter is running | • Submit a valid Situation Report with call_sign field empty or missing<br>• Verify the Adapter applies fallback handling for call_sign<br>• Verify Domain Event is created successfully with fallback call_sign<br>• Submit a Situation Report with both external_id and incident_number missing/empty<br>• Verify the Adapter cannot complete incident correlation<br>• Verify an appropriate error is returned to ALAMOS FE2 | • Situation Report is received by Adapter<br>• authoring_resource.call_sign uses fallback value<br>• Domain Event is generated without error<br>• Both correlation keys are unavailable<br>• Correlation failure is detected<br>• Error response indicating incident correlation failure is returned | US-ADAPTER-ALAMOS-002 | Pending |

---

## Feature: FacadeService – Routing Layer (US-ADAPTER-ALAMOS-003)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-006:** Verify FacadeService routing, synchronous processing, and response propagation | • Adapter and FacadeService are running<br>• Routing configuration for EVENT path is enabled<br>• IPL endpoint is available | • Generate a valid incident.situation_report_received Domain Event<br>• Verify FacadeService receives the Domain Event<br>• Verify FacadeService determines EVENT processing path based on capability-specific routing configuration<br>• Verify FacadeService coordinates synchronous processing via IPL<br>• Verify IPL returns success response<br>• Verify FacadeService propagates success response back to Adapter<br>• Configure IPL to return business fault, repeat steps 1-4<br>• Verify FacadeService propagates failure response back to Adapter<br>• Verify FacadeService operates without Inbox, Outbox, Event Bus, or Process Tracker | • Domain Event is created by Adapter<br>• FacadeService receives the event<br>• Routing configuration resolves to EVENT path<br>• Processing is coordinated synchronously<br>• IPL processing completes successfully<br>• Adapter receives success indication<br>• Business fault is configured<br>• Adapter receives failure indication with fault details<br>• No persistence mechanisms are invoked | US-ADAPTER-ALAMOS-003 | Pending |
| **TC-007:** Verify FacadeService handles invalid routing configuration | • Adapter and FacadeService are running<br>• Invalid routing configuration is set | • Configure FacadeService with invalid routing for Situation Report capability<br>• Submit a valid Situation Report<br>• Verify FacadeService cannot resolve to valid processing path<br>• Verify error response is returned to ALAMOS FE2 | • Invalid configuration is applied<br>• Request is received by Adapter<br>• Invalid configuration is detected<br>• Error indicating routing failure is propagated | US-ADAPTER-ALAMOS-003 | Pending |

---

## Feature: FacadeService – IPL Processing (US-ADAPTER-ALAMOS-004)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-008:** Verify FacadeService IPL invocation with request mapping and response handling | • FacadeService is running<br>• IPL endpoint POST /einsatztransfer/erzeugeEinsatzmeldung is available | • Generate incident.situation_report_received Domain Event with all required data<br>• Verify FacadeService validates all required data for IPL request generation<br>• Verify FacadeService maps Domain Event data to IPL request structure<br>• Verify FacadeService invokes POST /einsatztransfer/erzeugeEinsatzmeldung synchronously<br>• Verify IPL returns success response<br>• Verify success result is propagated back to ALAMOS FE2 | • Valid Domain Event is created<br>• Validation passes<br>• Request mapping is performed correctly<br>• SOAP request is sent to IPL<br>• IPL processing completes successfully<br>• Success acknowledgment is returned | US-ADAPTER-ALAMOS-004 | Pending |
| **TC-009:** Verify FacadeService handles IPL errors (business fault, technical fault, unavailable, timeout) | • FacadeService is running<br>• IPL endpoint can be configured for various error scenarios | • Configure IPL to return a business fault, submit valid Situation Report<br>• Verify business fault is propagated to ALAMOS FE2 with appropriate error details<br>• Configure IPL to return a technical fault (e.g., internal server error)<br>• Verify technical fault is propagated to ALAMOS FE2<br>• Stop IPL endpoint, submit valid Situation Report<br>• Verify communication failure is handled and propagated to ALAMOS FE2<br>• Configure IPL to delay response beyond timeout threshold<br>• Verify timeout failure is propagated to ALAMOS FE2 | • Business fault is received<br>• Failure acknowledgment with business fault details is returned<br>• Technical fault is received<br>• Failure acknowledgment with technical error is returned<br>• Connection failure occurs<br>• Failure acknowledgment indicating IPL unavailable is returned<br>• Timeout occurs<br>• Failure acknowledgment indicating timeout is returned | US-ADAPTER-ALAMOS-004 | Pending |

---

## Feature: ALAMOS Gateway – Legacy Alerting (US-ALAMOS-GW-001)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-010:** Verify Gateway processes valid Alerting request and handles ALAMOS FE2 responses | • ALAMOS Gateway is running<br>• IPL is configured<br>• ALAMOS FE2 is available | • IPL sends a valid SOAP AlarmRequest to the ALAMOS Gateway<br>• Verify ALAMOS Gateway receives and parses the request<br>• Verify Gateway transforms request to REST Alarm API format<br>• Verify Gateway forwards request to ALAMOS FE2<br>• Verify ALAMOS FE2 returns success acknowledgment<br>• Verify Gateway propagates success back to IPL | • AlarmRequest is transmitted<br>• Gateway receives AlarmRequest<br>• Request is mapped correctly<br>• REST Alarm API call is made<br>• Success response is received<br>• SOAP response indicating success is returned to IPL | US-ALAMOS-GW-001 | Pending |
| **TC-011:** Verify Gateway handles Alerting errors (business error, communication failure, malformed request) | • ALAMOS Gateway is running<br>• ALAMOS FE2 can be configured for error scenarios | • Configure ALAMOS FE2 to return a business error, send valid AlarmRequest from IPL<br>• Verify business error is propagated back to IPL<br>• Simulate communication failure with ALAMOS FE2 (timeout/connectivity)<br>• Verify communication failure is handled and propagated to IPL<br>• Send an invalid/malformed SOAP AlarmRequest from IPL<br>• Verify malformed request is rejected | • Business error is received<br>• IPL receives business error response<br>• Communication failure occurs<br>• IPL receives appropriate error response<br>• Gateway validates the request<br>• Error response returned to IPL | US-ALAMOS-GW-001 | Pending |

---

## Feature: Continuous Mission Updates (US-ALAMOS-GW-002)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-012:** Verify Gateway processes Continuous Mission Updates for all triggers (incident/resource/keyword/location) | • ALAMOS Gateway is running<br>• ALAMOS is available<br>• IPL can trigger all update types | • Trigger an incident status change in IPL<br>• Verify Gateway processes and forwards the update to ALAMOS<br>• Verify ALAMOS response is propagated back to IPL<br>• Trigger a resource status change in IPL<br>• Verify update is processed and forwarded, response propagated to IPL<br>• Trigger a keyword change in IPL<br>• Verify update is processed and forwarded, response propagated to IPL<br>• Trigger a location change in IPL<br>• Verify update is processed and forwarded, response propagated to IPL<br>• Verify all updates maintain backward compatibility with existing gateway implementation | • Mission Update for incident status is generated<br>• Update is forwarded successfully<br>• IPL receives acknowledgment<br>• Mission Update for resource status is generated<br>• Complete flow successful<br>• Mission Update for keyword change is generated<br>• Complete flow successful<br>• Mission Update for location change is generated<br>• Complete flow successful<br>• Existing functionality remains unaffected | US-ALAMOS-GW-002 | Pending |
| **TC-013:** Verify Gateway handles Mission Update errors from ALAMOS | • ALAMOS Gateway is running<br>• ALAMOS can return error responses | • Configure ALAMOS to return business error, trigger Mission Update from IPL<br>• Verify business error is propagated back to IPL<br>• Configure ALAMOS to return technical error, trigger Mission Update from IPL<br>• Verify technical error is propagated back to IPL | • Update is sent to ALAMOS<br>• IPL receives business error<br>• Update is sent to ALAMOS<br>• IPL receives technical error | US-ALAMOS-GW-002 | Pending |

---

## Feature: Squad Information Extension (US-ALAMOS-GW-003)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-014:** Verify Gateway processes squad information (single/multiple squads) with backward compatibility | • ALAMOS Gateway is running<br>• ALAMOS FE2 is available | • Send Alerting request with single squad in `<squads>` element<br>• Verify squad information is extracted and mapped to ALAMOS message structure<br>• Verify request is forwarded to ALAMOS FE2 with squad data<br>• Send Alerting request with multiple squads in `<squads>` element<br>• Verify all squad entries are correctly mapped to ALAMOS message structure<br>• Verify all squads are transmitted to ALAMOS FE2<br>• Send Alerting request without `<squads>` element<br>• Verify request is processed successfully without errors (backward compatibility)<br>• Verify acknowledgments are propagated back to IPL without loss of information | • Gateway receives the request<br>• Single squad is correctly mapped<br>• Squad information is transmitted correctly<br>• Gateway receives the request<br>• Multiple squads are correctly mapped<br>• All squad data received by ALAMOS FE2<br>• Gateway receives the request<br>• Request processed, response propagated to IPL<br>• IPL receives complete acknowledgment | US-ALAMOS-GW-003 | Pending |

---

## Feature: Reliability – Retry & DLQ (US-ADAPTER-RELIABILITY-001)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-015:** Verify retry, DLQ, and logging behavior across all ALAMOS flows | • Adapter/Gateway running<br>• Retry policies and DLQ configured<br>• Logging enabled | • Simulate a temporary communication failure during Situation Report processing<br>• Verify message is retried according to existing retry policy<br>• Resolve the transient failure before retry limit<br>• Verify message is processed successfully after retry<br>• Simulate persistent failure for Alerting flow exceeding retry limit<br>• Verify message is routed to existing DLQ<br>• Simulate a business validation error from IPL<br>• Verify business validation error does NOT trigger unnecessary retries<br>• Verify retry attempts, DLQ events, and failures are logged with sufficient diagnostic information<br>• Verify success and fault responses are propagated correctly to originating caller | • Initial attempt fails<br>• Retry is triggered<br>• Next retry succeeds<br>• Success response propagated<br>• All retry attempts fail<br>• Message is in DLQ<br>• Business error is returned<br>• No retries triggered for business error<br>• Logs contain correlation IDs, timestamps, error details<br>• Responses accurately reflect processing result | US-ADAPTER-RELIABILITY-001 | Pending |

---

## Feature: Mock Gateway Service (US-ALAMOSGW-MOCK-001)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-016:** Verify Gateway mock mode functionality for development/testing | • Gateway mock mode configuration available | • Enable mock mode configuration and start ALAMOS Gateway<br>• Send a valid Alerting request with squad information<br>• Verify predefined success response is returned without connecting to ALAMOS FE2<br>• Configure mock mode to return an error response<br>• Send another Alerting request<br>• Send Mission Update request in mock mode<br>• Verify mock response is returned for Mission Update<br>• Disable mock mode and restart Gateway in normal mode<br>• Verify mock mode configuration has no impact on normal gateway operation | • Gateway starts successfully in mock mode<br>• Gateway processes in mock mode<br>• Mock success response returned<br>• Error configuration applied<br>• Gateway returns configured error response<br>• Gateway processes in mock mode<br>• Mock response returned<br>• Gateway starts normally<br>• Gateway operates with real ALAMOS FE2 connectivity | US-ALAMOSGW-MOCK-001 | Pending |

---

## Feature: End-to-End Integration (US-INTEGRATION-E2E-001)

| Test | Pre-Requisite | Test Detail | Expected Outcome | Reference & Status | Status |
|------|---------------|-------------|------------------|-------------------|--------|
| **TC-017:** Verify complete Alerting with Squad Information flow (E2E) | • All components running (IPL, Facade Service, ALAMOS Gateway, ALAMOS FE2)<br>• Network connectivity established | • Send SOAP AlarmRequest with squads from IPL<br>• Verify request flows through: IPL → Facade Service → ALAMOS Gateway → ALAMOS FE2<br>• Verify squad information is correctly transmitted to ALAMOS FE2<br>• Verify acknowledgment flows back: ALAMOS FE2 → ALAMOS Gateway → Facade Service → IPL<br>• Verify no data loss or transformation errors across component boundaries | • Request enters the system<br>• Request traverses all components<br>• Squad data intact at destination<br>• Acknowledgment propagated correctly<br>• Data integrity maintained | US-INTEGRATION-E2E-001 | Pending |
| **TC-018:** Verify complete Situation Report flow (E2E) | • All components running (ALAMOS FE2, Adapter, FacadeService, IPL)<br>• Network connectivity established | • Send Situation Report from ALAMOS FE2 to Adapter<br>• Verify incident.situation_report_received Domain Event is created with all required attributes<br>• Verify FacadeService routes and maps event to IPL request<br>• Verify IPL erzeugeEinsatzmeldung is invoked and returns success<br>• Verify acknowledgment is propagated back to ALAMOS FE2<br>• Verify logging and traceability across all components | • Report enters the Adapter<br>• Domain Event created correctly<br>• Request transformation successful<br>• IPL processes successfully<br>• ALAMOS FE2 receives success acknowledgment<br>• Correlation IDs and logs available | US-INTEGRATION-E2E-001 | Pending |
| **TC-019:** Verify E2E failure propagation and retry/DLQ behavior | • All components running<br>• Retry and DLQ mechanisms configured | • Trigger IPL business validation failure during Situation Report processing<br>• Verify failure is propagated correctly back to ALAMOS FE2<br>• Simulate temporary ALAMOS FE2 unavailability during Alerting flow<br>• Verify retry mechanism works end-to-end and succeeds when FE2 recovers<br>• Simulate persistent failure exceeding retry limits<br>• Verify message is routed to DLQ with no unexpected message loss<br>• Verify logging and monitoring data is available across all E2E flows | • Business failure occurs<br>• ALAMOS FE2 receives accurate failure response<br>• Communication failure triggers retry<br>• Alerting completes after retry<br>• All retries fail<br>• DLQ contains failed message<br>• Complete diagnostic trail available | US-INTEGRATION-E2E-001 | Pending |

---

## Test Execution Summary

| Category | Total | Passed | Failed | Blocked | Pending |
|----------|-------|--------|--------|---------|---------|
| Functional (Happy Path) | 9 | - | - | - | 9 |
| Negative Scenario | 7 | - | - | - | 7 |
| Edge Case / Negative | 1 | - | - | - | 1 |
| Integration (E2E) | 3 | - | - | - | 3 |
| **Total** | **19** | **-** | **-** | **-** | **19** |

---

## Risks & Dependencies

### Dependencies
- IPL SOAP endpoints must be available and unchanged
- ALAMOS FE2 connectivity required for E2E tests (or mock mode for isolated testing)
- Retry and DLQ mechanisms must be pre-configured
- Valid test data and authentication credentials required

### Risks
- Synchronous coupling means real-time IPL availability is required
- No Domain Event persistence in Release 26.3 limits replay/investigation capability
- Mock mode testing may not catch production-specific issues

---

## Approval Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| QA Lead | | | |
| Dev Lead | | | |
| Product Owner | | | |
| Release Manager | | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-28 | QA Team | Initial version - 19 optimized test cases with bullet point format |

---

*Document End*
