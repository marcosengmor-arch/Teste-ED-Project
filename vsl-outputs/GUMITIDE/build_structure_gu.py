import json, re
W='VSL-Pipeline-GUMITIDE'
S=json.load(open(f'{W}/sentences.json'))
by={s['i']:s for s in S}
fix={
 22:"I'm really glad you're here today because I'm joined by Jillian Michaels, the go-to weight loss specialist for celebrities, who has spent over 20 years behind some of the most dramatic body transformations, helping women completely transform their bodies and take back their confidence, their health, and their lives.",
 84:"My hands started shaking as I picked it up, and then I saw it— me on the cover in big bold letters.",
 118:"The weight kept piling, bloating, water retention.",
 139:"But there's one thing I can't wrap my head around.",
 159:"Think of it like a mom taking her child, glucose, into school— your cells.",
 180:"That's because when you eat, it's not your full stomach that sends the signal to stop.",
 188:"So even when a woman is on a diet, fasting, and going to the gym every day, without these hormones, her body is still turning the food into fat?",
 200:"And the proof is right here: a major clinical trial published in the New England Journal of Medicine proved that women who activate both their GLP-1 and GIP hormones naturally lose up to 21 times more weight than those who rely on diet and exercise alone.",
 203:"Wow.",
 214:"But why do Mounjaro and these other weight loss pens cause such a… The problem is that those shots don't stimulate these hormones, they replace them.",
 222:"My God, Dr. Ania, is what's happening to Oprah normal?",223:None,
 231:"That way, my GLP-1 and GIP levels will stay high forever.",
 240:"And I actually remember that the former CMS administrator, Dr. Oz himself, held a press conference at the Department of Health recently addressing exactly this issue.",241:None,
 246:"And that's exactly why drugs like Ozempic and Mounjaro exploded in popularity almost… They force your body to mimic these 2 hormones, and yes, the weight comes off fast.",
 251:"And now the consequences are starting to surface.",252:None,
 257:"The risk is significantly higher for women at that age because the hormonal environment is already fragile because of menopause, and forcing synthetic hormones on top of that creates a dangerous chemical conflict in the body.",
 259:"But as Dr. Oz said, the risk to your health is enormous, isn't it, Jillian?",260:None,
 269:"And that's exactly why my team and I spent a long time researching a way to raise GLP-1 and GIP levels the same way these weight loss shots do, but naturally and 100% safely.",
 274:"Well, after studying dozens of articles from the National Library of Medicine, we came across a study published in JAMA showing that 2 compounds have the capacity to make your body produce GLP-1 and GIP naturally and at accelerated levels.",
 321:"Instead of burning it, it accumulates in your belly, legs, back, arms, and even your face.",
 327:"Your body finally releases that fat and uses it as energy naturally.",
 342:"The first and most powerful ingredient is pure gelatin, which, as I said before, contains concentrated levels of glycine and alanine, 2 special amino acids capable of restoring the natural production of GLP-1 and GIP, signaling your body to switch into fat-burning mode.",343:None,
 399:"It's only when you do it the right way, combining these 4 ingredients in their purest and most concentrated forms, in the exact proportions, that you create what we call the metabolic transformation cascade.",
 404:"Together, your body shifts into automatic fat-burning mode, 24 hours a day, 7 days a week, with the ability to easily eliminate localized fat in your belly, arms, back, thighs, and even your face.",
 414:"Because now, for the first time in their lives, their own body chemistry is working for them, not against them.",
 424:"I found a simple way, without anyone having to spend almost anything, for everyone watching at home to use this formula.",425:None,
 433:"We arrived at the final form: a powerful gummy made of pure gelatin with the highest concentrations of glycine and alanine, along with the purest and most concentrated forms of Japanese green tea extract, curcumin with gingerol, and hydrolyzed type 1 collagen, all mixed in the exact proportions, precise down to the milligram.",434:None,
 439:"These gummies are absolutely beautiful, and I can already smell how amazing they…",
 440:"Jenna, this is not a supplement. This is not the gelatin you buy at Walmart.",
 447:"I remember the day… When my friend told me about the gelatin trick, I laughed.",
 480:"And what happened? I lost 152 pounds in just 5 months, Jenna.",
 529:"A consortium of private wellness investors, the American Wellness Group, reached out to me directly.",
 538:"In this initiative, we created Gumitide, the only formula that combines pure gelatin with the other 3 natural ingredients of the gelatin trick in the exact ratio and concentration to maximally activate the natural production of GLP-1 and GIP… being considered one of the most effective treatments ever analyzed by the FDA for fat burning.",
 542:"I had never seen anything so complete. The pharmaceutical industry tried to boycott it, but after the FDA filed it and the tests proved its efficacy and safety, it became impossible to ignore.",
 551:"In other words, it doesn't depend on your age, genetics, or specific health history to work.",
 557:"At the end of the day, many of the people watching us right now have already tried everything; they need to see real results.",
 560:"The first one only proved that Gumitide is safe for consumption, and any capsule sold out there has that.",
 572:"At the same time, a few solutions based on real biological mechanisms have been ignored, or worse, copied, diluted, and falsified.",
 587:"This happens because Mounjaro works by stimulating the body to use fat as an energy source.",
 590:"And that's exactly what we observed: Gumitide, because it is formulated with ingredients that stimulate GLP-1, is more easily recognized by the body.",
 602:"Around 9%.",606:"Absorption reached about 32%, but there was a problem.",
 607:"When diluted, effectiveness dropped, and it also wasn't a practical format to consume.",
 608:"That's when I read a study published by Dr. Oz on absorption and bioavailability in the gummy format, showing that the absorption of amino acids can be up to 3 times greater than in powder form.",609:None,
 616:"It almost seems impossible not to see results.",
 648:"And we know that, Jenna: most of the thousands of women our medical team has followed over the past few months were living exactly that reality, taking care of their kids, their husbands, their homes, and putting themselves last.",
 652:"Over time, the body starts to adjust and begins producing GLP-1 and GIP hormones in a more consistent and natural way, and that's exactly where the difference happens.",
 666:"When I first heard about Gumitide, I have to admit I was skeptical, but when I saw the statement from the head of the FDA and the patent on the formula, something caught my attention.",
 691:"So besides Kathy Bates, Reba, Dolly, even Oprah and Kelly Clarkson are also using and recommending Gumitide to lose weight for this summer.",
 693:"And various other celebrities keep posting their transformations on social media thanks to Gumitide.",
 699:"Gumitide officially received the Guaranteed Efficacy Seal, an unprecedented certification granted by the FDA in the weight loss category, after studies confirmed that the natural formula is up to 10 times more effective than the active ingredient in Mounjaro.",
 702:"Women who now look in the mirror and feel happy and proud of their own bodies, free from that annoying fat accumulated on their bellies, arms, and thighs.",
 710:"For sure.",
 711:"But the problem is that due to the rarity of Gumitide's ingredients and the difficulty of producing it, we can only manufacture a new batch in 6 months.",
 714:"But why did you stop the sales, Jillian?",
 729:"I bought 3 bottles of Gumitide when you launched it.",
 741:"15,000 women, women who were stuck in the corrupt weight loss industry, spending more than $1,500 a month on Mounjaro, on procedures, and on expensive doctor visits.",
 752:"Karen, keep watching the show, you won't regret it.",
 763:"That's why I took money out of my own pocket and created the New Body for the Summer campaign, which is going to give 4 bottles of Gumitide completely free to these women.",
 774:"That's exactly why I said the New Body for the Summer campaign is the biggest opportunity of their lives to achieve the body of their dreams and show it off this summer.",
 784:"Since we know you're gonna lose weight, we wanna share your success story to inspire other women who also wanna lose weight.",
 790:"You pay for one and get the other one for free with a huge 84% discount off the original price.",
 795:"And with new import tariffs from the current administration, combined with the rarity of the ingredients, the costs to bring them into the United States have skyrocketed.",
 825:"Once you select your treatment, you'll be redirected to our secure payment page with top-level encryption.",
 830:"If you live in the United States, your order will arrive in 3 to 5 business days, right to your door, depending on your region.",831:None,
 837:"So don't wait, take action now and select the 6-bottle kit below while the promotion is still active.",
 848:"It's absolutely the best option because not only does it guarantee a bigger discount, it also delivers the maximum effectiveness of the formula and long-lasting results.",
 854:"And like I said, the next batch will only be produced 6 months from now at the earliest, so there's a real risk of running out of the product before you experience the long-term effects.",
 900:"These recipes will erase your wrinkles, dark spots, and crow's feet, naturally rejuvenating your skin, enhancing your facial expressions, and leaving the skin of your arms, your neck, and your belly perfect for this summer.",
 912:"Oh my God, Jillian, any woman with access to Gumitide and these 3 bonuses is gonna be ready to rock this summer.",
 921:"Your libido will come back with full force, and you'll rediscover the energy, the desire, and the vitality of when you were 20 years old.",
 926:"With this bonus, you'll eliminate gut inflammation, get rid of that bloating and constipation that bother you so much, and keep your belly flat all day long.",
 949:"After all, once you lose the weight, you deserve a new wardrobe to celebrate this new chapter of your life, don't you think?",
 967:"The average American woman spends more than $200,000 over a lifetime trying to lose weight.",
 970:"Heart attacks, strokes, diabetes, Alzheimer's, all of these risks increase dramatically when you're overweight.",
 981:"Imagine wearing shorts or walking on the beach in a bikini, drawing every look without fear, without shame, without worrying about what others might think. Imagine looking at yourself in the mirror and feeling younger than ever, with the energy to play with your kids or grandkids for hours, going on vacation, eating that food you love at the restaurant without guilt, without shame, without that fear of waking up heavier the next day.",982:None,
 983:"Imagine hearing your doctor say that you are healthy, that your heart, your lungs, and your organs have miraculously been renewed, your libido coming back, your hormones back in balance. You deserve to live a long and happy life, and without a doubt, this is the easiest choice.",
 994:"Click the button below this video right now and secure your kit under these special conditions.",
}
for i,t in fix.items():
    if t is None: del by[i]
    else: by[i]['text']=t
# inserted sentences (speaker change inside an ASR sentence)
by[714.5]={"i":714.5,"speaker":"3A","start_ms":by[714]['start_ms']+2500,"end_ms":by[714]['end_ms'],"text":"Since you had already invited me to your show, I decided to reserve the last remaining bottles of Gumitide for the women watching us on today's show."}
by[714]['end_ms']=by[714]['start_ms']+2500
for i in by: by[i]['text']=re.sub(r'\b(Gummitide|Gumotide|Gumatide|Lumetide|gummitide|Gummatide)\b','Gumitide',by[i]['text'])
for i in by: by[i]['text']=re.sub(r'\bManjaro\b','Mounjaro',by[i]['text'])
S=[by[k] for k in sorted(by)]
JIL="JILLIAN MICHAELS (avatar)"; JEN="JENNA BUSH HAGER (apresentadora, Today with Jenna & Friends, avatar)"
SPK={"1A":JEN,"1B":JIL,"1C":"REBA McENTIRE (avatar, depoimento)","1D":"DOLLY PARTON (avatar, depoimento)","1E":"KATHY BATES (avatar, depoimento)","1F":"OPRAH WINFREY (avatar)","1G":"DRA. ANIA (médica, avatar)","1H":"DR. OZ (avatar, coletiva)",
     "2A":JIL,"2B":JEN,"2C":"KATHY BATES (avatar, depoimento)","2D":"KAREN, de Tulsa (depoimento ao vivo)",
     "3A":JIL,"3B":JEN,"3C":"ÂNCORA DE TV (voz, avatar)","3D":"ENDOCRINOLOGISTA (avatar)","3E":"CHEFE DA FDA (avatar, Casa Branca)","3F":"SUSAN, 65 anos (depoimento)","3G":"OPRAH WINFREY (avatar)","3H":"KELLY CLARKSON (avatar)",
     "4A":JIL,"4B":JEN,"4C":"GANHADORA DO GIFT CARD (depoimento)"}
over={}
for i in range(496,511): over[i]="LINDA, de Knoxville (depoimento ao vivo)"
over[531]=JEN
for i in (696,697,698,699): over[i]="ÂNCORA DE TV (voz, avatar)"
for i in (737,738): over[i]="KAREN (depoimento ao vivo)"
for i in list(range(726,736))+[753,754]: over[i]="KAREN (depoimento ao vivo)"
def spk(s):
    o=over.get(s['i'])
    return o if o else SPK[s['speaker']]
blocks=[(0,"PRÉ-LEAD: a gelatina rosa de Kelly Clarkson e Oprah, 'o problema' e o teste da receita (versão errada x versão certa)"),
 (21,"ABERTURA DO PROGRAMA: Jenna apresenta Jillian Michaels (The Biggest Loser, 20 anos de transformações)"),
 (30,"A PROMESSA: o truque da gelatina com 3 ingredientes da cozinha, até 15 libras; Reba (18 lb) e Dolly (37 lb)"),
 (41,"DEPOIMENTOS I: Reba McEntire (71 anos, 18 libras) e Dolly Parton (37 libras em 2 meses)"),
 (73,"KATHY BATES I: 115.000 mulheres, o caso mais difícil, a capa da revista ('gorda, inchada, fora de controle'), 240 libras"),
 (100,"KATHY BATES II: 77 anos, Oscar por Misery, os 3 médicos ($15.000 jejum, $12.000 keto, $23.000 Mounjaro) e as 100 libras"),
 (137,"POR QUE TUDO FALHA: metabolismo basal (o magro que come tudo), keto e a sensibilidade à insulina (a mãe levando a glicose à escola)"),
 (166,"MOUNJARO E OS 2 HORMÔNIOS: o que GLP-1 e GIP fazem, o corpo em pânico que estoca gordura"),
 (194,"PROVA: 'nunca foi força de vontade', o estudo do NEJM (21x mais, 2,4% x 50,4%)"),
 (209,"O REBOTE: as canetas substituem em vez de estimular, dependência química, Oprah e a Dra. Ania (mulheres 60+)"),
 (230,"EFEITOS COLATERAIS: o rótulo do Mounjaro, Dr. Oz na coletiva, os processos contra Novo Nordisk e Eli Lilly"),
 (267,"A SOLUÇÃO NATURAL: o estudo do JAMA, glicina e alanina, por que a gelatina 'engana a fome' e o jeito certo de preparar"),
 (302,"NA COZINHA: a gordura da paciente 1 (travada) x paciente 2 (solta), menopausa e a fome constante"),
 (330,"A DEMONSTRAÇÃO: o pó de glicina e alanina derrete a gordura travada, 24h por dia, sem rebote"),
 (341,"INGREDIENTE 1: gelatina pura sem sabor (Harvard: GLP-1 +182%, GIP +144%), não é o Jell-O do mercado"),
 (351,"INGREDIENTE 2: extrato de chá verde japonês, 'o acelerador silencioso' (OMS: Japão 3,6% x EUA 42%; 10x mais gordura localizada)"),
 (367,"INGREDIENTE 3: curcumina com gingerol, 'os guardiões' contra a inflamação intestinal (Cleveland Clinic: -87%) e o rebote"),
 (378,"INGREDIENTE 4: colágeno tipo 1 hidrolisado contra a pele flácida e o 'rosto de Ozempic' (6x mais colágeno)"),
 (396,"A CASCATA DA TRANSFORMAÇÃO METABÓLICA: os 4 ingredientes juntos, modo queima de gordura 24/7, Kathy e as 100 libras"),
 (416,"O PROBLEMA DA PUREZA (99% diluído, proporção ao miligrama), o post no Facebook, a Sasaki Labs e a primeira goma"),
 (445,"DEPOIMENTO DE KATHY BATES: 1 goma antes de dormir, 17 libras em 10 dias, 100 libras em 4 meses, as mentiras da mídia"),
 (472,"AO VIVO: Karen de Tulsa (152 libras, tireoide) e Linda de Knoxville (67 libras); 150.000 americanas"),
 (522,"ESCALA: fábrica GMP/FDA, American Wellness Group ($200 milhões, Boulder, Colorado), 'Take Your Body Back' e nasce o GUMITIDE"),
 (539,"APROVAÇÃO DA FDA: a notícia, a endocrinologista, segurança para qualquer condição (pressão, diabetes, tireoide)"),
 (556,"2ª ETAPA DA FDA: o chefe da FDA no laboratório, Mounjaro x Gumitide na gordura, '10x mais poderoso'"),
 (598,"POR QUE GOMA: cápsula absorve 9%, pó 32%, o estudo do Dr. Oz (3x mais) e a endocrinologista"),
 (615,"RESULTADOS NO TEMPO: 1 mês (barriga, culotes, braços), 3 meses (32 libras) e Susan, 65 anos (47 libras, vestido vermelho)"),
 (639,"OS 6 MESES: 97,6% dos melhores resultados, sem rebote; Oprah (76 libras, 72 anos) e Kelly Clarkson (38 libras)"),
 (693,"NA MÍDIA: esgotou em 1 hora, 115.000 mulheres, o Selo de Eficácia Garantida da FDA e o future pacing (biquíni, marido)"),
 (711,"ESCASSEZ: novo lote só em 6 meses, as últimas 84 garrafas no estúdio, Karen ao vivo ('pago $500 cada')"),
 (760,"OFERTA 'NEW BODY FOR THE SUMMER': kit de 6 (pague 2, leve 6, $49), kit de 3 ($69), cash back para as 10 primeiras, kit de 2 ($79)"),
 (793,"URGÊNCIA E COMPRA: tarifas de importação, 'agora ou nunca', pagamento seguro, entrega em 3 a 5 dias, frete grátis, só na página oficial"),
 (843,"63 GARRAFAS, a indústria que mente há décadas, GARANTIA de 60 dias e 'risco zero'"),
 (879,"OS 5 BÔNUS: Bikini Ready in 4 Weeks, 6 Keys to Perfect Skin Over 50, Smooth and Toned Legs, Reclaim Your Body After Menopause, Bloat-Free and Gut Reset"),
 (934,"GIFT CARD DA MACY'S de $1.000 para as 10 primeiras, a ganhadora, só 27 garrafas"),
 (955,"FECHAMENTO: as 2 escolhas, $200.000 numa vida, o custo humano, future pacing final, garantia e CTA")]
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
doc={"titulo":"GUMITIDE VSL — Transcrição EN + Tradução PT-BR + Prints",
 "fonte":"Fonte: 'Gumitide 29/07' (Drive, 1:22:38, vertical 1080x1350). Transcrição: AssemblyAI (speaker labels), áudio processado em 4 partes de ~20 min e remontado com as minutagens originais. Tradução fiel: nomes, marcas, valores em dólares, libras e referências dos EUA mantidos como falados. Formato: VSL em estilo de programa de TV ('Today with Jenna & Friends') com avatares de Jillian Michaels (blazer salmão) e de Jenna Bush Hager (vestido rosa), mais depoimentos de celebridades (Reba McEntire, Dolly Parton, Kathy Bates, Oprah, Kelly Clarkson), Dr. Oz, 'chefe da FDA' e clientes 'ao vivo'.",
 "nota_prints":"Timing: cada mini-bloco traz o intervalo x → y em que a fala acontece no vídeo. Prints: frames dos momentos mais importantes (letterings, provas, personagens, produto, oferta), nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "correcoes_asr":"Nome do produto normalizado para 'Gumitide' (rótulo do frasco; ASR: Gummitide, Gumotide, Gumatide, Lumetide); 'Manjaro' → Mounjaro; 'Dr. Anya' → Dra. Ania; 'me on the COVID' → 'cover'; gaguejos (um/uh) e repetições removidos; reticências (…) marcam cortes de edição no áudio original. Falas cortadas no meio por troca de falante foram separadas (35:18 Jenna/Jillian; 58:01 Jenna pergunta e Jillian responde). Inconsistências do roteiro mantidas: 'Kathy and Dolly's transformations' (5:14) após os vídeos de Reba e Dolly; Reba diz 18 libras 'em menos de 1 mês' (3:49) e Jenna 'em 3 meses' (3:02); Kathy 'em 2 semanas' x 'em 4 meses'; Karen aparece como cliente de Tulsa (38:04) e como compradora do lançamento (58:48); 'mais de 100.000 pessoas' seguido de '15.000 mulheres' (59:43); estoque 84 → 63 → 27 garrafas.",
 "falantes":fal,"frames_dir":f"{W}/frames","img_width_in":2.35,"blocos":out}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'blocos',sum(len(b['mini']) for b in out),'minis',sum(len(m['falas']) for b in out for m in b['mini']),'falas')
with open(f'{W}/falas_en.txt','w') as f:
    for b in out:
        for k,m in enumerate(b['mini'],1):
            for j,x in enumerate(m['falas']): f.write(f"### {b['n']}.{k}.{j} [{m['inicio']}] {x['falante']}\n{x['en']}\n\n")
