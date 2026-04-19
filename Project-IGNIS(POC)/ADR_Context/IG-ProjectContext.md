# Project Context: IGNIS Adapter Integration Service

## Application
- **Name:** Adapter Integration Service (Event Backbone)
- **Type:** API / Integration Service
- **Domain:** Emergency Services / Event-driven Messaging / Integration Platform

## Tech Stack
- **Frontend:** Not applicable (backend service only)
- **Backend:** Java 17+, Quarkus Framework
- **Database:** Not specified (prototype excludes persistence)
- **API Type:** REST (IPL-facing), gRPC over HTTP/2 (WDX-facing)
- **Messaging:** Kafka (distributed mode) / Vert.x EventBus (in-memory standalone mode)
- **Architecture:** Hexagonal Architecture (Ports and Adapters)

## Environment
- **Dev URL:** Not specified in requirements
- **Staging URL:** Not specified in requirements
- **Test URL:** wdx3-test.cloud.ise-cobra.de:443 (WDX)
- **Prod URL:** Not specified in requirements

## System Architecture

### Deployment Modes
| Mode | Description |
|------|-------------|
| Domain Modular (Standalone) | Single deployable service; internal communication via in-memory event bus (Vert.x) |
| Distributed (Kafka-Based) | Three independent services (Receiver, Handler, Dispatcher) communicating via Kafka |

### Core Components
| Component | Description |
|-----------|-------------|
| Receiver | Ingress of events - consumes events via messaging ports |
| Handler | Transformation and orchestration logic - business logic processing |
| Dispatcher | Egress of events - determines outbound routing and publishes events |

### Dispatch Centers
| Center | Topic | Description |
|--------|-------|-------------|
| IPL | events-ipl | Source system initiating incident dispatch |
| WDX | events-wdx | Operational hub for incident distribution |
| UCRI | events-ucri | Emergency services dispatch center |
| POLICE | events-police | Law enforcement dispatch center |

## Key Constraints

### Architectural Constraints
- Messaging must be transport-agnostic (Kafka or in-memory switch via configuration)
- Domain logic must remain independent of infrastructure
- Only one messaging adapter per port with delegation to active transport
- Architecture must follow Hexagonal Architecture (Ports and Adapters)
- No transport-specific dependencies allowed in domain module
- Configuration-driven behavior only (no recompilation for transport switching)
- Must support modular monolith and distributed deployment modes
- Cross-cutting concerns (logging, retry, metrics) must be implemented via decorators
- Strict architecture guardrails enforced via automated checks (build failure on violation)

### Technical Constraints
- Single codebase for all deployment modes
- Runtime configuration via application properties
- Long-term maintainability required
- Strong isolation between business logic and messaging technology
- Each event must be acknowledged within 10 seconds
- Event ordering preserved based on partition key

### Configuration Properties
| Property | Description | Default |
|----------|-------------|---------|
| adapter.transport | Transport mode selection | in-memory / kafka |
| adapter.receiver.enabled | Enable/disable Receiver module | true |
| adapter.handler.enabled | Enable/disable Handler module | true |
| adapter.dispatcher.enabled | Enable/disable Dispatcher module | true |

### Dispatch Center Configuration
| Property | Description | Default |
|----------|-------------|---------|
| dispatch-center.inbound.topic | Incoming events topic | events-inbound |
| dispatch-center.default.retry-attempts | Retry attempts on failure | 3 |
| dispatch-center.default.retry-delay-ms | Delay between retries | 1000 |
| dispatch-center.default.timeout-ms | Connection timeout | 5000 |
| dispatch-center.default.ssl-enabled | Enable SSL/TLS | false |
| dispatch-center.default.dlq-topic | Dead Letter Queue topic | events-dlq |

## Port Abstractions
| Port | Purpose |
|------|---------|
| EventPublisherPort | Publishing events outbound |
| EventSubscriberPort | Subscribing to and unsubscribing from event channels |
| EventReceiverPort | Receiving and processing inbound events |

## Known Limitations (Current Release)
- Mock IPL service only; real IPL system integration deferred
- No database or cache layer (no persistence)
- No storage of ID mappings or control center information
- Patient data within mission dispatch messages is not processed
- No entity or system identifier mapping logic
- No retry mechanisms, fallback routing, or automatic error recovery (prototype)
- Testing performed in controlled environments only
