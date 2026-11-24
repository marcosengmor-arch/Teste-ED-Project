import json, re
W='VSL-Pipeline-DREW'
S=json.load(open(f'{W}/sentences.json'))
by={s['i']:s for s in S}
fix={9:"So we've teamed up with women's telehealth company Midi Health, and joining us is their Chief Medical Officer, Dr. Kathleen Jordan.",10:None,
     15:"So thank you for doing this because…",
     44:"Is the not sleeping adding to the brain fog, or is that just completely something else?",
     70:"And the good news is there's a lot we can do, but realizing that our cholesterol goes up, our blood sugars go up, our weight and our waist goes up.",
     78:"What people don't realize is that muscle may look good, it looks toned, but it actually is metabolically active and actually helps your metabolism.",
     85:"That means walking right after you eat.",
     110:"And if you want more information, you can go to Midi Health and you can have an individualized experience with them.",
     121:"So thank you to Midi Health and Dr. Kathleen Jordan.",122:None,
     123:"Thank you, Dr. Jordan.",124:None,
     125:"It's an honor to talk about Midi Health."}
for i,t in fix.items():
    if t is None: del by[i]
    else: by[i]['text']=t
by[15.5]={"i":15.5,"speaker":"A","start_ms":by[15]['start_ms']+2000,"end_ms":by[15]['end_ms'],"text":"We do it all."}
by[15]['end_ms']=by[15]['start_ms']+2000
for i in by: by[i]['text']=re.sub(r'\bMiddie Health\b','Midi Health',by[i]['text'])
S=[by[k] for k in sorted(by)]
DREW="DREW BARRYMORE (apresentadora)"; VAL="VALERIE BERTINELLI (convidada, 'for Midi Health')"; DOC="DRA. KATHLEEN JORDAN (Chief Medical Officer, Midi Health)"; CO="COAPRESENTADORA (blazer branco)"
SPK={"A":DREW,"B":CO,"C":CO,"D":VAL,"E":DOC}
over={84:DREW,107:DREW}
def spk(s): return over.get(s['i']) or SPK[s['speaker']]
blocks=[(0,"ABERTURA: 'vamos falar de menopausa', não é um modelo único, parceria com a Midi Health e a Dra. Kathleen Jordan"),
 (14,"VALERIE, A PÓS-MENOPÁUSICA: 'queria ter tido isso 10, 15 anos atrás'"),
 (19,"SONO: suores noturnos, 20% sem fogachos mas sem dormir, estrogênio/serotonina e progesterona/GABA, o que checar"),
 (43,"BRAIN FOG: temporário, 'whatchamacallit', não é demência"),
 (54,"GANHO DE PESO: a barriga alta ('onde estão meus pés?'), metabolismo, colesterol e glicose, carboidratos, músculo, remédios de emagrecimento"),
 (81,"MOVIMENTO: passear com o cachorro, caminhada pós-prandial ('fart walk')"),
 (91,"TRH E A 'CABEÇA-DURA': 'não precisa viver a menopausa da sua mãe', não precisa aguentar calada"),
 (101,"A OFERTA MIDI HEALTH: clínicas especializadas, plano personalizado, consultas virtuais em todos os estados, cobertas por seguros"),
 (106,"HORMÔNIOS SUBUTILIZADOS, saúde óssea, 'fui dispensada por médicos' e ENCERRAMENTO (JoinMidi.com)")]
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
doc={"titulo":"DREW BARRYMORE SHOW × MIDI HEALTH (menopausa) — Transcrição EN + Tradução PT-BR + Prints",
 "fonte":"Fonte: 'Drew Barrymore Learns About Surprising Menopause Symptoms and How to Manage Them' (YouTube 7ZKsLCJFjbU, 6:45, 720p, via Drive). Segmento patrocinado ('Sponsored by Midi') do The Drew Barrymore Show. Transcrição: AssemblyAI (speaker labels). Tradução fiel: nomes, marcas e referências dos EUA mantidos. Falantes identificados pelos lower thirds: Drew Barrymore (blazer cinza), Valerie Bertinelli ('for Midi Health', óculos e jeans), Dra. Kathleen Jordan (Chief Medical Officer, Midi Health, blazer magenta) e uma coapresentadora de blazer branco (não identificada na tela).",
 "nota_prints":"Timing: cada mini-bloco traz o intervalo x → y em que a fala acontece no vídeo. Prints: frames dos momentos mais importantes (lower thirds, cartelas de tema, falantes, reações, CTA), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr":"'Middie Health' → Midi Health (lower third 'Sponsored by Midi' / 'www.JoinMidi.com'); 'Dr.' + 'Kathleen Jordan' unidos; 'We do it all' (0:48) separado como fala da Drew; 'What's that mean?' (4:35) e 'Yeah' (5:51) atribuídos à Drew; gaguejos removidos; reticências (…) marcam cortes.",
 "falantes":fal,"frames_dir":f"{W}/frames","img_width_in":2.35,"blocos":out}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'blocos',sum(len(b['mini']) for b in out),'minis',sum(len(m['falas']) for b in out for m in b['mini']),'falas')
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']): f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
