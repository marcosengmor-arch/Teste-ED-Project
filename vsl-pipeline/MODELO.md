# Layout do doc-modelo (SODA TIDE VSL — Transcrição EN + Tradução PT-BR + Prints)

Extraído do docx de referência (81:33, 19 blocos, 124 mini-blocos, 198 prints).
`vsl.py docx` reproduz exatamente esta estrutura a partir de `doc.json`.

## Página e fontes
- US Letter **paisagem** (11 × 8,5 pol), margens 0,8 pol laterais e 0,7 pol topo/rodapé.
- Calibri. Title 26 pt #17365D · Heading 1 14 pt negrito #366091 · Heading 2 13 pt negrito #4F81BD.

## Cabeçalho (topo do doc)
1. **Title**: `NOME VSL — Transcrição EN + Tradução PT-BR + Prints`
2. Itálico 9,5 pt: `Fonte: arquivo.mp4 (duração, resolução). Transcrição: AssemblyAI (modelo, speaker labels). Tradução fiel: ...`
3. Itálico 9,5 pt: `Timing: cada mini-bloco traz o intervalo x → y ... Prints: N frames ... nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.`
4. 9,5 pt: `Falantes: A · B · C ...` (separador " · ")
5. **Heading 1** `Estrutura da VSL (N blocos)` + uma linha 10 pt por bloco:
   `BLOCO n — TÍTULO (resumo)  —  m:ss → m:ss`

## PARTE 1 — TRANSCRIÇÃO EM INGLÊS POR BLOCOS (Title)
Para cada bloco:
- **Heading 1**: `BLOCO n — TÍTULO  [m:ss – m:ss]`
- Para cada mini-bloco: **Heading 2** `n.k   ⏱ m:ss → m:ss`, depois uma linha por fala:
  run negrito azul-marinho #1F3A93 `FALANTE: ` + texto normal.
- Mini-bloco = 15–60 s de fala, abre novo na troca de assunto/cena; dentro dele pode haver
  várias falas alternadas (diálogo Oprah/Dr. Oz).

## LER AQUI (Title) → PARTE 2 — TRADUÇÃO PT-BR + PRINTS (Title)
Mesma estrutura de blocos e mini-blocos. Em cada mini-bloco que tem prints, logo abaixo do
Heading 2 e **antes** das falas:
- Tabela sem bordas, 2 colunas, até 2 linhas (máx. 4 prints por mini-bloco; o mais comum é 1–2).
- Cada célula: parágrafo centralizado com a imagem (largura 2,35 pol; altura segue a proporção
  do vídeo, 2,94 pol no vídeo 720x900), depois parágrafo centralizado com a legenda:
  itálico 8,5 pt `📷 m:ss — legenda` + quebra de linha + 7 pt cinza #888888 `nome-do-arquivo.jpg`.
- Parágrafo vazio, depois as falas traduzidas no mesmo formato de Parte 1.

## Timestamps
- No doc: `m:ss`, minutos sem limite (`80:57`, não `1:20:57`).
- No nome do arquivo: `HH-MM-SS` (`01-20-57`).

## Prints
- Nome: `bNN_descricao-curta_HH-MM-SS.jpg` (NN = bloco, descrição em minúsculo com `_`).
- O que vira print: lettering na tela, screenshots de prova, estudos, ambientes/cenários,
  personagens, produto, oferta/preços, antes/depois, demos, CTA. Densidade do modelo: ~2,4 prints/min.
- Legenda em PT-BR descrevendo só o que aparece no frame; lettering e marcas em EN-US entre aspas.

## Tradução (decisão do Marcos: fiel, como no modelo)
"Tradução fiel: nomes, marcas, valores em dólares, libras e referências dos EUA mantidos
exatamente como falados." O doc é material de estudo/modelagem, não de produção. Portanto:
- Nomes, marcas, preços em dólar, libras, °F, datas, celebridades e referências dos EUA ficam
  como no original. Números podem ficar em algarismos.
- Português natural e fiel ao ritmo: frase curta continua curta, repetições propositais mantidas,
  nada melhorado, cortado ou adicionado. Gírias por equivalente natural em PT-BR, sem literalidade.
- Erros óbvios de transcrição (nomes próprios, termos técnicos) corrigidos na Parte 1 e na 2.
- Sem seção NOTAS DE ADAPTAÇÃO (não há `notas` no doc.json). As regras de adaptação da Fase 5
  do PROMPT só entram se um projeto pedir explicitamente "adaptar"; aí `notas` é preenchido e
  a seção aparece no final.

## Imagens
Como no exemplo: largura 2,35 pol, altura pela proporção do vídeo. É material de referência;
não escalar para vídeos horizontais.

## doc.json (o que o Claude produz nas Fases 4–5)
Ver `doc.exemplo.json`: `titulo`, `fonte`, `nota_prints`, `falantes`, `frames_dir`,
`blocos[] { n, titulo, inicio, fim, mini[] { inicio, fim, prints[] {ts, legenda, arquivo},
falas[] {falante, en, pt} } }`, `notas{}` opcional.
