#!/usr/bin/env python3
"""
Generate styled PDFs from all markdown documents in the flow-funding-playbook folder.
Design matches the Bioregional Flow Funding Playbook aesthetic:
  - Clean, professional layout
  - Earth-toned color palette (greens, warm grays)
  - Elegant typography
  - Consistent headers/footers with Kinship Earth branding
"""

import os
import sys
import glob
import re
import markdown
from weasyprint import HTML, CSS

# ── Directory setup ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "pdfs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── CSS styling matching the Bioregional Flow Funding Playbook design ────────
STYLESHEET = """
@page {
    size: letter;
    margin: 1in 1in 1.2in 1in;

    @top-center {
        content: "Kinship Earth  |  Flow Funding";
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
    font-size: 11pt;
    line-height: 1.65;
    color: #2c2c2c;
    max-width: 100%;
}

/* ── Cover / Title Block ──────────────────────────────────── */

.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 2.5in;
}

.cover h1 {
    font-size: 26pt;
    font-weight: normal;
    color: #3d5a3a;
    letter-spacing: 1pt;
    line-height: 1.3;
    margin-bottom: 0.3in;
}

.cover .subtitle {
    font-size: 12pt;
    font-style: italic;
    color: #6b7c5e;
    margin-bottom: 0.6in;
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
    margin: 0.5in auto;
}

/* ── Headings ─────────────────────────────────────────────── */

h1 {
    font-size: 22pt;
    font-weight: normal;
    color: #3d5a3a;
    letter-spacing: 0.5pt;
    margin-top: 0.5in;
    margin-bottom: 0.2in;
    padding-bottom: 6pt;
    border-bottom: 1.5pt solid #b8c7a8;
    page-break-after: avoid;
}

h2 {
    font-size: 16pt;
    font-weight: normal;
    color: #4a6d45;
    margin-top: 0.4in;
    margin-bottom: 0.15in;
    page-break-after: avoid;
}

h3 {
    font-size: 13pt;
    font-weight: bold;
    color: #4a6d45;
    margin-top: 0.3in;
    margin-bottom: 0.1in;
    page-break-after: avoid;
}

h4 {
    font-size: 11.5pt;
    font-weight: bold;
    color: #5a7a55;
    margin-top: 0.25in;
    margin-bottom: 0.08in;
    page-break-after: avoid;
}

/* ── Paragraphs & Lists ───────────────────────────────────── */

p {
    margin-bottom: 0.12in;
    text-align: left;
    orphans: 3;
    widows: 3;
}

ul, ol {
    margin-left: 0.25in;
    margin-bottom: 0.12in;
}

li {
    margin-bottom: 0.06in;
}

li p {
    margin-bottom: 0.04in;
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
    margin: 0.3in 0;
}

/* ── Tables ───────────────────────────────────────────────── */

table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.2in 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

thead {
    background: #eaf0e4;
}

th {
    font-weight: bold;
    color: #3d5a3a;
    text-align: left;
    padding: 8pt 10pt;
    border-bottom: 1.5pt solid #b8c7a8;
}

td {
    padding: 6pt 10pt;
    border-bottom: 0.5pt solid #dde5d6;
    vertical-align: top;
}

tr:nth-child(even) {
    background: #f8faf6;
}

/* ── Code / Pre ───────────────────────────────────────────── */

code {
    font-family: 'Courier New', monospace;
    font-size: 9.5pt;
    background: #f0f4ec;
    padding: 1pt 4pt;
    border-radius: 2pt;
}

pre {
    background: #f0f4ec;
    padding: 0.15in;
    border-left: 3pt solid #b8c7a8;
    font-size: 9pt;
    line-height: 1.5;
    overflow-wrap: break-word;
    white-space: pre-wrap;
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

/* ── Signature blocks ─────────────────────────────────────── */

.signature-line {
    border-bottom: 1pt solid #2c2c2c;
    width: 250pt;
    display: inline-block;
    margin-top: 6pt;
}
"""

# ── Document metadata for clean titles and subtitles ─────────────────────────
# Maps filename stems to (clean_title, subtitle)
DOCUMENT_META = {
    "BIOREGIONAL-FLOW-FUNDING-PLAYBOOK": (
        "The Bioregional Flow Funding Playbook",
        "A Guide for Bioregional Communities Creating Their Own Flow Funds"
    ),
    "Bioregional Flow Funding Playbook": (
        "Bioregional Flow Funding Playbook",
        "Introduction, Origins & Templated Resources"
    ),
    "Kinship Earth Flow Funding Playbook 11_7": (
        "Kinship Earth Flow Funding Playbook",
        "Preface: Reimagining How Resources Flow"
    ),
    "Kinship Earth Core Agreements & Flow Funding Practices ": (
        "Core Agreements & Flow Funding Practices",
        "Co-created in Partnership with Our Flow Fund Advisors"
    ),
    "Kinship Earth Community of Practice Framework": (
        "Community of Practice Framework",
        "A Template for Bioregional Flow Funding Groups"
    ),
    "Kinship Earth Flow Fund _ Flow Funder Role & Responsibilities": (
        "Flow Funder Role & Responsibilities",
        "Welcome to Kinship Earth"
    ),
    "Kinship Earth Agreement with Flow Funder 4_3_25 (MAKE A COPY).docx": (
        "Flow Fund Agreement with Flow Funders",
        "Kinship Earth Flow Funder Agreement Template"
    ),
    "Criteria & Process for Identifying & Selecting Flow Funders": (
        "Criteria & Process for Identifying & Selecting Flow Funders",
        "A Guide for Bioregional Flow Funding Groups"
    ),
    "Flowing Funds from Individual to Individual": (
        "Flowing Funds from Individual to Individual",
        "Tax Considerations for Individual-to-Individual Giving in the U.S."
    ),
    "How to Tell a Flow Funding Story_ The Journey of Impact": (
        "How to Tell a Flow Funding Story",
        "The Journey of Impact"
    ),
    "Form for those who want to contribute to playbook _  Kinship Earth & Partners' Bioregional Flow Funding Playbook & Resource Library": (
        "Playbook Contribution Form",
        "Bioregional Flow Funding Playbook & Resource Library"
    ),
    "What If You Don\u2019t Have 501(c)(3) Status Yet": (
        "What If You Don\u2019t Have 501(c)(3) Status Yet?",
        "Fiscal Sponsorship as an Option"
    ),
    "Kinship Earth Flow Funder Onboarding Form Questions": (
        "Flow Funder Onboarding Form",
        "Kinship Earth Onboarding Questions"
    ),
    "Kinship Earth reporting form questions": (
        "Flow Funding Disbursement & Reporting Form",
        "Kinship Earth Reporting Questions & Requests"
    ),
    "NE Bioregional Activation Series _ 2_10_26  - for Su (1)": (
        "Bridging Bioregional Wisdom in the Northeast of Turtle Island",
        "A Co-Created Bioregional Activation Series"
    ),
    "\U0001f310 Insights_ Deploying Funds Domestically in the U": (
        "Insights: Deploying Funds Domestically vs. Internationally",
        "For U.S.-Based Flow Funds"
    ),
}


def clean_markdown(md_text):
    """Clean up common markdown artifacts from Google Docs exports."""
    # Remove escaped special chars that aren't needed
    md_text = md_text.replace("\\-", "-")
    md_text = md_text.replace("\\*", "*")
    md_text = md_text.replace("\\~", "~")
    # Clean up multiple consecutive blank lines
    md_text = re.sub(r'\n{4,}', '\n\n\n', md_text)
    # Remove leading/trailing whitespace
    md_text = md_text.strip()
    return md_text


def build_cover_page(title, subtitle):
    """Generate the HTML cover page block."""
    return f"""
    <div class="cover">
        <div class="divider"></div>
        <h1>{title}</h1>
        <p class="subtitle">{subtitle}</p>
        <div class="divider"></div>
        <p class="org">Kinship Earth</p>
        <p class="subtitle">Published Q1 2026</p>
    </div>
    """


def md_to_styled_html(md_text, title, subtitle):
    """Convert markdown to a full HTML document with cover page and styling."""
    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'toc', 'smarty', 'sane_lists']
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
</head>
<body>
{build_cover_page(title, subtitle)}
{html_body}
</body>
</html>"""
    return full_html


def generate_pdf(md_path, output_path, title, subtitle):
    """Generate a PDF from a markdown file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    md_text = clean_markdown(md_text)
    html_content = md_to_styled_html(md_text, title, subtitle)

    html_doc = HTML(string=html_content, base_url=SCRIPT_DIR)
    css = CSS(string=STYLESHEET)
    html_doc.write_pdf(output_path, stylesheets=[css])


def get_clean_filename(stem):
    """Generate a clean PDF filename from the original stem."""
    # Map to cleaner names
    name_map = {
        "BIOREGIONAL-FLOW-FUNDING-PLAYBOOK": "Bioregional-Flow-Funding-Playbook",
        "Bioregional Flow Funding Playbook": "Bioregional-Flow-Funding-Playbook-Overview",
        "Kinship Earth Flow Funding Playbook 11_7": "Flow-Funding-Playbook-Preface",
        "Kinship Earth Core Agreements & Flow Funding Practices ": "Core-Agreements-and-Flow-Funding-Practices",
        "Kinship Earth Community of Practice Framework": "Community-of-Practice-Framework",
        "Kinship Earth Flow Fund _ Flow Funder Role & Responsibilities": "Flow-Funder-Role-and-Responsibilities",
        "Kinship Earth Agreement with Flow Funder 4_3_25 (MAKE A COPY).docx": "Flow-Funder-Agreement-Template",
        "Criteria & Process for Identifying & Selecting Flow Funders": "Criteria-for-Selecting-Flow-Funders",
        "Flowing Funds from Individual to Individual": "Individual-to-Individual-Giving",
        "How to Tell a Flow Funding Story_ The Journey of Impact": "How-to-Tell-a-Flow-Funding-Story",
        "Form for those who want to contribute to playbook _  Kinship Earth & Partners' Bioregional Flow Funding Playbook & Resource Library": "Playbook-Contribution-Form",
        "What If You Don\u2019t Have 501(c)(3) Status Yet": "Fiscal-Sponsorship-Without-501c3",
        "Kinship Earth Flow Funder Onboarding Form Questions": "Flow-Funder-Onboarding-Form",
        "Kinship Earth reporting form questions": "Disbursement-and-Reporting-Form",
        "NE Bioregional Activation Series _ 2_10_26  - for Su (1)": "NE-Bioregional-Activation-Series",
        "\U0001f310 Insights_ Deploying Funds Domestically in the U": "Insights-Domestic-vs-International-Funding",
    }
    return name_map.get(stem, stem.replace(" ", "-").replace("&", "and"))


def main():
    md_files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.md")))

    if not md_files:
        print("No markdown files found.")
        sys.exit(1)

    print(f"Found {len(md_files)} markdown files. Generating PDFs...\n")

    for md_path in md_files:
        basename = os.path.basename(md_path)
        stem = os.path.splitext(basename)[0]

        # Skip hidden files
        if stem.startswith('.'):
            continue

        meta = DOCUMENT_META.get(stem)
        if meta:
            title, subtitle = meta
        else:
            title = stem.replace("_", " ").replace("-", " ").title()
            subtitle = "Kinship Earth Flow Funding Resource"

        clean_name = get_clean_filename(stem)
        output_path = os.path.join(OUTPUT_DIR, f"{clean_name}.pdf")

        print(f"  Converting: {basename}")
        print(f"       Title: {title}")
        print(f"      Output: {os.path.basename(output_path)}")

        try:
            generate_pdf(md_path, output_path, title, subtitle)
            print(f"          OK\n")
        except Exception as e:
            print(f"       ERROR: {e}\n")

    print(f"Done! PDFs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
