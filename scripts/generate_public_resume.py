from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Adam_Hemmouda_Resume_Public.pdf"
FONT_DIR = ROOT / "assets" / "fonts"

FONT_REGULAR = "LiberationSans"
FONT_BOLD = "LiberationSans-Bold"
FONT_ITALIC = "LiberationSans-Italic"
FONT_BOLD_ITALIC = "LiberationSans-BoldItalic"

NAVY = colors.HexColor("#202023")
BLUE = colors.HexColor("#4B4B4E")
AMBER = colors.HexColor("#E2AF1D")
INK = colors.HexColor("#29292C")
MUTED = colors.HexColor("#66666A")
LINE = colors.HexColor("#D7DEE8")


def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, FONT_DIR / "LiberationSans-Regular.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, FONT_DIR / "LiberationSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_ITALIC, FONT_DIR / "LiberationSans-Italic.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD_ITALIC, FONT_DIR / "LiberationSans-BoldItalic.ttf"))
    pdfmetrics.registerFontFamily(
        FONT_REGULAR,
        normal=FONT_REGULAR,
        bold=FONT_BOLD,
        italic=FONT_ITALIC,
        boldItalic=FONT_BOLD_ITALIC,
    )


def paragraph(text, style):
    return Paragraph(text, style)


def bullet(text, styles):
    return Paragraph(f"- {text}", styles["bullet"])


def section(title, styles):
    return [
        Spacer(1, 6),
        Paragraph(title.upper(), styles["section"]),
        HRFlowable(width="100%", thickness=0.8, color=AMBER, spaceBefore=2, spaceAfter=5),
    ]


def role_block(title, organization, dates, bullets, styles):
    heading = Table(
        [[Paragraph(f"<b>{title}</b><br/><font color='#4B4B4E'>{organization}</font>", styles["role"]),
          Paragraph(dates, styles["date"]) ]],
        colWidths=[5.75 * inch, 1.25 * inch],
        hAlign="LEFT",
    )
    heading.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    content = [heading]
    content.extend(bullet(item, styles) for item in bullets)
    content.append(Spacer(1, 4))
    return KeepTogether(content)


def draw_page(canvas, doc):
    width, height = LETTER
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 8, width, 8, stroke=0, fill=1)
    canvas.setFillColor(AMBER)
    canvas.rect(0, height - 8, 1.65 * inch, 8, stroke=0, fill=1)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.42 * inch, width - doc.rightMargin, 0.42 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 7)
    canvas.drawString(doc.leftMargin, 0.26 * inch, "ADAM HEMMOUDA | PUBLIC RESUME")
    canvas.drawRightString(width - doc.rightMargin, 0.26 * inch, "adamhemmouda.com")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()
    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name", parent=base["Normal"], fontName=FONT_BOLD, fontSize=22,
            leading=24, textColor=NAVY, spaceAfter=2,
        ),
        "tagline": ParagraphStyle(
            "Tagline", parent=base["Normal"], fontName=FONT_BOLD, fontSize=9,
            leading=11, textColor=BLUE, uppercase=True, spaceAfter=3,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=8,
            leading=10, textColor=MUTED,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Normal"], fontName=FONT_BOLD, fontSize=8.5,
            leading=10, textColor=NAVY, tracking=1.1,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=8.4,
            leading=10.5, textColor=INK,
        ),
        "skill": ParagraphStyle(
            "Skill", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=7.8,
            leading=9.7, textColor=INK,
        ),
        "role": ParagraphStyle(
            "Role", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=8.7,
            leading=10.7, textColor=INK,
        ),
        "date": ParagraphStyle(
            "Date", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=7.7,
            leading=9.4, textColor=MUTED, alignment=TA_RIGHT,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName=FONT_REGULAR, fontSize=8.0,
            leading=9.8, textColor=INK, leftIndent=12, firstLineIndent=-7,
            bulletIndent=0, spaceBefore=1.2,
        ),
    }

    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=LETTER,
        leftMargin=0.58 * inch, rightMargin=0.58 * inch,
        topMargin=0.48 * inch, bottomMargin=0.52 * inch,
        title="Adam Hemmouda - Public Resume",
        author="Adam Hemmouda",
        subject="Computer engineering, embedded systems, and technical leadership",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="resume", frames=[frame], onPage=draw_page))

    story = [
        Paragraph("ADAM HEMMOUDA", styles["name"]),
        Paragraph("COMPUTER ENGINEER | EMBEDDED SYSTEMS | TECHNICAL LEADERSHIP", styles["tagline"]),
        Paragraph(
            "<link href='mailto:ah1469@rit.edu' color='#4B4B4E'>ah1469@rit.edu</link> &nbsp;|&nbsp; "
            "<link href='https://www.linkedin.com/in/ah1469/' color='#4B4B4E'>linkedin.com/in/ah1469</link> &nbsp;|&nbsp; "
            "<link href='https://adamhemmouda.com' color='#4B4B4E'>adamhemmouda.com</link>",
            styles["contact"],
        ),
    ]

    story += section("Profile", styles)
    story.append(Paragraph(
        "Computer engineering graduate and U.S. Army Signal Corps officer with hands-on experience in FPGA design, embedded systems, networked applications, electronics manufacturing, technical documentation, and cross-team leadership. Brings disciplined systems thinking to defense and aerospace engineering challenges.",
        styles["body"],
    ))

    story += section("Education", styles)
    education = Table(
        [[Paragraph("<b>Rochester Institute of Technology</b><br/>B.S. Computer Engineering Technology, <i>cum laude</i>", styles["role"]),
          Paragraph("May 2026", styles["date"]) ]],
        colWidths=[5.75 * inch, 1.25 * inch],
    )
    education.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(education)

    story += section("Core Capabilities", styles)
    skill_rows = [
        ("Embedded & Digital", "C/C++, VHDL, FPGA development, microcontrollers, RTOS, state machines, HDL simulation"),
        ("Signals & Electronics", "DSP, sampling, digital filtering, RF PCB design, signal conditioning, A/D and D/A conversion"),
        ("Software & Networking", "Python, Java, Assembly, MATLAB, TCP/IP, SQL, LAN/WAN, system integration"),
        ("Engineering Tools", "Quartus II, Multisim, STM32CubeIDE, Code Composer Studio, Eclipse, Git/GitHub"),
    ]
    skills_table = Table(
        [[Paragraph(f"<b>{label}</b>", styles["skill"]), Paragraph(value, styles["skill"])] for label, value in skill_rows],
        colWidths=[1.35 * inch, 5.65 * inch],
    )
    skills_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(skills_table)

    story += section("Selected Engineering Work", styles)
    story.append(role_block(
        "FPGA Stereo Vision Tennis Ball Tracker", "Senior Capstone", "2025-2026",
        [
            "Implemented a VHDL image-processing pipeline on a Snickerdoodle FPGA to threshold stereo images, detect centroids, calculate disparity, and reconstruct 3D position.",
            "Built a physics-based Blender test environment and used MATLAB to model stereo geometry; integrated Simulink over Wi-Fi and Python for camera, pipeline, and control logic.",
            "Presented formal preliminary and critical design reviews supported by system diagrams and engineering documentation.",
        ], styles,
    ))

    story += section("Experience", styles)
    story.append(role_block(
        "Second Lieutenant, Signal Corps Officer", "United States Army - Infantry Branch Detail", "May 2026-Present",
        [
            "Commissioned through RIT Army ROTC; as cadet Task Force OIC, led a 170+ person training operation across four ROTC programs.",
        ], styles,
    ))
    story.append(role_block(
        "Junior Manufacturing Engineer", "Simcona Electronics Corp.", "Oct 2025-Jun 2026",
        [
            "Developed a TCP/IP approval application backed by SQL, replacing manual paperwork with assigned signers, authenticated access, and email notifications.",
            "Prepared 13 wire lists and 26 equipment-label files with a four-person engineering team while resolving manufacturing and documentation discrepancies.",
            "Authored a 127-page illustrated technical manual covering configuration, assembly, and troubleshooting.",
        ], styles,
    ))
    story.append(role_block(
        "Control Panel Manufacturing & Inspection Co-op", "Simcona Electronics Corp.", "Sep 2024-May 2025",
        [
            "Built a CAD-modeled workstation prototype using 80/20 extrusion, mechanical hardware, and linear actuators.",
            "Created a Python label-printing tool using QR codes, panel-specific layouts, and XML commands to improve traceability.",
            "Manufactured and inspected four control-panel variants; established a 10-unit batch workflow and produced 50 units against a 20-unit weekly quota on one configuration.",
        ], styles,
    ))

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
