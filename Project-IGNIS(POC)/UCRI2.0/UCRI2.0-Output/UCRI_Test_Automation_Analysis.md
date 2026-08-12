# UCRI 2.0 Test Automation Analysis

## Source: TestCases_20260428_105917.xlsx
## Total Test Cases: 48

---

## Automation Feasibility Summary

| Category | Total TCs | Automatable (Shell) | Partially Automatable | Not Automatable |
|----------|-----------|---------------------|-----------------------|-----------------|
| In-Memory Transport (IMT) | 13 | 8 | 3 | 2 |
| Forward Flow (FWD) | 14 | 12 | 2 | 0 |
| Reverse Flow (REV) | 8 | 6 | 2 | 0 |
| Cross-Client (U2U) | 12 | 9 | 2 | 1 |
| Test Client (TC) | 2 | 1 | 0 | 1 |
| **Total** | **48** | **36** | **9** | **4** |

---

## Fully Automatable via Shell Script (36 Test Cases)

These test cases can be automated using `curl` (REST API calls), `grep`/`jq` (log/response verification), and shell configuration commands.

### In-Memory Transport (IMT)
| TID | Test Case | Automation Approach |
|-----|-----------|---------------------|
| IMT-001 | In-Memory Transport Initialization | Set config, start service, grep startup logs |
| IMT-004 | Envelope Metadata Preservation | Send event via curl, grep logs for correlationId |
| IMT-005 | Invalid Event Rejected by Receiver | Send malformed event via curl, verify rejection |
| IMT-006 | Receiver Module Disabled | Set config, start service, verify module state in logs |
| IMT-007 | Handler Module Disabled | Set config, start service, send event, verify logs |
| IMT-008 | Dispatcher Module Disabled | Set config, start service, send event, verify logs |
| IMT-009 | Invalid Transport Configuration | Set invalid config, attempt start, check error |
| IMT-010 | Missing Transport Configuration | Remove config, attempt start, check error |

### Forward Flow — IPL to UCRI (FWD)
| TID | Test Case | Automation Approach |
|-----|-----------|---------------------|
| FWD-001 | Happy Path: Event Accepted (EMPFANG) | curl POST /einsatztransfer/erzeugeEinsatz, verify 200/202 + EMPFANG ACK |
| FWD-002 | Event Rejected (EINSATZ_ABGELEHNT) | curl POST, verify rejection ACK |
| FWD-003 | Timeout (TECHNISCHER_FEHLER) | curl POST, wait for timeout, verify error ACK |
| FWD-004 | Validation Failure at Receiver | curl POST with invalid payload, verify error response |
| FWD-005 | P2P Authentication Failure | curl POST with invalid token, verify auth error |
| FWD-006 | Field Mapping Validation | curl POST, verify response field mappings via jq |
| FWD-007 | Missing sourceMandant | curl POST without sourceMandant, verify validation error |
| FWD-008 | Missing targetMandant | curl POST without targetMandant, verify validation error |
| FWD-009 | Missing einsatzId | curl POST without einsatzId, verify validation error |
| FWD-010 | Empty Payload | curl POST with empty body, verify rejection |
| FWD-011 | UCRI Dispatch Center Disabled | Set config, curl POST, verify no dispatch |
| FWD-012 | CorrelationId Traceability | curl POST with unique correlationId, grep logs |

### Reverse Flow — UCRI to IPL (REV)
| TID | Test Case | Automation Approach |
|-----|-----------|---------------------|
| REV-001 | Happy Path: Mission Accepted | curl POST messaging/send, verify ACK propagation |
| REV-002 | Mission Rejected by IPL | curl POST, verify Reject ACK |
| REV-003 | IPL Timeout | curl POST, verify timeout handling |
| REV-004 | Invalid Mission Payload | curl POST with malformed data, verify rejection |
| REV-005 | Field Mapping Validation | curl POST, verify field mappings |
| REV-006 | CorrelationId Traceability | curl POST, grep logs for correlationId |

### Cross-Client — UCRI to UCRI (U2U)
| TID | Test Case | Automation Approach |
|-----|-----------|---------------------|
| U2U-001 | Happy Path: UCRI-1 to UCRI-2 Accepted | curl POST with cross-client mandants, verify ACK |
| U2U-002 | Mission Rejected by UCRI-2 | curl POST, verify Reject ACK |
| U2U-003 | Timeout (UCRI-2 No Response) | curl POST, verify timeout handling |
| U2U-004 | Reverse Direction: UCRI-2 to UCRI-1 | curl POST reverse direction, verify ACK |
| U2U-005 | Invalid sourceMandant | curl POST with unknown sender, verify rejection |
| U2U-006 | Invalid targetMandant | curl POST with unknown target, verify error |
| U2U-007 | P2P Auth Failure Cross-Client | curl POST with invalid token, verify auth error |
| U2U-008 | Field Mapping Cross-Client | curl POST, verify field mappings |
| U2U-009 | CorrelationId Traceability | curl POST, grep logs |

### Test Client (TC)
| TID | Test Case | Automation Approach |
|-----|-----------|---------------------|
| TC-002 | Send Mission and Receive ACK | curl POST via test client API, verify ACK |

---

## Partially Automatable (9 Test Cases)

These require simulation of specific conditions (transient failures, timing, parallel execution) that are achievable but complex in shell scripts.

| TID | Test Case | Challenge |
|-----|-----------|-----------|
| IMT-002 | End-to-End Flow | Requires internal EventBus verification beyond API layer |
| IMT-003 | Event Ordering Preservation | Timing-sensitive; needs rapid sequential sends + order verification |
| IMT-011 | Retry Decorator | Requires transient failure simulation at Dispatcher |
| IMT-012 | Dead Letter Queue | Requires permanent failure simulation + DLQ topic access |
| IMT-013 | Logging Traceability | Requires log file access across 3 service modules |
| FWD-013 | Multiple Events Same Partition Key | Timing-sensitive; ordering verification at UCRM |
| FWD-014 | P2P Token Expired During Session | Requires token expiry timing control |
| REV-007 | Multiple Missions Sequential | Requires sequential processing verification |
| REV-008 | ACK Propagation Timing | Requires timing measurement |

---

## Not Automatable via Shell Script (4 Test Cases)

| TID | Test Case | Reason |
|-----|-----------|--------|
| U2U-010 | Simultaneous Bi-Directional Transfer | Requires true parallel execution with data isolation verification |
| U2U-011 | Retry on Dispatcher Failure | Requires transient failure injection at cross-client Dispatcher |
| U2U-012 | DLQ After Retries Exhausted | Requires permanent failure injection + DLQ verification |
| TC-001 | UCRM Test Client Installation | Manual installation and environment setup process |
