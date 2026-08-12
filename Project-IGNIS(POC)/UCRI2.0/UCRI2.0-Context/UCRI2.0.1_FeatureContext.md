# Feature Context: UCRI-P2P — End-to-End IPL ↔ Adapter (Receiver-Handler-Dispatcher) ↔ UCRM — Revised

## Overview
UCRI-P2P (Universal Control Room Interface - Peer-to-Peer) is an end-to-end integration feature enabling bi-directional communication between IPL (Integration Platform Layer) and UCRM (Universal Control Room Messaging) via the Adapter. The Adapter is composed of three internal services — **Receiver**, **Handler**, and **Dispatcher** — following Hexagonal Architecture principles. The system supports mission dispatch, event handling, acknowledgment processing (Accept/Reject/Timeout), and transport-agnostic messaging (in-memory or Kafka) for emergency services/control room operations.

## User Stories

### Adapter User Stories (Receiver + Handler + Dispatcher)

#### US-A1: Receive Business (Tenant Payload) from IPL
- As the **Adapter (Receiver)**, I want to **receive business/tenant payload from IPL via `/einsatztransfer/erzeugeEinsatz`** so that **I can initiate the message forwarding process to UCRM**

#### US-A2: Validate Incoming Request at Adapter
- As the **Adapter (Receiver)**, I want to **validate incoming requests** so that **only properly formatted and authorized requests are processed by the Handler**

#### US-A3: Authenticate Adapter to UCRM via P2P Token
- As the **Adapter (Handler)**, I want to **authenticate to UCRM using P2P token** so that **secure communication is established with UCRM**

#### US-A4: Forward Message from Adapter to UCRM via messaging/send
- As the **Adapter (Dispatcher)**, I want to **forward messages to UCRM via messaging/send endpoint** so that **IPL events are delivered to UCRM**

#### US-A5: Handle UCRM Acceptance/Rejection/Timeout Response at Adapter
- As the **Adapter (Receiver + Handler)**, I want to **handle Accept, Reject, and Timeout responses from UCRM** so that **the outcome can be communicated back to IPL with correct ACK status**:
  - **Accept** → log `EMPFANG` via `Einsatztransfer/quittiereTranferEinsatz`
  - **Reject** → log `EINSATZ_ABGELEHNT` via `Einsatztransfer/quittiereTranferEinsatz`
  - **Timeout** → log `TECHNISCHER_FEHLER` via `Einsatztransfer/quittiereTranferEinsatz`

#### US-A6: Propagate UCRM Outcome Back to IPL
- As the **Adapter (Dispatcher)**, I want to **propagate UCRM outcomes back to IPL via `/einsatztransfer/quittiereTranferEinsatz`** so that **IPL receives confirmation of message processing with the correct status (EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER)**

#### US-A7: Support Reverse Flow UCRM → IPL via messaging/send
- As the **Adapter (Receiver → Handler → Dispatcher)**, I want to **support reverse flow from UCRM to IPL** so that **missions originating from UCRM can reach IPL**

#### US-A8: Logging, Monitoring, and Traceability for P2P Flows
- As an **Operations Team**, I want to **have comprehensive logging, monitoring, and traceability across Receiver, Handler, and Dispatcher** so that **all P2P flows can be tracked and debugged**

#### US-A9: Confirm Scope and Prerequisites for UCRM Test Client Usage
- As a **Tester/Developer**, I want to **confirm scope and prerequisites for UCRM Test Client** so that **I can properly set up the test environment**

#### US-A10: Installation Package and Deployment Guide for UCRM Test Client
- As a **Tester/Developer**, I want to **have installation package and deployment guide** so that **I can deploy and configure the UCRM Test Client**

### IPL User Stories

#### US-I1: IPL Sends Event to Adapter
- As **IPL**, I want to **send events to the Adapter via `/einsatztransfer/erzeugeEinsatz`** so that **events can be forwarded to UCRM**

#### US-I2: IPL Handles Validation Response from Adapter
- As **IPL**, I want to **handle validation responses from Adapter** so that **I know if my request was properly formatted**

#### US-I3: IPL Processes "Accept" ACK from Adapter (UCRM Accepted — EMPFANG)
- As **IPL**, I want to **process Accept acknowledgments from Adapter** so that **I know UCRM accepted my event**
- **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `EMPFANG`

#### US-I4: IPL Processes "Reject" ACK from Adapter (UCRM Rejected — EINSATZ_ABGELEHNT)
- As **IPL**, I want to **process Reject acknowledgments from Adapter** so that **I know UCRM rejected my event and can take appropriate action**
- **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `EINSATZ_ABGELEHNT`

#### US-I5: IPL Processes Timeout from Adapter (TECHNISCHER_FEHLER)
- As **IPL**, I want to **process Timeout notifications from Adapter** so that **I know UCRM did not respond within the allowed time and can handle the technical error**
- **Log verification:** `Einsatztransfer/quittiereTranferEinsatz` contains `TECHNISCHER_FEHLER`

#### US-I6: IPL Processes Mission from UCRM via Adapter (Reverse Flow)
- As **IPL**, I want to **process missions received from UCRM via Adapter** so that **missions can be handled in the IPL system**

#### US-I7: IPL Sends ACK (Accept/Reject) for Mission to Adapter
- As **IPL**, I want to **send Accept/Reject acknowledgments for missions to Adapter** so that **UCRM receives confirmation of mission processing**

### Architecture & Transport User Stories

#### US-T1: In-Memory Transport Operation
- As a **developer**, I want **in-memory transport (Vert.x EventBus) for Receiver → Handler → Dispatcher communication** so that **the system operates without external infrastructure during development and testing**

#### US-T2: Configuration-Driven Transport Selection
- As an **operator**, I want to **select messaging transport via `adapter.transport=in-memory|kafka`** so that **deployment flexibility is maintained without code changes**

#### US-T3: Module Enable/Disable via Configuration
- As an **operator**, I want to **enable/disable Receiver, Handler, and Dispatcher individually via configuration** so that **flexible deployment scenarios are supported**

#### US-T4: End-to-End Message Flow Validation
- As a **developer**, I want **end-to-end message flow (Receiver → Handler → Dispatcher) validated** so that **the architecture operates correctly with in-memory transport**

## Acceptance Criteria

### Adapter Acceptance Criteria (Receiver + Handler + Dispatcher)
- [ ] Receiver successfully receives tenant payload from IPL via `/einsatztransfer/erzeugeEinsatz`
- [ ] Receiver validates all incoming requests before forwarding to Handler
- [ ] Handler authenticates to UCRM using P2P token mechanism
- [ ] Dispatcher forwards messages to UCRM via messaging/send endpoint
- [ ] Adapter correctly handles Accept response from UCRM → logs `EMPFANG`
- [ ] Adapter correctly handles Reject response from UCRM → logs `EINSATZ_ABGELEHNT`
- [ ] Adapter correctly handles Timeout (no UCRM response) → logs `TECHNISCHER_FEHLER`
- [ ] Dispatcher propagates outcomes to IPL via `/einsatztransfer/quittiereTranferEinsatz`
- [ ] Adapter supports reverse flow (UCRM → Receiver → Handler → Dispatcher → IPL)
- [ ] All P2P flows are logged with full traceability across all three services
- [ ] Monitoring capabilities are operational
- [ ] UCRM Test Client installation and deployment documented

### IPL Acceptance Criteria
- [ ] IPL successfully sends events to Adapter via `/einsatztransfer/erzeugeEinsatz`
- [ ] IPL handles validation responses from Adapter
- [ ] IPL correctly processes Accept ACK (log shows EMPFANG)
- [ ] IPL correctly processes Reject ACK (log shows EINSATZ_ABGELEHNT)
- [ ] IPL correctly processes Timeout (log shows TECHNISCHER_FEHLER)
- [ ] IPL processes missions from UCRM via Adapter (reverse flow)
- [ ] IPL sends Accept/Reject ACK for missions back to Adapter

### Transport & Architecture Acceptance Criteria
- [ ] In-memory transport works for Receiver → Handler → Dispatcher flow
- [ ] Transport selected via `adapter.transport=in-memory` configuration
- [ ] Receiver, Handler, Dispatcher can be individually enabled/disabled
- [ ] Envelope metadata (correlationId, headers) preserved end-to-end
- [ ] Event ordering preserved based on partition key
- [ ] Disabled modules not instantiated, consume no resources

## API Endpoints

| Method | Endpoint | Direction | Description |
|--------|----------|-----------|-------------|
| POST | /einsatztransfer/erzeugeEinsatz | IPL → Adapter (Receiver) | Mission/event payload submission from IPL |
| POST | /einsatztransfer/quittiereTranferEinsatz | Adapter (Dispatcher) → IPL | ACK feedback: EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER |
| POST | messaging/send | Adapter (Dispatcher) ↔ UCRM | Forward/receive messages to/from UCRM |

## UI Elements
- Not applicable — Backend integration service only

## Validation Rules

| Field | Rule |
|-------|------|
| Tenant Payload | Must be valid business payload format (TransferEinsatz structure) |
| P2P Token | Valid authentication token required, not expired |
| Request Format | Must pass Adapter (Receiver) validation rules |
| ACK Type | Must be one of: EMPFANG (Accept), EINSATZ_ABGELEHNT (Reject), TECHNISCHER_FEHLER (Timeout) |
| sourceMandant | Required — sender client identifier |
| targetMandant | Required — receiver client identifier |
| einsatzId | Required — operation identifier |
| adapter.transport | Must be "in-memory" or "kafka" |
| dispatch-center.ucri.enabled | Boolean (true/false) |
| dispatch-center.ucri.topic | Required when enabled=true |

## Error Messages / ACK Status Values

| ACK Status | Log Value (quittiereTranferEinsatz) | Scenario |
|------------|--------------------------------------|----------|
| Accepted | `EMPFANG` | UCRM accepted the event/mission |
| Rejected | `EINSATZ_ABGELEHNT` | UCRM rejected the event/mission |
| Timeout | `TECHNISCHER_FEHLER` | UCRM did not respond within allowed time |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| UCRM Accept | Adapter logs EMPFANG, propagates Accept to IPL |
| UCRM Reject | Adapter logs EINSATZ_ABGELEHNT, propagates Reject to IPL |
| UCRM Timeout (no response) | Adapter logs TECHNISCHER_FEHLER, propagates timeout error to IPL |
| Invalid request at Receiver | Rejected with clear reason logged, no forwarding to Handler |
| P2P authentication failure | Error propagated to IPL, logged with details |
| No transport configured | Startup fails with descriptive error |
| Invalid transport value | Startup fails listing valid options |
| Publish failure | Retry with configurable attempts, then DLQ |

## Flow Diagrams
- **IPL to UCRI Flow:** Documented in "IPL to UCRI.png" — shows IPL → Adapter (Receiver → Handler → Dispatcher) → UCRM with Accept/Reject/Timeout outcomes
- **UCRI to IPL Flow:** Documented in "UCRI to IPL.png" — shows UCRM → Adapter (Receiver → Handler → Dispatcher) → IPL with mission dispatch
- **P2P Flow Diagram:** Documented in "UCRI 2.0- P2P (Peer-to-Peer) FlowDiagram"

## Data Mapping

### IPL → UCRM Field Mapping (TransferEinsatz)
| IPL Field | UCRM Field | Mapping Logic |
|-----------|------------|---------------|
| sourceMandant | header.sender_client_id | 1:1 Mapping |
| targetMandant | header.receiver_client_id | 1:1 Mapping |
| transferEinsatz.einsatzId | operation.id | 1:1 Mapping |
| transferEinsatz.einsatznummerKurz | operation.name | 1:1 Mapping |
| transferEinsatz.kategorie | operation.occassion.type_1 | 1:1 Mapping |
| transferEinsatz.einsatzStichwort | operation.occassion.keyword_1 | 1:1 Mapping |
| transferEinsatz.alarmierungsstichwortText | operation.occassion.keyword_1_text | 1:1 Mapping |

### ACK Response Mapping (UCRM → IPL)
| UCRM Response | IPL ACK (quittiereTranferEinsatz) | Log Value |
|---------------|-----------------------------------|-----------|
| Accept | Accepted | EMPFANG |
| Reject | Rejected | EINSATZ_ABGELEHNT |
| No Response | Timeout | TECHNISCHER_FEHLER |

### Reference Documents
- **Mapping Specification:** "IPL-Mapping (UCRI)" document
- **Complete Specification:** "complete_spec en-US 1.pdf"
- **UCRI Outline:** "UCRI-Universal-Control-Room-Interface-Outline-V2.0"

## Cross-Cutting Concerns (Decorators)
| Concern | Description |
|---------|-------------|
| Logging | Logs publish/receive operations with context across Receiver, Handler, Dispatcher |
| Retry | Retries failed publish with configurable backoff (default: 3 attempts, 1000ms delay) |
| Metrics | Exposes publish/receive/failure counts and latency |

## Dependencies
- IPL system must be operational (or mock IPL running)
- UCRM must be accessible via P2P connection
- P2P token authentication mechanism must be configured
- Network connectivity between IPL, Adapter (all 3 services), and UCRM required
- For in-memory mode: no external infrastructure required
- For Kafka mode: Kafka broker must be running
- Logging infrastructure operational for ACK verification (EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER)
