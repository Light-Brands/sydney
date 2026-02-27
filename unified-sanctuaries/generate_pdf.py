#!/usr/bin/env python3
"""Generate a professional PDF of the Unified Sanctuaries Investor Business Plan.

Uses fpdf2 (pip install fpdf2).
"""

from fpdf import FPDF

FONT = "FreeSans"
FONT_DIR = "/usr/share/fonts/truetype/freefont/"


class BusinessPlanPDF(FPDF):
    ACCENT = (45, 106, 79)       # forest green
    DARK = (33, 37, 41)          # near-black
    MEDIUM = (73, 80, 87)        # dark gray
    LIGHT_BG = (235, 245, 238)   # light green tint
    WHITE = (255, 255, 255)
    TABLE_HEADER_BG = (45, 106, 79)
    TABLE_ALT_BG = (245, 250, 245)
    GOLD = (184, 134, 11)

    def _register_fonts(self):
        self.add_font(FONT, "", FONT_DIR + "FreeSans.ttf")
        self.add_font(FONT, "B", FONT_DIR + "FreeSansBold.ttf")
        self.add_font(FONT, "I", FONT_DIR + "FreeSansOblique.ttf")
        self.add_font(FONT, "BI", FONT_DIR + "FreeSansBoldOblique.ttf")

    def header(self):
        if self.page_no() > 1:
            self.set_font(FONT, "I", 8)
            self.set_text_color(*self.MEDIUM)
            self.cell(
                0, 6,
                "Unified Sanctuaries  |  Investor Business Plan  |  Confidential",
                align="R",
            )
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT, "I", 8)
        self.set_text_color(*self.MEDIUM)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── helpers ──────────────────────────────────────────────────────

    def accent_rule(self):
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.7)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(6)

    def section_title(self, text):
        self.set_font(FONT, "B", 17)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 11, text, new_x="LMARGIN", new_y="NEXT")
        self.accent_rule()

    def subsection_title(self, text):
        self.set_font(FONT, "B", 13)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def sub2_title(self, text):
        self.set_font(FONT, "B", 11)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body(self, text):
        self.set_font(FONT, "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def body_bold(self, text):
        self.set_font(FONT, "B", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def body_italic(self, text):
        self.set_font(FONT, "I", 10)
        self.set_text_color(*self.MEDIUM)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def highlight_block(self, text):
        """Green-tinted highlight box."""
        w = self.w - self.l_margin - self.r_margin
        self.set_font(FONT, "B", 10.5)
        lines = self.multi_cell(w - 16, 5.8, text, dry_run=True, output="LINES")
        h = len(lines) * 5.8 + 14
        y = self.get_y()
        if y + h > self.h - 25:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(*self.LIGHT_BG)
        self.rect(self.l_margin, y, w, h, style="F")
        # left accent bar
        self.set_fill_color(*self.ACCENT)
        self.rect(self.l_margin, y, 3, h, style="F")
        self.set_xy(self.l_margin + 10, y + 7)
        self.set_text_color(*self.ACCENT)
        self.multi_cell(w - 16, 5.8, text)
        self.set_y(y + h + 5)

    def bullet(self, text, bold_prefix=""):
        self.set_font(FONT, "", 10)
        self.set_text_color(*self.DARK)
        x0 = self.get_x()
        self.cell(8, 5.5, "\u2022")
        if bold_prefix:
            self.set_font(FONT, "B", 10)
            bw = self.get_string_width(bold_prefix) + 1
            self.cell(bw, 5.5, bold_prefix)
            self.set_font(FONT, "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1.5)

    def pillar_block(self, title, revenue, description):
        w = self.w - self.l_margin - self.r_margin
        self.set_font(FONT, "", 10)
        lines = self.multi_cell(w - 14, 5.5, description,
                                dry_run=True, output="LINES")
        box_h = 10 + 6 + len(lines) * 5.5 + 6
        y = self.get_y()
        if y + box_h > self.h - 25:
            self.add_page()
            y = self.get_y()

        # background
        self.set_fill_color(*self.LIGHT_BG)
        self.rect(self.l_margin, y, w, box_h, style="F")
        # left accent bar
        self.set_fill_color(*self.ACCENT)
        self.rect(self.l_margin, y, 3, box_h, style="F")

        self.set_xy(self.l_margin + 8, y + 5)
        self.set_font(FONT, "B", 11)
        self.set_text_color(*self.ACCENT)
        tw = self.get_string_width(title)
        self.cell(tw + 3, 6, title)

        self.set_font(FONT, "", 10)
        self.set_text_color(*self.MEDIUM)
        self.cell(0, 6, revenue)

        self.set_xy(self.l_margin + 8, y + 16)
        self.set_font(FONT, "", 10)
        self.set_text_color(*self.DARK)
        self.multi_cell(w - 14, 5.5, description)

        self.set_y(y + box_h + 5)

    def draw_table(self, headers, rows, col_widths=None):
        usable = self.w - self.l_margin - self.r_margin
        if col_widths is None:
            col_widths = [usable / len(headers)] * len(headers)

        row_h = 8
        # header
        self.set_fill_color(*self.TABLE_HEADER_BG)
        self.set_text_color(*self.WHITE)
        self.set_font(FONT, "B", 9)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], row_h, f"  {h}", border=0, fill=True)
        self.ln(row_h)

        # rows
        self.set_font(FONT, "", 9)
        for row_idx, row in enumerate(rows):
            alt = row_idx % 2 == 0
            if alt:
                self.set_fill_color(*self.TABLE_ALT_BG)
            else:
                self.set_fill_color(*self.WHITE)

            # calc max cell height
            line_counts = []
            for i, cell_text in enumerate(row):
                ls = self.multi_cell(col_widths[i] - 4, 5, cell_text,
                                     dry_run=True, output="LINES")
                line_counts.append(len(ls))
            cell_h = max(max(line_counts) * 5, 7) + 4

            # page break?
            if self.get_y() + cell_h > self.h - 25:
                self.add_page()
                self.set_fill_color(*self.TABLE_HEADER_BG)
                self.set_text_color(*self.WHITE)
                self.set_font(FONT, "B", 9)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], row_h, f"  {h}", border=0, fill=True)
                self.ln(row_h)
                self.set_font(FONT, "", 9)
                if alt:
                    self.set_fill_color(*self.TABLE_ALT_BG)
                else:
                    self.set_fill_color(*self.WHITE)

            y0 = self.get_y()
            x0 = self.get_x()

            # fill rects
            xp = x0
            for i in range(len(row)):
                self.rect(xp, y0, col_widths[i], cell_h, style="F")
                xp += col_widths[i]
            # draw thin grid lines
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.3)
            xp = x0
            for i in range(len(row)):
                self.rect(xp, y0, col_widths[i], cell_h, style="D")
                xp += col_widths[i]

            # text
            self.set_text_color(*self.DARK)
            xp = x0
            for i, cell_text in enumerate(row):
                if i == 0:
                    self.set_font(FONT, "B", 9)
                else:
                    self.set_font(FONT, "", 9)
                self.set_xy(xp + 2, y0 + 2)
                self.multi_cell(col_widths[i] - 4, 5, cell_text)
                xp += col_widths[i]

            self.set_xy(x0, y0 + cell_h)

        self.ln(5)


def build_pdf(output_path):
    pdf = BusinessPlanPDF(orientation="P", unit="mm", format="Letter")
    pdf._register_fonts()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ================================================================
    # COVER PAGE
    # ================================================================
    pdf.add_page()
    pdf.ln(55)
    pdf.set_font(FONT, "B", 34)
    pdf.set_text_color(*pdf.ACCENT)
    pdf.cell(0, 15, "Unified Sanctuaries", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font(FONT, "", 16)
    pdf.set_text_color(*pdf.DARK)
    pdf.cell(0, 10, "Investor Business Plan", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # gold accent line
    mid = pdf.w / 2
    pdf.set_draw_color(*pdf.GOLD)
    pdf.set_line_width(1.2)
    pdf.line(mid - 35, pdf.get_y(), mid + 35, pdf.get_y())
    pdf.ln(8)

    pdf.set_font(FONT, "I", 13)
    pdf.set_text_color(*pdf.MEDIUM)
    pdf.cell(0, 8, "A Regenerative Village on University Infrastructure",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_font(FONT, "", 11)
    pdf.set_text_color(*pdf.MEDIUM)
    pdf.cell(0, 7, "Prepared February 2026", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Confidential \u2014 For Aligned Investors Only",
             align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(28)

    pdf.set_font(FONT, "I", 9.5)
    pdf.set_text_color(*pdf.MEDIUM)
    pdf.multi_cell(0, 5.5,
        "For an investor who understands land, knows the value of community, "
        "and has watched institutions fail the people they were built to serve "
        "\u2014 this is a chance to repurpose that infrastructure for what it "
        "should have been all along: a place where people learn to grow food, "
        "heal, build together, and take care of each other.",
        align="C")

    pdf.ln(20)
    pdf.set_font(FONT, "", 10)
    pdf.cell(0, 7,
             "Contact: Syd Harvey Griffith  |  sydney.griffith123@gmail.com",
             align="C", new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    # PAGE 1 — THE OPPORTUNITY
    # ================================================================
    pdf.add_page()
    pdf.section_title(
        "The Opportunity: A University Campus Becomes a Living Village")

    pdf.body(
        "Across the country, small universities and college campuses are "
        "closing or consolidating \u2014 leaving behind extraordinary "
        "infrastructure: dining halls, dormitories, classrooms, performance "
        "spaces, agricultural land, gathering halls, workshops, and utilities "
        "already built to code. These properties represent tens of millions "
        "of dollars in existing infrastructure that would cost multiples to "
        "build from scratch."
    )
    pdf.body(
        "Unified Sanctuaries is positioned to acquire one of these campuses "
        "and transform it into a self-sustaining regenerative village \u2014 a "
        "place where farming, healing, education, cultural gathering, and "
        "cooperative living operate as one integrated community. Not a "
        "commune. Not a resort. A functioning village economy with multiple "
        "revenue streams, a proven team, and a replicable model designed to "
        "be shared openly with the world."
    )

    pdf.subsection_title("Why University Infrastructure")
    pdf.body("A campus provides what would otherwise take years and millions "
             "to develop:")

    pdf.draw_table(
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
        col_widths=[55, 62, 53],
    )

    pdf.highlight_block(
        "The result: instead of a 5-year buildout, we can be "
        "revenue-generating within months of acquisition. Infrastructure "
        "that a university spent decades building can be reactivated for a "
        "community that will actually use every square foot of it."
    )

    # ================================================================
    # PAGE 2 — PLAN, TEAM, TRACK RECORD
    # ================================================================
    pdf.add_page()
    pdf.section_title("The Plan, the Team, and the Track Record")

    pdf.subsection_title(
        "Four Revenue Pillars \u2014 $1.4M to $4.5M+ Annually at Maturity")

    pdf.pillar_block(
        "1. Permaculture Farm & Education Center",
        "\u2014 $315K to $1M+/year",
        "Regenerative agriculture, a community cafe, forest school "
        "programming, agritourism (U-pick, farm dinners, workshops), and a "
        "farm stand. This is the heart of the land ethic \u2014 growing food, "
        "teaching people how to grow food, and building food sovereignty for "
        "the region. Our team has hands-on experience managing farm "
        "operations, soil science, compost systems, herbalism, and "
        "permaculture design across 40+ land-based projects.",
    )
    pdf.pillar_block(
        "2. Retreat & Healing Arts Center + Bathhouse",
        "\u2014 $570K to $1.75M/year",
        "Immersive retreats, somatic therapy, art therapy, herbalism, a spa "
        "and bathhouse, a campground, and a makerspace. Campus wellness "
        "facilities, studios, and residential halls convert directly into "
        "retreat infrastructure. Our team includes practitioners in somatic "
        "therapy, herbalism, ritual theater, visual and performing arts, "
        "consent-based facilitation, and ecstatic movement.",
    )
    pdf.pillar_block(
        "3. Event Venue & Innovation Hall",
        "\u2014 $310K to $1.16M/year",
        "Festivals, concerts, weddings, conferences, knowledge-sharing "
        "gatherings, and AV/multimedia production. Campus auditoriums, "
        "outdoor spaces, and dining facilities are already built for large "
        "gatherings. Our team has direct experience in festival production, "
        "event logistics, financial operations, and multimedia production "
        "at scale.",
    )
    pdf.pillar_block(
        "4. Community Living / Regenerative Neighborhood",
        "\u2014 $195K to $580K/year",
        "Cooperative living for 20+ households in converted campus housing "
        "and new eco-builds. Residents contribute to the village economy and "
        "form the stable social fabric that sustains all other pillars. "
        "Revenue from housing fees, membership dues, and shared stewardship "
        "contributions.",
    )

    # ── The Team ────────────────────────────────────────────────────
    pdf.subsection_title(
        "The Team \u2014 Proven, Ready, and Already Working Together")

    pdf.body(
        "This is not a group of strangers with a business plan. This is a "
        "team that has been building together for years \u2014 across 50+ "
        "learn-by-doing events, 40+ land-based project sites, and a network "
        "of 2,200+ participants. We have raised over $800,000 through our "
        "nonprofit Kinship Earth and deployed $370,000+ in direct grants to "
        "grassroots leaders across 12+ bioregions. We are already operating."
    )

    pdf.draw_table(
        ["Team Member", "What They Bring"],
        [
            ["Syd Harvey Griffith",
             "Lead visionary. Executive Director of Kinship Earth ($800K+ "
             "raised). Co-founder of Permatours (50+ events, 40+ projects, "
             "2,200+ participants). Systems designer, capital strategist, "
             "community organizer."],
            ["Lynney Rey",
             "Farm operations, community cafe, herbalism, forest school, "
             "performing and visual arts. Direct agricultural and "
             "food-systems experience."],
            ["Scotty Guzman",
             "Soil scientist, compost specialist, natural builder, engineer. "
             "Has built infrastructure at dozens of land-based projects."],
            ["Fuego Gale",
             "Accounting, financial operations, festival production, "
             "membership sales. Experienced in managing money, events, and "
             "compliance for mission-driven organizations."],
            ["Josie Watson",
             "Earth lawyer, governance designer, playwright. Founder of "
             "Mycelial Law. Designs legal and governance structures that "
             "protect the land and community long-term."],
            ["Eslerh Oreste",
             "Film, multimedia, ritual theater, healing arts. Drives "
             "storytelling, media production, and cultural programming."],
            ["Pato Collins",
             "Permaculture installations, global hub partnerships, nonprofit "
             "management. Experienced in international regenerative networks."],
            ["Nina Landau",
             "Storytelling, herbal goods, farm operations, fundraising. "
             "Bridges agricultural production with narrative and revenue "
             "generation."],
            ["Tiff Von Walter",
             "Somatic therapy, art therapy, retreat facilitation. Anchors "
             "healing arts and retreat programming with professional "
             "clinical experience."],
            ["Jess Mortell",
             "Bathhouse operations, consent workshops, civil engineering, "
             "ecstatic dance. Technical infrastructure knowledge and "
             "embodied wellness experience."],
        ],
        col_widths=[38, 132],
    )

    # ── Ecosystem ───────────────────────────────────────────────────
    pdf.subsection_title("Ecosystem Backing")
    pdf.body(
        "Unified Sanctuaries does not operate in isolation. It sits within "
        "a constellation of established organizations:")

    pdf.bullet(
        " Global regenerative finance nonprofit. $800K+ raised, $370K+ "
        "deployed across 12+ bioregions. Provides fiscal infrastructure, "
        "donor networks, and philanthropic credibility.",
        bold_prefix="Kinship Earth (501c3) \u2014",
    )
    pdf.bullet(
        " Northeast permaculture action network. 50+ events, 40+ project "
        "sites, 1,000+ active members. Provides a ready-made pipeline of "
        "skilled volunteers, educators, and community members.",
        bold_prefix="Permatours (501c3) \u2014",
    )
    pdf.bullet(
        " Diggers Cooperative (compost), Birds Nest Builders (natural "
        "building co-op), Eco Phi (regenerative architecture), Mycelial Law "
        "(earth law), Micelio Media (film), Herbaria (herbalism & catering), "
        "and dozens more aligned producers and practitioners.",
        bold_prefix="Partner Network \u2014",
    )

    # ================================================================
    # PAGE 3 — EXECUTION, FINANCIALS, THE ASK
    # ================================================================
    pdf.add_page()
    pdf.section_title("Execution Plan, Financial Model, and the Ask")

    pdf.subsection_title("Upon Acquisition: The 90-Day Activation")
    pdf.body(
        "This is not a \"build it someday\" plan. Upon campus acquisition, "
        "the team executes immediately:")

    pdf.sub2_title("Days 1\u201330: Foundation")
    for b in [
        "Founding team moves on-site; key personnel occupy campus housing",
        "Legal structures finalized (Community Land Trust, pillar-specific "
        "trusts, stewardship agreements)",
        "Farm assessment: soil testing, existing agricultural infrastructure "
        "inventory, first-season crop planning",
        "Building audit: which campus facilities map to which pillar, what "
        "needs renovation vs. immediate activation",
        "Early membership and community engagement launch",
    ]:
        pdf.bullet(b)
    pdf.ln(3)

    pdf.sub2_title("Days 31\u201360: First Revenue")
    for b in [
        "Farm stand and community cafe open (using campus commercial kitchen "
        "and existing agricultural land)",
        "First retreat and workshop programming scheduled (using campus "
        "studios, residential halls, wellness spaces)",
        "Event venue bookings begin (weddings, conferences, festivals \u2014 "
        "campus auditoriums and outdoor spaces)",
        "Permatours activates volunteer network for initial work days, "
        "builds, and plantings on-site",
    ]:
        pdf.bullet(b)
    pdf.ln(3)

    pdf.sub2_title("Days 61\u201390: Community Formation")
    for b in [
        "First residents onboarded into cooperative living (converted "
        "campus housing)",
        "Governance structures activated (Anchor Circle, pillar-specific "
        "autonomous nodes, community agreements)",
        "Circular economy infrastructure launched (community utility token, "
        "voice governance tokens)",
        "Public storytelling and media production begins \u2014 documenting the "
        "transformation for fundraising and replication",
    ]:
        pdf.bullet(b)
    pdf.ln(5)

    # ── Financial Summary ───────────────────────────────────────────
    pdf.subsection_title("Financial Summary")

    pdf.draw_table(
        ["", "Year 1 (Conservative)", "Year 2", "Year 3 (At Maturity)"],
        [
            ["Farm & Education",      "$315K", "$600K", "$1M+"],
            ["Retreat & Healing Arts", "$570K", "$1M",   "$1.75M"],
            ["Event Venue",           "$310K", "$700K", "$1.16M"],
            ["Community Living",      "$195K", "$400K", "$580K"],
            ["Total Revenue",         "$1.4M", "$2.7M", "$4.5M+"],
        ],
        col_widths=[44, 40, 40, 46],
    )

    pdf.body(
        "Revenue is diversified across four independent pillars. No single "
        "pillar carries the model \u2014 if one has a slow season, three others "
        "continue generating. This is the resilience of a village economy "
        "versus a single-purpose business."
    )

    # ── Capital Strategy ────────────────────────────────────────────
    pdf.subsection_title("Capital Strategy")

    pdf.draw_table(
        ["Phase", "Target", "Timeline", "Purpose"],
        [
            ["Phase 1", "$10M", "End of 2026",
             "Campus acquisition, legal structuring, initial activation, "
             "first-year operations"],
            ["Phase 2", "$100M", "2028",
             "Full buildout, eco-home construction, expanded programming, "
             "infrastructure upgrades, open-source documentation"],
        ],
        col_widths=[24, 24, 30, 92],
    )

    pdf.body(
        "Capital sources: impact investment, philanthropic donations, "
        "community memberships, earned revenue, aligned partnerships, and "
        "government grants (USDA Beginning Farmer, Vermont Housing & "
        "Conservation Board, climate programs)."
    )

    # ================================================================
    # PAGE 4 — WHAT MAKES THIS DIFFERENT + THE ASK
    # ================================================================
    pdf.add_page()
    pdf.section_title("What Makes This Investment Different")

    differentiators = [
        ("1. Existing Infrastructure Eliminates the Biggest Risk.",
         "The #1 reason land-based community projects fail is the "
         "multi-year, multi-million-dollar buildout before any revenue "
         "flows. A university campus removes that barrier. We inherit "
         "decades of investment in buildings, utilities, and land \u2014 and "
         "activate them for their highest purpose."),
        ("2. The Team is Already Operating.",
         "This is not a first-time founder with a pitch deck. This is a "
         "team with years of shared work, $800K+ raised and deployed "
         "through established nonprofits, 50+ events produced, 40+ land "
         "projects served, and a living network of 2,200+ practitioners "
         "ready to show up. We are not asking for money to figure it out. "
         "We are asking for the asset so we can do what we already know "
         "how to do \u2014 at scale."),
        ("3. Non-Speculative Land Stewardship.",
         "The land goes into a Community Land Trust \u2014 permanently removed "
         "from market speculation. This is not a real estate play. This is "
         "a regenerative investment in a community asset that grows in "
         "value through stewardship, not extraction. For an investor who "
         "cares about legacy, this means the land serves people and ecology "
         "forever, not just until the next sale."),
        ("4. Community is the Product.",
         "Every pillar is designed around gathering people: farmers growing "
         "food together, healers practicing together, artists creating "
         "together, neighbors living together. Revenue comes from the "
         "natural activity of a thriving community \u2014 not from artificial "
         "demand or marketing gimmicks. For someone who loves building "
         "community, this is community as the entire business model."),
        ("5. Open-Source Blueprint.",
         "Every governance framework, financial model, and operational "
         "design will be documented and shared publicly. This is not just "
         "one village \u2014 it is the template for hundreds. Your investment "
         "doesn't end at one property line. It seeds a movement."),
    ]
    for title, desc in differentiators:
        pdf.set_font(FONT, "B", 11)
        pdf.set_text_color(*pdf.DARK)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.body(desc)
        pdf.ln(1)

    pdf.ln(4)
    pdf.section_title("The Ask")

    pdf.body(
        "We are seeking an aligned investor-partner to acquire a university "
        "campus in the Southern Vermont corridor (Brattleboro / Guilford / "
        "Putney) \u2014 or a comparable campus property with the right "
        "infrastructure \u2014 and place it into a Community Land Trust as the "
        "permanent home of Unified Sanctuaries."
    )
    pdf.body("This is an invitation for someone who:")
    for item in [
        "Understands that the best infrastructure in America is sitting "
        "empty while communities go without",
        "Knows from experience that farming is both a livelihood and a way "
        "of life worth protecting",
        "Believes that helping people and building community is not just "
        "good ethics \u2014 it is good economics",
        "Wants their capital to create something that outlasts them",
    ]:
        pdf.bullet(item)

    pdf.ln(8)
    pdf.highlight_block(
        "We have the team. We have the plan. We have the network. "
        "We have the track record. We need the land."
    )

    # closing
    pdf.ln(10)
    mid = pdf.w / 2
    pdf.set_draw_color(*pdf.GOLD)
    pdf.set_line_width(1)
    pdf.line(mid - 30, pdf.get_y(), mid + 30, pdf.get_y())
    pdf.ln(10)
    pdf.body_italic(
        "Contact: Syd Harvey Griffith  |  sydney.griffith123@gmail.com")
    pdf.body_italic(
        "Prepared February 2026  |  Unified Sanctuaries  |  "
        "Confidential \u2014 For Aligned Investors Only")

    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    import os
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Unified-Sanctuaries-Investor-Business-Plan.pdf",
    )
    build_pdf(out)
