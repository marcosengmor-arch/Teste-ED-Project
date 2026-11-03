import json, re
W = 'VSL-Pipeline-SOULFLUSH'
S = json.load(open(f'{W}/sentences.json'))
by = {s['i']: s for s in S}
fix = {
 104: "When this discovery reached the Vatican, Pope Pius XII, known for his diplomatic alliances with Nazi Germany, made a decision that cost us dearly.",
 285: None,
 385: "But I didn't create Soul Flush [ASR: \"Soul Flesh\"] for the Hollywood elite.",
 420: "That's why my recommendation as a friend is that you choose 6 bottles of Soul Flush for $49 per bottle for the complete and permanent unlocking of your bridge to your soul… to God.",
 421: None, 422: None,
 249: "That's when I understood that I could no longer keep this just for myself as a family tradition.",
 258: "A world where people are free to manifest their desires instead of accepting crumbs.",
}
for i, t in fix.items():
    if t is None: del by[i]
    else: by[i]['text'] = t
def merge(a, b):
    by[a]['text'] += ' ' + by[b]['text']; by[a]['end_ms'] = by[b]['end_ms']; del by[b]
merge(227, 228); merge(370, 371); merge(526, 527); merge(597, 598)
S = [by[k] for k in sorted(by)]
TC = "THERESA CAPUTO (narradora)"
spk_ranges = [
 (0,10,TC),(11,12,"VOZ EM OFF (clipe)"),(13,26,TC),(27,31,"DR. OZ (clipe)"),(32,35,"KIM KARDASHIAN (clipe)"),
 (36,302,TC),(303,317,"MARY (depoimento)"),(318,335,TC),(336,339,"MULHER (depoimento, primeira casa)"),(340,364,TC),
 (365,369,"BRENDA (depoimento, diabetes tipo 2)"),(370,511,TC),(512,520,"MULHER (depoimento, promovida a VP)"),(521,596,TC),
 (597,600,"SUSAN, DO TEXAS (pergunta)"),(601,606,TC),(607,610,"BRENDA, DA FLÓRIDA (pergunta)"),(611,618,TC),
 (619,624,"SARAH, DE CHICAGO (pergunta)"),(625,635,TC),(636,639,"CLAIRE, DE OHIO (pergunta)"),(640,651,TC),
]
def spk(i):
    for a,b,l in spk_ranges:
        if a <= i <= b: return l
    raise SystemExit(f"sem falante para {i}")
blocks = [
 (0,"LEAD: a mensagem censurada, a glândula do tamanho de um grão de arroz, Taylor Swift / J.Lo / Kim, 15 bilhões de views e o Vaticano"),
 (36,"PROMESSA + QUEM É THERESA CAPUTO: 4 ingredientes bíblicos, 'não atualize a página', a pineal como antena de TV, $50.000 por ano"),
 (72,"ORIGEM: as mulheres de energia pesada, a avó, Peniel (Gênesis 32:30), o papa amigo de Hitler e o fluoreto nos campos de concentração"),
 (107,"MECANISMO DO PROBLEMA: fluoreto na água e na pasta de dente, NRC 2006, a nuvem cinza, a carta que não chega a Deus, melatonina"),
 (149,"O SISTEMA + A CIÊNCIA: Rochester, visão profética, a receita bíblica da avó, a COVID e a promessa de não deixar o conhecimento morrer"),
 (173,"OS 4 INGREDIENTES BÍBLICOS: hissopo (Sl 51:7), olíbano (Mt 2:11), mirra e canela (Êx 30:22-25)"),
 (200,"AS PRIMEIRAS CURAS: Clarice (18 libras em 2 semanas) e Amanda ($33.000 de dívida e a herança)"),
 (222,"TAYLOR SWIFT: o episódio especial, Travis Kelce, a carta do Vaticano e as fitas apagadas"),
 (251,"A MISSÃO: a nuvem de energia negativa, a raiva e 'não é justo que só as celebridades tenham acesso'"),
 (269,"APRESENTAÇÃO DO SOUL FLUSH: a fórmula bíblica, ingredientes de Galileia, Etiópia, Sinai e Ceilão"),
 (286,"ESTÁGIO 1 — PURIFICAÇÃO DO TEMPLO (7 dias): calafrios, o rádio desliga, sono de bebê + depoimento de Mary"),
 (318,"ESTÁGIO 2 — CONEXÃO COM A FONTE: o olíbano eleva a frequência, intuição afiada + depoimento da primeira casa"),
 (340,"ESTÁGIO 3 — ESCUDO SAGRADO (6 meses): imune ao fluoreto, conselho de amiga, John ($400.000) e Brenda (diabetes)"),
 (370,"OFERTA: 6 meses, 1 conta-gotas por dia, $50.000 / $1.000 / $500 e os 6 frascos a $49 ($1,63 por dia)"),
 (393,"OS 2 TIPOS DE MULHERES: 3 meses x 6 meses, Taylor, 'vacinar a alma', kits de 6 ($49) e 3 ($69), frete grátis"),
 (434,"O MUNDO CONTINUA TÓXICO + GARANTIA DE 180 DIAS ('garantia da bênção')"),
 (449,"OS 3 PRESENTES: sessões semanais de energia ($12.000), Canto Angelical ($3.000) e Guia de Interpretação de Sinais"),
 (483,"ESCASSEZ (92 → 86 frascos), as consequências (Cleveland Clinic) e como usar"),
 (511,"DEPOIMENTO DA VICE-PRESIDENTE + Divine Purity a $49, estoque limitado e 'movimento de luz'"),
 (534,"FECHAMENTO: a encruzilhada, o Holocausto, 'diga sim', o arrependimento, os agradecimentos e o botão"),
 (592,"FAQ: Susan (Texas), Brenda (Flórida), Sarah (Chicago) e Claire (Ohio)"),
]
starts = [b[0] for b in blocks] + [10**9]
def tsd(ms): s=int(ms//1000); return f"{s//60}:{s%60:02d}"
MAXS = 42
out = []
for n,(st,title) in enumerate(blocks,1):
    sents = [s for s in S if st <= s['i'] < starts[n]]
    minis, cur = [], []
    for s in sents:
        if cur and (s['start_ms'] - cur[0]['start_ms'])/1000 >= MAXS:
            minis.append(cur); cur = []
        cur.append(s)
    if cur: minis.append(cur)
    if len(minis) > 1 and (minis[-1][-1]['end_ms'] - minis[-1][0]['start_ms']) < 8000:
        last = minis.pop(); minis[-1].extend(last)
    mb = []
    for m in minis:
        falas = []
        for s in m:
            sp = spk(s['i'])
            if falas and falas[-1]['falante'] == sp: falas[-1]['en'] += ' ' + s['text']
            else: falas.append({"falante": sp, "en": s['text'], "pt": ""})
        mb.append({"inicio": tsd(m[0]['start_ms']), "fim": tsd(m[-1]['end_ms']), "prints": [], "falas": falas})
    out.append({"n": n, "titulo": title, "inicio": mb[0]['inicio'], "fim": mb[-1]['fim'], "mini": mb})
falantes = []
for _,_,l in spk_ranges:
    if l not in falantes: falantes.append(l)
doc = {
 "titulo": "SOUL FLUSH VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte": "Fonte: Vsl SoulFlush.mp4 (51:34). Transcrição: AssemblyAI (speaker labels). Tradução fiel: nomes, marcas, valores em dólares, libras, versículos e referências dos EUA mantidos exatamente como falados.",
 "nota_prints": "Timing: cada mini-bloco traz o intervalo de tempo x → y em que aquela fala acontece no vídeo. Prints: N frames dos momentos mais importantes (provas, documentos, ambientes, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr": "'Soul Flesh' → 'Soul Flush' (30:20); repetição 'Pope Pius XII Pope Pius XII' removida (8:16); o roteiro alterna os nomes 'Soul Flush', 'Divine Purity' e 'Soul Detox' para o mesmo produto — mantidos como falados; em 49:33 a narradora responde 'Margaret' à pergunta de Sarah — mantido como falado; reticências (…) indicam cortes de edição no áudio original.",
 "falantes": falantes, "frames_dir": f"{W}/frames", "img_width_in": 2.35, "blocos": out,
}
json.dump(doc, open(f'{W}/doc.json','w'), ensure_ascii=False, indent=1)
nm = sum(len(b['mini']) for b in out); nf = sum(len(m['falas']) for b in out for m in b['mini'])
print(len(out), "blocos,", nm, "mini-blocos,", nf, "falas,", sum(len(f['en'].split()) for b in out for m in b['mini'] for f in m['falas']), "palavras EN")
with open(f'{W}/estrutura.txt','w') as f:
    for b in out:
        f.write(f"\nBLOCO {b['n']} — {b['titulo']}  [{b['inicio']} – {b['fim']}]\n")
        for k,m in enumerate(b['mini'],1):
            f.write(f"  {b['n']}.{k} ⏱ {m['inicio']} → {m['fim']}  " + " | ".join(f"{x['falante']}: {x['en'][:50]}…" for x in m['falas']) + "\n")
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']):
                f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
