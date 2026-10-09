import json, re
W = 'VSL-Pipeline-ALPHAEREC'
S = json.load(open(f'{W}/sentences.json'))
by = {s['i']: s for s in S}
fix = {
 90: "Top 5 in the United States [ASR: \"5 inches\"] in the health category for 4 years in a row.",
 239: "Peter's door.",
 593: "[Tongkat Ali.] This one reactivates.",
 613: None,
 862: "The first bonus is the Johnny Sins Manual, How to Use Your New Dick, a technical guide created in partnership with the most well-known American porn actor in the…",
 190: "It was gentleness, like someone lifting a… She took my hand like she was taking a crying child off their lap, and my dick sat there in her hand, limp, naked, warm from the drug that had gotten into my bloodstream but hadn't gotten where it needed to go.",
}
for i, t in fix.items():
    if t is None: del by[i]
    else: by[i]['text'] = t
# nome do produto
for i in by:
    by[i]['text'] = re.sub(r'\bAlpha ?(Erych|Eryc|Eryk|Erek|Eric|Erec)\b', 'Alpha Erec', by[i]['text'])
def merge(a, b):
    by[a]['text'] += ' ' + by[b]['text']; by[a]['end_ms'] = by[b]['end_ms']; del by[b]
merge(22, 23); merge(24, 25); merge(29, 30); merge(60, 61); merge(80, 81); merge(238, 239); merge(820, 821); merge(883, 884)
# 862: dividir narrador / Johnny Sins
by[862.5] = {"i": 862.5, "speaker": "P", "start_ms": by[862]['start_ms'] + 9000, "end_ms": by[862]['end_ms'],
             "text": "I'm Johnny Sins, 46 years old, over 2,000 professional films in 15 years of career."}
by[862]['end_ms'] = by[862]['start_ms'] + 9000
S = [by[k] for k in sorted(by)]

NAR = "NARRADOR (DR. PETER ATTIA)"; SLY = "SYLVESTER STALLONE"
spk_ranges = [
 (0,1,"APRESENTADOR"),(2,25,"ATOR PORNÔ EX-BRAZZERS"),(26,30,"APRESENTADOR"),(31,54,NAR),
 (55,57,"HOMEM, 78 ANOS (depoimento)"),(58,64,"HOMEM, 64 ANOS (depoimento)"),(65,72,"MULHER (depoimento, namorada)"),
 (73,139,NAR),(140,216,SLY),(217,217,"CLIPE"),(218,239,SLY),(240,277,NAR),(278,282,"EX-CIENTISTA DA FDA"),(283,297,NAR),
 (298,303,"EX-EXECUTIVO DA BIG PHARMA (depoimento)"),(304,634,NAR),(635,639,SLY),(640,641,NAR),(642,653,SLY),(654,668,NAR),
 (669,679,"BRANDON, 58 ANOS (voluntário)"),(680,696,NAR),(697,701,"ROBERT CALLAHAN (NOVATECH LABS)"),(702,714,NAR),
 (715,717,"VOLUNTÁRIO ANÔNIMO (depoimento)"),(718,777,NAR),(778,778,NAR),(779,793,"ARNOLD SCHWARZENEGGER"),(794,794,NAR),
 (795,810,"JEAN-CLAUDE VAN DAMME"),(811,816,NAR),(817,832,"DIANE HOLLOWAY (esposa do Ray)"),(833,862,NAR),(862.5,868,"JOHNNY SINS"),
 (869,894,NAR),(895,900,SLY),(901,986,NAR),
]
def spk(i):
    for a,b,l in spk_ranges:
        if a <= i <= b: return l
    raise SystemExit(f"sem falante para {i}")
blocks = [
 (0,"PRÉ-LEAD: apresentador e o ator pornô ex-Brazzers revelam o truque"),
 (31,"LEAD: gelatina 6x mais potente que o Viagra, 36.600 homens, atores pornô e a Big Pharma"),
 (55,"DEPOIMENTOS DE ABERTURA (78 anos, 64 anos, namorada) + promessa"),
 (79,"QUEM É O DR. PETER ATTIA: Stanford, The Drive e o amigo Sylvester Stallone"),
 (117,"A LIGAÇÃO DE SÁBADO: 3 podcasts cancelados, $350.000 e as 3 coisas"),
 (140,"STALLONE I: Jennifer, as desculpas, o Viagra e a noite de quinta ('it's okay, Sly')"),
 (196,"STALLONE II: TRT, a academia, o café de Beverly Hills e 'he's more of a man than you'"),
 (240,"INVESTIGAÇÃO: 73 estudos, quem paga, glifosato / Roundup, Bayer Monsanto e a FDA"),
 (278,"EX-CIENTISTA DA FDA, memo 04 Beta (1998), Big Pharma $32 bi, Pfizer $47 mi e o insider"),
 (304,"BILL GATES, o carrapato Lone Star, a carne vegetal e as 3 corporações"),
 (328,"MECANISMO DO PROBLEMA I: corpo cavernoso, colágeno tipo III, glifosato 14x"),
 (363,"MECANISMO DO PROBLEMA II: fibrose oxidativa, tipo I = cicatriz, placas tóxicas e a mangueira"),
 (421,"POR QUE NADA FUNCIONOU + Bayer Monsanto tem nome"),
 (446,"O RELÓGIO: os 60% do Stallone, 0,3% por bife, os 3 marcos e a rendição"),
 (514,"MECANISMO DA SOLUÇÃO I: colágeno de garanhão Percheron (DISSOLVE), Lexington, $1,4 mi e a régua"),
 (568,"MECANISMO DA SOLUÇÃO II–IV: Vitamina C lipossomal, Pycnogenol, Tongkat Ali + linha do tempo"),
 (616,"O PRIMEIRO HOMEM: Whitfield Farms, a cozinha de Stallone, dia 4, dia 11, ressonância 60→38"),
 (659,"OS 37 VOLUNTÁRIOS, Brandon, 14 laboratórios, Robert Callahan, nasce o Alpha Erec, trial de 3.000"),
 (718,"APRESENTAÇÃO DO ALPHA EREC: o que é, 4 substâncias, como tomar, FDA e 'não importa'"),
 (778,"CELEBRIDADES: Schwarzenegger, Van Damme e Diane Holloway"),
 (833,"ESCASSEZ (67 frascos) e OFERTA: kits, preços, 5 bônus e garantia de 60 dias"),
 (895,"FECHAMENTO: Stallone, os dois caminhos, future pacing e 3 razões"),
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
 "titulo": "ALPHA EREC VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte": "Fonte: OT237ED - Troca de Produto - EXTERNO ALPHAEREC - Interna - 11.08.2026.mp4 (63:26, 1080x1920). Transcrição: AssemblyAI (universal-3-5-pro, speaker labels). Tradução fiel: nomes, marcas, valores em dólares, polegadas e referências dos EUA mantidos exatamente como falados.",
 "nota_prints": "Timing: cada mini-bloco traz o intervalo de tempo x → y em que aquela fala acontece no vídeo. Prints: N frames dos momentos mais importantes (provas, estudos, ambientes, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr": "Nome do produto normalizado para 'Alpha Erec' (ASR: Erych/Eryc/Eryk/Erek/Eric); 'Top 5 inches' → 'Top 5 in'; 'Dr. Peters' → 'Dr. Peter's'; nome 'Tongkat Ali' omitido pelo ASR em 39:18 inserido entre colchetes; 'Dr. Brazza' mantido como falado (nome do médico citado pelo ator); a narração alterna 3 vozes sintéticas (rótulos C/D/E da diarização) unificadas como NARRADOR; reticências (…) indicam cortes de edição no áudio original. Inconsistências do original mantidas (trial de 3.000 vs 1.800; 2 vs 2,5 polegadas aos 21 dias; 3-5 vs 3,5 polegadas).",
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
