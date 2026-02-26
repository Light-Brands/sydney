#!/usr/bin/env python3
"""Generate a PDF of the Unified Sanctuaries Executive Summary."""

from fpdf import FPDF
import re
import os

# --- Color palette ---
BROWN = (141, 110, 99)
DARK_BROWN = (93, 64, 55)
TEAL = (0, 121, 107)
GREEN = (165, 214, 167)
PURPLE = (206, 147, 216)
YELLOW = (255, 224, 130)
BLUE = (144, 202, 249)
RED = (239, 83, 80)
WHITE = (255, 255, 255)
BLACK = (33, 33, 33)
GRAY = (100, 100, 100)
TABLE_HEADER_BG = (93, 64, 55)
TABLE_ROW_ALT = (245, 241, 237)


class ExecutiveSummaryPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*GRAY)
            self.cell(0, 8, "Unified Sanctuaries  |  Executive Summary  |  February 2026", align="C")
            self.ln(6)

    def footer(self):
        self.set_y(-18)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*TEAL)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*TEAL)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def subsection_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*DARK_BROWN)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bold_label_text(self, label, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DARK_BROWN)
        self.write(5.5, label + " ")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        x = self.get_x()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(x + indent)
        # Write bullet character
        self.write(5.5, "-  ")
        # Parse bold segments
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", 10)
                self.write(5.5, part[2:-2])
            else:
                self.set_font("Helvetica", "", 10)
                self.write(5.5, part)
        self.ln(7)

    def numbered_item(self, number, text):
        x = self.get_x()
        self.set_x(x + 5)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEAL)
        self.write(5.5, f"{number}. ")
        # Parse bold segments
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(*DARK_BROWN)
                self.write(5.5, part[2:-2])
            else:
                self.set_font("Helvetica", "", 10)
                self.set_text_color(*BLACK)
                self.write(5.5, part)
        self.ln(7)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            avail = self.w - self.l_margin - self.r_margin
            col_widths = [avail / len(headers)] * len(headers)

        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*TABLE_HEADER_BG)
        self.set_text_color(*WHITE)
        self.set_draw_color(180, 180, 180)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 9, h, border=1, fill=True, align="C")
        self.ln()

        # Data rows
        self.set_text_color(*BLACK)
        for r_idx, row in enumerate(rows):
            if r_idx % 2 == 1:
                self.set_fill_color(*TABLE_ROW_ALT)
            else:
                self.set_fill_color(*WHITE)

            # Calculate needed height
            max_lines = 1
            for i, cell_text in enumerate(row):
                lines = self.multi_cell(col_widths[i], 5.5, cell_text, dry_run=True, output="LINES")
                max_lines = max(max_lines, len(lines))
            row_h = max(9, max_lines * 5.5 + 3)

            x_start = self.get_x()
            y_start = self.get_y()

            if y_start + row_h > self.h - 30:
                self.add_page()
                y_start = self.get_y()
                x_start = self.get_x()

            fill_color = TABLE_ROW_ALT if r_idx % 2 == 1 else WHITE
            for i, cell_text in enumerate(row):
                cx = x_start + sum(col_widths[:i])
                self.set_xy(cx, y_start)
                # Background
                self.set_fill_color(*fill_color)
                self.rect(cx, y_start, col_widths[i], row_h, style="DF")
                # Text
                self.set_xy(cx + 2, y_start + 1.5)
                is_first_col = (i == 0)
                self.set_font("Helvetica", "B" if is_first_col else "", 9)
                self.set_text_color(*BLACK)
                self.multi_cell(col_widths[i] - 4, 5.5, cell_text)

            self.set_xy(x_start, y_start + row_h)
        self.ln(4)

    def pillar_box(self, title, description, revenue, color):
        if self.get_y() > self.h - 45:
            self.add_page()
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin

        # Colored left bar + light background
        self.set_fill_color(*color)
        self.rect(x, self.get_y(), 4, 24, style="F")
        bg = tuple(min(255, int(c * 0.3 + 255 * 0.7)) for c in color)
        self.set_fill_color(*bg)
        self.rect(x + 4, self.get_y(), w - 4, 24, style="F")

        y_box = self.get_y()
        self.set_xy(x + 8, y_box + 2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DARK_BROWN)
        self.cell(w - 12, 6, title)

        self.set_xy(x + 8, y_box + 9)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BLACK)
        self.multi_cell(w - 12, 4.5, description)

        self.set_xy(x + 8, y_box + 18)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEAL)
        self.cell(w - 12, 5, f"Annual Revenue Potential: {revenue}")
        self.set_text_color(*BLACK)
        self.set_y(y_box + 27)

    def phase_box(self, title, subtitle, items, fill_color, text_white=False):
        if self.get_y() > self.h - 55:
            self.add_page()
        x = self.l_margin
        w = self.w - self.l_margin - self.r_margin

        # Title bar
        self.set_fill_color(*fill_color)
        self.rect(x, self.get_y(), w, 10, style="F")
        self.set_xy(x + 4, self.get_y() + 2)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*(WHITE if text_white else BLACK))
        self.cell(0, 6, title)
        self.ln(7)
        self.set_x(x + 4)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*(WHITE if text_white else GRAY))
        self.cell(0, 4, subtitle)
        self.set_text_color(*BLACK)
        self.ln(7)

        for item in items:
            self.set_x(x + 8)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(*BLACK)
            self.cell(4, 5, "-")
            self.multi_cell(w - 14, 5, item)
            self.ln(0.5)
        self.ln(4)


def build_pdf():
    pdf = ExecutiveSummaryPDF()
    pdf.alias_nb_pages()
    pdf.set_margins(20, 20, 20)

    # ===== COVER PAGE =====
    pdf.add_page()
    pdf.ln(45)
    pdf.set_font("Helvetica", "B", 34)
    pdf.set_text_color(*DARK_BROWN)
    pdf.cell(0, 15, "Unified Sanctuaries", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Decorative line
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(1.2)
    mid = pdf.w / 2
    pdf.line(mid - 45, pdf.get_y(), mid + 45, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 10, "Executive Summary", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(12)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*DARK_BROWN)
    pdf.cell(0, 8, "Land-Based Regenerative Village", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Southern Vermont", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 8, "Prepared: February 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, "Contact: sydney.griffith123@gmail.com", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*BROWN)
    pdf.cell(0, 6, "Current Phase: Searching for Land, Planning", align="C", new_x="LMARGIN", new_y="NEXT")

    # ===== OVERVIEW =====
    pdf.add_page()
    pdf.section_title("Overview")
    pdf.body_text(
        "Unified Sanctuaries is a land-based regenerative community planned for Southern Vermont "
        "(Brattleboro / Guilford / Putney corridor) that integrates permaculture farming, healing arts, "
        "cultural programming, and cooperative living into a single, self-sustaining village. Conceived "
        "as a living laboratory for regenerative development, the project operates at the intersection "
        "of ecological stewardship, community economics, and cultural innovation. It is designed from "
        "the ground up as an open-source blueprint -- every governance framework, financial model, and "
        "operational design will be publicly shared so that communities worldwide can learn from and "
        "adapt the model per their own unique use case."
    )

    # ===== MISSION & VISION =====
    pdf.section_title("Mission & Vision")
    pdf.bold_label_text(
        "Mission:",
        "To establish a thriving, multi-pillar sanctuary that regenerates land, culture, and "
        "livelihoods; hosts aligned businesses, residents, and gatherings; and demonstrates a viable "
        "alternative to extractive real estate development."
    )
    pdf.bold_label_text(
        "Vision:",
        "Unified Sanctuaries is an experimental hub for learning -- a living lab and museum exploring "
        "healing approaches through permaculture, healing arts, community living, and education. It aims "
        "to serve as a regenerative model of village-scale living rooted in equity, Indigenous wisdom, and "
        "ecological stewardship -- and to catalyze a global network of similar sanctuaries."
    )

    # ===== THE FOUR PILLARS =====
    pdf.section_title("The Four Pillars")
    pdf.body_text(
        "The community is organized around four interdependent platforms, each operating with internal "
        "autonomy while sharing infrastructure, governance, and economic systems."
    )
    pdf.ln(2)

    pdf.pillar_box(
        "1. Permaculture Farm & Education Center",
        "Regenerative agriculture, farm stand, a community cafe, forest school programming, "
        "agritourism / you pick programs, and hands-on education. This pillar anchors the land "
        "ethic of the project.",
        "$315K -- $1M+",
        (102, 187, 106)  # green
    )
    pdf.pillar_box(
        "2. Retreat & Healing Arts Center + Bathhouse",
        "Immersive retreats, healing arts, somatic therapy, herbalism, a spa/bathhouse, a campground, "
        "a makerspace for crafts and design, and dwellings to stay overnight.",
        "$570K -- $1.75M",
        (171, 71, 188)  # purple
    )
    pdf.pillar_box(
        "3. Event Venue + Innovation Hall",
        "Festivals, concerts, weddings, markets, conferences, knowledge-sharing gatherings, and "
        "AV/multimedia production. Positions the sanctuary as a cultural and economic hub.",
        "$310K -- $1.16M",
        (255, 193, 7)  # amber
    )
    pdf.pillar_box(
        "4. Community Living / Regenerative Neighborhood",
        "Eco-homes, tiny dwellings, shared stewardship, and cooperative living for 20+ households. "
        "Residents form the stable social fabric that sustains all other pillars.",
        "$195K -- $580K",
        (66, 165, 245)  # blue
    )
    pdf.ln(2)

    # Combined revenue highlight
    x = pdf.l_margin
    w = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.set_fill_color(*RED)
    pdf.rect(x, pdf.get_y(), w, 13, style="F")
    pdf.set_xy(x, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*WHITE)
    pdf.cell(w, 7, "Combined Annual Revenue Potential: $1.4M -- $4.5M+ (Year 1-3, at maturity)", align="C")
    pdf.set_text_color(*BLACK)
    pdf.ln(18)

    # ===== CAPITAL STRATEGY =====
    pdf.section_title("Capital Strategy & Financial Targets")
    pdf.add_table(
        ["Milestone", "Target", "Timeline"],
        [
            ["Seed / Phase 1 Capital Raise", "$1,000,000", "End of 2026"],
            ["Growth / Phase 2+", "$10,000,000", "2027"],
            ["Mature / Phase 3+", "$100,000,000", "2029"],
        ],
        [70, 50, 50]
    )
    pdf.body_text(
        "Capital sources include philanthropic donations, impact investment, earned revenue, community "
        "memberships, and aligned partnerships. The project is actively engaging donors and impact "
        "investors during the current pre-acquisition phase."
    )

    # ===== ECONOMIC MODEL =====
    pdf.section_title("Economic Model")
    pdf.body_text(
        "Unified Sanctuaries employs a circular internal economy designed to keep value local and "
        "reward contribution over capital:"
    )
    pdf.bullet("**Utility Token:** A community currency exchangeable for goods and services within the ecosystem -- food, retreat sessions, event access, housing credits, and more.")
    pdf.bullet("**Voice Token (Governance):** Earned through participation and stewardship, granting decision-making weight in community governance. Contribution, not capital, determines influence.")
    pdf.bullet("**Trust Units:** Earned through infrastructure development and improvements to the land. Trust units can be liquidated upon exit, ensuring that contributors build tangible equity through their work.")
    pdf.bullet("**Non-Speculative Land Stewardship:** Land is held in a Trust, removing it from market speculation and ensuring permanent community stewardship.")
    pdf.ln(1)
    pdf.body_text(
        "Each pillar autonomously structures its own way of operating and governing itself, including "
        "its compensation and reward mechanisms while participating in the shared economic infrastructure "
        "of Unified Sanctuaries."
    )

    # ===== GOVERNANCE STRUCTURE =====
    pdf.section_title("Governance Structure")
    pdf.body_text(
        "Unified Sanctuaries blends sociocracy and holacracy principles into a consent-based, "
        "rotating governance model:"
    )
    pdf.bullet("**Anchor Circle (Council):** The central governance body that guides interconnected autonomous platforms, maintains shared infrastructure, upholds core values, and stewards the economic systems.")
    pdf.bullet("**Autonomous Nodes:** Each of the four pillars operates as a self-governing unit with its own internal decision-making, compensation structures, and operational authority -- while remaining accountable to the shared governance framework.")
    pdf.bullet("**Consent-Based Decision-Making:** Decisions are made through consent rather than consensus or majority rule, ensuring that no one is overruled while maintaining operational agility.")
    pdf.bullet("**Rotating Leadership:** Governance roles rotate to distribute power and develop leadership capacity across the community.")

    # ===== LEGAL & ENTITY STRUCTURE =====
    pdf.section_title("Legal & Entity Structure")
    pdf.bullet("**Unified Sanctuaries Land Trust:** Owns and stewards the land in perpetuity, keeping it outside market speculation. Its role is asset protection and long-term stewardship, not operations.")
    pdf.ln(1)
    pdf.subsection_title("Pillar Trusts")
    pdf.body_text("Each core pillar operates through its own trust:")
    for trust in ["Retreat & Healing Arts Trust", "Event Venue Trust", "Farm Trust", "Community Living Trust"]:
        pdf.set_x(pdf.l_margin + 15)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*BLACK)
        pdf.cell(0, 6, "-  " + trust, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.body_text("Each pillar trust has an agreement with the Land Trust and governs activities within its domain.")
    pdf.bullet("**Businesses & Partnerships:** Existing businesses can partner with the relevant pillar trust through agreements, while new ventures may be created within a pillar trust. Businesses do not need to be owned by a trust; alignment happens through contracts.")
    pdf.bullet("**Anchor / Stewardship Layer:** A coordinating trust stewards pooled funds and supports shared infrastructure across pillars while maintaining autonomy between trusts.")
    pdf.ln(1)
    pdf.body_text(
        "Pooled funds are shared resources contributed by businesses, members, and programs into a common "
        "stewardship pool -- held by the Anchor Circle / Trust -- to support land stewardship, shared "
        "infrastructure, and ecosystem-wide needs rather than any single pillar. They provide continuity "
        "and coordination without controlling individual trusts or enterprises."
    )

    # ===== DEVELOPMENT PHASES =====
    pdf.section_title("Development Phases")
    pdf.phase_box(
        "Phase 1 (Present - Q4 2026)", "Land & Foundation",
        [
            "Identify and secure the right property in Southern Vermont",
            "Establish legal, governance, and stewardship structures",
            "Invite early members and anchor contributors",
            "Refine governance frameworks and community agreements",
            "Engage donors and impact investors for the $1M raise",
        ],
        (239, 235, 233), text_white=False
    )
    pdf.phase_box(
        "Phase 2 (Q1 2027 - Q4 2028)", "Build & Activate",
        [
            "Develop core infrastructure: housing (10+ eco-homes), farm systems, gathering spaces, bathhouse, retreat facilities, and event venue",
            "Onboard residents and mission-aligned businesses",
            "Host retreats, residencies, activations, festivals, and educational programming",
            "Launch the circular economy and scale revenue across all four pillars",
            "$10M raise",
        ],
        BROWN, text_white=True
    )
    pdf.phase_box(
        "Phase 3 (Q1 2029 onward)", "Blueprint & Network",
        [
            "20+ total eco-homes built",
            "Document all learnings -- governance models, financial systems, construction methods, community processes",
            "Publish the open-source blueprint for global replication",
            "Support the emergence of additional sanctuaries in other bioregions",
            "Serve as a hub within larger bioregional and global regenerative ecosystems",
            "$100M raise",
        ],
        DARK_BROWN, text_white=True
    )

    # ===== ECOSYSTEM & STRATEGIC PARTNERSHIPS =====
    pdf.section_title("Ecosystem & Strategic Partnerships")
    pdf.body_text(
        "Unified Sanctuaries is one node in a broader ecosystem of regenerative projects and partners:"
    )
    pdf.add_table(
        ["Partner Entity", "Relationship"],
        [
            ["Permatours", "NE permaculture action and education network"],
            ["Diggers Cooperative", "Compost co-op"],
            ["Birds Nest Builders", "Natural builder co-op"],
            ["Micelio Media", "Film maker, documentarian"],
            ["Mycelial Law", "Earth law firm, serving life and living systems"],
            ["Eco Phi", "Regenerative architecture firm"],
            ["Light Brands", "Tech development"],
            ["Herbaria", "Herbalism, retreats, and gourmet catering"],
            ["Pinky Toe Chai", "Tea blend producer"],
            ["Regen Civics", "Network of aligned ecovillages"],
            ["SEEDS", "Global ecosystem of regenerators focused on systems change, including community currencies"],
        ],
        [55, 115]
    )
    pdf.body_text(
        "And a plethora of aligned producers and service providers who have participated in "
        "Permatours events, and beyond."
    )

    # ===== PHASE 1 COLLABORATORS =====
    pdf.section_title("Phase 1 Collaborators")
    pdf.add_table(
        ["Name", "Core Expertise"],
        [
            ["Syd Harvey Griffith", "Executive Director of Kinship Earth, co-founder of Permatours, systems designer, capital strategist, community organizer"],
            ["Lynney Rey", "Farm operations, cafe, herbalism, forest school, performing / visual / healing arts"],
            ["Eslerh Oreste", "Film, multimedia, ritual theater, performing / healing arts"],
            ["Fuego Gale", "Accounting, financial operations, festival production, membership sales"],
            ["Josie Watson", "Earth lawyer, governance designer, playwright, performing / healing arts"],
            ["Scotty Guzman", "Soil scientist, compost specialist, nature builder, engineer, acro yogi clown"],
        ],
        [45, 125]
    )

    # ===== HOW TO GET INVOLVED =====
    pdf.section_title("How to Get Involved")
    pdf.add_table(
        ["Pathway", "Description"],
        [
            ["Donate", "Philanthropic contributions to support pre-acquisition operations and planning"],
            ["Invest", "Impact investment aligned with the $1M (2026), $10M (2027), and $100M (2029) capital raises"],
            ["Live On-Site", "Apply to become a resident in the regenerative neighborhood (20+ homes)"],
            ["Host Your Business", "Apply to operate a mission-aligned business within the sanctuary ecosystem"],
            ["Become a Member", "Purchase early membership to secure a stake in the community and its governance"],
            ["Share Skills & Network", "Contribute expertise, professional connections, or labor/skills exchange"],
            ["Scout Property", "Help identify and evaluate the right land in Southern Vermont"],
        ],
        [45, 125]
    )

    # ===== WHAT MAKES US UNIQUE =====
    pdf.section_title("What Makes Unified Sanctuaries Unique")
    unique_items = [
        ("Non-Speculative Land Model:", "Property held in trust, permanently removed from market speculation."),
        ("Governance earned through contribution:", "Stewardship and participation determine governance power."),
        ("Circular Internal Economy:", "Community utility currency and governance tokens keep value local and reward engagement."),
        ("Open-Source Blueprint:", "Every system -- governance, finance, construction, community process -- is documented and shared for global replication."),
        ("Multi-Revenue Resilience:", "Four distinct but interconnected revenue pillars reduce dependence on any single income stream."),
        ("Consent-Based Governance:", "Sociocratic/holacratic hybrid model with rotating leadership and autonomous nodes."),
        ("Ecosystem Integration:", "Connected to a local and global network of aligned organizations."),
        ("Deep Team Expertise:", "A founding team with demonstrated experience increasing the capacity of 50+ land-based projects through permaculture action and natural building workshops, practicing regenerative finance, community organizing, and participating in cooperative governance structures."),
    ]
    for i, (label, desc) in enumerate(unique_items, 1):
        pdf.numbered_item(i, f"**{label}** {desc}")

    # ===== KEY RISKS =====
    pdf.section_title("Key Risks & Open Questions")
    pdf.bullet("**Land Acquisition:** The right property has not yet been secured. Location, price, zoning, and condition will shape timelines and costs.")
    pdf.bullet("**Capital Raise Execution:** Achieving $1M by end of 2026, $10M by 2027, and $100M by 2028 requires aggressive fundraising across philanthropy and impact investment.")
    pdf.bullet("**Entity & Governance Structuring:** Trusts and governance structure in process of becoming established. Practicing consent-based governance will require careful onboarding and conflict resolution systems.")
    pdf.bullet("**Pre-Land Momentum:** Maintaining community energy and investor confidence during acquisition phase requires creative interim programming.")
    pdf.bullet("**Regulatory & Zoning:** Vermont land use, housing, and agricultural regulations will shape what can be built and how quickly.")

    # ===== SUMMARY =====
    pdf.section_title("Summary")
    pdf.body_text(
        "Unified Sanctuaries represents an ambitious and deeply considered approach to regenerative "
        "community development. With a proven founding team, a multi-pillar revenue model projecting "
        "$1.4M-$4.5M+ at maturity, a circular economy designed to keep value local, and a governance "
        "structure that distributes power through contribution rather than capital, the project is "
        "positioned to become both a thriving community and a replicable blueprint for regenerative "
        "villages worldwide. The immediate priorities are securing land in Southern Vermont, closing "
        "the Phase 1 capital raise of $1M, and building the founding community - while documenting "
        "processes and learnings for the communities that follow."
    )

    # Closing
    pdf.ln(8)
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.6)
    mid = pdf.w / 2
    pdf.line(mid - 35, pdf.get_y(), mid + 35, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 6, "Prepared February 2026  |  Unified Sanctuaries  |  Southern Vermont", align="C")

    # Output
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "Unified-Sanctuaries-Executive-Summary.pdf")
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf()
