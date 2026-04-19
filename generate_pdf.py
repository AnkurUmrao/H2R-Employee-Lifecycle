"""
generate_pdf.py
Generates the 5-page A4 project documentation PDF as required by Capstone guidelines.
Format: A4, Arial (simulated via Helvetica), Justified, Page number bottom-right.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "H2R_SAP_HR_Project_Documentation.pdf")

W, H = A4

# ── Page template with header + footer ──────────────────────────────────────
class DocCanvas:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, canv, doc):
        canv.saveState()
        # Header bar
        canv.setFillColor(colors.HexColor("#1a2433"))
        canv.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
        canv.setFont("Helvetica-Bold", 10)
        canv.setFillColor(colors.white)
        canv.drawString(1.5*cm, H - 0.75*cm, "SAP HR — Hire-to-Retire (H2R) Employee Lifecycle Portal")
        canv.drawRightString(W - 1.5*cm, H - 0.75*cm, "KIIT Capstone Project 2026")

        # Footer line
        canv.setStrokeColor(colors.HexColor("#dee2e8"))
        canv.line(1.5*cm, 1.3*cm, W - 1.5*cm, 1.3*cm)
        canv.setFont("Helvetica", 8)
        canv.setFillColor(colors.HexColor("#667788"))
        canv.drawString(1.5*cm, 0.8*cm, "Hire-to-Retire (H2R) — Employee Lifecycle in SAP HR")
        # Page number bottom-right
        canv.drawRightString(W - 1.5*cm, 0.8*cm, f"Page {doc.page}")
        canv.restoreState()


def build_styles():
    s = {}
    s["title"] = ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=22,
        alignment=TA_CENTER, textColor=colors.HexColor("#0070f2"),
        spaceAfter=6
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=13,
        alignment=TA_CENTER, textColor=colors.HexColor("#445566"),
        spaceAfter=4
    )
    s["meta"] = ParagraphStyle(
        "meta", fontName="Helvetica", fontSize=11,
        alignment=TA_CENTER, textColor=colors.HexColor("#667788"),
        spaceAfter=2
    )
    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=15,
        textColor=colors.HexColor("#1a2433"), spaceBefore=16, spaceAfter=6,
        borderPad=4
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13,
        textColor=colors.HexColor("#0070f2"), spaceBefore=12, spaceAfter=4
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=12,
        alignment=TA_JUSTIFY, leading=18, spaceAfter=8,
        textColor=colors.HexColor("#1a2433")
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=12,
        alignment=TA_JUSTIFY, leading=18, spaceAfter=4,
        leftIndent=16, textColor=colors.HexColor("#1a2433")
    )
    s["code"] = ParagraphStyle(
        "code", fontName="Courier", fontSize=10,
        backColor=colors.HexColor("#f4f6f9"),
        borderColor=colors.HexColor("#dee2e8"),
        borderWidth=1, borderPad=6,
        leading=14, spaceAfter=8,
        textColor=colors.HexColor("#1a2433")
    )
    s["caption"] = ParagraphStyle(
        "caption", fontName="Helvetica-Oblique", fontSize=10,
        alignment=TA_CENTER, textColor=colors.HexColor("#667788"),
        spaceAfter=8
    )
    return s

def divider(color="#0070f2", thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness,
                      color=colors.HexColor(color), spaceAfter=8, spaceBefore=4)


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm
    )
    s = build_styles()
    story = []
    cb = DocCanvas(OUTPUT)

    # ═══════════════════════════════════════════════════════════════════
    # PAGE 1 — TITLE PAGE
    # ═══════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 2.5*cm))

    # Blue title block
    title_data = [[Paragraph(
        "Hire-to-Retire (H2R)<br/>Employee Lifecycle Portal",
        ParagraphStyle("tb", fontName="Helvetica-Bold", fontSize=24,
                       textColor=colors.white, alignment=TA_CENTER, leading=32)
    )]]
    title_table = Table(title_data, colWidths=[W - 4.6*cm])
    title_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0070f2")),
        ("TOPPADDING",    (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING",   (0, 0), (-1, -1), 24),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 24),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 0.6*cm))

    story.append(Paragraph("SAP Human Capital Management (HCM) Simulation", s["subtitle"]))
    story.append(Spacer(1, 2*cm))

    meta = [
        ["Program", "SAP Functional & Technical Training"],
        ["Institute", "KIIT — Capstone Project 2026"],
        ["Topic", "Hire-to-Retire (H2R) — Employee Lifecycle in SAP HR"],
        ["Tech Stack", "Python 3.10 | Flask 3.0 | ReportLab | JSON"],
        ["Submission", "April 21, 2026"],
    ]
    mt = Table(meta, colWidths=[4.5*cm, 10*cm])
    mt.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",  (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0070f2")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1a2433")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1),
         [colors.HexColor("#f4f6f9"), colors.white]),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("BOX",    (0, 0), (-1, -1), 1, colors.HexColor("#dee2e8")),
        ("INNERGRID",(0,0),(-1,-1), 0.5, colors.HexColor("#dee2e8")),
    ]))
    story.append(mt)
    story.append(Spacer(1, 2*cm))

    story.append(Paragraph(
        "This project simulates the complete end-to-end SAP HR Hire-to-Retire lifecycle, "
        "covering hiring, master data management, time management, payroll processing, "
        "training, promotions, and employee separation — mapped to real SAP transactions "
        "and infotypes.",
        ParagraphStyle("intro", fontName="Helvetica-Oblique", fontSize=12,
                       alignment=TA_CENTER, textColor=colors.HexColor("#445566"),
                       leading=20)
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # PAGE 2 — PROBLEM STATEMENT + SOLUTION OVERVIEW
    # ═══════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Problem Statement", s["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "Managing the complete employee lifecycle in an enterprise is one of the most "
        "complex HR challenges. From the moment a candidate accepts an offer to the day "
        "they retire or resign, HR teams must handle hundreds of data points, statutory "
        "compliance requirements, payroll cycles, leave records, training programs, and "
        "organisational changes — all while ensuring data accuracy and audit traceability.",
        s["body"]
    ))
    story.append(Paragraph(
        "SAP HCM (Human Capital Management) provides a robust framework for managing "
        "this end-to-end lifecycle. However, understanding and configuring these processes "
        "requires hands-on experience that is difficult to gain without a live SAP system. "
        "This project bridges that gap by building a fully functional H2R simulation "
        "application that mirrors SAP HCM's core modules, transactions, and infotype logic.",
        s["body"]
    ))

    story.append(Paragraph("Key Challenges Addressed", s["h2"]))
    challenges = [
        ("Fragmented Employee Data", "Employee personal, organisational, and pay data must "
         "be maintained in structured infotypes (IT0001, IT0002, IT0008) — this project "
         "replicates that structure using a JSON-based master data store."),
        ("Payroll Compliance", "Indian payroll involves complex statutory deductions: "
         "Provident Fund (PF), Employee State Insurance (ESI), Professional Tax (PT), "
         "and Tax Deducted at Source (TDS). The system calculates all of these automatically."),
        ("Audit Trail Requirements", "Every HR action (hiring, promotion, separation) must "
         "be logged with effective dates — replicated here as an IT0000-style actions log."),
        ("Lifecycle Continuity", "The system must track the full arc from Day 1 onboarding "
         "to final separation, including mid-cycle events like transfers and training."),
    ]
    for title, desc in challenges:
        story.append(Paragraph(
            f"<b>{title}:</b> {desc}", s["bullet"]
        ))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("2. Solution & Features", s["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "The H2R Employee Lifecycle Portal is a web-based SAP HR simulation built with "
        "Python (Flask) on the backend and a custom SAP-inspired UI on the frontend. "
        "Each module corresponds directly to a SAP transaction code or infotype, providing "
        "a realistic simulation of enterprise HR processes.",
        s["body"]
    ))

    features = [
        ["Module", "SAP Equivalent", "Description"],
        ["Hire Employee",       "PA40 → Hiring Action",      "Captures IT0001, IT0002, IT0008 data"],
        ["Master Data",         "PA30 Maintain HR Master",   "Edit personal, org, and pay details"],
        ["Time Management",     "IT2001 Absences",           "Leave types, dates, auto day-count"],
        ["Payroll Processing",  "PC00_M99_CALC Driver",      "Gross, PF/ESI/PT/TDS, net payslip"],
        ["Training & Dev",      "LSO Learning Solution",     "Course enrollment and status tracking"],
        ["Promotion/Transfer",  "PA40 Promotion/Transfer",   "Role change + salary revision + log"],
        ["Separation",          "PA40 Leaving (IT0000=0)",   "Reason, last working day, deactivation"],
    ]
    ft = Table(features, colWidths=[3.8*cm, 4.5*cm, 6.5*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#1a2433")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.HexColor("#f4f6f9"), colors.white]),
        ("TEXTCOLOR",     (0, 1), (0, -1),  colors.HexColor("#0070f2")),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e8")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(ft)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # PAGE 3 — TECH STACK + SYSTEM ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Tech Stack", s["h1"]))
    story.append(divider())

    tech = [
        ["Layer", "Technology", "Purpose"],
        ["Backend Framework", "Python 3.10 + Flask 3.0",  "Route handling, business logic, REST API"],
        ["Frontend",          "HTML5 + CSS3 + JS",         "SAP-inspired responsive UI"],
        ["Data Layer",        "JSON Flat Files",            "Simulates SAP HR database tables"],
        ["PDF Reports",       "ReportLab 4.2",              "Project documentation generation"],
        ["Payroll Engine",    "Pure Python",                "PF, ESI, PT, TDS calculations"],
        ["Styling",           "Custom CSS Variables",       "SAP Fiori-inspired design system"],
    ]
    tt = Table(tech, colWidths=[4*cm, 5*cm, 5.8*cm])
    tt.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#0070f2")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f4f6f9")]),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e8")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(tt)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("4. System Architecture", s["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "The application follows a clean MVC (Model-View-Controller) pattern aligned with "
        "Flask conventions. The architecture separates concerns across three distinct layers:",
        s["body"]
    ))

    arch_items = [
        ("Model (hr_processes.py)",
         "All SAP HR business logic resides here. Functions map directly to SAP personnel "
         "actions — hire_employee() mirrors PA40 Hiring, process_payroll() mirrors the "
         "PC00_M99_CALC payroll driver, and terminate_employee() mirrors the PA40 Leaving "
         "action. Data is persisted in two JSON files: employees.json and payroll.json."),
        ("View (templates/)",
         "Eleven Jinja2 HTML templates render the user interface. The base.html template "
         "provides a persistent SAP-inspired sidebar with navigation to all modules. Each "
         "functional page corresponds to a specific SAP transaction: hire.html mirrors PA40, "
         "employee_detail.html mirrors PA20/PA30, and payroll.html mirrors the payroll "
         "processing cockpit."),
        ("Controller (app.py)",
         "Flask routes connect HTTP requests to business logic and templates. Eight primary "
         "routes handle the full H2R lifecycle. A JSON REST endpoint (/api/employee/<id>) "
         "provides AJAX data access for dynamic UI updates."),
    ]
    for layer, desc in arch_items:
        story.append(Paragraph(f"<b>{layer}:</b> {desc}", s["bullet"]))
        story.append(Spacer(1, 0.1*cm))

    story.append(Paragraph("Project File Structure", s["h2"]))
    story.append(Paragraph(
        "app.py  |  hr_processes.py  |  seed_data.py  |  requirements.txt<br/>"
        "data/ (employees.json, payroll.json)<br/>"
        "templates/ (11 HTML templates)<br/>"
        "static/css/style.css  |  static/js/main.js",
        s["code"]
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # PAGE 4 — PAYROLL + SCREENSHOTS DESCRIPTION
    # ═══════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Payroll Calculation Engine", s["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "One of the most critical components of any SAP HR implementation is the payroll "
        "engine. The application includes a fully functional Indian payroll calculator "
        "that mirrors the logic of SAP's PC00_M99_CALC payroll driver.",
        s["body"]
    ))

    pay_data = [
        ["Component",          "Formula / Value",                    "Type"],
        ["Basic Salary",       "As configured in IT0008",             "Earning"],
        ["HRA",                "40% of Basic Salary",                 "Earning"],
        ["Transport Allowance","Fixed: Rs. 1,600 per month",          "Earning"],
        ["Special Allowance",  "10% of Basic Salary",                 "Earning"],
        ["Gross Pay",          "Basic + HRA + TA + Special Allow.",   "Total Earning"],
        ["PF Deduction",       "12% of Basic (Employee share)",       "Statutory Deduction"],
        ["ESI",                "0.75% of Gross (if Gross <= Rs.21k)", "Statutory Deduction"],
        ["Professional Tax",   "Rs. 200 flat per month",              "Statutory Deduction"],
        ["TDS",                "Simplified slab: 5% above Rs.2.5L pa","Statutory Deduction"],
        ["Net Pay",            "Gross Pay - Total Deductions",        "Final Disbursement"],
    ]
    pt = Table(pay_data, colWidths=[4.5*cm, 6.5*cm, 3.8*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#30914c")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f4f6f9")]),
        ("TEXTCOLOR",     (0, 10), (-1, 10), colors.HexColor("#30914c")),
        ("FONTNAME",      (0, 10), (-1, 10), "Helvetica-Bold"),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e8")),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.4*cm))

    story.append(Paragraph("Sample Payroll Output (EMP100001 — Arjun Sharma)", s["h2"]))
    sample = [
        ["Earnings", "Amount (Rs.)", "Deductions", "Amount (Rs.)"],
        ["Basic Salary",        "85,000.00", "PF (12%)",         "10,200.00"],
        ["HRA (40%)",           "34,000.00", "ESI",              "0.00"],
        ["Transport Allow.",    " 1,600.00", "Professional Tax", "  200.00"],
        ["Special Allow. (10%)","8,500.00",  "TDS",              "2,813.33"],
        ["",                    "",          "",                  ""],
        ["Gross Pay",           "1,29,100.00","Total Deductions","13,213.33"],
        ["",                    "",          "NET PAY",          "1,15,886.67"],
    ]
    st = Table(sample, colWidths=[4.5*cm, 3.2*cm, 4.5*cm, 3.2*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),   colors.HexColor("#1a2433")),
        ("TEXTCOLOR",    (0, 0), (-1, 0),   colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),   "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1),  10),
        ("FONTNAME",     (0, 1), (-1, -1),  "Helvetica"),
        ("FONTNAME",     (0, 6), (-1, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",    (2, 7), (3, 7),    colors.HexColor("#30914c")),
        ("ROWBACKGROUNDS",(0,1),(-1,5),
         [colors.white, colors.HexColor("#f4f6f9")]),
        ("BACKGROUND",   (0, 6), (-1, 6),   colors.HexColor("#eef0f3")),
        ("BACKGROUND",   (0, 7), (-1, 7),   colors.HexColor("#e6f4ea")),
        ("GRID",         (0, 0), (-1, -1),  0.5, colors.HexColor("#dee2e8")),
        ("TOPPADDING",   (0, 0), (-1, -1),  7),
        ("BOTTOMPADDING",(0, 0), (-1, -1),  7),
        ("LEFTPADDING",  (0, 0), (-1, -1),  10),
        ("ALIGN",        (1, 0), (1, -1),   "RIGHT"),
        ("ALIGN",        (3, 0), (3, -1),   "RIGHT"),
    ]))
    story.append(st)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # PAGE 5 — UNIQUE POINTS + FUTURE + CONCLUSION
    # ═══════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Unique Points & Highlights", s["h1"]))
    story.append(divider())

    unique = [
        ("Direct SAP Infotype Mapping",
         "Every data field and process maps to a real SAP infotype or transaction. "
         "IT0001 (Org Assignment), IT0002 (Personal Data), IT0008 (Basic Pay), "
         "IT0000 (Actions), IT2001 (Absences) — the simulation is architecturally "
         "aligned with how SAP HCM stores and processes HR data."),
        ("Complete Statutory Payroll",
         "Unlike typical demo projects that use placeholder calculations, this system "
         "implements actual Indian statutory deductions: PF at 12% of basic, ESI "
         "at 0.75% for applicable employees, Professional Tax at Rs. 200, and a "
         "simplified TDS calculation based on annual income slabs."),
        ("Audit Trail (IT0000-style Actions Log)",
         "Every personnel action — hiring, promotion, transfer, and separation — is "
         "logged with the effective date and details. This mirrors the IT0000 (Actions) "
         "infotype that SAP uses to maintain a chronological history of all HR actions."),
        ("Full Lifecycle in One Application",
         "Most SAP tutorials cover individual transactions in isolation. This project "
         "demonstrates the complete H2R arc — from Day 1 hiring to final separation — "
         "within a single integrated application, showing how each step flows into the next."),
        ("Production-Quality UI",
         "The frontend uses a custom SAP Fiori-inspired design system with a persistent "
         "sidebar, KPI dashboard cards, an animated lifecycle flow diagram, and a "
         "professional payslip renderer — demonstrating frontend engineering alongside "
         "the SAP domain knowledge."),
    ]
    for i, (title, desc) in enumerate(unique):
        row_color = colors.HexColor("#f0f4ff") if i % 2 == 0 else colors.white
        block = Table(
            [[Paragraph(f"<b>{title}</b>", ParagraphStyle(
                  "uh", fontName="Helvetica-Bold", fontSize=11,
                  textColor=colors.HexColor("#0070f2"))),
              Paragraph(desc, ParagraphStyle(
                  "ub", fontName="Helvetica", fontSize=11,
                  alignment=TA_JUSTIFY, leading=16))]],
            colWidths=[4.5*cm, 10.3*cm]
        )
        block.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), row_color),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e8")),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(block)
        story.append(Spacer(1, 0.15*cm))

    story.append(Paragraph("7. Future Improvements", s["h1"]))
    story.append(divider())

    future = [
        "Integration with a relational database (PostgreSQL) to replace the JSON flat-file store, enabling better query performance and concurrent access.",
        "Role-based access control (RBAC) — differentiating HR Admin, Manager, and Employee self-service roles, mirroring SAP's authorisation concept.",
        "PDF payslip generation: allow employees to download their monthly payslip as a formatted PDF using ReportLab.",
        "SAP BAPI/RFC simulation: add mock RFC call stubs so the application can demonstrate how external systems would interface with SAP HR via standard APIs.",
        "Leave balance tracking with carry-forward rules and leave encashment calculation at the time of separation.",
        "REST API expansion for integration with attendance systems, biometric devices, and third-party payroll processors.",
    ]
    for item in future:
        story.append(Paragraph(f"• {item}", s["bullet"]))

    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("8. Conclusion", s["h1"]))
    story.append(divider())
    story.append(Paragraph(
        "The H2R Employee Lifecycle Portal successfully demonstrates the end-to-end "
        "SAP HR employee lifecycle through a fully functional web application. By mapping "
        "each feature to a real SAP transaction or infotype, the project bridges the gap "
        "between SAP theory and hands-on implementation experience.",
        s["body"]
    ))
    story.append(Paragraph(
        "The combination of a clean MVC architecture, accurate Indian statutory payroll "
        "calculations, a complete actions audit trail, and a professional SAP Fiori-inspired "
        "interface demonstrates both technical depth and domain expertise in SAP Human "
        "Capital Management — fulfilling the objectives of the KIIT Capstone Project 2026.",
        s["body"]
    ))

    # Build
    doc.build(story, onFirstPage=cb, onLaterPages=cb)
    print(f"PDF created: {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
