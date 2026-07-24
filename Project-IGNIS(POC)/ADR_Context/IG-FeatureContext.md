# Feature Context: ADR-001 Messaging Abstraction Strategy

## Overview
Implementation of a transport-agnostic messaging architecture using Hexagonal Architecture principles for the Adapter Integration Service. This enables the system to switch messaging transport (Kafka or in-memory) via configuration without code changes, while maintaining strong isolation between domain logic and infrastructure.

## User Stories

### US-01: Define Messaging Port Abstractions
- As a developer, I want messaging port interfaces defined in the domain module so that domain and application logic remain independent of messaging infrastructure.

### US-02: Define Standard Message Envelope and Metadata Model
- As a developer, I want a standard message envelope with metadata and payload so that messaging remains consistent, traceable, and transport-agnostic.

### US-03: Implement Messaging Adapter Delegation Layer
- As a developer, I want a single messaging adapter per port that delegates to the active transport implementation so that domain code interacts with one consistent adapter regardless of which transport is running.

### US-04: Implement In-Memory Transport
- As a developer, I want an in-memory transport implementation so that the messaging adapter can operate without external infrastructure during development, testing, and single-process deployments.

### US-05: Implement Architecture Guardrails
- As an architect, I want architectural guardrails enforced automatically so that hexagonal architecture boundaries remain intact as the codebase evolves.

### US-06: Implement Receiver Module
- As a developer, I want a Receiver module that consumes events via messaging ports so that event ingress follows architectural boundaries and feeds events into domain processing.

### US-07: Implement Handler Module
- As a developer, I want a Handler module that processes events so that business logic remains independent of messaging infrastructure.

### US-08: Implement Dispatcher Module
- As a developer, I want a Dispatcher module that determines outbound routing and publishes events via messaging ports so that event egress remains transport-agnostic and supports flexible routing.

### US-09: Implement Kafka Transport
- As a developer, I want a Kafka transport implementation so that the messaging adapter can operate in distributed environments with durable event delivery.

### US-10: Enable Configuration-Driven Transport Selection
- As an operator, I want to select messaging transport via configuration so that deployment flexibility is maintained without code changes or recompilation.

### US-11: Support Module Enable/Disable via Configuration
- As an operator, I want functional modules to be enabled or disabled via configuration so that flexible deployment scenarios are supported.

### US-12: Implement Cross-Cutting Concerns Using Port Decorators
- As an architect, I want logging, retry, and metrics implemented using port decorators in the infrastructure layer so that domain logic remains clean and unaware of cross-cutting concerns.

### US-13: Validate End-to-End Message Flow
- As a developer, I want end-to-end message flow validated across both transports so that the architecture operates correctly, and transport interchangeability is confirmed.

### US-14: Provide Architecture and Configuration Documentation
- As a developer and operator, I want architecture and configuration documented so that the system can be maintained, extended, and deployed correctly.

## Acceptance Criteria

### Port Abstractions (US-01)
- [ ] EventPublisherPort interface defined for publishing events outbound
- [ ] EventSubscriberPort interface defined for subscribing/unsubscribing from event channels
- [ ] EventReceiverPort interface defined for receiving and processing inbound events
- [ ] All port interfaces reside in domain module with no infrastructure dependencies
- [ ] Domain logic depends only on port interfaces, never on implementations

### Message Envelope (US-02)
- [ ] Standard message envelope defined with metadata and payload fields
- [ ] Envelope is immutable once created
- [ ] Envelope can be serialized/deserialized without transport-specific dependencies
- [ ] correlationId and headers support observability and distributed tracing

### Adapter Delegation Layer (US-03)
- [ ] One adapter implements EventPublisherPort delegating to active transport
- [ ] One adapter implements EventSubscriberPort delegating to active transport
- [ ] Adapter contains no transport-specific logic (delegation only)
- [ ] Adapter accepts transport implementation through dependency injection

### In-Memory Transport (US-04)
- [ ] In-memory transport implements internal transport interface
- [ ] Selected when configuration property set to in-memory
- [ ] Publishing delivers to subscribers within same process
- [ ] Ordering preserved based on partition key
- [ ] No external infrastructure required

### Kafka Transport (US-09)
- [ ] Kafka transport implements internal transport interface
- [ ] Selected when configuration property set to kafka
- [ ] Topic configuration is externalized (not hardcoded)
- [ ] Consumer group configuration supported and externalized
- [ ] Partition ordering preserved based on partition key

### Configuration-Driven Selection (US-10)
- [ ] Transport selected via single property: adapter.transport=in-memory|kafka
- [ ] Switching requires only configuration change (no code changes)
- [ ] Only one transport active at runtime
- [ ] Startup logs indicate which transport is active
- [ ] Invalid/missing transport config fails startup with descriptive error

### Module Enable/Disable (US-11)
- [ ] adapter.receiver.enabled configurable (default: true)
- [ ] adapter.handler.enabled configurable (default: true)
- [ ] adapter.dispatcher.enabled configurable (default: true)
- [ ] Disabled modules not instantiated, consume no resources
- [ ] System functions with subset of modules enabled

### Architecture Guardrails (US-05)
- [ ] Domain module does not depend on infrastructure/adapter modules
- [ ] Port interfaces do not depend on adapter implementations
- [ ] Handler does not depend on Kafka or transport implementations
- [ ] Build fails automatically on architecture violations

### End-to-End Flow (US-13)
- [ ] Complete flow works: Receiver → Handler → Dispatcher
- [ ] Flow works with in-memory transport
- [ ] Flow works with Kafka transport
- [ ] Same test scenarios run against both transports without code changes
- [ ] Envelope metadata preserved end-to-end

## Dispatch Center Communication

### Routing Model
| Source | Target | Event Type | Topic |
|--------|--------|------------|-------|
| IPL | WDX | CreateRequest | events-wdx |
| IPL | UCRI | CreateRequest | events-ucri |
| IPL | POLICE | CreateRequest | events-police |
| WDX | IPL | AcceptOperation | events-ipl |
| WDX | IPL | RejectOperation | events-ipl |
| UCRI | IPL | AcceptOperation | events-ipl |
| POLICE | IPL | AcceptOperation | events-ipl |

### Per-Dispatch Center Configuration
| Property | Description |
|----------|-------------|
| dispatch-center.{name}.enabled | Enable/disable dispatch center |
| dispatch-center.{name}.topic | Event Bus address / Kafka topic |
| dispatch-center.{name}.url | Connection URL for dispatch center API |
| dispatch-center.{name}.retry-attempts | Retry attempts on failure |
| dispatch-center.{name}.retry-delay-ms | Delay between retries |
| dispatch-center.{name}.timeout-ms | Connection timeout |
| dispatch-center.{name}.ssl-enabled | Enable SSL/TLS |
| dispatch-center.{name}.cert-path | Certificate file path |
| dispatch-center.{name}.key-path | Private key file path |
| dispatch-center.{name}.dlq-topic | Dead Letter Queue topic |

## Validation Rules
| Field | Rule |
|-------|------|
| adapter.transport | Must be "in-memory" or "kafka" |
| dispatch-center.{name}.enabled | Boolean (true/false) |
| dispatch-center.{name}.topic | Required when enabled=true |
| dispatch-center.{name}.url | Required when enabled=true |
| dispatch-center.{name}.retry-attempts | Integer >= 0 |
| dispatch-center.{name}.timeout-ms | Integer > 0 |

## Error Handling
| Scenario | Behavior |
|----------|----------|
| No transport configured | Startup fails with descriptive error |
| Invalid transport value | Startup fails listing valid options |
| Disabled module | No resources consumed, no subscriptions created |
| Event validation failure | Rejected with clear reason logged |
| Publish failure | Retry with configurable attempts, then DLQ |
| Connection failure | Clear actionable error message |

## Cross-Cutting Concerns (Decorators)
| Concern | Description |
|---------|-------------|
| Logging | Logs publish/receive operations with context |
| Retry | Retries failed publish with configurable backoff |
| Metrics | Exposes publish/receive/failure counts and latency |
