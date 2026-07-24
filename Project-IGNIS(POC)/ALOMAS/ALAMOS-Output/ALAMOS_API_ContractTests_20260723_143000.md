# ALAMOS Integration – Release 26.3 API Contract Tests

**Generated:** 2026-07-23 14:30:00  
**Source:** ALAMOS_Feature_Context.md, ALAMOS_Project_Context.md, ALAMOS_Testing_Context.md  
**Template:** API04-API Contract Testing.md

---

## Notes

- All contract tests are derived exclusively from the documented API specifications and Domain Event contracts.
- Items marked **[Needs clarification]** indicate missing or undocumented specifications.
- The only documented schema is the `incident.situation_report_received/v1` Domain Event minimum payload.
- Full OpenAPI/Swagger or WSDL specifications are NOT available in source documents.
- Response schemas for success and error responses are NOT documented.

---

## API Contracts Covered

| # | Contract | Type | Source | Schema Available |
|---|----------|------|--------|------------------|
| 1 | incident.situation_report_received/v1 | Domain Event | ALAMOS Integration – Phase 1.md | Minimum payload documented |
| 2 | Adapter Situation Report Response | REST Response | US-ADAPTER-ALAMOS-001 | Not documented |
| 3 | IPL erzeugeEinsatzmeldung Response | SOAP Response | US-ADAPTER-ALAMOS-004 | Not documented |
| 4 | ALAMOS Gateway AlarmRequest Response | SOAP Response | US-ALAMOS-GW-001 | Not documented |
| 5 | ALAMOS REST ALARM API Response | REST Response | US-ALAMOS-GW-001 | Not documented |

---

## 1. Domain Event Contract: incident.situation_report_received/v1

**Contract:** incident.situation_report_received/v1  
**Type:** Internal Domain Event  
**Source:** ALAMOS Integration – Phase 1.md

### 1.1 Success Response Schema Validation

Based on the documented minimum payload:

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

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-001 | Domain Event | event_id | string (UUID) | Yes | Must be valid UUID format |
| CNT-002 | Domain Event | event_type | string | Yes | Must equal "incident.situation_report_received" |
| CNT-003 | Domain Event | occurred_at | string (ISO8601) | Yes | Must be valid ISO8601 datetime |
| CNT-004 | Domain Event | source_system | string | Yes | Must equal "ALAMOS" for this flow |
| CNT-005 | Domain Event | tenant_id | string | Yes | Must be non-empty string |
| CNT-006 | Domain Event | incident | object | Yes | Must contain incident correlation fields |
| CNT-007 | Domain Event | incident.external_id | string | Conditional | Primary correlation key (required if incident_number absent) |
| CNT-008 | Domain Event | incident.incident_number | string | Conditional | Fallback correlation key (required if external_id absent) |
| CNT-009 | Domain Event | authoring_resource | object | Yes | Must contain resource identification fields |
| CNT-010 | Domain Event | authoring_resource.external_resource_id | string | Yes | Must be non-empty string |
| CNT-011 | Domain Event | authoring_resource.call_sign | string | Conditional | Required or fallback applied **[Needs clarification]** |
| CNT-012 | Domain Event | situation_report | object | Yes | Must contain report content |
| CNT-013 | Domain Event | situation_report.text | string | Yes | Report content text |
| CNT-014 | Domain Event | situation_report.reported_at | string (ISO8601) | Yes | Must be valid ISO8601 datetime |

### 1.2 Negative Contract Tests – Domain Event

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-015 | Domain Event | event_id | integer (wrong type) | N/A | Reject: event_id must be string |
| CNT-016 | Domain Event | occurred_at | string (invalid format) | N/A | Reject: must be valid ISO8601 |
| CNT-017 | Domain Event | incident | null | N/A | Reject: incident object required |
| CNT-018 | Domain Event | authoring_resource | null | N/A | Reject: authoring_resource object required |
| CNT-019 | Domain Event | situation_report | null | N/A | Reject: situation_report object required |
| CNT-020 | Domain Event | Additional unknown field | any | N/A | **[Needs clarification: strict or lenient schema?]** |

---

## 2. Adapter Situation Report – Response Contract Tests

**Endpoint:** REST Adapter Situation Report Endpoint  
**Source:** US-ADAPTER-ALAMOS-001

### 2.1 Success Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-021 | Success | HTTP Status Code | integer | Yes | **[Needs clarification: expected success code (200, 201, 202?)]** |
| CNT-022 | Success | Response Body | object/string | **[Needs clarification]** | **[Needs clarification: response schema not documented]** |
| CNT-023 | Success | Acknowledgment | **[Needs clarification]** | **[Needs clarification]** | Must reflect successful IPL processing |

### 2.2 Error Response – Contract Violation

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-024 | Error | HTTP Status Code | integer | Yes | **[Needs clarification: expected error code (400, 422?)]** |
| CNT-025 | Error | Error Message | string | **[Needs clarification]** | Clear validation error for contract violation |
| CNT-026 | Error | Error Code | string/integer | **[Needs clarification]** | **[Needs clarification: error code structure not documented]** |

### 2.3 Error Response – IPL Processing Failure

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-027 | Error | HTTP Status Code | integer | Yes | **[Needs clarification: expected error code (500, 502?)]** |
| CNT-028 | Error | Acknowledgment | **[Needs clarification]** | **[Needs clarification]** | Must accurately reflect IPL processing failure |

### 2.4 Error Response – Technical Error (Invalid Method/Content-Type)

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-029 | Error | HTTP Status Code | integer | Yes | **[Needs clarification: 405 for method, 415 for content-type?]** |
| CNT-030 | Error | Error Message | string | **[Needs clarification]** | Technical error response |

---

## 3. IPL erzeugeEinsatzmeldung – Response Contract Tests

**Endpoint:** POST /einsatztransfer/erzeugeEinsatzmeldung  
**Protocol:** SOAP  
**Source:** US-ADAPTER-ALAMOS-004

### 3.1 Success Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-031 | SOAP Success | SOAP Envelope | XML | Yes | Valid SOAP envelope structure |
| CNT-032 | SOAP Success | Response Body | **[Needs clarification]** | **[Needs clarification]** | **[Needs clarification: WSDL/schema not documented]** |

### 3.2 Business Fault Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-033 | SOAP Fault | Fault Code | string | **[Needs clarification]** | **[Needs clarification: IPL fault codes not documented]** |
| CNT-034 | SOAP Fault | Fault String | string | **[Needs clarification]** | **[Needs clarification: IPL fault messages not documented]** |
| CNT-035 | SOAP Fault | Detail | **[Needs clarification]** | **[Needs clarification]** | Business fault details |

### 3.3 Technical Fault Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-036 | SOAP Fault | Fault Code | string | **[Needs clarification]** | Technical fault indicator |
| CNT-037 | SOAP Fault | Fault String | string | **[Needs clarification]** | Technical fault description |

---

## 4. ALAMOS Gateway AlarmRequest – Response Contract Tests

**Endpoint:** SOAP AlarmRequest  
**Protocol:** SOAP  
**Source:** US-ALAMOS-GW-001

### 4.1 Success Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-038 | SOAP Success | SOAP Envelope | XML | Yes | Valid SOAP envelope structure |
| CNT-039 | SOAP Success | Acknowledgment | **[Needs clarification]** | **[Needs clarification]** | Success acknowledgment from ALAMOS FE2 |

### 4.2 Error Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-040 | SOAP Fault | Fault Code | string | **[Needs clarification]** | Business or technical error indicator |
| CNT-041 | SOAP Fault | Fault String | string | **[Needs clarification]** | Error description |

---

## 5. ALAMOS REST ALARM API – Response Contract Tests

**Endpoint:** REST ALARM API  
**Direction:** ALAMOS Gateway → ALAMOS FE2  
**Source:** US-ALAMOS-GW-001

### 5.1 Success Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-042 | Success | HTTP Status Code | integer | Yes | **[Needs clarification: expected success code]** |
| CNT-043 | Success | Response Body | **[Needs clarification]** | **[Needs clarification]** | **[Needs clarification: response schema not documented]** |

### 5.2 Error Response

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-044 | Error | HTTP Status Code | integer | Yes | **[Needs clarification: error codes]** |
| CNT-045 | Error | Error Body | **[Needs clarification]** | **[Needs clarification]** | Business or technical error response |

---

## 6. Cross-Cutting Contract Validations

### 6.1 Nullable Fields Handling

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-046 | Domain Event | incident.external_id | string/null | Conditional | null allowed if incident_number present |
| CNT-047 | Domain Event | incident.incident_number | string/null | Conditional | null allowed if external_id present |
| CNT-048 | Domain Event | authoring_resource.call_sign | string/null | Conditional | **[Needs clarification: null triggers fallback?]** |

### 6.2 Array Handling (Squad Information)

| Test ID | Response Type | Field | Expected Type | Required | Validation |
|---------|---------------|-------|---------------|----------|------------|
| CNT-049 | AlarmRequest | squads | array | No | Optional squad information array |
| CNT-050 | AlarmRequest | squads[] | **[Needs clarification]** | **[Needs clarification]** | **[Needs clarification: squad element structure not documented]** |
| CNT-051 | AlarmRequest | squads.length | integer | N/A | **[Needs clarification: min/max entries not documented]** |

---

## Summary of Contract Test Coverage

| Contract | Total Tests | Fully Specified | Needs Clarification |
|----------|-------------|-----------------|---------------------|
| incident.situation_report_received/v1 | 20 | 14 | 6 |
| Adapter Situation Report Response | 10 | 0 | 10 |
| IPL erzeugeEinsatzmeldung Response | 7 | 1 | 6 |
| ALAMOS Gateway AlarmRequest Response | 4 | 1 | 3 |
| ALAMOS REST ALARM API Response | 4 | 0 | 4 |
| Cross-Cutting (Nullable/Arrays) | 6 | 2 | 4 |
| **Total** | **51** | **18** | **33** |

---

## Contract Schema Summary

### Documented Schema: incident.situation_report_received/v1

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "incident.situation_report_received/v1",
  "description": "Domain Event contract for Situation Reports - Minimum payload",
  "type": "object",
  "required": ["event_id", "event_type", "occurred_at", "source_system", "tenant_id", "incident", "authoring_resource", "situation_report"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event identifier"
    },
    "event_type": {
      "type": "string",
      "const": "incident.situation_report_received",
      "description": "Event type identifier"
    },
    "occurred_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO8601 timestamp when the event occurred"
    },
    "source_system": {
      "type": "string",
      "description": "Source system identifier (ALAMOS for this flow)"
    },
    "tenant_id": {
      "type": "string",
      "description": "Tenant identifier"
    },
    "incident": {
      "type": "object",
      "description": "Incident correlation information",
      "properties": {
        "external_id": {
          "type": "string",
          "description": "Primary external identifier for incident correlation"
        },
        "incident_number": {
          "type": "string",
          "description": "Fallback incident number for correlation"
        }
      },
      "anyOf": [
        {"required": ["external_id"]},
        {"required": ["incident_number"]}
      ]
    },
    "authoring_resource": {
      "type": "object",
      "required": ["external_resource_id"],
      "properties": {
        "external_resource_id": {
          "type": "string",
          "description": "External resource identifier"
        },
        "call_sign": {
          "type": "string",
          "description": "Resource call sign (fallback handling applied if missing)"
        }
      }
    },
    "situation_report": {
      "type": "object",
      "required": ["text", "reported_at"],
      "properties": {
        "text": {
          "type": "string",
          "description": "Situation report content"
        },
        "reported_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO8601 timestamp when the report was created"
        }
      }
    }
  }
}
```

**Note:** This schema is inferred from the documented minimum payload. The actual contract may include additional fields. Full schema reference at `incident.situation_report_received/v1` is mentioned but not provided in source documents.

---

## Items Requiring Clarification for Contract Testing

| Category | Gap | Impact |
|----------|-----|--------|
| Response Schemas | Success/error response structures not documented for any endpoint | Cannot verify response schema compliance |
| HTTP Status Codes | Expected status codes not documented | Cannot verify correct status code usage |
| SOAP Fault Codes | IPL and ALAMOS SOAP fault codes not documented | Cannot verify fault code compliance |
| Error Response Format | Error response body structure not documented | Cannot verify error response schema |
| Squad Element Schema | Structure of individual squad entries not documented | Cannot verify squad array element compliance |
| Strict vs Lenient | Unknown if schemas are strict (reject unknown fields) or lenient | Cannot verify unknown field handling |
| Full Contract Reference | Referenced contract `incident.situation_report_received/v1` not included | Only minimum payload documented |
| WSDL/OpenAPI | No WSDL or OpenAPI specifications available | Cannot generate comprehensive contract tests |

---

## Recommendations

1. **Obtain Full Contract Specifications:**
   - Request OpenAPI/Swagger specifications for REST endpoints
   - Request WSDL definitions for SOAP endpoints
   - Request full `incident.situation_report_received/v1` contract schema

2. **Document Response Schemas:**
   - Define success response structure for all endpoints
   - Define error response structure with error codes and messages

3. **Define Status Codes:**
   - Document expected HTTP status codes for all scenarios
   - Document SOAP fault codes for all error conditions

4. **Specify Squad Structure:**
   - Document the structure of squad elements within `<squads>` array
   - Define required/optional fields within each squad entry

5. **Clarify Schema Strictness:**
   - Define whether schemas should reject unknown fields (strict) or ignore them (lenient)
