import json, re
W='VSL-Pipeline-DIVINE'
S=json.load(open(f'{W}/sentences.json'))
by={s['i']:s for s in S}
fix={14:"He and Dr. Amir Shalev, an Israeli neuroscientist, mapped the vibrations of these verses into exact sound frequencies.",15:None,
     22:"It was not just relief; it was cellular restoration.",
     36:"Some had been living with chronic pain for years: knee problems, back problems, migraines.",
     37:"After just a few days of listening to the same prayer tones, their pain simply vanished.",
     43:"Because it was censored, Raymond."}
for i,t in fix.items():
    if t is None: del by[i]
    else: by[i]['text']=t
S=[by[k] for k in sorted(by)]
RAY="RAYMOND ARROYO (apresentador, Arroyo Grande Podcast, avatar)"; MEL="MEL GIBSON (avatar)"; WARN="VOZ DO AVISO ('WARNING')"
SPK={"A":RAY,"B":MEL,"C":WARN}
def spk(s): return SPK[s['speaker']]
blocks=[(0,"PRÉ-LEAD: Raymond Arroyo, 'milagres de cura só na Bíblia?', Mel Gibson tem a prova viva (frequências esquecidas)"),
 (5,"MEL GIBSON I: corpo quebrado, dores crônicas sem diagnóstico, o Pastor Samuel e o manuscrito hebraico"),
 (12,"MEL GIBSON II: Dr. Amir Shalev mapeia os versículos em frequências sonoras, a primeira manhã e a 'restauração celular'"),
 (23,"MEL GIBSON III: 'você parece 10 anos mais jovem', o familiar (glicose, pressão, memória em 7 dias) e a equipe do filme"),
 (41,"A OBJEÇÃO ('por que a igreja nunca ouviu falar?'): censura, 2 imperadores romanos no século 4, a caverna em Jerusalém em 1938"),
 (46,"GANCHO PARA O PASTOR: 'frequências divinas', o monopólio da indústria farmacêutica, Matusalém e Noé"),
 (51,"AVISO 'WARNING': removido do YouTube, 'você foi escolhido', 'não sei quanto tempo esta página fica no ar' e a entrada do pastor")]
starts=[b[0] for b in blocks]+[10**9]
def tsd(ms): s=int(ms//1000); return f"{s//60}:{s%60:02d}"
out=[]
for n,(st,title) in enumerate(blocks,1):
    sents=[s for s in S if st<=s['i']<starts[n]]
    minis=[];cur=[]
    for s in sents:
        if cur and (s['start_ms']-cur[0]['start_ms'])/1000>=30: minis.append(cur);cur=[]
        cur.append(s)
    if cur: minis.append(cur)
    if len(minis)>1 and (minis[-1][-1]['end_ms']-minis[-1][0]['start_ms'])<8000:
        last=minis.pop(); minis[-1].extend(last)
    mb=[]
    for m in minis:
        falas=[]
        for s in m:
            sp=spk(s)
            if falas and falas[-1]['falante']==sp: falas[-1]['en']+=' '+s['text']
            else: falas.append({"falante":sp,"en":s['text'],"pt":""})
        mb.append({"inicio":tsd(m[0]['start_ms']),"fim":tsd(m[-1]['end_ms']),"prints":[],"falas":falas})
    out.append({"n":n,"titulo":title,"inicio":mb[0]['inicio'],"fim":mb[-1]['fim'],"mini":mb})
fal=[]
for b in out:
    for m in b['mini']:
        for f in m['falas']:
            if f['falante'] not in fal: fal.append(f['falante'])
doc={"titulo":"DIVINE HEAL APP — LEAD (0:00 a 3:40) — Transcrição EN + Tradução PT-BR + Prints",
 "fonte":"Fonte: 'Divine Heal App 17/08' (Drive, 52:13 no total; extraído apenas 0:00 → 3:40 a pedido). Vídeo vertical 404x720. Transcrição: AssemblyAI (speaker labels). Tradução fiel: nomes, marcas e referências mantidos. Formato: entrevista falsa em estilo podcast com avatares de Raymond Arroyo (lower third 'Host, Arroyo Grande Podcast') e Mel Gibson (lower third 'Director, Flight Risk'), legendas em caixa alta amarela, cena de 'Nós Que Aqui Estamos' (Mel de capacete), b-roll de Mel em oficina e idoso à porta; aos 3:23 entra a cartela 'WARNING' e aos 3:40 o pastor com o pergaminho.",
 "nota_prints":"Timing: cada mini-bloco traz o intervalo x → y em que a fala acontece no vídeo. Prints: frames dos momentos mais importantes (lower thirds, legendas-chave, b-roll, cartela de aviso), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr":"'Dr.' + 'Amir Shalev' unidos; travessões do ASR normalizados; 'censored Raymond' pontuado como vocativo. O trecho termina no início da fala do pastor (3:40), por isso o último bloco fecha com a cartela de aviso.",
 "falantes":fal,"frames_dir":f"{W}/frames","img_width_in":2.35,"blocos":out}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'blocos',sum(len(b['mini']) for b in out),'minis',sum(len(m['falas']) for b in out for m in b['mini']),'falas')
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']): f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
