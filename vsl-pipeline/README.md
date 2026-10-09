# Pipeline VSL → transcrição → tradução → doc com prints

Referência completa: `PROMPT-Pipeline-VSL.md` (8 fases). Este diretório
implementa as fases mecânicas em `vsl.py`; as fases de julgamento ficam com
o Claude na sessão.

## Configuração (uma vez, nas settings do ambiente cloud)

A chave da AssemblyAI fica **só** no ambiente, como secret. Nunca em
arquivo (`~/.assemblyai_key` não persiste aqui) nem colada no chat.

1. Menu do ambiente cloud na barra de título da sessão → **Edit**.
2. **Network secrets** (ou variável de ambiente): `ASSEMBLYAI_API_KEY` = sua chave.
3. **Network access**: liberar `api.assemblyai.com` em *Allowed domains*
   ("Allow package managers" marcado). VSL por link → liberar o domínio do vídeo.
4. Abrir uma **sessão nova**.

```bash
python3 vsl-pipeline/vsl.py check     # deve responder OK
```

## Mapa das fases

| Fase | O que | Quem | Comando |
|---|---|---|---|
| 1 Preparação | pasta `VSL-Pipeline-NOME/`, duração | script | `vsl.py prep VIDEO --name NOME` |
| 2 Áudio | `audio_vsl.mp3` 128k | script | `vsl.py audio VIDEO --name NOME` |
| 3 Transcrição | AssemblyAI **com diarização** (`speaker_labels`) → `transcricao_raw.json`, `segments.json`, `transcricao.md` | script | `vsl.py transcribe --name NOME --lang en\|pt` |
| 4 Falantes + blocos | mapear A/B/C → NARRADOR, depoimento, médico; blocos da VSL | Claude | lê `transcricao.md` |
| 5 Tradução | regras do prompt (números por extenso, moeda psicológica, nomes, gírias, log de adaptações) | Claude | escreve `doc.json` |
| 6 Frames | troca de falante + a cada 60 s + extras (início de bloco, [B-ROLL]); fallback ±2 s | script | `vsl.py frames VIDEO --name NOME --extra 00:05:00 ...` |
| 7 Doc | `.docx` no layout do prompt + notas de adaptação; upload ao Drive ("Transcrições VSL") | script + Claude | `vsl.py docx --name NOME` |
| 8 Verificação | checklist do prompt | Claude | — |

`doc.exemplo.json` mostra o formato que a Fase 5 produz e a Fase 7 consome
(blocos → segmentos com falante, timestamp, frame, tradução, original,
comentário de editor; mais as notas finais).

## Modos

"Pipeline completo" (1–8), "Só transcreve" (1–4), "Transcreve e traduz" (1–5
+ doc sem frames), "Só monta o doc com prints" (6–7), "Adiciona prints" (6).
