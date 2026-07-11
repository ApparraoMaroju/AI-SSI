# Feature Context: UCRI-P2P — End-to-End IPL ↔ Adapter ↔ UCRM

## Overview
UCRI-P2P (Universal Control Room Interface - Peer-to-Peer) is an end-to-end integration feature enabling bi-directional communication between IPL (Integration Platform Layer), an Adapter component, and UCRM (Universal Control Room Messaging). This feature provides a P2P messaging flow for mission dispatch, event handling, and acknowledgment processing within emergency services/control room operations.

## User Stories

### Adapter User Stories

#### US-A1: Receive Business (Tenant Payload) from IPL
- As an **Adapter**, I want to **receive business/tenant payload from IPL** so that **I can initiate the message forwarding process to UCRM**

#### US-A2: Validate Incoming Request at Adapter
- As an **Adapter**, I want to **validate incoming requests** so that **only properly formatted and authorized requests are processed**

#### US-A3: Authenticate Adapter to UCRM via P2P Token
- As an **Adapter**, I want to **authenticate to UCRM using P2P token** so that **secure communication is established with UCRM**

#### US-A4: Forward Message from Adapter to UCRM via messaging/send
- As an **Adapter**, I want to **forward messages to UCRM via messaging/send endpoint** so that **IPL events are delivered to UCRM**

#### US-A5: Handle UCRM Acceptance/Rejection Response at Adapter
- As an **Adapter**, I want to **handle Accept/Reject responses from UCRM** so that **the outcome can be communicated back to IPL**

#### US-A6: Propagate UCRM Outcome Back to IPL
- As an **Adapter**, I want to **propagate UCRM outcomes back to IPL** so that **IPL receives confirmation of message processing**

#### US-A7: Support Reverse Flow UCRM → IPL via messaging/send
- As an **Adapter**, I want to **support reverse flow from UCRM to IPL** so that **missions originating from UCRM can reach IPL**

#### US-A8: Logging, Monitoring, and Traceability for P2P Flows
- As an **Operations Team**, I want to **have comprehensive logging, monitoring, and traceability** so that **all P2P flows can be tracked and debugged**

#### US-A9: Confirm Scope and Prerequisites for UCRM Test Client Usage
- As a **Tester/Developer**, I want to **confirm scope and prerequisites for UCRM Test Client** so that **I can properly set up the test environment**

#### US-A10: Installation Package and Deployment Guide for UCRM Test Client
- As a **Tester/Developer**, I want to **have installation package and deployment guide** so that **I can deploy and configure the UCRM Test Client**

### IPL User Stories

#### US-I1: IPL Sends Event to Adapter
- As **IPL**, I want to **send events to the Adapter** so that **events can be forwarded to UCRM**

#### US-I2: IPL Handles Validation Response from Adapter
- As **IPL**, I want to **handle validation responses from Adapter** so that **I know if my request was properly formatted**

#### US-I3: IPL Processes "Accept" ACK from Adapter (UCRM Accepted)
- As **IPL**, I want to **process Accept acknowledgments from Adapter** so that **I know UCRM accepted my event**

#### US-I4: IPL Processes "Reject" ACK from Adapter (UCRM Rejected)
- As **IPL**, I want to **process Reject acknowledgments from Adapter** so that **I know UCRM rejected my event and can take appropriate action**

#### US-I5: IPL Processes Mission from UCRM via Adapter (Reverse Flow)
- As **IPL**, I want to **process missions received from UCRM via Adapter** so that **missions can be handled in the IPL system**

#### US-I6: IPL Sends ACK (Accept/Reject) for Mission to Adapter
- As **IPL**, I want to **send Accept/Reject acknowledgments for missions to Adapter** so that **UCRM receives confirmation of mission processing**

## Acceptance Criteria

### Adapter Acceptance Criteria
- [ ] Adapter successfully receives tenant payload from IPL
- [ ] Adapter validates all incoming requests before processing
- [ ] Adapter authenticates to UCRM using P2P token mechanism
- [ ] Adapter forwards messages to UCRM via messaging/send endpoint
- [ ] Adapter correctly handles both Accept and Reject responses from UCRM
- [ ] Adapter propagates UCRM outcomes back to IPL
- [ ] Adapter supports reverse flow (UCRM → IPL)
- [ ] All P2P flows are logged with full traceability
- [ ] Monitoring capabilities are operational
- [ ] UCRM Test Client installation and deployment documented

### IPL Acceptance Criteria
- [ ] IPL successfully sends events to Adapter
- [ ] IPL handles validation responses from Adapter
- [ ] IPL correctly processes Accept ACK (UCRM Accepted)
- [ ] IPL correctly processes Reject ACK (UCRM Rejected)
- [ ] IPL processes missions from UCRM via Adapter (reverse flow)
- [ ] IPL sends Accept/Reject ACK for missions back to Adapter

## API Endpoints (if applicable)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | messaging/send | [ASSUMPTION] Forward message from Adapter to UCRM |
| POST | [NEEDS CLARIFICATION] | IPL event submission endpoint |
| POST | [NEEDS CLARIFICATION] | IPL ACK response endpoint |
| POST | [NEEDS CLARIFICATION] | Adapter to IPL callback endpoint |

## UI Elements
- Not applicable - Backend integration service only

## Validation Rules

| Field | Rule |
|-------|------|
| Tenant Payload | Must be valid business payload format |
| P2P Token | Valid authentication token required |
| Request Format | Must pass Adapter validation rules |
| ACK Type | Must be "Accept" or "Reject" |
| Message Format | [NEEDS CLARIFICATION] - Per UCRI specification |

## Error Messages

| Code | Message |
|------|---------|
| [NEEDS CLARIFICATION] | Validation failed - invalid request format |
| [NEEDS CLARIFICATION] | Authentication failed - invalid P2P token |
| [NEEDS CLARIFICATION] | UCRM rejection - message not accepted |
| [NEEDS CLARIFICATION] | Timeout - UCRM did not respond |
| [NEEDS CLARIFICATION] | Forward failed - messaging/send error |

## Flow Diagrams
- **IPL to UCRI Flow:** Documented in "IPL to UCRI.png"
- **UCRI to IPL Flow:** Documented in "UCRI to IPL.png"
- **P2P Flow Diagram:** Documented in "UCRI 2.0- P2P (Peer-to-Peer) FlowDiagram"

## Data Mapping
- **Mapping Specification:** Documented in "IPL-Mapping (UCRI)" document
- **Complete Specification:** Documented in "complete_spec en-US 1.pdf"
- **UCRI Outline:** Documented in "UCRI-Universal-Control-Room-Interface-Outline-V2.0"

## Dependencies
- IPL system must be operational
- UCRM must be accessible via P2P connection
- P2P token authentication mechanism must be configured
- Network connectivity between all three components required
