# Project Context

## Application
- **Name:** ALAMOS Integration (IGNIS Platform) — also referred to as "ALAMOS Adapter" / "ALAMOS Gateway" / "IPL Event Exchange Service (EES)" ecosystem.
  Source: `ALAMOS Integration – Phase 1.md`
- **Type:** Backend system-to-system integration middleware (Adapter + Gateway services). No end-user frontend application is documented.
  Source: `ALAMOS Integration – Phase 1.md`, `Technical Feasibility Analysis.md`
- **Domain:** Public safety / emergency dispatch and incident (mission) management — integration between the IGNIS platform (via "IPL") and the external ALAMOS alerting/mission system (via "ALAMOS FE2").
  Source: `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-001.md` through `US-ADAPTER-ALAMOS-004.md`

## Tech Stack
- **Frontend:** Not Available in Source Documents.
- **Backend:** Quarkus (Java, running on Vert.x/Netty internally) is used for the Event Integration Adapter.
  Source: `Technical Feasibility Analysis.md`
- **Database:** Not Available in Source Documents.
- **API Type:**
  - REST/JSON — inbound Situation Report endpoint on the Adapter, and the "REST ALARM API" used by the ALAMOS Gateway toward ALAMOS FE2.
    Source: `US-ADAPTER-ALAMOS-001.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`
  - SOAP/XML — `AlarmRequest` (IPL → ALAMOS Gateway) and IPL endpoint `POST /einsatztransfer/erzeugeEinsatzmeldung` (FacadeService → IPL).
    Source: `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-004.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`, `Situation Reports (EVENT).svg`
  - HTTPS/TLS transport for inbound Adapter traffic (IPL, UCRI, future partners).
    Source: `Technical Feasibility Analysis.md`

## Environment
- **Dev URL:** Not Available in Source Documents.
- **Staging URL:** Not Available in Source Documents.
- **Prod URL:** Not Available in Source Documents.
- **Example endpoint pattern (illustrative, from technical analysis, not an environment URL):** `https://adapter.company.com:8443`
  Source: `Technical Feasibility Analysis.md`

## Key Constraints
- Release 26.3 must avoid full gateway migration risk; a "controlled strangler" approach is used instead. Source: `ALAMOS Integration – Phase 1.md`
- IPL must remain unchanged in Release 26.3 (existing SOAP endpoints reused). Source: `ALAMOS Integration – Phase 1.md`
- No Inbox, Outbox, Process Tracker, Event Bus, or standalone EES service in Release 26.3; these are deferred to Release 26.4. Source: `ALAMOS Integration – Phase 1.md`
- Internal Domain Events are not persisted in Release 26.3. Source: `ALAMOS Integration – Phase 1.md`
- A single shared inbound TLS server certificate is required for the Adapter because TLS certificate selection occurs before HTTP-level caller identity is known (protocol-level constraint, applies to all frameworks). Source: `Technical Feasibility Analysis.md`

---

# Additional Project-Level Information

## Vision
Deliver ALAMOS integration for Release 26.3 using a controlled strangler approach: keep existing (legacy) Alerting and Continuous Mission Update capabilities on the proven legacy ALAMOS Gateway path, while introducing Situation Reports as a new inbound event-driven capability, and lay groundwork (via an internal Domain Event and an extractable FacadeService) for a future full event-driven migration in Release 26.4.
Source: `ALAMOS Integration – Phase 1.md`

## Scope

### In Scope (Release 26.3)
| Capability | Direction | State | Outcome |
|---|---|---|---|
| Alerting | IPL → ALAMOS | LEGACY | Gateway supports `AlarmRequest` including `<squads>` |
| Continuous Mission Updates | IPL → ALAMOS | LEGACY | Existing gateway forwards all updates without dispatch correlation |
| Situation Reports | ALAMOS → IPL | EVENT (Stage 1) | Domain Event created and synchronously mapped to IPL |

Source: `ALAMOS Integration – Phase 1.md`

### Out of Scope (Release 26.3)
- IPL-to-ALAMOS flow for Situation Reports (not supported per Epic 6.1 and Phase-1 scope).
- Inbox, Outbox, Process Tracker, Event Bus, standalone EES service.
- Dispatch correlation for Continuous Mission Updates.

Source: `ALAMOS Integration – Phase 1.md`

## Objectives
- Avoid migration risk for Release 26.3.
- Deliver Situation Reports as a new inbound integration capability.
- Preserve existing ALAMOS Alerting and Continuous Mission Update implementations.
- Introduce the internal Domain Event contract `incident.situation_report_received`.
- Keep IPL unchanged by reusing existing SOAP endpoints.
- Prepare FacadeService extraction into EES in Release 26.4.
- Enable future Inbox/Outbox-based asynchronous processing.

Source: `ALAMOS Integration – Phase 1.md`

## Stakeholders / Actors
- Adapter Integration (system/team) — `US-ADAPTER-ALAMOS-001.md`, `US-ADAPTER-ALAMOS-002.md`, `US-ADAPTER-RELIABILITY-001.md`, `US-INTEGRATION-E2E-001.md`
- FacadeService (ALAMOS Adapter) — `US-ADAPTER-ALAMOS-003.md`, `US-ADAPTER-ALAMOS-004.md`
- ALAMOS Gateway — `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-002.md`, `US-ALAMOS-GW-003.md`, `US-ALAMOSGW-MOCK-001.md`
- ALAMOS FE2 (external ALAMOS front-end/system) — `ALAMOS Integration – Phase 1.md`, sequence diagrams
- IPL / IPL Server (IGNIS platform component) — all user stories
- Integration team (mock gateway usage/testing) — `US-ALAMOSGW-MOCK-001.md`
- Adapter Integration Team (build/CI/CD) — `US-PLATFORM-CICD-001.md`
- External partner systems referenced only in the technical feasibility analysis: IPL, UCRI, "future partners" — `Technical Feasibility Analysis.md`

## Business Domain
Public safety / rescue and incident dispatch integration — exchange of alerting, mission update, and situation report information between the IGNIS platform (IPL) and the ALAMOS system (ALAMOS Gateway / ALAMOS FE2).
Source: `ALAMOS Integration – Phase 1.md`

## Functional Summary
1. **Alerting (LEGACY):** IPL sends `AlarmRequest` (including `<squads>` squad information) through the Facade Service (legacy) to the ALAMOS Gateway, which forwards to ALAMOS FE2 via a REST Alarm API; acknowledgements propagate back to IPL. Source: `ALAMOS Integration – Phase 1.md`, `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`
2. **Continuous Mission Updates (LEGACY):** IPL sends mission updates (triggered by incident status, resource status, keyword, or location changes) through the legacy Facade Service and ALAMOS Gateway; no dispatch correlation. Source: `ALAMOS Integration – Phase 1.md`, `US-ALAMOS-GW-002.md`
3. **Situation Reports (EVENT, Stage 1):** ALAMOS FE2 sends a Situation Report to the ALAMOS Adapter; the Adapter validates and creates the internal Domain Event `incident.situation_report_received`; the FacadeService (inside the Adapter) maps this event to an IPL request and invokes IPL's `erzeugeEinsatzmeldung` SOAP endpoint synchronously; the result is acknowledged back to ALAMOS FE2. Source: `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-001.md` – `US-ADAPTER-ALAMOS-004.md`, `Situation Reports (EVENT).svg`
4. **Mock Gateway:** The ALAMOS Gateway can run in a configurable mock mode for development/testing without live ALAMOS FE2 connectivity. Source: `US-ALAMOSGW-MOCK-001.md`
5. **Reliability:** Existing retry, DLQ, error-handling, and logging mechanisms are validated across all ALAMOS flows. Source: `US-ADAPTER-RELIABILITY-001.md`
6. **Build/CI-CD:** Build, automated test, and packaging pipelines are configured for the Adapter and Gateway. Source: `US-PLATFORM-CICD-001.md`

## Non-Functional Requirements
- **Security / Transport:** Inbound HTTPS to the Adapter must use a single shared TLS server certificate (technically cannot differentiate per-caller certificates before the HTTP layer is reached because of the TLS handshake protocol); caller identity should be validated via mTLS client certificates and/or application-level authorization instead. Source: `Technical Feasibility Analysis.md`
- **Reliability:** Existing retry and DLQ (Dead Letter Queue) mechanisms must handle recoverable and non-recoverable failures consistently, with logging/traceability of retry attempts and DLQ events. Source: `US-ADAPTER-RELIABILITY-001.md`
- **Synchronous processing:** Situation Report processing (Adapter → FacadeService → IPL) is fully synchronous in Release 26.3; no asynchronous infrastructure (Inbox/Outbox/Event Bus) is introduced yet. Source: `ALAMOS Integration – Phase 1.md`
- **Backward compatibility:** Alerting and Continuous Mission Update flows must remain backward compatible with existing implementations, including behavior when squad information is absent. Source: `US-ALAMOS-GW-001.md`, `US-ALAMOS-GW-003.md`
- **Testability:** A mock mode for the ALAMOS Gateway must be supported for integration/E2E testing without impacting normal operation when disabled. Source: `US-ALAMOSGW-MOCK-001.md`
- **Build automation:** Builds must run automated unit/integration tests, fail artifact generation on failure, and produce diagnostic logging. Source: `US-PLATFORM-CICD-001.md`
- Specific performance, availability, scalability, or compliance NFR targets: Not Available in Source Documents.

## Architecture Overview
Release 26.3 uses a controlled strangler pattern with three logical paths:

1. **Alerting (LEGACY):** `IPL → Facade Service (LEGACY) → ALAMOS Gateway → ALAMOS FE2`, with `<squads>` support implemented in the Legacy ALAMOS Gateway. No involvement of Adapter or EES.
2. **Continuous Mission Updates (LEGACY):** `IPL → Facade Service (LEGACY) → ALAMOS Gateway (LEGACY) → ALAMOS FE2`. No involvement of Adapter or EES.
3. **Situation Reports (EVENT, Stage 1):** `ALAMOS FE2 → ALAMOS Adapter → (create Domain Event incident.situation_report_received) → FacadeService (running inside the Adapter) → IPL`.

The FacadeService is implemented as a standalone, extractable component inside the Adapter so it can later be extracted into the EES (Event Exchange Service) during Release 26.4. Domain Events are not persisted in 26.3 (no Inbox/Outbox/Process Tracker/Event Bus).

Source: `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-003.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg`, `Situation Reports (EVENT).svg`

### Domain Event Contract
- **Event name:** `incident.situation_report_received`
- **Contract:** `incident.situation_report_received/v1`
- **Minimum payload:** `event_id`, `event_type`, `occurred_at`, `source_system`, `tenant_id`, `incident.external_id`, `incident.incident_number`, `authoring_resource.external_resource_id`, `authoring_resource.call_sign`, `situation_report.text`, `situation_report.reported_at`.

Source: `ALAMOS Integration – Phase 1.md`

### TLS Handshake Constraint (Adapter inbound HTTPS)
The Adapter's inbound TLS server certificate must be selected immediately after `ClientHello`, before any HTTP data (headers, URI, payload, auth token, business/caller identity) is available. Therefore a single Quarkus/Vert.x HTTPS listener cannot present a different server certificate per calling partner (e.g., IPL vs. UCRI) if they share the same hostname/IP/port. Recommended approach: one shared server certificate, with caller identity validated via mTLS and/or application-level authorization.
Source: `Technical Feasibility Analysis.md`, `TLS Handshake Works.svg`, `Screenshot 2026-07-13 171532.jpg` (duplicate visual representation of the same diagram)

## Integrations
| System | Direction | Protocol | Purpose | Source |
|---|---|---|---|---|
| IPL (IGNIS) | IPL → ALAMOS Gateway | SOAP (`AlarmRequest`) | Alerting (legacy) | `ALAMOS Integration – Phase 1.md`, `ALERTING WITH SQUAD INFORMATION (LEGACY).svg` |
| IPL (IGNIS) | IPL → ALAMOS Gateway | Legacy gateway protocol | Continuous Mission Updates | `US-ALAMOS-GW-002.md` |
| ALAMOS Gateway → ALAMOS FE2 | Gateway → FE2 | REST Alarm API | Alerting delivery | `ALERTING WITH SQUAD INFORMATION (LEGACY).svg` |
| ALAMOS FE2 → Adapter | FE2 → Adapter | REST (Situation Report) | Inbound Situation Report | `US-ADAPTER-ALAMOS-001.md`, `Situation Reports (EVENT).svg` |
| Adapter/FacadeService → IPL | Adapter → IPL | SOAP `POST /einsatztransfer/erzeugeEinsatzmeldung` | Situation Report processing | `US-ADAPTER-ALAMOS-004.md`, `Situation Reports (EVENT).svg` |
| UCRI and future partners → Adapter | Partner → Adapter | HTTPS (inbound) | Mentioned only in TLS feasibility context; no functional integration details documented | `Technical Feasibility Analysis.md` |

## Risks
- Synchronous coupling exists between Adapter → FacadeService → IPL; processing depends on real-time availability of IPL endpoints. Source: `ALAMOS Integration – Phase 1.md`
- No Inbox, Outbox, Queue, Process Tracker, or Event Bus is used in 26.3 — failures are not durably queued at the Domain Event level. Source: `ALAMOS Integration – Phase 1.md`
- Internal Domain Events are not persisted in 26.3. Source: `ALAMOS Integration – Phase 1.md`
- FacadeService must be extracted into EES during Release 26.4 (future migration dependency/risk). Source: `ALAMOS Integration – Phase 1.md`
- Multiple exposed HTTPS ports (an evaluated but not recommended alternative) would increase attack surface, security policy complexity, and compliance tracking effort. Source: `Technical Feasibility Analysis.md`

## Assumptions
Not Available in Source Documents (no assumptions are explicitly documented/labeled as assumptions in the source files; the Phase-1 document distinguishes "Open Questions" instead — see below).

## Dependencies
- Existing IPL SOAP endpoints must remain available/unchanged until future migration phases. Source: `ALAMOS Integration – Phase 1.md`
- Existing Retry & DLQ mechanisms (pre-existing, validated rather than newly built). Source: `US-ADAPTER-RELIABILITY-001.md`
- ALAMOS Gateway mock mode dependency for development/testing without live ALAMOS FE2. Source: `US-ALAMOSGW-MOCK-001.md`
- Build/CI pipeline templates must be updated to support ALAMOS Phase 1 changes. Source: `US-PLATFORM-CICD-001.md`

## Open Questions
- "Where will the Domain Event be created – Adapter or EES?" → Answered in-document: Domain event will be created in Adapter. Source: `ALAMOS Integration – Phase 1.md`
- "What transport protocol should be used between Adapter and EES?" → REST + JSON Domain Event marked ✅; SOAP + XML Domain Event marked ❌ (i.e., REST/JSON is the intended choice, but this is listed under "Clarifications Required," so it is not stated as fully finalized). Source: `ALAMOS Integration – Phase 1.md`

## Glossary
| Term | Definition (as used in source documents) | Source |
|---|---|---|
| ALAMOS | External alerting/mission system integrated with IGNIS via Gateway/Adapter/FE2 | `ALAMOS Integration – Phase 1.md` |
| ALAMOS FE2 | ALAMOS front-end system that sends/receives Alerting, Mission Update, and Situation Report traffic | `ALAMOS Integration – Phase 1.md` |
| ALAMOS Gateway | Existing/legacy component forwarding Alerting and Continuous Mission Update traffic between IPL and ALAMOS FE2 | `ALAMOS Integration – Phase 1.md`, `US-ALAMOS-GW-001.md` |
| ALAMOS Adapter | New component receiving Situation Reports from ALAMOS FE2 and creating Domain Events | `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-001.md` |
| FacadeService | Component inside the Adapter that maps Domain Events to IPL requests and invokes IPL synchronously; extractable to EES in Release 26.4 | `ALAMOS Integration – Phase 1.md`, `US-ADAPTER-ALAMOS-003.md` |
| IPL | IGNIS platform component/interface consuming and producing Alerting, Mission Update, and Situation Report data | All user stories |
| EES | Event Exchange Service — future standalone service the FacadeService will be extracted into (Release 26.4) | `ALAMOS Integration – Phase 1.md` |
| Domain Event | Internal, Adapter-local event representation (e.g., `incident.situation_report_received`), not persisted in 26.3 | `ALAMOS Integration – Phase 1.md` |
| DLQ | Dead Letter Queue — existing mechanism for unrecoverable failed messages | `US-ADAPTER-RELIABILITY-001.md` |
| Strangler pattern | Migration approach where legacy paths are preserved while new capabilities are incrementally introduced | `ALAMOS Integration – Phase 1.md` |
| `<squads>` | Squad information field added to Alerting `AlarmRequest` | `ALAMOS Integration – Phase 1.md`, `US-ALAMOS-GW-003.md` |
| mTLS | Mutual TLS — recommended mechanism for validating caller identity when a shared server certificate is used | `Technical Feasibility Analysis.md` |

## Conflicts / Observations Detected
1. **Dual story-identifier schemes:** `ALAMOS Integration – Phase 1.md` references Confluence-style story IDs "US-100" (Alerting/Squads), "US-200" (Continuous Mission Updates), and "US-300" (Situation Reports), while the Jira-tracked user story files use different IDs (`US-ADAPTER-ALAMOS-00x`, `US-ALAMOS-GW-00x`). `US-INTEGRATION-E2E-001.md` refers to these same features as "US-ALAMOS-100/200/300". The source documents do not explicitly cross-reference these two ID schemes to one another; this mapping is inferred from feature descriptions only and is recorded here as an observation, not resolved as fact.
2. **Duplicate diagram sources:** `Screenshot 2026-07-13 171532.jpg` and `TLS Handshake Works.svg` depict the same "TLS Handshake — Certificate Selection Timing (Adapter)" diagram content. No content conflict was found between them.
3. **UCRI mentioned in isolation:** `Technical Feasibility Analysis.md` introduces "UCRI" as an inbound partner system to the Adapter, but no other input document defines, describes, or references UCRI. Not Available in Source Documents beyond this single mention.
4. No explicit timestamps were found in any source document to allow "most recent version" conflict resolution; where ambiguity existed, it is documented above rather than arbitrarily resolved.
