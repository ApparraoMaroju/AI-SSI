# Testing Context: ADR-001 Messaging Abstraction Architecture

## Scope

### In Scope
- **Messaging Port Abstractions:** EventPublisherPort, EventSubscriberPort, EventReceiverPort
- **Message Envelope and Metadata Model:** Envelope structure, serialization, traceability
- **Adapter Delegation Layer:** Single adapter per port delegating to active transport
- **In-Memory Transport:** Vert.x EventBus implementation for standalone mode
- **Kafka Transport:** Kafka implementation for distributed mode
- **Receiver Module:** Event ingestion and validation
- **Handler Module:** Business logic processing and transformation
- **Dispatcher Module:** Event routing and publishing to dispatch centers
- **Configuration-Driven Transport Switching:** adapter.transport property
- **Module Enable/Disable via Configuration:** Receiver, Handler, Dispatcher toggles
- **Cross-Cutting Concerns:** Logging, retry, metrics via port decorators
- **Architecture Guardrails:** Automated boundary enforcement
- **End-to-End Message Flow:** Receiver → Handler → Dispatcher validation
- **Dispatch Center Communication:** IPL, WDX, UCRI, POLICE event routing

### Out of Scope
- UI testing (Not applicable - backend service only)
- Database-related testing (No persistence in prototype)
- Patient data processing (Excluded from prototype)
- Event schema governance or contract versioning
- Kafka infrastructure provisioning or operations
- Performance benchmarking [NEEDS CLARIFICATION]

## Test Data

### Transport Configuration
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Transport config | adapter.transport=in-memory | Validate in-memory mode |
| Transport config | adapter.transport=kafka | Validate Kafka mode |
| Invalid transport | adapter.transport=invalid | Validate error handling |
| Missing transport | (property absent) | Validate startup failure |

### Module Configuration
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Module config | adapter.receiver.enabled=true | Validate Receiver active |
| Module config | adapter.receiver.enabled=false | Validate Receiver disabled |
| Module config | adapter.handler.enabled=true | Validate Handler active |
| Module config | adapter.handler.enabled=false | Validate Handler disabled |
| Module config | adapter.dispatcher.enabled=true | Validate Dispatcher active |
| Module config | adapter.dispatcher.enabled=false | Validate Dispatcher disabled |

### Message Envelope Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid event message | Well-formed envelope with payload and metadata | Happy path processing |
| Invalid event message | Malformed or incomplete envelope | Validation failure in Receiver |
| Correlation ID | Unique identifier value | Traceability and observability |
| Headers | Key-value metadata pairs | Metadata propagation validation |
| Partition Key | Logical entity identifier | Ordering validation |

### Dispatch Center Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| IPL topic | events-ipl | IPL routing validation |
| WDX topic | events-wdx | WDX routing validation |
| UCRI topic | events-ucri | UCRI routing validation |
| POLICE topic | events-police | POLICE routing validation |
| DLQ topic | events-{center}-dlq | Dead letter queue validation |
| Valid sourceMandant | IPL_CENTER_001 | Sender client ID mapping |
| Valid targetMandant | WDX_CENTER_001 | Receiver client ID mapping |

## Test Environment

- **Tool:** Postman (primary), JUnit (unit tests), Integration test framework
- **Kafka:** Required for Kafka transport tests (broker must be running)
- **In-Memory:** No external dependency required
- **OS:** Linux (recommended), Windows compatible
- **Java Version:** Java 17+ (OpenJDK recommended)

## Dependencies

### Required for In-Memory Mode
- Adapter Integration Service deployed and started
- Configuration properties correctly set
- No external infrastructure required

### Required for Kafka Mode
- Kafka broker must be running and accessible
- Topics pre-created or auto-creation enabled
- Consumer groups configured

### Required for All Tests
- Architecture validation tool/framework integrated
- Test framework capable of running same tests across both transports
- Logging enabled for message conversion validation

## Test Scenarios

### Scenario 1: Transport Abstraction - In-Memory Mode
1. Configure adapter.transport=in-memory
2. Start Adapter Service
3. Verify startup logs indicate in-memory transport active
4. Publish event via EventPublisherPort
5. Verify event delivered to subscriber within same process
6. Confirm ordering preserved based on partition key

### Scenario 2: Transport Abstraction - Kafka Mode
1. Configure adapter.transport=kafka
2. Start Adapter Service with Kafka broker available
3. Verify startup logs indicate Kafka transport active
4. Publish event via EventPublisherPort
5. Verify event present on expected Kafka topic
6. Confirm partition ordering preserved

### Scenario 3: End-to-End Flow - Receiver → Handler → Dispatcher
1. Send event to Receiver
2. Verify Receiver validates and forwards to Handler
3. Verify Handler processes and publishes to Dispatcher
4. Verify Dispatcher routes to correct dispatch center topic
5. Confirm envelope metadata preserved end-to-end

### Scenario 4: Dispatch Center Routing - IPL to WDX
1. Configure IPL and WDX dispatch centers enabled
2. Send CreateRequest event with targetMandant=WDX
3. Verify event routed to events-wdx topic
4. Confirm field mappings executed correctly

### Scenario 5: Dispatch Center Routing - IPL to UCRI
1. Configure IPL and UCRI dispatch centers enabled
2. Send CreateRequest event with targetMandant=UCRI
3. Verify event routed to events-ucri topic

### Scenario 6: Dispatch Center Routing - IPL to POLICE
1. Configure IPL and POLICE dispatch centers enabled
2. Send CreateRequest event with targetMandant=POLICE
3. Verify event routed to events-police topic

### Scenario 7: Multi-Dispatch Center Routing
1. Configure all dispatch centers enabled (IPL, WDX, UCRI, POLICE)
2. Send event requiring multiple destinations
3. Verify Dispatcher sends to all target topics
4. Confirm independent processing per center

### Scenario 8: Module Enable/Disable
1. Disable Receiver module via configuration
2. Verify no subscriptions created, no resources consumed
3. Enable Receiver, disable Handler
4. Verify Receiver active but events not processed
5. Enable all modules, verify full flow works

### Scenario 9: Architecture Guardrails
1. Attempt to add infrastructure import to domain module
2. Run build
3. Verify build fails with architecture violation error
4. Remove violation, verify build succeeds

### Scenario 10: Cross-Cutting Concerns - Retry
1. Configure retry decorator (3 attempts, 1000ms delay)
2. Simulate transient publish failure
3. Verify retry occurs per configuration
4. Verify metrics reflect retry attempts

### Scenario 11: Cross-Cutting Concerns - DLQ
1. Configure DLQ for dispatch center
2. Send event that fails after all retries
3. Verify event sent to DLQ topic
4. Confirm DLQ contains failed event with error context

### Scenario 12: Invalid Configuration Handling
1. Configure adapter.transport=invalid_value
2. Start service
3. Verify startup fails with descriptive error listing valid options

### Scenario 13: Feedback Events - WDX to IPL
1. Trigger AcceptOperation event from WDX
2. Verify Adapter receives via streaming
3. Verify translation to IPL format
4. Verify IPL receives acceptance event

### Scenario 14: Transport Interchangeability
1. Run same test scenarios against in-memory transport
2. Run same test scenarios against Kafka transport
3. Compare results
4. Document any behavioral differences with root cause

## Validation Methods

### Log-Based Verification
- Adapter Service logs for message conversions
- Transport selection confirmation in startup logs
- Event receipt and dispatch logging
- Retry attempt logging
- DLQ event logging

### Metric-Based Verification
- Publish count per dispatch center
- Receive count per channel
- Failure count per dispatch center
- Latency metrics

### Architectural Verification
- Build failure on architecture violation
- Dependency analysis output

## Acceptance Criteria Checklist

### Port Abstractions
- [ ] EventPublisherPort defined in domain module
- [ ] EventSubscriberPort defined in domain module
- [ ] EventReceiverPort defined in domain module
- [ ] No infrastructure dependencies in port interfaces

### Transport Implementations
- [ ] In-memory transport works correctly
- [ ] Kafka transport works correctly
- [ ] Transport switching via configuration works
- [ ] Only one transport active at runtime

### Module Configuration
- [ ] Receiver can be enabled/disabled
- [ ] Handler can be enabled/disabled
- [ ] Dispatcher can be enabled/disabled
- [ ] Disabled modules consume no resources

### Dispatch Center Communication
- [ ] IPL to WDX routing works
- [ ] IPL to UCRI routing works
- [ ] IPL to POLICE routing works
- [ ] WDX to IPL feedback works
- [ ] Multi-destination routing works

### End-to-End Flow
- [ ] Receiver → Handler → Dispatcher flow works (in-memory)
- [ ] Receiver → Handler → Dispatcher flow works (Kafka)
- [ ] Same tests pass on both transports
- [ ] Envelope metadata preserved end-to-end
- [ ] Ordering preserved based on partition key

### Cross-Cutting Concerns
- [ ] Logging decorator works
- [ ] Retry decorator works with configuration
- [ ] Metrics decorator exposes correct values
- [ ] DLQ handling works

### Architecture Guardrails
- [ ] Build fails on domain → infrastructure dependency
- [ ] Build fails on port → implementation dependency
- [ ] Build fails on Handler → Kafka dependency

## Known Issues / Limitations

- Mock IPL service only; real IPL integration deferred
- No data persistence or caching in prototype
- Testing performed in controlled environments only
- Patient data inside mission dispatch not processed
- No automatic error recovery in prototype
- Single streaming filter configuration (enum = NEW)

## Test Deliverables Checklist

- [ ] Port abstraction unit tests (3 ports)
- [ ] In-memory transport integration tests
- [ ] Kafka transport integration tests
- [ ] Transport switching functional tests
- [ ] Module enable/disable tests
- [ ] Receiver module tests
- [ ] Handler module tests
- [ ] Dispatcher module tests
- [ ] IPL ↔ WDX communication tests
- [ ] IPL ↔ UCRI communication tests
- [ ] IPL ↔ POLICE communication tests
- [ ] Multi-dispatch center routing tests
- [ ] Architecture guardrail validation tests
- [ ] Cross-cutting concerns tests (logging, retry, metrics)
- [ ] DLQ handling tests
- [ ] End-to-end flow tests (both transports)
- [ ] Transport interchangeability comparison report
