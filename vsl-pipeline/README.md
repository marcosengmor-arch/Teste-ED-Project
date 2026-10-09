# Pipeline VSL → transcrição + prints

Passo 1 (transcrição) usa a AssemblyAI. A chave fica **somente** no ambiente
cloud do Claude Code, como secret, nunca em arquivo ou no chat.

## Configuração (uma vez, nas settings do ambiente)

1. Menu do ambiente cloud na barra de título da sessão → **Edit**.
2. **Network secrets** (ou variável de ambiente): nome `ASSEMBLYAI_API_KEY`, valor = sua chave.
3. **Network access**: liberar `api.assemblyai.com` em *Allowed domains*
   (manter "Allow package managers" marcado). Para baixar VSL por link,
   liberar também os domínios do vídeo (ex.: YouTube/Vimeo).
4. Abrir uma **sessão nova** (a sessão atual não recebe as mudanças).

## Teste

```bash
python3 vsl-pipeline/assemblyai_transcribe.py --check
```

## Transcrever

```bash
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 audio.wav
python3 vsl-pipeline/assemblyai_transcribe.py audio.wav -o transcript.json
```

Saída: `transcript.json` com `utterances` (falante A/B/C, início/fim em ms, texto),
base para os blocos, frames e o `.docx` no padrão SODA TIDE.
