# Pipeline VSL → transcrição → tradução → doc com prints

Referência completa: `PROMPT-Pipeline-VSL.md` (8 fases). Este diretório
implementa as fases mecânicas em `vsl.py`; as fases de julgamento ficam com
o Claude na sessão.

## Configuração (uma vez, nas settings do ambiente cloud)

A chave da AssemblyAI entra como **network secret** do ambiente. O proxy da
Anthropic injeta o header na saída da requisição; a sessão nunca vê a chave,
e ela não existe como variável de ambiente nem em arquivo. Nunca cole a chave
no chat.

1. Em claude.ai/code, menu do ambiente cloud na barra de título → **Edit**.
2. Seção **Network secrets** → **Add secret**:
   - **Nome**: um rótulo, ex. `AssemblyAI` (não é a chave).
   - **Tipo de segredo**: Bearer (padrão).
   - **Sites permitidos**: `api.assemblyai.com`.
   - **Prefixos de caminho**: vazio.
   - **Custom headers**: uma linha com Name `Authorization`, **Prefix vazio**
     (apagar o "Bearer"; a AssemblyAI usa a chave crua), Value = a chave.
3. **Connect**. Não precisa mexer em Network access: o host listado no secret
   já fica acessível.
4. Abrir uma **sessão nova** e rodar:

```bash
python3 vsl-pipeline/vsl.py check     # deve responder OK
```

Para baixar VSL por link (YouTube etc.), aí sim liberar o domínio do vídeo em
**Network access → Custom → Allowed domains**.

## Mapa das fases

| Fase | O que | Quem | Comando |
|---|---|---|---|
| 1 Preparação | pasta `VSL-Pipeline-NOME/`, duração, resolução | script | `vsl.py prep VIDEO --name NOME` |
| 2 Áudio | `audio_vsl.mp3` 128k | script | `vsl.py audio VIDEO --name NOME` |
| 3 Transcrição | AssemblyAI **com diarização** → `transcricao_raw.json`, `segments.json`, `transcricao.md` | script | `vsl.py transcribe --name NOME --lang en\|pt` |
| 4 Falantes + blocos | A/B/C → papéis reais; blocos e mini-blocos com timestamps | Claude | lê `transcricao.md` |
| 5 Tradução | **fiel** (padrão, como no modelo: nomes, marcas, dólares, libras e referências dos EUA mantidos). Adaptação da Fase 5 só sob pedido explícito | Claude | escreve `doc.json` |
| 6 Frames | prévia automática (`frames` sem `--doc`), contact sheet (`sheet`) para legendar olhando, depois extração final pelos nomes do `doc.json` (`frames --doc`) | script + Claude | `vsl.py frames VIDEO --name NOME [--doc doc.json]` · `vsl.py sheet --name NOME` |
| 7 Doc | `.docx` no layout do modelo (`MODELO.md`); upload ao Drive "Transcrições VSL" | script + Claude | `vsl.py docx --name NOME` |
| 8 Verificação | contagens, ordem de timestamps, prints dentro do intervalo, arquivos, nomes | script + Claude | `vsl.py verify --name NOME` |

`doc.exemplo.json` mostra o formato que as Fases 4–5 produzem e a Fase 7 consome.
`MODELO.md` descreve o layout exato do doc de referência.

## Modos

"Pipeline completo" (1–8), "Só transcreve" (1–4), "Transcreve e traduz" (1–5
+ doc sem frames), "Só monta o doc com prints" (6–7), "Adiciona prints" (6).
