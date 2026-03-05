#!/usr/bin/env python3
"""Generate the Executive Summary PDF from markdown with proper table pagination."""

import re
import base64
import markdown
from weasyprint import HTML
from mermaid import Mermaid
from mermaid.graph import Graph

MD_FILE = "EXECUTIVE-SUMMARY.md"
PDF_FILE = "Kinship-Earth-Executive-Summary.pdf"

# Read markdown
with open(MD_FILE, "r") as f:
    md_content = f.read()


def render_mermaid_png(match):
    """Render a mermaid code block to an embedded PNG image."""
    mermaid_code = match.group(1).strip()
    try:
        graph = Graph("diagram", mermaid_code)
        m = Mermaid(graph)
        resp = m.img_response
        if resp.status_code == 200:
            b64 = base64.b64encode(resp.content).decode("utf-8")
            return (
                f'<div class="mermaid-diagram">'
                f'<img src="data:image/png;base64,{b64}" />'
                f'</div>'
            )
    except Exception as e:
        print(f"Warning: Failed to render mermaid diagram: {e}")
    return '<p><em>[Diagram failed to render]</em></p>'


# Replace mermaid code blocks with rendered PNGs
md_content = re.sub(
    r'```mermaid\n(.*?)```',
    render_mermaid_png,
    md_content,
    flags=re.DOTALL
)

# Convert markdown to HTML
html_body = markdown.markdown(md_content, extensions=['tables'])

# Wrap in full HTML with CSS for proper table pagination
html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: letter;
    margin: 1in 0.75in;
}}

body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222;
}}

h1 {{
    font-size: 20pt;
    color: #1565C0;
    border-bottom: 2px solid #1565C0;
    padding-bottom: 6pt;
    margin-top: 0;
}}

h2 {{
    font-size: 15pt;
    color: #1565C0;
    margin-top: 18pt;
    page-break-after: avoid;
}}

h3 {{
    font-size: 12pt;
    color: #333;
    margin-top: 14pt;
    page-break-after: avoid;
}}

p {{
    margin: 6pt 0;
}}

/* KEY: Prevent tables from splitting across pages */
table {{
    page-break-inside: avoid;
    border-collapse: collapse;
    width: 100%;
    margin: 10pt 0;
    font-size: 9.5pt;
}}

thead {{
    page-break-after: avoid;
}}

tr {{
    page-break-inside: avoid;
}}

th {{
    background-color: #1565C0;
    color: white;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: bold;
}}

td {{
    padding: 5pt 8pt;
    border-bottom: 1px solid #ddd;
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background-color: #f5f5f5;
}}

ul, ol {{
    margin: 6pt 0;
    padding-left: 20pt;
}}

li {{
    margin: 3pt 0;
}}

hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 14pt 0;
}}

blockquote {{
    border-left: 3px solid #1565C0;
    margin: 12pt 0;
    padding: 6pt 12pt;
    color: #555;
    font-style: italic;
}}

strong {{
    color: #111;
}}

a {{
    color: #1565C0;
    text-decoration: none;
}}

/* Prevent headings from being orphaned at bottom of page */
h2, h3 {{
    page-break-after: avoid;
}}

/* Keep section content together with its heading */
h2 + *, h3 + * {{
    page-break-before: avoid;
}}

/* Mermaid diagram styling */
.mermaid-diagram {{
    text-align: center;
    margin: 12pt 0;
    page-break-inside: avoid;
}}

.mermaid-diagram img {{
    max-width: 100%;
    height: auto;
}}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

# Generate PDF
HTML(string=html_doc).write_pdf(PDF_FILE)
print(f"Generated {PDF_FILE}")
