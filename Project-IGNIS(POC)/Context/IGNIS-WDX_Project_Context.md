# Project Context: IGNIS-WDX Integration (IPL-WDX Adapter)

## Application
- **Name:** Adapter Integration Service (AdapterIntegration Flottenserver)
- **Type:** API / Integration Service
- **Domain:** Emergency Services / Incident Dispatch Integration Platform

## Tech Stack
- **Frontend:** Not applicable (backend service only)
- **Backend:** Java 17, Quarkus Framework
- **Database:** Not specified (prototype excludes persistence)
- **API Type:** 
  - REST (IPL-facing interface)
  - gRPC over HTTP/2 (WDX-facing interface)
- **Protocol:** Protocol Buffers (Protobuf) for WDX communication

## Environment
- **Test URL:** `wdx3-test.cloud.ise-cobra.de:443`
- **Dev URL:** Not specified in requirements
- **Staging URL:** Not specified in requirements
- **Prod URL:** Not specified in requirements

## System Architecture

### Components
| Component | Description |
|-----------|-------------|
| Sender System (IPL) | Source system initiating incident dispatch |
| AdapterIntegration Flottenserver | Integration component translating between IPL and WDX |
| WDX3 Flottenserver | Receiver / operational hub for incident distribution |
| IPL Mock Service | Drop-in replacement simulating IPL interface (for prototype) |
| Partner Control Center | Receives and processes incidents (conceptual) |

### Target Services
- **WDX Operation Service:** `ise.wdx.operation.v1.WDX3OperationService`
- **WDX Patient Service:** `ise.wdx.patient.v1.WDX3PatientService` (not covered in prototype)

## Communication Flows

### IPL → WDX Flow
1. Sender System (IPL) submits incident to AdapterIntegration
2. AdapterIntegration transforms to WDX-compliant message
3. AdapterIntegration forwards to WDX3 Flottenserver
4. WDX distributes to partner control centers

### WDX → IPL Flow
1. WDX sends Accept/Reject feedback events
2. AdapterIntegration receives and translates to IPL format
3. AdapterIntegration forwards to IPL system

## Key Events/Operations

| Event Name | Direction | Description |
|------------|-----------|-------------|
| CreateRequest | IPL → WDX | Create new operation/incident in WDX |
| AcceptOperation | WDX → IPL | Feedback event for acceptance |
| RejectOperation | WDX → IPL | Feedback event for rejection |

## IPL Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /einsatztransfer/erzeugeEinsatz | POST | Mission payload submission |
| /einsatztransfer/quittiereTranferEinsatz | POST | Receive Accept/Reject feedback |

## Key Constraints

### Technical Constraints
- Authentication via certificate and login token (ise_auth_token)
- Each request contains WDX3Header with sender_client_id and receiver_client_id
- Every event must be acknowledged within **10 seconds**
- Patient events arrive on separate stream from operation events
- Streaming connection filtered using enum value = `NEW` (only newly created events)

### Prototype Constraints (Current Release)
- No database or cache layer (no persistence)
- No storage of ID mappings or control center information
- Patient data within mission dispatch messages is not processed
- No entity or system identifier mapping logic
- No retry mechanisms, fallback routing, or automatic error recovery
- Mock IPL service used instead of real IPL system

### Deployment Requirements
| Component | Requirement | Notes |
|-----------|-------------|-------|
| Java Version | Java 17+ | OpenJDK recommended |
| Operating System | Linux (recommended) | Windows compatible |
| Disk Space | 1 GB minimum | Additional space for logs |
| RAM | 512 MB minimum (2 GB recommended) | For production environments |
| Network | Outbound HTTPS access | To wdx3-test.cloud.ise-cobra.de:443 |
| Certificates | Client TLS certificates | Must be valid and not expired |

### Certificate Requirements
- `wdx3-test-client.crt` (Client certificate in PEM format)
- `wdx3-test-client.pk8` (Client private key in PKCS#8 format)

## Data Mapping Overview

### TransferEinsatz (IPL) → Operation (WDX)

| IPL Field | WDX Field | Mapping Logic |
|-----------|-----------|---------------|
| sourceMandant | header.sender_client_id | 1:1 Mapping |
| targetMandant | header.receiver_client_id | 1:1 Mapping |
| (no field) | CreateRequest.send_time | Set by Adapter at send time |
| transferEinsatz.einsatzId | operation.id | 1:1 Mapping |
| transferEinsatz.einsatznummerKurz | operation.name | 1:1 Mapping |
| transferEinsatz.kategorie | operation.occassion.type_1 | 1:1 Mapping |
| transferEinsatz.einsatzStichwort | operation.occassion.keyword_1 | 1:1 Mapping |
| transferEinsatz.alarmierungsstichwortText | operation.occassion.keyword_1_text | 1:1 Mapping |

### Patient Data Mapping (Java → Protobuf)

| Java Field | Protobuf Field | Mapping Logic |
|------------|----------------|---------------|
| transferId | Patient.id | 1:1 |
| vorname | Patient.person_data.firstname | 1:1 |
| nachname | Patient.person_data.lastname | 1:1 |
| geburtsdatum | Patient.person_data.birth_date | Conversion: java.util.Date → google.protobuf.Timestamp |
| geschlecht | Patient.person_data.gender | Enum mapping: GeschlechtEnum → wdx.v1.Person enum |
| wohnAdresse | Patient.person_data.location.street | Parse street name from free text |
| wohnAdresse | Patient.person_data.location.house_number | Parse house number from free text |
| wohnPlz | Patient.person_data.location.postal_code | Extract digits only |

## Directory Structure
```
release-package-0.1.0/
├── AdditionInfo.txt                    # Curl and WDX user information
├── TransferEinsatzRequest.json         # IPL Sample mission request
└── adapter-integration/
    ├── adapter-integration-1.0.0-SNAPSHOT-runner.jar  # Main application JAR
    ├── certs/
    │   ├── wdx3-test-client.crt        # Client certificate (PEM)
    │   └── wdx3-test-client.pk8        # Client private key (PKCS#8)
    └── config/
        └── application.properties       # Configuration file
```

## Configuration
- All configuration managed through `application.properties` file
- Log path: `/opt/local/acp/logs/adapter-integration/adapter-integration.log`

## Known Limitations (Prototype)
- Mock IPL service only; real IPL system integration deferred
- No data persistence or caching
- Testing performed in controlled environments only
- Single streaming filter configuration (enum = NEW)
