const fs = require("fs");
const path = require("path");
const MarkdownIt = require("markdown-it");
const { chromium } = require("playwright");

const md = new MarkdownIt({
  html: true,
  typographer: true,
});

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&display=swap');

@page {
  size: letter;
  margin: 0.85in 0.75in 1in 0.75in;

  @bottom-center {
    content: counter(page);
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    color: #8a8a8a;
  }
}

@page:first {
  margin-top: 0;
  @bottom-center { content: none; }
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 10.5px;
  line-height: 1.65;
  color: #1a1a2e;
  -webkit-font-smoothing: antialiased;
}

/* ── Cover Page ── */
.cover-page {
  page-break-after: always;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  padding: 2in 1in;
  background: linear-gradient(165deg, #f8faf9 0%, #eef5f2 40%, #e8f0ec 100%);
}

.cover-page .logo-mark {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2d6a4f 0%, #40916c 50%, #52b788 100%);
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.25);
}

.cover-page .logo-mark span {
  font-size: 32px;
  color: white;
  font-weight: 700;
  font-family: 'Source Serif 4', Georgia, serif;
}

.cover-page h1 {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1.2;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.cover-page .subtitle {
  font-size: 15px;
  font-weight: 400;
  color: #40916c;
  margin-bottom: 40px;
  letter-spacing: 0.5px;
}

.cover-page .tagline {
  font-family: 'Source Serif 4', Georgia, serif;
  font-style: italic;
  font-size: 13px;
  color: #555;
  max-width: 420px;
  line-height: 1.6;
  margin-bottom: 48px;
}

.cover-page .meta-info {
  font-size: 9.5px;
  color: #777;
  line-height: 1.8;
}

.cover-page .meta-info strong {
  color: #444;
  font-weight: 600;
}

.cover-divider {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #2d6a4f, #52b788);
  margin: 24px auto;
  border: none;
}

/* ── Typography ── */
h1 {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-top: 36px;
  margin-bottom: 16px;
  letter-spacing: -0.3px;
  page-break-after: avoid;
}

h2 {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 18px;
  font-weight: 600;
  color: #2d6a4f;
  margin-top: 32px;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1.5px solid #d8e8df;
  page-break-after: avoid;
}

h3 {
  font-size: 13px;
  font-weight: 600;
  color: #1a1a2e;
  margin-top: 22px;
  margin-bottom: 8px;
  letter-spacing: 0.2px;
  page-break-after: avoid;
}

h4 {
  font-size: 11.5px;
  font-weight: 600;
  color: #40916c;
  margin-top: 16px;
  margin-bottom: 6px;
}

p {
  margin-bottom: 10px;
  orphans: 3;
  widows: 3;
}

strong {
  font-weight: 600;
  color: #1a1a2e;
}

em {
  font-style: italic;
  color: #555;
}

/* ── Horizontal Rules ── */
hr {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, #c8d8cf, transparent);
  margin: 28px 0;
}

/* ── Tables ── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0 18px 0;
  font-size: 9.5px;
  line-height: 1.5;
  page-break-inside: auto;
}

thead {
  display: table-header-group;
}

tr {
  page-break-inside: avoid;
}

thead tr {
  background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%);
}

thead th {
  color: white;
  font-weight: 600;
  text-align: left;
  padding: 8px 10px;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
}

thead th:first-child {
  border-radius: 4px 0 0 0;
}

thead th:last-child {
  border-radius: 0 4px 0 0;
}

tbody tr {
  border-bottom: 1px solid #e8ede9;
}

tbody tr:nth-child(even) {
  background-color: #f7faf8;
}

tbody tr:hover {
  background-color: #eef5f1;
}

tbody td {
  padding: 7px 10px;
  vertical-align: top;
  color: #333;
}

tbody tr:last-child td:first-child {
  border-radius: 0 0 0 4px;
}

tbody tr:last-child td:last-child {
  border-radius: 0 0 4px 0;
}

/* Bold rows (totals) */
tbody tr td strong {
  color: #1a1a2e;
  font-weight: 700;
}

/* ── Code / Diagrams ── */
pre {
  background: #f8faf9;
  border: 1px solid #dbe5de;
  border-radius: 6px;
  padding: 16px 18px;
  font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 9px;
  line-height: 1.55;
  overflow-x: auto;
  margin: 14px 0;
  color: #2d3748;
  page-break-inside: avoid;
}

code {
  font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 9.5px;
  background: #eef5f1;
  padding: 1px 5px;
  border-radius: 3px;
  color: #2d6a4f;
}

pre code {
  background: none;
  padding: 0;
  border-radius: 0;
  color: inherit;
}

/* ── Lists ── */
ul, ol {
  margin: 8px 0 12px 20px;
  padding: 0;
}

li {
  margin-bottom: 4px;
  padding-left: 4px;
}

li::marker {
  color: #40916c;
}

/* ── Blockquotes (callouts) ── */
blockquote {
  border-left: 3px solid #52b788;
  background: #f0f7f3;
  padding: 10px 14px;
  margin: 12px 0;
  border-radius: 0 4px 4px 0;
  font-size: 10px;
  color: #2d6a4f;
}

/* ── Links ── */
a {
  color: #2d6a4f;
  text-decoration: none;
  font-weight: 500;
}

/* ── Special Sections ── */
.content > h2:first-of-type {
  margin-top: 0;
}

/* Table of Contents styling */
.content > h2#table-of-contents + ol,
.content > h2#table-of-contents + ul {
  columns: 2;
  column-gap: 24px;
}

/* ── Page Break Hints ── */
h2 {
  page-break-before: auto;
}

.page-break {
  page-break-before: always;
}

/* Ensure major sections start on new pages */
`;

async function generatePDF() {
  const markdownPath = path.join(__dirname, "FINANCIAL-MODEL.md");
  const outputPath = path.join(__dirname, "FINANCIAL-MODEL.pdf");

  const markdownContent = fs.readFileSync(markdownPath, "utf-8");

  // Remove the first H1 and the subtitle line + first hr from the markdown
  // (we'll render them in the cover page instead)
  let bodyMarkdown = markdownContent;

  // Extract the title and subtitle
  const titleMatch = bodyMarkdown.match(/^# (.+)$/m);
  const title = titleMatch ? titleMatch[1] : "Financial Model";

  // Remove the first heading and the bold subtitle that follows
  bodyMarkdown = bodyMarkdown.replace(/^# .+\n\n\*\*.+\*\*\n\n.+\n\n---/m, "");

  // Convert remaining markdown to HTML
  const contentHtml = md.render(bodyMarkdown);

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>${CSS}</style>
</head>
<body>

  <!-- Cover Page -->
  <div class="cover-page">
    <div class="logo-mark"><span>P</span></div>
    <h1>Planetary Party Protocol</h1>
    <div class="subtitle">INSTITUTIONAL FINANCIAL MODEL</div>
    <hr class="cover-divider">
    <div class="tagline">
      A Capital Framework for Funding Bioregional Regeneration at Scale
    </div>
    <div class="meta-info">
      <strong>Prepared for</strong> prospective impact investors, philanthropic partners,<br>
      and mission-aligned capital allocators<br><br>
      <strong>Fiscal Sponsors</strong><br>
      Kinship Earth (501(c)(3) Private Foundation)<br>
      Na'luea Living Trust<br><br>
      <strong>February 2026</strong>
    </div>
  </div>

  <!-- Document Content -->
  <div class="content">
    ${contentHtml}
  </div>

</body>
</html>`;

  // Write HTML for debugging if needed
  const htmlPath = path.join(__dirname, "FINANCIAL-MODEL.html");
  fs.writeFileSync(htmlPath, html);

  // Generate PDF with Playwright
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.setContent(html, { waitUntil: "networkidle" });

  // Wait for fonts to load
  await page.waitForTimeout(2000);

  await page.pdf({
    path: outputPath,
    format: "Letter",
    printBackground: true,
    margin: {
      top: "0.85in",
      bottom: "1in",
      left: "0.75in",
      right: "0.75in",
    },
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: `
      <div style="width: 100%; text-align: center; font-size: 8px; color: #aaa; font-family: Inter, sans-serif; padding: 0 0.75in;">
        <span style="float: left; color: #999;">Planetary Party Protocol — Institutional Financial Model</span>
        <span style="float: right; color: #999;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
      </div>
    `,
  });

  await browser.close();

  // Clean up intermediate HTML
  fs.unlinkSync(htmlPath);

  const stats = fs.statSync(outputPath);
  console.log(`PDF generated: ${outputPath}`);
  console.log(`File size: ${(stats.size / 1024).toFixed(0)} KB`);
}

generatePDF().catch((err) => {
  console.error("PDF generation failed:", err);
  process.exit(1);
});
