"""Gera o docx em formato PT-BR único: sumário por bloco + transcrição com minutagens + prints.
Uso: python3 docx_pt.py doc.json saida.docx
doc.json: {titulo, fonte, nota_prints, frames_dir, img_width_in,
           sumario:[{bloco, inicio, fim, descricao}],
           blocos:[{n, titulo, inicio, fim, mini:[{inicio, fim, prints:[{ts,legenda,arquivo}], paras:[{ts, texto}]}]}]}
"""
import json, sys
from pathlib import Path
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

d = json.load(open(sys.argv[1]))
out = sys.argv[2]
fdir = Path(d["frames_dir"])
NAVY, GRAY = RGBColor(0x1F, 0x3A, 0x93), RGBColor(0x88, 0x88, 0x88)
img_w = Inches(d.get("img_width_in", 2.35))

doc = Document()
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Inches(11), Inches(8.5)
sec.left_margin = sec.right_margin = Inches(0.8)
sec.top_margin = sec.bottom_margin = Inches(0.7)
for sname, size, color in (("Title", 26, "17365D"), ("Heading 1", 14, "366091"), ("Heading 2", 13, "4F81BD")):
    st = doc.styles[sname]
    st.font.name, st.font.size = "Calibri", Pt(size)
    st.font.color.rgb = RGBColor.from_string(color)
    if sname != "Title": st.font.bold = True
doc.styles["Normal"].font.name = "Calibri"

def small(text, italic=True, size=9.5):
    p = doc.add_paragraph(); r = p.add_run(text); r.italic, r.font.size = italic, Pt(size); return p

doc.add_heading(d["titulo"], level=0)
small(d["fonte"]); small(d["nota_prints"])

# Sumário
doc.add_heading(f"SUMÁRIO DA VSL — blocos e minutagens ({len(d['sumario'])} blocos)", level=1)
t = doc.add_table(rows=1, cols=3); t.style = "Light Grid Accent 1"
for i, h in enumerate(("Bloco", "Minutagem", "O que acontece")):
    c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True
for s in d["sumario"]:
    row = t.add_row().cells
    row[0].text = s["bloco"]; row[1].text = f"{s['inicio']} → {s['fim']}"; row[2].text = s["descricao"]
for row in t.rows:
    for c, w in zip(row.cells, (Inches(1.9), Inches(1.3), Inches(6.1))):
        c.width = w
        for p in c.paragraphs:
            for r in p.runs: r.font.size = Pt(9.5)
doc.add_paragraph()

# Transcrição
doc.add_heading("TRANSCRIÇÃO COM MINUTAGENS + PRINTS", level=0)
n_frames = 0
for b in d["blocos"]:
    doc.add_heading(f"{b['titulo']}  [{b['inicio']} – {b['fim']}]", level=1)
    for k, mb in enumerate(b["mini"], 1):
        doc.add_heading(f"{b['n']}.{k}   ⏱ {mb['inicio']} → {mb['fim']}", level=2)
        prints = mb.get("prints", [])
        if prints:
            rows = (len(prints) + 1) // 2
            tt = doc.add_table(rows=rows, cols=2)
            for i, pr in enumerate(prints):
                cell = tt.cell(i // 2, i % 2)
                pimg = cell.paragraphs[0]; pimg.alignment = WD_ALIGN_PARAGRAPH.CENTER
                fpath = fdir / pr["arquivo"]
                if fpath.is_file():
                    pimg.add_run().add_picture(str(fpath), width=img_w); n_frames += 1
                else:
                    pimg.add_run(f"[FRAME INDISPONÍVEL em {pr['ts']}]").italic = True
                pc = cell.add_paragraph(); pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
                rc = pc.add_run(f"📷 {pr['ts']} — {pr['legenda']}"); rc.italic, rc.font.size = True, Pt(8.5)
                rc.add_break(); rf = pc.add_run(pr["arquivo"]); rf.font.size, rf.font.color.rgb = Pt(7), GRAY
            doc.add_paragraph()
        for para in mb["paras"]:
            p = doc.add_paragraph()
            r = p.add_run(f"[{para['ts']}] "); r.bold, r.font.color.rgb = True, NAVY
            p.add_run(para["texto"])
doc.save(out)
print(f"Doc: {out} — {len(d['blocos'])} blocos, {sum(len(b['mini']) for b in d['blocos'])} mini-blocos, {n_frames} frames")
