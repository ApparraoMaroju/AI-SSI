# ALAMOS Integration – Release 26.3 Functional Test Cases

**Generated:** 2026-07-23 14:30:00  
**Source:** ALAMOS_Feature_Context.md, ALAMOS_Project_Context.md, ALAMOS_Testing_Context.md  
**Template:** FTC02-ComprehensiveTestCase.md

---

## Notes

- This document follows the FTC02 template structure but is provided in Markdown format (convertible to Excel).
- All test cases are derived exclusively from the documented acceptance criteria and validation rules.
- Items marked **[Needs clarification]** indicate missing or ambiguous requirements.
- Specific error codes/messages are NOT documented in source files and are marked accordingly.

---

## Test Case Summary

| Category | Count |
|----------|-------|
| Functional (Happy Path) | 28 |
| Negative Scenarios | 24 |
| Boundary Value Analysis | 6 |
| Edge Cases | 10 |
| **Total** | **68** |

---

## Test Cases

### Feature: Situation Reports – Adapter Receive & Validate (US-ADAPTER-ALAMOS-001)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-001 | Valid Situation Report - Successful Processing | Functional | Verify that a valid Situation Report from ALAMOS FE2 is received, validated, and acknowledged successfully | Adapter is running; IPL endpoint is available; ALAMOS FE2 connectivity is established | 1 | Send a valid Situation Report payload compliant with the ALAMOS contract to the Adapter REST endpoint | Adapter accepts the request and begins processing |  High |
| | | | | | 2 | Adapter validates the payload against the ALAMOS contract | Validation passes without errors | |
| | | | | | 3 | Adapter forwards the request to IPL via FacadeService | Request is forwarded successfully | |
| | | | | | 4 | IPL processes the request and returns a successful response | IPL returns a success response | |
| | | | | | 5 | Verify the synchronous acknowledgment returned to ALAMOS FE2 | Success acknowledgment is returned to ALAMOS FE2 reflecting successful IPL processing | |
| | | | | | | | | |
| TC-002 | Situation Report - ALAMOS Contract Validation | Functional | Verify that incoming requests are validated against the ALAMOS contract | Adapter is running | 1 | Send a Situation Report payload that complies with the ALAMOS contract | Adapter accepts the payload for further processing | High |
| | | | | | 2 | Verify validation logs/traces | Validation step is logged as successful | |
| | | | | | | | | |
| TC-003 | Situation Report - Mandatory Fields Present | Functional | Verify that Situation Reports with all mandatory fields are accepted | Adapter is running | 1 | Send a Situation Report with all mandatory fields populated | Adapter accepts the request | High |
| | | | | | 2 | Verify the request proceeds to downstream processing | Request is forwarded to FacadeService | |
| | | | | | | | | |
| TC-004 | Situation Report - Valid Request Headers | Functional | Verify that valid request headers and authentication are accepted | Adapter is running | 1 | Send a Situation Report with valid request headers and authentication | Adapter accepts the request | High |
| | | | | | 2 | Verify technical prerequisites are satisfied | Request proceeds to payload validation | |
| | | | | | | | | |
| TC-005 | Situation Report - Valid Content Type | Functional | Verify that requests with valid content type are accepted | Adapter is running | 1 | Send a Situation Report with valid content type | Adapter accepts the request | Medium |
| | | | | | 2 | Verify content type validation passes | Request proceeds to payload validation | |
| | | | | | | | | |
| TC-006 | Situation Report - IPL Failure Acknowledgment | Functional | Verify that IPL processing failure results in a failure acknowledgment to ALAMOS FE2 | Adapter is running; IPL returns an error | 1 | Send a valid Situation Report to the Adapter | Adapter accepts and processes the request | High |
| | | | | | 2 | IPL returns a failure/error response | Adapter receives the IPL error | |
| | | | | | 3 | Verify the synchronous acknowledgment to ALAMOS FE2 | Failure acknowledgment is returned to ALAMOS FE2 accurately reflecting the IPL processing result | |
| | | | | | | | | |
| TC-007 | Situation Report - Contract Violation Rejection | Negative | Verify that Situation Reports violating the ALAMOS contract are rejected | Adapter is running | 1 | Send a Situation Report payload that violates the ALAMOS contract | Adapter rejects the request | High |
| | | | | | 2 | Verify the error response | A clear validation error is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-008 | Situation Report - Missing Mandatory Fields | Negative | Verify that Situation Reports with missing mandatory fields are rejected | Adapter is running | 1 | Send a Situation Report with one or more mandatory fields missing | Adapter rejects the request | High |
| | | | | | 2 | Verify the error response | Request is rejected with validation error **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-009 | Situation Report - Invalid Request Headers | Negative | Verify that requests with invalid headers are rejected | Adapter is running | 1 | Send a Situation Report with invalid or missing request headers | Adapter rejects the request | High |
| | | | | | 2 | Verify the error response | Appropriate technical error response is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-010 | Situation Report - Invalid Authentication | Negative | Verify that requests with invalid authentication are rejected | Adapter is running | 1 | Send a Situation Report with invalid authentication information | Adapter rejects the request | High |
| | | | | | 2 | Verify the error response | Appropriate technical error response is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-011 | Situation Report - Unsupported HTTP Method | Negative | Verify that unsupported HTTP methods are rejected | Adapter is running | 1 | Send a request using an unsupported HTTP method (e.g., GET, DELETE, PUT) | Adapter rejects the request | Medium |
| | | | | | 2 | Verify the error response | Appropriate technical error response is returned **[Needs clarification: specific error code/message and supported methods not documented]** | |
| | | | | | | | | |
| TC-012 | Situation Report - Invalid Content Type | Negative | Verify that requests with invalid content type are rejected | Adapter is running | 1 | Send a Situation Report with an invalid content type | Adapter rejects the request | Medium |
| | | | | | 2 | Verify the error response | Appropriate technical error response is returned **[Needs clarification: specific error code/message and valid content types not documented]** | |

---

### Feature: Situation Reports – Domain Event Generation (US-ADAPTER-ALAMOS-002)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-013 | Domain Event - Successful Transformation | Functional | Verify that validated Situation Reports are transformed into the canonical Domain Event | Adapter is running; valid Situation Report received | 1 | Submit a valid Situation Report that passes initial validation | Situation Report is accepted | High |
| | | | | | 2 | Verify Domain Event generation | `incident.situation_report_received/v1` Domain Event is created | |
| | | | | | 3 | Verify all required attributes/metadata are present | Event contains: event_id, event_type, occurred_at, source_system, tenant_id, incident (external_id, incident_number), authoring_resource (external_resource_id, call_sign), situation_report (text, reported_at) | |
| | | | | | | | | |
| TC-014 | Domain Event - Incident Correlation via external_id | Functional | Verify incident correlation uses external_id when available | Adapter is running; Situation Report with external_id received | 1 | Submit a Situation Report with a valid external_id | Situation Report is accepted | High |
| | | | | | 2 | Verify incident correlation | Incident is correlated using external_id as the primary key | |
| | | | | | | | | |
| TC-015 | Domain Event - Incident Correlation Fallback to incident_number | Functional | Verify incident correlation falls back to incident_number when external_id is unavailable | Adapter is running; Situation Report without external_id received | 1 | Submit a Situation Report without external_id but with valid incident_number | Situation Report is accepted | High |
| | | | | | 2 | Verify incident correlation | Incident is correlated using incident_number as fallback | |
| | | | | | | | | |
| TC-016 | Domain Event - Resource Mapping | Functional | Verify reporting resources are mapped to the canonical event structure | Adapter is running | 1 | Submit a Situation Report with authoring resource information | Situation Report is accepted | High |
| | | | | | 2 | Verify resource mapping in the Domain Event | Reporting resources are correctly mapped to authoring_resource structure (external_resource_id, call_sign) | |
| | | | | | | | | |
| TC-017 | Domain Event - call_sign Available | Functional | Verify call_sign is mapped directly when available | Adapter is running | 1 | Submit a Situation Report with a valid call_sign | Situation Report is accepted | Medium |
| | | | | | 2 | Verify call_sign in Domain Event | call_sign is mapped directly without fallback | |
| | | | | | | | | |
| TC-018 | Domain Event - Event Validation Before Downstream | Functional | Verify the generated event is validated prior to downstream processing | Adapter is running | 1 | Submit a valid Situation Report | Domain Event is generated | High |
| | | | | | 2 | Verify event validation | Event is validated to conform to `incident.situation_report_received/v1` contract before downstream consumption | |
| | | | | | | | | |
| TC-019 | Domain Event - call_sign Fallback Handling | Edge Case | Verify call_sign fallback logic when call_sign is missing/invalid | Adapter is running | 1 | Submit a Situation Report with missing or invalid call_sign | Situation Report is accepted | Medium |
| | | | | | 2 | Verify fallback handling | call_sign fallback handling is applied **[Needs clarification: specific fallback logic not documented]** | |
| | | | | | | | | |
| TC-020 | Domain Event - external_id Unavailable, incident_number Fallback | Edge Case | Verify fallback to incident_number when external_id is not available | Adapter is running | 1 | Submit a Situation Report with external_id empty/null/missing | Situation Report is accepted | High |
| | | | | | 2 | Verify correlation uses incident_number | Incident is correlated using incident_number | |
| | | | | | | | | |
| TC-021 | Domain Event - Missing Required Attributes | Negative | Verify error when required event attributes are missing | Adapter is running | 1 | Submit a Situation Report that would result in missing required Domain Event attributes | Event generation fails | High |
| | | | | | 2 | Verify error response | Appropriate error is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-022 | Domain Event - Incident Correlation Failure | Negative | Verify error when incident correlation cannot be completed | Adapter is running | 1 | Submit a Situation Report where incident correlation cannot succeed (e.g., no external_id and no incident_number) | Correlation fails | High |
| | | | | | 2 | Verify error response | Appropriate error is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-023 | Domain Event - Resource Mapping Failure | Negative | Verify error when resource mapping cannot be completed | Adapter is running | 1 | Submit a Situation Report where resource mapping fails | Mapping fails | Medium |
| | | | | | 2 | Verify error response | Appropriate error is returned **[Needs clarification: specific error code/message not documented]** | |

---

### Feature: FacadeService – Routing Layer (US-ADAPTER-ALAMOS-003)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-024 | FacadeService - Receive Domain Events | Functional | Verify FacadeService receives Domain Events from the Adapter | FacadeService running inside Adapter | 1 | Generate a valid `incident.situation_report_received` Domain Event in the Adapter | Event is created | High |
| | | | | | 2 | Verify FacadeService receives the event | FacadeService receives the Domain Event for routing | |
| | | | | | | | | |
| TC-025 | FacadeService - Route to EVENT Processing | Functional | Verify routing to EVENT processing path | FacadeService running; EVENT capability configured | 1 | Submit a Situation Report Domain Event | FacadeService receives the event | High |
| | | | | | 2 | Verify routing decision | FacadeService routes to EVENT processing path | |
| | | | | | | | | |
| TC-026 | FacadeService - Route to LEGACY Processing | Functional | Verify routing to LEGACY processing path for applicable capabilities | FacadeService running; LEGACY capability configured | 1 | Submit a request/event for a LEGACY capability | FacadeService receives the request | High |
| | | | | | 2 | Verify routing decision | FacadeService routes to LEGACY processing path | |
| | | | | | | | | |
| TC-027 | FacadeService - Synchronous Processing | Functional | Verify FacadeService coordinates synchronous processing | FacadeService running | 1 | Submit a Domain Event for processing | FacadeService receives and routes the event | High |
| | | | | | 2 | Verify synchronous coordination | Processing is coordinated synchronously; result is returned to the calling component | |
| | | | | | | | | |
| TC-028 | FacadeService - Success Response Propagation | Functional | Verify success responses are propagated back to Adapter | FacadeService running; downstream processing succeeds | 1 | Submit a Domain Event that is processed successfully | Processing completes | High |
| | | | | | 2 | Verify response propagation | Success response is propagated back to the Adapter | |
| | | | | | | | | |
| TC-029 | FacadeService - Failure Response Propagation | Functional | Verify failure responses are propagated back to Adapter | FacadeService running; downstream processing fails | 1 | Submit a Domain Event that results in processing failure | Processing fails | High |
| | | | | | 2 | Verify response propagation | Failure response is propagated back to the Adapter | |
| | | | | | | | | |
| TC-030 | FacadeService - Invalid Routing Configuration | Negative | Verify error when routing configuration is invalid | FacadeService running | 1 | Attempt to process a request with invalid routing configuration | Routing fails | Medium |
| | | | | | 2 | Verify error response | Appropriate error is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-031 | FacadeService - Unsupported Capability | Negative | Verify error when an unsupported capability is requested | FacadeService running | 1 | Submit a request for an unsupported capability | Routing fails | Medium |
| | | | | | 2 | Verify error response | Appropriate error is returned **[Needs clarification: specific error code/message not documented]** | |
| | | | | | | | | |
| TC-032 | FacadeService - No Persistence Mechanisms | Functional | Verify FacadeService operates without Inbox, Outbox, Event Bus, or Process Tracker | FacadeService running | 1 | Process multiple Domain Events | Events are processed | Medium |
| | | | | | 2 | Verify no persistence mechanisms are invoked | No Inbox, Outbox, Event Bus, or Process Tracker is used | |

---

### Feature: FacadeService – IPL Processing (US-ADAPTER-ALAMOS-004)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-033 | IPL Processing - Successful Invocation | Functional | Verify FacadeService successfully invokes IPL for Situation Report processing | FacadeService running; IPL endpoint available | 1 | Submit a valid `incident.situation_report_received` Domain Event | FacadeService receives the event | High |
| | | | | | 2 | Verify event-to-request mapping | Event data is mapped to IPL request structure | |
| | | | | | 3 | Verify IPL invocation | FacadeService invokes IPL `POST /einsatztransfer/erzeugeEinsatzmeldung` synchronously | |
| | | | | | 4 | Verify successful response handling | IPL returns success; result is propagated back to Adapter and ALAMOS FE2 | |
| | | | | | | | | |
| TC-034 | IPL Processing - Required Data Validation | Functional | Verify required data is validated before IPL invocation | FacadeService running | 1 | Submit a Domain Event with all required data for IPL request | Event is received | High |
| | | | | | 2 | Verify data validation | All required data is validated as available before invoking IPL | |
| | | | | | | | | |
| TC-035 | IPL Processing - Event-to-Request Mapping | Functional | Verify Situation Report event data is correctly mapped to IPL request | FacadeService running | 1 | Submit a valid Domain Event | Event is received | High |
| | | | | | 2 | Verify mapping | Event data is correctly mapped to the IPL request structure | |
| | | | | | | | | |
| TC-036 | IPL Processing - Business Fault Response | Negative | Verify FacadeService handles IPL business fault responses | FacadeService running; IPL returns business fault | 1 | Submit a valid Domain Event | FacadeService invokes IPL | High |
| | | | | | 2 | IPL returns a business fault response | FacadeService receives the fault | |
| | | | | | 3 | Verify response propagation | Business fault is propagated back through Adapter to ALAMOS FE2 | |
| | | | | | | | | |
| TC-037 | IPL Processing - Technical Fault Response | Negative | Verify FacadeService handles IPL technical fault responses | FacadeService running; IPL returns technical fault | 1 | Submit a valid Domain Event | FacadeService invokes IPL | High |
| | | | | | 2 | IPL returns a technical fault response | FacadeService receives the fault | |
| | | | | | 3 | Verify response propagation | Technical fault is propagated back through Adapter to ALAMOS FE2 | |
| | | | | | | | | |
| TC-038 | IPL Processing - Endpoint Unavailable | Negative | Verify handling when IPL endpoint is unavailable | FacadeService running; IPL endpoint unavailable | 1 | Submit a valid Domain Event | FacadeService attempts to invoke IPL | High |
| | | | | | 2 | Verify handling of unavailable endpoint | Communication failure is handled appropriately; error is propagated to ALAMOS FE2 | |
| | | | | | | | | |
| TC-039 | IPL Processing - Timeout | Negative | Verify handling when IPL endpoint times out | FacadeService running; IPL endpoint times out | 1 | Submit a valid Domain Event | FacadeService attempts to invoke IPL | High |
| | | | | | 2 | Verify timeout handling | Timeout is handled appropriately; error is propagated to ALAMOS FE2 | |
| | | | | | | | | |
| TC-040 | IPL Processing - Missing Required Data | Negative | Verify error when required data for IPL request is missing | FacadeService running | 1 | Submit a Domain Event with missing required data | FacadeService validates data | High |
| | | | | | 2 | Verify error response | Event is not submitted to IPL; error is returned **[Needs clarification: specific error code/message not documented]** | |

---

### Feature: Reliability – Retry & DLQ Validation (US-ADAPTER-RELIABILITY-001)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-041 | Retry - Recoverable Failure Retried | Functional | Verify recoverable communication failures are retried | Adapter/Gateway running; retry policies configured | 1 | Simulate a temporary communication failure during Situation Report processing | Initial attempt fails | High |
| | | | | | 2 | Verify retry behavior | Message is retried according to existing retry policy | |
| | | | | | 3 | Resolve the transient failure | Next retry succeeds | |
| | | | | | 4 | Verify successful processing | Message is processed successfully after retry | |
| | | | | | | | | |
| TC-042 | Retry - Transient Failure Resolution Within Limits | Functional | Verify messages process successfully when transient failures resolve within retry limits | Adapter/Gateway running | 1 | Simulate transient failures that resolve before retry limit is exceeded | Initial attempts fail | High |
| | | | | | 2 | Verify message processing | Message is processed successfully once transient failure resolves | |
| | | | | | | | | |
| TC-043 | DLQ - Retry Limit Exceeded | Functional | Verify messages are routed to DLQ when retry limits are exceeded | Adapter/Gateway running; DLQ configured | 1 | Simulate persistent communication failure | All retry attempts fail | High |
| | | | | | 2 | Verify DLQ routing | Message is routed to the existing DLQ | |
| | | | | | | | | |
| TC-044 | Retry - Business Validation Error No Retry | Negative | Verify business validation errors do not trigger unnecessary retries | Adapter/Gateway running | 1 | Simulate a business validation error (e.g., from IPL or ALAMOS) | Error is returned | High |
| | | | | | 2 | Verify no retry | Business validation error does not trigger retries | |
| | | | | | | | | |
| TC-045 | Retry - Logging and Traceability | Functional | Verify retry attempts and DLQ events are logged with diagnostic information | Adapter/Gateway running | 1 | Trigger retry scenarios and DLQ routing | Retries occur and message is routed to DLQ | High |
| | | | | | 2 | Verify logging | Retry attempts, DLQ events, and processing failures are logged with sufficient diagnostic information | |
| | | | | | | | | |
| TC-046 | Retry - Response Propagation | Functional | Verify success and fault responses are propagated correctly after retries | Adapter/Gateway running | 1 | Process a message that succeeds after retry | Processing completes | High |
| | | | | | 2 | Verify response propagation | Success response is propagated to the originating caller | |
| | | | | | | | | |
| TC-047 | DLQ - Investigation and Recovery | Edge Case | Verify DLQ messages can be investigated and recovered | DLQ contains messages | 1 | Route a message to DLQ | Message is in DLQ | Medium |
| | | | | | 2 | Verify DLQ message accessibility | DLQ messages are accessible for investigation and recovery **[Needs clarification: specific DLQ access/recovery procedures not documented]** | |

---

### Feature: ALAMOS Gateway – Legacy Alerting (US-ALAMOS-GW-001)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-048 | Alerting - Successful Processing with Squads | Functional | Verify Alerting request with squad information is processed successfully | ALAMOS Gateway running; ALAMOS FE2 available | 1 | Send a valid SOAP AlarmRequest from IPL containing squad information (`<squads>`) | Gateway receives the request | High |
| | | | | | 2 | Verify squad mapping | Squad information is correctly mapped to the ALAMOS request format | |
| | | | | | 3 | Verify forwarding to ALAMOS FE2 | Request is forwarded to ALAMOS FE2 via REST ALARM API | |
| | | | | | 4 | ALAMOS FE2 returns successful acknowledgment | Gateway receives success response | |
| | | | | | 5 | Verify response propagation to IPL | Success response is propagated back to IPL | |
| | | | | | | | | |
| TC-049 | Alerting - Successful Processing without Squads | Functional | Verify Alerting request without squad information is processed successfully (backward compatibility) | ALAMOS Gateway running; ALAMOS FE2 available | 1 | Send a valid SOAP AlarmRequest from IPL without squad information | Gateway receives the request | High |
| | | | | | 2 | Verify request is forwarded | Request is forwarded to ALAMOS FE2 | |
| | | | | | 3 | Verify successful acknowledgment | Success response is propagated back to IPL | |
| | | | | | | | | |
| TC-050 | Alerting - ALAMOS FE2 Business Error | Negative | Verify handling of ALAMOS FE2 business error | ALAMOS Gateway running; ALAMOS FE2 returns business error | 1 | Send a valid SOAP AlarmRequest from IPL | Gateway forwards to ALAMOS FE2 | High |
| | | | | | 2 | ALAMOS FE2 returns a business error | Gateway receives the error | |
| | | | | | 3 | Verify error propagation to IPL | Business error is propagated back to IPL | |
| | | | | | | | | |
| TC-051 | Alerting - ALAMOS FE2 Technical Error | Negative | Verify handling of ALAMOS FE2 technical error | ALAMOS Gateway running; ALAMOS FE2 returns technical error | 1 | Send a valid SOAP AlarmRequest from IPL | Gateway forwards to ALAMOS FE2 | High |
| | | | | | 2 | ALAMOS FE2 returns a technical error | Gateway receives the error | |
| | | | | | 3 | Verify error propagation to IPL | Technical error is propagated back to IPL | |
| | | | | | | | | |
| TC-052 | Alerting - Communication Timeout | Negative | Verify handling of communication timeout with ALAMOS FE2 | ALAMOS Gateway running; ALAMOS FE2 times out | 1 | Send a valid SOAP AlarmRequest from IPL | Gateway forwards to ALAMOS FE2 | High |
| | | | | | 2 | ALAMOS FE2 connection times out | Gateway handles timeout | |
| | | | | | 3 | Verify error response to IPL | Timeout error is handled and propagated back to IPL | |
| | | | | | | | | |
| TC-053 | Alerting - Invalid/Malformed Request | Negative | Verify invalid or malformed Alerting requests are rejected | ALAMOS Gateway running | 1 | Send an invalid or malformed SOAP AlarmRequest from IPL | Gateway validates the request | Medium |
| | | | | | 2 | Verify rejection | Request is rejected **[Needs clarification: specific error code/message not documented]** | |

---

### Feature: ALAMOS Gateway – Continuous Mission Updates (US-ALAMOS-GW-002)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-054 | Mission Update - Incident Status Change | Functional | Verify Continuous Mission Update is triggered and forwarded on incident status change | ALAMOS Gateway running; ALAMOS available | 1 | Trigger an incident status change in IPL | Mission Update is generated | High |
| | | | | | 2 | Verify Gateway processes the update | Gateway receives and transforms the update | |
| | | | | | 3 | Verify forwarding to ALAMOS | Update is forwarded to ALAMOS | |
| | | | | | 4 | Verify acknowledgment to IPL | ALAMOS response is propagated back to IPL | |
| | | | | | | | | |
| TC-055 | Mission Update - Resource Status Change | Functional | Verify Continuous Mission Update is triggered and forwarded on resource status change | ALAMOS Gateway running; ALAMOS available | 1 | Trigger a resource status change in IPL | Mission Update is generated | High |
| | | | | | 2 | Verify update is processed and forwarded | Update is forwarded to ALAMOS and response is propagated to IPL | |
| | | | | | | | | |
| TC-056 | Mission Update - Keyword Change | Functional | Verify Continuous Mission Update is triggered and forwarded on keyword change | ALAMOS Gateway running; ALAMOS available | 1 | Trigger a keyword change in IPL | Mission Update is generated | High |
| | | | | | 2 | Verify update is processed and forwarded | Update is forwarded to ALAMOS and response is propagated to IPL | |
| | | | | | | | | |
| TC-057 | Mission Update - Location Change | Functional | Verify Continuous Mission Update is triggered and forwarded on location change | ALAMOS Gateway running; ALAMOS available | 1 | Trigger a location change in IPL | Mission Update is generated | High |
| | | | | | 2 | Verify update is processed and forwarded | Update is forwarded to ALAMOS and response is propagated to IPL | |
| | | | | | | | | |
| TC-058 | Mission Update - ALAMOS Business Error | Negative | Verify handling of ALAMOS business error for Mission Updates | ALAMOS Gateway running; ALAMOS returns business error | 1 | Trigger a Mission Update | Gateway forwards to ALAMOS | High |
| | | | | | 2 | ALAMOS returns business error | Error is propagated back to IPL | |
| | | | | | | | | |
| TC-059 | Mission Update - ALAMOS Technical Error | Negative | Verify handling of ALAMOS technical error for Mission Updates | ALAMOS Gateway running; ALAMOS returns technical error | 1 | Trigger a Mission Update | Gateway forwards to ALAMOS | High |
| | | | | | 2 | ALAMOS returns technical error | Error is propagated back to IPL | |
| | | | | | | | | |
| TC-060 | Mission Update - Backward Compatibility | Functional | Verify existing Mission Update functionality remains backward compatible | ALAMOS Gateway running | 1 | Execute Mission Updates using existing gateway implementation | Updates are processed | High |
| | | | | | 2 | Verify backward compatibility | Existing functionality remains unaffected | |

---

### Feature: ALAMOS Gateway – Squad Information Extension (US-ALAMOS-GW-003)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-061 | Squad Info - Single Squad Extraction and Mapping | Functional | Verify single squad information is extracted and mapped correctly | ALAMOS Gateway running | 1 | Send Alerting request with single squad in `<squads>` | Gateway receives the request | High |
| | | | | | 2 | Verify extraction and mapping | Squad information is extracted and mapped to ALAMOS message structure | |
| | | | | | | | | |
| TC-062 | Squad Info - Multiple Squads | Functional | Verify multiple squad entries are supported | ALAMOS Gateway running | 1 | Send Alerting request with multiple squads in `<squads>` | Gateway receives the request | High |
| | | | | | 2 | Verify all squads are mapped | All squad entries are correctly mapped to ALAMOS message structure | |
| | | | | | | | | |
| TC-063 | Squad Info - No Squad Information (Backward Compatibility) | Edge Case | Verify Alerting requests without squad information continue to work | ALAMOS Gateway running | 1 | Send Alerting request without `<squads>` element | Gateway receives the request | High |
| | | | | | 2 | Verify request is processed successfully | Request is processed without errors; backward compatibility maintained | |
| | | | | | | | | |
| TC-064 | Squad Info - Acknowledgment Propagation | Functional | Verify acknowledgments are propagated back to IPL without loss | ALAMOS Gateway running; ALAMOS FE2 available | 1 | Send Alerting request with squad information | Request is processed by ALAMOS FE2 | High |
| | | | | | 2 | Verify acknowledgment | Acknowledgment is propagated back to IPL without loss of information | |
| | | | | | | | | |
| TC-065 | Squad Info - E2E Verification | Functional | Verify squad information is correctly transmitted to ALAMOS FE2 end-to-end | ALAMOS Gateway running; ALAMOS FE2 available | 1 | Send Alerting request with squad information | Request reaches ALAMOS FE2 | High |
| | | | | | 2 | Verify squad data at ALAMOS FE2 | Squad information is correctly transmitted and received by ALAMOS FE2 | |

---

### Feature: ALAMOS Gateway – Mock Service (US-ALAMOSGW-MOCK-001)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-066 | Mock Mode - Startup | Functional | Verify ALAMOS Gateway starts successfully in mock mode | Mock mode configuration enabled | 1 | Start ALAMOS Gateway in mock mode | Gateway starts as standalone application | High |
| | | | | | 2 | Verify mock mode is active | Mock mode is operational | |
| | | | | | | | | |
| TC-067 | Mock Mode - Predefined Success Responses | Functional | Verify mock mode returns predefined success responses | Gateway running in mock mode | 1 | Send a valid Alerting request | Gateway processes in mock mode | High |
| | | | | | 2 | Verify response | Predefined success response is returned without connecting to ALAMOS FE2 | |
| | | | | | | | | |
| TC-068 | Mock Mode - Configurable Error Responses | Functional | Verify mock mode supports configurable error responses | Gateway running in mock mode; error response configured | 1 | Configure mock mode to return an error | Configuration is applied | High |
| | | | | | 2 | Send a request | Gateway returns configured error response | |
| | | | | | | | | |
| TC-069 | Mock Mode - Alerting with Squads | Functional | Verify Alerting requests with squad information are testable in mock mode | Gateway running in mock mode | 1 | Send Alerting request with squad information | Gateway processes in mock mode | High |
| | | | | | 2 | Verify mock response | Request is processed and mock response is returned | |
| | | | | | | | | |
| TC-070 | Mock Mode - Continuous Mission Updates | Functional | Verify Mission Update requests are testable in mock mode | Gateway running in mock mode | 1 | Send Mission Update request | Gateway processes in mock mode | High |
| | | | | | 2 | Verify mock response | Request is processed and mock response is returned | |
| | | | | | | | | |
| TC-071 | Mock Mode - No Impact When Disabled | Edge Case | Verify mock mode configuration does not impact normal gateway operation when disabled | Mock mode disabled | 1 | Disable mock mode | Configuration updated | High |
| | | | | | 2 | Start gateway in normal mode | Gateway starts normally | |
| | | | | | 3 | Verify normal operation | Gateway operates normally; mock configuration has no impact | |

---

### Feature: End-to-End Integration Testing (US-INTEGRATION-E2E-001)

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-072 | E2E - Alerting with Squad Information | Functional | Validate complete Alerting with Squad Information flow end-to-end | All components running | 1 | Send SOAP AlarmRequest with squads from IPL | Request enters the system | High |
| | | | | | 2 | Verify flow through all components | Request flows: IPL → Facade Service → ALAMOS Gateway → ALAMOS FE2 | |
| | | | | | 3 | Verify squad transmission | Squad information is correctly transmitted to ALAMOS FE2 | |
| | | | | | 4 | Verify acknowledgment propagation | Acknowledgment flows back: ALAMOS FE2 → ALAMOS Gateway → Facade Service → IPL | |
| | | | | | | | | |
| TC-073 | E2E - Continuous Mission Update | Functional | Validate complete Continuous Mission Update flow end-to-end | All components running | 1 | Trigger Mission Update from IPL | Update enters the system | High |
| | | | | | 2 | Verify flow through ALAMOS Gateway | Update is processed and forwarded to ALAMOS | |
| | | | | | 3 | Verify response propagation | Response is propagated back to IPL | |
| | | | | | | | | |
| TC-074 | E2E - Situation Report | Functional | Validate complete Situation Report flow end-to-end | All components running | 1 | Send Situation Report from ALAMOS FE2 | Report enters the Adapter | High |
| | | | | | 2 | Verify Domain Event creation | `incident.situation_report_received` event is created | |
| | | | | | 3 | Verify FacadeService processing | Event is routed and mapped to IPL request | |
| | | | | | 4 | Verify IPL invocation | IPL `erzeugeEinsatzmeldung` is invoked | |
| | | | | | 5 | Verify acknowledgment to ALAMOS FE2 | Acknowledgment is propagated back to ALAMOS FE2 | |
| | | | | | | | | |
| TC-075 | E2E - Failure Propagation | Negative | Validate business/technical failures propagate correctly end-to-end | All components running | 1 | Trigger a business validation failure | Failure occurs in the flow | High |
| | | | | | 2 | Verify failure propagation | Failure is propagated correctly to the originating system | |
| | | | | | | | | |
| TC-076 | E2E - Retry and DLQ | Functional | Validate retry and DLQ mechanisms end-to-end | All components running | 1 | Trigger failure scenarios | Failures occur | High |
| | | | | | 2 | Verify retry behavior | Retries occur as expected | |
| | | | | | 3 | Exceed retry limits | Message goes to DLQ | |
| | | | | | 4 | Verify no message loss | No unexpected message loss occurs | |
| | | | | | | | | |
| TC-077 | E2E - Logging and Traceability | Functional | Verify logging and traceability across all integration flows | All components running | 1 | Execute all integration flows | Flows complete | High |
| | | | | | 2 | Verify logs | Logging, monitoring, and traceability information are available across all flows | |

---

### Boundary Value Analysis

| TID | Test Case Name | Category | Description | Pre-conditions | Step No | Step Description | Expected Result | Priority |
|-----|----------------|----------|-------------|----------------|---------|------------------|-----------------|----------|
| TC-078 | Boundary - Minimum Valid Payload | Boundary | Verify minimum valid Situation Report payload is accepted | Adapter running | 1 | Send Situation Report with minimum required fields only | Adapter accepts the request | Medium |
| | | | | | 2 | Verify processing | Request is processed successfully | |
| | | | | | | | | |
| TC-079 | Boundary - Single Squad Entry | Boundary | Verify single squad entry boundary | ALAMOS Gateway running | 1 | Send Alerting with exactly one squad entry | Gateway processes the request | Medium |
| | | | | | 2 | Verify mapping | Single squad is mapped correctly | |
| | | | | | | | | |
| TC-080 | Boundary - Empty Squads Element | Boundary | Verify empty squads element handling | ALAMOS Gateway running | 1 | Send Alerting with empty `<squads>` element | Gateway processes the request | Medium |
| | | | | | 2 | Verify handling | Request is handled appropriately **[Needs clarification: expected behavior for empty squads not documented]** | |
| | | | | | | | | |
| TC-081 | Boundary - Payload Size Limits | Boundary | Verify payload size limit handling | Adapter/Gateway running | 1 | Send payloads at/near size limits | Request is submitted | Low |
| | | | | | 2 | Verify handling | **[Needs clarification: payload size limits not documented]** | |
| | | | | | | | | |
| TC-082 | Boundary - Retry Limit Exact | Boundary | Verify behavior at exact retry limit | Adapter/Gateway running | 1 | Cause failures up to exactly the configured retry limit | Retries occur | Medium |
| | | | | | 2 | Verify DLQ routing at exact limit | Message is routed to DLQ when retry limit is exactly exceeded **[Needs clarification: exact retry limit values not documented]** | |
| | | | | | | | | |
| TC-083 | Boundary - Timeout Threshold | Boundary | Verify behavior at communication timeout threshold | Adapter/Gateway running | 1 | Simulate response times at timeout threshold | Request is submitted | Medium |
| | | | | | 2 | Verify timeout handling | **[Needs clarification: timeout threshold values not documented]** | |

---

## Traceability Matrix

| Test Case ID Range | Feature | User Story |
|--------------------|---------|------------|
| TC-001 – TC-012 | Situation Reports – Receive & Validate | US-ADAPTER-ALAMOS-001 |
| TC-013 – TC-023 | Situation Reports – Domain Event Generation | US-ADAPTER-ALAMOS-002 |
| TC-024 – TC-032 | FacadeService – Routing Layer | US-ADAPTER-ALAMOS-003 |
| TC-033 – TC-040 | FacadeService – IPL Processing | US-ADAPTER-ALAMOS-004 |
| TC-041 – TC-047 | Reliability – Retry & DLQ | US-ADAPTER-RELIABILITY-001 |
| TC-048 – TC-053 | ALAMOS Gateway – Legacy Alerting | US-ALAMOS-GW-001 |
| TC-054 – TC-060 | ALAMOS Gateway – Continuous Mission Updates | US-ALAMOS-GW-002 |
| TC-061 – TC-065 | ALAMOS Gateway – Squad Information Extension | US-ALAMOS-GW-003 |
| TC-066 – TC-071 | ALAMOS Gateway – Mock Service | US-ALAMOSGW-MOCK-001 |
| TC-072 – TC-077 | End-to-End Integration Testing | US-INTEGRATION-E2E-001 |
| TC-078 – TC-083 | Boundary Value Analysis | Cross-feature |

---

## Items Requiring Clarification

| Item | Reference | Issue |
|------|-----------|-------|
| Specific error codes/messages | Multiple features | No error codes or message text documented in source documents |
| Exact HTTP method for Situation Report endpoint | US-ADAPTER-ALAMOS-001 | REST method/path not specified |
| Valid content types | US-ADAPTER-ALAMOS-001 | Supported content types not documented |
| call_sign fallback logic | US-ADAPTER-ALAMOS-002 | Fallback handling logic details not documented |
| Empty squads element handling | US-ALAMOS-GW-003 | Expected behavior not documented |
| Payload size limits | All features | No size limits documented |
| Retry limit values | US-ADAPTER-RELIABILITY-001 | Specific retry limits not documented |
| Timeout threshold values | Multiple features | Communication timeout thresholds not documented |
| DLQ access/recovery procedures | US-ADAPTER-RELIABILITY-001 | Specific procedures not documented |
