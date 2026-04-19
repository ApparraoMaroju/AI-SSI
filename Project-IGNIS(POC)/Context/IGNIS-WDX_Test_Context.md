# Testing Context: IGNIS-WDX Integration (IPL-WDX Adapter)

## Scope

### In Scope
- **WDX Streaming Connection:** Functional streaming integration to WDX with event filtering (enum = NEW)
- **Bi-directional Mission Flow:** Complete IPL → WDX → IPL mission dispatch cycle
- **Message Translation:** IPL to WDX format conversion and vice versa
- **Event Processing:** Full WDX → IPL → WDX event handling
- **IPL Mock Service:** Drop-in replacement simulating IPL interface behavior
- **Log-based Validation:** Comprehensive logging of all message conversions and payloads
- **CreateRequest Event:** Create new operation in WDX (mission dispatch)
- **AcceptOperation Event:** Feedback event for acceptance
- **RejectOperation Event:** Feedback event for rejection
- **Field Mapping Validation:** TransferEinsatz to Operation mapping
- **Acknowledgment Handling:** 10-second acknowledgment requirement

### Out of Scope
- Patient events (CreateRequest/updates under `ise.wdx.patient.v1.WDX3PatientService`)
- Patient data processing within mission dispatch messages
- Persistence & Caching (no database or cache layer)
- Advanced ID Mapping (patient IDs, control center IDs, system identifiers)
- Retry & Failover Logic (automatic retry, fallback routing, error recovery)
- Real IPL system integration (mock service used)
- Performance benchmarking (not explicitly specified)

## Test Data

| Data Type | Value | Purpose |
|-----------|-------|---------|
| TransferEinsatzRequest | JSON payload with mission data | IPL to WDX mission flow |
| Valid sourceMandant | Sender client identifier | Header mapping validation |
| Valid targetMandant | Receiver client identifier | Header mapping validation |
| Valid einsatzId | Operation identifier | Operation ID mapping |
| Valid einsatznummerKurz | Short incident number | Operation name mapping |
| Valid kategorie | Incident category code | Occasion type_1 mapping |
| Valid einsatzStichwort | Alarm keyword (coded) | Occasion keyword_1 mapping |
| WDX AcceptOperation | Accept feedback event | WDX to IPL acceptance flow |
| WDX RejectOperation | Reject feedback event | WDX to IPL rejection flow |
| Patient transferId | Patient identifier | Patient ID mapping |
| Patient vorname | First name string | Person data firstname mapping |
| Patient nachname | Last name string | Person data lastname mapping |
| Patient geburtsdatum | java.util.Date value | Date to Timestamp conversion |
| Patient geschlecht | GeschlechtEnum value | Gender enum mapping |
| Patient wohnAdresse | Free text address | Address parsing (street + house number) |
| Patient wohnPlz | Postal code string | Postal code extraction |

## Test Environment

- **Tool:** Postman (primary test tool)
- **WDX Test System:** wdx3-test.cloud.ise-cobra.de:443
- **Protocol:** gRPC over HTTP/2 (WDX), REST (IPL)
- **Authentication:** Certificate + login token (ise_auth_token)
- **OS:** Linux (recommended), Windows compatible
- **Java Version:** Java 17+ (OpenJDK recommended)

## Dependencies

### Required Services
- WDX3 Flottenserver must be accessible
- IPL Mock Service must be running and configured
- Adapter Integration Service must be deployed and started

### Required Certificates
- `wdx3-test-client.crt` (Client certificate in PEM format) - Must be valid and not expired
- `wdx3-test-client.pk8` (Client private key in PKCS#8 format)

### Required Configuration
- `application.properties` properly configured
- Logs directory must exist and be writable: `/opt/local/acp/logs/adapter-integration/`
- Outbound HTTPS access to WDX test environment

### Pre-Test Setup
- Ensure logs directory specified in configuration exists and is writable
- Verify certificates are valid and properly placed in `certs/` directory
- Confirm network connectivity to WDX3 test endpoint

## Test Scenarios

### Scenario 1: IPL → Adapter → WDX → Adapter → IPL Mock (Mission Flow)
1. Trigger a mission request using Postman (acting as IPL)
2. Validate translation into WDX format (CreateRequest)
3. Ensure WDX processes and sends acknowledgment
4. Verify ACK is translated back to IPL format
5. Confirm IPL ACK appears in mock service logs

### Scenario 2: WDX → Adapter → IPL Mock → Adapter → WDX (Event Flow)
1. Trigger an event from WDX test system (Accept/Reject)
2. Validate translation to IPL format
3. Verify IPL Mock Service receives the event
4. Ensure IPL mock ACK flows back to WDX via adapter
5. Confirm WDX receives translated acknowledgment

### Scenario 3: Message Conversion Validation
1. Send mission request with all mappable fields
2. Verify all field mappings in adapter logs
3. Validate TransferEinsatz → Operation conversion
4. Verify Patient data field mappings (if applicable)
5. Confirm no data loss in translation

### Scenario 4: Acknowledgment Timing
1. Send CreateRequest to WDX
2. Verify acknowledgment is received within 10 seconds
3. Log timing metrics for validation

## Validation Methods

### Log-Based Verification
All intermediate conversions, payloads, and ACK responses validated through logs at:
- Adapter Integration Service logs
- IPL Mock Service logs
- WDX response logs (if available)

### Key Validation Points
- Receipt and transmission of WDX events through streaming
- Translation of IPL mission requests to WDX-compatible formats
- Translation of incoming WDX requests/ACKs into IPL-style formats
- Round-trip functional testing completion
- Event filtering (enum = NEW) working correctly

## Acceptance Criteria

- [ ] The AdapterIntegration Flottenserver successfully sends the CreateRequest event to WDX
- [ ] WDX confirms receipt on the transport level
- [ ] Accept/Reject events are received and acknowledged within 10 seconds
- [ ] IPL Mock Service correctly receives translated events
- [ ] All field mappings execute correctly per specification
- [ ] Bi-directional message flow completes successfully
- [ ] All message conversions logged and verifiable

## Known Issues

### Current Prototype Limitations
- Mock IPL service only; real IPL system integration deferred
- No data persistence or caching implemented
- Testing performed in controlled environments only
- Single streaming filter configuration (enum = NEW)
- Patient data inside mission dispatch message is not processed
- No retry mechanisms or automatic error recovery

### Data Mapping Considerations
- **wohnAdresse parsing:** Best-effort parsing to split into street + house number; may not handle all address formats
- **geburtsdatum conversion:** Requires transformation between java.util.Date and google.protobuf.Timestamp
- **geschlecht mapping:** GeschlechtEnum must map to corresponding wdx.v1.Person enum values

## Test Deliverables Checklist

- [ ] Functional WDX streaming connection validated
- [ ] IPL → WDX → IPL mission flow (end-to-end) tested
- [ ] WDX → IPL → WDX event flow (end-to-end) tested
- [ ] IPL Mock Service request simulation verified
- [ ] ACK response handling confirmed
- [ ] Log-based message validation completed across all components
- [ ] Field mapping accuracy verified
- [ ] 10-second acknowledgment requirement validated
