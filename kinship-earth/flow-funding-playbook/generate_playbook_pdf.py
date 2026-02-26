#!/usr/bin/env python3
"""
Generate a well-designed PDF of the Bioregional Flow Funding Playbook.
Uses reportlab for professional PDF generation with custom typography and layout.
"""

import re
import os
import math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black, Color
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
        "TOCEntry", fontName="LibSerif", fontSize=10, leading=16,
        textColor=C_TEXT, leftIndent=10, alignment=TA_LEFT,
        spaceAfter=2,
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
    s["section_subtitle"] = ParagraphStyle(
        "SectionSubtitle", fontName="LibSerif-Italic", fontSize=12, leading=17,
        textColor=C_TEXT_LIGHT, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=8,
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
# Section Illustration Flowable — organic nature-themed drawings
# ---------------------------------------------------------------------------

# Transparent color helpers
def _alpha(hex_color, alpha):
    """Return an RGBA Color from a HexColor and alpha value."""
    return Color(hex_color.red, hex_color.green, hex_color.blue, alpha)


class SectionIllustration(Flowable):
    """
    A nature-themed illustration drawn with ReportLab canvas primitives.
    Uses Bezier curves, organic shapes, and the earthy color palette
    for a woodcut / botanical illustration aesthetic.
    """

    ILLUST_HEIGHT = 200  # points — fits under title, under half-page

    def __init__(self, section_num, width=None):
        super().__init__()
        self.section_num = section_num
        self.width = width or FRAME_W
        self._fixedWidth = self.width
        self._fixedHeight = self.ILLUST_HEIGHT

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.ILLUST_HEIGHT

    # -- colour shortcuts ---------------------------------------------------
    @staticmethod
    def _set(c, fill=None, stroke=None, lw=None):
        if fill:
            c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
        if lw is not None:
            c.setLineWidth(lw)

    # -- primitive helpers --------------------------------------------------
    @staticmethod
    def _leaf(c, cx, cy, size, angle, fill_color, stroke_color=None):
        """Draw an organic leaf shape using Bezier curves."""
        c.saveState()
        c.translate(cx, cy)
        c.rotate(angle)
        c.setFillColor(fill_color)
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(0.5)
        else:
            c.setStrokeColor(fill_color)
            c.setLineWidth(0)

        p = c.beginPath()
        s = size
        p.moveTo(0, 0)
        p.curveTo(s * 0.3, s * 0.6, s * 0.2, s * 0.9, 0, s)
        p.curveTo(-s * 0.2, s * 0.9, -s * 0.3, s * 0.6, 0, 0)
        c.drawPath(p, fill=1, stroke=1 if stroke_color else 0)

        # Central vein
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(0.4)
            c.line(0, s * 0.1, 0, s * 0.85)

        c.restoreState()

    @staticmethod
    def _circle(c, cx, cy, r, fill_color, stroke_color=None, lw=0.5):
        """Draw a filled circle."""
        c.saveState()
        c.setFillColor(fill_color)
        if stroke_color:
            c.setStrokeColor(stroke_color)
            c.setLineWidth(lw)
            c.circle(cx, cy, r, fill=1, stroke=1)
        else:
            c.circle(cx, cy, r, fill=1, stroke=0)
        c.restoreState()

    @staticmethod
    def _flowing_line(c, points, color, lw=1.5):
        """Draw a smooth flowing line through a series of (x,y) points using Bezier curves."""
        if len(points) < 2:
            return
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        p = c.beginPath()
        p.moveTo(points[0][0], points[0][1])
        for i in range(1, len(points)):
            x0, y0 = points[i - 1]
            x1, y1 = points[i]
            cpx = (x0 + x1) / 2
            p.curveTo(cpx, y0, cpx, y1, x1, y1)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

    @staticmethod
    def _mountain(c, x, y, w, h, fill_color):
        """Draw a mountain/triangle shape with slightly curved sides."""
        c.saveState()
        c.setFillColor(fill_color)
        c.setStrokeColor(fill_color)
        c.setLineWidth(0)
        p = c.beginPath()
        p.moveTo(x, y)
        p.curveTo(x + w * 0.15, y + h * 0.5, x + w * 0.35, y + h * 0.85, x + w * 0.5, y + h)
        p.curveTo(x + w * 0.65, y + h * 0.85, x + w * 0.85, y + h * 0.5, x + w, y)
        p.lineTo(x, y)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

    @staticmethod
    def _tree(c, x, base_y, trunk_h, canopy_r, trunk_color, canopy_color):
        """Draw a simple stylised tree."""
        c.saveState()
        # Trunk
        c.setFillColor(trunk_color)
        c.setStrokeColor(trunk_color)
        tw = canopy_r * 0.3
        c.rect(x - tw / 2, base_y, tw, trunk_h, fill=1, stroke=0)
        # Canopy
        c.setFillColor(canopy_color)
        c.circle(x, base_y + trunk_h + canopy_r * 0.6, canopy_r, fill=1, stroke=0)
        c.restoreState()

    @staticmethod
    def _drop(c, cx, cy, size, fill_color):
        """Draw a water drop shape."""
        c.saveState()
        c.setFillColor(fill_color)
        p = c.beginPath()
        s = size
        p.moveTo(cx, cy + s)
        p.curveTo(cx - s * 0.5, cy + s * 0.3, cx - s * 0.5, cy - s * 0.2, cx, cy - s * 0.5)
        p.curveTo(cx + s * 0.5, cy - s * 0.2, cx + s * 0.5, cy + s * 0.3, cx, cy + s)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

    @staticmethod
    def _root_branch(c, x0, y0, length, angle, depth, color, lw=1.5):
        """Recursively draw a branching root / mycelium line."""
        if depth <= 0 or length < 3:
            return
        rad = math.radians(angle)
        x1 = x0 + length * math.cos(rad)
        y1 = y0 + length * math.sin(rad)
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        c.line(x0, y0, x1, y1)
        c.restoreState()
        # Branch
        SectionIllustration._root_branch(c, x1, y1, length * 0.68, angle - 28, depth - 1, color, lw * 0.7)
        SectionIllustration._root_branch(c, x1, y1, length * 0.62, angle + 32, depth - 1, color, lw * 0.7)

    @staticmethod
    def _seed(c, cx, cy, w, h, fill_color):
        """Draw a seed/oval shape."""
        c.saveState()
        c.setFillColor(fill_color)
        p = c.beginPath()
        p.moveTo(cx, cy - h / 2)
        p.curveTo(cx + w * 0.6, cy - h * 0.3, cx + w * 0.6, cy + h * 0.3, cx, cy + h / 2)
        p.curveTo(cx - w * 0.6, cy + h * 0.3, cx - w * 0.6, cy - h * 0.3, cx, cy - h / 2)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

    @staticmethod
    def _wave_band(c, x_start, x_end, y_center, amplitude, color, lw=1.2, phase=0):
        """Draw a sine-wave band."""
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        p = c.beginPath()
        steps = 60
        dx = (x_end - x_start) / steps
        for j in range(steps + 1):
            x = x_start + j * dx
            y = y_center + amplitude * math.sin(phase + (j / steps) * math.pi * 4)
            if j == 0:
                p.moveTo(x, y)
            else:
                p.lineTo(x, y)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

    # -- drawing ground line ------------------------------------------------
    def _ground_line(self, c, y, color):
        """Subtle ground/horizon line."""
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(0.5)
        margin = self.width * 0.08
        c.line(margin, y, self.width - margin, y)
        c.restoreState()

    # -- per-section drawing methods ----------------------------------------

    def _draw_01_interconnected_roots(self, c):
        """Section 1 — About Kinship Earth: interconnected root system."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Ground line
        ground_y = h * 0.55
        self._ground_line(c, ground_y, _alpha(C_SECONDARY, 0.3))

        # Three small trees above ground
        tree_positions = [cx - 120, cx, cx + 120]
        canopy_colors = [_alpha(C_PRIMARY, 0.7), _alpha(C_PRIMARY, 0.85), _alpha(C_PRIMARY, 0.6)]
        for i, tx in enumerate(tree_positions):
            self._tree(c, tx, ground_y, 30, 18, _alpha(C_SECONDARY, 0.7), canopy_colors[i])

        # Root system below ground — interconnected
        root_color = _alpha(C_SECONDARY, 0.55)
        for tx in tree_positions:
            self._root_branch(c, tx, ground_y, 35, -90, 4, root_color, 1.8)
            self._root_branch(c, tx, ground_y, 28, -60, 3, root_color, 1.2)
            self._root_branch(c, tx, ground_y, 28, -120, 3, root_color, 1.2)

        # Connecting horizontal root lines between trees
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.35))
        c.setLineWidth(1.0)
        root_y = ground_y - 25
        pts = [(tree_positions[0], root_y), (cx - 40, root_y - 8),
               (cx + 40, root_y - 12), (tree_positions[2], root_y)]
        self._flowing_line(c, pts, _alpha(C_SECONDARY, 0.4), 1.2)
        pts2 = [(tree_positions[0] + 15, root_y - 15), (cx, root_y - 22),
                (tree_positions[2] - 15, root_y - 15)]
        self._flowing_line(c, pts2, _alpha(C_SECONDARY, 0.3), 0.8)
        c.restoreState()

        # Small dots at root connection nodes
        for tx in tree_positions:
            self._circle(c, tx, ground_y - 2, 3, _alpha(C_SECONDARY, 0.6))

        # Scattered leaves above canopy
        for tx in tree_positions:
            self._leaf(c, tx - 8, ground_y + 55, 8, 30, _alpha(C_PRIMARY, 0.3))
            self._leaf(c, tx + 10, ground_y + 60, 6, -20, _alpha(C_PRIMARY, 0.25))

    def _draw_02_layered_landscape(self, c):
        """Section 2 — What Is Bioregionalism?: layered landscape."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Background mountain range (distant, faded)
        self._mountain(c, w * 0.05, h * 0.28, w * 0.35, h * 0.55, _alpha(C_PRIMARY, 0.15))
        self._mountain(c, w * 0.25, h * 0.28, w * 0.4, h * 0.65, _alpha(C_PRIMARY, 0.2))
        self._mountain(c, w * 0.55, h * 0.28, w * 0.35, h * 0.5, _alpha(C_PRIMARY, 0.12))

        # Mid-ground hills
        self._mountain(c, w * 0.0, h * 0.2, w * 0.45, h * 0.3, _alpha(C_PRIMARY, 0.3))
        self._mountain(c, w * 0.35, h * 0.2, w * 0.35, h * 0.25, _alpha(C_PRIMARY, 0.25))
        self._mountain(c, w * 0.6, h * 0.2, w * 0.4, h * 0.28, _alpha(C_PRIMARY, 0.28))

        # Valley floor
        c.saveState()
        c.setFillColor(_alpha(C_PRIMARY, 0.1))
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, h * 0.22)
        p.curveTo(w * 0.3, h * 0.26, w * 0.7, h * 0.18, w, h * 0.22)
        p.lineTo(w, 0)
        p.lineTo(0, 0)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Winding river through the valley
        river_pts = [(w * 0.35, h * 0.02), (w * 0.42, h * 0.1), (w * 0.38, h * 0.18),
                     (w * 0.44, h * 0.28), (w * 0.5, h * 0.4), (w * 0.52, h * 0.55)]
        self._flowing_line(c, river_pts, _alpha(HexColor("#3B7A9E"), 0.5), 2.5)
        # Second river line for width
        river_pts2 = [(x + 4, y + 1) for x, y in river_pts]
        self._flowing_line(c, river_pts2, _alpha(HexColor("#3B7A9E"), 0.3), 1.5)

        # Small trees dotted across foothills
        for pos in [(w * 0.12, h * 0.24), (w * 0.22, h * 0.27), (w * 0.7, h * 0.23),
                    (w * 0.82, h * 0.26), (w * 0.55, h * 0.22)]:
            self._tree(c, pos[0], pos[1], 10, 7, _alpha(C_SECONDARY, 0.5), _alpha(C_PRIMARY, 0.5))

    def _draw_03_organizing_groups(self, c):
        """Section 3 — Why Bioregional Organizing Groups Matter: clustered circles."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Three overlapping community clusters
        clusters = [
            (cx - 130, h * 0.5, 42, _alpha(C_PRIMARY, 0.15)),
            (cx, h * 0.45, 50, _alpha(C_PRIMARY, 0.12)),
            (cx + 130, h * 0.5, 42, _alpha(C_PRIMARY, 0.15)),
        ]
        for x, y, r, col in clusters:
            self._circle(c, x, y, r, col)

        # People-like dots within clusters
        import random
        rng = random.Random(42)  # deterministic
        for x, y, r, _ in clusters:
            for _ in range(7):
                dx = rng.uniform(-r * 0.6, r * 0.6)
                dy = rng.uniform(-r * 0.6, r * 0.6)
                self._circle(c, x + dx, y + dy, 3.5, _alpha(C_SECONDARY, 0.6))

        # Connecting lines between clusters
        c.saveState()
        c.setStrokeColor(_alpha(C_ACCENT, 0.3))
        c.setLineWidth(1.0)
        c.setDash([4, 3])
        c.line(clusters[0][0] + 42, clusters[0][1], clusters[1][0] - 50, clusters[1][1])
        c.line(clusters[1][0] + 50, clusters[1][1], clusters[2][0] - 42, clusters[2][1])
        c.restoreState()

        # Leaves around the clusters
        for x, y, r, _ in clusters:
            self._leaf(c, x - r - 8, y + r * 0.5, 12, 45, _alpha(C_PRIMARY, 0.35))
            self._leaf(c, x + r + 5, y + r * 0.3, 10, -30, _alpha(C_PRIMARY, 0.3))

        # Ground with small grass tufts
        self._ground_line(c, h * 0.15, _alpha(C_DIVIDER, 0.4))
        for gx in range(int(w * 0.1), int(w * 0.9), 30):
            self._leaf(c, gx, h * 0.15, 6, 80 + rng.uniform(-15, 15), _alpha(C_PRIMARY, 0.2))

    def _draw_04_flowing_water(self, c):
        """Section 4 — What Is Flow Funding?: flowing water/river motif."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Multiple flowing water streams
        stream_colors = [
            _alpha(HexColor("#3B7A9E"), 0.35),
            _alpha(HexColor("#3B7A9E"), 0.25),
            _alpha(HexColor("#3B7A9E"), 0.45),
            _alpha(HexColor("#3B7A9E"), 0.2),
            _alpha(HexColor("#3B7A9E"), 0.3),
        ]
        for idx, (y_off, amp, phase) in enumerate([
            (h * 0.7, 15, 0), (h * 0.55, 12, 1.2), (h * 0.4, 18, 2.5),
            (h * 0.28, 10, 0.8), (h * 0.15, 14, 3.5)
        ]):
            self._wave_band(c, w * 0.05, w * 0.95, y_off, amp,
                            stream_colors[idx], lw=2.0 - idx * 0.2, phase=phase)

        # Water drops scattered
        drop_positions = [
            (w * 0.15, h * 0.82), (w * 0.4, h * 0.85), (w * 0.65, h * 0.78),
            (w * 0.85, h * 0.83), (w * 0.3, h * 0.05), (w * 0.7, h * 0.08),
        ]
        for dx, dy in drop_positions:
            self._drop(c, dx, dy, 7, _alpha(HexColor("#3B7A9E"), 0.3))

        # Small pebbles/stones at bottom
        for sx in [w * 0.1, w * 0.25, w * 0.5, w * 0.7, w * 0.88]:
            c.saveState()
            c.setFillColor(_alpha(C_SECONDARY, 0.2))
            c.ellipse(sx - 6, h * 0.02, sx + 6, h * 0.06, fill=1, stroke=0)
            c.restoreState()

    def _draw_05_systemic_problems(self, c):
        """Section 5 — Systemic Problems: cracked/dry earth with wilting plant."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Dry cracked earth — horizontal layers with cracks
        ground_y = h * 0.3
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.12))
        c.rect(0, 0, w, ground_y, fill=1, stroke=0)
        c.restoreState()

        # Crack lines
        crack_color = _alpha(C_SECONDARY, 0.35)
        cracks = [
            [(cx - 80, ground_y), (cx - 60, ground_y - 15), (cx - 30, ground_y - 25),
             (cx - 20, ground_y - 10), (cx, ground_y - 30)],
            [(cx + 20, ground_y), (cx + 40, ground_y - 20), (cx + 70, ground_y - 12),
             (cx + 90, ground_y - 28)],
            [(cx - 40, ground_y - 8), (cx - 10, 0)],
            [(cx + 30, ground_y - 5), (cx + 50, 0)],
        ]
        for crack in cracks:
            self._flowing_line(c, crack, crack_color, 0.8)

        # Wilting plant in center
        c.saveState()
        c.setStrokeColor(_alpha(C_PRIMARY, 0.4))
        c.setLineWidth(1.5)
        # Stem — slightly bent
        p = c.beginPath()
        p.moveTo(cx, ground_y)
        p.curveTo(cx + 3, ground_y + 30, cx - 5, ground_y + 50, cx - 8, ground_y + 70)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Drooping leaves
        self._leaf(c, cx - 10, ground_y + 65, 15, 210, _alpha(C_PRIMARY, 0.3))
        self._leaf(c, cx + 2, ground_y + 55, 12, 150, _alpha(C_PRIMARY, 0.25))
        self._leaf(c, cx - 15, ground_y + 45, 10, 230, _alpha(C_PRIMARY, 0.2))

        # Faint lock symbols (barriers) on sides — simplified as rectangles with arch
        for bx in [w * 0.15, w * 0.85]:
            c.saveState()
            c.setStrokeColor(_alpha(C_SECONDARY, 0.25))
            c.setLineWidth(1.2)
            c.setFillColor(_alpha(C_SECONDARY, 0.08))
            c.rect(bx - 10, h * 0.45, 20, 18, fill=1, stroke=1)
            # Arch
            p = c.beginPath()
            p.moveTo(bx - 6, h * 0.45 + 18)
            p.curveTo(bx - 6, h * 0.45 + 30, bx + 6, h * 0.45 + 30, bx + 6, h * 0.45 + 18)
            c.drawPath(p, fill=0, stroke=1)
            c.restoreState()

    def _draw_06_flow_addresses(self, c):
        """Section 6 — How Flow Funding Addresses Problems: healthy growing garden."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Rich ground
        ground_y = h * 0.25
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.1))
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, ground_y)
        p.curveTo(w * 0.25, ground_y + 8, w * 0.75, ground_y - 5, w, ground_y)
        p.lineTo(w, 0)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Multiple growing plants of various sizes
        plants = [
            (w * 0.12, ground_y, 25, 10, 0),
            (w * 0.28, ground_y, 40, 14, 5),
            (w * 0.42, ground_y, 55, 16, -3),
            (w * 0.58, ground_y, 65, 18, 2),
            (w * 0.72, ground_y, 50, 15, -5),
            (w * 0.88, ground_y, 35, 12, 4),
        ]
        for px, py, stem_h, leaf_sz, lean in plants:
            # Stem
            c.saveState()
            c.setStrokeColor(_alpha(C_PRIMARY, 0.5))
            c.setLineWidth(1.5)
            p = c.beginPath()
            p.moveTo(px, py)
            p.curveTo(px + lean, py + stem_h * 0.5, px + lean * 0.5, py + stem_h * 0.8,
                      px + lean * 0.3, py + stem_h)
            c.drawPath(p, fill=0, stroke=1)
            c.restoreState()

            # Leaves
            top_x = px + lean * 0.3
            top_y = py + stem_h
            self._leaf(c, top_x - 3, top_y - 8, leaf_sz * 0.6, 40, _alpha(C_PRIMARY, 0.4))
            self._leaf(c, top_x + 3, top_y - 5, leaf_sz * 0.5, -35, _alpha(C_PRIMARY, 0.35))
            self._leaf(c, top_x, top_y, leaf_sz * 0.7, 10, _alpha(C_PRIMARY, 0.5))

        # Sun/warmth in upper right
        sun_x, sun_y = w * 0.85, h * 0.8
        self._circle(c, sun_x, sun_y, 15, _alpha(C_ACCENT, 0.25))
        self._circle(c, sun_x, sun_y, 10, _alpha(C_ACCENT, 0.35))
        # Rays
        c.saveState()
        c.setStrokeColor(_alpha(C_ACCENT, 0.2))
        c.setLineWidth(0.8)
        for angle_deg in range(0, 360, 30):
            rad = math.radians(angle_deg)
            c.line(sun_x + 18 * math.cos(rad), sun_y + 18 * math.sin(rad),
                   sun_x + 28 * math.cos(rad), sun_y + 28 * math.sin(rad))
        c.restoreState()

    def _draw_07_four_step_cycle(self, c):
        """Section 7 — The Four-Step Cycle: circular seed-to-tree lifecycle."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx, cy = w / 2, h * 0.48
        radius = min(w, h) * 0.32

        # Circular path (dashed)
        c.saveState()
        c.setStrokeColor(_alpha(C_DIVIDER, 0.5))
        c.setLineWidth(1.5)
        c.setDash([6, 4])
        c.circle(cx, cy, radius, fill=0, stroke=1)
        c.restoreState()

        # Four stages at compass points
        # Top: Seed (Identify)
        seed_x, seed_y = cx, cy + radius
        self._seed(c, seed_x, seed_y, 12, 16, _alpha(C_SECONDARY, 0.6))
        # Small label dot
        self._circle(c, seed_x, seed_y + 18, 2, _alpha(C_ACCENT, 0.6))

        # Right: Sprout (Deploy)
        sprout_x, sprout_y = cx + radius, cy
        c.saveState()
        c.setStrokeColor(_alpha(C_PRIMARY, 0.5))
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(sprout_x, sprout_y - 10)
        p.curveTo(sprout_x + 2, sprout_y, sprout_x - 2, sprout_y + 8, sprout_x, sprout_y + 15)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()
        self._leaf(c, sprout_x - 4, sprout_y + 8, 8, 30, _alpha(C_PRIMARY, 0.45))
        self._leaf(c, sprout_x + 4, sprout_y + 5, 7, -25, _alpha(C_PRIMARY, 0.4))

        # Bottom: Young tree (Report)
        tree_x, tree_y = cx, cy - radius
        self._tree(c, tree_x, tree_y - 12, 16, 10, _alpha(C_SECONDARY, 0.5), _alpha(C_PRIMARY, 0.5))

        # Left: Full tree dropping seeds (Recommend)
        tree2_x, tree2_y = cx - radius, cy
        self._tree(c, tree2_x, tree2_y - 8, 20, 14, _alpha(C_SECONDARY, 0.6), _alpha(C_PRIMARY, 0.6))
        # Falling seeds
        self._seed(c, tree2_x - 12, tree2_y + 22, 5, 7, _alpha(C_SECONDARY, 0.35))
        self._seed(c, tree2_x + 10, tree2_y + 18, 4, 6, _alpha(C_SECONDARY, 0.3))

        # Curved arrows between stages
        arrow_color = _alpha(C_ACCENT, 0.4)
        c.saveState()
        c.setStrokeColor(arrow_color)
        c.setLineWidth(1.2)
        # Draw small arrow chevrons at midpoints
        for angle_start in [45, 135, 225, 315]:
            rad = math.radians(angle_start)
            ax = cx + (radius * 0.75) * math.cos(rad)
            ay = cy + (radius * 0.75) * math.sin(rad)
            # Small chevron
            perp = angle_start + 90
            pr = math.radians(perp)
            c.line(ax - 4 * math.cos(pr), ay - 4 * math.sin(pr),
                   ax + 5 * math.cos(rad), ay + 5 * math.sin(rad))
            c.line(ax + 4 * math.cos(pr), ay + 4 * math.sin(pr),
                   ax + 5 * math.cos(rad), ay + 5 * math.sin(rad))
        c.restoreState()

    def _draw_08_creating_fund(self, c):
        """Section 8 — Creating Your Own Fund: sprouting seedling in cupped hands."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Cupped hands shape (two curved lines)
        hand_y = h * 0.3
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.12))
        c.setStrokeColor(_alpha(C_SECONDARY, 0.35))
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(cx - 80, hand_y + 30)
        p.curveTo(cx - 60, hand_y - 10, cx - 20, hand_y - 20, cx, hand_y - 15)
        p.curveTo(cx + 20, hand_y - 20, cx + 60, hand_y - 10, cx + 80, hand_y + 30)
        p.curveTo(cx + 50, hand_y + 10, cx - 50, hand_y + 10, cx - 80, hand_y + 30)
        c.drawPath(p, fill=1, stroke=1)
        c.restoreState()

        # Soil in hands
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.2))
        p = c.beginPath()
        p.moveTo(cx - 40, hand_y)
        p.curveTo(cx - 20, hand_y - 8, cx + 20, hand_y - 8, cx + 40, hand_y)
        p.curveTo(cx + 20, hand_y + 5, cx - 20, hand_y + 5, cx - 40, hand_y)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Seedling growing from soil
        c.saveState()
        c.setStrokeColor(_alpha(C_PRIMARY, 0.6))
        c.setLineWidth(2)
        p = c.beginPath()
        p.moveTo(cx, hand_y)
        p.curveTo(cx + 2, hand_y + 25, cx - 2, hand_y + 45, cx, hand_y + 65)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Two unfurling leaves at top
        self._leaf(c, cx - 5, hand_y + 55, 18, 40, _alpha(C_PRIMARY, 0.5), _alpha(C_PRIMARY, 0.7))
        self._leaf(c, cx + 5, hand_y + 50, 16, -35, _alpha(C_PRIMARY, 0.45), _alpha(C_PRIMARY, 0.65))

        # Tiny emerging leaf at very top
        self._leaf(c, cx, hand_y + 65, 10, 5, _alpha(C_PRIMARY, 0.55))

        # Small roots below
        self._root_branch(c, cx, hand_y - 5, 18, -90, 3, _alpha(C_SECONDARY, 0.3), 0.8)

        # Subtle glow / energy around seedling
        self._circle(c, cx, hand_y + 45, 35, _alpha(C_ACCENT, 0.06))
        self._circle(c, cx, hand_y + 45, 50, _alpha(C_ACCENT, 0.03))

    def _draw_09_legal(self, c):
        """Section 9 — Legal Considerations: structured tree with clear trunk layers."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Stylised tree trunk — three stacked segments (entity types)
        base_y = h * 0.15
        seg_h = 30
        seg_w = 20
        colors = [_alpha(C_SECONDARY, 0.4), _alpha(C_SECONDARY, 0.3), _alpha(C_SECONDARY, 0.5)]

        for i, col in enumerate(colors):
            y = base_y + i * seg_h
            c.saveState()
            c.setFillColor(col)
            c.setStrokeColor(_alpha(C_SECONDARY, 0.2))
            c.setLineWidth(0.5)
            c.rect(cx - seg_w / 2, y, seg_w, seg_h, fill=1, stroke=1)
            c.restoreState()

        # Branches splitting from top of trunk
        trunk_top = base_y + 3 * seg_h
        branch_color = _alpha(C_PRIMARY, 0.4)
        for angle, length in [(-50, 50), (-20, 60), (20, 60), (50, 50)]:
            rad = math.radians(90 + angle)
            ex = cx + length * math.cos(rad)
            ey = trunk_top + length * math.sin(rad)
            c.saveState()
            c.setStrokeColor(branch_color)
            c.setLineWidth(1.5)
            p = c.beginPath()
            p.moveTo(cx, trunk_top)
            cpx = (cx + ex) / 2 + angle * 0.3
            cpy = (trunk_top + ey) / 2 + 10
            p.curveTo(cpx, cpy, cpx, cpy, ex, ey)
            c.drawPath(p, fill=0, stroke=1)
            c.restoreState()
            # Leaf clusters at branch ends
            self._leaf(c, ex, ey, 10, 15 + angle, _alpha(C_PRIMARY, 0.4))
            self._leaf(c, ex + 5, ey - 4, 8, -10 + angle, _alpha(C_PRIMARY, 0.3))

        # Roots (foundations)
        self._root_branch(c, cx, base_y, 25, -90, 3, _alpha(C_SECONDARY, 0.3), 1.2)
        self._root_branch(c, cx, base_y, 20, -60, 2, _alpha(C_SECONDARY, 0.25), 1.0)
        self._root_branch(c, cx, base_y, 20, -120, 2, _alpha(C_SECONDARY, 0.25), 1.0)

        # Horizontal lines through trunk segments (like document lines)
        for i in range(3):
            y = base_y + i * seg_h + seg_h / 2
            c.saveState()
            c.setStrokeColor(_alpha(C_ACCENT, 0.3))
            c.setLineWidth(0.5)
            c.line(cx - seg_w / 2 + 3, y, cx + seg_w / 2 - 3, y)
            c.restoreState()

    def _draw_10_governance(self, c):
        """Section 10 — Governance: mycelium network."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Network of nodes and connections (mycelium)
        import random
        rng = random.Random(100)

        # Generate node positions
        nodes = []
        for _ in range(18):
            x = rng.uniform(w * 0.08, w * 0.92)
            y = rng.uniform(h * 0.1, h * 0.9)
            nodes.append((x, y))

        # Draw connections (edges) — connect nearby nodes
        c.saveState()
        for i, (x1, y1) in enumerate(nodes):
            for j, (x2, y2) in enumerate(nodes):
                if i >= j:
                    continue
                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < w * 0.28:
                    alpha = max(0.08, 0.3 - dist / (w * 0.5))
                    c.setStrokeColor(_alpha(C_PRIMARY, alpha))
                    c.setLineWidth(0.8)
                    # Curved connection
                    cpx = (x1 + x2) / 2 + rng.uniform(-15, 15)
                    cpy = (y1 + y2) / 2 + rng.uniform(-15, 15)
                    p = c.beginPath()
                    p.moveTo(x1, y1)
                    p.curveTo(cpx, cpy, cpx, cpy, x2, y2)
                    c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Draw nodes as small circles with varying sizes
        for x, y in nodes:
            r = rng.uniform(3, 6)
            self._circle(c, x, y, r, _alpha(C_PRIMARY, 0.35))
            # Inner dot
            self._circle(c, x, y, r * 0.4, _alpha(C_ACCENT, 0.4))

        # A few mushroom fruiting bodies
        for mx, my in [(w * 0.2, h * 0.3), (w * 0.7, h * 0.6), (w * 0.5, h * 0.15)]:
            # Stem
            c.saveState()
            c.setFillColor(_alpha(C_SECONDARY, 0.3))
            c.rect(mx - 2, my, 4, 12, fill=1, stroke=0)
            c.restoreState()
            # Cap
            c.saveState()
            c.setFillColor(_alpha(C_SECONDARY, 0.4))
            p = c.beginPath()
            p.moveTo(mx - 10, my + 12)
            p.curveTo(mx - 8, my + 22, mx + 8, my + 22, mx + 10, my + 12)
            p.lineTo(mx - 10, my + 12)
            c.drawPath(p, fill=1, stroke=0)
            c.restoreState()

    def _draw_11_attracting_capital(self, c):
        """Section 11 — Attracting Capital: watershed with tributaries converging."""
        w, h = self.width, self.ILLUST_HEIGHT

        water_color = HexColor("#3B7A9E")

        # Multiple tributaries flowing into central river
        tributaries = [
            [(w * 0.05, h * 0.9), (w * 0.15, h * 0.7), (w * 0.25, h * 0.5), (w * 0.4, h * 0.35)],
            [(w * 0.95, h * 0.85), (w * 0.8, h * 0.65), (w * 0.65, h * 0.45), (w * 0.55, h * 0.35)],
            [(w * 0.3, h * 0.95), (w * 0.35, h * 0.75), (w * 0.42, h * 0.5), (w * 0.47, h * 0.35)],
            [(w * 0.7, h * 0.95), (w * 0.65, h * 0.7), (w * 0.58, h * 0.5), (w * 0.52, h * 0.35)],
        ]

        for i, pts in enumerate(tributaries):
            alpha = 0.25 + i * 0.05
            lw = 1.2 + i * 0.3
            self._flowing_line(c, pts, _alpha(water_color, alpha), lw)

        # Main river flowing down from convergence
        main_river = [(w * 0.48, h * 0.35), (w * 0.5, h * 0.2), (w * 0.48, h * 0.1), (w * 0.5, h * 0.0)]
        self._flowing_line(c, main_river, _alpha(water_color, 0.5), 3.5)
        # Parallel line for river width
        main_river2 = [(x + 5, y + 1) for x, y in main_river]
        self._flowing_line(c, main_river2, _alpha(water_color, 0.3), 2.0)

        # Convergence point emphasis
        self._circle(c, w * 0.5, h * 0.35, 8, _alpha(water_color, 0.15))
        self._circle(c, w * 0.5, h * 0.35, 4, _alpha(water_color, 0.25))

        # Banks / terrain lines
        for offset in [-35, 35]:
            bank_pts = [(w * 0.48 + offset, h * 0.35),
                        (w * 0.5 + offset * 0.8, h * 0.2),
                        (w * 0.48 + offset * 0.6, h * 0.1)]
            self._flowing_line(c, bank_pts, _alpha(C_PRIMARY, 0.15), 0.8)

        # Small vegetation along banks
        for vx, vy in [(w * 0.35, h * 0.4), (w * 0.62, h * 0.42), (w * 0.42, h * 0.15),
                        (w * 0.58, h * 0.13)]:
            self._leaf(c, vx, vy, 8, 70, _alpha(C_PRIMARY, 0.3))
            self._leaf(c, vx + 6, vy - 2, 6, 110, _alpha(C_PRIMARY, 0.25))

    def _draw_12_storytelling(self, c):
        """Section 12 — Storytelling: tree rings / growth rings."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx, cy = w / 2, h * 0.48

        # Concentric rings (tree cross-section)
        max_r = min(w, h) * 0.38
        ring_count = 10
        for i in range(ring_count, 0, -1):
            r = max_r * (i / ring_count)
            alpha = 0.08 + (ring_count - i) * 0.025
            c.saveState()
            c.setStrokeColor(_alpha(C_SECONDARY, alpha + 0.1))
            c.setLineWidth(1.0)
            c.setFillColor(_alpha(C_SECONDARY, alpha))
            # Slightly irregular rings using an ellipse with wobble
            wobble_x = 2 * math.sin(i * 1.3)
            wobble_y = 2 * math.cos(i * 0.9)
            c.ellipse(cx - r + wobble_x, cy - r * 0.9 + wobble_y,
                      cx + r + wobble_x, cy + r * 0.9 + wobble_y, fill=1, stroke=1)
            c.restoreState()

        # Center heartwood
        self._circle(c, cx, cy, 8, _alpha(C_SECONDARY, 0.45))

        # Radial lines (like grain / cracks)
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.15))
        c.setLineWidth(0.4)
        for angle_deg in range(0, 360, 45):
            rad = math.radians(angle_deg)
            c.line(cx + 12 * math.cos(rad), cy + 12 * math.sin(rad),
                   cx + max_r * 0.85 * math.cos(rad), cy + max_r * 0.78 * math.sin(rad))
        c.restoreState()

        # Small bark-like texture at outer edge
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.2))
        c.setLineWidth(0.6)
        for angle_deg in range(0, 360, 12):
            rad = math.radians(angle_deg)
            r_inner = max_r * 0.9
            r_outer = max_r * 1.02
            c.line(cx + r_inner * math.cos(rad), cy + r_inner * 0.88 * math.sin(rad),
                   cx + r_outer * math.cos(rad), cy + r_outer * 0.88 * math.sin(rad))
        c.restoreState()

    def _draw_13_activation_series(self, c):
        """Section 13 — Bioregional Activation: landscape with rising sun and paths."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Rising sun at top center
        sun_x, sun_y = w / 2, h * 0.78
        self._circle(c, sun_x, sun_y, 30, _alpha(C_ACCENT, 0.15))
        self._circle(c, sun_x, sun_y, 22, _alpha(C_ACCENT, 0.2))
        self._circle(c, sun_x, sun_y, 14, _alpha(C_ACCENT, 0.3))

        # Sun rays
        c.saveState()
        c.setStrokeColor(_alpha(C_ACCENT, 0.15))
        c.setLineWidth(0.8)
        for angle_deg in range(0, 180, 15):
            rad = math.radians(angle_deg)
            c.line(sun_x + 34 * math.cos(rad), sun_y + 34 * math.sin(rad),
                   sun_x + 50 * math.cos(rad), sun_y + 50 * math.sin(rad))
        c.restoreState()

        # Horizon / rolling hills
        hill_y = h * 0.35
        c.saveState()
        c.setFillColor(_alpha(C_PRIMARY, 0.15))
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, hill_y)
        p.curveTo(w * 0.15, hill_y + 20, w * 0.3, hill_y + 10, w * 0.45, hill_y + 15)
        p.curveTo(w * 0.6, hill_y + 20, w * 0.8, hill_y + 5, w, hill_y + 12)
        p.lineTo(w, 0)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Winding path from foreground to horizon
        path_pts = [(w * 0.5, h * 0.02), (w * 0.48, h * 0.12), (w * 0.52, h * 0.22),
                    (w * 0.5, hill_y)]
        self._flowing_line(c, path_pts, _alpha(C_SECONDARY, 0.3), 2.0)
        # Second line for path width
        path_pts2 = [(x + 8, y) for x, y in path_pts]
        self._flowing_line(c, path_pts2, _alpha(C_SECONDARY, 0.2), 1.2)

        # Small figures / markers along path
        for px, py in [(w * 0.49, h * 0.08), (w * 0.51, h * 0.18), (w * 0.5, h * 0.28)]:
            self._circle(c, px, py, 3, _alpha(C_SECONDARY, 0.4))

        # Trees on either side of path
        for tx, ty in [(w * 0.2, hill_y), (w * 0.35, hill_y + 5), (w * 0.65, hill_y + 3),
                        (w * 0.8, hill_y - 2)]:
            self._tree(c, tx, ty, 12, 8, _alpha(C_SECONDARY, 0.4), _alpha(C_PRIMARY, 0.4))

    def _draw_14_tools_templates(self, c):
        """Section 14 — Tools and Templates: toolkit / workbench with botanical elements."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Horizontal workbench surface
        bench_y = h * 0.3
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.12))
        c.setStrokeColor(_alpha(C_SECONDARY, 0.25))
        c.setLineWidth(1)
        c.rect(w * 0.1, bench_y - 5, w * 0.8, 10, fill=1, stroke=1)
        c.restoreState()

        # Various "tools" on the bench — stylised as natural forms
        # Pencil / stick
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.5))
        c.setLineWidth(2)
        c.line(w * 0.2, bench_y + 5, w * 0.2, bench_y + 50)
        c.restoreState()
        self._leaf(c, w * 0.2, bench_y + 45, 8, 10, _alpha(C_PRIMARY, 0.4))

        # Seed packets
        for sx, offset in [(w * 0.35, 0), (w * 0.4, 3)]:
            c.saveState()
            c.setFillColor(_alpha(C_ACCENT, 0.15 + offset * 0.02))
            c.setStrokeColor(_alpha(C_ACCENT, 0.3))
            c.setLineWidth(0.8)
            c.rect(sx - 8, bench_y + 5, 16, 22, fill=1, stroke=1)
            c.restoreState()
            self._seed(c, sx, bench_y + 20, 6, 8, _alpha(C_SECONDARY, 0.35))

        # Compass/circle tool
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.4))
        c.setLineWidth(1)
        c.circle(w * 0.55, bench_y + 30, 15, fill=0, stroke=1)
        c.setDash([3, 2])
        c.line(w * 0.55, bench_y + 30, w * 0.55 + 12, bench_y + 38)
        c.restoreState()
        self._circle(c, w * 0.55, bench_y + 30, 2, _alpha(C_SECONDARY, 0.5))

        # Scroll/paper
        c.saveState()
        c.setFillColor(_alpha(C_BLOCKQUOTE, 0.8))
        c.setStrokeColor(_alpha(C_SECONDARY, 0.3))
        c.setLineWidth(0.8)
        c.rect(w * 0.68, bench_y + 5, 25, 40, fill=1, stroke=1)
        # Lines on paper
        c.setStrokeColor(_alpha(C_SECONDARY, 0.15))
        for ly in range(int(bench_y + 12), int(bench_y + 42), 6):
            c.line(w * 0.7, ly, w * 0.68 + 22, ly)
        c.restoreState()

        # Watering can
        wc_x = w * 0.82
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.2))
        c.setStrokeColor(_alpha(C_SECONDARY, 0.35))
        c.setLineWidth(0.8)
        c.roundRect(wc_x - 8, bench_y + 5, 16, 20, 3, fill=1, stroke=1)
        # Spout
        p = c.beginPath()
        p.moveTo(wc_x + 8, bench_y + 20)
        p.lineTo(wc_x + 22, bench_y + 30)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()
        # Water drops from spout
        self._drop(c, wc_x + 20, bench_y + 35, 4, _alpha(HexColor("#3B7A9E"), 0.3))
        self._drop(c, wc_x + 24, bench_y + 32, 3, _alpha(HexColor("#3B7A9E"), 0.2))

        # Botanical vines around edges
        vine_color = _alpha(C_PRIMARY, 0.2)
        vine_pts = [(w * 0.05, h * 0.1), (w * 0.08, h * 0.3), (w * 0.06, h * 0.5),
                    (w * 0.09, h * 0.7), (w * 0.06, h * 0.9)]
        self._flowing_line(c, vine_pts, vine_color, 1.0)
        for _, vy in vine_pts[1:]:
            self._leaf(c, w * 0.08, vy, 6, -30, _alpha(C_PRIMARY, 0.2))

    def _draw_15_kinship_support(self, c):
        """Section 15 — How Kinship Earth Can Support You: sheltering tree with open branches."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Large central tree
        base_y = h * 0.12
        trunk_h = h * 0.35

        # Trunk
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.45))
        tw = 18
        p = c.beginPath()
        p.moveTo(cx - tw, base_y)
        p.curveTo(cx - tw - 3, base_y + trunk_h * 0.5, cx - tw + 2, base_y + trunk_h * 0.8,
                  cx - tw * 0.6, base_y + trunk_h)
        p.lineTo(cx + tw * 0.6, base_y + trunk_h)
        p.curveTo(cx + tw + 2, base_y + trunk_h * 0.8, cx + tw + 3, base_y + trunk_h * 0.5,
                  cx + tw, base_y)
        p.lineTo(cx - tw, base_y)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Wide canopy — large organic shape
        canopy_y = base_y + trunk_h
        c.saveState()
        c.setFillColor(_alpha(C_PRIMARY, 0.25))
        p = c.beginPath()
        p.moveTo(cx - 120, canopy_y + 10)
        p.curveTo(cx - 100, canopy_y + 60, cx - 40, canopy_y + 80, cx, canopy_y + 75)
        p.curveTo(cx + 40, canopy_y + 80, cx + 100, canopy_y + 60, cx + 120, canopy_y + 10)
        p.curveTo(cx + 80, canopy_y + 30, cx - 80, canopy_y + 30, cx - 120, canopy_y + 10)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Second canopy layer (darker)
        c.saveState()
        c.setFillColor(_alpha(C_PRIMARY, 0.2))
        p = c.beginPath()
        p.moveTo(cx - 90, canopy_y + 20)
        p.curveTo(cx - 60, canopy_y + 55, cx - 20, canopy_y + 65, cx, canopy_y + 60)
        p.curveTo(cx + 20, canopy_y + 65, cx + 60, canopy_y + 55, cx + 90, canopy_y + 20)
        p.curveTo(cx + 50, canopy_y + 35, cx - 50, canopy_y + 35, cx - 90, canopy_y + 20)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Small figures sheltering under tree
        for fx, fy in [(cx - 50, base_y + 5), (cx - 20, base_y + 3), (cx + 15, base_y + 4),
                        (cx + 45, base_y + 6)]:
            self._circle(c, fx, fy, 4, _alpha(C_SECONDARY, 0.35))
            # Body line
            c.saveState()
            c.setStrokeColor(_alpha(C_SECONDARY, 0.3))
            c.setLineWidth(1)
            c.line(fx, fy + 4, fx, fy + 12)
            c.restoreState()

        # Roots spreading wide
        self._root_branch(c, cx - 10, base_y, 30, -100, 3, _alpha(C_SECONDARY, 0.25), 1.2)
        self._root_branch(c, cx + 10, base_y, 30, -80, 3, _alpha(C_SECONDARY, 0.25), 1.2)

    def _draw_16_coming_next(self, c):
        """Section 16 — What Is Coming Next: horizon with seeds in flight."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Horizon line
        horizon_y = h * 0.35
        self._ground_line(c, horizon_y, _alpha(C_DIVIDER, 0.4))

        # Gentle hills
        c.saveState()
        c.setFillColor(_alpha(C_PRIMARY, 0.08))
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, horizon_y)
        p.curveTo(w * 0.2, horizon_y + 12, w * 0.4, horizon_y + 5, w * 0.6, horizon_y + 15)
        p.curveTo(w * 0.8, horizon_y + 8, w * 0.9, horizon_y + 3, w, horizon_y + 10)
        p.lineTo(w, 0)
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

        # Dandelion seeds floating in the sky
        seed_positions = [
            (w * 0.2, h * 0.55), (w * 0.35, h * 0.7), (w * 0.5, h * 0.65),
            (w * 0.65, h * 0.75), (w * 0.8, h * 0.6), (w * 0.45, h * 0.85),
            (w * 0.72, h * 0.82),
        ]
        for sx, sy in seed_positions:
            # Seed body
            self._seed(c, sx, sy, 3, 5, _alpha(C_SECONDARY, 0.35))
            # Wispy filaments
            c.saveState()
            c.setStrokeColor(_alpha(C_SECONDARY, 0.2))
            c.setLineWidth(0.4)
            for a in range(-40, 50, 20):
                rad = math.radians(90 + a)
                ex = sx + 8 * math.cos(rad)
                ey = sy + 8 * math.sin(rad)
                c.line(sx, sy + 2, ex, ey)
            c.restoreState()

        # Parent dandelion plant at left
        plant_x = w * 0.1
        c.saveState()
        c.setStrokeColor(_alpha(C_PRIMARY, 0.4))
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(plant_x, horizon_y)
        p.curveTo(plant_x + 2, horizon_y + 20, plant_x - 2, horizon_y + 35, plant_x, horizon_y + 50)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Dandelion puff (partially dispersed)
        self._circle(c, plant_x, horizon_y + 55, 10, _alpha(C_SECONDARY, 0.15))
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.25))
        c.setLineWidth(0.3)
        for a in range(0, 360, 25):
            rad = math.radians(a)
            c.line(plant_x + 3 * math.cos(rad), horizon_y + 55 + 3 * math.sin(rad),
                   plant_x + 10 * math.cos(rad), horizon_y + 55 + 10 * math.sin(rad))
        c.restoreState()

    def _draw_17_faq(self, c):
        """Section 17 — FAQ: branching question-mark tree."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Central trunk
        base_y = h * 0.1
        c.saveState()
        c.setStrokeColor(_alpha(C_SECONDARY, 0.5))
        c.setLineWidth(3)
        p = c.beginPath()
        p.moveTo(cx, base_y)
        p.curveTo(cx + 2, base_y + 30, cx - 2, base_y + 55, cx, base_y + 80)
        c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Branches that curve into question-mark shapes
        branch_starts = [
            (cx, base_y + 60, -40, 45),
            (cx, base_y + 70, 35, 40),
            (cx, base_y + 45, -55, 38),
            (cx, base_y + 50, 50, 35),
            (cx, base_y + 75, -20, 35),
            (cx, base_y + 80, 15, 30),
        ]
        for bx, by, angle, length in branch_starts:
            rad = math.radians(90 + angle)
            mid_x = bx + length * 0.5 * math.cos(rad)
            mid_y = by + length * 0.5 * math.sin(rad)
            end_x = bx + length * math.cos(rad)
            end_y = by + length * math.sin(rad)

            c.saveState()
            c.setStrokeColor(_alpha(C_PRIMARY, 0.35))
            c.setLineWidth(1.5)
            p = c.beginPath()
            p.moveTo(bx, by)
            # Curve that hooks at end (question-mark-like)
            hook_x = end_x + 8 * (1 if angle > 0 else -1)
            p.curveTo(mid_x, mid_y + 5, end_x, end_y + 5, hook_x, end_y - 3)
            c.drawPath(p, fill=0, stroke=1)
            c.restoreState()

            # Dot at end of question mark
            self._circle(c, hook_x, end_y - 8, 2.5, _alpha(C_ACCENT, 0.5))

            # Small leaf at branch joint
            self._leaf(c, bx + 3 * (1 if angle > 0 else -1), by + 3, 7,
                       angle + 45, _alpha(C_PRIMARY, 0.3))

        # Roots
        self._root_branch(c, cx, base_y, 25, -90, 3, _alpha(C_SECONDARY, 0.3), 1.0)

    def _draw_18_closing(self, c):
        """Section 18 — Closing Invitation: open hand releasing seeds / birds."""
        w, h = self.width, self.ILLUST_HEIGHT
        cx = w / 2

        # Open hand shape (simplified)
        hand_y = h * 0.25
        c.saveState()
        c.setFillColor(_alpha(C_SECONDARY, 0.12))
        c.setStrokeColor(_alpha(C_SECONDARY, 0.3))
        c.setLineWidth(1.2)
        p = c.beginPath()
        p.moveTo(cx - 50, hand_y)
        p.curveTo(cx - 40, hand_y + 20, cx - 15, hand_y + 25, cx, hand_y + 20)
        p.curveTo(cx + 15, hand_y + 25, cx + 40, hand_y + 20, cx + 50, hand_y)
        p.curveTo(cx + 30, hand_y - 10, cx - 30, hand_y - 10, cx - 50, hand_y)
        c.drawPath(p, fill=1, stroke=1)
        c.restoreState()

        # Seeds and leaf-birds rising from the hand
        rising = [
            (cx - 25, hand_y + 35, 8, 50),
            (cx, hand_y + 45, 10, 30),
            (cx + 20, hand_y + 40, 9, -40),
            (cx - 10, hand_y + 60, 7, 20),
            (cx + 30, hand_y + 55, 6, -30),
        ]
        for rx, ry, sz, angle in rising:
            self._leaf(c, rx, ry, sz, angle, _alpha(C_PRIMARY, 0.35))

        # Stylised birds (simple V-shapes) higher up
        bird_positions = [(cx - 60, h * 0.75), (cx - 20, h * 0.85), (cx + 30, h * 0.8),
                          (cx + 55, h * 0.72)]
        c.saveState()
        c.setStrokeColor(_alpha(C_PRIMARY, 0.3))
        c.setLineWidth(1)
        for bx, by in bird_positions:
            p = c.beginPath()
            p.moveTo(bx - 8, by - 3)
            p.curveTo(bx - 4, by + 4, bx + 4, by + 4, bx + 8, by - 3)
            c.drawPath(p, fill=0, stroke=1)
        c.restoreState()

        # Subtle glow from hand
        self._circle(c, cx, hand_y + 30, 40, _alpha(C_ACCENT, 0.04))
        self._circle(c, cx, hand_y + 30, 60, _alpha(C_ACCENT, 0.02))

    def _draw_19_appendix(self, c):
        """Section 19 — Appendix Resource Library: bookshelf with pressed botanicals."""
        w, h = self.width, self.ILLUST_HEIGHT

        # Bookshelf — two horizontal shelves
        shelf_color = _alpha(C_SECONDARY, 0.25)
        for sy in [h * 0.25, h * 0.55]:
            c.saveState()
            c.setFillColor(shelf_color)
            c.rect(w * 0.1, sy, w * 0.8, 4, fill=1, stroke=0)
            c.restoreState()

        # Books on lower shelf
        book_colors = [
            _alpha(C_PRIMARY, 0.35), _alpha(C_SECONDARY, 0.3), _alpha(C_ACCENT, 0.3),
            _alpha(C_PRIMARY, 0.25), _alpha(C_SECONDARY, 0.4), _alpha(C_ACCENT, 0.25),
            _alpha(C_PRIMARY, 0.3),
        ]
        bx = w * 0.14
        for i, col in enumerate(book_colors):
            bw = 14 + (i % 3) * 3
            bh = 35 + (i % 4) * 5
            c.saveState()
            c.setFillColor(col)
            c.setStrokeColor(_alpha(C_SECONDARY, 0.15))
            c.setLineWidth(0.5)
            c.rect(bx, h * 0.25 + 4, bw, bh, fill=1, stroke=1)
            c.restoreState()
            bx += bw + 3

        # Books on upper shelf
        bx = w * 0.18
        for i in range(5):
            col = book_colors[(i + 3) % len(book_colors)]
            bw = 16 + (i % 2) * 4
            bh = 30 + (i % 3) * 6
            c.saveState()
            c.setFillColor(col)
            c.setStrokeColor(_alpha(C_SECONDARY, 0.12))
            c.setLineWidth(0.5)
            c.rect(bx, h * 0.55 + 4, bw, bh, fill=1, stroke=1)
            c.restoreState()
            bx += bw + 4

        # Pressed botanical specimens — leaves and flowers between books
        pressed_positions = [
            (w * 0.55, h * 0.32, 12, 15, C_PRIMARY),
            (w * 0.65, h * 0.35, 10, -25, C_PRIMARY),
            (w * 0.75, h * 0.3, 8, 40, C_PRIMARY),
            (w * 0.5, h * 0.62, 11, 20, C_PRIMARY),
            (w * 0.7, h * 0.65, 9, -15, C_PRIMARY),
        ]
        for px, py, sz, angle, col in pressed_positions:
            self._leaf(c, px, py, sz, angle, _alpha(col, 0.3), _alpha(col, 0.15))

        # Small flower shapes (simple)
        for fx, fy in [(w * 0.8, h * 0.62), (w * 0.62, h * 0.38)]:
            for petal_angle in range(0, 360, 60):
                rad = math.radians(petal_angle)
                px = fx + 5 * math.cos(rad)
                py = fy + 5 * math.sin(rad)
                self._circle(c, px, py, 3, _alpha(C_ACCENT, 0.2))
            self._circle(c, fx, fy, 2.5, _alpha(C_ACCENT, 0.35))

    # -- dispatch -----------------------------------------------------------

    _DRAW_MAP = {
        1: _draw_01_interconnected_roots,
        2: _draw_02_layered_landscape,
        3: _draw_03_organizing_groups,
        4: _draw_04_flowing_water,
        5: _draw_05_systemic_problems,
        6: _draw_06_flow_addresses,
        7: _draw_07_four_step_cycle,
        8: _draw_08_creating_fund,
        9: _draw_09_legal,
        10: _draw_10_governance,
        11: _draw_11_attracting_capital,
        12: _draw_12_storytelling,
        13: _draw_13_activation_series,
        14: _draw_14_tools_templates,
        15: _draw_15_kinship_support,
        16: _draw_16_coming_next,
        17: _draw_17_faq,
        18: _draw_18_closing,
        19: _draw_19_appendix,
    }

    def draw(self):
        draw_fn = self._DRAW_MAP.get(self.section_num)
        if draw_fn:
            self.canv.saveState()
            draw_fn(self, self.canv)
            self.canv.restoreState()


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

            # Check for an italic subtitle line immediately after the heading
            # (blank line then *subtitle text*)
            peek = i + 1
            if peek < len(lines) and lines[peek].strip() == "":
                peek += 1
            if peek < len(lines):
                sub_stripped = lines[peek].strip()
                sub_match = re.match(r'^\*([^*]+)\*$', sub_stripped)
                if sub_match:
                    subtitle_text = sub_match.group(1)
                    flowables.append(Paragraph(subtitle_text, STYLES["section_subtitle"]))
                    flowables.append(Spacer(1, 6))
                    i = peek + 1
                else:
                    flowables.append(Spacer(1, 2))
                    i += 1
            else:
                flowables.append(Spacer(1, 2))
                i += 1

            # --- Section illustration (organic, nature-themed) ---
            if sec_num in SectionIllustration._DRAW_MAP:
                flowables.append(SectionIllustration(sec_num))
                flowables.append(Spacer(1, 10))

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
