# Story: ALAMOS Phase 1 – Generate Situation Report Domain Events

| Field | Value |
|--------|-------|
| **Story ID** | US-ADAPTER-ALAMOS-002 |
| **Story Name** | ALAMOS Phase 1 – Generate Situation Report Domain Events |
| **Actor** | Adapter Integration |
| **Goal** | Transform ALAMOS Situation Reports into canonical domain events |
| **Business Value** | Enables standardized event-driven processing by converting validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event while ensuring proper incident correlation and resource mapping. |
| **Jira Ticket** | IPL-26910 – Generate Situation Report Domain Events *(Open)* |

---

## User Story

**As** an Adapter Integration system,  
**I want** to transform validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event,  
**So that** Situation Reports can be consumed consistently by downstream systems using a standardized event model with accurate incident correlation and resource mapping.

---

## Key Scenarios & Variations

### Happy Path
- Valid ALAMOS Situation Report is received and transformed successfully.
- Reporting resources are mapped to the canonical event structure.
- `call_sign` is available and mapped directly.

### Incident Correlation
- Incident correlation performed using `external_id`.
- Incident correlation performed using `incident_number` when `external_id` is unavailable.

### Fallback Handling
- `call_sign` fallback logic is applied when the value is missing.

### Validation & Processing Failures
- Required event attributes are missing or invalid.
- Canonical Domain Event payload generation fails due to mapping or validation issues.

---

## Acceptance Criteria

### Event Transformation
- The Adapter must transform validated ALAMOS Situation Reports into the canonical `incident.situation_report_received/v1` Domain Event.
- The Adapter must generate a valid canonical Domain Event payload containing all required attributes and metadata.

### Incident Correlation
- The Adapter must perform incident correlation using `external_id` when available.
- The Adapter must use `incident_number` as a fallback mechanism when `external_id` is not available.

### Resource Mapping
- The Adapter must map reporting resources from the ALAMOS payload into the canonical event structure.
- The Adapter must apply defined `call_sign` fallback handling when a reporting resource does not provide a valid `call_sign`.

### Validation
- The Adapter must validate the generated event prior to publication or downstream processing.

### Error Handling
- The Adapter must return an appropriate error when incident correlation, resource mapping, or event generation cannot be completed successfully.

### Output
- The generated event must conform to the `incident.situation_report_received/v1` contract and be ready for downstream consumption.