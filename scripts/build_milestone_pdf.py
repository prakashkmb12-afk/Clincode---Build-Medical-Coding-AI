import os
import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def convert_md_to_pdf(md_path: str, pdf_path: str):
    print(f"Converting {md_path} -> {pdf_path}...")
    if not os.path.exists(md_path):
        print(f"Error: {md_path} does not exist.")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Code'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    lines = md_text.splitlines()
    in_code_block = False
    code_lines = []

    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Code block handling
        if stripped.startswith("```"):
            if in_code_block:
                code_text = "<br/>".join([c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") for c in code_lines])
                story.append(Paragraph(code_text, code_style))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Table handling
        if "|" in line and (line.startswith("|") or line.endswith("|")):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
            continue
        else:
            if in_table:
                # Flush table
                in_table = False
                parsed_rows = []
                for tr in table_lines:
                    if "---" in tr:
                        continue
                    cells = [c.strip() for c in tr.split("|")[1:-1]]
                    parsed_rows.append([Paragraph(re.sub(r'`(.*?)`', r'<b>\1</b>', cell), body_style) for cell in cells])

                if parsed_rows:
                    t = Table(parsed_rows, colWidths=None)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                        ('TOPPADDING', (0,0), (-1,-1), 4),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 6))
                table_lines = []

        if not stripped:
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], h2_style))
        elif stripped == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceBefore=8, spaceAfter=8))
        else:
            # Format inline bold/code
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', stripped)
            formatted = re.sub(r'`(.*?)`', r'<font color="#0F172A"><b>\1</b></font>', formatted)
            story.append(Paragraph(formatted, body_style))

    doc.build(story)
    print(f"Successfully generated PDF: {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        convert_md_to_pdf(sys.argv[1], sys.argv[2])
    else:
        convert_md_to_pdf(
            "docs/milestone-pdfs/ClinCode_M1_Documentation.md",
            "docs/milestone-pdfs/ClinCode_M1_Documentation.pdf"
        )
