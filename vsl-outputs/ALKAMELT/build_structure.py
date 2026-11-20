import json
W='VSL-Pipeline-ALKAMELT'
S=json.load(open(f'{W}/sentences.json'))
by={s['i']:s for s in S}
fix={2:"I'm Dr. Ania Jastreboff, weight loss specialist for women over 40.",3:None,
     12:"The real baking soda shot, the one that helped me drop 56 pounds in 45 days, came from Dr. Ania.",13:None,
     24:"Then I switched to the real recipe Dr. Ania showed, and look what happened.",25:None,
     29:"Thank God I found Dr. Ania's video teaching the real baking soda water shot.",30:None,
     6:"Just one glass of this recipe every morning.",
     21:"And when you take it the right way, it cleans your intestine from the inside out, waking up your fat-burning hormones and triggering a process that can melt up to 1 pound of fat a day.",
     35:"That's why I went on Today with Oprah and revealed the real recipe on live TV, step by step.",
     43:"Big Pharma is making $50 billion a year on weight loss injections. A natural recipe that costs less than a dollar and works better than their drugs?",
     64:None,65:None,66:None,67:None,
     129:"And that's when Dr. Ania explained something to me that changed everything.",130:None,
     136:"And speaking of Dr. Ania, she's actually here with us today.",137:None,
     138:"Dr. Ania Jastreboff is a Yale-trained obesity specialist.",139:None,
     144:"Dr. Ania, welcome.",145:None,
     147:"Now, before you show us how to make the baking soda recipe, I have to ask what everyone watching is thinking right now.",
     154:"When you eat, it's not your… It's GLP-1 and GIP sending a signal that says, we're good, stop eating, start burning.",
     188:"According to the latest research, after you stop, losing weight becomes up to 5 times harder than it was before you ever took… Wait, 5 times harder?",
     203:"Your L cells, the gut cells responsible for producing GLP-1 and GIP, are like seeds waiting to grow, but if the soil is too acidic, nothing grows.",
     206:"Your L cells are… They're still there, but they've gone to sleep.",207:None,
     217:"Dr. Ania, I think everyone watching right now is grabbing a pen.",218:None,
     236:"That's… Now I get why you keep saying it's not about willpower, Oprah.",
     240:"Okay, Dr. Ania, how do we actually make this baking soda recipe?",241:None,
     264:"So now you have 2 pieces working together: baking soda to wake up your L cells and get your body producing GLP-1 and GIP again, and gingerol to protect those hormones from being destroyed.",
     297:"When Dr. Ania first showed me the studies behind all of this, I was shocked.",298:None,
     308:"The problem is that your system got thrown off by stress, by processed food, by the chemicals in everything we eat.",
     340:"Okay, Dr. Ania, I have to ask because I know everyone watching is thinking the same thing.",341:None,
     359:"So most people don't have the equipment or the knowledge to get this right at home. And that's exactly what I told her.",
     364:"So I reached out to BioActive Naturals, the only lab I knew that could actually produce this at the quality we needed. They've been doing this for over 25 years.",
     384:"This science shouldn't be locked behind… This is the first and only formula designed to restore your gut's natural balance and turn your body's own GLP-1 and GIP production back on.",
     387:"I've been taking this for 2 months now.",388:"AlkaMelt works with your body, not against it.",
     392:"But Dr. Ania, what makes AlkaMelt different from all the other solutions out there?",393:None,
     410:"It reactivates fat-burning mode so your body stops storing and starts burning, and it protects your hormones from being destroyed so the results actually last.",
     425:"Studies show it can accelerate skin healing by up to… So you don't just lose weight, you actually look younger.",
     431:"I get messages every day from women showing me their before and after photos.",432:None,
     451:"Okay, Dr. Ania, before we get into how to get AlkaMelt, just walk us through real quick.",452:None,
     486:"AlkaMelt isn't just safe, it's actually recommended for women dealing with thyroid imbalances, prediabetes, or high cholesterol.",
     495:"Patients who've tried everything and failed, those are the ones I put on AlkaMelt, and the results speak for themselves.",
     497:"And unlike with the… Over 6 months, AlkaMelt has proven to be safer and more effective than anything I've seen.",
     510:"Cheap ingredients, generic doses, zero personalization. That's why AlkaMelt is different.",
     512:"This tells us exactly what your body needs, so we can customize it.",
     521:"Along with your kit, you get access to our brand new AlkaMelt app.",523:None,
     531:"Every AlkaMelt member gets 2 free consultations per month.",
     549:"Okay, Dr. Ania, I have to say, this is unlike anything I've seen.",550:None,
     558:"By the end of week 1, energy's up, bloating's down, and your clothes start fitting different.",
     562:"So your cravings disappear, your energy stabilizes, and your body finally starts burning instead of storing. But here's where it gets really interesting.",
     563:"After 3 months… Yeah, that's when people started stopping me.",
     590:"Now, Dr. Ania, how do people actually get AlkaMelt?",591:None,
     600:"Gayle called me like, Oprah, what is this? I need it!",601:None,
     611:"Okay, Dr. Ania, I know everyone at home is thinking the same thing right now.",612:None,
     617:"You also won't find it on Amazon or eBay.",618:None,
     624:"When we first launched, one bottle cost $185, and people were happy to pay it because it worked.",
     642:"That brings your cost down from $198 [ASR; dito $185 antes] to just $49 per bottle, saving you over $300.",
     667:"It's taught by my friend Dr. Lauren Sinclair, the nutritionist who preps Victoria's Secret models before their shows, and she agreed to share the secrets that never leave the fashion world's inner circle.",668:None,
     677:"It's called the Youth Glow Masterclass, and it's taught by Dr. Ellen Marmur, a world-renowned dermatologist.",678:None,
     687:"I've actually consulted with Dr. Marmur in person twice.",688:None,
     689:"I paid $7,000 each time, and the information in this masterclass, it's the same stuff she told me in her office.",
     707:"I've paid way more than $10,000 for specialists who don't even come close to Dr. Ania.",708:None,
     713:"The Runway Waist Formula with Dr. Lauren Sinclair, valued at $247.",714:None,
     715:"The Youth Glow Masterclass with Dr. Ellen Marmur, worth $150.",716:None,
     717:"And if you're one of the first 50, a private one-on-one consultation with Dr. Ania herself, worth $10,000.",718:None,
     723:"Now, Dr. Ania, we actually got a message here from a viewer asking about guarantees.",724:None,
     726:"I completely understand, and honestly, that question comes up a lot because most people watching have been through it.",
     728:"And that's why I did something different with AlkaMelt, because this isn't another Band-Aid, another empty promise.",
     746:"Most orders arrive within 3 to 5 business days, and once it gets there, you just take 5 drops every morning before breakfast.",
     750:"Your brain finally gets the message, we're good, stop eating, and your metabolism switches back into fat-burning mode 24 hours a day, 7 days a week. That's why women are losing 15, 20, even 30 pounds a month on AlkaMelt.",
     770:"Dr. Ania, before we go, anything else you want to say to everyone watching?",771:None,
     772:"Just this: if you've made it this far, you've seen everything: how AlkaMelt works, why it works, the science behind it, the real results, and you know your investment is protected.",
     789:"If I could do it after all these years, after every failure, every headline, every public humiliation.",
     799:"Someone takes a photo and you don't run to the back.",
     807:"Well, Oprah, Dr. Ania, thank you so much for being here with us on Today.",808:None,809:None,
     817:"Most people are going with the 6-bottle kit because they don't want to run out halfway. Once it sells out, that's it.",
     }
for i,t in fix.items():
    if t is None: del by[i]
    else: by[i]['text']=t
import re
for i in by: by[i]['text']=re.sub(r'\b(Alka-?Melt|Alkamel|Alkamil|AlkaMilt|Alchemelt|Alka Melt)\b','AlkaMelt',by[i]['text'])
def merge(a,b): by[a]['text']+=' '+by[b]['text']; by[a]['end_ms']=by[b]['end_ms']; del by[b]
S=[by[k] for k in sorted(by)]
ANIA="DRA. ANIA JASTREBOFF (avatar)"; OPRAH="OPRAH WINFREY (avatar)"; HODA="SHEINELLE JONES (apresentadora, Today, avatar)"; JENNA="JENNA BUSH HAGER (apresentadora, Today, avatar)"
SPK={"A":ANIA,"B":OPRAH,"C":"MULHER 1 (depoimento)","D":"MULHER 2 (depoimento, pós-parto)","E":HODA,"F":JENNA,"G":"MÃE (depoimento, bebê)","H":"MULHER DE 50 ANOS (depoimento)","I":"MÉDICA 2 (depoimento)","J":"JESSICA SIMPSON (avatar, depoimento ex-Mounjaro)","K":"MULHER 4 (depoimento, 40+)"}
over={59:"B",115:"F",495:"MED1",754:"J"}
def spk(s):
    o=over.get(s['i'])
    if o=="MED1": return "MÉDICA 1 (depoimento)"
    return SPK[o or s['speaker']]
blocks=[(0,"PRÉ-LEAD: o shot de bicarbonato errado, Dra. Ania Jastreboff e a receita que a Oprah usou (56 libras em 45 dias)"),
 (14,"LEAD: por que a receita errada desliga o GLP-1 e o GIP, os 2 ingredientes, depoimentos e a promessa (7 libras na 1ª semana ou rasgo o diploma de Yale)"),
 (47,"ABERTURA DO 'TODAY': a jornada da Oprah, Ozempic, o rebote e o ritual matinal"),
 (68,"ENTREVISTA I: a liberdade, o 'food noise', a frase do pai ('você sempre vai ser grande')"),
 (107,"ENTREVISTA II: Ozempic/Mounjaro, os 20 libras de volta, 'tem que haver outro jeito' e a entrada da Dra. Ania"),
 (149,"MECANISMO DO PROBLEMA I: GLP-1 e GIP, o corpo em pânico, 'não é disciplina'"),
 (175,"MECANISMO DO PROBLEMA II: as injeções substituem os hormônios, o corpo desliga, o rebote 5x mais difícil"),
 (195,"MECANISMO DA SOLUÇÃO I: bicarbonato neutraliza o ácido, o jardim e as células L adormecidas"),
 (220,"PROVA: o scan cerebral (Journal of Clinical Endocrinology, 2023)"),
 (243,"MECANISMO DA SOLUÇÃO II: a enzima DPP-4 e o gengibre (gingerol inibe 93%)"),
 (265,"MECANISMO DA SOLUÇÃO III: o interruptor metabólico AMPK e a berberina (estudo de Yale, 3x mais gordura)"),
 (296,"A COMBINAÇÃO EXATA, o ceticismo da Oprah e o resultado (56 libras em 3 meses, 72 anos)"),
 (340,"O PROBLEMA DA PUREZA e da proporção: por que não dá para fazer em casa"),
 (362,"NASCE O ALKAMELT: BioActive Naturals, fórmula líquida em gotas (10x mais rápido, 6x mais composto)"),
 (382,"APRESENTAÇÃO DO ALKAMELT: o que é, por que é diferente, NAD+ e a pele"),
 (434,"DEPOIMENTOS I: mãe (28 libras) e mulher de 50 anos (34 libras, biquíni)"),
 (451,"COMO TOMAR (5 gotas em jejum), segurança, tireoide/pré-diabetes e os médicos"),
 (502,"PERSONALIZAÇÃO (perfil de saúde), o app AlkaMelt, a Academy e o Inner Circle"),
 (549,"LINHA DO TEMPO: dia 1, semana 1, dia 30, 3 meses, 6 meses"),
 (589,"ESCASSEZ: lotes esgotados, 300 kits, 'eu sou a Oprah e esperei 3 semanas'"),
 (614,"OFERTA: por que não está em farmácias/Amazon, de $185 para $98 e para $49 (6 pelo preço de 3)"),
 (653,"COMO COMPRAR (botão verde/vermelho) e os 3 PRESENTES: Runway Waist, Youth Glow e consulta com a Dra. Ania"),
 (709,"RECAPITULAÇÃO DA OFERTA e GARANTIA de 60 dias"),
 (737,"O PROCESSO DE COMPRA, o que acontece no corpo e DEPOIMENTOS II"),
 (770,"FECHAMENTO: Oprah ('não é sua culpa, é biologia'), future pacing e encerramento do programa")]
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
fal=[]
for b in out:
    for m in b['mini']:
        for f in m['falas']:
            if f['falante'] not in fal: fal.append(f['falante'])
doc={"titulo":"ALKAMELT VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte":"Fonte: 'AlkaMelt 07/09' (Drive, 51:36). Transcrição: AssemblyAI (speaker labels). Tradução fiel: nomes, marcas, valores em dólares, libras e referências dos EUA mantidos como falados. Formato: VSL em estilo de programa de TV (Today) com avatares da Dra. Ania Jastreboff, da Oprah Winfrey e das apresentadoras Jenna Bush Hager e Sheinelle Jones (lower third 'Jenna & Sheinelle'), identificados pelas imagens. Vídeo vertical (9:16).",
 "nota_prints":"Timing: cada mini-bloco traz o intervalo x → y em que a fala acontece no vídeo. Prints: frames dos momentos mais importantes (letterings, provas, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr":"Nome do produto normalizado para 'AlkaMelt' (ASR: Alka-Melt, Alkamel, Alkamil, AlkaMilt, Alchemelt); 'Dr. Ania/Anya/Anea/Aneas' unificado como Dra. Ania; 'Dr. Marmar/Marmer' → Marmur; gaguejos e repetições removidos; reticências (…) marcam cortes de edição no áudio original. Inconsistências do roteiro mantidas: Oprah perde 56 libras em 45 dias (lead), 43 libras em 2 meses (9:17) e 56 libras em 3 meses (21:05); preço de lançamento $185 (38:44) e 'de $198 para $49' (40:01); 'menos de 300 frascos' no fechamento após '300 kits'.",
 "falantes":fal,"frames_dir":f"{W}/frames","img_width_in":2.35,"blocos":out}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'blocos',sum(len(b['mini']) for b in out),'minis',sum(len(m['falas']) for b in out for m in b['mini']),'falas')
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']): f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
