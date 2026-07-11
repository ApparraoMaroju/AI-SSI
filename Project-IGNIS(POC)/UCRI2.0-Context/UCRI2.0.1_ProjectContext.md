# Project Context: UCRI 2.0 P2P Integration (IPL-Adapter-UCRM) — Revised

## Application
- **Name:** UCRI 2.0 P2P Adapter Integration Service
- **Type:** API / Integration Service
- **Domain:** Emergency Services / Universal Control Room Interface / Incident Dispatch

## Tech Stack
- **Frontend:** Not applicable (backend service only)
- **Backend:** Java 17+, Quarkus Framework
- **Database:** Not specified (prototype excludes persistence)
- **API Type:**
  - REST (IPL-facing interface)
  - P2P Messaging Protocol (UCRM-facing interface via messaging/send)
- **Messaging:** Vert.x EventBus (in-memory standalone mode) / Kafka (distributed mode)
- **Architecture:** Hexagonal Architecture (Ports and Adapters)
- **Authentication:** P2P Token-based authentication for UCRM

## Environment
- **Dev URL:** Not specified in requirements
- **Staging URL:** Not specified in requirements
- **Prod URL:** Not specified in requirements
- **Test Client:** UCRM Test Client (installation and deployment guide available)

## System Architecture

### Components
| Component | Description |
|-----------|-------------|
| IPL (Integration Platform Layer) | Source/target system for event/mission dispatch |
| Adapter (Receiver + Handler + Dispatcher) | Integration service mediating between IPL and UCRM, composed of three sub-services |
| UCRM (Universal Control Room Messaging) | Universal messaging system for control room operations |
| UCRM Test Client | Test utility for UCRM integration validation |

### Adapter Internal Architecture (3-Service Model)
The Adapter is composed of three internal services operating together:

| Service | Role | Description |
|---------|------|-------------|
| **Receiver** | Event Ingress | Consumes events via messaging ports, validates inbound events, feeds into domain processing |
| **Handler** | Business Logic | Processes events, transforms/translates between IPL and UCRM formats, orchestration logic |
| **Dispatcher** | Event Egress | Determines outbound routing, publishes events to target dispatch centers via messaging ports |

### Deployment Modes
| Mode | Description |
|------|-------------|
| Domain Modular (Standalone) | Single deployable service; Receiver, Handler, Dispatcher communicate via in-memory event bus (Vert.x) |
| Distributed (Kafka-Based) | Three independent services communicating via Kafka topics |

### Port Abstractions (Hexagonal Architecture)
| Port | Purpose |
|------|---------|
| EventPublisherPort | Publishing events outbound (used by Dispatcher) |
| EventSubscriberPort | Subscribing to and unsubscribing from event channels |
| EventReceiverPort | Receiving and processing inbound events (used by Receiver) |

### Dispatch Centers
| Center | Topic | Description |
|--------|-------|-------------|
| IPL | events-ipl | Source system for incident dispatch |
| UCRI | events-ucri | Emergency services dispatch center (UCRM) |
| WDX | events-wdx | Operational hub for incident distribution |
| POLICE | events-police | Law enforcement dispatch center |

### Communication Flows

#### Forward Flow: IPL → Adapter (Receiver → Handler → Dispatcher) → UCRM
1. IPL sends business/tenant payload via `/einsatztransfer/erzeugeEinsatz` (POST)
2. **Receiver** accepts and validates incoming request
3. **Handler** transforms IPL format to UCRM-compliant message, authenticates via P2P token
4. **Dispatcher** forwards message to UCRM via messaging/send endpoint
5. UCRM processes and returns Accept/Reject/Timeout response
6. **Receiver** receives UCRM response
7. **Handler** translates response to IPL ACK format
8. **Dispatcher** propagates outcome back to IPL via `/einsatztransfer/quittiereTranferEinsatz` (POST)

#### Reverse Flow: UCRM → Adapter (Receiver → Handler → Dispatcher) → IPL
1. UCRM sends mission to Adapter via messaging/send
2. **Receiver** accepts mission payload
3. **Handler** translates UCRM mission to IPL format
4. **Dispatcher** forwards mission to IPL
5. IPL processes mission and sends ACK (Accept/Reject) back
6. **Receiver** receives IPL ACK
7. **Handler** translates ACK to UCRM format
8. **Dispatcher** propagates ACK to UCRM

## IPL Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /einsatztransfer/erzeugeEinsatz | POST | Mission/event payload submission from IPL to Adapter |
| /einsatztransfer/quittiereTranferEinsatz | POST | Receive Accept/Reject/Timeout feedback from Adapter to IPL |
| messaging/send | POST | Forward message from Adapter to UCRM (P2P) |

## ACK Response Types and Log Verification

### ACK Outcomes via `/einsatztransfer/quittiereTranferEinsatz`
| ACK Status | Log Value | Description |
|------------|-----------|-------------|
| **Accepted** | `EMPFANG` | UCRM accepted the event/mission — log entry on `Einsatztransfer/quittiereTranferEinsatz` shows `EMPFANG` |
| **Rejected** | `EINSATZ_ABGELEHNT` | UCRM rejected the event/mission — log entry on `Einsatztransfer/quittiereTranferEinsatz` shows `EINSATZ_ABGELEHNT` |
| **Timeout** | `TECHNISCHER_FEHLER` | UCRM did not respond within allowed time — log entry on `Einsatztransfer/quittiereTranferEinsatz` shows `TECHNISCHER_FEHLER` |

## Key Operations

### Adapter Operations (Receiver + Handler + Dispatcher)
| Operation | Service | Direction | Description |
|-----------|---------|-----------|-------------|
| Receive Tenant Payload | Receiver | IPL → Adapter | Accept and validate business payload |
| Validate Request | Receiver | Adapter | Validate incoming request format and data |
| Transform Message | Handler | Adapter | Translate between IPL and UCRM formats |
| P2P Authentication | Handler | Adapter → UCRM | Authenticate to UCRM via P2P token |
| Forward Message | Dispatcher | Adapter → UCRM | Forward message via messaging/send |
| Handle Response | Receiver | UCRM → Adapter | Handle UCRM Accept/Reject/Timeout response |
| Propagate Outcome | Dispatcher | Adapter → IPL | Return outcome to IPL via quittiereTranferEinsatz |
| Reverse Flow | All | UCRM → Adapter → IPL | Support mission flow from UCRM to IPL |

### IPL Operations
| Operation | Direction | Description |
|-----------|-----------|-------------|
| Send Event | IPL → Adapter | IPL sends event via /einsatztransfer/erzeugeEinsatz |
| Handle Validation | Adapter → IPL | IPL handles validation response from Adapter |
| Process Accept ACK | Adapter → IPL | IPL processes EMPFANG acknowledgment |
| Process Reject ACK | Adapter → IPL | IPL processes EINSATZ_ABGELEHNT acknowledgment |
| Process Timeout | Adapter → IPL | IPL processes TECHNISCHER_FEHLER (timeout) |
| Process Mission | Adapter → IPL | IPL processes mission from UCRM (reverse flow) |
| Send ACK | IPL → Adapter | IPL sends Accept/Reject for mission |

## Configuration Properties

### Transport Configuration
| Property | Description | Default |
|----------|-------------|---------|
| adapter.transport | Transport mode selection | in-memory / kafka |
| adapter.receiver.enabled | Enable/disable Receiver service | true |
| adapter.handler.enabled | Enable/disable Handler service | true |
| adapter.dispatcher.enabled | Enable/disable Dispatcher service | true |

### Dispatch Center Configuration
| Property | Description | Default |
|----------|-------------|---------|
| dispatch-center.ucri.enabled | Enable/disable UCRI dispatch center | true |
| dispatch-center.ucri.topic | UCRI event topic | events-ucri |
| dispatch-center.ucri.url | UCRM connection URL | [NEEDS CLARIFICATION] |
| dispatch-center.ucri.timeout-ms | Connection timeout | 5000 |
| dispatch-center.ucri.retry-attempts | Retry attempts on failure | 3 |
| dispatch-center.ucri.retry-delay-ms | Delay between retries | 1000 |
| dispatch-center.ucri.dlq-topic | Dead Letter Queue topic | events-ucri-dlq |

## Data Mapping Overview

### IPL → UCRM Field Mapping (via Adapter Handler)
| IPL Field | UCRM Field | Mapping Logic |
|-----------|------------|---------------|
| sourceMandant | header.sender_client_id | 1:1 Mapping |
| targetMandant | header.receiver_client_id | 1:1 Mapping |
| transferEinsatz.einsatzId | operation.id | 1:1 Mapping |
| transferEinsatz.einsatznummerKurz | operation.name | 1:1 Mapping |
| transferEinsatz.kategorie | operation.occassion.type_1 | 1:1 Mapping |
| transferEinsatz.einsatzStichwort | operation.occassion.keyword_1 | 1:1 Mapping |
| transferEinsatz.alarmierungsstichwortText | operation.occassion.keyword_1_text | 1:1 Mapping |

### ACK Mapping (UCRM → IPL via Adapter Handler)
| UCRM Response | IPL Log Value (quittiereTranferEinsatz) | Meaning |
|---------------|----------------------------------------|---------|
| Accept | EMPFANG | Mission/event accepted |
| Reject | EINSATZ_ABGELEHNT | Mission/event rejected |
| No Response (Timeout) | TECHNISCHER_FEHLER | Technical error / timeout |

## Key Constraints

### Architectural Constraints
- Adapter follows Hexagonal Architecture (Ports and Adapters)
- Messaging must be transport-agnostic (Kafka or in-memory switch via configuration)
- Domain logic (Handler) must remain independent of infrastructure
- Cross-cutting concerns (logging, retry, metrics) implemented via decorators
- Configuration-driven behavior only (no recompilation for transport switching)

### Technical Constraints
- P2P token-based authentication required for UCRM communication
- Bi-directional communication flow support required
- Every event must be acknowledged within **10 seconds** (timeout → TECHNISCHER_FEHLER)
- Event ordering preserved based on partition key
- Logging, monitoring, and traceability required for all P2P flows

### Integration Constraints
- UCRM Test Client prerequisites must be confirmed before usage
- Adapter must handle Accept, Reject, and Timeout responses from UCRM
- Three distinct ACK statuses must be logged correctly: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER

### Prototype Constraints
- No database or cache layer (no persistence)
- Mock IPL service used instead of real IPL system
- No retry mechanisms, fallback routing, or automatic error recovery (prototype)
- Patient data within mission dispatch messages is not processed

## Observability

### Logging & Monitoring
- Comprehensive logging for all P2P flows (Receiver, Handler, Dispatcher)
- ACK outcomes logged via `Einsatztransfer/quittiereTranferEinsatz` with status values: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER
- Traceability support via correlationId for request/response tracking
- Cross-cutting metrics via decorators: publish/receive/failure counts and latency

### Log Verification Points
| Log Entry | Contains | Scenario |
|-----------|----------|----------|
| Einsatztransfer/quittiereTranferEinsatz | EMPFANG | Accepted case |
| Einsatztransfer/quittiereTranferEinsatz | EINSATZ_ABGELEHNT | Rejected case |
| Einsatztransfer/quittiereTranferEinsatz | TECHNISCHER_FEHLER | Timeout case |

## Known Limitations
- Specific UCRM API endpoint details not fully specified in available documentation
- Environment URLs not specified in requirements
- Patient data processing excluded from prototype
- No automatic error recovery in prototype
