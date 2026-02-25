#!/usr/bin/env python3
"""
Generate a well-designed PDF of the Bioregional Flow Funding Playbook.
Uses reportlab for professional PDF generation with custom typography and layout.
"""

import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether, NextPageTemplate,
    Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "BIOREGIONAL-FLOW-FUNDING-PLAYBOOK.md")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "pdfs", "Bioregional-Flow-Funding-Playbook.pdf")

# GitHub base URL for PDF links
PDF_BASE_URL = (
    "https://github.com/Light-Brands/sydney/blob/main/"
    "kinship-earth/flow-funding-playbook/pdfs/"
)

# Section 14 no longer links to external PDFs -- resources are in the Appendix.
# This map is kept empty but retained for code compatibility.
SECTION14_PDF_MAP = {}

# ---------------------------------------------------------------------------
# Color palette — earthy, organic, professional
# ---------------------------------------------------------------------------

C_PRIMARY      = HexColor("#2B4A1E")   # Deep forest green
C_SECONDARY    = HexColor("#5C3D2E")   # Earth brown
C_ACCENT       = HexColor("#8B6914")   # Warm amber/gold
C_LINK         = HexColor("#1A6847")   # Teal-green link color
C_TEXT         = HexColor("#2C2C2C")   # Dark charcoal
C_TEXT_LIGHT   = HexColor("#555555")   # Medium gray
C_DIVIDER      = HexColor("#B5C9A8")   # Sage green divider
C_TABLE_HEAD   = HexColor("#2B4A1E")   # Forest green table header
C_TABLE_HEAD_T = white                  # White text on header
C_TABLE_ALT    = HexColor("#EDF4E8")   # Very light sage for alt rows
C_TABLE_BORDER = HexColor("#94AD84")   # Muted green border
C_COVER_BG     = HexColor("#F7F5F0")   # Warm cream
C_BLOCKQUOTE   = HexColor("#F0EDE6")   # Warm light background
C_BQ_BAR       = HexColor("#8B6914")   # Gold bar for blockquotes

# ---------------------------------------------------------------------------
# Register fonts
# ---------------------------------------------------------------------------

pdfmetrics.registerFont(TTFont("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-Bold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-Italic", "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibSans-BI", "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-Italic", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LibSerif-BI", "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"))

pdfmetrics.registerFontFamily(
    "LibSerif",
    normal="LibSerif", bold="LibSerif-Bold",
    italic="LibSerif-Italic", boldItalic="LibSerif-BI",
)
pdfmetrics.registerFontFamily(
    "LibSans",
    normal="LibSans", bold="LibSans-Bold",
    italic="LibSans-Italic", boldItalic="LibSans-BI",
)

# ---------------------------------------------------------------------------
# Page dimensions
# ---------------------------------------------------------------------------

PAGE_W, PAGE_H = letter
MARGIN_LEFT = 1.0 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 1.0 * inch
MARGIN_BOTTOM = 0.9 * inch
FRAME_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
FRAME_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def make_styles():
    """Create and return all paragraph styles."""
    s = {}

    s["body"] = ParagraphStyle(
        "Body", fontName="LibSerif", fontSize=10.5, leading=15.5,
        textColor=C_TEXT, alignment=TA_JUSTIFY, spaceAfter=8,
        spaceBefore=2,
    )
    s["body_center"] = ParagraphStyle(
        "BodyCenter", parent=s["body"], alignment=TA_CENTER,
    )
    s["h1"] = ParagraphStyle(
        "H1", fontName="LibSans-Bold", fontSize=26, leading=32,
        textColor=C_PRIMARY, spaceAfter=6, spaceBefore=0,
        alignment=TA_LEFT,
    )
    s["h2"] = ParagraphStyle(
        "H2", fontName="LibSans-Bold", fontSize=18, leading=24,
        textColor=C_PRIMARY, spaceAfter=10, spaceBefore=20,
        alignment=TA_LEFT,
    )
    s["h3"] = ParagraphStyle(
        "H3", fontName="LibSans-Bold", fontSize=13, leading=18,
        textColor=C_SECONDARY, spaceAfter=6, spaceBefore=14,
        alignment=TA_LEFT,
    )
    s["h4"] = ParagraphStyle(
        "H4", fontName="LibSans-Bold", fontSize=11, leading=15,
        textColor=C_SECONDARY, spaceAfter=4, spaceBefore=10,
        alignment=TA_LEFT,
    )
    s["subtitle"] = ParagraphStyle(
        "Subtitle", fontName="LibSerif-Italic", fontSize=13, leading=18,
        textColor=C_TEXT_LIGHT, alignment=TA_CENTER, spaceAfter=4,
    )
    s["bullet"] = ParagraphStyle(
        "Bullet", parent=s["body"], leftIndent=24, bulletIndent=12,
        spaceBefore=2, spaceAfter=3,
    )
    s["bullet2"] = ParagraphStyle(
        "Bullet2", parent=s["body"], leftIndent=42, bulletIndent=30,
        spaceBefore=1, spaceAfter=2, fontSize=10, leading=14.5,
    )
    s["numbered"] = ParagraphStyle(
        "Numbered", parent=s["body"], leftIndent=24, spaceBefore=2,
        spaceAfter=3,
    )
    s["blockquote"] = ParagraphStyle(
        "BlockQuote", fontName="LibSerif-Italic", fontSize=11.5,
        leading=17, textColor=C_TEXT_LIGHT, leftIndent=20,
        rightIndent=20, spaceBefore=8, spaceAfter=8,
        alignment=TA_LEFT, backColor=C_BLOCKQUOTE,
        borderPadding=(8, 10, 8, 10),
    )
    s["table_head"] = ParagraphStyle(
        "TableHead", fontName="LibSans-Bold", fontSize=9.5, leading=13,
        textColor=C_TABLE_HEAD_T, alignment=TA_LEFT,
    )
    s["table_cell"] = ParagraphStyle(
        "TableCell", fontName="LibSerif", fontSize=9.5, leading=13.5,
        textColor=C_TEXT, alignment=TA_LEFT,
    )
    s["footer"] = ParagraphStyle(
        "Footer", fontName="LibSans", fontSize=8, leading=10,
        textColor=C_TEXT_LIGHT, alignment=TA_CENTER,
    )
    s["cover_title"] = ParagraphStyle(
        "CoverTitle", fontName="LibSans-Bold", fontSize=34, leading=42,
        textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=12,
    )
    s["cover_subtitle"] = ParagraphStyle(
        "CoverSubtitle", fontName="LibSerif", fontSize=16, leading=22,
        textColor=C_TEXT, alignment=TA_CENTER, spaceAfter=6,
    )
    s["cover_meta"] = ParagraphStyle(
        "CoverMeta", fontName="LibSerif-Italic", fontSize=12, leading=16,
        textColor=C_TEXT_LIGHT, alignment=TA_CENTER, spaceAfter=4,
    )
    s["toc_entry"] = ParagraphStyle(
        "TOCEntry", fontName="LibSerif", fontSize=11, leading=20,
        textColor=C_TEXT, leftIndent=10, alignment=TA_LEFT,
    )
    s["toc_title"] = ParagraphStyle(
        "TOCTitle", fontName="LibSans-Bold", fontSize=20, leading=26,
        textColor=C_PRIMARY, alignment=TA_LEFT, spaceAfter=16,
    )
    s["note_box"] = ParagraphStyle(
        "NoteBox", fontName="LibSerif-Italic", fontSize=10.5, leading=15,
        textColor=C_TEXT_LIGHT, alignment=TA_LEFT,
        leftIndent=10, rightIndent=10,
        spaceBefore=4, spaceAfter=4,
    )

    return s

STYLES = make_styles()


# ---------------------------------------------------------------------------
# Custom Flowables
# ---------------------------------------------------------------------------

class SectionDivider(Flowable):
    """A decorative horizontal rule with earthy styling."""

    def __init__(self, width=None, color=C_DIVIDER, thickness=1.2):
        super().__init__()
        self.width = width or FRAME_W
        self.color = color
        self.thickness = thickness
        self._fixedWidth = self.width
        self._fixedHeight = 14

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = 7
        self.canv.line(0, y, self.width, y)


class AccentBar(Flowable):
    """A thick colored accent bar used above section headings."""

    def __init__(self, width=60, color=C_ACCENT, thickness=3):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
        self._fixedWidth = width
        self._fixedHeight = 10

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 5, self.width, 5)


class BlockQuoteBox(Flowable):
    """A blockquote with a left accent bar and background."""

    def __init__(self, text, style, bar_color=C_BQ_BAR, bg_color=C_BLOCKQUOTE):
        super().__init__()
        self.text = text
        self.style = style
        self.bar_color = bar_color
        self.bg_color = bg_color
        self._para = Paragraph(text, style)

    def wrap(self, availWidth, availHeight):
        self.availWidth = availWidth
        w, h = self._para.wrap(availWidth - 16, availHeight)
        self.para_h = h
        return availWidth, h + 20

    def draw(self):
        # Background
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.availWidth, self.para_h + 20, 4, fill=1, stroke=0)
        # Left bar
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, 0, 4, self.para_h + 20, fill=1, stroke=0)
        # Text
        self._para.drawOn(self.canv, 16, 10)


# ---------------------------------------------------------------------------
# Markdown → reportlab helpers
# ---------------------------------------------------------------------------

def md_inline(text, in_section14=False):
    """Convert markdown inline formatting to reportlab XML markup."""
    # Escape XML special chars first (but preserve our own tags later)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    # Links: [text](url)
    def link_repl(m):
        link_text = m.group(1)
        url = m.group(2)
        # Internal anchor links — just render as styled text (no hyperlink)
        if url.startswith("#"):
            return f'<i>{link_text}</i>'
        return f'<a href="{url}" color="{C_LINK.hexval()}">{link_text}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, text)

    # Bold+italic: ***text*** or ___text___
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic: *text*
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)

    # Note: em-dash conversion removed; source uses regular dashes/commas

    return text


def build_table(rows, col_count, in_section14=False):
    """Build a styled reportlab Table from parsed markdown table rows."""
    if not rows:
        return None

    # Determine if this is a Section 14 tools/templates table
    is_tools_table = in_section14 and col_count == 2

    # Build cell data
    table_data = []
    for i, row in enumerate(rows):
        cells = []
        for j, cell_text in enumerate(row):
            cell_text = cell_text.strip()

            if i == 0:
                style = STYLES["table_head"]
            else:
                style = STYLES["table_cell"]

            # In Section 14 tools table, add PDF links to the Tool column
            if is_tools_table and i > 0 and j == 0:
                # Extract the tool name from bold markdown
                tool_name_match = re.search(r'\*\*(.+?)\*\*', cell_text)
                if tool_name_match:
                    tool_name = tool_name_match.group(1)
                    pdf_file = SECTION14_PDF_MAP.get(tool_name)
                    if pdf_file:
                        url = PDF_BASE_URL + pdf_file
                        linked = md_inline(cell_text)
                        linked += (
                            f'<br/><font size="8" color="{C_LINK.hexval()}">'
                            f'<a href="{url}" color="{C_LINK.hexval()}">'
                            f'Download PDF</a></font>'
                        )
                        cells.append(Paragraph(linked, style))
                        continue

            cells.append(Paragraph(md_inline(cell_text), style))
        table_data.append(cells)

    if not table_data:
        return None

    # Calculate column widths
    avail = FRAME_W - 4
    if col_count == 2:
        col_widths = [avail * 0.35, avail * 0.65]
    elif col_count == 3:
        col_widths = [avail * 0.30, avail * 0.35, avail * 0.35]
    elif col_count == 4:
        col_widths = [avail * 0.22, avail * 0.26, avail * 0.26, avail * 0.26]
    else:
        col_widths = [avail / col_count] * col_count

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Style
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), C_TABLE_HEAD),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_TABLE_HEAD_T),
        ("FONTNAME", (0, 0), (-1, 0), "LibSans-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, C_TABLE_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, C_TABLE_ALT]),
    ]

    tbl.setStyle(TableStyle(style_cmds))
    return tbl


# ---------------------------------------------------------------------------
# Parse the markdown file into flowables
# ---------------------------------------------------------------------------

def parse_markdown(filepath):
    """Parse the playbook markdown and return a list of reportlab flowables."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    flowables = []
    i = 0
    current_section = 0  # track which ## section we're in
    in_section14 = False
    paragraph_buffer = []
    table_rows = []
    table_col_count = 0
    is_cover_done = False
    skip_toc = False

    def flush_paragraph():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            text = " ".join(paragraph_buffer)
            text = md_inline(text, in_section14)
            flowables.append(Paragraph(text, STYLES["body"]))
            paragraph_buffer = []

    def flush_table():
        nonlocal table_rows, table_col_count
        if table_rows:
            tbl = build_table(table_rows, table_col_count, in_section14)
            if tbl:
                flowables.append(Spacer(1, 4))
                flowables.append(tbl)
                flowables.append(Spacer(1, 8))
            table_rows = []
            table_col_count = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        # ----- Cover page (title + subtitle + date) -----
        if not is_cover_done:
            if stripped.startswith("# "):
                title = stripped[2:].strip()
                # Build cover page
                flowables.append(Spacer(1, 1.8 * inch))

                # Decorative top bar
                flowables.append(SectionDivider(width=FRAME_W, color=C_PRIMARY, thickness=3))
                flowables.append(Spacer(1, 30))

                flowables.append(Paragraph(title, STYLES["cover_title"]))
                flowables.append(Spacer(1, 12))

                # Read subtitle and date from next lines
                i += 1
                while i < len(lines):
                    nxt = lines[i].strip()
                    if nxt.startswith("**") and nxt.endswith("**"):
                        sub = nxt.strip("*").strip()
                        flowables.append(
                            Paragraph(sub, STYLES["cover_subtitle"])
                        )
                        flowables.append(Spacer(1, 8))
                    elif nxt.startswith("*") and nxt.endswith("*"):
                        meta = nxt.strip("*").strip()
                        flowables.append(
                            Paragraph(meta, STYLES["cover_meta"])
                        )
                        flowables.append(Spacer(1, 8))
                    elif nxt == "---":
                        break
                    i += 1

                flowables.append(Spacer(1, 30))
                flowables.append(SectionDivider(width=FRAME_W, color=C_PRIMARY, thickness=3))

                # Contact info at bottom of cover
                flowables.append(Spacer(1, 1.5 * inch))
                flowables.append(Paragraph(
                    '<font name="LibSans" size="10" color="{}">'
                    'kinshipearth.org &nbsp;|&nbsp; flowfunding.org'
                    '</font>'.format(C_TEXT_LIGHT.hexval()),
                    STYLES["body_center"]
                ))

                flowables.append(PageBreak())
                is_cover_done = True
                i += 1
                continue

        # ----- "A Note Before You Begin" section -----
        if stripped == "## A Note Before You Begin":
            flush_paragraph()
            flush_table()
            flowables.append(Spacer(1, 30))
            flowables.append(AccentBar(width=50, color=C_ACCENT))
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph("A Note Before You Begin", STYLES["h2"]))
            i += 1
            # Gather paragraphs until ---
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt == "---":
                    flush_paragraph()
                    flowables.append(Spacer(1, 8))
                    i += 1
                    break
                elif nxt == "":
                    flush_paragraph()
                else:
                    paragraph_buffer.append(nxt)
                i += 1
            flowables.append(PageBreak())
            continue

        # ----- Table of Contents -----
        if stripped == "## Table of Contents":
            flush_paragraph()
            flush_table()
            flowables.append(Spacer(1, 20))
            flowables.append(AccentBar(width=50, color=C_ACCENT))
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph("Table of Contents", STYLES["toc_title"]))
            flowables.append(Spacer(1, 10))
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt == "---":
                    i += 1
                    break
                if nxt == "":
                    i += 1
                    continue
                # Parse TOC entries like "1. [About Kinship Earth](#...)"
                toc_match = re.match(r'(\d+)\.\s+\[(.+?)\]\(#.+?\)', nxt)
                if toc_match:
                    num = toc_match.group(1)
                    name = toc_match.group(2)
                    entry_text = (
                        f'<font name="LibSans-Bold" color="{C_ACCENT.hexval()}">'
                        f'{num}.</font>&nbsp;&nbsp;{name}'
                    )
                    flowables.append(Paragraph(entry_text, STYLES["toc_entry"]))
                i += 1
            flowables.append(PageBreak())
            continue

        # ----- Horizontal rules → section dividers -----
        if stripped == "---":
            flush_paragraph()
            flush_table()
            flowables.append(Spacer(1, 6))
            flowables.append(SectionDivider())
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # ----- Tables -----
        if "|" in stripped and stripped.startswith("|"):
            flush_paragraph()
            # Check if separator row
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(re.match(r'^[-:]+$', c) for c in cells):
                # Separator row — skip
                i += 1
                continue
            if not table_rows:
                table_col_count = len(cells)
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # ----- Headings -----
        h2_match = re.match(r'^## (\d+)\.\s+(.+)$', stripped)
        if h2_match:
            flush_paragraph()
            sec_num = int(h2_match.group(1))
            sec_title = h2_match.group(2)
            current_section = sec_num
            in_section14 = (sec_num == 14)

            # Page break before each major section (except very first)
            if sec_num > 1:
                flowables.append(PageBreak())

            flowables.append(Spacer(1, 8))
            flowables.append(AccentBar(width=50, color=C_ACCENT))
            flowables.append(Spacer(1, 4))

            heading_text = (
                f'<font color="{C_ACCENT.hexval()}">{sec_num}.</font>'
                f'&nbsp;&nbsp;{sec_title}'
            )
            flowables.append(Paragraph(heading_text, STYLES["h2"]))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # Generic ## heading (no number)
        if stripped.startswith("## "):
            flush_paragraph()
            title = stripped[3:].strip()
            flowables.append(Spacer(1, 8))
            flowables.append(AccentBar(width=50, color=C_ACCENT))
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph(md_inline(title), STYLES["h2"]))
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # ### sub-headings
        if stripped.startswith("### "):
            flush_paragraph()
            title = stripped[4:].strip()
            # Appendix items get a page break before each one
            if title.startswith("Appendix A-"):
                flowables.append(PageBreak())
                flowables.append(Spacer(1, 8))
                flowables.append(AccentBar(width=50, color=C_ACCENT))
                flowables.append(Spacer(1, 4))
                flowables.append(Paragraph(md_inline(title), STYLES["h2"]))
                flowables.append(Spacer(1, 4))
            else:
                flowables.append(Spacer(1, 6))
                flowables.append(Paragraph(md_inline(title), STYLES["h3"]))
            i += 1
            continue

        # #### sub-sub-headings (Phase headers etc.)
        if stripped.startswith("#### "):
            flush_paragraph()
            title = stripped[5:].strip()
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph(md_inline(title), STYLES["h4"]))
            i += 1
            continue

        # ----- Blockquotes -----
        if stripped.startswith("> "):
            flush_paragraph()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_lines.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            bq_text = " ".join(bq_lines)
            bq_text = md_inline(bq_text)
            flowables.append(Spacer(1, 6))
            flowables.append(BlockQuoteBox(bq_text, STYLES["blockquote"]))
            flowables.append(Spacer(1, 6))
            continue

        # ----- Bullet lists -----
        if stripped.startswith("- "):
            flush_paragraph()
            bullet_text = stripped[2:].strip()
            bullet_text = md_inline(bullet_text, in_section14)
            flowables.append(
                Paragraph(
                    f'<bullet>&bull;</bullet>{bullet_text}',
                    STYLES["bullet"]
                )
            )
            i += 1
            continue

        # Sub-bullets (indented with spaces)
        if re.match(r'^\s{2,}-\s', line):
            flush_paragraph()
            bullet_text = stripped.lstrip("- ").strip()
            bullet_text = md_inline(bullet_text, in_section14)
            flowables.append(
                Paragraph(
                    f'<bullet>&ndash;</bullet>{bullet_text}',
                    STYLES["bullet2"]
                )
            )
            i += 1
            continue

        # ----- Numbered lists (within body text, like "1. ...", "2. ...") -----
        num_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if num_match and current_section > 0:  # Only inside sections
            flush_paragraph()
            num = num_match.group(1)
            text = md_inline(num_match.group(2), in_section14)
            flowables.append(
                Paragraph(
                    f'<font name="LibSans-Bold" color="{C_ACCENT.hexval()}">'
                    f'{num}.</font>&nbsp;&nbsp;{text}',
                    STYLES["numbered"]
                )
            )
            i += 1
            continue

        # ----- Bold-prefixed paragraphs (like "**1. Capital is locked up...**") -----
        bold_num_match = re.match(r'^\*\*(\d+)\.\s+(.+?)\*\*\s*$', stripped)
        if bold_num_match:
            flush_paragraph()
            text = md_inline(stripped)
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph(text, STYLES["body"]))
            i += 1
            continue

        # ----- Empty lines -----
        if stripped == "":
            flush_paragraph()
            i += 1
            continue

        # ----- Regular paragraph text -----
        paragraph_buffer.append(stripped)
        i += 1

    # Final flush
    flush_paragraph()
    flush_table()

    return flowables


# ---------------------------------------------------------------------------
# Page template with header/footer
# ---------------------------------------------------------------------------

def on_page(canvas, doc):
    """Draw header and footer on each content page."""
    canvas.saveState()

    # Footer line
    canvas.setStrokeColor(C_DIVIDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_LEFT, MARGIN_BOTTOM - 15, PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 15)

    # Footer text (left side)
    canvas.setFont("LibSans", 8)
    canvas.setFillColor(C_TEXT_LIGHT)
    canvas.drawString(
        MARGIN_LEFT, MARGIN_BOTTOM - 28,
        "A Bioregional Flow Funding Playbook  |  Kinship Earth  |  March, 2026"
    )

    # Page number (centered at bottom)
    canvas.setFont("LibSans-Bold", 9)
    canvas.setFillColor(C_TEXT)
    canvas.drawCentredString(
        PAGE_W / 2, MARGIN_BOTTOM - 42,
        str(doc.page)
    )

    # Top accent line
    canvas.setStrokeColor(C_PRIMARY)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN_LEFT, PAGE_H - MARGIN_TOP + 12, PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP + 12)

    canvas.restoreState()


def on_cover_page(canvas, doc):
    """Cover page — no header/footer, just subtle border."""
    canvas.saveState()
    # Subtle border
    canvas.setStrokeColor(C_PRIMARY)
    canvas.setLineWidth(2)
    margin = 0.6 * inch
    canvas.rect(margin, margin, PAGE_W - 2 * margin, PAGE_H - 2 * margin, fill=0)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Build the PDF
# ---------------------------------------------------------------------------

def build_pdf():
    """Main function to build the playbook PDF."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="A Bioregional Flow Funding Playbook",
        author="Kinship Earth",
        subject="A Guide for Bioregional Communities Creating Their Own Flow Funds",
    )

    # Frames
    content_frame = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, FRAME_W, FRAME_H,
        id="content",
    )

    cover_frame = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, FRAME_W, FRAME_H,
        id="cover",
    )

    # Page templates
    cover_template = PageTemplate(
        id="cover", frames=[cover_frame], onPage=on_cover_page
    )
    content_template = PageTemplate(
        id="content", frames=[content_frame], onPage=on_page
    )

    doc.addPageTemplates([cover_template, content_template])

    # Parse markdown into flowables
    flowables = parse_markdown(MD_FILE)

    # Insert template switch BEFORE the first PageBreak so page 2 uses content template
    final_flowables = []
    cover_break_found = False
    for f in flowables:
        if isinstance(f, PageBreak) and not cover_break_found:
            final_flowables.append(NextPageTemplate("content"))
            cover_break_found = True
        final_flowables.append(f)

    doc.build(final_flowables)
    print(f"PDF generated: {OUTPUT_FILE}")
    print(f"Size: {os.path.getsize(OUTPUT_FILE):,} bytes")


if __name__ == "__main__":
    build_pdf()
