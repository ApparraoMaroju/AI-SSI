# ALAMOS Integration – Release 26.3 API Validation Tests

**Generated:** 2026-07-23 14:30:00  
**Source:** ALAMOS_Feature_Context.md, ALAMOS_Project_Context.md, ALAMOS_Testing_Context.md  
**Template:** API02-API Validation Tests.md

---

## Notes

- All validation tests are derived exclusively from the documented validation rules and API specifications.
- Items marked **[Needs clarification]** indicate missing or undocumented specifications.
- Specific error codes and messages are NOT documented in source files; placeholders indicate expected error categories only.
- Field constraints, data types, and format requirements are partially documented; gaps are explicitly noted.

---

## API Endpoints Covered

| # | API | Protocol | Direction | Source |
|---|-----|----------|-----------|--------|
| 1 | Adapter Situation Report Endpoint | REST | ALAMOS FE2 → Adapter | US-ADAPTER-ALAMOS-001 |
| 2 | IPL erzeugeEinsatzmeldung | SOAP POST | FacadeService → IPL | US-ADAPTER-ALAMOS-004 |
| 3 | ALAMOS Gateway AlarmRequest | SOAP | IPL → Gateway | US-ALAMOS-GW-001, US-ALAMOS-GW-003 |
| 4 | ALAMOS Gateway REST ALARM API | REST | Gateway → ALAMOS FE2 | US-ALAMOS-GW-001 |

---

## 1. Adapter Situation Report Endpoint – Input Validation Tests

**Endpoint:** REST (exact method/path not specified)  
**Direction:** ALAMOS FE2 → Adapter  
**Source:** US-ADAPTER-ALAMOS-001, ALAMOS Integration – Phase 1.md

### 1.1 Required Fields

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-001 | HTTP Method | GET (unsupported) | **[Needs clarification]** | Technical error: unsupported HTTP method |
| API-VAL-002 | HTTP Method | PUT (unsupported) | **[Needs clarification]** | Technical error: unsupported HTTP method |
| API-VAL-003 | HTTP Method | DELETE (unsupported) | **[Needs clarification]** | Technical error: unsupported HTTP method |
| API-VAL-004 | Content-Type | application/xml (if invalid) | **[Needs clarification]** | Technical error: invalid content type |
| API-VAL-005 | Content-Type | text/plain | **[Needs clarification]** | Technical error: invalid content type |
| API-VAL-006 | Content-Type | Missing/empty | **[Needs clarification]** | Technical error: invalid content type |
| API-VAL-007 | Request Headers | Missing required headers | **[Needs clarification]** | Technical error: invalid headers |
| API-VAL-008 | Authentication | Missing authentication | **[Needs clarification]** | Technical error: invalid authentication |
| API-VAL-009 | Authentication | Invalid authentication credentials | **[Needs clarification]** | Technical error: invalid authentication |
| API-VAL-010 | Request Body | Missing (null/empty body) | **[Needs clarification]** | Validation error: payload required |
| API-VAL-011 | Request Body | Malformed JSON/payload | **[Needs clarification]** | Validation error: malformed payload |
| API-VAL-012 | ALAMOS Contract | Non-compliant payload structure | **[Needs clarification]** | Validation error: contract violation |

### 1.2 Situation Report Payload Fields (from Domain Event Contract)

Based on the documented minimum payload structure for `incident.situation_report_received/v1`:

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-013 | event_id | Missing | **[Needs clarification]** | Missing mandatory field: event_id |
| API-VAL-014 | event_id | Empty string | **[Needs clarification]** | Invalid format: event_id must be UUID |
| API-VAL-015 | event_id | Non-UUID format | **[Needs clarification]** | Invalid format: event_id must be UUID |
| API-VAL-016 | event_type | Missing | **[Needs clarification]** | Missing mandatory field: event_type |
| API-VAL-017 | event_type | Empty string | **[Needs clarification]** | Invalid value: event_type |
| API-VAL-018 | event_type | Invalid value (not "incident.situation_report_received") | **[Needs clarification]** | Invalid value: event_type |
| API-VAL-019 | occurred_at | Missing | **[Needs clarification]** | Missing mandatory field: occurred_at |
| API-VAL-020 | occurred_at | Invalid date format | **[Needs clarification]** | Invalid format: occurred_at must be ISO8601 |
| API-VAL-021 | occurred_at | Empty string | **[Needs clarification]** | Invalid format: occurred_at |
| API-VAL-022 | source_system | Missing | **[Needs clarification]** | Missing mandatory field: source_system |
| API-VAL-023 | source_system | Empty string | **[Needs clarification]** | Invalid value: source_system |
| API-VAL-024 | tenant_id | Missing | **[Needs clarification]** | Missing mandatory field: tenant_id |
| API-VAL-025 | tenant_id | Empty string | **[Needs clarification]** | Invalid value: tenant_id |
| API-VAL-026 | incident | Missing entire object | **[Needs clarification]** | Missing mandatory field: incident |
| API-VAL-027 | incident.external_id | Both external_id and incident_number missing | **[Needs clarification]** | Correlation failed: external_id or incident_number required |
| API-VAL-028 | incident.external_id | Empty string (with no incident_number) | **[Needs clarification]** | Correlation failed |
| API-VAL-029 | authoring_resource | Missing entire object | **[Needs clarification]** | Missing mandatory field: authoring_resource |
| API-VAL-030 | authoring_resource.external_resource_id | Missing | **[Needs clarification]** | Missing mandatory field: external_resource_id |
| API-VAL-031 | authoring_resource.external_resource_id | Empty string | **[Needs clarification]** | Invalid value: external_resource_id |
| API-VAL-032 | authoring_resource.call_sign | Missing | **[Needs clarification: fallback behavior expected]** | Fallback handling applied |
| API-VAL-033 | authoring_resource.call_sign | Empty string | **[Needs clarification: fallback behavior expected]** | Fallback handling applied |
| API-VAL-034 | situation_report | Missing entire object | **[Needs clarification]** | Missing mandatory field: situation_report |
| API-VAL-035 | situation_report.text | Missing | **[Needs clarification]** | Missing mandatory field: situation_report.text |
| API-VAL-036 | situation_report.text | Empty string | **[Needs clarification]** | Invalid value: situation_report.text (or accepted?) |
| API-VAL-037 | situation_report.reported_at | Missing | **[Needs clarification]** | Missing mandatory field: reported_at |
| API-VAL-038 | situation_report.reported_at | Invalid date format | **[Needs clarification]** | Invalid format: reported_at must be ISO8601 |

### 1.3 Boundary Values

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-039 | event_id | UUID with leading/trailing spaces | **[Needs clarification]** | **[Needs clarification: trim behavior]** |
| API-VAL-040 | situation_report.text | Maximum length exceeded | **[Needs clarification]** | **[Needs clarification: max length not documented]** |
| API-VAL-041 | tenant_id | Maximum length exceeded | **[Needs clarification]** | **[Needs clarification: max length not documented]** |
| API-VAL-042 | incident.external_id | Maximum length exceeded | **[Needs clarification]** | **[Needs clarification: max length not documented]** |
| API-VAL-043 | authoring_resource.call_sign | Maximum length exceeded | **[Needs clarification]** | **[Needs clarification: max length not documented]** |

### 1.4 Special Characters

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-044 | situation_report.text | Special characters (emoji, unicode) | **[Needs clarification]** | **[Needs clarification: encoding/character support not documented]** |
| API-VAL-045 | situation_report.text | SQL injection pattern | **[Needs clarification]** | **[Needs clarification: sanitization behavior not documented]** |
| API-VAL-046 | situation_report.text | Script injection pattern | **[Needs clarification]** | **[Needs clarification: sanitization behavior not documented]** |
| API-VAL-047 | tenant_id | Special characters | **[Needs clarification]** | **[Needs clarification: allowed character set not documented]** |

---

## 2. IPL erzeugeEinsatzmeldung Endpoint – Input Validation Tests

**Endpoint:** POST /einsatztransfer/erzeugeEinsatzmeldung  
**Protocol:** SOAP  
**Direction:** FacadeService → IPL  
**Source:** US-ADAPTER-ALAMOS-004

### 2.1 Request Validation (FacadeService to IPL)

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-048 | Request payload | Missing required data for IPL request generation | **[Needs clarification]** | Event not submitted to IPL; error returned |
| API-VAL-049 | Request payload | Invalid mapping from Domain Event | **[Needs clarification]** | Mapping failure error |
| API-VAL-050 | SOAP envelope | Malformed SOAP structure | **[Needs clarification]** | Technical fault |
| API-VAL-051 | Endpoint | IPL endpoint unavailable | **[Needs clarification]** | Communication failure |
| API-VAL-052 | Endpoint | IPL endpoint timeout | **[Needs clarification]** | Timeout error |

### 2.2 IPL Response Handling

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-053 | IPL Response | Business fault response | **[IPL business fault]** | Business fault propagated to ALAMOS FE2 |
| API-VAL-054 | IPL Response | Technical fault response | **[IPL technical fault]** | Technical fault propagated to ALAMOS FE2 |

---

## 3. ALAMOS Gateway AlarmRequest – Input Validation Tests

**Endpoint:** SOAP AlarmRequest  
**Direction:** IPL → ALAMOS Gateway  
**Source:** US-ALAMOS-GW-001, US-ALAMOS-GW-003

### 3.1 AlarmRequest Validation

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-055 | AlarmRequest | Missing entire request | **[Needs clarification]** | Invalid/malformed request rejected |
| API-VAL-056 | AlarmRequest | Malformed SOAP structure | **[Needs clarification]** | Invalid/malformed request rejected |
| API-VAL-057 | AlarmRequest | Empty SOAP body | **[Needs clarification]** | Invalid/malformed request rejected |

### 3.2 Squad Information (`<squads>`) Validation

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-058 | `<squads>` | Empty squads element | **[Needs clarification]** | **[Needs clarification: expected behavior not documented]** |
| API-VAL-059 | `<squads>` | Malformed squads structure | **[Needs clarification]** | Validation error |
| API-VAL-060 | `<squads>` | Invalid squad entry data | **[Needs clarification]** | **[Needs clarification: squad field constraints not documented]** |
| API-VAL-061 | `<squads>` | Missing squads (backward compatibility) | N/A (valid) | Request processed successfully (backward compatibility) |

---

## 4. ALAMOS Gateway REST ALARM API – Input Validation Tests

**Endpoint:** REST ALARM API  
**Direction:** ALAMOS Gateway → ALAMOS FE2  
**Source:** US-ALAMOS-GW-001

### 4.1 Outbound Request Validation

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-062 | Endpoint | ALAMOS FE2 unavailable | **[Needs clarification]** | Communication failure |
| API-VAL-063 | Endpoint | ALAMOS FE2 timeout | **[Needs clarification]** | Communication timeout |

### 4.2 ALAMOS FE2 Response Handling

| Test ID | Field | Invalid Input | Expected Error Code | Expected Message |
|---------|-------|---------------|---------------------|------------------|
| API-VAL-064 | Response | ALAMOS FE2 business error | **[ALAMOS business error]** | Business error propagated to IPL |
| API-VAL-065 | Response | ALAMOS FE2 technical error | **[ALAMOS technical error]** | Technical error propagated to IPL |

---

## Summary of Validation Test Coverage

| API Endpoint | Total Tests | Fully Specified | Needs Clarification |
|--------------|-------------|-----------------|---------------------|
| Adapter Situation Report | 47 | 0 | 47 |
| IPL erzeugeEinsatzmeldung | 7 | 0 | 7 |
| ALAMOS Gateway AlarmRequest | 7 | 1 | 6 |
| ALAMOS Gateway REST ALARM API | 4 | 0 | 4 |
| **Total** | **65** | **1** | **64** |

---

## Items Requiring Clarification for API Validation

| Category | Gap | Impact |
|----------|-----|--------|
| Error Codes | No error codes documented for any API | Cannot verify specific error code responses |
| Error Messages | No error message text documented | Cannot verify specific error message content |
| Field Constraints | No min/max length, format patterns, or character restrictions documented | Cannot perform comprehensive boundary testing |
| HTTP Methods | Supported HTTP methods for Adapter endpoint not specified | Cannot confirm which methods should be rejected |
| Content Types | Valid content types for Adapter endpoint not specified | Cannot confirm which content types should be accepted/rejected |
| Authentication | Authentication mechanism/requirements not specified | Cannot design specific authentication validation tests |
| Squad Field Structure | Structure and constraints of squad entries not documented | Cannot validate individual squad fields |
| Fallback Behavior | call_sign fallback logic not detailed | Cannot verify specific fallback behavior |
| Sanitization | Input sanitization/encoding behavior not documented | Cannot verify security-related validation |

---

## Recommendations

1. **Obtain API Specifications:** Request OpenAPI/Swagger specifications or WSDL definitions for all endpoints.
2. **Document Error Codes:** Request comprehensive error code documentation for all validation scenarios.
3. **Define Field Constraints:** Request field-level constraints (required, length limits, formats, allowed characters).
4. **Clarify Authentication:** Document authentication requirements and error responses.
5. **Define Squad Structure:** Document the structure and validation rules for squad information.
