"""Docx para anúncios curtos: por ad, grade de prints (3 colunas) + falas EN e PT com minutagem.
Uso: python3 docx_ads.py doc.json saida.docx"""
import json, sys
from pathlib import Path
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
d=json.load(open(sys.argv[1])); out=sys.argv[2]
fdir=Path(sys.argv[1]).parent/'frames'
NAVY,GRAY=RGBColor(0x1F,0x3A,0x93),RGBColor(0x88,0x88,0x88)
doc=Document(); sec=doc.sections[0]; sec.orientation=WD_ORIENT.LANDSCAPE
sec.page_width,sec.page_height=Inches(11),Inches(8.5); sec.left_margin=sec.right_margin=Inches(0.8); sec.top_margin=sec.bottom_margin=Inches(0.7)
for sname,size,color in (("Title",26,"17365D"),("Heading 1",14,"366091"),("Heading 2",13,"4F81BD")):
    st=doc.styles[sname]; st.font.name,st.font.size="Calibri",Pt(size); st.font.color.rgb=RGBColor.from_string(color)
    if sname!="Title": st.font.bold=True
doc.styles["Normal"].font.name="Calibri"
def small(t,italic=True,size=9.5):
    p=doc.add_paragraph(); r=p.add_run(t); r.italic,r.font.size=italic,Pt(size)
doc.add_heading(d["titulo"],level=0); small(d["fonte"]); small(d["nota_prints"]); small("Falantes: "+" · ".join(d["falantes"]),italic=False)
n_frames=0
for b in d["blocos"]:
    doc.add_page_break(); doc.add_heading(f"{b['titulo']}  [{b['inicio']} – {b['fim']}]",level=1)
    doc.add_heading("Transcrição em inglês",level=2)
    for f in b["falas"]:
        p=doc.add_paragraph(); r=p.add_run(f"[{f['ts']}] "); r.bold,r.font.color.rgb=True,NAVY
        r2=p.add_run(f"{f['falante']}: "); r2.bold=True; p.add_run(f["en"])
    doc.add_heading("Tradução PT-BR",level=2)
    for f in b["falas"]:
        p=doc.add_paragraph(); r=p.add_run(f"[{f['ts']}] "); r.bold,r.font.color.rgb=True,NAVY
        r2=p.add_run(f"{f['falante']}: "); r2.bold=True; p.add_run(f["pt"])
    doc.add_heading(f"Prints visuais ({len(b['prints'])} cenas)",level=2)
    prints=b["prints"]; COLS=3; rows=(len(prints)+COLS-1)//COLS
    t=doc.add_table(rows=rows,cols=COLS)
    for i,pr in enumerate(prints):
        cell=t.cell(i//COLS,i%COLS); pimg=cell.paragraphs[0]; pimg.alignment=WD_ALIGN_PARAGRAPH.CENTER
        fp=fdir/pr["arquivo"]
        if fp.is_file(): pimg.add_run().add_picture(str(fp),width=Inches(1.6)); n_frames+=1
        pc=cell.add_paragraph(); pc.alignment=WD_ALIGN_PARAGRAPH.CENTER
        rc=pc.add_run(f"📷 {pr['ts']} — {pr['legenda']}"); rc.italic,rc.font.size=True,Pt(8)
        rc.add_break(); rf=pc.add_run(pr["arquivo"]); rf.font.size,rf.font.color.rgb=Pt(6.5),GRAY
doc.save(out); print(f"Doc: {out} — {len(d['blocos'])} ads, {n_frames} frames")
