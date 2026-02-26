#!/usr/bin/env python3
"""Generate a professional PDF of the Unified Sanctuaries Investor Business Plan."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, KeepTogether
)
from reportlab.lib import colors

# ── Colour palette ──────────────────────────────────────────────────
DARK_GREEN  = HexColor("#2D5016")
MID_GREEN   = HexColor("#4A7C28")
LIGHT_GREEN = HexColor("#E8F5E0")
CREAM       = HexColor("#FAF8F0")
DARK_TEXT    = HexColor("#1A1A1A")
MID_TEXT     = HexColor("#3A3A3A")
ACCENT_GOLD = HexColor("#B8860B")
TABLE_HEADER = HexColor("#2D5016")
TABLE_ALT    = HexColor("#F0F7EC")
RULE_COLOR   = HexColor("#4A7C28")


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "CoverTitle", fontName="Helvetica-Bold", fontSize=28,
        leading=34, textColor=DARK_GREEN, alignment=TA_CENTER,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle", fontName="Helvetica", fontSize=14,
        leading=18, textColor=MID_GREEN, alignment=TA_CENTER,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "CoverDate", fontName="Helvetica-Oblique", fontSize=11,
        leading=14, textColor=MID_TEXT, alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "SectionHead", fontName="Helvetica-Bold", fontSize=18,
        leading=22, textColor=DARK_GREEN, spaceBefore=18, spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        "SubHead", fontName="Helvetica-Bold", fontSize=14,
        leading=18, textColor=MID_GREEN, spaceBefore=14, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "SubHead2", fontName="Helvetica-Bold", fontSize=12,
        leading=16, textColor=DARK_GREEN, spaceBefore=10, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=10,
        leading=14, textColor=DARK_TEXT, alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "BodyBold", fontName="Helvetica-Bold", fontSize=10,
        leading=14, textColor=DARK_TEXT, alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "Highlight", fontName="Helvetica-Bold", fontSize=10.5,
        leading=15, textColor=DARK_GREEN, alignment=TA_JUSTIFY,
        spaceAfter=8, borderColor=MID_GREEN, borderWidth=0,
        leftIndent=12, rightIndent=12,
    ))
    styles.add(ParagraphStyle(
        "PillarTitle", fontName="Helvetica-Bold", fontSize=11,
        leading=15, textColor=MID_GREEN, spaceBefore=8, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "TableCell", fontName="Helvetica", fontSize=9,
        leading=12, textColor=DARK_TEXT,
    ))
    styles.add(ParagraphStyle(
        "TableCellBold", fontName="Helvetica-Bold", fontSize=9,
        leading=12, textColor=DARK_TEXT,
    ))
    styles.add(ParagraphStyle(
        "TableHeader", fontName="Helvetica-Bold", fontSize=9,
        leading=12, textColor=colors.white,
    ))
    styles.add(ParagraphStyle(
        "BulletItem", fontName="Helvetica", fontSize=10,
        leading=14, textColor=DARK_TEXT, leftIndent=24,
        bulletIndent=12, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        "Footer", fontName="Helvetica-Oblique", fontSize=9,
        leading=12, textColor=MID_TEXT, alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "ContactInfo", fontName="Helvetica", fontSize=10,
        leading=14, textColor=MID_TEXT, alignment=TA_CENTER,
        spaceAfter=4,
    ))
    return styles


def hr():
    return HRFlowable(
        width="100%", thickness=1, color=RULE_COLOR,
        spaceBefore=10, spaceAfter=10,
    )


def make_table(header, rows, col_widths=None):
    """Build a styled table from header list and row lists."""
    s = build_styles()
    t_header = [Paragraph(c, s["TableHeader"]) for c in header]
    t_rows = []
    for row in rows:
        t_rows.append([
            Paragraph(str(c), s["TableCellBold"] if i == 0 else s["TableCell"])
            for i, c in enumerate(row)
        ])
    data = [t_header] + t_rows

    if col_widths is None:
        col_widths = [None] * len(header)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND",  (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING",  (0, 0), (-1, 0), 8),
        ("GRID",        (0, 0), (-1, -1), 0.5, HexColor("#C0C0C0")),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",(0, 0), (-1, -1), 8),
        ("TOPPADDING",  (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 1), (-1, -1), 6),
    ]
    # Alternating row colours
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.setFillColor(MID_TEXT)
    canvas.drawCentredString(
        letter[0] / 2, 0.5 * inch,
        "Unified Sanctuaries  |  Confidential \u2014 For Aligned Investors Only  |  February 2026"
    )
    canvas.drawRightString(
        letter[0] - 0.75 * inch, 0.5 * inch,
        f"Page {doc.page}"
    )
    canvas.restoreState()


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        topMargin=0.75 * inch, bottomMargin=0.85 * inch,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
    )
    s = build_styles()
    story = []

    # ── COVER ────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.6 * inch))
    story.append(Paragraph("Unified Sanctuaries", s["CoverTitle"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Investor Business Plan", s["CoverSubtitle"]))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="40%", thickness=2, color=ACCENT_GOLD,
                             spaceBefore=4, spaceAfter=4))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "A Regenerative Village on University Infrastructure", s["CoverSubtitle"]))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Prepared February 2026  |  Confidential", s["CoverDate"]))
    story.append(Spacer(1, 1.2 * inch))

    # Tagline
    story.append(Paragraph(
        "<i>For an investor who understands land, knows the value of community, "
        "and has watched institutions fail the people they were built to serve \u2014 "
        "this is a chance to repurpose that infrastructure for what it should have "
        "been all along: a place where people learn to grow food, heal, build "
        "together, and take care of each other.</i>",
        s["Footer"]
    ))
    story.append(PageBreak())

    # ── PAGE 1: THE OPPORTUNITY ──────────────────────────────────────
    story.append(Paragraph(
        "The Opportunity: A University Campus Becomes a Living Village",
        s["SectionHead"]))
    story.append(hr())

    story.append(Paragraph(
        "Across the country, small universities and college campuses are closing "
        "or consolidating \u2014 leaving behind extraordinary infrastructure: dining "
        "halls, dormitories, classrooms, performance spaces, agricultural land, "
        "gathering halls, workshops, and utilities already built to code. These "
        "properties represent tens of millions of dollars in existing infrastructure "
        "that would cost multiples to build from scratch.",
        s["Body"]))

    story.append(Paragraph(
        "Unified Sanctuaries is positioned to acquire one of these campuses and "
        "transform it into a self-sustaining regenerative village \u2014 a place where "
        "farming, healing, education, cultural gathering, and cooperative living "
        "operate as one integrated community. Not a commune. Not a resort. "
        "A functioning village economy with multiple revenue streams, a proven "
        "team, and a replicable model designed to be shared openly with the world.",
        s["Body"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Why University Infrastructure", s["SubHead"]))

    story.append(Paragraph(
        "A campus provides what would otherwise take years and millions to develop:",
        s["Body"]))

    campus_table = make_table(
        ["Campus Asset", "Village Function", "Revenue Pillar"],
        [
            ["Agricultural land, greenhouses, barns",
             "Regenerative farm, food forest, farm stand, cafe",
             "Permaculture Farm & Education"],
            ["Student housing, residential halls",
             "Eco-homes, cooperative living for 20+ households",
             "Community Living"],
            ["Auditoriums, gyms, outdoor amphitheaters",
             "Festivals, concerts, weddings, conferences, markets",
             "Event Venue & Innovation Hall"],
            ["Classrooms, studios, wellness facilities",
             "Retreat center, healing arts, bathhouse, makerspace",
             "Retreat & Healing Arts Center"],
            ["Commercial kitchens, dining halls",
             "Community cafe, catering, herbal apothecary",
             "Shared across all pillars"],
            ["Utilities, roads, water/sewer",
             "Fully operational from day one",
             "Foundation for all operations"],
        ],
        col_widths=[2.1 * inch, 2.4 * inch, 2.0 * inch],
    )
    story.append(campus_table)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>The result: instead of a 5-year buildout, we can be revenue-generating "
        "within months of acquisition.</b> Infrastructure that a university spent "
        "decades building can be reactivated for a community that will actually "
        "use every square foot of it.",
        s["Highlight"]))

    story.append(PageBreak())

    # ── PAGE 2: PLAN, TEAM, TRACK RECORD ─────────────────────────────
    story.append(Paragraph(
        "The Plan, the Team, and the Track Record", s["SectionHead"]))
    story.append(hr())

    story.append(Paragraph(
        "Four Revenue Pillars \u2014 $1.4M to $4.5M+ Annually at Maturity",
        s["SubHead"]))

    # Pillar 1
    story.append(Paragraph(
        "1. Permaculture Farm & Education Center \u2014 $315K to $1M+/year",
        s["PillarTitle"]))
    story.append(Paragraph(
        "Regenerative agriculture, a community cafe, forest school programming, "
        "agritourism (U-pick, farm dinners, workshops), and a farm stand. This is "
        "the heart of the land ethic \u2014 growing food, teaching people how to grow "
        "food, and building food sovereignty for the region. Our team has hands-on "
        "experience managing farm operations, soil science, compost systems, "
        "herbalism, and permaculture design across 40+ land-based projects.",
        s["Body"]))

    # Pillar 2
    story.append(Paragraph(
        "2. Retreat & Healing Arts Center + Bathhouse \u2014 $570K to $1.75M/year",
        s["PillarTitle"]))
    story.append(Paragraph(
        "Immersive retreats, somatic therapy, art therapy, herbalism, a spa and "
        "bathhouse, a campground, and a makerspace. Campus wellness facilities, "
        "studios, and residential halls convert directly into retreat infrastructure. "
        "Our team includes practitioners in somatic therapy, herbalism, ritual "
        "theater, visual and performing arts, consent-based facilitation, and "
        "ecstatic movement.",
        s["Body"]))

    # Pillar 3
    story.append(Paragraph(
        "3. Event Venue & Innovation Hall \u2014 $310K to $1.16M/year",
        s["PillarTitle"]))
    story.append(Paragraph(
        "Festivals, concerts, weddings, conferences, knowledge-sharing gatherings, "
        "and AV/multimedia production. Campus auditoriums, outdoor spaces, and "
        "dining facilities are already built for large gatherings. Our team has "
        "direct experience in festival production, event logistics, financial "
        "operations, and multimedia production at scale.",
        s["Body"]))

    # Pillar 4
    story.append(Paragraph(
        "4. Community Living / Regenerative Neighborhood \u2014 $195K to $580K/year",
        s["PillarTitle"]))
    story.append(Paragraph(
        "Cooperative living for 20+ households in converted campus housing and "
        "new eco-builds. Residents contribute to the village economy and form the "
        "stable social fabric that sustains all other pillars. Revenue from housing "
        "fees, membership dues, and shared stewardship contributions.",
        s["Body"]))

    story.append(Spacer(1, 6))

    # ── The Team ─────────────────────────────────────────────────────
    story.append(Paragraph(
        "The Team \u2014 Proven, Ready, and Already Working Together",
        s["SubHead"]))

    story.append(Paragraph(
        "This is not a group of strangers with a business plan. This is a team "
        "that has been building together for years \u2014 across 50+ learn-by-doing "
        "events, 40+ land-based project sites, and a network of 2,200+ "
        "participants. We have raised over $800,000 through our nonprofit "
        "Kinship Earth and deployed $370,000+ in direct grants to grassroots "
        "leaders across 12+ bioregions. We are already operating.",
        s["Body"]))

    team_data = [
        ["Syd Harvey Griffith",
         "Lead visionary. Executive Director of Kinship Earth (global regenerative "
         "finance nonprofit, $800K+ raised). Co-founder of Permatours (50+ events, "
         "40+ projects, 2,200+ participants). Systems designer, capital strategist, "
         "community organizer."],
        ["Lynney Rey",
         "Farm operations, community cafe, herbalism, forest school, performing "
         "and visual arts."],
        ["Scotty Guzman",
         "Soil scientist, compost specialist, natural builder, engineer. Has built "
         "infrastructure at dozens of land-based projects."],
        ["Fuego Gale",
         "Accounting, financial operations, festival production, membership sales. "
         "The operational backbone for mission-driven organizations."],
        ["Josie Watson",
         "Earth lawyer, governance designer, playwright. Founder of Mycelial Law. "
         "Designs legal and governance structures that protect the land and community."],
        ["Eslerh Oreste",
         "Film, multimedia, ritual theater, healing arts. Drives storytelling, "
         "media production, and cultural programming."],
        ["Pato",
         "Permaculture installations, global hub partnerships, nonprofit management."],
        ["Nina",
         "Storytelling, herbal goods, farm operations, fundraising."],
        ["Tiff",
         "Somatic therapy, art therapy, retreat facilitation."],
        ["Jess",
         "Bathhouse operations, consent workshops, civil engineering, ecstatic dance."],
    ]
    team_table = make_table(
        ["Team Member", "What They Bring"],
        team_data,
        col_widths=[1.6 * inch, 5.0 * inch],
    )
    story.append(team_table)

    story.append(Spacer(1, 10))

    # ── Ecosystem ────────────────────────────────────────────────────
    story.append(Paragraph("Ecosystem Backing", s["SubHead"]))
    story.append(Paragraph(
        "Unified Sanctuaries does not operate in isolation. It sits within a "
        "constellation of established organizations:", s["Body"]))

    eco_items = [
        ("<b>Kinship Earth</b> (501c3) \u2014 Global regenerative finance nonprofit. "
         "$800K+ raised, $370K+ deployed across 12+ bioregions. Provides fiscal "
         "infrastructure, donor networks, and philanthropic credibility."),
        ("<b>Permatours</b> (501c3) \u2014 Northeast permaculture action network. "
         "50+ events, 40+ project sites, 1,000+ active members. Provides a "
         "ready-made pipeline of skilled volunteers, educators, and community members."),
        ("<b>Planetary Party</b> \u2014 Global coordination protocol active across "
         "5+ bioregions (Colombia, Jamaica, Mexico, Guatemala, NE Turtle Island). "
         "Provides cultural programming, governance frameworks, and international visibility."),
        ("<b>Partner Network</b> \u2014 Diggers Cooperative (compost), Birds Nest "
         "Builders (natural building co-op), Eco Phi (regenerative architecture), "
         "Mycelial Law (earth law), Micelio Media (film), Herbaria (herbalism & "
         "catering), and dozens more aligned producers and practitioners."),
    ]
    for item in eco_items:
        story.append(Paragraph(item, s["BulletItem"], bulletText="\u2022"))

    story.append(PageBreak())

    # ── PAGE 3: EXECUTION, FINANCIALS, THE ASK ───────────────────────
    story.append(Paragraph(
        "Execution Plan, Financial Model, and the Ask", s["SectionHead"]))
    story.append(hr())

    story.append(Paragraph(
        "Upon Acquisition: The 90-Day Activation", s["SubHead"]))
    story.append(Paragraph(
        'This is not a "build it someday" plan. Upon campus acquisition, the '
        "team executes immediately:", s["Body"]))

    # Days 1-30
    story.append(Paragraph("Days 1\u201330: Foundation", s["SubHead2"]))
    for b in [
        "Founding team moves on-site; key personnel occupy campus housing",
        "Legal structures finalized (Community Land Trust, pillar-specific trusts, stewardship agreements)",
        "Farm assessment: soil testing, existing agricultural infrastructure inventory, first-season crop planning",
        "Building audit: which campus facilities map to which pillar, what needs renovation vs. immediate activation",
        "Early membership and community engagement launch",
    ]:
        story.append(Paragraph(b, s["BulletItem"], bulletText="\u2022"))

    # Days 31-60
    story.append(Paragraph("Days 31\u201360: First Revenue", s["SubHead2"]))
    for b in [
        "Farm stand and community cafe open (using campus commercial kitchen and existing agricultural land)",
        "First retreat and workshop programming scheduled (using campus studios, residential halls, wellness spaces)",
        "Event venue bookings begin (weddings, conferences, festivals \u2014 campus auditoriums and outdoor spaces)",
        "Permatours activates volunteer network for initial work days, builds, and plantings on-site",
    ]:
        story.append(Paragraph(b, s["BulletItem"], bulletText="\u2022"))

    # Days 61-90
    story.append(Paragraph("Days 61\u201390: Community Formation", s["SubHead2"]))
    for b in [
        "First residents onboarded into cooperative living (converted campus housing)",
        "Governance structures activated (Anchor Circle, pillar-specific autonomous nodes, community agreements)",
        "Circular economy infrastructure launched (community utility token, voice governance tokens)",
        "Public storytelling and media production begins \u2014 documenting the transformation for fundraising and replication",
    ]:
        story.append(Paragraph(b, s["BulletItem"], bulletText="\u2022"))

    story.append(Spacer(1, 8))

    # ── Financial Summary ────────────────────────────────────────────
    story.append(Paragraph("Financial Summary", s["SubHead"]))

    fin_table = make_table(
        ["", "Year 1 (Conservative)", "Year 2", "Year 3 (At Maturity)"],
        [
            ["Farm & Education",        "$315K",   "$600K",   "$1M+"],
            ["Retreat & Healing Arts",   "$570K",   "$1M",     "$1.75M"],
            ["Event Venue",             "$310K",   "$700K",   "$1.16M"],
            ["Community Living",        "$195K",   "$400K",   "$580K"],
            ["Total Revenue",           "$1.4M",   "$2.7M",   "$4.5M+"],
        ],
        col_widths=[1.8 * inch, 1.6 * inch, 1.3 * inch, 1.8 * inch],
    )
    story.append(fin_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Revenue is diversified across four independent pillars. No single pillar "
        "carries the model \u2014 if one has a slow season, three others continue "
        "generating. This is the resilience of a village economy versus a "
        "single-purpose business.",
        s["Body"]))

    # ── Capital Strategy ─────────────────────────────────────────────
    story.append(Paragraph("Capital Strategy", s["SubHead"]))
    cap_table = make_table(
        ["Phase", "Target", "Timeline", "Purpose"],
        [
            ["Phase 1", "$10M", "End of 2026",
             "Campus acquisition, legal structuring, initial activation, first-year operations"],
            ["Phase 2", "$100M", "2028",
             "Full buildout, eco-home construction, expanded programming, infrastructure upgrades, open-source documentation"],
        ],
        col_widths=[1.0 * inch, 1.0 * inch, 1.2 * inch, 3.3 * inch],
    )
    story.append(cap_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Capital sources: impact investment, philanthropic donations, community "
        "memberships, earned revenue, aligned partnerships, and government grants "
        "(USDA Beginning Farmer, Vermont Housing & Conservation Board, climate programs).",
        s["Body"]))

    story.append(PageBreak())

    # ── What Makes This Different ────────────────────────────────────
    story.append(Paragraph("What Makes This Investment Different", s["SubHead"]))

    differentiators = [
        ("<b>1. Existing Infrastructure Eliminates the Biggest Risk.</b> "
         "The #1 reason land-based community projects fail is the multi-year, "
         "multi-million-dollar buildout before any revenue flows. A university "
         "campus removes that barrier. We inherit decades of investment in "
         "buildings, utilities, and land \u2014 and activate them for their highest purpose."),
        ("<b>2. The Team is Already Operating.</b> "
         "This is not a first-time founder with a pitch deck. This is a team with "
         "years of shared work, $800K+ raised and deployed through established "
         "nonprofits, 50+ events produced, 40+ land projects served, and a living "
         "network of 2,200+ practitioners ready to show up."),
        ("<b>3. Non-Speculative Land Stewardship.</b> "
         "The land goes into a Community Land Trust \u2014 permanently removed from "
         "market speculation. This is not a real estate play. This is a regenerative "
         "investment in a community asset that grows in value through stewardship, "
         "not extraction."),
        ("<b>4. Community is the Product.</b> "
         "Every pillar is designed around gathering people: farmers growing food "
         "together, healers practicing together, artists creating together, neighbors "
         "living together. Revenue comes from the natural activity of a thriving "
         "community \u2014 not from artificial demand or marketing gimmicks."),
        ("<b>5. Open-Source Blueprint.</b> "
         "Every governance framework, financial model, and operational design will "
         "be documented and shared publicly. This is not just one village \u2014 it is "
         "the template for hundreds. Your investment doesn't end at one property "
         "line. It seeds a movement."),
    ]
    for d in differentiators:
        story.append(Paragraph(d, s["Body"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))

    # ── The Ask ──────────────────────────────────────────────────────
    story.append(Paragraph("The Ask", s["SubHead"]))

    story.append(Paragraph(
        "We are seeking an aligned investor-partner to acquire a university campus "
        "in the Southern Vermont corridor (Brattleboro / Guilford / Putney) \u2014 or "
        "a comparable campus property with the right infrastructure \u2014 and place it "
        "into a Community Land Trust as the permanent home of Unified Sanctuaries.",
        s["Body"]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("This is an invitation for someone who:", s["Body"]))
    for item in [
        "Understands that the best infrastructure in America is sitting empty while communities go without",
        "Knows from experience that farming is both a livelihood and a way of life worth protecting",
        "Believes that helping people and building community is not just good ethics \u2014 it is good economics",
        "Wants their capital to create something that outlasts them",
    ]:
        story.append(Paragraph(item, s["BulletItem"], bulletText="\u2022"))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>We have the team. We have the plan. We have the network. "
        "We have the track record. We need the land.</b>",
        s["Highlight"]))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="60%", thickness=1.5, color=ACCENT_GOLD,
                             spaceBefore=6, spaceAfter=12))

    # ── Contact ──────────────────────────────────────────────────────
    story.append(Paragraph(
        "Contact: Syd Harvey Griffith  |  sydney.griffith123@gmail.com",
        s["ContactInfo"]))
    story.append(Paragraph(
        "Kinship Earth: kinshipearth.org  |  Permatours: permatours.org  |  "
        "Planetary Party: planetaryparty.com",
        s["ContactInfo"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<i>Prepared February 2026  |  Unified Sanctuaries  |  "
        "Confidential \u2014 For Aligned Investors Only</i>",
        s["Footer"]))

    # ── Build ────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__),
                       "Unified-Sanctuaries-Investor-Business-Plan.pdf")
    build_pdf(out)
