# Project Context

## Application
- **Name:** Adapter Service Messaging and Processing Layer
- **Type:** API
- **Domain:** Event-driven Messaging / Integration Platform

## Tech Stack
- **Frontend:** Not specified in requirements
- **Backend:** Java
- **Database:** Not specified in requirements
- **API Type:** REST

## Environment
- **Dev URL:** Not specified in requirements
- **Staging URL:** Not specified in requirements
- **Prod URL:** Not specified in requirements

## Key Constraints
- Messaging must be transport-agnostic (Kafka or in-memory switch via configuration)
- Domain logic must remain independent of infrastructure
- Only one messaging adapter per port with delegation to active transport
- Architecture must follow Hexagonal Architecture (Ports and Adapters)
- No transport-specific dependencies allowed in domain module
- Configuration-driven behavior only (no recompilation for transport switching)
- Must support modular monolith and distributed deployment modes
- Cross-cutting concerns (logging, retry, metrics) must be implemented via decorators
- Strict architecture guardrails enforced via automated checks (build failure on violation)