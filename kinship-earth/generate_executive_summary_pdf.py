#!/usr/bin/env python3
"""
Generate a styled PDF of the Kinship Earth Executive Summary.
Design matches the Bioregional Flow Funding Playbook aesthetic:
  - Clean, professional layout
  - Earth-toned color palette (greens, warm grays)
  - Elegant typography
  - Consistent headers/footers with Kinship Earth branding
  - Mermaid diagrams rendered as styled HTML flow diagrams
"""

import os
import re
import markdown
from weasyprint import HTML, CSS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "EXECUTIVE-SUMMARY.md")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Kinship-Earth-Executive-Summary.pdf")

# ── CSS styling matching the Bioregional Flow Funding Playbook design ────────
STYLESHEET = """
@page {
    size: letter;
    margin: 0.85in 0.85in 1in 0.85in;

    @top-center {
        content: "Kinship Earth  |  Executive Summary";
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 8pt;
        color: #7a8a6e;
        letter-spacing: 1.5pt;
        text-transform: uppercase;
        border-bottom: 0.5pt solid #c5d1b8;
        padding-bottom: 6pt;
    }

    @bottom-center {
        content: counter(page);
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 9pt;
        color: #7a8a6e;
    }

    @bottom-right {
        content: "kinshipearth.org  |  flowfunding.org";
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 7pt;
        color: #a0a99a;
        letter-spacing: 0.5pt;
    }
}

@page :first {
    @top-center { content: none; }
}

/* ── Base ──────────────────────────────────────────────────── */

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: #2c2c2c;
    max-width: 100%;
}

/* ── Cover / Title Block ──────────────────────────────────── */

.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 2in;
}

.cover h1 {
    font-size: 28pt;
    font-weight: normal;
    color: #3d5a3a;
    letter-spacing: 1pt;
    line-height: 1.3;
    margin-bottom: 0.15in;
    border-bottom: none;
}

.cover .subtitle {
    font-size: 13pt;
    font-style: italic;
    color: #6b7c5e;
    margin-bottom: 0.5in;
}

.cover .org {
    font-size: 10pt;
    color: #7a8a6e;
    letter-spacing: 2pt;
    text-transform: uppercase;
}

.cover .divider {
    width: 60px;
    height: 1px;
    background: #b8c7a8;
    margin: 0.4in auto;
}

.cover p {
    text-align: center;
}

.cover .meta-line {
    font-size: 9pt;
    color: #999;
    margin-top: 0.08in;
}

/* ── Headings ─────────────────────────────────────────────── */

h1 {
    font-size: 20pt;
    font-weight: normal;
    color: #3d5a3a;
    letter-spacing: 0.5pt;
    margin-top: 0.4in;
    margin-bottom: 0.15in;
    padding-bottom: 5pt;
    border-bottom: 1.5pt solid #b8c7a8;
    page-break-after: avoid;
}

h2 {
    font-size: 15pt;
    font-weight: normal;
    color: #4a6d45;
    margin-top: 0.35in;
    margin-bottom: 0.12in;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    color: #4a6d45;
    margin-top: 0.25in;
    margin-bottom: 0.08in;
    page-break-after: avoid;
}

h4 {
    font-size: 11pt;
    font-weight: bold;
    color: #5a7a55;
    margin-top: 0.2in;
    margin-bottom: 0.06in;
    page-break-after: avoid;
}

/* ── Paragraphs & Lists ───────────────────────────────────── */

p {
    margin-bottom: 0.1in;
    text-align: left;
    orphans: 3;
    widows: 3;
}

ul, ol {
    margin-left: 0.25in;
    margin-bottom: 0.1in;
}

li {
    margin-bottom: 0.05in;
}

li p {
    margin-bottom: 0.03in;
}

/* ── Blockquotes ──────────────────────────────────────────── */

blockquote {
    border-left: 3pt solid #b8c7a8;
    margin: 0.2in 0 0.2in 0.15in;
    padding: 0.1in 0 0.1in 0.2in;
    color: #4a6d45;
    font-style: italic;
    background: #f4f7f1;
}

blockquote p {
    margin-bottom: 0.06in;
}

/* ── Horizontal Rules ─────────────────────────────────────── */

hr {
    border: none;
    border-top: 1pt solid #c5d1b8;
    margin: 0.25in 0;
}

/* ── Tables ───────────────────────────────────────────────── */

table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.15in 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead {
    background: #eaf0e4;
}

th {
    font-weight: bold;
    color: #3d5a3a;
    text-align: left;
    padding: 6pt 8pt;
    border-bottom: 1.5pt solid #b8c7a8;
}

td {
    padding: 5pt 8pt;
    border-bottom: 0.5pt solid #dde5d6;
    vertical-align: top;
}

tr:nth-child(even) {
    background: #f8faf6;
}

/* ── Links ────────────────────────────────────────────────── */

a {
    color: #4a6d45;
    text-decoration: none;
    border-bottom: 0.5pt dotted #7a8a6e;
}

/* ── Bold / Italic ────────────────────────────────────────── */

strong {
    color: #2c2c2c;
}

em {
    color: #4a4a4a;
}

/* ── Flow Diagram Boxes ──────────────────────────────────── */

.flow-diagram {
    margin: 0.15in 0;
    page-break-inside: avoid;
}

.flow-diagram-title {
    font-size: 9pt;
    font-weight: bold;
    color: #7a8a6e;
    text-transform: uppercase;
    letter-spacing: 1pt;
    margin-bottom: 0.1in;
    text-align: center;
}

/* Horizontal flow row (for the 4-step process & phases) */
.flow-row {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 6pt;
    margin-bottom: 8pt;
    flex-wrap: wrap;
}

.flow-box {
    flex: 0 1 auto;
    width: 145pt;
    border-radius: 6pt;
    padding: 10pt 8pt;
    text-align: center;
    font-size: 8.5pt;
    line-height: 1.4;
}

.flow-box .flow-num {
    font-size: 10pt;
    font-weight: bold;
    display: block;
    margin-bottom: 3pt;
}

.flow-box .flow-label {
    font-weight: bold;
    font-size: 9pt;
    display: block;
    margin-bottom: 4pt;
}

.flow-arrow {
    text-align: center;
    font-size: 14pt;
    color: #7a8a6e;
    padding: 0 2pt;
    align-self: center;
}

/* Color classes for flow boxes */
.flow-blue { background: #e3f2fd; border: 1pt solid #90caf9; color: #1565c0; }
.flow-green { background: #e8f5e9; border: 1pt solid #81c784; color: #2e7d32; }
.flow-orange { background: #fff3e0; border: 1pt solid #ffb74d; color: #e65100; }
.flow-purple { background: #f3e5f5; border: 1pt solid #ce93d8; color: #6a1b9a; }
.flow-teal { background: #e0f2f1; border: 1pt solid #80cbc4; color: #00695c; }
.flow-light-blue { background: #e3f2fd; border: 1pt solid #90caf9; color: #0d47a1; }
.flow-dark-blue { background: #bbdefb; border: 1pt solid #64b5f6; color: #0d47a1; }
.flow-light-green { background: #e8f5e9; border: 1pt solid #81c784; color: #2e7d32; }

/* Vertical flow (block layout — avoids weasyprint flex stretching) */
.flow-vertical {
    text-align: center;
}

.flow-vertical .flow-box {
    display: inline-block;
    width: 320pt;
    margin: 0 auto;
    text-align: center;
}

.flow-vertical .flow-arrow {
    display: block;
    text-align: center;
    font-size: 12pt;
    margin: 3pt 0;
}

.flow-vertical .flow-row {
    margin-bottom: 0;
}

/* Bioregion grid below capital flow */
.flow-region-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6pt;
    margin-top: 6pt;
}

.flow-region-box {
    border-radius: 4pt;
    padding: 6pt 10pt;
    text-align: center;
    font-size: 8.5pt;
    line-height: 1.3;
    width: 90pt;
}

/* Phase timeline */
.phase-row {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 8pt;
    margin: 0.15in 0;
}

.phase-box {
    flex: 0 1 auto;
    width: 180pt;
    border-radius: 6pt;
    padding: 10pt;
    font-size: 8.5pt;
    line-height: 1.4;
}

.phase-box .phase-title {
    font-weight: bold;
    font-size: 9.5pt;
    display: block;
    margin-bottom: 2pt;
}

.phase-box .phase-dates {
    font-style: italic;
    font-size: 8pt;
    display: block;
    margin-bottom: 5pt;
    opacity: 0.8;
}

.phase-arrow {
    align-self: center;
    font-size: 14pt;
    color: #7a8a6e;
}

/* Code blocks (hide mermaid source) */
pre {
    display: none;
}

code {
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background: #f0f4ec;
    padding: 1pt 3pt;
    border-radius: 2pt;
}
"""


def build_cover_page():
    """Generate the HTML cover page."""
    return """
    <div class="cover">
        <div class="divider"></div>
        <h1>Kinship Earth</h1>
        <p class="subtitle">Executive Summary</p>
        <div class="divider"></div>
        <p class="org">Private Foundation &middot; 501(c)(3)</p>
        <p class="meta-line">Flow Funding &mdash; Participatory, Trust-Based Grantmaking</p>
        <p class="meta-line" style="margin-top: 0.6in; color: #aaa;">kinshipearth.org &nbsp;|&nbsp; flowfunding.org</p>
        <p class="meta-line">Prepared March 2026</p>
    </div>
    """


def build_flow_funding_steps_diagram():
    """HTML replacement for the 'How It Works' mermaid flowchart."""
    return """
<div class="flow-diagram">
    <div class="flow-diagram-title">How Flow Funding Works</div>
    <div class="flow-row">
        <div class="flow-box flow-blue">
            <span class="flow-num">1</span>
            <span class="flow-label">Identify</span>
            Trusted community leaders via Flow Fund Advisors, Kinship Earth leadership, and existing Flow Funders
        </div>
        <div class="flow-arrow">&rarr;</div>
        <div class="flow-box flow-green">
            <span class="flow-num">2</span>
            <span class="flow-label">Deploy</span>
            Unrestricted funds; community leaders and organizing groups decide how capital moves
        </div>
        <div class="flow-arrow">&rarr;</div>
        <div class="flow-box flow-orange">
            <span class="flow-num">3</span>
            <span class="flow-label">Report</span>
            Lightweight, story-based accountability; no heavy compliance; minimal reporting
        </div>
        <div class="flow-arrow">&rarr;</div>
        <div class="flow-box flow-purple">
            <span class="flow-num">4</span>
            <span class="flow-label">Recommend</span>
            Flow Funders nominate next cohort when funding allows; cultivating a self-perpetuating network
        </div>
    </div>
</div>
"""


def build_capital_flow_diagram():
    """HTML replacement for the 'Capital Flow Architecture' mermaid flowchart."""
    return """
<div class="flow-diagram">
    <div class="flow-diagram-title">Capital Flow Architecture</div>
    <div style="text-align: center; margin-bottom: 3pt;">
        <div class="flow-box flow-light-blue" style="display: inline-block; width: 320pt;">
            <span class="flow-label">Donors</span>
            Foundations, Family Offices, DAFs, Individuals
        </div>
    </div>
    <div style="text-align: center; font-size: 12pt; color: #7a8a6e; margin: 3pt 0;">&darr; <span style="font-size: 8pt;">Philanthropic capital</span></div>
    <div style="text-align: center; margin-bottom: 3pt;">
        <div class="flow-box flow-blue" style="display: inline-block; width: 320pt;">
            <span class="flow-label">Kinship Earth</span>
            Private Foundation &middot; 501(c)(3)
        </div>
    </div>
    <div style="text-align: center; font-size: 12pt; color: #7a8a6e; margin: 3pt 0;">&darr; <span style="font-size: 8pt;">Unrestricted grants</span></div>
    <div style="text-align: center; margin-bottom: 3pt;">
        <div class="flow-box flow-dark-blue" style="display: inline-block; width: 320pt;">
            <span class="flow-label">Flow Funders</span>
            23 Flow Funders &middot; 12+ Bioregions Resourced
        </div>
    </div>
    <div class="flow-region-grid" style="margin-top: 6pt;">
        <div class="flow-region-box flow-light-green">Cascadia</div>
        <div class="flow-region-box flow-light-green">NE of Turtle Island</div>
        <div class="flow-region-box flow-light-green">Cloud Forest<br/>(Mexico)</div>
        <div class="flow-region-box flow-light-green">Montego Bay<br/>(Jamaica)</div>
        <div class="flow-region-box flow-light-green">Bioregions in<br/>Colombia</div>
        <div class="flow-region-box flow-light-green">East Africa</div>
    </div>
</div>
"""


def build_governance_diagram():
    """HTML replacement for the 'Governance Structure' mermaid flowchart."""
    return """
<div class="flow-diagram">
    <div class="flow-diagram-title">Governance Structure</div>
    <div class="flow-row" style="margin-bottom: 2pt;">
        <div class="flow-box flow-dark-blue">
            <span class="flow-label">Board Members</span>
            Governance Oversight
        </div>
        <div class="flow-box flow-blue">
            <span class="flow-label">Board of Advisors</span>
            Strategic Guidance
        </div>
    </div>
    <div style="text-align: center; font-size: 12pt; color: #7a8a6e; margin: 3pt 0;">&darr;</div>
    <div style="text-align: center; margin-bottom: 3pt;">
        <div class="flow-box flow-light-blue" style="display: inline-block; width: 320pt;">
            <span class="flow-label">Team</span>
            Operations &amp; Leadership
        </div>
    </div>
    <div style="text-align: center; font-size: 12pt; color: #7a8a6e; margin: 3pt 0;">&darr;</div>
    <div style="text-align: center; margin-bottom: 3pt;">
        <div class="flow-box flow-light-blue" style="display: inline-block; width: 320pt; background: #d6eaf8;">
            <span class="flow-label">Flow Fund Advisors, Kinship Earth Leadership, &amp; Existing Flow Funders</span>
            Identify Flow Funder Candidates
        </div>
    </div>
    <div style="text-align: center; font-size: 12pt; color: #7a8a6e; margin: 3pt 0;">&darr;</div>
    <div style="text-align: center;">
        <div class="flow-box flow-light-blue" style="display: inline-block; width: 320pt; background: #ebf5fb;">
            <span class="flow-label">Flow Funders</span>
            Deploy Funds &amp; Share Learnings as a Community of Practice
        </div>
    </div>
</div>
"""


def build_phases_diagram():
    """HTML replacement for the 'Development Phases' mermaid flowchart."""
    return """
<div class="flow-diagram">
    <div class="flow-diagram-title">Development Phases</div>
    <div class="phase-row">
        <div class="phase-box flow-light-blue">
            <span class="phase-title">Phase 1: Capital &amp; Cohort Continuity</span>
            <span class="phase-dates">Q4 2024 &ndash; present</span>
            Flow Funding to 3 Cohorts; Support Bioregional Groups; Educate Philanthropists
        </div>
        <div class="phase-arrow">&rarr;</div>
        <div class="phase-box flow-blue">
            <span class="phase-title">Phase 2: Education &amp; Field Building</span>
            <span class="phase-dates">Q1 2026 &ndash; Q4 2026</span>
            Publish Flow Funding Playbook; Renew Cohort 1 &amp; 2 Grants; Refine CoP for Cohort 3
        </div>
        <div class="phase-arrow">&rarr;</div>
        <div class="phase-box flow-blue" style="background: #90caf9; color: #0d47a1;">
            <span class="phase-title">Phase 3: Bioregional Scaling</span>
            <span class="phase-dates">Q4 2026 onwards</span>
            Supporting Autonomous Flow Funds; Legal + Educational + Relational Backbone
        </div>
    </div>
</div>
"""


# Map mermaid code blocks to their HTML replacements
MERMAID_REPLACEMENTS = [
    ("S1[", build_flow_funding_steps_diagram),      # How It Works
    ("DONORS[", build_capital_flow_diagram),          # Capital Flow Architecture
    ("BOARD[", build_governance_diagram),              # Governance Structure
    ("P1[", build_phases_diagram),                     # Development Phases
]


def replace_mermaid_blocks(md_text):
    """Replace mermaid code blocks with styled HTML diagrams."""
    # Find all mermaid code blocks
    mermaid_pattern = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
    blocks = list(mermaid_pattern.finditer(md_text))

    # Process in reverse order to preserve positions
    for match in reversed(blocks):
        block_content = match.group(1)
        replacement = ""

        for identifier, builder in MERMAID_REPLACEMENTS:
            if identifier in block_content:
                replacement = builder()
                break

        md_text = md_text[:match.start()] + replacement + md_text[match.end():]

    return md_text


def clean_markdown(md_text):
    """Clean up common markdown artifacts."""
    md_text = md_text.replace("\\-", "-")
    md_text = md_text.replace("\\*", "*")
    md_text = md_text.replace("\\~", "~")
    md_text = re.sub(r'\n{4,}', '\n\n\n', md_text)
    md_text = md_text.strip()
    return md_text


def md_to_styled_html(md_text):
    """Convert markdown to a full HTML document with cover page, styled diagrams, and branding."""
    # Replace mermaid blocks with HTML before markdown conversion
    md_text = replace_mermaid_blocks(md_text)

    # Split out the HTML diagram blocks before markdown processing
    html_blocks = []
    placeholder_prefix = "DIAGRAMPLACEHOLDER"

    def replace_with_placeholder(match):
        idx = len(html_blocks)
        html_blocks.append(match.group(0))
        return f"\n\n{placeholder_prefix}{idx}\n\n"

    # Extract HTML blocks (our flow diagrams) — match from opening to the final closing tag
    html_block_pattern = re.compile(r'<div class="flow-diagram">.*?</div>\n</div>', re.DOTALL)
    md_text = html_block_pattern.sub(replace_with_placeholder, md_text)

    # Remove the first H1 (title) since we have a cover page
    md_text = re.sub(r'^# Kinship Earth -- Executive Summary\s*\n', '', md_text)

    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'toc', 'smarty', 'sane_lists']
    )

    # Restore HTML diagram blocks
    for idx, block in enumerate(html_blocks):
        html_body = html_body.replace(f"<p>{placeholder_prefix}{idx}</p>", block)
        html_body = html_body.replace(f"{placeholder_prefix}{idx}", block)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Kinship Earth — Executive Summary</title>
</head>
<body>
{build_cover_page()}
{html_body}
</body>
</html>"""
    return full_html


def main():
    print(f"Reading: {INPUT_FILE}")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()

    md_text = clean_markdown(md_text)
    html_content = md_to_styled_html(md_text)

    print("Generating PDF...")
    html_doc = HTML(string=html_content, base_url=SCRIPT_DIR)
    css = CSS(string=STYLESHEET)
    html_doc.write_pdf(OUTPUT_FILE, stylesheets=[css])

    print(f"Done! PDF saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
