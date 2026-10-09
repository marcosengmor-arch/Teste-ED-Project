#!/usr/bin/env python3
"""Pipeline VSL: vídeo → transcrição → (tradução) → doc com prints.

Implementa as fases mecânicas do PROMPT-Pipeline-VSL.md. As fases de
julgamento (identificar falantes, mapear blocos, traduzir, legendar) são
feitas pelo Claude e gravadas em doc.json, que o subcomando `docx` monta.

Chave da AssemblyAI: SOMENTE via variável de ambiente ASSEMBLYAI_API_KEY
(secret do ambiente). Nunca em arquivo, log ou chat.

Subcomandos:
  check                       testa chave + acesso a api.assemblyai.com
  prep   VIDEO --name NOME    cria VSL-Pipeline-NOME/, mostra duração (Fase 1)
  audio  VIDEO --name NOME    extrai audio_vsl.mp3 (Fase 2)
  transcribe --name NOME [--lang en|pt]   AssemblyAI c/ diarização (Fase 3)
  frames VIDEO --name NOME [--every 60] [--extra 00:05:00 ...]   (Fase 6)
  docx   --name NOME [--doc doc.json]     monta o .docx (Fase 7)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

AAI = "https://api.assemblyai.com/v2"


# ---------- utilidades ----------
def work(name):
    return Path(f"VSL-Pipeline-{name}")


def ms_to_ts(ms):
    s = int(ms) // 1000
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


def ts_to_sec(ts):
    parts = [int(p) for p in ts.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


def duration(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def headers():
    key = os.environ.get("ASSEMBLYAI_API_KEY", "").strip()
    if not key:
        sys.exit("ASSEMBLYAI_API_KEY não encontrada. Configure como secret do ambiente "
                 "e abra uma sessão nova.")
    return {"authorization": key}


# ---------- fases ----------
def cmd_check(a):
    import requests
    try:
        r = requests.get(f"{AAI}/transcript", headers=headers(), params={"limit": 1}, timeout=20)
    except requests.RequestException as e:
        print(f"REDE: não alcançou api.assemblyai.com -> {e}")
        print("Libere api.assemblyai.com na política de rede do ambiente.")
        return 1
    if r.status_code == 200:
        print("OK: chave válida e api.assemblyai.com acessível.")
        return 0
    if r.status_code in (401, 403):
        print(f"CHAVE: AssemblyAI respondeu {r.status_code} (chave inválida).")
        return 1
    print(f"Resposta inesperada {r.status_code}: {r.text[:200]}")
    return 1


def cmd_prep(a):
    if not Path(a.video).is_file():
        sys.exit(f"Vídeo não encontrado: {a.video}")
    w = work(a.name)
    (w / "frames").mkdir(parents=True, exist_ok=True)
    d = duration(a.video)
    meta = {"video": str(Path(a.video).resolve()), "duracao_s": d, "duracao": ms_to_ts(d * 1000)}
    (w / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"Pasta {w}/ criada. Duração: {meta['duracao']} "
          f"({os.path.getsize(a.video) / 1e6:.1f} MB)")
    return 0


def cmd_audio(a):
    w = work(a.name)
    w.mkdir(parents=True, exist_ok=True)
    out = w / "audio_vsl.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vn",
                    "-acodec", "libmp3lame", "-ab", "128k", "-ar", "44100", str(out)], check=True)
    print(f"Áudio: {out} ({out.stat().st_size / 1e6:.1f} MB)")
    return 0


def cmd_transcribe(a):
    import requests
    h = headers()
    w = work(a.name)
    audio = w / "audio_vsl.mp3"
    if not audio.is_file():
        sys.exit(f"{audio} não existe. Rode `audio` antes.")

    with open(audio, "rb") as f:
        up = requests.post(f"{AAI}/upload", headers=h, data=f, timeout=900)
    up.raise_for_status()

    j = requests.post(f"{AAI}/transcript", headers=h, timeout=60, json={
        "audio_url": up.json()["upload_url"],
        "language_code": a.lang,
        "speaker_labels": True,
        "punctuate": True,
        "format_text": True,
    })
    j.raise_for_status()
    tid = j.json()["id"]
    print(f"Job {tid} enviado. Aguardando...")

    while True:
        r = requests.get(f"{AAI}/transcript/{tid}", headers=h, timeout=60).json()
        if r["status"] == "completed":
            break
        if r["status"] == "error":
            sys.exit(f"Erro AssemblyAI: {r.get('error')}")
        time.sleep(15)

    (w / "transcricao_raw.json").write_text(json.dumps(r, ensure_ascii=False, indent=2))

    utts = [{"speaker": u["speaker"], "start": ms_to_ts(u["start"]), "end": ms_to_ts(u["end"]),
             "start_ms": u["start"], "end_ms": u["end"], "text": u["text"]}
            for u in (r.get("utterances") or [])]
    (w / "segments.json").write_text(json.dumps(utts, ensure_ascii=False, indent=2))

    # versão legível para revisão / identificação de falantes (Fase 4)
    with open(w / "transcricao.md", "w", encoding="utf-8") as f:
        f.write(f"# Transcrição bruta — {a.name}\n\n")
        for u in utts:
            f.write(f"**[{u['start']} - {u['end']}] Falante {u['speaker']}:** {u['text']}\n\n")

    speakers = sorted({u["speaker"] for u in utts})
    print(f"Concluído: {len(utts)} falas, falantes detectados {speakers}, "
          f"{r.get('audio_duration')}s. Arquivos: transcricao_raw.json, segments.json, transcricao.md")
    return 0


def frame_timestamps(segments, every, extra, total_s):
    """Troca de falante + a cada N s de fala contínua + pontos extras."""
    pts = {0}
    prev = None
    last_mark = 0
    for u in segments:
        s = u["start_ms"] // 1000
        if u["speaker"] != prev:
            pts.add(s)
            last_mark = s
            prev = u["speaker"]
        e = u["end_ms"] // 1000
        while e - last_mark > every:
            last_mark += every
            pts.add(last_mark)
    for ts in extra:
        pts.add(ts_to_sec(ts))
    return sorted(p for p in pts if p < total_s)


def extract_frame(video, sec, out):
    for delta in (0, -2, 2):
        t = sec + delta
        if t < 0:
            continue
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", video,
                            "-frames:v", "1", "-q:v", "2", str(out)], capture_output=True)
        if r.returncode == 0 and out.is_file() and out.stat().st_size > 0:
            return t
    return None


def cmd_frames(a):
    w = work(a.name)
    seg_file = w / "segments.json"
    segments = json.loads(seg_file.read_text()) if seg_file.is_file() else []
    if not segments and not a.extra:
        sys.exit("Sem segments.json e sem --extra: nada para extrair.")
    total = duration(a.video)
    pts = frame_timestamps(segments, a.every, a.extra, total)
    (w / "frames").mkdir(parents=True, exist_ok=True)
    index, missing = {}, []
    for sec in pts:
        ts = ms_to_ts(sec * 1000)
        out = w / "frames" / f"frame_{ts.replace(':', '')}.jpg"
        got = extract_frame(a.video, sec, out)
        if got is None:
            missing.append(ts)
            index[ts] = None
        else:
            index[ts] = str(out)
    (w / "frames" / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(f"Frames: {len(pts) - len(missing)} extraídos, {len(missing)} indisponíveis {missing}")
    return 0


def cmd_docx(a):
    from datetime import date
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt, RGBColor

    w = work(a.name)
    doc_json = Path(a.doc) if a.doc else w / "doc.json"
    d = json.loads(doc_json.read_text(encoding="utf-8"))
    gray, light, blue = RGBColor(128, 128, 128), RGBColor(150, 150, 150), RGBColor(0, 100, 180)
    incluir_original = d.get("incluir_original", True)

    doc = Document()
    doc.add_heading(f"VSL TRADUZIDA — {d['projeto']}", level=0)
    p = doc.add_paragraph()
    for label, val in (("Direção: ", d.get("direcao", "")), ("Mercado: ", d.get("mercado", "")),
                       ("Duração: ", d.get("duracao", "")),
                       ("Falantes: ", f"{len(d.get('falantes', []))} identificados "
                                      f"({', '.join(d.get('falantes', []))})"),
                       ("Data: ", date.today().strftime("%d/%m/%Y"))):
        p.add_run(label).bold = True
        p.add_run(val + "\n")
    doc.add_paragraph("─" * 60)

    n_frames = 0
    for bloco in d["blocos"]:
        doc.add_heading(f"{bloco.get('emoji', '')} {bloco['nome']} "
                        f"[{bloco['ts_inicio']} - {bloco['ts_fim']}]".strip(), level=1)
        for seg in bloco["segmentos"]:
            fp = seg.get("frame_path")
            if fp and Path(fp).is_file():
                doc.add_picture(fp, width=Inches(5.5))
                n_frames += 1
                tp = doc.add_paragraph(f"[{seg['timestamp']}]")
                tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in tp.runs:
                    run.font.size, run.font.color.rgb = Pt(9), gray
            elif fp:
                doc.add_paragraph(f"[FRAME INDISPONÍVEL em {seg['timestamp']}]")

            p = doc.add_paragraph()
            r = p.add_run(f"{seg['falante']}:")
            r.bold, r.font.size = True, Pt(11)
            tr = p.add_run(f"  [{seg['timestamp']}]")
            tr.font.size, tr.font.color.rgb = Pt(9), gray

            doc.add_paragraph(seg["texto_traduzido"])
            if incluir_original and seg.get("texto_original"):
                po = doc.add_paragraph()
                ro = po.add_run(f"[Original] {seg['texto_original']}")
                ro.italic, ro.font.size, ro.font.color.rgb = True, Pt(9), light
            if seg.get("comentario_editor"):
                pe = doc.add_paragraph()
                re_ = pe.add_run(seg["comentario_editor"])
                re_.italic, re_.font.color.rgb = True, blue

    notas = d.get("notas", {})
    doc.add_page_break()
    doc.add_heading("NOTAS DE ADAPTAÇÃO", level=1)
    for titulo, chave in (("Adaptações culturais", "adaptacoes_culturais"),
                          ("Personagens renomeados", "personagens_renomeados"),
                          ("Conversões de moeda/medida", "conversoes"),
                          ("Pontos com dúvida [?? ??]", "duvidas"),
                          ("Erros de transcrição corrigidos", "correcoes_asr"),
                          ("Inconsistências no original", "inconsistencias")):
        doc.add_heading(titulo, level=2)
        itens = notas.get(chave) or []
        if not itens:
            doc.add_paragraph("Nenhuma.")
        for it in itens:
            doc.add_paragraph(it, style="List Bullet")

    out = w / f"VSL_Traduzida_{d['projeto']}.docx"
    doc.save(out)
    n_seg = sum(len(b["segmentos"]) for b in d["blocos"])
    print(f"Doc: {out} — {len(d['blocos'])} blocos, {n_seg} segmentos, {n_frames} frames embutidos")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check").set_defaults(fn=cmd_check)
    for name, fn in (("prep", cmd_prep), ("audio", cmd_audio)):
        s = sub.add_parser(name)
        s.add_argument("video")
        s.add_argument("--name", required=True)
        s.set_defaults(fn=fn)

    s = sub.add_parser("transcribe")
    s.add_argument("--name", required=True)
    s.add_argument("--lang", default="en", help="en ou pt (padrão en)")
    s.set_defaults(fn=cmd_transcribe)

    s = sub.add_parser("frames")
    s.add_argument("video")
    s.add_argument("--name", required=True)
    s.add_argument("--every", type=int, default=60, help="segundos de fala contínua por frame")
    s.add_argument("--extra", nargs="*", default=[], help="timestamps extras HH:MM:SS")
    s.set_defaults(fn=cmd_frames)

    s = sub.add_parser("docx")
    s.add_argument("--name", required=True)
    s.add_argument("--doc", help="caminho do doc.json (padrão VSL-Pipeline-NOME/doc.json)")
    s.set_defaults(fn=cmd_docx)

    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
