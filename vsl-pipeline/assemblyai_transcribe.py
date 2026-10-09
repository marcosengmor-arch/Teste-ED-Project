#!/usr/bin/env python3
"""Transcrição de VSL via AssemblyAI (com diarização de falantes).

A chave NUNCA é passada por argumento nem gravada em arquivo: é lida da
variável de ambiente ASSEMBLYAI_API_KEY, configurada como secret do ambiente.

Uso:
  python3 assemblyai_transcribe.py --check                 # testa chave + rede
  python3 assemblyai_transcribe.py audio.wav -o out.json   # transcreve
  python3 assemblyai_transcribe.py audio.wav --lang en_us  # idioma (padrão en_us)
"""
import argparse
import json
import os
import sys
import time

import requests

AAI = "https://api.assemblyai.com/v2"


def headers():
    key = os.environ.get("ASSEMBLYAI_API_KEY", "").strip()
    if not key:
        sys.exit(
            "ASSEMBLYAI_API_KEY não encontrada no ambiente. Configure como secret "
            "do ambiente (Network secrets / variável de ambiente) e abra uma sessão nova."
        )
    return {"authorization": key}


def check():
    try:
        r = requests.get(f"{AAI}/transcript", headers=headers(), params={"limit": 1}, timeout=20)
    except requests.RequestException as e:
        print(f"REDE: falha ao alcançar api.assemblyai.com -> {e}")
        print("Verifique se api.assemblyai.com está liberado na política de rede do ambiente.")
        return 1
    if r.status_code == 200:
        print("OK: chave válida e api.assemblyai.com acessível.")
        return 0
    if r.status_code in (401, 403):
        print(f"CHAVE: AssemblyAI respondeu {r.status_code} (chave inválida ou sem permissão).")
        return 1
    print(f"Resposta inesperada {r.status_code}: {r.text[:200]}")
    return 1


def transcribe(path, lang, out):
    h = headers()
    with open(path, "rb") as f:
        up = requests.post(f"{AAI}/upload", headers=h, data=f, timeout=600)
    up.raise_for_status()
    audio_url = up.json()["upload_url"]

    j = requests.post(
        f"{AAI}/transcript",
        headers=h,
        json={"audio_url": audio_url, "speaker_labels": True, "language_code": lang},
        timeout=60,
    )
    j.raise_for_status()
    tid = j.json()["id"]
    print(f"Transcrição enviada (id {tid}). Aguardando...")

    while True:
        r = requests.get(f"{AAI}/transcript/{tid}", headers=h, timeout=60).json()
        if r["status"] == "completed":
            break
        if r["status"] == "error":
            sys.exit(f"Erro na AssemblyAI: {r.get('error')}")
        time.sleep(5)

    result = {
        "id": r["id"],
        "language_code": r.get("language_code"),
        "audio_duration": r.get("audio_duration"),
        "text": r.get("text"),
        "utterances": [
            {"speaker": u["speaker"], "start_ms": u["start"], "end_ms": u["end"], "text": u["text"]}
            for u in (r.get("utterances") or [])
        ],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Concluído: {len(result['utterances'])} utterances, "
          f"{result['audio_duration']}s de áudio -> {out}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("audio", nargs="?", help="arquivo de áudio/vídeo (wav, mp3, mp4...)")
    p.add_argument("-o", "--out", default="transcript.json")
    p.add_argument("--lang", default="en_us")
    p.add_argument("--check", action="store_true", help="só testa chave e rede")
    a = p.parse_args()

    if a.check:
        sys.exit(check())
    if not a.audio:
        p.error("informe o arquivo de áudio ou use --check")
    transcribe(a.audio, a.lang, a.out)


if __name__ == "__main__":
    main()
