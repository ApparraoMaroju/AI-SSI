from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from datetime import datetime
import os

doc = Document()

# ── Style helpers ──────────────────────────────────────────
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
style.paragraph_format.space_after = Pt(4)

for level in range(1, 5):
    hs = doc.styles[f'Heading {level}']
    hs.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

def add_table(doc, headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Light Grid Accent 1'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.rows[ri + 1].cells[ci]
            cell.text = str(val)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
    doc.add_paragraph()

def add_checklist(doc, items):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.text = f"☐  {item}"
        p.paragraph_format.space_after = Pt(2)

IMG_DIR = r"c:\Apparao Maroju\AI-SSI\Project-IGNIS(POC)\UCRI2.0-Input"
ipl_to_ucri_img = os.path.join(IMG_DIR, "IPL to UCRI.png")
ucri_to_ipl_img = os.path.join(IMG_DIR, "UCRI to IPL.png")

# ══════════════════════════════════════════════════════════════
# TITLE PAGE
# ══════════════════════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("UCRI 2.0 P2P Integration")
run.bold = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run("IPL ↔ Adapter (Receiver-Handler-Dispatcher) ↔ UCRM")
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0x4A, 0x4A, 0x4A)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = meta.add_run("Structured Knowledge Document")
run.font.size = Pt(14)

doc.add_paragraph()
date_p = doc.add_paragraph()
date_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = date_p.add_run(f"Generated: {datetime.now().strftime('%B %d, %Y')}")
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# TABLE OF CONTENTS (manual)
# ══════════════════════════════════════════════════════════════
doc.add_heading("Table of Contents", level=1)
toc_items = [
    "1. Feature Context",
    "    1.1 Overview",
    "    1.2 User Stories — Adapter",
    "    1.3 User Stories — IPL",
    "    1.4 User Stories — Architecture & Transport",
    "    1.5 Acceptance Criteria",
    "    1.6 API Endpoints",
    "    1.7 Validation Rules",
    "    1.8 ACK Status Values & Error Handling",
    "    1.9 Flow Diagrams",
    "    1.10 Data Mapping",
    "    1.11 Cross-Cutting Concerns",
    "    1.12 Dependencies",
    "2. Project Context",
    "    2.1 Application & Tech Stack",
    "    2.2 System Architecture",
    "    2.3 Communication Flows",
    "    2.4 ACK Response Types",
    "    2.5 Key Operations",
    "    2.6 Configuration Properties",
    "    2.7 Data Mapping Overview",
    "    2.8 Key Constraints",
    "    2.9 Observability",
    "    2.10 Known Limitations",
    "3. Testing Context",
    "    3.1 Scope",
    "    3.2 Test Data",
    "    3.3 Test Environment",
    "    3.4 Dependencies & Prerequisites",
    "    3.5 Test Scenarios",
    "    3.6 Validation Methods",
    "    3.7 Acceptance Criteria",
    "    3.8 Known Issues",
    "    3.9 Test Deliverables Checklist",
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(2)
    if not item.startswith("    "):
        for r in p.runs:
            r.bold = True

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# PART 1 — FEATURE CONTEXT
# ══════════════════════════════════════════════════════════════
doc.add_heading("1. Feature Context", level=1)
doc.add_heading("UCRI-P2P — End-to-End IPL ↔ Adapter (Receiver-Handler-Dispatcher) ↔ UCRM", level=2)

doc.add_heading("1.1 Overview", level=2)
doc.add_paragraph(
    "UCRI-P2P (Universal Control Room Interface - Peer-to-Peer) is an end-to-end integration feature "
    "enabling bi-directional communication between IPL (Integration Platform Layer) and UCRM (Universal "
    "Control Room Messaging) via the Adapter. The Adapter is composed of three internal services — "
    "Receiver, Handler, and Dispatcher — following Hexagonal Architecture principles. The system supports "
    "mission dispatch, event handling, acknowledgment processing (Accept/Reject/Timeout), and "
    "transport-agnostic messaging (in-memory or Kafka) for emergency services/control room operations."
)

# ── 1.2 User Stories — Adapter ──
doc.add_heading("1.2 User Stories — Adapter (Receiver + Handler + Dispatcher)", level=2)

adapter_stories = [
    ("US-A1", "Receive Business (Tenant Payload) from IPL",
     "Adapter (Receiver)", "receive business/tenant payload from IPL via /einsatztransfer/erzeugeEinsatz",
     "I can initiate the message forwarding process to UCRM"),
    ("US-A2", "Validate Incoming Request at Adapter",
     "Adapter (Receiver)", "validate incoming requests",
     "only properly formatted and authorized requests are processed by the Handler"),
    ("US-A3", "Authenticate Adapter to UCRM via P2P Token",
     "Adapter (Handler)", "authenticate to UCRM using P2P token",
     "secure communication is established with UCRM"),
    ("US-A4", "Forward Message from Adapter to UCRM via messaging/send",
     "Adapter (Dispatcher)", "forward messages to UCRM via messaging/send endpoint",
     "IPL events are delivered to UCRM"),
    ("US-A5", "Handle UCRM Acceptance/Rejection/Timeout Response at Adapter",
     "Adapter (Receiver + Handler)",
     "handle Accept, Reject, and Timeout responses from UCRM",
     "the outcome can be communicated back to IPL with correct ACK status:\n• Accept → log EMPFANG via Einsatztransfer/quittiereTranferEinsatz\n• Reject → log EINSATZ_ABGELEHNT\n• Timeout → log TECHNISCHER_FEHLER"),
    ("US-A6", "Propagate UCRM Outcome Back to IPL",
     "Adapter (Dispatcher)",
     "propagate UCRM outcomes back to IPL via /einsatztransfer/quittiereTranferEinsatz",
     "IPL receives confirmation with correct status (EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER)"),
    ("US-A7", "Support Reverse Flow UCRM → IPL via messaging/send",
     "Adapter (Receiver → Handler → Dispatcher)",
     "support reverse flow from UCRM to IPL",
     "missions originating from UCRM can reach IPL"),
    ("US-A8", "Logging, Monitoring, and Traceability for P2P Flows",
     "Operations Team",
     "have comprehensive logging, monitoring, and traceability across Receiver, Handler, and Dispatcher",
     "all P2P flows can be tracked and debugged"),
    ("US-A9", "Confirm Scope and Prerequisites for UCRM Test Client Usage",
     "Tester/Developer",
     "confirm scope and prerequisites for UCRM Test Client",
     "I can properly set up the test environment"),
    ("US-A10", "Installation Package and Deployment Guide for UCRM Test Client",
     "Tester/Developer",
     "have installation package and deployment guide",
     "I can deploy and configure the UCRM Test Client"),
]

for sid, title_text, role, action, benefit in adapter_stories:
    p = doc.add_paragraph()
    run = p.add_run(f"{sid}: {title_text}")
    run.bold = True
    p2 = doc.add_paragraph(
        f'As the {role}, I want to {action} so that {benefit}',
        style='List Bullet')
    p2.paragraph_format.space_after = Pt(4)

# ── 1.3 User Stories — IPL ──
doc.add_heading("1.3 User Stories — IPL", level=2)

ipl_stories = [
    ("US-I1", "IPL Sends Event to Adapter",
     "send events to the Adapter via /einsatztransfer/erzeugeEinsatz so that events can be forwarded to UCRM"),
    ("US-I2", "IPL Handles Validation Response from Adapter",
     "handle validation responses from Adapter so that I know if my request was properly formatted"),
    ("US-I3", "IPL Processes 'Accept' ACK (EMPFANG)",
     "process Accept acknowledgments from Adapter so that I know UCRM accepted my event.\nLog verification: Einsatztransfer/quittiereTranferEinsatz contains EMPFANG"),
    ("US-I4", "IPL Processes 'Reject' ACK (EINSATZ_ABGELEHNT)",
     "process Reject acknowledgments from Adapter so that I know UCRM rejected my event.\nLog verification: Einsatztransfer/quittiereTranferEinsatz contains EINSATZ_ABGELEHNT"),
    ("US-I5", "IPL Processes Timeout (TECHNISCHER_FEHLER)",
     "process Timeout notifications from Adapter so that I know UCRM did not respond within the allowed time.\nLog verification: Einsatztransfer/quittiereTranferEinsatz contains TECHNISCHER_FEHLER"),
    ("US-I6", "IPL Processes Mission from UCRM via Adapter (Reverse Flow)",
     "process missions received from UCRM via Adapter so that missions can be handled in the IPL system"),
    ("US-I7", "IPL Sends ACK (Accept/Reject) for Mission to Adapter",
     "send Accept/Reject acknowledgments for missions to Adapter so that UCRM receives confirmation of mission processing"),
]

for sid, title_text, desc in ipl_stories:
    p = doc.add_paragraph()
    run = p.add_run(f"{sid}: {title_text}")
    run.bold = True
    doc.add_paragraph(f"As IPL, I want to {desc}", style='List Bullet')

# ── 1.4 User Stories — Architecture & Transport ──
doc.add_heading("1.4 User Stories — Architecture & Transport", level=2)

arch_stories = [
    ("US-T1", "In-Memory Transport Operation",
     "As a developer, I want in-memory transport (Vert.x EventBus) for Receiver → Handler → Dispatcher communication so that the system operates without external infrastructure during development and testing."),
    ("US-T2", "Configuration-Driven Transport Selection",
     "As an operator, I want to select messaging transport via adapter.transport=in-memory|kafka so that deployment flexibility is maintained without code changes."),
    ("US-T3", "Module Enable/Disable via Configuration",
     "As an operator, I want to enable/disable Receiver, Handler, and Dispatcher individually via configuration so that flexible deployment scenarios are supported."),
    ("US-T4", "End-to-End Message Flow Validation",
     "As a developer, I want end-to-end message flow (Receiver → Handler → Dispatcher) validated so that the architecture operates correctly with in-memory transport."),
]
for sid, title_text, desc in arch_stories:
    p = doc.add_paragraph()
    run = p.add_run(f"{sid}: {title_text}")
    run.bold = True
    doc.add_paragraph(desc, style='List Bullet')

# ── 1.5 Acceptance Criteria ──
doc.add_heading("1.5 Acceptance Criteria", level=2)

doc.add_heading("Adapter Acceptance Criteria (Receiver + Handler + Dispatcher)", level=3)
add_checklist(doc, [
    "Receiver successfully receives tenant payload from IPL via /einsatztransfer/erzeugeEinsatz",
    "Receiver validates all incoming requests before forwarding to Handler",
    "Handler authenticates to UCRM using P2P token mechanism",
    "Dispatcher forwards messages to UCRM via messaging/send endpoint",
    "Adapter correctly handles Accept response from UCRM → logs EMPFANG",
    "Adapter correctly handles Reject response from UCRM → logs EINSATZ_ABGELEHNT",
    "Adapter correctly handles Timeout (no UCRM response) → logs TECHNISCHER_FEHLER",
    "Dispatcher propagates outcomes to IPL via /einsatztransfer/quittiereTranferEinsatz",
    "Adapter supports reverse flow (UCRM → Receiver → Handler → Dispatcher → IPL)",
    "All P2P flows are logged with full traceability across all three services",
    "Monitoring capabilities are operational",
    "UCRM Test Client installation and deployment documented",
])

doc.add_heading("IPL Acceptance Criteria", level=3)
add_checklist(doc, [
    "IPL successfully sends events to Adapter via /einsatztransfer/erzeugeEinsatz",
    "IPL handles validation responses from Adapter",
    "IPL correctly processes Accept ACK (log shows EMPFANG)",
    "IPL correctly processes Reject ACK (log shows EINSATZ_ABGELEHNT)",
    "IPL correctly processes Timeout (log shows TECHNISCHER_FEHLER)",
    "IPL processes missions from UCRM via Adapter (reverse flow)",
    "IPL sends Accept/Reject ACK for missions back to Adapter",
])

doc.add_heading("Transport & Architecture Acceptance Criteria", level=3)
add_checklist(doc, [
    "In-memory transport works for Receiver → Handler → Dispatcher flow",
    "Transport selected via adapter.transport=in-memory configuration",
    "Receiver, Handler, Dispatcher can be individually enabled/disabled",
    "Envelope metadata (correlationId, headers) preserved end-to-end",
    "Event ordering preserved based on partition key",
    "Disabled modules not instantiated, consume no resources",
])

# ── 1.6 API Endpoints ──
doc.add_heading("1.6 API Endpoints", level=2)
add_table(doc,
    ["Method", "Endpoint", "Direction", "Description"],
    [
        ["POST", "/einsatztransfer/erzeugeEinsatz", "IPL → Adapter (Receiver)", "Mission/event payload submission from IPL"],
        ["POST", "/einsatztransfer/quittiereTranferEinsatz", "Adapter (Dispatcher) → IPL", "ACK feedback: EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER"],
        ["POST", "messaging/send", "Adapter (Dispatcher) ↔ UCRM", "Forward/receive messages to/from UCRM"],
    ])

# ── 1.7 Validation Rules ──
doc.add_heading("1.7 Validation Rules", level=2)
add_table(doc,
    ["Field", "Rule"],
    [
        ["Tenant Payload", "Must be valid business payload format (TransferEinsatz structure)"],
        ["P2P Token", "Valid authentication token required, not expired"],
        ["Request Format", "Must pass Adapter (Receiver) validation rules"],
        ["ACK Type", "Must be one of: EMPFANG (Accept), EINSATZ_ABGELEHNT (Reject), TECHNISCHER_FEHLER (Timeout)"],
        ["sourceMandant", "Required — sender client identifier"],
        ["targetMandant", "Required — receiver client identifier"],
        ["einsatzId", "Required — operation identifier"],
        ["adapter.transport", 'Must be "in-memory" or "kafka"'],
        ["dispatch-center.ucri.enabled", "Boolean (true/false)"],
        ["dispatch-center.ucri.topic", "Required when enabled=true"],
    ])

# ── 1.8 ACK Status Values & Error Handling ──
doc.add_heading("1.8 ACK Status Values & Error Handling", level=2)

doc.add_heading("ACK Status Values", level=3)
add_table(doc,
    ["ACK Status", "Log Value (quittiereTranferEinsatz)", "Scenario"],
    [
        ["Accepted", "EMPFANG", "UCRM accepted the event/mission"],
        ["Rejected", "EINSATZ_ABGELEHNT", "UCRM rejected the event/mission"],
        ["Timeout", "TECHNISCHER_FEHLER", "UCRM did not respond within allowed time"],
    ])

doc.add_heading("Error Handling", level=3)
add_table(doc,
    ["Scenario", "Behavior"],
    [
        ["UCRM Accept", "Adapter logs EMPFANG, propagates Accept to IPL"],
        ["UCRM Reject", "Adapter logs EINSATZ_ABGELEHNT, propagates Reject to IPL"],
        ["UCRM Timeout (no response)", "Adapter logs TECHNISCHER_FEHLER, propagates timeout error to IPL"],
        ["Invalid request at Receiver", "Rejected with clear reason logged, no forwarding to Handler"],
        ["P2P authentication failure", "Error propagated to IPL, logged with details"],
        ["No transport configured", "Startup fails with descriptive error"],
        ["Invalid transport value", "Startup fails listing valid options"],
        ["Publish failure", "Retry with configurable attempts, then DLQ"],
    ])

# ── 1.9 Flow Diagrams ──
doc.add_heading("1.9 Flow Diagrams", level=2)

doc.add_heading("IPL to UCRI Flow", level=3)
doc.add_paragraph(
    "The diagram below illustrates the forward flow: IPL → Adapter (Receiver → Handler → Dispatcher) → UCRM "
    "with Accept/Reject/Timeout outcomes."
)
if os.path.exists(ipl_to_ucri_img):
    doc.add_picture(ipl_to_ucri_img, width=Inches(6.0))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph("Figure 1: IPL to UCRI Flow Diagram")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
else:
    doc.add_paragraph("[IMAGE NOT FOUND: IPL to UCRI.png]")

doc.add_paragraph()

doc.add_heading("UCRI to IPL Flow", level=3)
doc.add_paragraph(
    "The diagram below illustrates the reverse flow: UCRM → Adapter (Receiver → Handler → Dispatcher) → IPL "
    "with mission dispatch."
)
if os.path.exists(ucri_to_ipl_img):
    doc.add_picture(ucri_to_ipl_img, width=Inches(6.0))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph("Figure 2: UCRI to IPL Flow Diagram")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
else:
    doc.add_paragraph("[IMAGE NOT FOUND: UCRI to IPL.png]")

# ── 1.10 Data Mapping ──
doc.add_heading("1.10 Data Mapping", level=2)

doc.add_heading("IPL → UCRM Field Mapping (TransferEinsatz)", level=3)
add_table(doc,
    ["IPL Field", "UCRM Field", "Mapping Logic"],
    [
        ["sourceMandant", "header.sender_client_id", "1:1 Mapping"],
        ["targetMandant", "header.receiver_client_id", "1:1 Mapping"],
        ["transferEinsatz.einsatzId", "operation.id", "1:1 Mapping"],
        ["transferEinsatz.einsatznummerKurz", "operation.name", "1:1 Mapping"],
        ["transferEinsatz.kategorie", "operation.occassion.type_1", "1:1 Mapping"],
        ["transferEinsatz.einsatzStichwort", "operation.occassion.keyword_1", "1:1 Mapping"],
        ["transferEinsatz.alarmierungsstichwortText", "operation.occassion.keyword_1_text", "1:1 Mapping"],
    ])

doc.add_heading("ACK Response Mapping (UCRM → IPL)", level=3)
add_table(doc,
    ["UCRM Response", "IPL ACK (quittiereTranferEinsatz)", "Log Value"],
    [
        ["Accept", "Accepted", "EMPFANG"],
        ["Reject", "Rejected", "EINSATZ_ABGELEHNT"],
        ["No Response", "Timeout", "TECHNISCHER_FEHLER"],
    ])

doc.add_heading("Reference Documents", level=3)
doc.add_paragraph("• IPL-Mapping (UCRI) — Mapping Specification", style='List Bullet')
doc.add_paragraph("• complete_spec en-US 1.pdf — Complete Specification", style='List Bullet')
doc.add_paragraph("• UCRI-Universal-Control-Room-Interface-Outline-V2.0 — UCRI Outline", style='List Bullet')

# ── 1.11 Cross-Cutting Concerns ──
doc.add_heading("1.11 Cross-Cutting Concerns (Decorators)", level=2)
add_table(doc,
    ["Concern", "Description"],
    [
        ["Logging", "Logs publish/receive operations with context across Receiver, Handler, Dispatcher"],
        ["Retry", "Retries failed publish with configurable backoff (default: 3 attempts, 1000ms delay)"],
        ["Metrics", "Exposes publish/receive/failure counts and latency"],
    ])

# ── 1.12 Dependencies ──
doc.add_heading("1.12 Dependencies", level=2)
deps = [
    "IPL system must be operational (or mock IPL running)",
    "UCRM must be accessible via P2P connection",
    "P2P token authentication mechanism must be configured",
    "Network connectivity between IPL, Adapter (all 3 services), and UCRM required",
    "For in-memory mode: no external infrastructure required",
    "For Kafka mode: Kafka broker must be running",
    "Logging infrastructure operational for ACK verification (EMPFANG / EINSATZ_ABGELEHNT / TECHNISCHER_FEHLER)",
]
for d in deps:
    doc.add_paragraph(d, style='List Bullet')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# PART 2 — PROJECT CONTEXT
# ══════════════════════════════════════════════════════════════
doc.add_heading("2. Project Context", level=1)
doc.add_heading("UCRI 2.0 P2P Integration (IPL-Adapter-UCRM)", level=2)

# ── 2.1 Application & Tech Stack ──
doc.add_heading("2.1 Application & Tech Stack", level=2)
add_table(doc,
    ["Property", "Value"],
    [
        ["Name", "UCRI 2.0 P2P Adapter Integration Service"],
        ["Type", "API / Integration Service"],
        ["Domain", "Emergency Services / Universal Control Room Interface / Incident Dispatch"],
        ["Frontend", "Not applicable (backend service only)"],
        ["Backend", "Java 17+, Quarkus Framework"],
        ["Database", "Not specified (prototype excludes persistence)"],
        ["API Type (IPL)", "REST"],
        ["API Type (UCRM)", "P2P Messaging Protocol via messaging/send"],
        ["Messaging", "Vert.x EventBus (in-memory) / Kafka (distributed)"],
        ["Architecture", "Hexagonal Architecture (Ports and Adapters)"],
        ["Authentication", "P2P Token-based authentication for UCRM"],
        ["Test Client", "UCRM Test Client"],
    ])

# ── 2.2 System Architecture ──
doc.add_heading("2.2 System Architecture", level=2)

doc.add_heading("System Components", level=3)
add_table(doc,
    ["Component", "Description"],
    [
        ["IPL (Integration Platform Layer)", "Source/target system for event/mission dispatch"],
        ["Adapter (Receiver + Handler + Dispatcher)", "Integration service mediating between IPL and UCRM, composed of three sub-services"],
        ["UCRM (Universal Control Room Messaging)", "Universal messaging system for control room operations"],
        ["UCRM Test Client", "Test utility for UCRM integration validation"],
    ])

doc.add_heading("Adapter Internal Architecture (3-Service Model)", level=3)
add_table(doc,
    ["Service", "Role", "Description"],
    [
        ["Receiver", "Event Ingress", "Consumes events via messaging ports, validates inbound events, feeds into domain processing"],
        ["Handler", "Business Logic", "Processes events, transforms/translates between IPL and UCRM formats, orchestration logic"],
        ["Dispatcher", "Event Egress", "Determines outbound routing, publishes events to target dispatch centers via messaging ports"],
    ])

doc.add_heading("Deployment Modes", level=3)
add_table(doc,
    ["Mode", "Description"],
    [
        ["Domain Modular (Standalone)", "Single deployable service; Receiver, Handler, Dispatcher communicate via in-memory event bus (Vert.x)"],
        ["Distributed (Kafka-Based)", "Three independent services communicating via Kafka topics"],
    ])

doc.add_heading("Port Abstractions (Hexagonal Architecture)", level=3)
add_table(doc,
    ["Port", "Purpose"],
    [
        ["EventPublisherPort", "Publishing events outbound (used by Dispatcher)"],
        ["EventSubscriberPort", "Subscribing to and unsubscribing from event channels"],
        ["EventReceiverPort", "Receiving and processing inbound events (used by Receiver)"],
    ])

doc.add_heading("Dispatch Centers", level=3)
add_table(doc,
    ["Center", "Topic", "Description"],
    [
        ["IPL", "events-ipl", "Source system for incident dispatch"],
        ["UCRI", "events-ucri", "Emergency services dispatch center (UCRM)"],
        ["WDX", "events-wdx", "Operational hub for incident distribution"],
        ["POLICE", "events-police", "Law enforcement dispatch center"],
    ])

# ── 2.3 Communication Flows ──
doc.add_heading("2.3 Communication Flows", level=2)

doc.add_heading("Forward Flow: IPL → Adapter → UCRM", level=3)
fwd_steps = [
    "IPL sends business/tenant payload via /einsatztransfer/erzeugeEinsatz (POST)",
    "Receiver accepts and validates incoming request",
    "Handler transforms IPL format to UCRM-compliant message, authenticates via P2P token",
    "Dispatcher forwards message to UCRM via messaging/send endpoint",
    "UCRM processes and returns Accept/Reject/Timeout response",
    "Receiver receives UCRM response",
    "Handler translates response to IPL ACK format",
    "Dispatcher propagates outcome back to IPL via /einsatztransfer/quittiereTranferEinsatz (POST)",
]
for i, s in enumerate(fwd_steps, 1):
    doc.add_paragraph(f"{i}. {s}")

# Insert IPL to UCRI diagram here as well (in communication flows context)
if os.path.exists(ipl_to_ucri_img):
    doc.add_picture(ipl_to_ucri_img, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph("Figure 3: Forward Flow — IPL to UCRI")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_heading("Reverse Flow: UCRM → Adapter → IPL", level=3)
rev_steps = [
    "UCRM sends mission to Adapter via messaging/send",
    "Receiver accepts mission payload",
    "Handler translates UCRM mission to IPL format",
    "Dispatcher forwards mission to IPL",
    "IPL processes mission and sends ACK (Accept/Reject) back",
    "Receiver receives IPL ACK",
    "Handler translates ACK to UCRM format",
    "Dispatcher propagates ACK to UCRM",
]
for i, s in enumerate(rev_steps, 1):
    doc.add_paragraph(f"{i}. {s}")

if os.path.exists(ucri_to_ipl_img):
    doc.add_picture(ucri_to_ipl_img, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph("Figure 4: Reverse Flow — UCRI to IPL")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    cap.runs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# ── 2.4 ACK Response Types ──
doc.add_heading("2.4 ACK Response Types and Log Verification", level=2)
add_table(doc,
    ["ACK Status", "Log Value", "Description"],
    [
        ["Accepted", "EMPFANG", "UCRM accepted — Einsatztransfer/quittiereTranferEinsatz shows EMPFANG"],
        ["Rejected", "EINSATZ_ABGELEHNT", "UCRM rejected — log shows EINSATZ_ABGELEHNT"],
        ["Timeout", "TECHNISCHER_FEHLER", "UCRM did not respond — log shows TECHNISCHER_FEHLER"],
    ])

# ── 2.5 Key Operations ──
doc.add_heading("2.5 Key Operations", level=2)

doc.add_heading("Adapter Operations", level=3)
add_table(doc,
    ["Operation", "Service", "Direction", "Description"],
    [
        ["Receive Tenant Payload", "Receiver", "IPL → Adapter", "Accept and validate business payload"],
        ["Validate Request", "Receiver", "Adapter", "Validate incoming request format and data"],
        ["Transform Message", "Handler", "Adapter", "Translate between IPL and UCRM formats"],
        ["P2P Authentication", "Handler", "Adapter → UCRM", "Authenticate to UCRM via P2P token"],
        ["Forward Message", "Dispatcher", "Adapter → UCRM", "Forward message via messaging/send"],
        ["Handle Response", "Receiver", "UCRM → Adapter", "Handle UCRM Accept/Reject/Timeout response"],
        ["Propagate Outcome", "Dispatcher", "Adapter → IPL", "Return outcome to IPL via quittiereTranferEinsatz"],
        ["Reverse Flow", "All", "UCRM → Adapter → IPL", "Support mission flow from UCRM to IPL"],
    ])

doc.add_heading("IPL Operations", level=3)
add_table(doc,
    ["Operation", "Direction", "Description"],
    [
        ["Send Event", "IPL → Adapter", "IPL sends event via /einsatztransfer/erzeugeEinsatz"],
        ["Handle Validation", "Adapter → IPL", "IPL handles validation response from Adapter"],
        ["Process Accept ACK", "Adapter → IPL", "IPL processes EMPFANG acknowledgment"],
        ["Process Reject ACK", "Adapter → IPL", "IPL processes EINSATZ_ABGELEHNT acknowledgment"],
        ["Process Timeout", "Adapter → IPL", "IPL processes TECHNISCHER_FEHLER (timeout)"],
        ["Process Mission", "Adapter → IPL", "IPL processes mission from UCRM (reverse flow)"],
        ["Send ACK", "IPL → Adapter", "IPL sends Accept/Reject for mission"],
    ])

# ── 2.6 Configuration Properties ──
doc.add_heading("2.6 Configuration Properties", level=2)

doc.add_heading("Transport Configuration", level=3)
add_table(doc,
    ["Property", "Description", "Default"],
    [
        ["adapter.transport", "Transport mode selection", "in-memory / kafka"],
        ["adapter.receiver.enabled", "Enable/disable Receiver service", "true"],
        ["adapter.handler.enabled", "Enable/disable Handler service", "true"],
        ["adapter.dispatcher.enabled", "Enable/disable Dispatcher service", "true"],
    ])

doc.add_heading("Dispatch Center Configuration", level=3)
add_table(doc,
    ["Property", "Description", "Default"],
    [
        ["dispatch-center.ucri.enabled", "Enable/disable UCRI dispatch center", "true"],
        ["dispatch-center.ucri.topic", "UCRI event topic", "events-ucri"],
        ["dispatch-center.ucri.url", "UCRM connection URL", "[NEEDS CLARIFICATION]"],
        ["dispatch-center.ucri.timeout-ms", "Connection timeout", "5000"],
        ["dispatch-center.ucri.retry-attempts", "Retry attempts on failure", "3"],
        ["dispatch-center.ucri.retry-delay-ms", "Delay between retries", "1000"],
        ["dispatch-center.ucri.dlq-topic", "Dead Letter Queue topic", "events-ucri-dlq"],
    ])

# ── 2.7 Data Mapping Overview ──
doc.add_heading("2.7 Data Mapping Overview", level=2)

doc.add_heading("IPL → UCRM Field Mapping (via Adapter Handler)", level=3)
add_table(doc,
    ["IPL Field", "UCRM Field", "Mapping Logic"],
    [
        ["sourceMandant", "header.sender_client_id", "1:1 Mapping"],
        ["targetMandant", "header.receiver_client_id", "1:1 Mapping"],
        ["transferEinsatz.einsatzId", "operation.id", "1:1 Mapping"],
        ["transferEinsatz.einsatznummerKurz", "operation.name", "1:1 Mapping"],
        ["transferEinsatz.kategorie", "operation.occassion.type_1", "1:1 Mapping"],
        ["transferEinsatz.einsatzStichwort", "operation.occassion.keyword_1", "1:1 Mapping"],
        ["transferEinsatz.alarmierungsstichwortText", "operation.occassion.keyword_1_text", "1:1 Mapping"],
    ])

doc.add_heading("ACK Mapping (UCRM → IPL via Adapter Handler)", level=3)
add_table(doc,
    ["UCRM Response", "IPL Log Value", "Meaning"],
    [
        ["Accept", "EMPFANG", "Mission/event accepted"],
        ["Reject", "EINSATZ_ABGELEHNT", "Mission/event rejected"],
        ["No Response (Timeout)", "TECHNISCHER_FEHLER", "Technical error / timeout"],
    ])

# ── 2.8 Key Constraints ──
doc.add_heading("2.8 Key Constraints", level=2)

doc.add_heading("Architectural Constraints", level=3)
for c in [
    "Adapter follows Hexagonal Architecture (Ports and Adapters)",
    "Messaging must be transport-agnostic (Kafka or in-memory switch via configuration)",
    "Domain logic (Handler) must remain independent of infrastructure",
    "Cross-cutting concerns (logging, retry, metrics) implemented via decorators",
    "Configuration-driven behavior only (no recompilation for transport switching)",
]:
    doc.add_paragraph(c, style='List Bullet')

doc.add_heading("Technical Constraints", level=3)
for c in [
    "P2P token-based authentication required for UCRM communication",
    "Bi-directional communication flow support required",
    "Every event must be acknowledged within 10 seconds (timeout → TECHNISCHER_FEHLER)",
    "Event ordering preserved based on partition key",
    "Logging, monitoring, and traceability required for all P2P flows",
]:
    doc.add_paragraph(c, style='List Bullet')

doc.add_heading("Prototype Constraints", level=3)
for c in [
    "No database or cache layer (no persistence)",
    "Mock IPL service used instead of real IPL system",
    "No retry mechanisms, fallback routing, or automatic error recovery (prototype)",
    "Patient data within mission dispatch messages is not processed",
]:
    doc.add_paragraph(c, style='List Bullet')

# ── 2.9 Observability ──
doc.add_heading("2.9 Observability", level=2)
doc.add_paragraph("Logging & Monitoring:")
for item in [
    "Comprehensive logging for all P2P flows (Receiver, Handler, Dispatcher)",
    "ACK outcomes logged via Einsatztransfer/quittiereTranferEinsatz with status values: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER",
    "Traceability support via correlationId for request/response tracking",
    "Cross-cutting metrics via decorators: publish/receive/failure counts and latency",
]:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("Log Verification Points", level=3)
add_table(doc,
    ["Log Entry", "Contains", "Scenario"],
    [
        ["Einsatztransfer/quittiereTranferEinsatz", "EMPFANG", "Accepted case"],
        ["Einsatztransfer/quittiereTranferEinsatz", "EINSATZ_ABGELEHNT", "Rejected case"],
        ["Einsatztransfer/quittiereTranferEinsatz", "TECHNISCHER_FEHLER", "Timeout case"],
    ])

# ── 2.10 Known Limitations ──
doc.add_heading("2.10 Known Limitations", level=2)
for lim in [
    "Specific UCRM API endpoint details not fully specified in available documentation",
    "Environment URLs not specified in requirements",
    "Patient data processing excluded from prototype",
    "No automatic error recovery in prototype",
]:
    doc.add_paragraph(lim, style='List Bullet')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# PART 3 — TESTING CONTEXT
# ══════════════════════════════════════════════════════════════
doc.add_heading("3. Testing Context", level=1)
doc.add_heading("UCRI 2.0 P2P Integration — Test Strategy", level=2)

# ── 3.1 Scope ──
doc.add_heading("3.1 Scope", level=2)

doc.add_heading("In Scope", level=3)
in_scope = [
    "Forward Flow Testing: IPL → Adapter (Receiver → Handler → Dispatcher) → UCRM",
    "Reverse Flow Testing: UCRM → Adapter (Receiver → Handler → Dispatcher) → IPL",
    "Adapter Validation (Receiver): Incoming request validation",
    "P2P Authentication (Handler): Adapter to UCRM authentication via P2P token",
    "Message Forwarding (Dispatcher): messaging/send and /einsatztransfer/quittiereTranferEinsatz",
    "Accept Handling: UCRM Accept → ACK with EMPFANG",
    "Reject Handling: UCRM Reject → ACK with EINSATZ_ABGELEHNT",
    "Timeout Handling: UCRM no response → ACK with TECHNISCHER_FEHLER",
    "Reverse Flow ACK: IPL Accept/Reject acknowledgment for UCRM missions",
    "In-Memory Transport: Vert.x EventBus for Receiver → Handler → Dispatcher",
    "Module Configuration: Enable/disable Receiver, Handler, Dispatcher individually",
    "Bi-directional Communication: Full round-trip message flow validation",
    "Logging & Traceability: P2P flow logging, monitoring, ACK status verification",
    "Field Mapping Validation: TransferEinsatz to UCRM operation mapping",
    "UCRM Test Client: Installation and usage validation",
    "Cross-Cutting Concerns: Retry decorator, DLQ, metrics validation",
    "End-to-End Flow: Receiver → Handler → Dispatcher with in-memory transport",
]
for s in in_scope:
    doc.add_paragraph(s, style='List Bullet')

doc.add_heading("Out of Scope", level=3)
out_scope = [
    "UI Testing (Not applicable — backend service only)",
    "Database Testing (prototype excludes persistence)",
    "Patient Data Processing (excluded from prototype)",
    "Kafka Transport Testing (Phase 1 focuses on in-memory only)",
    "Performance Benchmarking [NEEDS CLARIFICATION]",
    "Load Testing (not specified in requirements)",
    "Security Penetration Testing (not specified)",
]
for s in out_scope:
    doc.add_paragraph(s, style='List Bullet')

# ── 3.2 Test Data ──
doc.add_heading("3.2 Test Data", level=2)

doc.add_heading("Mission/Event Data", level=3)
add_table(doc,
    ["Data Type", "Value", "Purpose"],
    [
        ["Valid TransferEinsatzRequest", "JSON payload with mission data", "Forward flow happy path"],
        ["Invalid TransferEinsatzRequest", "Malformed/incomplete payload", "Receiver validation negative test"],
        ["Empty Payload", "Empty body", "Boundary test"],
        ["Valid sourceMandant", "e.g., IPL_CENTER_001", "Header mapping validation"],
        ["Valid targetMandant", "e.g., UCRI_CENTER_001", "Header mapping validation"],
        ["Valid einsatzId", "Operation identifier", "Operation ID mapping"],
        ["Valid einsatznummerKurz", "Short incident number", "Operation name mapping"],
        ["Valid kategorie", "Incident category code", "Occasion type_1 mapping"],
        ["Valid einsatzStichwort", "Alarm keyword (coded)", "Occasion keyword_1 mapping"],
    ])

doc.add_heading("Authentication Data", level=3)
add_table(doc,
    ["Data Type", "Value", "Purpose"],
    [
        ["Valid P2P Token", "Authorized authentication token", "P2P authentication happy path"],
        ["Invalid P2P Token", "Expired/revoked token", "Authentication failure test"],
        ["Missing P2P Token", "No token provided", "Authentication boundary test"],
    ])

doc.add_heading("ACK Response Data", level=3)
add_table(doc,
    ["Data Type", "Value", "Log Verification", "Purpose"],
    [
        ["UCRM Accept Response", "Accept ACK", "EMPFANG", "Acceptance flow"],
        ["UCRM Reject Response", "Reject ACK", "EINSATZ_ABGELEHNT", "Rejection flow"],
        ["UCRM Timeout", "Timeout", "TECHNISCHER_FEHLER", "Timeout flow"],
        ["IPL Accept ACK", "Accept for reverse flow", "N/A", "Reverse flow ACK test"],
        ["IPL Reject ACK", "Reject for reverse flow", "N/A", "Reverse flow rejection test"],
    ])

doc.add_heading("Transport & Module Configuration Data", level=3)
add_table(doc,
    ["Data Type", "Value", "Purpose"],
    [
        ["Transport config", "adapter.transport=in-memory", "Validate in-memory mode"],
        ["Invalid transport", "adapter.transport=invalid", "Validate error handling"],
        ["Missing transport", "(property absent)", "Validate startup failure"],
        ["Receiver enabled", "adapter.receiver.enabled=true/false", "Module toggle test"],
        ["Handler enabled", "adapter.handler.enabled=true/false", "Module toggle test"],
        ["Dispatcher enabled", "adapter.dispatcher.enabled=true/false", "Module toggle test"],
    ])

# ── 3.3 Test Environment ──
doc.add_heading("3.3 Test Environment", level=2)
add_table(doc,
    ["Property", "Value"],
    [
        ["Tool", "Postman (primary), JUnit (unit tests)"],
        ["Test Client", "UCRM Test Client (per deployment guide)"],
        ["Protocol", "P2P Messaging / REST"],
        ["Transport", "In-Memory (Vert.x EventBus) for Phase 1"],
        ["Authentication", "P2P Token-based"],
        ["Browser", "Not applicable (API testing only)"],
        ["Device", "Desktop"],
        ["OS", "Linux (recommended), Windows compatible"],
        ["Java Version", "Java 17+ (OpenJDK recommended)"],
    ])

# ── 3.4 Dependencies & Prerequisites ──
doc.add_heading("3.4 Dependencies & Prerequisites", level=2)

doc.add_heading("Required Services", level=3)
for s in [
    "IPL system must be running (or mock IPL)",
    "UCRM must be accessible via P2P connection",
    "Adapter service deployed: all three services (Receiver, Handler, Dispatcher) must be started",
    "UCRM Test Client must be installed (per User Story A10)",
]:
    doc.add_paragraph(s, style='List Bullet')

doc.add_heading("Prerequisites", level=3)
for s in [
    "UCRM Test Client scope and prerequisites confirmed (per User Story A9)",
    "P2P authentication tokens must be provisioned",
    "Network connectivity between IPL, Adapter, and UCRM established",
    "Logging infrastructure operational for ACK status verification",
    "adapter.transport=in-memory configured for Phase 1",
]:
    doc.add_paragraph(s, style='List Bullet')

doc.add_heading("Pre-Test Setup", level=3)
for s in [
    "Follow UCRM Test Client deployment guide",
    "Verify all service connectivity (IPL ↔ Adapter ↔ UCRM)",
    "Confirm P2P token validity",
    "Validate logging configuration — ensure logs capture Einsatztransfer/quittiereTranferEinsatz entries",
    "Verify Receiver, Handler, Dispatcher modules enabled in configuration",
]:
    doc.add_paragraph(s, style='List Bullet')

# ── 3.5 Test Scenarios ──
doc.add_heading("3.5 Test Scenarios", level=2)

scenarios = [
    ("Forward Flow Tests (IPL → Adapter → UCRM)", [
        ("Scenario 1: Happy Path — Event Sent and Accepted (EMPFANG)", [
            "IPL sends valid TransferEinsatzRequest to Adapter via /einsatztransfer/erzeugeEinsatz",
            "Receiver validates request (passes)",
            "Handler authenticates to UCRM via P2P token",
            "Handler transforms IPL payload to UCRM format",
            "Dispatcher forwards message to UCRM via messaging/send",
            "UCRM accepts and returns Accept response",
            "Receiver receives Accept response from UCRM",
            "Handler translates to IPL ACK format",
            "Dispatcher calls /einsatztransfer/quittiereTranferEinsatz with Accept",
            "Log verification: Einsatztransfer/quittiereTranferEinsatz contains EMPFANG",
        ]),
        ("Scenario 2: Event Sent and Rejected (EINSATZ_ABGELEHNT)", [
            "IPL sends valid TransferEinsatzRequest",
            "Receiver validates (passes), Handler authenticates and transforms",
            "Dispatcher forwards to UCRM via messaging/send",
            "UCRM rejects and returns Reject response",
            "Handler translates to IPL ACK format",
            "Dispatcher calls /einsatztransfer/quittiereTranferEinsatz with Reject",
            "Log verification: contains EINSATZ_ABGELEHNT",
        ]),
        ("Scenario 3: Timeout — UCRM Does Not Respond (TECHNISCHER_FEHLER)", [
            "IPL sends valid TransferEinsatzRequest",
            "Receiver validates, Handler authenticates and transforms",
            "Dispatcher forwards to UCRM via messaging/send",
            "UCRM does not respond within allowed time",
            "Handler detects timeout condition",
            "Dispatcher calls /einsatztransfer/quittiereTranferEinsatz with Timeout",
            "Log verification: contains TECHNISCHER_FEHLER",
        ]),
        ("Scenario 4: Validation Failure at Receiver", [
            "IPL sends invalid/malformed payload",
            "Receiver validation fails",
            "Receiver returns validation error to IPL",
            "Verify: No message forwarded to Handler or Dispatcher",
            "Verify: No quittiereTranferEinsatz log entry generated",
        ]),
        ("Scenario 5: P2P Authentication Failure at Handler", [
            "IPL sends valid event to Adapter",
            "Receiver validates (passes), forwards to Handler",
            "Handler attempts P2P authentication with invalid/expired token",
            "Authentication fails; error propagated back to IPL",
            "Verify: No message forwarded to UCRM via Dispatcher",
        ]),
    ]),
    ("Reverse Flow Tests (UCRM → Adapter → IPL)", [
        ("Scenario 6: Mission Received and Accepted by IPL", [
            "UCRM sends mission to Adapter via messaging/send",
            "Receiver accepts mission, Handler translates to IPL format",
            "Dispatcher forwards mission to IPL",
            "IPL processes successfully, sends Accept ACK",
            "Handler translates, Dispatcher propagates Accept ACK to UCRM",
        ]),
        ("Scenario 7: Mission Received and Rejected by IPL", [
            "UCRM sends mission to Adapter",
            "Adapter forwards to IPL; IPL rejects mission",
            "IPL sends Reject ACK; Adapter propagates Reject ACK to UCRM",
        ]),
        ("Scenario 8: Reverse Flow — IPL Does Not Respond (Timeout)", [
            "UCRM sends mission to Adapter",
            "Adapter forwards to IPL; IPL does not respond within allowed time",
            "Adapter handles timeout",
            "Verify: Timeout handling for reverse flow [NEEDS CLARIFICATION]",
        ]),
    ]),
    ("In-Memory Transport Tests", [
        ("Scenario 9: In-Memory Transport Initialization", [
            "Configure adapter.transport=in-memory",
            "Start Adapter service (Receiver, Handler, Dispatcher)",
            "Verify startup logs indicate in-memory transport active",
            "Verify no external Kafka broker connection attempted",
        ]),
        ("Scenario 10: End-to-End Flow via In-Memory Transport", [
            "Configure in-memory transport with all modules enabled",
            "Send event to Receiver",
            "Verify Receiver → Handler → Dispatcher flow via in-memory bus",
            "Verify Dispatcher routes to correct dispatch center topic",
            "Confirm envelope metadata preserved end-to-end",
        ]),
        ("Scenario 11: Event Ordering with In-Memory Transport", [
            "Publish multiple events with same partition key",
            "Verify events delivered in published order",
            "Confirm ordering preserved based on partition key",
        ]),
    ]),
    ("Module Configuration Tests", [
        ("Scenario 12: Receiver Module Disable/Enable", [
            "Set adapter.receiver.enabled=false",
            "Verify no event subscriptions created",
            "Enable → verify Receiver functional",
        ]),
        ("Scenario 13: Handler Module Disable/Enable", [
            "Set adapter.handler.enabled=false",
            "Send event → Receiver accepts but Handler does not process",
            "Enable → verify full flow works",
        ]),
        ("Scenario 14: Dispatcher Module Disable/Enable", [
            "Set adapter.dispatcher.enabled=false",
            "Process event through Handler → verify no dispatch",
            "Enable → verify routing works",
        ]),
    ]),
    ("ACK Log Verification Tests", [
        ("Scenario 15: Verify EMPFANG Log Entry", [
            "Complete forward flow with UCRM Accept",
            "Check logs for Einsatztransfer/quittiereTranferEinsatz → EMPFANG",
            "Verify correlationId matches original request",
        ]),
        ("Scenario 16: Verify EINSATZ_ABGELEHNT Log Entry", [
            "Complete forward flow with UCRM Reject",
            "Check logs → EINSATZ_ABGELEHNT",
            "Verify correlationId matches",
        ]),
        ("Scenario 17: Verify TECHNISCHER_FEHLER Log Entry", [
            "Complete forward flow where UCRM times out",
            "Check logs → TECHNISCHER_FEHLER",
            "Verify correlationId matches",
        ]),
    ]),
    ("Cross-Cutting Tests", [
        ("Scenario 18: Logging and Traceability Across All 3 Services", [
            "Execute forward flow test",
            "Verify Receiver, Handler, Dispatcher logs with correlationId",
            "Confirm end-to-end traceability",
        ]),
        ("Scenario 19: Field Mapping Validation", [
            "Send TransferEinsatzRequest with all mappable fields",
            "Verify all 7 field mappings (sourceMandant → header.sender_client_id, etc.)",
            "Confirm no data loss in translation",
        ]),
        ("Scenario 20: UCRM Test Client Validation", [
            "Install UCRM Test Client per deployment guide",
            "Verify prerequisites, execute connectivity test",
            "Validate Test Client functionality",
        ]),
        ("Scenario 21: Retry Decorator", [
            "Configure retry (3 attempts, 1000ms delay)",
            "Simulate transient Dispatcher publish failure",
            "Verify retry occurs per configuration; verify metrics",
        ]),
        ("Scenario 22: Dead Letter Queue", [
            "Configure DLQ for UCRI dispatch center",
            "Send event that fails permanently after all retries",
            "Verify event sent to DLQ (events-ucri-dlq) with original payload and error context",
        ]),
        ("Scenario 23: Invalid Transport Configuration", [
            "Set adapter.transport=invalid_value",
            "Start service → verify startup fails with descriptive error",
        ]),
    ]),
]

for section_title, section_scenarios in scenarios:
    doc.add_heading(section_title, level=3)
    for scenario_title, steps in section_scenarios:
        p = doc.add_paragraph()
        run = p.add_run(scenario_title)
        run.bold = True
        for i, step in enumerate(steps, 1):
            doc.add_paragraph(f"{i}. {step}")
        doc.add_paragraph()

# ── 3.6 Validation Methods ──
doc.add_heading("3.6 Validation Methods", level=2)

doc.add_heading("Log-Based Verification (Primary)", level=3)
add_table(doc,
    ["Log Entry", "Expected Value", "Scenario"],
    [
        ["Einsatztransfer/quittiereTranferEinsatz", "EMPFANG", "Accepted case"],
        ["Einsatztransfer/quittiereTranferEinsatz", "EINSATZ_ABGELEHNT", "Rejected case"],
        ["Einsatztransfer/quittiereTranferEinsatz", "TECHNISCHER_FEHLER", "Timeout case"],
    ])

doc.add_heading("Service-Level Log Verification", level=3)
for item in [
    "Receiver logs: Event receipt, validation pass/fail",
    "Handler logs: Transformation, authentication, timeout detection",
    "Dispatcher logs: Message forwarding, ACK propagation, retry attempts",
    "Transport logs: Startup confirmation (in-memory/kafka active)",
]:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("Response Verification", level=3)
for item in [
    "Correct HTTP status codes from /einsatztransfer/erzeugeEinsatz",
    "Proper ACK format from /einsatztransfer/quittiereTranferEinsatz",
    "Error messages match specification",
]:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("Metric-Based Verification", level=3)
for item in [
    "Publish count per dispatch center (UCRI)",
    "Receive count per channel",
    "Failure/timeout count",
    "Latency metrics",
]:
    doc.add_paragraph(item, style='List Bullet')

# ── 3.7 Acceptance Criteria ──
doc.add_heading("3.7 Acceptance Criteria", level=2)

for section, items in [
    ("Forward Flow", [
        "IPL sends event to Adapter via /einsatztransfer/erzeugeEinsatz",
        "Receiver validates incoming requests correctly",
        "P2P authentication at Handler succeeds with valid token",
        "Dispatcher forwards message to UCRM via messaging/send",
        "UCRM Accept → log shows EMPFANG",
        "UCRM Reject → log shows EINSATZ_ABGELEHNT",
        "UCRM Timeout → log shows TECHNISCHER_FEHLER",
        "Outcome propagated to IPL via /einsatztransfer/quittiereTranferEinsatz",
    ]),
    ("Reverse Flow", [
        "UCRM mission received at Adapter (Receiver)",
        "Mission translated (Handler) and forwarded (Dispatcher) to IPL",
        "IPL Accept ACK sent and propagated to UCRM",
        "IPL Reject ACK sent and propagated to UCRM",
    ]),
    ("In-Memory Transport", [
        "Receiver → Handler → Dispatcher flow works with in-memory transport",
        "Envelope metadata preserved end-to-end",
        "Event ordering preserved based on partition key",
        "No external infrastructure required",
    ]),
    ("Module Configuration", [
        "Receiver can be enabled/disabled",
        "Handler can be enabled/disabled",
        "Dispatcher can be enabled/disabled",
        "Disabled modules consume no resources",
    ]),
    ("Cross-Cutting", [
        "Logging across all 3 services with correlationId traceability",
        "Retry decorator works",
        "DLQ handles permanent failures",
        "Monitoring metrics operational",
    ]),
]:
    doc.add_heading(section, level=3)
    add_checklist(doc, items)

# ── 3.8 Known Issues ──
doc.add_heading("3.8 Known Issues", level=2)

doc.add_heading("Current Prototype Limitations", level=3)
for item in [
    "Mock IPL service only; real IPL system integration deferred",
    "No data persistence or caching implemented",
    "Testing performed in controlled environments only",
    "Patient data inside mission dispatch message is not processed",
    "No automatic error recovery in prototype",
]:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("ACK/Log Considerations", level=3)
for item in [
    "Three ACK statuses verified via log: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER",
    "Exact timeout threshold for TECHNISCHER_FEHLER not specified [NEEDS CLARIFICATION] — 10-second ACK requirement documented for WDX; UCRM timeout may differ",
    "Reverse flow timeout handling not explicitly specified [NEEDS CLARIFICATION]",
]:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading("Data Mapping Considerations", level=3)
doc.add_paragraph("Detailed UCRM-specific field mapping beyond WDX fields requires clarification from 'IPL-Mapping (UCRI)' document.", style='List Bullet')

# ── 3.9 Test Deliverables Checklist ──
doc.add_heading("3.9 Test Deliverables Checklist", level=2)
add_checklist(doc, [
    "Forward flow — Accept (EMPFANG) tested end-to-end",
    "Forward flow — Reject (EINSATZ_ABGELEHNT) tested end-to-end",
    "Forward flow — Timeout (TECHNISCHER_FEHLER) tested end-to-end",
    "Reverse flow (UCRM → Adapter → IPL) tested end-to-end",
    "Receiver validation logic verified",
    "P2P authentication at Handler verified",
    "Dispatcher message forwarding verified",
    "ACK log verification: EMPFANG, EINSATZ_ABGELEHNT, TECHNISCHER_FEHLER",
    "In-memory transport (Receiver → Handler → Dispatcher) validated",
    "Module enable/disable tested for all 3 services",
    "Field mapping accuracy verified",
    "Logging and traceability across all 3 services verified",
    "UCRM Test Client deployment validated",
    "Retry and DLQ handling validated",
    "All user stories covered with test scenarios",
])

# ── Save ──
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
outpath = rf"c:\Apparao Maroju\AI-SSI\Project-IGNIS(POC)\UCRI2.0-Output\UCRI2.0_Knowledge_Document_{timestamp}.docx"
doc.save(outpath)
print(f"Document saved to: {outpath}")
