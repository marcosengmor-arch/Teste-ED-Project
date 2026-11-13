import json
W='VSL-Pipeline-VSL12'
S=json.load(open(f'{W}/sentences.json'))
by={s['i']:s for s in S}
fix={4:"Hollywood celebrities who paid up to $40,000 per session just so I would activate their third eye before signing multimillion-dollar movie deals.",
     172:None,173:None,
     122:"But if you don't activate this button, you simply get forgotten by the universe.",
     145:"And as the harpist played, the hand of the Lord came upon Elisha and he saw everything.",
     149:"The sequence of vibrations from David's harp is an exact key made to activate what's been switched off.",
     205:"It took months of processing, running day and night on a supercomputer until one Tuesday in the early hours of the morning at the lab, my lead engineer handed me a… [corte na edição]",
     281:"And the richest man on the planet is already saying in public what the elite has always known in silence.",
     343:"If I would release the David Song for free on the internet.",
     334:"You saw what they did to my Joe Rogan episode. 24 hours and it was gone.",335:None}
for i,t in fix.items():
    if t is None: del by[i]
    else: by[i]['text']=t
def merge(a,b): by[a]['text']+=' '+by[b]['text']; by[a]['end_ms']=by[b]['end_ms']; del by[b]
merge(95,96); merge(264,265); merge(432,433)
S=[by[k] for k in sorted(by)]
SPK={"A":"JOE DISPENZA (narrador, avatar)","B":"KANYE WEST (avatar, podcast)","C":"JIM CARREY (avatar)","D":"ELON MUSK (avatar)","E":"KIM KARDASHIAN (avatar)","F":"DR. OZ (avatar)","G":"OPRAH WINFREY (avatar)",
     "H":"JOE ROGAN (avatar, podcast)","I":"HOMEM (depoimento, promoção)","J":"DEPOIMENTO (diabetes tipo 2)","K":"IMIGRANTE MEXICANO (depoimento, Powerball)",
     "L":"NEUROCIENTISTA (depoimento)","M":"MÃE (depoimento, sonho do acidente)","N":"O CÉTICO DA FAMÍLIA (depoimento)"}
over={76:"H"}
def spk(s): return SPK[over.get(s['i'],s['speaker'])]
blocks=[(0,"LEAD: o botão da manifestação, o sistema Rockefeller, celebridades a $40.000 por sessão, Epstein e Bohemian Grove"),
 (26,"O capítulo censurado de The Secret, o episódio com Joe Rogan derrubado, o ritual de 15 segundos e as 2 pílulas"),
 (42,"QUEM É JOE DISPENZA: o botão nasceu com você, as 6 vértebras fraturadas, a glândula pineal e a pinha do Vaticano"),
 (67,"O ESCÂNDALO MAIOR QUE O DE EPSTEIN: as 3 famílias, os Rockefeller, os nazistas, o segredo dos judeus e 1945"),
 (94,"O SISTEMA: a corrida dos ratos, celebridades fantoches, rituais de iniciação e o programa tirado do ar"),
 (113,"MECANISMO: a antena (TV), as vibrações do universo e por que os judeus prosperam (Nobel, Forbes)"),
 (131,"A HARPA DO REI DAVI: Salomão, Saul (1 Samuel 16:23) e Eliseu (2 Reis 3:15)"),
 (151,"MICROCRISTAIS E PIEZOELETRICIDADE: a pineal como antena, a gota d'água e Jobs, Taylor Swift e Michael Jordan"),
 (169,"A RECONSTRUÇÃO: arquivos queimados, os fragmentos, o kinnor, a afinação (432 Hz) e a IA dos pergaminhos do Vesúvio"),
 (217,"O DAVID SONG: 7 vibrações em 7 noites, como usar e os primeiros sinais"),
 (233,"DEPOIMENTOS: a promoção, o diabetes e o Powerball de $4,7 milhões"),
 (263,"A NEUROCIENTISTA, os retiros de $50.000 e o depoimento de Elon Musk"),
 (289,"O PACTO DAS 7 NOITES e o future pacing"),
 (313,"PREÇO: de $5.000 para $39, e por que não é de graça"),
 (348,"ACESSO DIGITAL VITALÍCIO e GARANTIA de 60 dias"),
 (378,"DEPOIMENTOS: a mãe que sonhou com o acidente e o cético da família"),
 (402,"ESCASSEZ e OS 7 BÔNUS (valor total de $2.076)"),
 (460,"FECHAMENTO: as 2 portas")]
starts=[b[0] for b in blocks]+[10**9]
def tsd(ms): s=int(ms//1000); return f"{s//60}:{s%60:02d}"
out=[]
for n,(st,title) in enumerate(blocks,1):
    sents=[s for s in S if st<=s['i']<starts[n]]
    minis=[];cur=[]
    for s in sents:
        if cur and (s['start_ms']-cur[0]['start_ms'])/1000>=42: minis.append(cur);cur=[]
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
doc={"titulo":"DAVID SONG VSL — Transcrição EN + Tradução PT-BR + Prints","fonte":"","nota_prints":"","falantes":[],"frames_dir":f"{W}/frames","img_width_in":2.35,"blocos":out}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'blocos',sum(len(b['mini']) for b in out),'minis',sum(len(m['falas']) for b in out for m in b['mini']),'falas')
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']): f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
