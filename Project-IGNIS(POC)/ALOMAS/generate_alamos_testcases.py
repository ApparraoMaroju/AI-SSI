"""
ALAMOS Integration - Functional Integration Test Cases Generator
Generates 50 comprehensive test cases based on PRD and Testing Context
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

def create_test_cases_workbook():
    """Generate Excel workbook with 50 functional integration test cases"""
    
    # Create workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    
    # Define columns
    columns = [
        "TID", "Test Case Name", "Category", "Description", "Pre-conditions",
        "Step No", "Step Description", "Expected Result", "Priority", "User Story Reference"
    ]
    
    # Write header row
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    # Freeze header row
    ws.freeze_panes = 'A2'
    
    # Define all 50 test cases
    test_cases = [
        # ============================================================================
        # SITUATION REPORTS - Adapter Receive & Validate (US-ADAPTER-ALAMOS-001)
        # ============================================================================
        {
            "tid": "TC-001",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter receives valid Situation Report from ALAMOS FE2",
            "category": "Functional (Happy Path)",
            "description": "Validate that the Adapter successfully receives and accepts a valid Situation Report from ALAMOS FE2 with all mandatory fields populated correctly.",
            "preconditions": "1. Adapter REST endpoint is available\n2. ALAMOS FE2 is configured and connected\n3. Valid authentication credentials are available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Prepare a valid Situation Report payload with all mandatory fields (external_id, incident_number, call_sign, situation_report.text, reported_at)", "Payload is correctly structured per ALAMOS contract"),
                ("2", "Send the Situation Report to the Adapter REST endpoint with valid headers and authentication", "Request is received by the Adapter"),
                ("3", "Verify the Adapter validates the payload against the ALAMOS contract", "Payload validation passes without errors"),
                ("4", "Verify the Adapter accepts the request for downstream processing", "Situation Report is accepted and forwarded for processing"),
                ("5", "Verify the Adapter returns a synchronous success acknowledgment", "HTTP 200 response with success acknowledgment is returned to ALAMOS FE2")
            ]
        },
        {
            "tid": "TC-002",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter rejects Situation Report with missing mandatory fields",
            "category": "Negative Scenario",
            "description": "Validate that the Adapter rejects a Situation Report when mandatory fields are missing and returns appropriate validation error.",
            "preconditions": "1. Adapter REST endpoint is available\n2. Valid authentication credentials are available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Prepare a Situation Report payload with external_id field missing", "Incomplete payload is prepared"),
                ("2", "Send the invalid Situation Report to the Adapter REST endpoint", "Request is received by the Adapter"),
                ("3", "Verify the Adapter performs initial payload validation", "Adapter detects missing mandatory field"),
                ("4", "Verify the Adapter returns a clear validation error response", "HTTP 400 response with validation error message indicating missing external_id is returned")
            ]
        },
        {
            "tid": "TC-003",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter rejects request with unsupported HTTP method",
            "category": "Negative Scenario",
            "description": "Validate that the Adapter rejects requests using unsupported HTTP methods with appropriate technical error response.",
            "preconditions": "1. Adapter REST endpoint is available",
            "priority": "Medium",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Prepare a valid Situation Report payload", "Valid payload is prepared"),
                ("2", "Send the request using GET method instead of POST", "Request is sent with unsupported HTTP method"),
                ("3", "Verify the Adapter rejects the request", "Adapter identifies unsupported method"),
                ("4", "Verify appropriate technical error response is returned", "HTTP 405 Method Not Allowed response is returned")
            ]
        },
        {
            "tid": "TC-004",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter rejects request with invalid Content-Type",
            "category": "Negative Scenario",
            "description": "Validate that the Adapter rejects requests with invalid content type header.",
            "preconditions": "1. Adapter REST endpoint is available",
            "priority": "Medium",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Prepare a valid Situation Report payload", "Valid payload is prepared"),
                ("2", "Send the request with Content-Type: text/plain instead of application/json", "Request is sent with invalid content type"),
                ("3", "Verify the Adapter rejects the request", "Adapter identifies invalid content type"),
                ("4", "Verify appropriate technical error response is returned", "HTTP 415 Unsupported Media Type response is returned")
            ]
        },
        {
            "tid": "TC-005",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter rejects request with invalid authentication",
            "category": "Negative Scenario",
            "description": "Validate that the Adapter rejects requests with invalid or missing authentication credentials.",
            "preconditions": "1. Adapter REST endpoint is available\n2. Authentication mechanism is enabled",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Prepare a valid Situation Report payload", "Valid payload is prepared"),
                ("2", "Send the request without authentication headers", "Request is sent without credentials"),
                ("3", "Verify the Adapter rejects the request before processing", "Adapter identifies missing authentication"),
                ("4", "Verify appropriate authentication error response is returned", "HTTP 401 Unauthorized response is returned")
            ]
        },
        {
            "tid": "TC-006",
            "name": "[US-ADAPTER-ALAMOS-001] Verify Adapter returns failure acknowledgment when IPL processing fails",
            "category": "Negative Scenario",
            "description": "Validate that the Adapter returns synchronous failure acknowledgment when downstream IPL processing fails.",
            "preconditions": "1. Adapter REST endpoint is available\n2. IPL endpoint is configured to return a fault response",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-001",
            "steps": [
                ("1", "Configure IPL endpoint to return a business fault for the test scenario", "IPL mock/stub is configured to return fault"),
                ("2", "Send a valid Situation Report to the Adapter", "Request is received and validated by Adapter"),
                ("3", "Verify the Adapter forwards the request and waits for IPL response", "Adapter processes the request synchronously"),
                ("4", "Verify the Adapter receives the fault response from IPL", "Fault response is received from IPL"),
                ("5", "Verify the Adapter returns synchronous failure acknowledgment to ALAMOS FE2", "HTTP response with failure acknowledgment accurately reflecting IPL fault is returned")
            ]
        },
        # ============================================================================
        # SITUATION REPORTS - Domain Event Generation (US-ADAPTER-ALAMOS-002)
        # ============================================================================
        {
            "tid": "TC-007",
            "name": "[US-ADAPTER-ALAMOS-002] Verify Domain Event generation with external_id correlation",
            "category": "Functional (Happy Path)",
            "description": "Validate that the Adapter transforms a validated Situation Report into the canonical Domain Event using external_id for incident correlation.",
            "preconditions": "1. Adapter is running\n2. Valid Situation Report with external_id is available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-002",
            "steps": [
                ("1", "Submit a valid Situation Report with external_id populated", "Situation Report is received and validated"),
                ("2", "Verify the Adapter creates incident.situation_report_received/v1 Domain Event", "Domain Event is created with correct event_type"),
                ("3", "Verify incident correlation uses external_id from the payload", "incident.external_id in Domain Event matches the submitted external_id"),
                ("4", "Verify all required Domain Event attributes are populated", "event_id, occurred_at, source_system, tenant_id, authoring_resource, situation_report fields are present"),
                ("5", "Verify the Domain Event is validated prior to downstream processing", "Domain Event passes contract validation")
            ]
        },
        {
            "tid": "TC-008",
            "name": "[US-ADAPTER-ALAMOS-002] Verify Domain Event uses incident_number fallback when external_id unavailable",
            "category": "Alternate Flow",
            "description": "Validate that incident correlation falls back to incident_number when external_id is not available.",
            "preconditions": "1. Adapter is running\n2. Valid Situation Report without external_id but with incident_number is available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-002",
            "steps": [
                ("1", "Submit a valid Situation Report with external_id empty/null and incident_number populated", "Situation Report is received and validated"),
                ("2", "Verify the Adapter identifies external_id is unavailable", "Adapter detects missing external_id"),
                ("3", "Verify incident correlation uses incident_number as fallback", "incident.incident_number in Domain Event is used for correlation"),
                ("4", "Verify the Domain Event is created successfully with incident_number", "Domain Event contains correct incident correlation data"),
                ("5", "Verify processing continues without error", "Domain Event is forwarded for downstream processing")
            ]
        },
        {
            "tid": "TC-009",
            "name": "[US-ADAPTER-ALAMOS-002] Verify call_sign fallback handling when call_sign is missing",
            "category": "Edge Case",
            "description": "Validate that the Adapter applies call_sign fallback handling when a reporting resource does not provide a valid call_sign.",
            "preconditions": "1. Adapter is running\n2. Situation Report with missing call_sign is available",
            "priority": "Medium",
            "user_story": "US-ADAPTER-ALAMOS-002",
            "steps": [
                ("1", "Submit a valid Situation Report with call_sign field empty or missing", "Situation Report is received by Adapter"),
                ("2", "Verify the Adapter detects missing call_sign", "Adapter identifies call_sign is not provided"),
                ("3", "Verify the Adapter applies fallback handling for call_sign", "Fallback logic is executed"),
                ("4", "Verify the Domain Event is created with appropriate authoring_resource mapping", "authoring_resource.call_sign uses fallback value"),
                ("5", "Verify processing continues successfully", "Domain Event is generated without error")
            ]
        },
        {
            "tid": "TC-010",
            "name": "[US-ADAPTER-ALAMOS-002] Verify error returned when incident correlation cannot be completed",
            "category": "Negative Scenario",
            "description": "Validate that an appropriate error is returned when both external_id and incident_number are missing and incident correlation cannot be completed.",
            "preconditions": "1. Adapter is running",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-002",
            "steps": [
                ("1", "Submit a Situation Report with both external_id and incident_number missing/empty", "Situation Report is received by Adapter"),
                ("2", "Verify the Adapter attempts incident correlation", "Adapter checks for external_id and incident_number"),
                ("3", "Verify the Adapter cannot complete incident correlation", "Both correlation keys are unavailable"),
                ("4", "Verify an appropriate error is returned", "Error response indicating incident correlation failure is returned to ALAMOS FE2")
            ]
        },
        {
            "tid": "TC-011",
            "name": "[US-ADAPTER-ALAMOS-002] Verify Domain Event contains all required attributes per contract",
            "category": "Functional (Happy Path)",
            "description": "Validate that the generated Domain Event contains all mandatory attributes as per the incident.situation_report_received/v1 contract.",
            "preconditions": "1. Adapter is running\n2. Complete valid Situation Report is available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-002",
            "steps": [
                ("1", "Submit a complete valid Situation Report with all fields populated", "Situation Report is received and validated"),
                ("2", "Capture the generated Domain Event", "Domain Event incident.situation_report_received/v1 is created"),
                ("3", "Verify event_id is a valid UUID", "event_id field is present and contains valid UUID"),
                ("4", "Verify event_type equals 'incident.situation_report_received'", "event_type field is correct"),
                ("5", "Verify occurred_at contains valid ISO 8601 timestamp", "occurred_at field is properly formatted"),
                ("6", "Verify source_system equals 'ALAMOS'", "source_system field is correct"),
                ("7", "Verify tenant_id, incident, authoring_resource, and situation_report objects are present", "All required objects are populated in Domain Event")
            ]
        },
        # ============================================================================
        # FACADESERVICE - Routing Layer (US-ADAPTER-ALAMOS-003)
        # ============================================================================
        {
            "tid": "TC-012",
            "name": "[US-ADAPTER-ALAMOS-003] Verify FacadeService routes Domain Event through EVENT processing path",
            "category": "Functional (Happy Path)",
            "description": "Validate that the FacadeService correctly routes incident.situation_report_received Domain Events through the EVENT processing path.",
            "preconditions": "1. Adapter and FacadeService are running\n2. Routing configuration for EVENT path is enabled",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-003",
            "steps": [
                ("1", "Generate a valid incident.situation_report_received Domain Event", "Domain Event is created by Adapter"),
                ("2", "Verify FacadeService receives the Domain Event", "FacadeService receives the event"),
                ("3", "Verify FacadeService determines EVENT processing path", "Routing configuration resolves to EVENT path"),
                ("4", "Verify the Domain Event is processed through the EVENT path", "Processing continues through correct path"),
                ("5", "Verify FacadeService returns the processing result to the Adapter", "Result is propagated back")
            ]
        },
        {
            "tid": "TC-013",
            "name": "[US-ADAPTER-ALAMOS-003] Verify FacadeService propagates success response to Adapter",
            "category": "Functional (Happy Path)",
            "description": "Validate that the FacadeService propagates successful processing result back to the Adapter after IPL processing completes.",
            "preconditions": "1. Adapter and FacadeService are running\n2. IPL endpoint is available and returns success",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-003",
            "steps": [
                ("1", "Submit a valid Situation Report that generates a Domain Event", "Domain Event is created"),
                ("2", "Verify FacadeService routes to IPL processing", "Request is routed correctly"),
                ("3", "Verify IPL returns success response", "IPL processing completes successfully"),
                ("4", "Verify FacadeService receives success response from IPL", "Success response is received"),
                ("5", "Verify FacadeService propagates success response to Adapter", "Adapter receives success indication"),
                ("6", "Verify Adapter returns success acknowledgment to ALAMOS FE2", "End-to-end success flow is complete")
            ]
        },
        {
            "tid": "TC-014",
            "name": "[US-ADAPTER-ALAMOS-003] Verify FacadeService propagates failure response to Adapter",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService propagates failure response back to the Adapter when IPL processing fails.",
            "preconditions": "1. Adapter and FacadeService are running\n2. IPL endpoint is configured to return failure",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-003",
            "steps": [
                ("1", "Configure IPL to return a business fault", "IPL mock is configured for failure"),
                ("2", "Submit a valid Situation Report that generates a Domain Event", "Domain Event is created"),
                ("3", "Verify FacadeService routes to IPL processing", "Request is routed correctly"),
                ("4", "Verify IPL returns fault response", "IPL returns business fault"),
                ("5", "Verify FacadeService receives fault response from IPL", "Fault response is received"),
                ("6", "Verify FacadeService propagates failure response to Adapter", "Adapter receives failure indication"),
                ("7", "Verify Adapter returns failure acknowledgment to ALAMOS FE2", "Failure is correctly communicated")
            ]
        },
        {
            "tid": "TC-015",
            "name": "[US-ADAPTER-ALAMOS-003] Verify FacadeService handles invalid routing configuration",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService returns error when routing configuration is invalid or capability is unsupported.",
            "preconditions": "1. Adapter and FacadeService are running\n2. Invalid routing configuration is set",
            "priority": "Medium",
            "user_story": "US-ADAPTER-ALAMOS-003",
            "steps": [
                ("1", "Configure FacadeService with invalid routing for Situation Report capability", "Invalid configuration is applied"),
                ("2", "Submit a valid Situation Report", "Request is received by Adapter"),
                ("3", "Verify FacadeService attempts to determine processing path", "Routing logic is executed"),
                ("4", "Verify FacadeService cannot resolve to valid processing path", "Invalid configuration is detected"),
                ("5", "Verify error response is returned indicating routing failure", "Error is propagated back to Adapter and ALAMOS FE2")
            ]
        },
        # ============================================================================
        # FACADESERVICE - IPL Processing (US-ADAPTER-ALAMOS-004)
        # ============================================================================
        {
            "tid": "TC-016",
            "name": "[US-ADAPTER-ALAMOS-004] Verify FacadeService invokes IPL erzeugeEinsatzmeldung endpoint successfully",
            "category": "Functional (Happy Path)",
            "description": "Validate that the FacadeService successfully transforms Domain Event to IPL request and invokes the IPL SOAP endpoint.",
            "preconditions": "1. FacadeService is running\n2. IPL endpoint POST /einsatztransfer/erzeugeEinsatzmeldung is available",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-004",
            "steps": [
                ("1", "Generate incident.situation_report_received Domain Event with all required data", "Valid Domain Event is created"),
                ("2", "Verify FacadeService receives the Domain Event", "FacadeService receives the event"),
                ("3", "Verify FacadeService validates all required data for IPL request generation", "Validation passes"),
                ("4", "Verify FacadeService maps Domain Event data to IPL request structure", "Request mapping is performed"),
                ("5", "Verify FacadeService invokes POST /einsatztransfer/erzeugeEinsatzmeldung synchronously", "SOAP request is sent to IPL"),
                ("6", "Verify IPL returns success response", "IPL processing completes successfully"),
                ("7", "Verify success result is propagated back to ALAMOS FE2", "Success acknowledgment is returned")
            ]
        },
        {
            "tid": "TC-017",
            "name": "[US-ADAPTER-ALAMOS-004] Verify FacadeService handles IPL business fault response",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService correctly processes business fault responses returned by IPL.",
            "preconditions": "1. FacadeService is running\n2. IPL endpoint is configured to return business fault",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-004",
            "steps": [
                ("1", "Configure IPL to return a business fault for the Situation Report", "IPL mock configured for business fault"),
                ("2", "Submit a valid Situation Report through the Adapter", "Domain Event is created and routed"),
                ("3", "Verify FacadeService invokes IPL endpoint", "SOAP request is sent"),
                ("4", "Verify IPL returns business fault response", "Business fault is received"),
                ("5", "Verify FacadeService processes the business fault", "Fault is handled appropriately"),
                ("6", "Verify business fault is propagated to ALAMOS FE2", "Failure acknowledgment with business fault details is returned")
            ]
        },
        {
            "tid": "TC-018",
            "name": "[US-ADAPTER-ALAMOS-004] Verify FacadeService handles IPL technical fault response",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService correctly processes technical fault responses returned by IPL.",
            "preconditions": "1. FacadeService is running\n2. IPL endpoint is configured to return technical fault",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-004",
            "steps": [
                ("1", "Configure IPL to return a technical fault (e.g., internal server error)", "IPL mock configured for technical fault"),
                ("2", "Submit a valid Situation Report through the Adapter", "Domain Event is created and routed"),
                ("3", "Verify FacadeService invokes IPL endpoint", "SOAP request is sent"),
                ("4", "Verify IPL returns technical fault response", "Technical fault is received"),
                ("5", "Verify FacadeService processes the technical fault", "Fault is handled appropriately"),
                ("6", "Verify technical fault is propagated to ALAMOS FE2", "Failure acknowledgment with technical error is returned")
            ]
        },
        {
            "tid": "TC-019",
            "name": "[US-ADAPTER-ALAMOS-004] Verify FacadeService handles IPL endpoint unavailable",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService handles communication failure when IPL endpoint is unavailable.",
            "preconditions": "1. FacadeService is running\n2. IPL endpoint is stopped/unavailable",
            "priority": "High",
            "user_story": "US-ADAPTER-ALAMOS-004",
            "steps": [
                ("1", "Stop or make IPL endpoint unavailable", "IPL endpoint is not reachable"),
                ("2", "Submit a valid Situation Report through the Adapter", "Domain Event is created and routed"),
                ("3", "Verify FacadeService attempts to invoke IPL endpoint", "Connection attempt is made"),
                ("4", "Verify FacadeService detects connectivity failure", "Connection refused or unreachable error"),
                ("5", "Verify communication failure is handled gracefully", "Error is logged and processed"),
                ("6", "Verify failure is propagated to ALAMOS FE2", "Failure acknowledgment indicating IPL unavailable is returned")
            ]
        },
        {
            "tid": "TC-020",
            "name": "[US-ADAPTER-ALAMOS-004] Verify FacadeService handles IPL timeout",
            "category": "Negative Scenario",
            "description": "Validate that the FacadeService handles timeout scenarios when IPL does not respond within configured timeout.",
            "preconditions": "1. FacadeService is running\n2. IPL endpoint is configured to delay response beyond timeout",
            "priority": "Medium",
            "user_story": "US-ADAPTER-ALAMOS-004",
            "steps": [
                ("1", "Configure IPL to delay response beyond FacadeService timeout threshold", "IPL mock configured with delay"),
                ("2", "Submit a valid Situation Report through the Adapter", "Domain Event is created and routed"),
                ("3", "Verify FacadeService invokes IPL endpoint", "SOAP request is sent"),
                ("4", "Verify FacadeService timeout is triggered before IPL responds", "Timeout occurs"),
                ("5", "Verify timeout is handled as communication failure", "Timeout error is processed"),
                ("6", "Verify timeout failure is propagated to ALAMOS FE2", "Failure acknowledgment indicating timeout is returned")
            ]
        },
        # ============================================================================
        # ALAMOS GATEWAY - Legacy Alerting (US-ALAMOS-GW-001)
        # ============================================================================
        {
            "tid": "TC-021",
            "name": "[US-ALAMOS-GW-001] Verify Gateway receives and processes valid Alerting request from IPL",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway successfully receives and processes an Alerting request from IPL using the existing integration path.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL is configured\n3. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-001",
            "steps": [
                ("1", "IPL sends a valid SOAP AlarmRequest to the ALAMOS Gateway", "AlarmRequest is transmitted"),
                ("2", "Verify ALAMOS Gateway receives the request", "Gateway receives and parses AlarmRequest"),
                ("3", "Verify Gateway transforms request to ALAMOS format", "Request is mapped to REST Alarm API format"),
                ("4", "Verify Gateway forwards request to ALAMOS FE2", "REST Alarm API call is made to ALAMOS FE2"),
                ("5", "Verify ALAMOS FE2 returns success acknowledgment", "Success response is received"),
                ("6", "Verify Gateway propagates success back to IPL", "SOAP response indicating success is returned to IPL")
            ]
        },
        {
            "tid": "TC-022",
            "name": "[US-ALAMOS-GW-001] Verify Gateway handles ALAMOS FE2 business error for Alerting",
            "category": "Negative Scenario",
            "description": "Validate that the ALAMOS Gateway correctly processes business error returned by ALAMOS FE2.",
            "preconditions": "1. ALAMOS Gateway is running\n2. ALAMOS FE2 is configured to return business error",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-001",
            "steps": [
                ("1", "Configure ALAMOS FE2 to return a business error response", "FE2 mock configured for business error"),
                ("2", "IPL sends a valid AlarmRequest to the Gateway", "AlarmRequest is transmitted"),
                ("3", "Verify Gateway forwards request to ALAMOS FE2", "REST Alarm API call is made"),
                ("4", "Verify ALAMOS FE2 returns business error", "Business error response is received"),
                ("5", "Verify Gateway processes the business error", "Error is handled appropriately"),
                ("6", "Verify Gateway propagates business error back to IPL", "SOAP response with business error is returned to IPL")
            ]
        },
        {
            "tid": "TC-023",
            "name": "[US-ALAMOS-GW-001] Verify Gateway handles communication failure with ALAMOS FE2",
            "category": "Negative Scenario",
            "description": "Validate that the ALAMOS Gateway handles connectivity issues with ALAMOS FE2.",
            "preconditions": "1. ALAMOS Gateway is running\n2. ALAMOS FE2 is unavailable",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-001",
            "steps": [
                ("1", "Stop or make ALAMOS FE2 unavailable", "FE2 is not reachable"),
                ("2", "IPL sends a valid AlarmRequest to the Gateway", "AlarmRequest is transmitted"),
                ("3", "Verify Gateway attempts to forward request to ALAMOS FE2", "Connection attempt is made"),
                ("4", "Verify Gateway detects connectivity failure", "Connection refused or timeout error"),
                ("5", "Verify Gateway handles the failure gracefully", "Error is logged"),
                ("6", "Verify Gateway propagates technical error back to IPL", "SOAP response with technical error is returned to IPL")
            ]
        },
        {
            "tid": "TC-024",
            "name": "[US-ALAMOS-GW-001] Verify Gateway rejects malformed Alerting request",
            "category": "Negative Scenario",
            "description": "Validate that the ALAMOS Gateway rejects invalid or malformed Alerting requests.",
            "preconditions": "1. ALAMOS Gateway is running",
            "priority": "Medium",
            "user_story": "US-ALAMOS-GW-001",
            "steps": [
                ("1", "Prepare a malformed AlarmRequest (e.g., missing required alarm fields)", "Invalid request is prepared"),
                ("2", "IPL sends the malformed AlarmRequest to the Gateway", "Request is transmitted"),
                ("3", "Verify Gateway validates the incoming request", "Validation is performed"),
                ("4", "Verify Gateway detects the malformed request", "Validation error is identified"),
                ("5", "Verify Gateway rejects the request without forwarding to ALAMOS FE2", "Request is not forwarded"),
                ("6", "Verify Gateway returns validation error to IPL", "SOAP fault with validation error is returned")
            ]
        },
        # ============================================================================
        # ALAMOS GATEWAY - Continuous Mission Updates (US-ALAMOS-GW-002)
        # ============================================================================
        {
            "tid": "TC-025",
            "name": "[US-ALAMOS-GW-002] Verify Gateway processes Continuous Mission Update for incident status change",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway processes and forwards Continuous Mission Update triggered by incident status change.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL is configured\n3. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-002",
            "steps": [
                ("1", "Trigger an incident status change in IPL", "Incident status is updated"),
                ("2", "IPL sends Continuous Mission Update to ALAMOS Gateway", "Update request is transmitted"),
                ("3", "Verify Gateway receives the update request", "Request is received"),
                ("4", "Verify Gateway transforms and forwards update to ALAMOS FE2", "Update is forwarded via existing path"),
                ("5", "Verify ALAMOS FE2 returns success acknowledgment", "Success response is received"),
                ("6", "Verify Gateway propagates result back to IPL", "Processing result is returned to IPL")
            ]
        },
        {
            "tid": "TC-026",
            "name": "[US-ALAMOS-GW-002] Verify Gateway processes Continuous Mission Update for resource status change",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway processes and forwards Continuous Mission Update triggered by resource status change.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL is configured\n3. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-002",
            "steps": [
                ("1", "Trigger a resource status change in IPL", "Resource status is updated"),
                ("2", "IPL sends Continuous Mission Update to ALAMOS Gateway", "Update request is transmitted"),
                ("3", "Verify Gateway receives the update request", "Request is received"),
                ("4", "Verify Gateway transforms and forwards update to ALAMOS FE2", "Update is forwarded via existing path"),
                ("5", "Verify ALAMOS FE2 returns success acknowledgment", "Success response is received"),
                ("6", "Verify Gateway propagates result back to IPL", "Processing result is returned to IPL")
            ]
        },
        {
            "tid": "TC-027",
            "name": "[US-ALAMOS-GW-002] Verify Gateway processes Continuous Mission Update for keyword change",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway processes and forwards Continuous Mission Update triggered by keyword change.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL is configured\n3. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-002",
            "steps": [
                ("1", "Trigger a keyword change in IPL mission", "Keyword is updated"),
                ("2", "IPL sends Continuous Mission Update to ALAMOS Gateway", "Update request is transmitted"),
                ("3", "Verify Gateway receives the update request", "Request is received"),
                ("4", "Verify Gateway transforms and forwards update to ALAMOS FE2", "Update is forwarded"),
                ("5", "Verify ALAMOS FE2 returns success acknowledgment", "Success response is received"),
                ("6", "Verify Gateway propagates result back to IPL", "Processing result is returned")
            ]
        },
        {
            "tid": "TC-028",
            "name": "[US-ALAMOS-GW-002] Verify Gateway processes Continuous Mission Update for location change",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway processes and forwards Continuous Mission Update triggered by location change.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL is configured\n3. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-002",
            "steps": [
                ("1", "Trigger a location change in IPL mission", "Location is updated"),
                ("2", "IPL sends Continuous Mission Update to ALAMOS Gateway", "Update request is transmitted"),
                ("3", "Verify Gateway receives the update request", "Request is received"),
                ("4", "Verify Gateway transforms and forwards update to ALAMOS FE2", "Update is forwarded"),
                ("5", "Verify ALAMOS FE2 returns success acknowledgment", "Success response is received"),
                ("6", "Verify Gateway propagates result back to IPL", "Processing result is returned")
            ]
        },
        {
            "tid": "TC-029",
            "name": "[US-ALAMOS-GW-002] Verify backward compatibility for existing Continuous Mission Update functionality",
            "category": "Functional (Happy Path)",
            "description": "Validate that existing Continuous Mission Update functionality remains backward compatible.",
            "preconditions": "1. ALAMOS Gateway is running with updated codebase\n2. Existing IPL integration is active",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-002",
            "steps": [
                ("1", "Use existing IPL client to send Continuous Mission Update in legacy format", "Legacy request format is used"),
                ("2", "Verify Gateway receives the update using existing integration path", "Request is received"),
                ("3", "Verify Gateway processes the update without errors", "Processing succeeds"),
                ("4", "Verify Gateway forwards to ALAMOS FE2 successfully", "Update reaches ALAMOS FE2"),
                ("5", "Verify response is returned in expected legacy format", "Backward compatibility is maintained")
            ]
        },
        # ============================================================================
        # ALAMOS GATEWAY - Squad Information Extension (US-ALAMOS-GW-003)
        # ============================================================================
        {
            "tid": "TC-030",
            "name": "[US-ALAMOS-GW-003] Verify Gateway processes Alerting request with single squad information",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway correctly processes Alerting request containing single squad information.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL and ALAMOS FE2 are available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-003",
            "steps": [
                ("1", "Prepare AlarmRequest with single <squads> entry containing squad details", "Request with one squad is prepared"),
                ("2", "IPL sends the AlarmRequest to ALAMOS Gateway", "Request is transmitted"),
                ("3", "Verify Gateway extracts squad information from request", "Squad data is extracted"),
                ("4", "Verify Gateway maps squad information to ALAMOS message structure", "Mapping is performed"),
                ("5", "Verify Gateway forwards enriched request to ALAMOS FE2", "Request with squad info is forwarded"),
                ("6", "Verify ALAMOS FE2 receives and acknowledges the squad information", "Squad data is received by FE2"),
                ("7", "Verify acknowledgment is propagated back to IPL", "Success response returned")
            ]
        },
        {
            "tid": "TC-031",
            "name": "[US-ALAMOS-GW-003] Verify Gateway processes Alerting request with multiple squad entries",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway correctly processes Alerting request containing multiple squad entries.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL and ALAMOS FE2 are available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-003",
            "steps": [
                ("1", "Prepare AlarmRequest with multiple <squads> entries (e.g., 3 squads)", "Request with multiple squads is prepared"),
                ("2", "IPL sends the AlarmRequest to ALAMOS Gateway", "Request is transmitted"),
                ("3", "Verify Gateway extracts all squad entries from request", "All squad data is extracted"),
                ("4", "Verify Gateway maps all squad information to ALAMOS message structure", "Multiple squads are mapped"),
                ("5", "Verify Gateway forwards enriched request with all squads to ALAMOS FE2", "Request with all squad info is forwarded"),
                ("6", "Verify ALAMOS FE2 receives all squad entries", "All squad data is received by FE2"),
                ("7", "Verify acknowledgment is propagated back to IPL", "Success response returned")
            ]
        },
        {
            "tid": "TC-032",
            "name": "[US-ALAMOS-GW-003] Verify backward compatibility for Alerting request without squad information",
            "category": "Functional (Happy Path)",
            "description": "Validate that Alerting requests without squad information continue to be processed successfully.",
            "preconditions": "1. ALAMOS Gateway is running\n2. IPL and ALAMOS FE2 are available",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-003",
            "steps": [
                ("1", "Prepare AlarmRequest without <squads> element (legacy format)", "Request without squads is prepared"),
                ("2", "IPL sends the AlarmRequest to ALAMOS Gateway", "Request is transmitted"),
                ("3", "Verify Gateway processes the request without errors", "Processing succeeds"),
                ("4", "Verify Gateway forwards request to ALAMOS FE2 in expected format", "Request is forwarded successfully"),
                ("5", "Verify ALAMOS FE2 processes the request without squad info", "FE2 processes successfully"),
                ("6", "Verify acknowledgment is propagated back to IPL", "Backward compatibility maintained")
            ]
        },
        {
            "tid": "TC-033",
            "name": "[US-ALAMOS-GW-003] Verify end-to-end squad information transmission to ALAMOS FE2",
            "category": "Functional (Happy Path)",
            "description": "Validate that squad information is correctly transmitted end-to-end from IPL to ALAMOS FE2.",
            "preconditions": "1. ALAMOS Gateway is running\n2. ALAMOS FE2 is available and can be monitored",
            "priority": "High",
            "user_story": "US-ALAMOS-GW-003",
            "steps": [
                ("1", "Prepare AlarmRequest with detailed squad information (squad ID, name, members)", "Complete squad data is prepared"),
                ("2", "IPL sends the AlarmRequest to ALAMOS Gateway", "Request is transmitted"),
                ("3", "Monitor the outbound request from Gateway to ALAMOS FE2", "Outbound traffic is captured"),
                ("4", "Verify all squad information fields are present in ALAMOS FE2 request", "Squad fields are correctly included"),
                ("5", "Verify squad data values match the original IPL request", "Data integrity is maintained"),
                ("6", "Verify ALAMOS FE2 acknowledges receipt of squad information", "Squad info successfully received")
            ]
        },
        # ============================================================================
        # RELIABILITY - Retry & DLQ Validation (US-ADAPTER-RELIABILITY-001)
        # ============================================================================
        {
            "tid": "TC-034",
            "name": "[US-ADAPTER-RELIABILITY-001] Verify successful retry after transient failure for Situation Report",
            "category": "Functional (Happy Path)",
            "description": "Validate that messages process successfully when transient failures resolve within configured retry limits.",
            "preconditions": "1. Adapter is running\n2. Retry mechanism is enabled\n3. IPL can be configured for transient failures",
            "priority": "High",
            "user_story": "US-ADAPTER-RELIABILITY-001",
            "steps": [
                ("1", "Configure IPL to fail first request and succeed on retry", "Transient failure simulation is set up"),
                ("2", "Submit a valid Situation Report to the Adapter", "Request is received"),
                ("3", "Verify first processing attempt fails with recoverable error", "First attempt fails"),
                ("4", "Verify retry mechanism triggers automatically", "Retry is initiated per policy"),
                ("5", "Verify second attempt succeeds", "Processing completes successfully on retry"),
                ("6", "Verify success acknowledgment is returned to ALAMOS FE2", "Transient failure was recovered")
            ]
        },
        {
            "tid": "TC-035",
            "name": "[US-ADAPTER-RELIABILITY-001] Verify message routes to DLQ when retry limits exceeded",
            "category": "Negative Scenario",
            "description": "Validate that messages are routed to the existing DLQ when retry limits are exceeded.",
            "preconditions": "1. Adapter is running\n2. Retry and DLQ mechanisms are enabled\n3. IPL configured to fail all requests",
            "priority": "High",
            "user_story": "US-ADAPTER-RELIABILITY-001",
            "steps": [
                ("1", "Configure IPL to fail all processing attempts", "Permanent failure simulation is set up"),
                ("2", "Submit a valid Situation Report to the Adapter", "Request is received"),
                ("3", "Verify first processing attempt fails", "First attempt fails"),
                ("4", "Verify all configured retry attempts are executed", "All retries are attempted"),
                ("5", "Verify retry limit is exceeded", "Maximum retries reached"),
                ("6", "Verify message is routed to existing DLQ", "Message appears in DLQ"),
                ("7", "Verify failure acknowledgment is returned to ALAMOS FE2", "Failure is communicated")
            ]
        },
        {
            "tid": "TC-036",
            "name": "[US-ADAPTER-RELIABILITY-001] Verify business validation error does not trigger retry",
            "category": "Negative Scenario",
            "description": "Validate that business validation errors do not trigger unnecessary retries.",
            "preconditions": "1. Adapter is running\n2. Retry mechanism is enabled",
            "priority": "High",
            "user_story": "US-ADAPTER-RELIABILITY-001",
            "steps": [
                ("1", "Submit a Situation Report that will fail business validation (e.g., invalid business data)", "Request with business validation issue is sent"),
                ("2", "Verify Adapter/FacadeService processes the request", "Request is processed"),
                ("3", "Verify business validation error is detected", "Business error is identified"),
                ("4", "Verify NO retry is triggered for the business error", "Retry counter remains at 0"),
                ("5", "Verify failure acknowledgment is returned immediately to ALAMOS FE2", "Business error is communicated without retry")
            ]
        },
        {
            "tid": "TC-037",
            "name": "[US-ADAPTER-RELIABILITY-001] Verify retry and DLQ logging with diagnostic information",
            "category": "Functional (Happy Path)",
            "description": "Validate that retry attempts, DLQ events, and processing failures are logged with sufficient diagnostic information.",
            "preconditions": "1. Adapter is running\n2. Logging is enabled\n3. Log monitoring is available",
            "priority": "Medium",
            "user_story": "US-ADAPTER-RELIABILITY-001",
            "steps": [
                ("1", "Configure IPL to fail all processing attempts", "Failure simulation is set up"),
                ("2", "Submit a valid Situation Report", "Request is received"),
                ("3", "Wait for all retries to complete and DLQ routing", "Retry cycle completes"),
                ("4", "Examine application logs", "Logs are reviewed"),
                ("5", "Verify each retry attempt is logged with timestamp and attempt number", "Retry logs contain diagnostic info"),
                ("6", "Verify DLQ routing event is logged", "DLQ event is logged"),
                ("7", "Verify error details and correlation ID are included in logs", "Sufficient traceability is available")
            ]
        },
        {
            "tid": "TC-038",
            "name": "[US-ADAPTER-RELIABILITY-001] Verify retry for Alerting flow communication failure",
            "category": "Functional (Happy Path)",
            "description": "Validate that retry mechanism works for Alerting flow when ALAMOS FE2 communication failure occurs.",
            "preconditions": "1. ALAMOS Gateway is running\n2. Retry mechanism is enabled\n3. ALAMOS FE2 can be toggled on/off",
            "priority": "High",
            "user_story": "US-ADAPTER-RELIABILITY-001",
            "steps": [
                ("1", "Stop ALAMOS FE2 to simulate communication failure", "FE2 is unavailable"),
                ("2", "IPL sends AlarmRequest to ALAMOS Gateway", "Request is transmitted"),
                ("3", "Verify first attempt fails with communication error", "First attempt fails"),
                ("4", "Start ALAMOS FE2 before retry limit is reached", "FE2 becomes available"),
                ("5", "Verify retry succeeds on subsequent attempt", "Processing completes on retry"),
                ("6", "Verify success is propagated to IPL", "Transient failure was recovered")
            ]
        },
        # ============================================================================
        # ALAMOS GATEWAY - Mock Service (US-ALAMOSGW-MOCK-001)
        # ============================================================================
        {
            "tid": "TC-039",
            "name": "[US-ALAMOSGW-MOCK-001] Verify Gateway runs successfully in mock mode",
            "category": "Functional (Happy Path)",
            "description": "Validate that the ALAMOS Gateway can be executed in mock mode as a standalone application.",
            "preconditions": "1. ALAMOS Gateway mock mode configuration is available",
            "priority": "High",
            "user_story": "US-ALAMOSGW-MOCK-001",
            "steps": [
                ("1", "Configure ALAMOS Gateway for mock mode", "Mock mode configuration is applied"),
                ("2", "Start ALAMOS Gateway as standalone application", "Gateway starts in mock mode"),
                ("3", "Verify Gateway is running and accepting requests", "Gateway endpoint is accessible"),
                ("4", "Verify no connection attempts are made to actual ALAMOS FE2", "No external ALAMOS connectivity"),
                ("5", "Verify mock mode indicator is logged or displayed", "Mock mode is confirmed active")
            ]
        },
        {
            "tid": "TC-040",
            "name": "[US-ALAMOSGW-MOCK-001] Verify mock mode returns predefined success response for Alerting",
            "category": "Functional (Happy Path)",
            "description": "Validate that mock mode returns predefined success responses for Alerting requests.",
            "preconditions": "1. ALAMOS Gateway is running in mock mode",
            "priority": "High",
            "user_story": "US-ALAMOSGW-MOCK-001",
            "steps": [
                ("1", "Ensure Gateway is running in mock mode with success response configured", "Mock mode is active"),
                ("2", "Send a valid AlarmRequest with squad information", "Request is transmitted"),
                ("3", "Verify Gateway does not contact ALAMOS FE2", "No external call is made"),
                ("4", "Verify Gateway returns predefined success response", "Success response is returned"),
                ("5", "Verify response format matches expected ALAMOS FE2 response structure", "Response is properly formatted")
            ]
        },
        {
            "tid": "TC-041",
            "name": "[US-ALAMOSGW-MOCK-001] Verify mock mode returns configurable error response for negative testing",
            "category": "Negative Scenario",
            "description": "Validate that mock mode supports configurable error responses for negative test scenarios.",
            "preconditions": "1. ALAMOS Gateway is running in mock mode\n2. Error response configuration is available",
            "priority": "Medium",
            "user_story": "US-ALAMOSGW-MOCK-001",
            "steps": [
                ("1", "Configure mock mode to return business error response", "Error configuration is applied"),
                ("2", "Send a valid AlarmRequest", "Request is transmitted"),
                ("3", "Verify Gateway returns configured error response", "Error response is returned"),
                ("4", "Verify error response matches the configured error type", "Correct error is simulated"),
                ("5", "Verify response is properly propagated to IPL", "Error flows correctly through the system")
            ]
        },
        {
            "tid": "TC-042",
            "name": "[US-ALAMOSGW-MOCK-001] Verify mock mode supports Continuous Mission Update testing",
            "category": "Functional (Happy Path)",
            "description": "Validate that Continuous Mission Update requests can be tested in mock mode.",
            "preconditions": "1. ALAMOS Gateway is running in mock mode",
            "priority": "High",
            "user_story": "US-ALAMOSGW-MOCK-001",
            "steps": [
                ("1", "Ensure Gateway is running in mock mode", "Mock mode is active"),
                ("2", "Send a Continuous Mission Update request for incident status change", "Update request is transmitted"),
                ("3", "Verify Gateway processes the request in mock mode", "Request is handled"),
                ("4", "Verify predefined response is returned", "Mock response is returned"),
                ("5", "Verify no actual ALAMOS FE2 communication occurs", "No external connectivity")
            ]
        },
        {
            "tid": "TC-043",
            "name": "[US-ALAMOSGW-MOCK-001] Verify mock mode does not affect normal gateway operation when disabled",
            "category": "Functional (Happy Path)",
            "description": "Validate that mock mode configuration does not impact normal gateway operation when disabled.",
            "preconditions": "1. ALAMOS Gateway with mock mode disabled\n2. ALAMOS FE2 is available",
            "priority": "High",
            "user_story": "US-ALAMOSGW-MOCK-001",
            "steps": [
                ("1", "Configure ALAMOS Gateway with mock mode disabled", "Normal mode configuration is applied"),
                ("2", "Start ALAMOS Gateway", "Gateway starts in normal mode"),
                ("3", "Send a valid AlarmRequest", "Request is transmitted"),
                ("4", "Verify Gateway connects to actual ALAMOS FE2", "Real connection is established"),
                ("5", "Verify real ALAMOS FE2 response is processed and returned", "Normal operation confirmed"),
                ("6", "Verify no mock responses are used", "Real responses are returned")
            ]
        },
        # ============================================================================
        # END-TO-END INTEGRATION TESTING (US-INTEGRATION-E2E-001)
        # ============================================================================
        {
            "tid": "TC-044",
            "name": "[US-INTEGRATION-E2E-001] Verify complete Alerting flow with squad information (E2E)",
            "category": "Functional (Happy Path)",
            "description": "Validate end-to-end Alerting flow including squad transmission from IPL through Gateway to ALAMOS FE2 and acknowledgement propagation.",
            "preconditions": "1. All components (IPL, Gateway, ALAMOS FE2) are running\n2. Network connectivity is established",
            "priority": "High",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "IPL Server initiates AlarmRequest with squad information", "Request originates from IPL"),
                ("2", "Verify request flows through Facade Service (LEGACY)", "Legacy routing is used"),
                ("3", "Verify ALAMOS Gateway receives and processes request", "Gateway processes request"),
                ("4", "Verify squad information is included in outbound request to ALAMOS FE2", "Squad data is transmitted"),
                ("5", "Verify ALAMOS FE2 receives and processes the Alerting request", "FE2 processes successfully"),
                ("6", "Verify acknowledgement flows back through Gateway to IPL", "Response propagates correctly"),
                ("7", "Verify logging and traceability information is available", "Complete trace is available")
            ]
        },
        {
            "tid": "TC-045",
            "name": "[US-INTEGRATION-E2E-001] Verify complete Continuous Mission Update flow (E2E)",
            "category": "Functional (Happy Path)",
            "description": "Validate end-to-end Continuous Mission Update flow from IPL through Gateway to ALAMOS FE2.",
            "preconditions": "1. All components (IPL, Gateway, ALAMOS FE2) are running\n2. Active mission exists in IPL",
            "priority": "High",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "Trigger incident status change in IPL", "Mission update is initiated"),
                ("2", "Verify Continuous Mission Update flows from IPL to Gateway", "Update reaches Gateway"),
                ("3", "Verify Gateway transforms and forwards update to ALAMOS FE2", "Update is forwarded"),
                ("4", "Verify ALAMOS FE2 receives the mission update", "FE2 receives update"),
                ("5", "Verify response flows back through Gateway to IPL", "Response propagates correctly"),
                ("6", "Verify ALAMOS is synchronized with the status change", "Systems are in sync")
            ]
        },
        {
            "tid": "TC-046",
            "name": "[US-INTEGRATION-E2E-001] Verify complete Situation Report flow (E2E)",
            "category": "Functional (Happy Path)",
            "description": "Validate end-to-end Situation Report flow from ALAMOS FE2 through Adapter to IPL and acknowledgement propagation.",
            "preconditions": "1. All components (Adapter, FacadeService, IPL) are running\n2. ALAMOS FE2 is configured",
            "priority": "High",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "ALAMOS FE2 sends Situation Report to ALAMOS Adapter", "Report is submitted"),
                ("2", "Verify Adapter receives and validates the Situation Report", "Validation passes"),
                ("3", "Verify Adapter creates incident.situation_report_received Domain Event", "Domain Event is generated"),
                ("4", "Verify FacadeService routes and processes the Domain Event", "Event is routed to IPL processing"),
                ("5", "Verify IPL erzeugeEinsatzmeldung endpoint is invoked successfully", "IPL processes the report"),
                ("6", "Verify success acknowledgement flows back to ALAMOS FE2", "End-to-end success confirmed"),
                ("7", "Verify logging and monitoring data is available across all components", "Complete traceability")
            ]
        },
        {
            "tid": "TC-047",
            "name": "[US-INTEGRATION-E2E-001] Verify E2E failure propagation for Situation Report IPL fault",
            "category": "Negative Scenario",
            "description": "Validate that business validation failures propagate correctly from IPL back to ALAMOS FE2 end-to-end.",
            "preconditions": "1. All components are running\n2. IPL configured to return business fault",
            "priority": "High",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "Configure IPL to return business fault for specific scenario", "Fault simulation is configured"),
                ("2", "ALAMOS FE2 sends Situation Report to Adapter", "Report is submitted"),
                ("3", "Verify Adapter validates and creates Domain Event", "Processing begins"),
                ("4", "Verify FacadeService invokes IPL", "IPL is called"),
                ("5", "Verify IPL returns business fault", "Fault response is received"),
                ("6", "Verify fault is propagated through FacadeService to Adapter", "Fault flows back"),
                ("7", "Verify ALAMOS FE2 receives accurate failure acknowledgement", "Fault is correctly communicated to originating system")
            ]
        },
        {
            "tid": "TC-048",
            "name": "[US-INTEGRATION-E2E-001] Verify E2E retry and DLQ with no message loss",
            "category": "Functional (Happy Path)",
            "description": "Validate that retry and DLQ mechanisms work correctly end-to-end with no unexpected message loss.",
            "preconditions": "1. All components are running\n2. Retry and DLQ mechanisms are enabled",
            "priority": "High",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "Configure target system (IPL or ALAMOS FE2) to fail intermittently", "Failure simulation is set up"),
                ("2", "Submit multiple test messages across all ALAMOS flows", "Messages are submitted"),
                ("3", "Verify retry mechanism triggers for failed messages", "Retries occur"),
                ("4", "Verify messages that exceed retry limits route to DLQ", "DLQ routing works"),
                ("5", "Verify successful messages complete normally", "Success path works"),
                ("6", "Count total messages: submitted = (successful + DLQ)", "No message loss occurs")
            ]
        },
        {
            "tid": "TC-049",
            "name": "[US-INTEGRATION-E2E-001] Verify logging and monitoring across all E2E flows",
            "category": "Functional (Happy Path)",
            "description": "Validate that logging, monitoring, and traceability information is available across all tested integration flows.",
            "preconditions": "1. All components are running\n2. Logging and monitoring are enabled",
            "priority": "Medium",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "Execute Alerting, Continuous Mission Update, and Situation Report flows", "All flows are executed"),
                ("2", "Access centralized logging/monitoring system", "Logs are retrieved"),
                ("3", "Verify each flow has correlation ID traceable across components", "Correlation IDs are consistent"),
                ("4", "Verify request/response timestamps are logged for each component", "Timing information is available"),
                ("5", "Verify error details are logged for any failures", "Error logging is complete"),
                ("6", "Verify monitoring dashboards show all flow metrics", "Monitoring data is available")
            ]
        },
        {
            "tid": "TC-050",
            "name": "[US-INTEGRATION-E2E-001] Verify E2E behavior under ALAMOS FE2 temporary unavailability",
            "category": "Edge Case",
            "description": "Validate end-to-end behavior when ALAMOS FE2 becomes temporarily unavailable during Alerting flow.",
            "preconditions": "1. All components are running\n2. ALAMOS FE2 availability can be controlled",
            "priority": "Medium",
            "user_story": "US-INTEGRATION-E2E-001",
            "steps": [
                ("1", "Start Alerting flow from IPL while ALAMOS FE2 is available", "Initial state is healthy"),
                ("2", "Stop ALAMOS FE2 mid-flow (after Gateway receives request)", "FE2 becomes unavailable"),
                ("3", "Verify Gateway detects communication failure", "Failure is detected"),
                ("4", "Verify retry mechanism is triggered", "Retries begin"),
                ("5", "Restart ALAMOS FE2 within retry window", "FE2 becomes available again"),
                ("6", "Verify subsequent retry succeeds and flow completes", "Recovery is successful"),
                ("7", "Verify IPL receives success acknowledgement", "End-to-end recovery confirmed")
            ]
        }
    ]
    
    # Write test cases to worksheet
    current_row = 2
    for tc in test_cases:
        first_step_row = current_row
        
        for idx, (step_no, step_desc, expected) in enumerate(tc["steps"]):
            row = current_row + idx
            
            # Write TID, Test Case Name, Category, Description, Pre-conditions, Priority, User Story only on first row
            if idx == 0:
                ws.cell(row=row, column=1, value=tc["tid"])
                ws.cell(row=row, column=2, value=tc["name"])
                ws.cell(row=row, column=3, value=tc["category"])
                ws.cell(row=row, column=4, value=tc["description"])
                ws.cell(row=row, column=5, value=tc["preconditions"])
                ws.cell(row=row, column=9, value=tc["priority"])
                ws.cell(row=row, column=10, value=tc["user_story"])
            
            # Write step details
            ws.cell(row=row, column=6, value=step_no)
            ws.cell(row=row, column=7, value=step_desc)
            ws.cell(row=row, column=8, value=expected)
        
        current_row += len(tc["steps"])
        
        # Add blank row after each test case
        current_row += 1
    
    # Apply formatting
    for row in ws.iter_rows(min_row=1, max_row=current_row):
        for cell in row:
            cell.alignment = Alignment(vertical='top', wrap_text=True)
    
    # Set column widths
    column_widths = {
        'A': 10,   # TID
        'B': 60,   # Test Case Name
        'C': 25,   # Category
        'D': 50,   # Description
        'E': 40,   # Pre-conditions
        'F': 10,   # Step No
        'G': 60,   # Step Description
        'H': 50,   # Expected Result
        'I': 10,   # Priority
        'J': 25    # User Story Reference
    }
    
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Enable Auto Filter
    ws.auto_filter.ref = f"A1:J{current_row}"
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ALAMOS_Functional_Integration_TestCases_{timestamp}.xlsx"
    
    return wb, filename

def main():
    """Main function to generate and save the test cases workbook"""
    output_dir = r"c:\Apparao Maroju\AI-SSI\Project-IGNIS(POC)\ALOMAS\ALAMOS-Output"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate workbook
    wb, filename = create_test_cases_workbook()
    
    # Save workbook
    filepath = os.path.join(output_dir, filename)
    wb.save(filepath)
    
    print(f"Test cases workbook generated successfully!")
    print(f"File: {filepath}")
    print(f"Total test cases: 50")
    
    return filepath

if __name__ == "__main__":
    main()
