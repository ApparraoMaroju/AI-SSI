"""
TickIT Plus Audit - Requirement Analysis Presentation Generator
Creates a professional PowerPoint presentation for the audit
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime
import os

# Configuration
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "TickIT_Audit_Requirement_Analysis.pptx")
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Template", "Template1.pptx")

# Color Scheme
PRIMARY_COLOR = RGBColor(0, 82, 147)      # Sopra Steria Blue
SECONDARY_COLOR = RGBColor(0, 150, 136)   # Teal
ACCENT_COLOR = RGBColor(255, 152, 0)      # Orange
TEXT_COLOR = RGBColor(51, 51, 51)         # Dark Gray
WHITE = RGBColor(255, 255, 255)

def add_title_slide(prs, title, subtitle):
    """Add title slide"""
    slide_layout = prs.slide_layouts[0]  # Title slide
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    if slide.shapes.title:
        title_shape = slide.shapes.title
        title_shape.text = title
        for paragraph in title_shape.text_frame.paragraphs:
            paragraph.font.size = Pt(44)
            paragraph.font.bold = True
            paragraph.font.color.rgb = PRIMARY_COLOR
    else:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5))
        title_tf = title_box.text_frame
        title_tf.text = title
        title_tf.paragraphs[0].font.size = Pt(44)
        title_tf.paragraphs[0].font.bold = True
        title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Find subtitle placeholder or create text box
    subtitle_shape = None
    for shape in slide.placeholders:
        if shape.placeholder_format.type == 4:  # Subtitle placeholder
            subtitle_shape = shape
            break
    
    if subtitle_shape:
        subtitle_shape.text = subtitle
        for paragraph in subtitle_shape.text_frame.paragraphs:
            paragraph.font.size = Pt(24)
            paragraph.font.color.rgb = TEXT_COLOR
    else:
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(12.3), Inches(2))
        subtitle_tf = subtitle_box.text_frame
        subtitle_tf.word_wrap = True
        subtitle_tf.text = subtitle
        for paragraph in subtitle_tf.paragraphs:
            paragraph.font.size = Pt(24)
            paragraph.font.color.rgb = TEXT_COLOR
            paragraph.alignment = PP_ALIGN.CENTER
    
    return slide

def add_content_slide(prs, title, bullet_points, notes=""):
    """Add content slide with bullets"""
    # Find a suitable layout with title and content
    slide_layout = None
    for layout in prs.slide_layouts:
        if layout.placeholders:
            has_title = any(ph.placeholder_format.type == 1 for ph in layout.placeholders)  # Title
            has_body = any(ph.placeholder_format.type == 2 for ph in layout.placeholders)   # Body
            if has_title and has_body:
                slide_layout = layout
                break
    
    if slide_layout is None:
        slide_layout = prs.slide_layouts[1] if len(prs.slide_layouts) > 1 else prs.slide_layouts[0]
    
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    if slide.shapes.title:
        title_shape = slide.shapes.title
        title_shape.text = title
        for paragraph in title_shape.text_frame.paragraphs:
            paragraph.font.size = Pt(32)
            paragraph.font.bold = True
            paragraph.font.color.rgb = PRIMARY_COLOR
    else:
        # Add title as text box
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
        title_tf = title_box.text_frame
        title_tf.text = title
        title_tf.paragraphs[0].font.size = Pt(32)
        title_tf.paragraphs[0].font.bold = True
        title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Find body placeholder or create text box
    body_shape = None
    for shape in slide.placeholders:
        if shape.placeholder_format.type == 2:  # Body placeholder
            body_shape = shape
            break
    
    if body_shape:
        tf = body_shape.text_frame
        tf.clear()
        for i, point in enumerate(bullet_points):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = point
            p.font.size = Pt(20)
            p.font.color.rgb = TEXT_COLOR
            p.level = 0
    else:
        # Create text box for bullets
        body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5.5))
        tf = body_box.text_frame
        tf.word_wrap = True
        for i, point in enumerate(bullet_points):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = "• " + point
            p.font.size = Pt(20)
            p.font.color.rgb = TEXT_COLOR
    
    # Add speaker notes
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
    
    return slide

def add_section_slide(prs, title, subtitle=""):
    """Add section divider slide"""
    slide_layout = prs.slide_layouts[0]  # Use first layout for section
    slide = prs.slides.add_slide(slide_layout)
    
    # Clear existing shapes that are not placeholders
    # Add title
    if slide.shapes.title:
        title_shape = slide.shapes.title
        title_shape.text = title
        for paragraph in title_shape.text_frame.paragraphs:
            paragraph.font.size = Pt(40)
            paragraph.font.bold = True
            paragraph.font.color.rgb = PRIMARY_COLOR
            paragraph.alignment = PP_ALIGN.CENTER
    else:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(12.3), Inches(1.5))
        title_tf = title_box.text_frame
        title_tf.text = title
        title_tf.paragraphs[0].font.size = Pt(40)
        title_tf.paragraphs[0].font.bold = True
        title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
        title_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(4), Inches(12.3), Inches(1))
        subtitle_tf = subtitle_box.text_frame
        subtitle_tf.text = subtitle
        subtitle_tf.paragraphs[0].font.size = Pt(20)
        subtitle_tf.paragraphs[0].font.color.rgb = TEXT_COLOR
        subtitle_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    return slide

def add_two_column_slide(prs, title, left_content, right_content, notes=""):
    """Add two-column content slide"""
    slide_layout = prs.slide_layouts[0]  # Use basic layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8))
    title_tf = title_box.text_frame
    title_tf.text = title
    title_tf.paragraphs[0].font.size = Pt(32)
    title_tf.paragraphs[0].font.bold = True
    title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Add left text box
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(5.8), Inches(5.5))
    left_tf = left_box.text_frame
    left_tf.word_wrap = True
    
    for i, item in enumerate(left_content):
        if i == 0:
            p = left_tf.paragraphs[0]
        else:
            p = left_tf.add_paragraph()
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_COLOR
        if item.endswith(":"):  # Header text
            p.font.bold = True
            p.font.color.rgb = PRIMARY_COLOR
    
    # Add right text box
    right_box = slide.shapes.add_textbox(Inches(6.8), Inches(1.3), Inches(5.8), Inches(5.5))
    right_tf = right_box.text_frame
    right_tf.word_wrap = True
    
    for i, item in enumerate(right_content):
        if i == 0:
            p = right_tf.paragraphs[0]
        else:
            p = right_tf.add_paragraph()
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_COLOR
        if item.endswith(":"):  # Header text
            p.font.bold = True
            p.font.color.rgb = PRIMARY_COLOR
    
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
    
    return slide

def add_table_slide(prs, title, headers, rows, notes=""):
    """Add slide with table"""
    slide_layout = prs.slide_layouts[0]  # Use basic layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8))
    title_tf = title_box.text_frame
    title_tf.text = title
    title_tf.paragraphs[0].font.size = Pt(32)
    title_tf.paragraphs[0].font.bold = True
    title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Create table
    num_cols = len(headers)
    num_rows = len(rows) + 1
    
    # Calculate table height based on rows
    row_height = 0.45
    table_height = min(num_rows * row_height, 5.5)
    
    table_shape = slide.shapes.add_table(num_rows, num_cols, Inches(0.5), Inches(1.3), Inches(12.3), Inches(table_height))
    table = table_shape.table
    
    # Set column widths
    col_width = Inches(12.3 / num_cols)
    for i in range(num_cols):
        table.columns[i].width = col_width
    
    # Add headers
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(14)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_COLOR
    
    # Add data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_data in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(cell_data)
            cell.text_frame.paragraphs[0].font.size = Pt(12)
            cell.text_frame.paragraphs[0].font.color.rgb = TEXT_COLOR
    
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
    
    return slide

def add_flow_diagram_slide(prs, title, steps, notes=""):
    """Add slide with flow diagram representation"""
    slide_layout = prs.slide_layouts[0]  # Use basic layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8))
    title_tf = title_box.text_frame
    title_tf.text = title
    title_tf.paragraphs[0].font.size = Pt(32)
    title_tf.paragraphs[0].font.bold = True
    title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    
    # Create flow boxes - arrange in rows of 5
    num_steps = len(steps)
    box_width = Inches(2.2)
    box_height = Inches(0.55)
    start_x = Inches(0.4)
    y_position = Inches(1.5)
    h_spacing = Inches(0.3)
    v_spacing = Inches(0.9)
    
    boxes_per_row = 5
    
    for i, step in enumerate(steps):
        row = i // boxes_per_row
        col = i % boxes_per_row
        
        x = start_x + col * (box_width + h_spacing)
        y = y_position + row * (box_height + v_spacing)
        
        # Add box
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x, y, box_width, box_height
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = PRIMARY_COLOR
        shape.line.color.rgb = PRIMARY_COLOR
        
        # Add text
        text_frame = shape.text_frame
        text_frame.text = step
        text_frame.paragraphs[0].font.size = Pt(11)
        text_frame.paragraphs[0].font.color.rgb = WHITE
        text_frame.paragraphs[0].font.bold = True
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.word_wrap = True
        
        # Add arrow to next box (if not last in row and not last overall)
        if i < num_steps - 1:
            next_col = (i + 1) % boxes_per_row
            if next_col != 0:  # Same row arrow
                arrow_x = x + box_width + Inches(0.02)
                arrow = slide.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW,
                    arrow_x, y + Inches(0.15), Inches(0.25), Inches(0.25)
                )
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = SECONDARY_COLOR
                arrow.line.fill.background()
    
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
    
    return slide

def add_thank_you_slide(prs):
    """Add thank you slide"""
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    
    # Add Thank You title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.5))
    title_tf = title_box.text_frame
    title_tf.text = "Thank You"
    title_tf.paragraphs[0].font.size = Pt(48)
    title_tf.paragraphs[0].font.bold = True
    title_tf.paragraphs[0].font.color.rgb = PRIMARY_COLOR
    title_tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Add contact info
    contact_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.5), Inches(12.3), Inches(3))
    contact_tf = contact_box.text_frame
    contact_tf.word_wrap = True
    
    lines = [
        "Questions & Discussion",
        "",
        "Apparao Maroju",
        "Scrum Master",
        "Sopra Steria Sales CRM Team"
    ]
    
    for i, line in enumerate(lines):
        if i == 0:
            p = contact_tf.paragraphs[0]
        else:
            p = contact_tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.CENTER
        if i == 0:
            p.font.size = Pt(28)
            p.font.color.rgb = SECONDARY_COLOR
        elif line == "":
            p.font.size = Pt(14)
        else:
            p.font.size = Pt(20)
            p.font.color.rgb = TEXT_COLOR
    
    return slide

def create_presentation():
    """Main function to create the TickIT Audit presentation"""
    
    # Create a new blank presentation with proper dimensions
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)
    print("Creating professional TickIT Audit presentation")
    
    # ================================================
    # SLIDE 1: Cover Slide
    # ================================================
    add_title_slide(
        prs,
        "TickIT Plus Audit",
        "Requirement Analysis Process\nSopra Steria Sales CRM\n\nPresented by: Apparao Maroju, Scrum Master\nDate: " + datetime.now().strftime("%B %d, %Y")
    )
    
    # ================================================
    # SLIDE 2: Agenda
    # ================================================
    add_content_slide(
        prs,
        "Agenda",
        [
            "Project Overview & Audit Scope",
            "Business Context",
            "Scrum Delivery Model",
            "Requirement Analysis Process",
            "Backlog Refinement & Solution Design",
            "Quality Gates & Definition of Ready",
            "Requirement Traceability",
            "Risk Controls & Key Evidence",
            "Key Performance Indicators",
            "Summary & Q&A"
        ],
        notes="Welcome to the TickIT Plus Audit presentation for Requirement Analysis. This presentation covers our comprehensive approach to requirement management within our Agile Scrum framework. We will demonstrate how our processes align with TickIT Plus standards and our Ways of Working."
    )
    
    # ================================================
    # SLIDE 3: Project Overview
    # ================================================
    add_content_slide(
        prs,
        "Project Overview",
        [
            "Project: Sopra Steria Sales CRM",
            "Audit Scope: Requirement Analysis Process",
            "Standards: TickIT Plus, Agile Scrum, Ways of Working",
            "Methodology: Agile Scrum",
            "Sprint Duration: 2 Weeks"
        ],
        notes="Our project is the Sopra Steria Sales CRM platform. The audit focuses specifically on our Requirement Analysis process. We follow TickIT Plus standards integrated with Agile Scrum methodology, delivering in 2-week sprint cycles. Our Ways of Working document defines our operational practices."
    )
    
    # ================================================
    # SLIDE 4: Business Overview
    # ================================================
    add_two_column_slide(
        prs,
        "Business Overview",
        [
            "Application Scope:",
            "• Sopra Steria SE (Germany)",
            "• Sopra Steria Austria",
            "• ISS Software GmbH",
            "• it-economics GmbH"
        ],
        [
            "Business Users:",
            "• Marketing",
            "• Pre-Sales",
            "• Industrial Direction",
            "• Finance & Controlling"
        ],
        notes="The Sales CRM platform serves four entities across Germany and Austria. Key business stakeholders include Marketing, Pre-Sales, Industrial Direction, and Finance & Controlling teams who rely on this platform for their daily operations."
    )
    
    # ================================================
    # SLIDE 5: Scrum Delivery Model
    # ================================================
    add_flow_diagram_slide(
        prs,
        "Scrum Delivery Model",
        [
            "Business Request",
            "Product Backlog",
            "Backlog Refinement",
            "Solution Design",
            "Story Estimation",
            "Definition of Ready",
            "Sprint Planning",
            "Development",
            "Testing",
            "Deployment"
        ],
        notes="Our Scrum delivery model follows a structured flow from business request to deployment. Each stage has defined inputs, outputs, and quality gates. This ensures requirements are properly analyzed and validated before entering development."
    )
    
    # ================================================
    # SLIDE 6: Requirement Analysis Objective
    # ================================================
    add_content_slide(
        prs,
        "Requirement Analysis Objective",
        [
            "Ensure every PBI is fully understood before Sprint entry",
            "Validate business value and acceptance criteria",
            "Conduct technical feasibility assessment",
            "Identify and resolve dependencies",
            "Accurate effort estimation through Planning Poker"
        ],
        notes="The primary objective of our requirement analysis process is to ensure every Product Backlog Item is thoroughly understood, designed, estimated, and validated before it enters a Sprint. This reduces development risks and ensures predictable delivery."
    )
    
    # ================================================
    # SLIDE 7: Requirement Inputs & Outputs
    # ================================================
    add_two_column_slide(
        prs,
        "Requirement Inputs & Outputs",
        [
            "INPUTS:",
            "• Business Requests",
            "• User Feedback",
            "• Product Owner Priorities",
            "• Operational Enhancements",
            "• Compliance Requirements"
        ],
        [
            "OUTPUT:",
            "• Ready for Sprint User Stories",
            "• Complete acceptance criteria",
            "• Estimated story points",
            "• Identified dependencies",
            "• Solution approach"
        ],
        notes="Requirement inputs come from multiple sources including business requests, user feedback, and compliance requirements. The output is always a Ready for Sprint User Story that meets our Definition of Ready criteria."
    )
    
    # ================================================
    # SLIDE 8: Backlog Refinement Process
    # ================================================
    add_content_slide(
        prs,
        "Backlog Refinement Process",
        [
            "Product Owner selects User Stories for refinement",
            "Team reviews business context and functional requirements",
            "Technical discussion and feasibility assessment",
            "Dependency identification across systems",
            "Initial solution proposal and design",
            "Story estimation using Planning Poker",
            "Definition of Ready validation"
        ],
        notes="Backlog refinement is a collaborative session where the team works together to understand, discuss, and prepare user stories. Stories are refined until they satisfy our Definition of Ready criteria."
    )
    
    # ================================================
    # SLIDE 9: Backlog Refinement Workflow
    # ================================================
    add_flow_diagram_slide(
        prs,
        "Backlog Refinement Workflow",
        [
            "Select Story",
            "Business Context",
            "Discussion",
            "Solution Design",
            "Planning Poker",
            "Definition of Ready",
            "Ready for Sprint"
        ],
        notes="The refinement workflow ensures each story progresses through structured stages. From selection through to Ready for Sprint status, each step validates different aspects of the requirement."
    )
    
    # ================================================
    # SLIDE 10: Solution Design
    # ================================================
    add_content_slide(
        prs,
        "Solution Design",
        [
            "Purpose: Develop technical approach before estimation",
            "Technical discussion with development team",
            "Dependency analysis across Salesforce components",
            "Feasibility assessment for complex requirements",
            "Solution validation with Product Owner",
            "Applicable to: Complex User Stories requiring design"
        ],
        notes="Solution design is conducted for complex user stories that require technical analysis. This ensures the team understands the implementation approach before committing to estimates."
    )
    
    # ================================================
    # SLIDE 11: Story Estimation
    # ================================================
    add_content_slide(
        prs,
        "Story Estimation: Planning Poker",
        [
            "Method: Planning Poker (Team-based estimation)",
            "Process: Consensus-driven discussion",
            "Scale: 1 Story Point ≈ 1 Engineering Day",
            "Complex stories refined across multiple sessions",
            "Allows independent solution thinking",
            "All team members participate in estimation"
        ],
        notes="We use Planning Poker for estimation, ensuring team consensus. One story point represents approximately one engineering day of effort. Complex stories may require multiple refinement sessions to reach accurate estimates."
    )
    
    # ================================================
    # SLIDE 12: Definition of Ready (DoR)
    # ================================================
    add_content_slide(
        prs,
        "Definition of Ready (DoR)",
        [
            "Quality gate before Sprint Planning entry",
            "✓ Business value clearly defined",
            "✓ Acceptance criteria available and testable",
            "✓ Initial solution design completed",
            "✓ Dependencies identified and documented",
            "✓ Story estimated using Planning Poker",
            "✓ INVEST criteria validated"
        ],
        notes="The Definition of Ready is our quality gate ensuring stories are properly prepared before Sprint entry. Each criterion must be satisfied, documented, and validated by the team."
    )
    
    # ================================================
    # SLIDE 13: INVEST Criteria
    # ================================================
    add_table_slide(
        prs,
        "INVEST Criteria Validation",
        ["Criterion", "Description"],
        [
            ["Independent", "Can be implemented independently"],
            ["Negotiable", "Details evolve through discussion"],
            ["Valuable", "Delivers measurable business value"],
            ["Estimable", "Team can estimate effort accurately"],
            ["Small", "Fits within a single Sprint"],
            ["Testable", "Acceptance criteria are measurable"]
        ],
        notes="The INVEST criteria ensure each user story is well-formed. We validate each criterion during backlog refinement to ensure stories are properly structured."
    )
    
    # ================================================
    # SLIDE 14: Clarification Call Process
    # ================================================
    add_content_slide(
        prs,
        "Clarification Call Process",
        [
            "Purpose: Resolve outstanding questions promptly",
            "Frequency: Daily (as required)",
            "Participants: PO, Scrum Master, Development Team",
            "Outcomes:",
            "  • Blockers resolved same day",
            "  • Requirements clarified",
            "  • Interim reviews conducted when needed"
        ],
        notes="Daily clarification calls ensure any questions or blockers are addressed immediately. This maintains development momentum and prevents requirement ambiguity from impacting delivery."
    )
    
    # ================================================
    # SLIDE 15: Sprint Planning
    # ================================================
    add_content_slide(
        prs,
        "Sprint Planning",
        [
            "Only Ready for Sprint stories can enter Sprint",
            "Sprint Goal presented by Product Owner",
            "Team capacity reviewed and validated",
            "User Stories selected based on priority and capacity",
            "Sprint Backlog finalized",
            "Team commits to Sprint delivery"
        ],
        notes="Sprint Planning ensures only properly refined stories enter the Sprint. The team commits to delivery based on validated capacity and story readiness."
    )
    
    # ================================================
    # SLIDE 16: Requirement Quality Gates
    # ================================================
    add_table_slide(
        prs,
        "Requirement Quality Gates",
        ["Stage", "Quality Check"],
        [
            ["Requirement Capture", "Business Need Validated"],
            ["Backlog Refinement", "Functional Review Complete"],
            ["Solution Design", "Technical Review Approved"],
            ["Estimation", "Planning Poker Completed"],
            ["Definition of Ready", "INVEST Compliance Verified"],
            ["Sprint Planning", "Capacity Validation Done"]
        ],
        notes="Each stage of our requirement process has a defined quality check. These gates ensure requirements progress only when properly validated."
    )
    
    # ================================================
    # SLIDE 17: Project Organization
    # ================================================
    add_two_column_slide(
        prs,
        "Project Organization",
        [
            "Onsite Team:",
            "• Business Sponsor: Marion Dietrich",
            "• Product Owner: Christoph Zaenker",
            "• Business Analyst: Fractional BA",
            "",
            "QA Team:",
            "• Test Manager: Manish Singhal",
            "• Test Engineer: Rishabh Bhatt"
        ],
        [
            "Offshore Team:",
            "• DU Head: Vishal Kalra",
            "• Scrum Master: Apparao Maroju",
            "• Account Expert: Ila",
            "• Ops Manager: Charu Bisht",
            "• Developers: Sunaina, Manmohan",
            "  Pratap, Shashwat Mishra"
        ],
        notes="Our distributed team structure ensures proper coverage across roles. Clear ownership and responsibilities are defined for requirement analysis activities."
    )
    
    # ================================================
    # SLIDE 18: Types of Work
    # ================================================
    add_content_slide(
        prs,
        "Types of Work",
        [
            "User Story:",
            "  • Functional or technical enhancements",
            "  • Full Scrum lifecycle application",
            "  • Complete refinement and estimation",
            "",
            "Minor Change:",
            "  • Small configuration changes",
            "  • Completed within ~4 hours",
            "  • Streamlined approval process"
        ],
        notes="We categorize work into User Stories requiring full Scrum process and Minor Changes for small configuration updates. This ensures appropriate process rigor for different work types."
    )
    
    # ================================================
    # SLIDE 19: Requirement Traceability
    # ================================================
    add_table_slide(
        prs,
        "Requirement Traceability",
        ["Phase", "Evidence"],
        [
            ["Business Request", "Business Requirement"],
            ["Product Backlog", "Jira PBI"],
            ["Solution Design", "Design Documentation"],
            ["Estimation", "Planning Poker Record"],
            ["Ready for Sprint", "DoR Checklist"],
            ["Sprint Planning", "Sprint Backlog"],
            ["Development", "Source Code"],
            ["Testing", "Test Cases"],
            ["Deployment", "Release Notes"]
        ],
        notes="Complete traceability is maintained from business request through deployment. Each phase produces documented evidence that links back to the original requirement."
    )
    
    # ================================================
    # SLIDE 20: Business Change Categories
    # ================================================
    add_content_slide(
        prs,
        "Business Change Categories",
        [
            "Process Changes: Lead Qualification Workflows",
            "Workflow Automation: Salesforce Flows",
            "Data Management: Data Migration & Quality",
            "Sales Process: Opportunity Stage Management",
            "Service Process: Case Routing Rules",
            "Reporting: Dashboards & Analytics",
            "Integration: ERP System Connectivity"
        ],
        notes="We handle diverse business change categories within Salesforce. Each category follows our standard requirement analysis process with domain-specific validation."
    )
    
    # ================================================
    # SLIDE 21: AI Usage & Controls
    # ================================================
    add_content_slide(
        prs,
        "AI Usage & Quality Safeguards",
        [
            "OpenAI Policy: Commercial tools prohibited",
            "Intellectual property protection enforced",
            "Data privacy requirements maintained",
            "GitHub Copilot: Approved for limited use",
            "  • Test design assistance",
            "  • Documentation support",
            "Mandatory: Human review of all AI outputs"
        ],
        notes="We have strict controls on AI tool usage. GitHub Copilot is approved only for test design and documentation, with mandatory human review of all AI-assisted outputs."
    )
    
    # ================================================
    # SLIDE 22: Risk Controls
    # ================================================
    add_table_slide(
        prs,
        "Risk Controls",
        ["Risk", "Control Measure"],
        [
            ["Requirement ambiguity", "Clarification Calls"],
            ["Missing acceptance criteria", "Definition of Ready"],
            ["Poor estimation", "Planning Poker"],
            ["Scope creep", "Sprint Planning gate"],
            ["Dependency issues", "Backlog Refinement"]
        ],
        notes="Each identified risk has a corresponding control measure. These controls are embedded in our standard processes to ensure consistent risk management."
    )
    
    # ================================================
    # SLIDE 23: Key Audit Evidence
    # ================================================
    add_two_column_slide(
        prs,
        "Key Audit Evidence",
        [
            "Process Artifacts:",
            "• Jira Product Backlog",
            "• User Stories & Sprint Backlogs",
            "• Planning Poker Estimates",
            "• Definition of Ready Checklist",
            "• Acceptance Criteria",
            "• Solution Design Documents"
        ],
        [
            "Meeting Records:",
            "• Clarification Call Notes",
            "• Sprint Planning Minutes",
            "• Capacity Planner",
            "• Sprint Reviews",
            "• Retrospectives",
            "• Confluence Ways of Working"
        ],
        notes="All audit evidence is maintained in Jira and Confluence. We can demonstrate traceability and compliance through these documented artifacts."
    )
    
    # ================================================
    # SLIDE 24: Key Performance Indicators
    # ================================================
    add_table_slide(
        prs,
        "Key Performance Indicators",
        ["KPI", "Target"],
        [
            ["Definition of Ready Compliance", "100%"],
            ["Story Estimation Coverage", "100%"],
            ["Acceptance Criteria Completeness", "100%"],
            ["Story Traceability", "100%"],
            ["Refinement Cadence", "Weekly"],
            ["Clarification Resolution", "Same Day"]
        ],
        notes="Our KPIs ensure consistent quality in requirement analysis. We target 100% compliance on all quality metrics with weekly refinement cadence and same-day clarification resolution."
    )
    
    # ================================================
    # SLIDE 25: Continuous Improvement
    # ================================================
    add_content_slide(
        prs,
        "Continuous Improvement",
        [
            "Sprint Retrospectives after each Sprint",
            "Lessons Learned documentation",
            "Root Cause Analysis for issues",
            "Process Optimization initiatives",
            "Quality Metrics Review monthly",
            "Backlog Health Monitoring weekly"
        ],
        notes="Continuous improvement is embedded in our process through retrospectives and regular reviews. We analyze metrics and implement process optimizations to enhance our requirement analysis capability."
    )
    
    # ================================================
    # SLIDE 26: Key Takeaways
    # ================================================
    add_content_slide(
        prs,
        "Key Takeaways",
        [
            "✓ Structured requirement analysis process",
            "✓ Defined governance and quality gates",
            "✓ End-to-end requirement traceability",
            "✓ Agile Scrum aligned with TickIT Plus",
            "✓ Continuous stakeholder collaboration",
            "✓ Human-reviewed AI usage",
            "✓ Continuous process improvement"
        ],
        notes="In summary, our requirement analysis process is comprehensive, structured, and aligned with TickIT Plus standards. We maintain full traceability and continuous improvement culture."
    )
    
    # ================================================
    # SLIDE 27: Thank You
    # ================================================
    add_thank_you_slide(prs)
    
    # Save the presentation
    prs.save(OUTPUT_PATH)
    print(f"\n✓ Presentation created successfully!")
    print(f"  Location: {OUTPUT_PATH}")
    print(f"  Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    create_presentation()
