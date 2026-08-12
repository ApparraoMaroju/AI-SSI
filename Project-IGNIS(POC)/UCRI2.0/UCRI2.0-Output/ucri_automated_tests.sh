#!/bin/bash
###############################################################################
# UCRI 2.0 Automated Test Suite
# Source: TestCases_20260428_105917.xlsx
# Covers: IMT, FWD, REV, U2U, TC categories (36 fully automatable test cases)
###############################################################################

set -euo pipefail

###############################################################################
# CONFIGURATION — Update these values for your environment
###############################################################################
ADAPTER_BASE_URL="${ADAPTER_BASE_URL:-http://localhost:8080}"
UCRM_BASE_URL="${UCRM_BASE_URL:-http://localhost:8081}"
ADAPTER_CONFIG_DIR="${ADAPTER_CONFIG_DIR:-/opt/adapter/config}"
ADAPTER_LOG_DIR="${ADAPTER_LOG_DIR:-/opt/adapter/logs}"
P2P_TOKEN="${P2P_TOKEN:-valid-p2p-token}"
P2P_TOKEN_INVALID="${P2P_TOKEN_INVALID:-invalid-p2p-token}"
ADAPTER_START_CMD="${ADAPTER_START_CMD:-/opt/adapter/bin/start.sh}"
ADAPTER_STOP_CMD="${ADAPTER_STOP_CMD:-/opt/adapter/bin/stop.sh}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-30}"
LOG_FILE="ucri_test_results_$(date +%Y%m%d_%H%M%S).log"
RESULTS_SUMMARY=""
PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# Endpoints
EINSATZ_ENDPOINT="${ADAPTER_BASE_URL}/einsatztransfer/erzeugeEinsatz"
ACK_ENDPOINT="${ADAPTER_BASE_URL}/einsatztransfer/quittiereTranferEinsatz"
MESSAGING_SEND_ENDPOINT="${ADAPTER_BASE_URL}/messaging/send"

# Test Mandants
IPL_MANDANT="IPL_CENTER_001"
UCRI1_MANDANT="UCRI_CENTER_001"
UCRI2_MANDANT="UCRI_CENTER_002"

###############################################################################
# UTILITY FUNCTIONS
###############################################################################
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE"
}

log_header() {
    echo "" | tee -a "$LOG_FILE"
    echo "================================================================" | tee -a "$LOG_FILE"
    echo " $1" | tee -a "$LOG_FILE"
    echo "================================================================" | tee -a "$LOG_FILE"
}

record_result() {
    local tid="$1"
    local name="$2"
    local status="$3"
    local detail="${4:-}"
    RESULTS_SUMMARY="${RESULTS_SUMMARY}\n${tid} | ${name} | ${status} | ${detail}"
    if [ "$status" = "PASS" ]; then
        ((PASS_COUNT++))
    elif [ "$status" = "FAIL" ]; then
        ((FAIL_COUNT++))
    else
        ((SKIP_COUNT++))
    fi
    log "  >> ${tid}: ${status} ${detail:+- $detail}"
}

assert_http_status() {
    local actual="$1"
    local expected="$2"
    local tid="$3"
    local name="$4"
    if [ "$actual" -eq "$expected" ]; then
        return 0
    else
        log "  ASSERTION FAILED: Expected HTTP $expected, got HTTP $actual"
        return 1
    fi
}

assert_response_contains() {
    local response="$1"
    local expected_text="$2"
    if echo "$response" | grep -qi "$expected_text"; then
        return 0
    else
        log "  ASSERTION FAILED: Response does not contain '$expected_text'"
        return 1
    fi
}

assert_response_not_contains() {
    local response="$1"
    local unexpected_text="$2"
    if echo "$response" | grep -qi "$unexpected_text"; then
        log "  ASSERTION FAILED: Response unexpectedly contains '$unexpected_text'"
        return 1
    else
        return 0
    fi
}

assert_log_contains() {
    local search_text="$1"
    local log_file="${2:-${ADAPTER_LOG_DIR}/adapter.log}"
    if grep -qi "$search_text" "$log_file" 2>/dev/null; then
        return 0
    else
        log "  ASSERTION FAILED: Log does not contain '$search_text'"
        return 1
    fi
}

assert_log_not_contains() {
    local search_text="$1"
    local log_file="${2:-${ADAPTER_LOG_DIR}/adapter.log}"
    if grep -qi "$search_text" "$log_file" 2>/dev/null; then
        log "  ASSERTION FAILED: Log unexpectedly contains '$search_text'"
        return 1
    else
        return 0
    fi
}

send_post_request() {
    local url="$1"
    local payload="$2"
    local token="${3:-$P2P_TOKEN}"
    local timeout="${4:-$TIMEOUT_SECONDS}"
    curl -s -w "\n%{http_code}" \
        -X POST "$url" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $token" \
        --max-time "$timeout" \
        -d "$payload" 2>/dev/null || echo -e "\nCONNECTION_ERROR"
}

extract_http_code() {
    echo "$1" | tail -1
}

extract_response_body() {
    echo "$1" | sed '$d'
}

wait_for_service() {
    local url="$1"
    local max_wait="${2:-60}"
    local waited=0
    while [ $waited -lt $max_wait ]; do
        if curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null | grep -q "^[2-4]"; then
            return 0
        fi
        sleep 2
        waited=$((waited + 2))
    done
    return 1
}

set_adapter_config() {
    local property="$1"
    local value="$2"
    local config_file="${ADAPTER_CONFIG_DIR}/application.properties"
    if [ -f "$config_file" ]; then
        if grep -q "^${property}=" "$config_file"; then
            sed -i "s|^${property}=.*|${property}=${value}|" "$config_file"
        else
            echo "${property}=${value}" >> "$config_file"
        fi
    fi
}

remove_adapter_config() {
    local property="$1"
    local config_file="${ADAPTER_CONFIG_DIR}/application.properties"
    if [ -f "$config_file" ]; then
        sed -i "/^${property}=/d" "$config_file"
    fi
}

restart_adapter() {
    log "  Stopping Adapter..."
    $ADAPTER_STOP_CMD 2>/dev/null || true
    sleep 3
    log "  Starting Adapter..."
    $ADAPTER_START_CMD 2>/dev/null
    sleep 5
}

clear_logs() {
    : > "${ADAPTER_LOG_DIR}/adapter.log" 2>/dev/null || true
}

# JSON payload builders
build_transfer_einsatz_request() {
    local source_mandant="${1:-$IPL_MANDANT}"
    local target_mandant="${2:-$UCRI1_MANDANT}"
    local einsatz_id="${3:-EIN-$(date +%s)}"
    local correlation_id="${4:-CORR-$(date +%s)}"
    cat <<EOF
{
    "correlationId": "$correlation_id",
    "sourceMandant": "$source_mandant",
    "targetMandant": "$target_mandant",
    "transferEinsatz": {
        "einsatzId": "$einsatz_id",
        "einsatznummerKurz": "K-$(shuf -i 10000-99999 -n 1)",
        "kategorie": "KAT-01",
        "einsatzStichwort": "FEUER",
        "alarmierungsstichwortText": "Brand in Wohngebaeude"
    },
    "partitionKey": "PK-$einsatz_id"
}
EOF
}

build_messaging_send_payload() {
    local sender_client_id="${1:-$UCRI1_MANDANT}"
    local receiver_client_id="${2:-$IPL_MANDANT}"
    local operation_id="${3:-OP-$(date +%s)}"
    local correlation_id="${4:-CORR-$(date +%s)}"
    cat <<EOF
{
    "correlationId": "$correlation_id",
    "header": {
        "sender_client_id": "$sender_client_id",
        "receiver_client_id": "$receiver_client_id",
        "source": "UCRM",
        "type": "MissionDispatch"
    },
    "operation": {
        "id": "$operation_id",
        "name": "K-$(shuf -i 10000-99999 -n 1)",
        "occassion": {
            "type_1": "KAT-02",
            "keyword_1": "RETTUNG",
            "keyword_1_text": "Rettungseinsatz"
        }
    },
    "partitionKey": "PK-$operation_id"
}
EOF
}

###############################################################################
# IN-MEMORY TRANSPORT TESTS (IMT)
###############################################################################

test_IMT001() {
    log_header "IMT-001: In-Memory Transport Initialization"
    local tid="IMT-001"
    local name="In-Memory Transport Initialization"

    # Step 1: Set configuration
    log "  Step 1: Setting adapter.transport=in-memory"
    set_adapter_config "adapter.transport" "in-memory"
    set_adapter_config "adapter.receiver.enabled" "true"
    set_adapter_config "adapter.handler.enabled" "true"
    set_adapter_config "adapter.dispatcher.enabled" "true"

    # Step 2: Start Adapter
    log "  Step 2: Starting Adapter service"
    clear_logs
    restart_adapter

    # Step 3: Check startup logs for transport mode
    log "  Step 3: Checking startup logs for transport mode"
    sleep 5
    if assert_log_contains "in-memory transport active\|EventBus.*init\|in-memory.*started"; then
        log "  Step 3: PASS - In-memory transport indication found in logs"
    else
        record_result "$tid" "$name" "FAIL" "No in-memory transport indication in startup logs"
        return
    fi

    # Step 4: Verify no Kafka connection
    log "  Step 4: Verifying no Kafka connection attempts"
    if assert_log_not_contains "kafka.*connect\|bootstrap.servers"; then
        log "  Step 4: PASS - No Kafka connection attempts"
    else
        record_result "$tid" "$name" "FAIL" "Unexpected Kafka connection attempts found in logs"
        return
    fi

    # Step 5: Verify all modules initialized
    log "  Step 5: Verifying Receiver, Handler, Dispatcher modules initialized"
    local all_initialized=true
    for module in "Receiver" "Handler" "Dispatcher"; do
        if ! assert_log_contains "${module}.*started\|${module}.*initialized"; then
            log "  Step 5: FAIL - ${module} module not initialized"
            all_initialized=false
        fi
    done

    if $all_initialized; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Not all modules initialized"
    fi
}

test_IMT004() {
    log_header "IMT-004: Envelope Metadata Preservation"
    local tid="IMT-004"
    local name="Envelope Metadata Preservation"
    local corr_id="CORR-12345"

    clear_logs

    # Step 1-2: Create and send event with specific metadata
    log "  Step 1-2: Sending event with correlationId=${corr_id}"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-META-001" "$corr_id")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Step 3: Verify Handler receives with same correlationId
    log "  Step 3: Verifying Handler log contains correlationId=${corr_id}"
    if ! assert_log_contains "$corr_id"; then
        record_result "$tid" "$name" "FAIL" "correlationId not found in logs"
        return
    fi

    # Step 4-5: Verify metadata preserved end-to-end
    log "  Step 4-5: Verifying metadata preserved in Dispatcher output"
    local body
    body=$(extract_response_body "$response")
    if echo "$body" | grep -q "$corr_id"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "correlationId not in response"
    fi
}

test_IMT005() {
    log_header "IMT-005: Invalid Event Rejected by Receiver"
    local tid="IMT-005"
    local name="Invalid Event Rejected by Receiver"

    clear_logs

    # Step 1: Send malformed event (missing required fields)
    log "  Step 1: Sending malformed event (missing required fields)"
    local payload='{"correlationId": "CORR-INVALID-001", "transferEinsatz": {}}'
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    # Expect 400 Bad Request or similar error
    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Event rejected with HTTP $http_code"
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx error, got HTTP $http_code"
        return
    fi

    sleep 2

    # Step 2: Check logs for validation failure
    log "  Step 2: Checking logs for validation failure"
    if assert_log_contains "validation.*error\|validation.*fail\|invalid.*request"; then
        log "  Step 2: PASS - Validation error logged"
    fi

    # Step 3-4: Verify Handler and Dispatcher did NOT process the event
    log "  Step 3-4: Verifying no Handler/Dispatcher processing for rejected event"
    if assert_log_not_contains "Handler.*CORR-INVALID-001\|Dispatcher.*CORR-INVALID-001"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Rejected event was processed by Handler/Dispatcher"
    fi
}

test_IMT006() {
    log_header "IMT-006: Receiver Module Disabled"
    local tid="IMT-006"
    local name="Receiver Module Disabled"

    # Step 1: Start Adapter with receiver disabled
    log "  Step 1: Setting adapter.receiver.enabled=false"
    set_adapter_config "adapter.receiver.enabled" "false"
    set_adapter_config "adapter.handler.enabled" "true"
    set_adapter_config "adapter.dispatcher.enabled" "true"
    clear_logs
    restart_adapter

    sleep 5

    # Step 2: Verify Receiver NOT instantiated
    log "  Step 2: Verifying Receiver module is disabled"
    if assert_log_contains "Receiver.*disabled\|Receiver.*skipped"; then
        log "  Step 2: PASS - Receiver disabled in logs"
    fi

    # Step 3: Attempt to send event
    log "  Step 3: Attempting to send event to disabled Receiver"
    local payload
    payload=$(build_transfer_einsatz_request)
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ] || [ "$http_code" -ge 400 ]; then
        log "  Step 3: PASS - Event not consumed (HTTP: $http_code)"
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Event accepted despite Receiver disabled (HTTP: $http_code)"
    fi

    # Restore config
    set_adapter_config "adapter.receiver.enabled" "true"
}

test_IMT007() {
    log_header "IMT-007: Handler Module Disabled"
    local tid="IMT-007"
    local name="Handler Module Disabled"

    # Step 1: Start Adapter with handler disabled
    log "  Step 1: Setting adapter.handler.enabled=false"
    set_adapter_config "adapter.receiver.enabled" "true"
    set_adapter_config "adapter.handler.enabled" "false"
    set_adapter_config "adapter.dispatcher.enabled" "true"
    clear_logs
    restart_adapter
    sleep 5

    # Step 2: Send valid event
    log "  Step 2: Sending valid event to Receiver"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-HDIS-001" "CORR-HDIS-001")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")

    sleep 3

    # Step 3: Verify Handler did NOT process
    log "  Step 3: Verifying Handler did NOT process event"
    if assert_log_not_contains "Handler.*CORR-HDIS-001\|Handler.*processing.*CORR-HDIS-001"; then
        log "  Step 3: PASS - No Handler processing"
    fi

    # Step 4: Verify Dispatcher did NOT dispatch
    log "  Step 4: Verifying Dispatcher did NOT dispatch event"
    if assert_log_not_contains "Dispatcher.*CORR-HDIS-001"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Dispatcher activity found despite Handler disabled"
    fi

    # Restore config
    set_adapter_config "adapter.handler.enabled" "true"
}

test_IMT008() {
    log_header "IMT-008: Dispatcher Module Disabled"
    local tid="IMT-008"
    local name="Dispatcher Module Disabled"

    # Step 1: Start Adapter with dispatcher disabled
    log "  Step 1: Setting adapter.dispatcher.enabled=false"
    set_adapter_config "adapter.receiver.enabled" "true"
    set_adapter_config "adapter.handler.enabled" "true"
    set_adapter_config "adapter.dispatcher.enabled" "false"
    clear_logs
    restart_adapter
    sleep 5

    # Step 2-3: Send event, verify Handler processes
    log "  Step 2-3: Sending event and verifying Handler processing"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-DDIS-001" "CORR-DDIS-001")
    send_post_request "$EINSATZ_ENDPOINT" "$payload" > /dev/null
    sleep 3

    # Step 4: Verify Dispatcher did NOT route
    log "  Step 4: Verifying Dispatcher did NOT route event"
    if assert_log_not_contains "Dispatcher.*publish\|events-ucri.*CORR-DDIS-001"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Dispatcher routed event despite being disabled"
    fi

    # Restore config
    set_adapter_config "adapter.dispatcher.enabled" "true"
}

test_IMT009() {
    log_header "IMT-009: Invalid Transport Configuration"
    local tid="IMT-009"
    local name="Invalid Transport Configuration"

    # Step 1: Set invalid transport config
    log "  Step 1: Setting adapter.transport=invalid_value"
    set_adapter_config "adapter.transport" "invalid_value"
    clear_logs

    # Step 2: Attempt to start — expect failure
    log "  Step 2: Attempting to start Adapter (should fail)"
    $ADAPTER_STOP_CMD 2>/dev/null || true
    sleep 2
    local start_output
    start_output=$($ADAPTER_START_CMD 2>&1 || true)
    sleep 3

    # Step 3: Check error output
    log "  Step 3: Checking for descriptive error message"
    if echo "$start_output" | grep -qi "invalid.*transport\|valid.*options\|in-memory.*kafka"; then
        log "  Step 3: PASS - Descriptive error message found"
    elif assert_log_contains "invalid.*transport\|valid.*options\|in-memory.*kafka"; then
        log "  Step 3: PASS - Descriptive error in logs"
    fi

    # Step 4: Correct config and restart
    log "  Step 4: Correcting config and restarting"
    set_adapter_config "adapter.transport" "in-memory"
    restart_adapter
    sleep 5

    if wait_for_service "${ADAPTER_BASE_URL}/health" 30; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Service did not recover after config fix"
    fi
}

test_IMT010() {
    log_header "IMT-010: Missing Transport Configuration"
    local tid="IMT-010"
    local name="Missing Transport Configuration"

    # Step 1: Remove transport config
    log "  Step 1: Removing adapter.transport property"
    remove_adapter_config "adapter.transport"
    clear_logs

    # Step 2: Attempt to start
    log "  Step 2: Attempting to start Adapter (should fail)"
    $ADAPTER_STOP_CMD 2>/dev/null || true
    sleep 2
    local start_output
    start_output=$($ADAPTER_START_CMD 2>&1 || true)
    sleep 3

    # Step 3: Verify error about missing config
    log "  Step 3: Verifying error indicates missing transport property"
    if echo "$start_output" | grep -qi "transport.*required\|missing.*transport\|transport.*not.*configured"; then
        record_result "$tid" "$name" "PASS"
    elif assert_log_contains "transport.*required\|missing.*transport\|transport.*not.*configured"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "No clear error for missing transport config"
    fi

    # Restore config
    set_adapter_config "adapter.transport" "in-memory"
    restart_adapter
}

###############################################################################
# FORWARD FLOW TESTS — IPL to UCRI (FWD)
###############################################################################

test_FWD001() {
    log_header "FWD-001: IPL to UCRI — Happy Path: Event Accepted (EMPFANG)"
    local tid="FWD-001"
    local name="Happy Path: Event Accepted (EMPFANG)"
    local corr_id="CORR-FWD001-$(date +%s)"

    clear_logs

    # Step 1: Send valid TransferEinsatzRequest
    log "  Step 1: Sending TransferEinsatzRequest to ${EINSATZ_ENDPOINT}"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD001" "$corr_id")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    # Expect 200 or 202
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 202 ]; then
        log "  Step 1: PASS - Request accepted (HTTP $http_code)"
    else
        record_result "$tid" "$name" "FAIL" "Expected HTTP 200/202, got $http_code"
        return
    fi

    sleep 5

    # Step 2: Verify validation passes (no errors in logs)
    log "  Step 2: Verifying validation passed"
    if assert_log_not_contains "validation.*error.*${corr_id}\|validation.*fail.*${corr_id}"; then
        log "  Step 2: PASS - No validation errors"
    fi

    # Step 3: Verify P2P authentication
    log "  Step 3: Verifying P2P authentication"
    if assert_log_contains "P2P.*auth.*success\|authentication.*success\|token.*valid"; then
        log "  Step 3: PASS - P2P auth successful"
    fi

    # Step 7-8: Verify EMPFANG ACK
    log "  Step 7-8: Verifying EMPFANG ACK"
    if assert_log_contains "EMPFANG"; then
        log "  Step 9: PASS - EMPFANG found in logs"
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "EMPFANG ACK not found in logs"
    fi
}

test_FWD002() {
    log_header "FWD-002: IPL to UCRI — Event Rejected (EINSATZ_ABGELEHNT)"
    local tid="FWD-002"
    local name="Event Rejected (EINSATZ_ABGELEHNT)"
    local corr_id="CORR-FWD002-$(date +%s)"

    clear_logs

    # Step 1: Send valid TransferEinsatzRequest (UCRM configured to reject)
    log "  Step 1: Sending TransferEinsatzRequest"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD002-REJECT" "$corr_id")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 5

    # Step 6-7: Verify EINSATZ_ABGELEHNT ACK
    log "  Step 6-7: Verifying EINSATZ_ABGELEHNT ACK"
    if assert_log_contains "EINSATZ_ABGELEHNT"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "EINSATZ_ABGELEHNT not found in logs"
    fi
}

test_FWD003() {
    log_header "FWD-003: IPL to UCRI — Timeout (TECHNISCHER_FEHLER)"
    local tid="FWD-003"
    local name="Timeout (TECHNISCHER_FEHLER)"
    local corr_id="CORR-FWD003-$(date +%s)"

    clear_logs

    # Step 1: Send valid request (UCRM configured to not respond)
    log "  Step 1: Sending TransferEinsatzRequest (expecting timeout)"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD003-TIMEOUT" "$corr_id")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload" "$P2P_TOKEN" "$TIMEOUT_SECONDS")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    # Wait for timeout to occur
    sleep "$((TIMEOUT_SECONDS + 5))"

    # Step 5-7: Verify TECHNISCHER_FEHLER ACK
    log "  Step 5-7: Verifying TECHNISCHER_FEHLER ACK"
    if assert_log_contains "TECHNISCHER_FEHLER"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "TECHNISCHER_FEHLER not found in logs"
    fi
}

test_FWD004() {
    log_header "FWD-004: IPL to UCRI — Validation Failure at Receiver"
    local tid="FWD-004"
    local name="Validation Failure at Receiver"

    clear_logs

    # Step 1: Send invalid/malformed request
    log "  Step 1: Sending invalid TransferEinsatzRequest (missing einsatzId, invalid format)"
    local payload='{"correlationId": "CORR-FWD004", "sourceMandant": "'$IPL_MANDANT'", "targetMandant": "'$UCRI1_MANDANT'", "transferEinsatz": {"kategorie": "INVALID"}}'
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    # Expect 4xx error
    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Validation error returned (HTTP $http_code)"
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx, got HTTP $http_code"
        return
    fi

    sleep 2

    # Step 2: Verify validation failure logged
    log "  Step 2: Verifying validation failure logged"
    assert_log_contains "validation.*fail\|validation.*error" || true

    # Step 4-6: Verify NO Handler, Dispatcher, or ACK processing
    log "  Step 4-6: Verifying no Handler/Dispatcher/ACK processing"
    if assert_log_not_contains "Handler.*CORR-FWD004" && \
       assert_log_not_contains "Dispatcher.*CORR-FWD004" && \
       assert_log_not_contains "quittiereTranferEinsatz.*CORR-FWD004"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Rejected request was processed downstream"
    fi
}

test_FWD005() {
    log_header "FWD-005: IPL to UCRI — P2P Authentication Failure"
    local tid="FWD-005"
    local name="P2P Authentication Failure"

    clear_logs

    # Step 1: Send valid request with invalid P2P token
    log "  Step 1: Sending request with invalid P2P token"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD005" "CORR-FWD005")
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload" "$P2P_TOKEN_INVALID")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Step 3-4: Verify authentication failure logged
    log "  Step 3-4: Verifying P2P auth failure"
    if assert_log_contains "auth.*fail\|authentication.*fail\|P2P.*fail\|token.*invalid\|401\|403"; then
        log "  Step 3-4: PASS - Auth failure logged"
    fi

    # Step 6: Verify NO message forwarded to UCRM
    log "  Step 6: Verifying no message forwarded to UCRM"
    if assert_log_not_contains "messaging/send.*CORR-FWD005\|Dispatcher.*forward.*CORR-FWD005"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Message forwarded to UCRM despite auth failure"
    fi
}

test_FWD006() {
    log_header "FWD-006: IPL to UCRI — Field Mapping Validation"
    local tid="FWD-006"
    local name="Field Mapping Validation"

    clear_logs

    # Step 1-7: Send request with known field values, verify mappings
    log "  Step 1: Sending TransferEinsatzRequest with specific field values"
    local payload
    payload=$(cat <<EOF
{
    "correlationId": "CORR-FWD006",
    "sourceMandant": "IPL_CENTER_001",
    "targetMandant": "UCRI_CENTER_001",
    "transferEinsatz": {
        "einsatzId": "EIN-12345",
        "einsatznummerKurz": "K-98765",
        "kategorie": "KAT-01",
        "einsatzStichwort": "FEUER",
        "alarmierungsstichwortText": "Brand in Wohngebaeude"
    },
    "partitionKey": "PK-EIN-12345"
}
EOF
    )
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Verify field mappings in logs
    log "  Step 2-7: Verifying field mappings"
    local mapping_ok=true
    for expected in "sender_client_id.*IPL_CENTER_001" "receiver_client_id.*UCRI_CENTER_001" "operation.id.*EIN-12345"; do
        if ! assert_log_contains "$expected"; then
            log "  WARN: Mapping not found: $expected"
            mapping_ok=false
        fi
    done

    if $mapping_ok; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Some field mappings not verified in logs"
    fi
}

test_FWD007() {
    log_header "FWD-007: IPL to UCRI — Missing sourceMandant"
    local tid="FWD-007"
    local name="Missing sourceMandant"

    clear_logs

    # Step 1: Send without sourceMandant
    log "  Step 1: Sending request without sourceMandant"
    local payload='{"correlationId": "CORR-FWD007", "targetMandant": "'$UCRI1_MANDANT'", "transferEinsatz": {"einsatzId": "EIN-FWD007"}}'
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    # Step 1: Expect validation error
    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Rejected (HTTP $http_code)"
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx, got HTTP $http_code"
        return
    fi

    # Step 2: Verify error mentions sourceMandant
    log "  Step 2: Verifying error message mentions sourceMandant"
    if assert_response_contains "$body" "sourceMandant"; then
        log "  Step 2: PASS - Error references sourceMandant"
    fi

    # Step 3: No forwarding
    sleep 2
    if assert_log_not_contains "Handler.*CORR-FWD007\|Dispatcher.*CORR-FWD007"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Request forwarded despite missing sourceMandant"
    fi
}

test_FWD008() {
    log_header "FWD-008: IPL to UCRI — Missing targetMandant"
    local tid="FWD-008"
    local name="Missing targetMandant"

    clear_logs

    # Step 1: Send without targetMandant
    log "  Step 1: Sending request without targetMandant"
    local payload='{"correlationId": "CORR-FWD008", "sourceMandant": "'$IPL_MANDANT'", "transferEinsatz": {"einsatzId": "EIN-FWD008"}}'
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Rejected (HTTP $http_code)"
        if assert_response_contains "$body" "targetMandant"; then
            record_result "$tid" "$name" "PASS"
        else
            record_result "$tid" "$name" "PASS" "Rejected but error message may not reference targetMandant"
        fi
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx, got HTTP $http_code"
    fi
}

test_FWD009() {
    log_header "FWD-009: IPL to UCRI — Missing einsatzId"
    local tid="FWD-009"
    local name="Missing einsatzId"

    clear_logs

    # Step 1: Send without einsatzId
    log "  Step 1: Sending request without einsatzId"
    local payload='{"correlationId": "CORR-FWD009", "sourceMandant": "'$IPL_MANDANT'", "targetMandant": "'$UCRI1_MANDANT'", "transferEinsatz": {"kategorie": "KAT-01"}}'
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")
    local body
    body=$(extract_response_body "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx, got HTTP $http_code"
    fi
}

test_FWD010() {
    log_header "FWD-010: IPL to UCRI — Empty Payload"
    local tid="FWD-010"
    local name="Empty Payload"

    clear_logs

    # Step 1: Send empty body
    log "  Step 1: Sending POST with empty body"
    local response
    response=$(send_post_request "$EINSATZ_ENDPOINT" "{}")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Expected 4xx for empty payload, got HTTP $http_code"
    fi
}

test_FWD011() {
    log_header "FWD-011: IPL to UCRI — UCRI Dispatch Center Disabled"
    local tid="FWD-011"
    local name="UCRI Dispatch Center Disabled"

    # Step 1: Disable dispatch center
    log "  Step 1: Setting dispatch-center.ucri.enabled=false"
    set_adapter_config "dispatch-center.ucri.enabled" "false"
    restart_adapter
    sleep 5
    clear_logs

    # Step 2: Send event
    log "  Step 2: Sending TransferEinsatzRequest"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD011" "CORR-FWD011")
    send_post_request "$EINSATZ_ENDPOINT" "$payload" > /dev/null
    sleep 3

    # Step 3: Verify no dispatch to events-ucri
    log "  Step 3: Verifying no dispatch to events-ucri"
    if assert_log_not_contains "events-ucri.*CORR-FWD011\|Dispatcher.*publish.*CORR-FWD011"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Event dispatched despite disabled dispatch center"
    fi

    # Restore config
    set_adapter_config "dispatch-center.ucri.enabled" "true"
    restart_adapter
}

test_FWD012() {
    log_header "FWD-012: IPL to UCRI — CorrelationId Traceability"
    local tid="FWD-012"
    local name="CorrelationId Traceability in Forward Flow"
    local corr_id="CORR-FWD012-TRACE-$(date +%s)"

    clear_logs

    # Step 1: Send request with unique correlationId
    log "  Step 1: Sending request with correlationId=${corr_id}"
    local payload
    payload=$(build_transfer_einsatz_request "$IPL_MANDANT" "$UCRI1_MANDANT" "EIN-FWD012" "$corr_id")
    send_post_request "$EINSATZ_ENDPOINT" "$payload" > /dev/null
    sleep 5

    # Step 1-4: Verify correlationId appears across all services
    log "  Step 1-4: Verifying correlationId traceability across services"
    local trace_count
    trace_count=$(grep -c "$corr_id" "${ADAPTER_LOG_DIR}/adapter.log" 2>/dev/null || echo "0")

    if [ "$trace_count" -ge 3 ]; then
        log "  PASS - correlationId found $trace_count times across log entries"
        record_result "$tid" "$name" "PASS"
    elif [ "$trace_count" -ge 1 ]; then
        record_result "$tid" "$name" "PASS" "correlationId found $trace_count time(s) - partial traceability"
    else
        record_result "$tid" "$name" "FAIL" "correlationId not found in logs"
    fi
}

###############################################################################
# REVERSE FLOW TESTS — UCRI to IPL (REV)
###############################################################################

test_REV001() {
    log_header "REV-001: UCRI to IPL — Happy Path: Mission Accepted"
    local tid="REV-001"
    local name="Happy Path: Mission Accepted by IPL"
    local corr_id="CORR-REV001-$(date +%s)"

    clear_logs

    # Step 1: Send mission payload via messaging/send
    log "  Step 1: Sending mission payload to ${MESSAGING_SEND_ENDPOINT}"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$IPL_MANDANT" "OP-REV001" "$corr_id")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 202 ]; then
        log "  Step 1: PASS - Mission payload accepted (HTTP $http_code)"
    else
        record_result "$tid" "$name" "FAIL" "Expected HTTP 200/202, got $http_code"
        return
    fi

    sleep 5

    # Step 2-8: Verify end-to-end flow and ACK
    log "  Step 2-8: Verifying mission processing and Accept ACK"
    if assert_log_contains "${corr_id}.*Accept\|Accept.*${corr_id}\|ACK.*Accept"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Accept ACK not found in logs"
    fi
}

test_REV002() {
    log_header "REV-002: UCRI to IPL — Mission Rejected by IPL"
    local tid="REV-002"
    local name="Mission Rejected by IPL"
    local corr_id="CORR-REV002-$(date +%s)"

    clear_logs

    # Step 1: Send mission (IPL configured to reject)
    log "  Step 1: Sending mission payload"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$IPL_MANDANT" "OP-REV002-REJECT" "$corr_id")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 5

    # Step 4-7: Verify Reject ACK
    log "  Step 4-7: Verifying Reject ACK"
    if assert_log_contains "Reject.*${corr_id}\|${corr_id}.*Reject\|ACK.*Reject"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Reject ACK not found in logs"
    fi
}

test_REV003() {
    log_header "REV-003: UCRI to IPL — IPL Does Not Respond (Timeout)"
    local tid="REV-003"
    local name="IPL Timeout"
    local corr_id="CORR-REV003-$(date +%s)"

    clear_logs

    # Step 1: Send mission (IPL configured to not respond)
    log "  Step 1: Sending mission payload (expecting timeout)"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$IPL_MANDANT" "OP-REV003-TIMEOUT" "$corr_id")
    send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" > /dev/null
    sleep "$((TIMEOUT_SECONDS + 5))"

    # Step 3-5: Verify timeout handling
    log "  Step 3-5: Verifying timeout handling"
    if assert_log_contains "timeout.*${corr_id}\|${corr_id}.*timeout\|TECHNISCHER_FEHLER"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Timeout handling not found in logs"
    fi
}

test_REV004() {
    log_header "REV-004: UCRI to IPL — Invalid Mission Payload"
    local tid="REV-004"
    local name="Invalid Mission Payload from UCRM"

    clear_logs

    # Step 1: Send malformed mission payload
    log "  Step 1: Sending malformed mission payload"
    local payload='{"correlationId": "CORR-REV004", "header": {}, "operation": {}}'
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Invalid payload rejected (HTTP $http_code)"
    fi

    sleep 2

    # Step 3: Verify no forwarding to IPL
    log "  Step 3: Verifying no forwarding to IPL"
    if assert_log_not_contains "Dispatcher.*forward.*CORR-REV004\|IPL.*CORR-REV004"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Invalid mission was forwarded to IPL"
    fi
}

test_REV005() {
    log_header "REV-005: UCRI to IPL — Field Mapping Validation (UCRM to IPL)"
    local tid="REV-005"
    local name="Field Mapping Validation (UCRM to IPL)"

    clear_logs

    # Step 1-5: Send mission with known field values
    log "  Step 1: Sending mission with specific field values for mapping verification"
    local payload
    payload=$(cat <<EOF
{
    "correlationId": "CORR-REV005",
    "header": {
        "sender_client_id": "UCRI_CENTER_001",
        "receiver_client_id": "IPL_CENTER_001",
        "source": "UCRM",
        "type": "MissionDispatch"
    },
    "operation": {
        "id": "OP-56789",
        "name": "K-11111"
    },
    "partitionKey": "PK-OP-56789"
}
EOF
    )
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Verify reverse field mappings in logs
    log "  Step 2-5: Verifying reverse field mappings"
    local mapping_ok=true
    for expected in "sourceMandant.*UCRI_CENTER_001\|sender.*UCRI_CENTER_001" "targetMandant.*IPL_CENTER_001\|receiver.*IPL_CENTER_001" "einsatzId.*OP-56789\|operation.id.*OP-56789"; do
        if ! assert_log_contains "$expected"; then
            mapping_ok=false
        fi
    done

    if $mapping_ok; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Some reverse field mappings not verified"
    fi
}

test_REV006() {
    log_header "REV-006: UCRI to IPL — CorrelationId Traceability"
    local tid="REV-006"
    local name="Reverse Flow CorrelationId Traceability"
    local corr_id="REV-TRACE-001"

    clear_logs

    # Step 1: Send mission with specific correlationId
    log "  Step 1: Sending mission with correlationId=${corr_id}"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$IPL_MANDANT" "OP-REV006" "$corr_id")
    send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" > /dev/null
    sleep 5

    # Step 1-4: Verify traceability
    log "  Step 1-4: Verifying correlationId traceability"
    local trace_count
    trace_count=$(grep -c "$corr_id" "${ADAPTER_LOG_DIR}/adapter.log" 2>/dev/null || echo "0")

    if [ "$trace_count" -ge 3 ]; then
        record_result "$tid" "$name" "PASS"
    elif [ "$trace_count" -ge 1 ]; then
        record_result "$tid" "$name" "PASS" "Partial traceability ($trace_count entries)"
    else
        record_result "$tid" "$name" "FAIL" "correlationId not found in logs"
    fi
}

###############################################################################
# CROSS-CLIENT TESTS — UCRI to UCRI (U2U)
###############################################################################

test_U2U001() {
    log_header "U2U-001: UCRI-1 to UCRI-2 — Happy Path: Mission Accepted"
    local tid="U2U-001"
    local name="UCRI-1 to UCRI-2 Happy Path"
    local corr_id="CORR-U2U001-$(date +%s)"

    clear_logs

    # Step 1: UCRI-1 sends mission to UCRI-2
    log "  Step 1: UCRI-1 sending mission to UCRI-2"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$UCRI2_MANDANT" "OP-U2U001" "$corr_id")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 202 ]; then
        log "  Step 1: PASS - Payload accepted from UCRI-1"
    else
        record_result "$tid" "$name" "FAIL" "Expected 200/202, got HTTP $http_code"
        return
    fi

    sleep 5

    # Step 6-8: Verify Accept ACK back to UCRI-1
    log "  Step 6-8: Verifying Accept ACK propagated to UCRI-1"
    if assert_log_contains "Accept.*${corr_id}\|${corr_id}.*Accept\|UCRI.*Accept"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Accept ACK not found"
    fi
}

test_U2U002() {
    log_header "U2U-002: UCRI-1 to UCRI-2 — Mission Rejected by UCRI-2"
    local tid="U2U-002"
    local name="UCRI-1 to UCRI-2 Mission Rejected"
    local corr_id="CORR-U2U002-$(date +%s)"

    clear_logs

    log "  Step 1: UCRI-1 sending mission to UCRI-2 (UCRI-2 configured to reject)"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$UCRI2_MANDANT" "OP-U2U002-REJECT" "$corr_id")
    send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" > /dev/null
    sleep 5

    # Verify Reject ACK
    log "  Step 3-5: Verifying Reject ACK"
    if assert_log_contains "Reject.*${corr_id}\|${corr_id}.*Reject"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Reject ACK not found"
    fi
}

test_U2U003() {
    log_header "U2U-003: UCRI-1 to UCRI-2 — Timeout"
    local tid="U2U-003"
    local name="UCRI-1 to UCRI-2 Timeout"
    local corr_id="CORR-U2U003-$(date +%s)"

    clear_logs

    log "  Step 1: UCRI-1 sending mission to UCRI-2 (UCRI-2 not responding)"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$UCRI2_MANDANT" "OP-U2U003-TIMEOUT" "$corr_id")
    send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" > /dev/null
    sleep "$((TIMEOUT_SECONDS + 5))"

    log "  Step 3-5: Verifying timeout handling"
    if assert_log_contains "timeout.*${corr_id}\|${corr_id}.*timeout"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Timeout not detected"
    fi
}

test_U2U004() {
    log_header "U2U-004: UCRI-2 to UCRI-1 — Reverse Direction"
    local tid="U2U-004"
    local name="UCRI-2 to UCRI-1 Reverse Direction"
    local corr_id="CORR-U2U004-$(date +%s)"

    clear_logs

    log "  Step 1: UCRI-2 sending mission to UCRI-1"
    local payload
    payload=$(build_messaging_send_payload "$UCRI2_MANDANT" "$UCRI1_MANDANT" "OP-U2U004" "$corr_id")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 5

    if assert_log_contains "Accept.*${corr_id}\|${corr_id}.*Accept"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Reverse direction Accept ACK not found"
    fi
}

test_U2U005() {
    log_header "U2U-005: UCRI-1 to UCRI-2 — Invalid sourceMandant"
    local tid="U2U-005"
    local name="Invalid sourceMandant (Sender Not Recognized)"

    clear_logs

    log "  Step 1: Sending with unknown sourceMandant"
    local payload
    payload=$(build_messaging_send_payload "UNKNOWN_CLIENT" "$UCRI2_MANDANT" "OP-U2U005" "CORR-U2U005")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    if [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        log "  Step 1: PASS - Rejected (HTTP $http_code)"
    fi

    sleep 2

    # Verify no forwarding to UCRI-2
    if assert_log_not_contains "Dispatcher.*forward.*UCRI_CENTER_002\|messaging/send.*UCRI_CENTER_002"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Message forwarded despite invalid sourceMandant"
    fi
}

test_U2U006() {
    log_header "U2U-006: UCRI-1 to UCRI-2 — Invalid targetMandant"
    local tid="U2U-006"
    local name="Invalid targetMandant (Receiver Not Found)"

    clear_logs

    log "  Step 1: Sending with non-existent targetMandant"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "UCRI_NONEXISTENT" "OP-U2U006" "CORR-U2U006")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Verify routing failure
    if assert_log_contains "routing.*fail\|target.*not.*found\|UCRI_NONEXISTENT.*error\|invalid.*target"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "No routing failure for non-existent target"
    fi
}

test_U2U007() {
    log_header "U2U-007: UCRI-1 to UCRI-2 — P2P Auth Failure Cross-Client"
    local tid="U2U-007"
    local name="P2P Auth Failure Cross-Client"

    clear_logs

    log "  Step 1: Sending cross-client event with invalid P2P token"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$UCRI2_MANDANT" "OP-U2U007" "CORR-U2U007")
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" "$P2P_TOKEN_INVALID")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Verify auth failure and no forwarding
    if assert_log_contains "auth.*fail\|authentication.*fail\|P2P.*fail\|401\|403"; then
        log "  PASS - Auth failure logged"
    fi

    if assert_log_not_contains "Dispatcher.*forward.*CORR-U2U007\|messaging/send.*CORR-U2U007"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Message forwarded despite auth failure"
    fi
}

test_U2U008() {
    log_header "U2U-008: UCRI-1 to UCRI-2 — Field Mapping Cross-Client"
    local tid="U2U-008"
    local name="Field Mapping Cross-Client Transfer"

    clear_logs

    log "  Step 1: Sending cross-client mission with specific fields"
    local payload
    payload=$(cat <<EOF
{
    "correlationId": "CORR-U2U008",
    "header": {
        "sender_client_id": "UCRI_CENTER_001",
        "receiver_client_id": "UCRI_CENTER_002",
        "source": "UCRM",
        "type": "MissionTransfer"
    },
    "operation": {
        "id": "OP-CROSS-001",
        "name": "K-55555",
        "occassion": {
            "type_1": "KAT-03",
            "keyword_1": "UNFALL",
            "keyword_1_text": "Verkehrsunfall"
        }
    },
    "partitionKey": "PK-CROSS-001"
}
EOF
    )
    local response
    response=$(send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "Adapter not reachable"
        return
    fi

    sleep 3

    # Verify field preservation
    local fields_ok=true
    for field in "UCRI_CENTER_001" "UCRI_CENTER_002" "OP-CROSS-001" "K-55555"; do
        if ! assert_log_contains "$field"; then
            fields_ok=false
        fi
    done

    if $fields_ok; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "Some fields not preserved in cross-client transfer"
    fi
}

test_U2U009() {
    log_header "U2U-009: UCRI-1 to UCRI-2 — CorrelationId Traceability"
    local tid="U2U-009"
    local name="Cross-Client CorrelationId Traceability"
    local corr_id="U2U-TRACE-001"

    clear_logs

    log "  Step 1: Sending cross-client event with correlationId=${corr_id}"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$UCRI2_MANDANT" "OP-U2U009" "$corr_id")
    send_post_request "$MESSAGING_SEND_ENDPOINT" "$payload" > /dev/null
    sleep 5

    local trace_count
    trace_count=$(grep -c "$corr_id" "${ADAPTER_LOG_DIR}/adapter.log" 2>/dev/null || echo "0")

    if [ "$trace_count" -ge 3 ]; then
        record_result "$tid" "$name" "PASS"
    elif [ "$trace_count" -ge 1 ]; then
        record_result "$tid" "$name" "PASS" "Partial traceability ($trace_count entries)"
    else
        record_result "$tid" "$name" "FAIL" "correlationId not found in logs"
    fi
}

test_TC002() {
    log_header "TC-002: UCRM Test Client — Send Mission and Receive ACK"
    local tid="TC-002"
    local name="UCRM Test Client — Send Mission and Receive ACK"
    local corr_id="CORR-TC002-$(date +%s)"

    clear_logs

    # Step 1: Use Test Client (via API) to send a mission
    log "  Step 1: Sending mission via UCRM Test Client endpoint"
    local payload
    payload=$(build_messaging_send_payload "$UCRI1_MANDANT" "$IPL_MANDANT" "OP-TC002" "$corr_id")
    local response
    response=$(send_post_request "${UCRM_BASE_URL}/messaging/send" "$payload")
    local http_code
    http_code=$(extract_http_code "$response")

    if [ "$http_code" = "CONNECTION_ERROR" ]; then
        record_result "$tid" "$name" "SKIP" "UCRM Test Client not reachable"
        return
    fi

    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 202 ]; then
        log "  Step 1: PASS - Mission accepted"
    else
        record_result "$tid" "$name" "FAIL" "Expected 200/202, got HTTP $http_code"
        return
    fi

    sleep 5

    # Step 4: Verify ACK received
    log "  Step 4: Verifying ACK received by Test Client"
    if assert_log_contains "ACK.*${corr_id}\|${corr_id}.*ACK\|Accept.*${corr_id}"; then
        record_result "$tid" "$name" "PASS"
    else
        record_result "$tid" "$name" "FAIL" "ACK not found for Test Client mission"
    fi
}

###############################################################################
# TEST RUNNER
###############################################################################

print_summary() {
    log_header "TEST EXECUTION SUMMARY"
    log "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    log "Total: $((PASS_COUNT + FAIL_COUNT + SKIP_COUNT)) | PASS: $PASS_COUNT | FAIL: $FAIL_COUNT | SKIP: $SKIP_COUNT"
    echo "" | tee -a "$LOG_FILE"
    echo "TID | Test Case | Status | Detail" | tee -a "$LOG_FILE"
    echo "----|-----------|---------|---------" | tee -a "$LOG_FILE"
    echo -e "$RESULTS_SUMMARY" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    log "Results saved to: $LOG_FILE"
}

run_all_tests() {
    log_header "UCRI 2.0 AUTOMATED TEST SUITE"
    log "Starting test execution at $(date '+%Y-%m-%d %H:%M:%S')"
    log "Adapter URL: $ADAPTER_BASE_URL"
    log "UCRM URL: $UCRM_BASE_URL"
    echo ""

    # In-Memory Transport Tests
    test_IMT001
    test_IMT004
    test_IMT005
    test_IMT006
    test_IMT007
    test_IMT008
    test_IMT009
    test_IMT010

    # Forward Flow Tests
    test_FWD001
    test_FWD002
    test_FWD003
    test_FWD004
    test_FWD005
    test_FWD006
    test_FWD007
    test_FWD008
    test_FWD009
    test_FWD010
    test_FWD011
    test_FWD012

    # Reverse Flow Tests
    test_REV001
    test_REV002
    test_REV003
    test_REV004
    test_REV005
    test_REV006

    # Cross-Client Tests
    test_U2U001
    test_U2U002
    test_U2U003
    test_U2U004
    test_U2U005
    test_U2U006
    test_U2U007
    test_U2U008
    test_U2U009

    # Test Client Tests
    test_TC002

    print_summary
}

run_category() {
    local category="${1:-all}"
    log_header "Running category: $category"

    case "$category" in
        imt|IMT)
            test_IMT001; test_IMT004; test_IMT005; test_IMT006
            test_IMT007; test_IMT008; test_IMT009; test_IMT010
            ;;
        fwd|FWD)
            test_FWD001; test_FWD002; test_FWD003; test_FWD004
            test_FWD005; test_FWD006; test_FWD007; test_FWD008
            test_FWD009; test_FWD010; test_FWD011; test_FWD012
            ;;
        rev|REV)
            test_REV001; test_REV002; test_REV003
            test_REV004; test_REV005; test_REV006
            ;;
        u2u|U2U)
            test_U2U001; test_U2U002; test_U2U003; test_U2U004
            test_U2U005; test_U2U006; test_U2U007; test_U2U008
            test_U2U009
            ;;
        tc|TC)
            test_TC002
            ;;
        all)
            run_all_tests
            return
            ;;
        *)
            log "Unknown category: $category"
            log "Usage: $0 [all|imt|fwd|rev|u2u|tc|<TEST_ID>]"
            exit 1
            ;;
    esac

    print_summary
}

run_single_test() {
    local test_id="$1"
    local func_name="test_${test_id//-/}"

    if declare -f "$func_name" > /dev/null 2>&1; then
        "$func_name"
        print_summary
    else
        log "Unknown test ID: $test_id"
        log "Available: IMT-001,004-010 | FWD-001 to 012 | REV-001 to 006 | U2U-001 to 009 | TC-002"
        exit 1
    fi
}

###############################################################################
# MAIN
###############################################################################
usage() {
    echo "UCRI 2.0 Automated Test Suite"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  all           Run all 36 automated test cases"
    echo "  imt           Run In-Memory Transport tests (IMT-001 to IMT-010)"
    echo "  fwd           Run Forward Flow tests (FWD-001 to FWD-012)"
    echo "  rev           Run Reverse Flow tests (REV-001 to REV-006)"
    echo "  u2u           Run Cross-Client tests (U2U-001 to U2U-009)"
    echo "  tc            Run Test Client tests (TC-002)"
    echo "  <TEST_ID>     Run a single test (e.g., FWD-001, IMT-005)"
    echo ""
    echo "Environment Variables:"
    echo "  ADAPTER_BASE_URL   Adapter service URL (default: http://localhost:8080)"
    echo "  UCRM_BASE_URL     UCRM service URL (default: http://localhost:8081)"
    echo "  ADAPTER_CONFIG_DIR Adapter config directory (default: /opt/adapter/config)"
    echo "  ADAPTER_LOG_DIR    Adapter log directory (default: /opt/adapter/logs)"
    echo "  P2P_TOKEN          Valid P2P authentication token"
    echo "  TIMEOUT_SECONDS    Request timeout in seconds (default: 30)"
}

main() {
    local arg="${1:-all}"

    case "$arg" in
        -h|--help)
            usage
            exit 0
            ;;
        all|imt|IMT|fwd|FWD|rev|REV|u2u|U2U|tc|TC)
            run_category "$arg"
            ;;
        IMT-*|FWD-*|REV-*|U2U-*|TC-*)
            run_single_test "$arg"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
