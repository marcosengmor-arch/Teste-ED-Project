import json, re
W = 'VSL-Pipeline-HORSE-JELLY'
S = json.load(open(f'{W}/sentences.json'))
by = {s['i']: s for s in S}
fix = {
 49: "Production, please play the video of Gary Brecka [ASR: \"Jerry Blackdot\"] and Mel Gibson.",
 264: "Called it GenX.",
 501: "Less doesn't break the cross-links of cavernous fibrosis.",
 537: "[Tongkat Ali.] This reactivates. Root from Malaysia in standardized extract, doesn't add testosterone, unlocks the receptors that still exist inside you and that your body gave up using.",
 699: "Unlike the standard FDA certificate, which only confirms safety for consumption, the Guaranteed Efficacy Seal is an official document that certifies the treatment's efficacy for men between 35 [ASR: \"30 35\"] and 80 years old, regardless of their condition.",
}
for i, t in fix.items(): by[i]['text'] = t
def merge(a, b):
    by[a]['text'] += ' ' + by[b]['text']; by[a]['end_ms'] = by[b]['end_ms']; del by[b]
merge(753, 754); merge(793, 794)
S = [by[k] for k in sorted(by)]

GARY = "GARY BRECKA (narrador)"; MEL = "MEL GIBSON"; APR = "APRESENTADORA (criadora adulta)"; FAQ = "NARRADOR DO FAQ"
spk_ranges = [
 (0,20,APR),(21,24,"HOMEM 1 (depoimento)"),(25,27,"HOMEM 2, MOTORISTA DE UBER (depoimento)"),(28,32,"HOMEM 3 (depoimento)"),(33,49,APR),
 (50,54,GARY),(55,58,"CONVIDADO DE PODCAST (depoimento)"),(59,60,"CLIPE"),(61,78,GARY),(79,191,MEL),(192,230,GARY),
 (231,235,"EX-CIENTISTA DA FDA"),(236,252,GARY),(253,258,"EX-EXECUTIVO DA BIG PHARMA (depoimento)"),(259,424,GARY),(425,425,"CLIPE"),
 (426,570,GARY),(571,574,MEL),(575,576,GARY),(577,584,MEL),(585,586,GARY),(587,588,MEL),(589,590,GARY),(591,600,MEL),
 (601,611,GARY),(612,622,"BRANDON, 58 ANOS (voluntário)"),(623,638,GARY),(639,642,"ROBERT CALLAHAN (NOVATECH LABS)"),(643,716,GARY),
 (717,731,"SYLVESTER STALLONE"),(732,732,GARY),(733,745,"ARNOLD SCHWARZENEGGER"),(746,749,GARY),(750,767,"DIANE HOLLOWAY (esposa do Ray)"),
 (768,794,GARY),(795,804,"DR. OZ (depoimento)"),(805,859,GARY),(860,866,"JOHNNY SINS"),(867,901,GARY),(902,908,MEL),(909,1008,GARY),(1009,1053,FAQ),
]
def spk(i):
    for a,b,l in spk_ranges:
        if a <= i <= b: return l
    raise SystemExit(f"sem falante para {i}")
blocks = [
 (0,"PRÉ-LEAD: apresentadora, o truque da gelatina de cavalo e a promessa"),
 (21,"DEPOIMENTOS RÁPIDOS: banheiro do trabalho, motorista de Uber, 'funcionou demais'"),
 (33,"APRESENTADORA: condições, 30 milhões de views, vídeo sem replay e os $97"),
 (50,"GARY BRECKA: quem é, a ligação de Mel Gibson e a promessa"),
 (79,"MEL GIBSON I: Rosalind Ross, as desculpas e a dependência do Viagra"),
 (114,"MEL GIBSON II: a noite que quebrou, 'it's okay', TRT e as bombas"),
 (152,"MEL GIBSON III: a festa, o cara de 40, 'este tem um pau que funciona' e o fim"),
 (192,"INVESTIGAÇÃO: 73 estudos, quem paga, PFAS, 3M/DuPont e a FDA"),
 (231,"EX-CIENTISTA DA FDA, memo 3M de 1998, Big Pharma $32 bi, Pfizer $47 mi e o insider"),
 (259,"GENX, GOLDMAN SACHS e o lodo no pasto, PFAS na chuva"),
 (291,"MECANISMO DO PROBLEMA I: esponja, colágeno tipo III, PFAS 14x, fibrose cavernosa"),
 (336,"MECANISMO DO PROBLEMA II: tipo I = cicatriz, a mangueira, declínio androgênico"),
 (383,"POR QUE NADA FUNCIONOU + os 60% do Mel e o ponto sem volta"),
 (413,"O RELÓGIO: 1,5–2% por ano, os 3 marcos, a rendição e a janela"),
 (461,"MECANISMO DA SOLUÇÃO I: colágeno de garanhão Percheron (DISSOLVE), Lexington, o equipamento de $1,4 mi e a régua"),
 (511,"MECANISMO DA SOLUÇÃO II–IV: Vitamina C lipossomal, Pycnogenol, Tongkat Ali + linha do tempo"),
 (552,"O PRIMEIRO HOMEM: Whitfield Farms, a cozinha de Mel, dia 4, dia 11, Rosalind volta, ressonância 60→38"),
 (604,"OS 37 VOLUNTÁRIOS, Brandon, 14 laboratórios, Robert Callahan, nasce o JellyRock, trial de 1.800"),
 (655,"APRESENTAÇÃO DO JELLYROCK: o que é, 4 substâncias, como tomar, FDA, selo e 'não importa'"),
 (716,"CELEBRIDADES: Stallone, Schwarzenegger e Diane Holloway"),
 (768,"ESCASSEZ (67 frascos), protocolo de 6 meses e Dr. Oz"),
 (805,"OFERTA: Nobel (54 homens), preços, kits, 15 minutos, 6 bônus e garantia"),
 (902,"FECHAMENTO: Mel, os dois caminhos, future pacing e 3 razões"),
 (1009,"FAQ PÓS-FECHAMENTO: perguntas de clientes"),
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
 "titulo": "HORSE JELLY SECRET (JELLYROCK) VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte": "Fonte: Horse Jelly Secret.ts (69:07, 404x720). Transcrição: AssemblyAI (universal-3-5-pro, speaker labels). Tradução fiel: nomes, marcas, valores em dólares, polegadas e referências dos EUA mantidos exatamente como falados.",
 "nota_prints": "Timing: cada mini-bloco traz o intervalo de tempo x → y em que aquela fala acontece no vídeo. Prints: N frames dos momentos mais importantes (provas, estudos, ambientes, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr": "'Jerry Blackdot' → 'Gary Brecka'; 'GeneX' → 'GenX'; 'Les' → 'Less'; nome 'Tongkat Ali' omitido pelo ASR em 35:00 inserido entre colchetes; '30 35' → '35'; trechos marcados [ASR: '…'] onde o áudio não permite certeza; reticências (…) indicam cortes de edição no áudio original. Inconsistências do original mantidas (94% vs 96%, trial de 1.800 vs 3.000, 5 vs 6 bônus).",
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
