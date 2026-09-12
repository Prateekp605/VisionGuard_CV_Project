"""
Compiles PROJECT_REPORT.md into a beautifully formatted, printable HTML report.
Can be converted to PDF via Chrome/Edge (Ctrl+P -> Save as PDF).
"""

import os
import re


def md_to_html(md_text: str) -> str:
    """Lightweight markdown to styled HTML converter."""
    html = md_text

    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Bold & Italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Inline Code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Fenced Code Blocks
    def code_repl(match):
        code = match.group(2)
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code>{code}</code></pre>'

    html = re.sub(r'```([a-z]*)\n([\s\S]*?)\n```', code_repl, html)

    # Tables
    lines = html.split("\n")
    in_table = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("|") and line.strip().endswith("|"):
            if not in_table:
                in_table = True
                new_lines.append('<div class="table-container"><table>')
            parts = [p.strip() for p in line.strip()[1:-1].split("|")]
            if all(set(p) <= set("-: ") for p in parts):
                continue
            tag = "th" if "<thead>" not in "".join(new_lines[-2:]) else "td"
            cells = "".join([f"<{tag}>{p}</{tag}>" for p in parts])
            new_lines.append(f"<tr>{cells}</tr>")
        else:
            if in_table:
                in_table = False
                new_lines.append("</table></div>")
            new_lines.append(line)
    if in_table:
        new_lines.append("</table></div>")
    html = "\n".join(new_lines)

    # Paragraphs
    paragraphs = html.split("\n\n")
    processed_p = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if p_clean.startswith(("<h1", "<h2", "<h3", "<h4", "<pre", "<div", "<table", "<ul", "<ol", "<hr", "---")):
            if p_clean.startswith("---"):
                processed_p.append("<hr>")
            else:
                processed_p.append(p_clean)
        else:
            processed_p.append(f"<p>{p_clean}</p>")

    return "\n".join(processed_p)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_md_path = os.path.join(base_dir, "PROJECT_REPORT.md")
    out_dir = os.path.join(base_dir, "output", "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_html_path = os.path.join(out_dir, "VisionGuard_Project_Report.html")

    with open(report_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    body_html = md_to_html(md_text)

    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>VisionGuard - Academic Project Report</title>
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
        }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            color: #1a1a24;
            line-height: 1.6;
            background-color: #fcfcfd;
            margin: 0;
            padding: 40px;
        }}
        .report-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 50px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        }}
        h1 {{
            color: #0d233a;
            border-bottom: 2px solid #2b6cb0;
            padding-bottom: 8px;
            margin-top: 40px;
        }}
        h2 {{
            color: #2b6cb0;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 30px;
        }}
        h3 {{
            color: #2d3748;
            margin-top: 20px;
        }}
        p, li {{
            color: #4a5568;
            font-size: 15px;
        }}
        pre {{
            background: #1e2430;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 13px;
        }}
        code {{
            background: #edf2f7;
            color: #c53030;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
        }}
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        .table-container {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 10px 12px;
            text-align: left;
        }}
        th {{
            background-color: #edf2f7;
            color: #2d3748;
            font-weight: 600;
        }}
        hr {{
            border: 0;
            border-top: 1px solid #e2e8f0;
            margin: 30px 0;
        }}
        .print-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2b6cb0;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .print-btn:hover {{
            background: #2c5282;
        }}
        @media print {{
            .print-btn {{ display: none; }}
            body {{ padding: 0; background: white; }}
            .report-wrapper {{ box-shadow: none; padding: 0; }}
            h1, h2 {{ page-break-after: avoid; }}
            pre, table {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">Print / Save as PDF</button>
    <div class="report-wrapper">
        {body_html}
    </div>
</body>
</html>
"""

    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html_document)

    print("=========================================================")
    print("      PROJECT REPORT GENERATION COMPLETED!               ")
    print("=========================================================")
    print(f"Generated printable report at:")
    print(f"-> {out_html_path}")
    print("\nTip: Open this file in your browser and click 'Print / Save as PDF'")
    print("     to obtain your official submission PDF document.")
    print("=========================================================\n")


if __name__ == "__main__":
    main()
