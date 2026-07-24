# 🚀 ALAMOS Integration – Phase 1

## 📌 Overview

This page describes the **Phase-1 implementation for ALAMOS integration** using a **controlled strangler approach**.

The objective is to:

- ✅ Deliver business value without introducing a full gateway migration
- ✅ Keep existing Alerting and Continuous Mission Update capabilities on the proven legacy gateway path
- ✅ Introduce Situation Reports as a new inbound event-driven capability
- ✅ Establish internal Domain Events within the Adapter as preparation for future event-driven migration
- ✅ Use a FacadeService inside the Adapter to bridge Domain Events to existing IPL interfaces

---

## 🎯 Goals

- 🚫 Avoid migration risk for Release 26.3
- ✅ Deliver Situation Reports as a new inbound integration capability
- ✅ Preserve existing ALAMOS Alerting and Continuous Mission Update implementations
- ✅ Introduce the internal Domain Event contract `incident.situation_report_received`
- ✅ Keep IPL unchanged by reusing existing SOAP endpoints
- ✅ Prepare FacadeService extraction into EES in Release 26.4
- ✅ Enable future Inbox/Outbox-based asynchronous processing

---

## 🧭 Scope (Release 26.3)

| Capability | Direction | State | Outcome | User Story Link |
|------------|-----------|-------|---------|-----------------|
| 🔔 Alerting | IPL → ALAMOS | 🟡 LEGACY | Gateway supports `AlarmRequest` including `<squads>` | US-100: Extending Alarms with Squad Information - IGNIS-Plus-Dokumentation - Confluence |
| 📡 Continuous Mission Updates (US-200) | IPL → ALAMOS | 🟡 LEGACY | Existing gateway forwards all updates without dispatch correlation | US-200: Triggers for Continuous Mission Updates - IGNIS-Plus-Dokumentation - Confluence |
| 📥 Situation Reports | ALAMOS → IPL | 🟢 EVENT (Stage 1) | Domain Event created and synchronously mapped to IPL | US-300: Processing of Situation Reports (Lagemeldung) from ALAMOS - IGNIS-Plus-Dokumentation - Confluence |

> **NOTE** - As defined in Epic 6.1 and the Phase 1 scope, the IPL-to-ALAMOS flow for Situation Reports is not supported.

Epic 6.1 → [epic-6.1-alamos-release-26.3_en.md - ipl_event_exchange_service](epic-6.1-alamos-release-26.3_en.md)

---

## ⚖️ Key Architectural Decisions

### 🔔 1. Alerting Remains LEGACY

```
IPL → Facade Service (LEGACY) → ALAMOS Gateway → ALAMOS FE2
```

- ✅ Existing Alerting flow remains authoritative
- ✅ `<squads>` support is implemented in the Legacy ALAMOS Gateway
- ✅ Acknowledgements are propagated synchronously back to IPL
- ⚠️ No involvement of Adapter or EES in this release

### 🔔 2. Continuous Mission Updates Remain LEGACY

```
IPL → Facade Service (LEGACY) → ALAMOS Gateway (LEGACY) → ALAMOS FE2
```

- ✅ All mission updates continue to use the existing gateway
- ✅ Incident status, resource status, keyword, and location change triggers are supported
- ✅ Gateway changes may be introduced if required
- ⚠️ No involvement of Adapter or EES in this release
- ❌ No dispatch correlation

### 📥 3. Situation Reports as EVENT (Stage 1)

Situation Reports are introduced as a new inbound EVENT capability using an Adapter-local event model.

```
ALAMOS FE2
    ↓
  ALAMOS Adapter
    ↓
Create Domain Event
incident.situation_report_received
    ↓
FacadeService
    ↓
   IPL
```

#### Phase-1 Constraints

- ✅ Domain Event contract established inside the Adapter
- ✅ Processing remains fully synchronous
- ✅ FacadeService runs inside the Adapter
- ✅ IPL remains unchanged
- ❌ No Inbox
- ❌ No Outbox
- ❌ No Process Tracker
- ❌ No Event Bus
- ❌ No standalone EES service

---

## 🧱 Domain Event Definition

### 📌 Event Name

```
incident.situation_report_received
```

### 📦 Contract

```
incident.situation_report_received/v1
```

Full schema and contract at - [incident.situation_report_received/v1](incident.situation_report_received/v1)

### 📄 Minimum Payload

```json
{
  "event_id": "uuid",
  "event_type": "incident.situation_report_received",
  "occurred_at": "2026-01-01T12:00:00Z",
  "source_system": "ALAMOS",
  "tenant_id": "string",
  "incident": {
    "external_id": "string",
    "incident_number": "string"
  },
  "authoring_resource": {
    "external_resource_id": "string",
    "call_sign": "string"
  },
  "situation_report": {
    "text": "string",
    "reported_at": "2026-01-01T12:00:00Z"
  }
}
```

---

## 🧠 Component Responsibilities

### Adapter Responsibilities

- ✅ Receive Situation Reports from ALAMOS FE2
- ✅ Validate inbound payloads
- ✅ Transform and map incoming messages
- ✅ Correlate incidents using external_id or incident_number
- ✅ Resolve authoring resource mappings
- ✅ Apply call_sign fallback handling
- ✅ Create `incident.situation_report_received` as an internal typed Domain Event
- ✅ Invoke FacadeService synchronously
- ✅ Return acknowledgements to ALAMOS FE2
- ✅ Apply existing Retry & DLQ mechanisms

### FacadeService Responsibilities

- ✅ Receive `incident.situation_report_received`
- ✅ Map Domain Events to the IPL request model
- ✅ Invoke IPL `erzeugeEinsatzmeldung` synchronously
- ✅ Propagate SOAP success and fault responses
- ✅ Remain implemented as a standalone extractable class for Release 26.4 migration

---

## 🔁 Sequence Diagrams (Phase-1 Architecture)

### Alerting (LEGACY)

*There were errors rendering macro: An unknown error occurred.*

### Situation Reports (EVENT)

*There were errors rendering macro: An unknown error occurred.*

---

## ⚠️ Error Handling

- ✅ Validation errors are returned from FacadeService to the Adapter
- ✅ SOAP faults returned from IPL are propagated back to ALAMOS FE2
- ✅ Adapter returns success/error acknowledgements to ALAMOS FE2
- ✅ Existing Retry & DLQ mechanisms handle communication failures
- ✅ Structured logging and traceability are maintained

---

## ⚠️ Known Trade-Offs

- ⚠️ Synchronous coupling exists between Adapter → FacadeService → IPL
- ⚠️ Processing depends on real-time availability of IPL endpoints
- ⚠️ No Inbox, Outbox, Queue, Process Tracker, or Event Bus is used in 26.3
- ⚠️ Alerting remains in the LEGACY path, including `<squads>` support in the ALAMOS Gateway
- ⚠️ Continuous Mission Updates remain entirely in the legacy gateway path
- ⚠️ Existing IPL SOAP endpoints remain required until future migration phases are completed
- ⚠️ Internal Domain Events are not persisted in 26.3
- ⚠️ FacadeService must be extracted into EES during Release 26.4

---

## 🧠 Conclusion

Release **26.3 delivers** a controlled ALAMOS migration where Alerting (US-100) and Continuous Mission Updates (US-200) continue to operate through the existing ALAMOS Gateway, while Situation Reports (US-300) introduce an internal event-driven model within the ALAMOS Adapter.

The Adapter receives, validates, and transforms incoming Situation Reports into the internal Domain Event `incident.situation_report_received` and processes them synchronously through an embedded FacadeService that invokes existing IPL interfaces. To minimize delivery risk and avoid IPL changes, Inbox, Outbox, Process Tracker, Event Bus, and standalone EES services are intentionally deferred to Release 26.4, while the FacadeService remains extractable for future migration.

---

## ❓ Open Questions & Architectural Clarifications

### Clarifications Required

- **Where will the Domain Event be created – Adapter or EES?**
  - Domain event will be created in Adapter.

- **What transport protocol should be used between Adapter and EES?**
  - REST + JSON Domain Event? ✅
  - SOAP + XML Domain Event? ❌

---

## 📦 Relevant Links

| Description | Link |
|-------------|------|
| Epic Link | [epic-6.1-alamos-release-26.3_en.md - ipl_event_exchange_service](epic-6.1-alamos-release-26.3_en.md) |
| Epic 9 Link for roadmap of 26.3 and 26.4 | [epic-9-resource-management-rescuetrack-fleetserver-migration_en.md - ipl_event_exchange_service](epic-9-resource-management-rescuetrack-fleetserver-migration_en.md) |
| High-level onboarding Document for EES | [onboarding-high-level-overview_en.md - ipl_event_exchange_service](onboarding-high-level-overview_en.md) |
| ADR for Strangler pattern | [ADR-0007-strangler-facade-for-gateway-migration_en.md - ipl_event_exchange_service](ADR-0007-strangler-facade-for-gateway-migration_en.md) |
| Alamos Access Information | [Accessing via HTTP POST/GET - Manual - Alamos Manual](https://alamos-manual.example.com/http-access) |
| Data Format External Interface | [Data Format External Interface - Manual - Alamos Manual](https://alamos-manual.example.com/data-format) |
