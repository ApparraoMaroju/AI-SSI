# Story: ALAMOS Phase 1 – Extend Alerting With Squad Information

| Field | Value |
|--------|-------|
| **Story ID** | US-ALAMOS-GW-003 |
| **Story Name** | ALAMOS Phase 1 – Extend Alerting With Squad Information |
| **Actor** | ALAMOS Gateway |
| **Goal** | Process and forward squad information during alerting |
| **Business Value** | Enables ALAMOS to receive complete alerting information, including assigned squad data, while preserving the existing Alerting integration path and maintaining backward compatibility with current IPL and ALAMOS Gateway implementations. |
| **Jira Ticket** | IPL-26936 – Extend Existing ALAMOS Gateway to Process `<squads>` Information *(Open)* |

---

## User Story

**As** an ALAMOS Gateway,  
**I want** to process squad information included in Alerting requests,  
**So that** ALAMOS receives complete alerting messages containing both alarm details and associated squad information.

---

## Key Scenarios & Variations

### Squad Information Processing
1. Alerting request contains valid squad information.
2. Alerting request does not contain squad information.
3. Multiple squads are supplied within a single alerting request.
4. Squad information is successfully mapped to the ALAMOS request format.

### Alerting Integration
5. Alerting request is successfully forwarded to ALAMOS FE2.
6. ALAMOS FE2 returns a successful acknowledgement.
7. ALAMOS FE2 returns a business or technical error.

### Backward Compatibility
8. Existing Alerting requests continue to function when no squad information is present.

---

## Acceptance Criteria

### Squad Information Handling
1. The ALAMOS Gateway shall support processing of squad information included in Alerting requests.
2. Squad information shall be extracted from the IPL Alerting request and mapped to the ALAMOS message structure.
3. Multiple squad entries shall be supported where provided by IPL.

### Backward Compatibility
4. Alerting requests without squad information shall continue to be processed successfully.
5. Existing Alerting functionality shall remain backward compatible.

### ALAMOS Integration
6. The ALAMOS Gateway shall forward the enriched Alerting request to ALAMOS FE2 using the existing integration path.
7. Success, business fault, and technical fault responses returned by ALAMOS FE2 shall be processed correctly.

### Response Handling & Validation
8. Acknowledgements shall be propagated back to IPL without loss of information.
9. End-to-end testing shall verify that squad information is correctly transmitted to ALAMOS FE2.