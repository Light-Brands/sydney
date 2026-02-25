#!/usr/bin/env python3
"""Convert the Bioregional Flow Funding Playbook from Markdown to PDF."""

import markdown
from weasyprint import HTML, CSS
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(SCRIPT_DIR, "BIOREGIONAL-FLOW-FUNDING-PLAYBOOK.md")
PDF_FILE = os.path.join(SCRIPT_DIR, "pdfs", "Bioregional-Flow-Funding-Playbook.pdf")

# Read markdown
with open(MD_FILE, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(
    md_content,
    extensions=["tables", "toc", "sane_lists", "smarty"],
)

# Wrap in full HTML with styling
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Bioregional Flow Funding Playbook</title>
</head>
<body>
{html_body}
</body>
</html>"""

# Professional CSS styling
css = CSS(string="""
@page {{
    size: letter;
    margin: 1in 0.85in;
    @top-center {{
        content: "The Bioregional Flow Funding Playbook";
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 8pt;
        color: #888;
        padding-bottom: 8pt;
        border-bottom: 0.5pt solid #ccc;
    }}
    @bottom-center {{
        content: "Kinship Earth  |  kinshipearth.org  |  flowfunding.org";
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 7.5pt;
        color: #888;
        padding-top: 8pt;
        border-top: 0.5pt solid #ccc;
    }}
    @bottom-right {{
        content: counter(page);
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 8pt;
        color: #888;
        padding-top: 8pt;
    }}
}}

@page :first {{
    @top-center {{
        content: none;
        border-bottom: none;
    }}
    @bottom-center {{
        content: none;
        border-top: none;
    }}
    @bottom-right {{
        content: none;
    }}
    margin-top: 2.5in;
}}

body {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #2a2a2a;
    max-width: 100%;
}}

h1 {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 26pt;
    color: #1a472a;
    text-align: center;
    margin-bottom: 0.3em;
    line-height: 1.2;
    page-break-after: avoid;
}}

h1 + p {{
    text-align: center;
    font-size: 13pt;
    color: #3a6b4a;
}}

h1 + p + p {{
    text-align: center;
    font-style: italic;
    color: #666;
    font-size: 10pt;
}}

h2 {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 17pt;
    color: #1a472a;
    border-bottom: 2pt solid #3a6b4a;
    padding-bottom: 6pt;
    margin-top: 36pt;
    margin-bottom: 14pt;
    page-break-after: avoid;
}}

h3 {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 13pt;
    color: #2d5a3d;
    margin-top: 22pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
}}

h4 {{
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    color: #3a6b4a;
    margin-top: 16pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}}

p {{
    margin-bottom: 10pt;
    text-align: justify;
    orphans: 3;
    widows: 3;
}}

a {{
    color: #2d5a3d;
    text-decoration: underline;
    text-decoration-color: #8ab89a;
}}

a:hover {{
    color: #1a472a;
}}

strong {{
    color: #1a3a24;
}}

em {{
    color: #444;
}}

blockquote {{
    border-left: 3pt solid #3a6b4a;
    margin: 18pt 0;
    padding: 12pt 20pt;
    background-color: #f4f9f5;
    font-style: italic;
    color: #3a5a42;
}}

blockquote p {{
    margin-bottom: 4pt;
}}

ul, ol {{
    margin-bottom: 12pt;
    padding-left: 24pt;
}}

li {{
    margin-bottom: 5pt;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16pt 0;
    font-size: 9.5pt;
    page-break-inside: auto;
}}

thead {{
    background-color: #1a472a;
    color: white;
}}

th {{
    padding: 10pt 12pt;
    text-align: left;
    font-weight: bold;
    font-size: 9.5pt;
}}

td {{
    padding: 9pt 12pt;
    border-bottom: 0.5pt solid #dde8df;
    vertical-align: top;
}}

tr:nth-child(even) {{
    background-color: #f7faf7;
}}

tr {{
    page-break-inside: avoid;
}}

hr {{
    border: none;
    border-top: 1pt solid #c5d8c8;
    margin: 28pt 0;
}}

code {{
    background-color: #f0f5f1;
    padding: 2pt 5pt;
    border-radius: 3pt;
    font-size: 9pt;
    font-family: 'Courier New', monospace;
}}
""")

# Generate PDF
html_doc = HTML(string=html_content)
html_doc.write_pdf(PDF_FILE, stylesheets=[css])

print(f"PDF generated: {PDF_FILE}")
