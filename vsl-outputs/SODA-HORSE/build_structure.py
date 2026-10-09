import json, re
W = 'VSL-Pipeline-SODA-HORSE'
S = json.load(open(f'{W}/sentences.json'))
by = {s['i']: s for s in S}

# --- correções óbvias de ASR (texto EN) ---
fix = {
 44: "I'm 54.",
 309: "Josh wasn't more of a man than Kevin.",
 635: "The guy from the kitchen camera, wanna be the first?",
 706: "29 years in pharmaceutical R&D, and I had never seen fibrosis reversal in a registered study.",
 722: "His name is Soda Horse Peak.",
 796: "30 days and I started waking up with a rock hard dick [ASR: \"heart\"].",
 836: "You dissolve 30 years of cement, rebuild the entire sponge [ASR: \"spine, plunge\"], and shield it so it never comes back.",
 905: "Where to touch, with what pressure, at what rhythm, to make her cum 3, 4 [times]. Value: $497.",
 952: "I showed you Kevin, Stallone, Ford, Carol, crying because she missed her own husband.",
 188: "Inside that bedroom, he was just a man with a dead dick [?? \"neck meat\" ??].",
}
for i, t in fix.items(): by[i]['text'] = t
for i in by:
    by[i]['text'] = re.sub(r'\b(Sota ?Horse|Sodahorse|Sotahorse|soda horse peak)\b', 'Soda Horse Peak', by[i]['text'].replace('Soda Horse Peak', 'Soda Horse Peak'))
    by[i]['text'] = by[i]['text'].replace('Soda Horse Peak Peak', 'Soda Horse Peak')
# merges (frase quebrada em "Dr." / "F.")
def merge(a, b):
    by[a]['text'] += ' ' + by[b]['text']; by[a]['end_ms'] = by[b]['end_ms']; del by[b]
merge(48, 49); merge(64, 65); merge(252, 253)
# 129: dividir em NARRADOR + KEVIN
by[129]['text'] = "Kevin, you called [me]."
by[129.5] = {"i": 129.5, "speaker": "B", "start_ms": by[129]['end_ms'], "end_ms": by[130]['start_ms'], "text": "You're a doctor, Pete."}
S = [by[k] for k in sorted(by)]

NAR = "NARRADOR (DR. PETER ATTIA)"
spk_ranges = [
 (0,38,NAR),(39,43,"SYLVESTER STALLONE"),(44,51,"HOMEM, 54 ANOS (depoimento)"),(52,56,"MULHER, 55 ANOS (depoimento)"),
 (57,95,NAR),(96,96,"CHRISTINE (ex-esposa do Kevin)"),(97,106,NAR),(107,107,"CLIPE"),(108,129,NAR),
 (129.5,138,"KEVIN COSTNER"),(139,139,NAR),(140,173,"KEVIN COSTNER"),(174,182,NAR),(183,204,"CHRISTINE (ex-esposa do Kevin)"),
 (205,211,NAR),(212,212,"CHRISTINE (ex-esposa do Kevin)"),(213,224,NAR),(225,225,"CLIPE"),(226,253,NAR),(254,254,"CLIPE"),
 (255,258,"ROBERT F. KENNEDY JR."),(259,261,NAR),(262,262,"ROBERT F. KENNEDY JR."),(263,275,NAR),(276,279,"EX-REVISOR DA FDA"),
 (280,352,NAR),(353,353,"CLIPE"),(354,508,NAR),(509,509,"CLIPE"),(510,639,NAR),(640,642,"KEVIN COSTNER"),(643,645,NAR),
 (646,656,"KEVIN COSTNER"),(657,671,NAR),(672,674,"MULHER JOVEM (depoimento)"),(675,684,NAR),(685,688,"MULHER, 4 DA MANHÃ (depoimento)"),
 (689,705,NAR),(706,709,"DAVID HARTMAN (MERIDIAN LABS)"),(710,786,NAR),(787,790,"SYLVESTER STALLONE"),(791,791,NAR),
 (792,800,"HARRISON FORD"),(801,802,NAR),(803,813,"AS DUAS IRMÃS (depoimento)"),(814,819,NAR),(820,825,"CAROL (esposa do Dale)"),
 (826,838,NAR),(839,843,"ANDREW HUBERMAN"),(844,892,NAR),(893,897,"JOHNNY SINS"),(898,921,NAR),(922,928,"KEVIN COSTNER"),(929,993,NAR),
]
def spk(i):
    for a,b,l in spk_ranges:
        if a <= i <= b: return l
    raise SystemExit(f"sem falante para {i}")

blocks = [
 (0,"LEAD / GANCHO: o truque do bicarbonato de cavalo"),
 (39,"DEPOIMENTOS DE ABERTURA (Stallone, homem de 54, mulher de 55) + promessa"),
 (62,"QUEM É O DR. PETER ATTIA e a vergonha de 13 anos"),
 (81,"HISTÓRIA: Kevin Costner, a ligação de sábado e a frase da esposa"),
 (129,"DEPOIMENTO KEVIN: as costas viradas, o vizinho e a câmera na cozinha"),
 (174,"DEPOIMENTO CHRISTINE: o vizinho, o volume e o pó"),
 (205,"O RANCHO, OS CAVALOS e a suspeita do tamanho"),
 (230,"A INVESTIGAÇÃO: quem financia os estudos, glifosato / Roundup, RFK Jr."),
 (263,"A CONSPIRAÇÃO: memo da Bayer (1998), FDA, Big Pharma e o vídeo derrubado"),
 (293,"O MUNDO DOS GARANHÕES: o pó secreto dos haras e o cavalo que escapa"),
 (322,"MECANISMO DO PROBLEMA I: a esponja de colágeno tipo III e o cimento"),
 (356,"MECANISMO DO PROBLEMA II: tamanho travado aos 15, as 7 polegadas e a placa tóxica"),
 (403,"POR QUE NADA FUNCIONOU (Viagra, TRT, prótese) e o relógio do cimento"),
 (458,"A RESPOSTA NO CAVALO: criadores, veterinário e os 4 passos"),
 (495,"MECANISMO DA SOLUÇÃO I: bicarbonato preparado (DISSOLVER)"),
 (532,"MECANISMO DA SOLUÇÃO II: colágeno de garanhão Percheron (RECONSTRUIR) + régua e ressonância"),
 (576,"MECANISMO DA SOLUÇÃO III e IV: Pycnogenol (PROTEGER) e Tongkat Ali (REATIVAR) + linha do tempo"),
 (630,"O PRIMEIRO HOMEM: Kevin toma o pó, a ressonância e os garanhões irmãos"),
 (675,"OS 37 VOLUNTÁRIOS, os laboratórios, David Hartman e o trial de 3.000"),
 (722,"APRESENTAÇÃO DO SODA HORSE PEAK: o que é, os 4 ingredientes, como tomar, selo"),
 (786,"CELEBRIDADES E DEPOIMENTOS: Stallone, Harrison Ford, as duas irmãs, Carol"),
 (826,"ESCASSEZ (67 frascos), protocolo de 4 a 6 meses e Andrew Huberman"),
 (844,"OFERTA: preços, kits, urgência (15 minutos), bônus e Garantia do Garanhão"),
 (922,"FECHAMENTO: Kevin, os dois caminhos, future pacing, 3 razões e CTA"),
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
    # mini muito curto no fim (< 8 s) junta ao anterior
    if len(minis) > 1 and (minis[-1][-1]['end_ms'] - minis[-1][0]['start_ms']) < 8000:
        last = minis.pop(); minis[-1].extend(last)
    mb = []
    for m in minis:
        falas = []
        for s in m:
            sp = spk(s['i'])
            if falas and falas[-1]['falante'] == sp:
                falas[-1]['en'] += ' ' + s['text']
            else:
                falas.append({"falante": sp, "en": s['text'], "pt": ""})
        mb.append({"inicio": tsd(m[0]['start_ms']), "fim": tsd(m[-1]['end_ms']), "s0": m[0]['i'], "prints": [], "falas": falas})
    out.append({"n": n, "titulo": title, "inicio": mb[0]['inicio'], "fim": mb[-1]['fim'], "mini": mb})

falantes = []
for _,_,l in spk_ranges:
    if l not in falantes: falantes.append(l)
doc = {
 "titulo": "SODA HORSE PEAK VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte": "Fonte: OT249ED - M01_C01 - SODA HORSE P - OT248_SPY - INTERNA - 11.09 pitch.mp4 (66:39, 1080x1920). Transcrição: AssemblyAI (universal-3-5-pro, speaker labels). Tradução fiel: nomes, marcas, valores em dólares, polegadas e referências dos EUA mantidos exatamente como falados.",
 "nota_prints": "Timing: cada mini-bloco traz o intervalo de tempo x → y em que aquela fala acontece no vídeo. Prints: N frames dos momentos mais importantes (provas, estudos, ambientes, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "falantes": falantes, "frames_dir": f"{W}/frames", "img_width_in": 2.35, "blocos": out,
}
total = sum(len(m['falas']) and 0 for b in out for m in b['mini'])
nsent = sum(1 for b in out for m in b['mini'] for _ in m['falas'])
json.dump(doc, open(f'{W}/doc.json','w'), ensure_ascii=False, indent=1)
nm = sum(len(b['mini']) for b in out); nf = sum(len(m['falas']) for b in out for m in b['mini'])
print(len(out), "blocos,", nm, "mini-blocos,", nf, "falas,", sum(len(f['en'].split()) for b in out for m in b['mini'] for f in m['falas']), "palavras EN")
with open(f'{W}/estrutura.txt','w') as f:
    for b in out:
        f.write(f"\nBLOCO {b['n']} — {b['titulo']}  [{b['inicio']} – {b['fim']}]\n")
        for k,m in enumerate(b['mini'],1):
            f.write(f"  {b['n']}.{k} ⏱ {m['inicio']} → {m['fim']}  " + " | ".join(f"{x['falante']}: {x['en'][:60]}…" for x in m['falas']) + "\n")
