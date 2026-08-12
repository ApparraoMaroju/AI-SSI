# Testing Context: UCRI 2.0 P2P Integration (IPL-Adapter-UCRM)

## Scope

### In Scope
- **Forward Flow Testing:** IPL → Adapter → UCRM end-to-end message flow
- **Reverse Flow Testing:** UCRM → Adapter → IPL mission dispatch flow
- **Adapter Validation:** Incoming request validation at Adapter
- **P2P Authentication:** Adapter to UCRM authentication via P2P token
- **Message Forwarding:** messaging/send endpoint functionality
- **Accept/Reject Handling:** UCRM response handling and propagation
- **ACK Processing:** IPL Accept/Reject acknowledgment handling
- **Bi-directional Communication:** Full round-trip message flow validation
- **Logging & Traceability:** P2P flow logging and monitoring verification
- **UCRM Test Client:** Test client installation and usage validation

### Out of Scope
- UI Testing (Not applicable - backend service only)
- Database Testing (Not specified in requirements)
- Performance Benchmarking (Not explicitly specified) [NEEDS CLARIFICATION]
- Load Testing (Not specified in requirements)
- Security Penetration Testing (Not specified in requirements)

## Test Data

| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid Tenant Payload | Business payload per specification | Forward flow happy path |
| Invalid Tenant Payload | Malformed payload | Adapter validation negative test |
| Valid P2P Token | Authorized authentication token | P2P authentication happy path |
| Invalid P2P Token | Expired/invalid token | Authentication failure test |
| Accept Response | UCRM Accept ACK | Positive acknowledgment flow |
| Reject Response | UCRM Reject ACK | Negative acknowledgment flow |
| Mission Payload | UCRM mission data | Reverse flow testing |
| IPL Accept ACK | Accept acknowledgment from IPL | Reverse flow ACK test |
| IPL Reject ACK | Reject acknowledgment from IPL | Reverse flow rejection test |
| Validation Error | Invalid request format | Validation failure scenario |
| Trace ID | Unique correlation identifier | Traceability verification |

## Test Environment

- **Tool:** Postman (primary test tool) [ASSUMPTION]
- **Test Client:** UCRM Test Client (per deployment guide)
- **Protocol:** P2P Messaging / REST
- **Authentication:** P2P Token-based
- **Browser:** Not applicable (API testing only)
- **Device:** Desktop
- **OS:** [NEEDS CLARIFICATION] - Per UCRM Test Client requirements

## Dependencies

### Required Services
- IPL system must be running (or mock IPL)
- UCRM must be accessible
- Adapter service must be deployed and started
- UCRM Test Client must be installed (per User Story 10)

### Prerequisites
- UCRM Test Client scope and prerequisites confirmed (per User Story 9)
- P2P authentication tokens must be provisioned
- Network connectivity between IPL, Adapter, and UCRM established
- Logging infrastructure operational

### Pre-Test Setup
- Follow UCRM Test Client deployment guide
- Verify all service connectivity
- Confirm P2P token validity
- Validate logging configuration

## Test Scenarios

### Forward Flow Tests (IPL → Adapter → UCRM)

#### Scenario 1: Happy Path - Event Sent and Accepted
1. IPL sends valid event to Adapter
2. Adapter validates request (passes)
3. Adapter authenticates to UCRM via P2P token
4. Adapter forwards message via messaging/send
5. UCRM accepts and returns Accept response
6. Adapter propagates Accept outcome to IPL
7. IPL receives and processes Accept ACK

#### Scenario 2: Happy Path - Event Sent and Rejected
1. IPL sends valid event to Adapter
2. Adapter validates request (passes)
3. Adapter authenticates and forwards to UCRM
4. UCRM rejects and returns Reject response
5. Adapter propagates Reject outcome to IPL
6. IPL receives and processes Reject ACK

#### Scenario 3: Validation Failure at Adapter
1. IPL sends invalid/malformed event to Adapter
2. Adapter validation fails
3. Adapter returns validation error to IPL
4. IPL handles validation response
5. No message forwarded to UCRM

#### Scenario 4: P2P Authentication Failure
1. IPL sends valid event to Adapter
2. Adapter validation passes
3. Adapter attempts P2P authentication with invalid token
4. Authentication fails
5. Error propagated back to IPL

### Reverse Flow Tests (UCRM → Adapter → IPL)

#### Scenario 5: Mission Received and Accepted
1. UCRM sends mission to Adapter via messaging/send
2. Adapter receives and translates mission
3. Adapter forwards mission to IPL
4. IPL processes mission successfully
5. IPL sends Accept ACK to Adapter
6. Adapter propagates Accept ACK to UCRM

#### Scenario 6: Mission Received and Rejected
1. UCRM sends mission to Adapter
2. Adapter forwards to IPL
3. IPL rejects mission
4. IPL sends Reject ACK to Adapter
5. Adapter propagates Reject ACK to UCRM

### Cross-Cutting Tests

#### Scenario 7: Logging and Traceability Validation
1. Execute forward flow test
2. Verify all steps logged with correlation/trace ID
3. Verify monitoring data captured
4. Confirm end-to-end traceability

#### Scenario 8: UCRM Test Client Validation
1. Install UCRM Test Client per deployment guide
2. Verify prerequisites are met
3. Execute basic connectivity test
4. Validate Test Client functionality

## Validation Methods

### Log-Based Verification
- All message flows logged at Adapter
- Request/response pairs traceable
- Correlation IDs maintained across flows
- Error conditions logged with details

### Response Verification
- Correct HTTP status codes returned
- Proper Accept/Reject response format
- Error messages match specification

## Acceptance Criteria

### Forward Flow
- [ ] IPL successfully sends event to Adapter
- [ ] Adapter validates incoming requests correctly
- [ ] P2P authentication succeeds with valid token
- [ ] Message forwarded to UCRM via messaging/send
- [ ] UCRM Accept response handled correctly
- [ ] UCRM Reject response handled correctly
- [ ] Outcome propagated back to IPL
- [ ] IPL correctly processes Accept/Reject ACK

### Reverse Flow
- [ ] UCRM mission received at Adapter
- [ ] Mission forwarded to IPL
- [ ] IPL processes mission correctly
- [ ] IPL Accept ACK sent and propagated to UCRM
- [ ] IPL Reject ACK sent and propagated to UCRM

### Cross-Cutting
- [ ] All P2P flows logged with traceability
- [ ] Monitoring operational
- [ ] UCRM Test Client installed and functional

## Known Issues

- Specific error codes and messages not specified in available documentation
- Detailed API specifications require document content extraction
- Test environment details not fully specified in requirements
- Performance and load testing requirements not specified [NEEDS CLARIFICATION]

## Test Deliverables Checklist

- [ ] Forward flow (IPL → Adapter → UCRM) tested end-to-end
- [ ] Reverse flow (UCRM → Adapter → IPL) tested end-to-end
- [ ] Adapter validation logic verified
- [ ] P2P authentication verified
- [ ] Accept/Reject handling verified (both directions)
- [ ] Logging and traceability verified
- [ ] UCRM Test Client deployment validated
- [ ] All 16 user stories covered with test scenarios
- [ ] Error handling scenarios validated
