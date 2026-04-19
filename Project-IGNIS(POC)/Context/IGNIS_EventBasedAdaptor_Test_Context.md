# Testing Context

## Scope
- **In Scope:**
  - Messaging port abstractions (EventPublisherPort, EventSubscriberPort, EventReceiverPort)
  - Message envelope and metadata model
  - Adapter delegation layer behavior
  - In-memory transport functionality
  - Kafka transport functionality
  - Receiver module (event ingestion and validation)
  - Handler module (business logic processing)
  - Dispatcher module (event routing and publishing)
  - Configuration-driven transport switching
  - Module enable/disable via configuration
  - Cross-cutting concerns (logging, retry, metrics via decorators)
  - End-to-end message flow validation (Receiver → Handler → Dispatcher)
  - Architecture guardrails enforcement

- **Out of Scope:**
  - UI testing (Not specified in requirements)
  - Database-related testing (Not specified in requirements)
  - External system behavior of Source/Target systems (only integration points considered)
  - Performance benchmarking (Not explicitly specified) [NEEDS CLARIFICATION]

## Test Data
| Data Type | Value | Purpose |
|-----------|-------|---------|
| Valid event message | Well-formed message envelope with payload and metadata | Happy path end-to-end processing |
| Invalid event message | Malformed or incomplete envelope | Validation failure in Receiver |
| Transport config | adapter.transport=in-memory | Validate in-memory mode |
| Transport config | adapter.transport=kafka | Validate Kafka mode |
| Module config | adapter.receiver.enabled=true/false | Validate Receiver enable/disable |
| Module config | adapter.handler.enabled=true/false | Validate Handler enable/disable |
| Module config | adapter.dispatcher.enabled=true/false | Validate Dispatcher enable/disable |
| Correlation ID | Unique identifier value | Traceability and observability |
| Headers | Key-value metadata | Validate metadata propagation |

## Test Environment
- **Tool:** Postman


## Dependencies
- Kafka broker must be running for Kafka transport tests
- In-memory transport requires no external dependency
- Configuration properties must be correctly set before startup
- Architecture validation tool/framework must be integrated for guardrail enforcement
- Test framework capable of running same tests across both transports

## Known Issues
- Not specified in requirements