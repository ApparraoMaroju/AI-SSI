# Project Context: UCRI 2.0 P2P Integration (IPL-Adapter-UCRM)

## Application
- **Name:** UCRI 2.0 P2P Adapter Integration Service
- **Type:** API / Integration Service
- **Domain:** Emergency Services / Universal Control Room Interface

## Tech Stack
- **Frontend:** Not applicable (backend service only)
- **Backend:** [NEEDS CLARIFICATION] - Not specified in requirements
- **Database:** [NEEDS CLARIFICATION] - Not specified in requirements
- **API Type:** 
  - REST (IPL-facing interface)
  - P2P Messaging Protocol (UCRM-facing interface via messaging/send)
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
| IPL (Integration Platform Layer) | Source/target system for event dispatch and mission processing |
| Adapter | Integration component mediating between IPL and UCRM |
| UCRM (Universal Control Room Messaging) | Universal messaging system for control room operations |
| UCRM Test Client | Test utility for UCRM integration validation |

### Communication Flows

#### Forward Flow: IPL → Adapter → UCRM
1. IPL sends business/tenant payload to Adapter
2. Adapter validates incoming request
3. Adapter authenticates to UCRM via P2P token
4. Adapter forwards message to UCRM via messaging/send
5. UCRM processes and returns Accept/Reject response
6. Adapter propagates UCRM outcome back to IPL

#### Reverse Flow: UCRM → Adapter → IPL
1. UCRM sends mission to Adapter via messaging/send
2. Adapter translates and forwards to IPL
3. IPL processes mission from UCRM
4. IPL sends ACK (Accept/Reject) back to Adapter
5. Adapter propagates ACK to UCRM

## Key Operations

### Adapter Operations
| Operation | Direction | Description |
|-----------|-----------|-------------|
| Receive Tenant Payload | IPL → Adapter | Receive business payload from IPL |
| Validate Request | Adapter | Validate incoming request at Adapter |
| P2P Authentication | Adapter → UCRM | Authenticate Adapter to UCRM via P2P token |
| Forward Message | Adapter → UCRM | Forward message via messaging/send endpoint |
| Handle Response | UCRM → Adapter | Handle UCRM Accept/Reject response |
| Propagate Outcome | Adapter → IPL | Return UCRM outcome to IPL |
| Reverse Flow | UCRM → Adapter → IPL | Support mission flow from UCRM to IPL |

### IPL Operations
| Operation | Direction | Description |
|-----------|-----------|-------------|
| Send Event | IPL → Adapter | IPL sends event to Adapter |
| Handle Validation | Adapter → IPL | IPL handles validation response from Adapter |
| Process Accept ACK | Adapter → IPL | IPL processes Accept acknowledgment |
| Process Reject ACK | Adapter → IPL | IPL processes Reject acknowledgment |
| Process Mission | Adapter → IPL | IPL processes mission from UCRM (reverse flow) |
| Send ACK | IPL → Adapter | IPL sends Accept/Reject for mission |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| messaging/send | POST | [ASSUMPTION] Forward message to UCRM |
| [NEEDS CLARIFICATION] | POST | IPL event submission endpoint |
| [NEEDS CLARIFICATION] | POST | IPL ACK/feedback endpoint |

## Key Constraints

### Technical Constraints
- P2P token-based authentication required for UCRM communication
- Bi-directional communication flow support required
- Logging, monitoring, and traceability required for all P2P flows

### Integration Constraints
- UCRM Test Client prerequisites must be confirmed before usage
- Installation package and deployment guide required for Test Client setup
- Adapter must handle both Accept and Reject responses from UCRM

### Deployment Requirements
| Component | Requirement | Notes |
|-----------|-------------|-------|
| UCRM Test Client | Installation required | Per deployment guide (User Story 10) |
| Prerequisites | Must be confirmed | Per User Story 9 |
| Network | P2P connectivity | To UCRM messaging endpoint |

## Data Mapping Overview
- **IPL to UCRM:** Field mapping specifications available in IPL-Mapping document
- **UCRM to IPL:** Reverse mapping for mission data and acknowledgments
- **Detailed mapping:** [NEEDS CLARIFICATION] - Refer to "IPL-Mapping (UCRI)" document for specifics

## Observability

### Logging & Monitoring
- Comprehensive logging for all P2P flows (per User Story 8)
- Traceability support for request/response tracking
- Monitoring capabilities for integration health

## Known Limitations
- Specific technical stack details not specified in available documentation
- Environment URLs not specified in requirements
- Detailed API specifications require document content extraction
