# Testing Context: UCRI 2.0 P2P Integration (IPL-Adapter-UCRM) — Revised

## Scope

### In Scope
- **Forward Flow Testing:** IPL → Adapter (Receiver → Handler → Dispatcher) → UCRM end-to-end message flow
- **Reverse Flow Testing:** UCRM → Adapter (Receiver → Handler → Dispatcher) → IPL mission dispatch flow
- **Adapter Validation (Receiver):** Incoming request validation at Receiver service
- **P2P Authentication (Handler):** Adapter to UCRM authentication via P2P token
- **Message Forwarding (Dispatcher):** messaging/send endpoint and `/einsatztransfer/quittiereTranferEinsatz` functionality
- **Accept Handling:** UCRM Accept → ACK with `EMPFANG` logged via `Einsatztransfer/quittiereTranferEinsatz`
- **Reject Handling:** UCRM Reject → ACK with `EINSATZ_ABGELEHNT` logged via `Einsatztransfer/quittiereTranferEinsatz`
- **Timeout Handling:** UCRM no response → ACK with `TECHNISCHER_FEHLER` logged via `Einsatztransfer/quittiereTranferEinsatz`
- **Reverse Flow ACK:** IPL Accept/Reject acknowledgment for UCRM missions
- **In-Memory Transport:** Vert.x EventBus for Receiver → Handler → Dispatcher communication
- **Module Configuration:** Enable/disable Receiver, Handler, Dispatcher individually
- **Bi-directional Communication:** Full round-trip message flow validation
- **Logging & Traceability:** P2P flow logging, monitoring, ACK status verification
- **Field Mapping Validation:** TransferEinsatz to UCRM operation mapping
- **UCRM Test Client:** Test client installation and usage validation
- **Cross-Cutting Concerns:** Retry decorator, DLQ, metrics validation
- **End-to-End Flow:** Receiver → Handler → Dispatcher with in-memory transport

### Out of Scope
- UI Testing (Not applicable — backend service only)
- Database Testing (Not specified in requirements — prototype excludes persistence)
- Patient Data Processing (Excluded from prototype)
- Kafka Transport Testing (Phase 1 focuses on in-memory transport only)
- Performance Benchmarking (Not explicitly specified) [NEEDS CLARIFICATION]
- Load Testing (Not specified in requirements)
- Security Penetration Testing (Not specified in requirements)

## Test Data

### Mission/Event Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid TransferEinsatzRequest | JSON payload with mission data via `/einsatztransfer/erzeugeEinsatz` | Forward flow happy path |
| Invalid TransferEinsatzRequest | Malformed/incomplete payload | Receiver validation negative test |
| Empty Payload | Empty body | Boundary test |
| Valid sourceMandant | Sender client identifier (e.g., IPL_CENTER_001) | Header mapping validation |
| Valid targetMandant | Receiver client identifier (e.g., UCRI_CENTER_001) | Header mapping validation |
| Valid einsatzId | Operation identifier | Operation ID mapping |
| Valid einsatznummerKurz | Short incident number | Operation name mapping |
| Valid kategorie | Incident category code | Occasion type_1 mapping |
| Valid einsatzStichwort | Alarm keyword (coded) | Occasion keyword_1 mapping |

### Authentication Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid P2P Token | Authorized authentication token | P2P authentication happy path |
| Invalid P2P Token | Expired/revoked token | Authentication failure test |
| Missing P2P Token | No token provided | Authentication boundary test |

### ACK Response Data
| Data Type | Value | Log Verification | Purpose |
|-----------|-------|------------------|---------|
| UCRM Accept Response | Accept ACK | `Einsatztransfer/quittiereTranferEinsatz` → `EMPFANG` | Acceptance flow |
| UCRM Reject Response | Reject ACK | `Einsatztransfer/quittiereTranferEinsatz` → `EINSATZ_ABGELEHNT` | Rejection flow |
| UCRM Timeout (No Response) | Timeout | `Einsatztransfer/quittiereTranferEinsatz` → `TECHNISCHER_FEHLER` | Timeout flow |
| IPL Accept ACK | Accept for reverse flow | N/A | Reverse flow ACK test |
| IPL Reject ACK | Reject for reverse flow | N/A | Reverse flow rejection test |

### Reverse Flow Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| UCRM Mission Payload | Mission data from UCRM | Reverse flow testing |
| IPL Accept ACK | Accept acknowledgment from IPL | Reverse flow acceptance |
| IPL Reject ACK | Reject acknowledgment from IPL | Reverse flow rejection |

### Transport & Module Configuration Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Transport config | adapter.transport=in-memory | Validate in-memory mode |
| Invalid transport | adapter.transport=invalid | Validate error handling |
| Missing transport | (property absent) | Validate startup failure |
| Receiver enabled | adapter.receiver.enabled=true/false | Module toggle test |
| Handler enabled | adapter.handler.enabled=true/false | Module toggle test |
| Dispatcher enabled | adapter.dispatcher.enabled=true/false | Module toggle test |

### Traceability Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Correlation ID | Unique identifier value | Traceability and observability |
| Headers | Key-value metadata pairs | Metadata propagation validation |
| Partition Key | Logical entity identifier | Ordering validation |

## Test Environment

- **Tool:** Postman (primary), JUnit (unit tests)
- **Test Client:** UCRM Test Client (per deployment guide)
- **Protocol:** P2P Messaging / REST
- **Transport:** In-Memory (Vert.x EventBus) for Phase 1
- **Authentication:** P2P Token-based
- **Browser:** Not applicable (API testing only)
- **Device:** Desktop
- **OS:** Linux (recommended), Windows compatible
- **Java Version:** Java 17+ (OpenJDK recommended)

## Dependencies

### Required Services
- IPL system must be running (or mock IPL)
- UCRM must be accessible via P2P connection
- Adapter service deployed: all three services (Receiver, Handler, Dispatcher) must be started
- UCRM Test Client must be installed (per User Story A10)

### Prerequisites
- UCRM Test Client scope and prerequisites confirmed (per User Story A9)
- P2P authentication tokens must be provisioned
- Network connectivity between IPL, Adapter (Receiver + Handler + Dispatcher), and UCRM established
- Logging infrastructure operational for ACK status verification
- `adapter.transport=in-memory` configured for Phase 1

### Pre-Test Setup
- Follow UCRM Test Client deployment guide
- Verify all service connectivity (IPL ↔ Adapter ↔ UCRM)
- Confirm P2P token validity
- Validate logging configuration — ensure logs capture `Einsatztransfer/quittiereTranferEinsatz` entries
- Verify Receiver, Handler, Dispatcher modules enabled in configuration

## Test Scenarios

### Forward Flow Tests (IPL → Adapter → UCRM)

#### Scenario 1: Happy Path — Event Sent and Accepted (EMPFANG)
1. IPL sends valid TransferEinsatzRequest to Adapter via `/einsatztransfer/erzeugeEinsatz`
2. Receiver validates request (passes)
3. Handler authenticates to UCRM via P2P token
4. Handler transforms IPL payload to UCRM format
5. Dispatcher forwards message to UCRM via messaging/send
6. UCRM accepts and returns Accept response
7. Receiver receives Accept response from UCRM
8. Handler translates to IPL ACK format
9. Dispatcher calls `/einsatztransfer/quittiereTranferEinsatz` with Accept
10. **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `EMPFANG`

#### Scenario 2: Happy Path — Event Sent and Rejected (EINSATZ_ABGELEHNT)
1. IPL sends valid TransferEinsatzRequest to Adapter via `/einsatztransfer/erzeugeEinsatz`
2. Receiver validates request (passes)
3. Handler authenticates and transforms payload
4. Dispatcher forwards to UCRM via messaging/send
5. UCRM rejects and returns Reject response
6. Handler translates to IPL ACK format
7. Dispatcher calls `/einsatztransfer/quittiereTranferEinsatz` with Reject
8. **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `EINSATZ_ABGELEHNT`

#### Scenario 3: Timeout — UCRM Does Not Respond (TECHNISCHER_FEHLER)
1. IPL sends valid TransferEinsatzRequest to Adapter via `/einsatztransfer/erzeugeEinsatz`
2. Receiver validates request (passes)
3. Handler authenticates and transforms payload
4. Dispatcher forwards to UCRM via messaging/send
5. UCRM does not respond within allowed time
6. Handler detects timeout condition
7. Dispatcher calls `/einsatztransfer/quittiereTranferEinsatz` with Timeout error
8. **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `TECHNISCHER_FEHLER`

#### Scenario 4: Validation Failure at Receiver
1. IPL sends invalid/malformed payload to Adapter via `/einsatztransfer/erzeugeEinsatz`
2. Receiver validation fails
3. Receiver returns validation error to IPL
4. IPL handles validation response
5. **Verify:** No message forwarded to Handler or Dispatcher
6. **Verify:** No `Einsatztransfer/quittiereTranferEinsatz` log entry generated

#### Scenario 5: P2P Authentication Failure at Handler
1. IPL sends valid event to Adapter
2. Receiver validates (passes), forwards to Handler
3. Handler attempts P2P authentication with invalid/expired token
4. Authentication fails
5. Error propagated back to IPL
6. **Verify:** No message forwarded to UCRM via Dispatcher

### Reverse Flow Tests (UCRM → Adapter → IPL)

#### Scenario 6: Mission Received and Accepted by IPL
1. UCRM sends mission to Adapter via messaging/send
2. Receiver accepts mission payload
3. Handler translates UCRM mission to IPL format
4. Dispatcher forwards mission to IPL
5. IPL processes mission successfully
6. IPL sends Accept ACK to Adapter
7. Receiver receives ACK, Handler translates
8. Dispatcher propagates Accept ACK to UCRM

#### Scenario 7: Mission Received and Rejected by IPL
1. UCRM sends mission to Adapter via messaging/send
2. Receiver accepts, Handler translates, Dispatcher forwards to IPL
3. IPL rejects mission
4. IPL sends Reject ACK to Adapter
5. Adapter propagates Reject ACK to UCRM

#### Scenario 8: Reverse Flow — IPL Does Not Respond (Timeout)
1. UCRM sends mission to Adapter
2. Adapter forwards to IPL
3. IPL does not respond within allowed time
4. Adapter handles timeout
5. **Verify:** Timeout handling for reverse flow [NEEDS CLARIFICATION]

### In-Memory Transport Tests

#### Scenario 9: In-Memory Transport Initialization
1. Configure `adapter.transport=in-memory`
2. Start Adapter service (Receiver, Handler, Dispatcher)
3. Verify startup logs indicate in-memory transport active
4. Verify no external Kafka broker connection attempted

#### Scenario 10: End-to-End Flow via In-Memory Transport
1. Configure in-memory transport with all modules enabled
2. Send event to Receiver
3. Verify Receiver validates and forwards to Handler via in-memory bus
4. Verify Handler processes and forwards to Dispatcher via in-memory bus
5. Verify Dispatcher routes to correct dispatch center topic (events-ucri)
6. Confirm envelope metadata (correlationId, headers) preserved end-to-end

#### Scenario 11: Event Ordering with In-Memory Transport
1. Publish multiple events with same partition key
2. Verify events delivered in published order
3. Confirm ordering preserved based on partition key

### Module Configuration Tests

#### Scenario 12: Receiver Module Disable/Enable
1. Set `adapter.receiver.enabled=false`
2. Start service → verify no event subscriptions created
3. Set `adapter.receiver.enabled=true` → verify Receiver functional

#### Scenario 13: Handler Module Disable/Enable
1. Set `adapter.handler.enabled=false`
2. Send event → verify Receiver accepts but Handler does not process
3. Enable Handler → verify full flow works

#### Scenario 14: Dispatcher Module Disable/Enable
1. Set `adapter.dispatcher.enabled=false`
2. Process event through Handler → verify no dispatch to target
3. Enable Dispatcher → verify routing works

### ACK Log Verification Tests

#### Scenario 15: Verify EMPFANG Log Entry
1. Complete forward flow with UCRM Accept
2. Check adapter logs for `Einsatztransfer/quittiereTranferEinsatz`
3. **Verify:** Log contains `EMPFANG`
4. Verify correlationId matches original request

#### Scenario 16: Verify EINSATZ_ABGELEHNT Log Entry
1. Complete forward flow with UCRM Reject
2. Check adapter logs for `Einsatztransfer/quittiereTranferEinsatz`
3. **Verify:** Log contains `EINSATZ_ABGELEHNT`
4. Verify correlationId matches original request

#### Scenario 17: Verify TECHNISCHER_FEHLER Log Entry
1. Complete forward flow where UCRM times out
2. Check adapter logs for `Einsatztransfer/quittiereTranferEinsatz`
3. **Verify:** Log contains `TECHNISCHER_FEHLER`
4. Verify correlationId matches original request

### Cross-Cutting Tests

#### Scenario 18: Logging and Traceability Across All 3 Services
1. Execute forward flow test
2. Verify Receiver logs event receipt with correlationId
3. Verify Handler logs transformation with correlationId
4. Verify Dispatcher logs dispatch with correlationId
5. Confirm end-to-end traceability across Receiver → Handler → Dispatcher

#### Scenario 19: Field Mapping Validation
1. Send TransferEinsatzRequest with all mappable fields
2. Verify sourceMandant → header.sender_client_id mapping
3. Verify targetMandant → header.receiver_client_id mapping
4. Verify einsatzId → operation.id mapping
5. Verify einsatznummerKurz → operation.name mapping
6. Verify kategorie → operation.occassion.type_1 mapping
7. Verify einsatzStichwort → operation.occassion.keyword_1 mapping
8. Confirm no data loss in translation

#### Scenario 20: UCRM Test Client Validation
1. Install UCRM Test Client per deployment guide
2. Verify prerequisites are met
3. Execute basic connectivity test
4. Validate Test Client functionality

#### Scenario 21: Cross-Cutting — Retry Decorator
1. Configure retry (3 attempts, 1000ms delay)
2. Simulate transient Dispatcher publish failure
3. Verify retry occurs per configuration
4. Verify metrics reflect retry attempts

#### Scenario 22: Cross-Cutting — Dead Letter Queue
1. Configure DLQ for UCRI dispatch center
2. Send event that fails permanently after all retries
3. Verify event sent to DLQ topic (events-ucri-dlq)
4. Confirm DLQ entry contains original payload and error context

#### Scenario 23: Invalid Transport Configuration
1. Set `adapter.transport=invalid_value`
2. Start service → verify startup fails with descriptive error

## Validation Methods

### Log-Based Verification (Primary)
| Log Entry | Expected Value | Scenario |
|-----------|---------------|----------|
| `Einsatztransfer/quittiereTranferEinsatz` | `EMPFANG` | Accepted case |
| `Einsatztransfer/quittiereTranferEinsatz` | `EINSATZ_ABGELEHNT` | Rejected case |
| `Einsatztransfer/quittiereTranferEinsatz` | `TECHNISCHER_FEHLER` | Timeout case |

### Service-Level Log Verification
- **Receiver logs:** Event receipt, validation pass/fail
- **Handler logs:** Transformation, authentication, timeout detection
- **Dispatcher logs:** Message forwarding, ACK propagation, retry attempts
- **Transport logs:** Startup confirmation (in-memory/kafka active)

### Response Verification
- Correct HTTP status codes from `/einsatztransfer/erzeugeEinsatz`
- Proper ACK format from `/einsatztransfer/quittiereTranferEinsatz`
- Error messages match specification

### Metric-Based Verification
- Publish count per dispatch center (UCRI)
- Receive count per channel
- Failure/timeout count
- Latency metrics

## Acceptance Criteria

### Forward Flow
- [ ] IPL sends event to Adapter via `/einsatztransfer/erzeugeEinsatz`
- [ ] Receiver validates incoming requests correctly
- [ ] P2P authentication at Handler succeeds with valid token
- [ ] Dispatcher forwards message to UCRM via messaging/send
- [ ] UCRM Accept → log shows `EMPFANG` on `Einsatztransfer/quittiereTranferEinsatz`
- [ ] UCRM Reject → log shows `EINSATZ_ABGELEHNT` on `Einsatztransfer/quittiereTranferEinsatz`
- [ ] UCRM Timeout → log shows `TECHNISCHER_FEHLER` on `Einsatztransfer/quittiereTranferEinsatz`
- [ ] Outcome propagated to IPL via `/einsatztransfer/quittiereTranferEinsatz`

### Reverse Flow
- [ ] UCRM mission received at Adapter (Receiver)
- [ ] Mission translated (Handler) and forwarded (Dispatcher) to IPL
- [ ] IPL Accept ACK sent and propagated to UCRM
- [ ] IPL Reject ACK sent and propagated to UCRM

### In-Memory Transport
- [ ] Receiver → Handler → Dispatcher flow works with in-memory transport
- [ ] Envelope metadata preserved end-to-end
- [ ] Event ordering preserved based on partition key
- [ ] No external infrastructure required

### Module Configuration
- [ ] Receiver can be enabled/disabled
- [ ] Handler can be enabled/disabled
- [ ] Dispatcher can be enabled/disabled
- [ ] Disabled modules consume no resources

### Cross-Cutting
- [ ] Logging across all 3 services with correlationId traceability
- [ ] Retry decorator works
- [ ] DLQ handles permanent failures
- [ ] Monitoring metrics operational

## Known Issues

### Current Prototype Limitations
- Mock IPL service only; real IPL system integration deferred
- No data persistence or caching implemented
- Testing performed in controlled environments only
- Patient data inside mission dispatch message is not processed
- No automatic error recovery in prototype

### ACK/Log Considerations
- Three ACK statuses verified via log: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER
- Exact timeout threshold for TECHNISCHER_FEHLER not specified [NEEDS CLARIFICATION] — 10-second ACK requirement documented for WDX; UCRM timeout threshold may differ
- Reverse flow timeout handling not explicitly specified [NEEDS CLARIFICATION]

### Data Mapping Considerations
- Detailed UCRM-specific field mapping beyond WDX fields requires clarification from "IPL-Mapping (UCRI)" document

## Test Deliverables Checklist

- [ ] Forward flow — Accept (EMPFANG) tested end-to-end
- [ ] Forward flow — Reject (EINSATZ_ABGELEHNT) tested end-to-end
- [ ] Forward flow — Timeout (TECHNISCHER_FEHLER) tested end-to-end
- [ ] Reverse flow (UCRM → Adapter → IPL) tested end-to-end
- [ ] Receiver validation logic verified
- [ ] P2P authentication at Handler verified
- [ ] Dispatcher message forwarding verified
- [ ] ACK log verification: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER
- [ ] In-memory transport (Receiver → Handler → Dispatcher) validated
- [ ] Module enable/disable tested for all 3 services
- [ ] Field mapping accuracy verified
- [ ] Logging and traceability across all 3 services verified
- [ ] UCRM Test Client deployment validated
- [ ] Retry and DLQ handling validated
- [ ] All user stories covered with test scenarios
