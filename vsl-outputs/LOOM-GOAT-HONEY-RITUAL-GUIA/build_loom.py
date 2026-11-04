import json, re
W='VSL-Pipeline-LOOM-MARCOS'
P=json.load(open(f'{W}/paras.json'))
# normalização de nomes que o ASR errou (fala do Marcos)
FIX=[(r'\b(Raimann|Raimundo|Raimi|Heimann|Hyman)\b','Hyman'),(r'Mark Hyman','Mark Hyman'),(r'Dr\. Mike Hyman','Dr. Mark Hyman'),
     (r'Soda R(oss|osa|oça)','Soda Horse'),(r'Dr\. Atcha','Dr. Attia'),(r'\bAlpatino\b','Al Pacino'),(r'\bPalpatine\b','Al Pacino'),
     (r'\bLidy\b','lead'),(r'\bali de 3\b','lead 3'),(r'bacon e soda','baking soda'),(r'Bake Soda','baking soda'),(r'bake soda','baking soda'),
     (r'\bBeerus\b','b-rolls'),(r'\bBirose\b','b-rolls'),(r'picolodinol','Pycnogenol'),(r'\bNuô\b','Noor'),(r'Dereck','Derek'),
     (r'\bmicrolite\b','micro-lead'),(r'eja o Zodaf J Borrado','e já o WSJ borrado'),(r'\bRicaltra\b','Hill Country'),(r'ali de um\b','lead 1'),(r'dali de uma\b','da lead 1'),(r'dali de um\b','da lead 1')]
for p in P:
    t=p['texto']
    for a,b in FIX: t=re.sub(a,b,t)
    p['texto']=t
# blocos: (índice do parágrafo inicial, rótulo, descrição)
B=[
 (0,"ABERTURA — Conceito da VSL (GOAT HONEY RITUAL)","Proposta: bode espanhol (chifres acentuados), mecanismo do cimento (já usado na oferta do touro), mecanismo da solução e bloco de oferta mais fortes; mistura baking soda + mel como visual central de tudo (takes, estoques, mistura cremosa na tigela)."),
 (3,"AVATAR PRINCIPAL — Mark Hyman (expert central)","Vídeo de referência do Hyman gerado em IA; cenário como o Dr. Attia na Soda Horse (consultório com estátua ao fundo), ele no microfone e mais distante; editor deve mandar confirmar a geração antes de fazer a VSL inteira."),
 (7,"PERSONAGENS DA WEBSÉRIE — Al Pacino (emotion) e Noor (esposa, 28)","Al Pacino gerado no sofá da casa dele olhando para o Hyman (frame de entrevista); Hyman gerado no mesmo sofá com outra roupa; Noor (28 anos, referência visual) entrevistada em outra sala conversando com o Hyman."),
 (12,"LEAD 01 — Cozinha + receita (Core/Kendra/Juliana)","Referência exata (ela na cozinha com os ingredientes); 3 tentativas de geração (rosto igual sem nada com ingredientes → olhando para frente → pior caso com roupa); ações da micro-lead validada: jogar baking soda, mel, misturar, segurar a colher, colocar de lado; Kendra e Juliana em pé na cerca do curral (não repetir a pegada do Texas), passar a mistura na boca do cara, marcar por cima da calça, celular com DMs no Instagram, antes/depois com régua (6 → 9 polegadas), zoom na marcação."),
 (31,"LEAD 02 — Poltrona, Tucker Carlson, Fox Breaking News, Corey e a live do ônibus","Cara mais velho na poltrona com ela (trocar a roupa, rosto exato, ele de cueca); Tucker Carlson em podcast; apresentador de jornal com banner 'Breaking News Alert' da Fox; não é a Brandi, é a Corey na mesma cozinha com os ingredientes; take com olho aberto; mockup de live do ônibus (estilo mockup de Instagram/TikTok das VSLs de emagrecimento); repete as ações da receita da lead 1."),
 (41,"LEAD 03 — Hyman no podcast + depoimentos","Hyman no podcast; depoimento do George Clooney gerado na cozinha fazendo a receita; cara normal sentado com a mulher dormindo e tigela de vidro na cabeceira; depoimento de mulher normal (nome no doc, buscar b-rolls no Google); volta para o Hyman e fecha."),
 (43,"PADRÃO DE QUALIDADE DA LEAD — exemplo da Soda Horse validada","30 segundos de uma lead validada: efeitos sonoros, transições, trilha (beats), geração de atores muito real, receita mastigável (gente comendo a mistura), blur ao fundo, estilo de lettering, legenda exata, b-rolls do rancho com bode espanhol (receita na comida do bode); tudo muito chamativo visualmente, inclusive depoimentos."),
 (51,"BACKGROUND — Autoridade do Hyman","Trilha para cima/empolgante; estoques de universidade, podcast, Hyman com famosos; tags laranja = referências de b-rolls de edição, tags verdes = referências visuais exatas; vídeos do Dr. Mark Hyman sobre testosterona/força/treino em casa, longevidade e antienvelhecimento; conexão com famosos (Harrison, George Clooney, Al Pacino); sempre mostrar mel (mais avermelhado) + baking soda juntos; depoimento 1, outro cara e Joe Rogan olhando para a câmera; comentários no doc compartilhados com o editor."),
 (60,"BACKGROUND — História do Al Pacino","Confissão de um homem (Pacino à direita, Hyman à esquerda na casa); cenas da história com a Noor (olhando o relógio, roupa dela descrita); b-rolls de testosterona/pâncreas; estoques do Oscar, 2 Emmys e 2 Tonys; ele triste na rua; mistura baking soda + mel; fundo do poço com o personal trainer (ela chegando em casa); receita na bancada (tigela de vidro, come e sobe a escada — 'look how calm the bastard is'); câmera da escada; roupa trocada; manchetes reais do divórcio; ela com as malas; fazenda de bode."),
 (69,"INVESTIGAÇÃO E PROVAS — Glifosato, jornais e o bode espanhol","Preto e branco com letras branco/vermelho nas situações constrangedoras; pesquisador de jaleco; Roundup e listas de glifosato bem provados; trecho do Robert F. Kennedy; material vazado; jornais sempre atuais (The Wall Street Journal), revistas, rosto borrado; bode espanhol de chifre comprido; Sandeep Gupta com certificação e bodes ao fundo; estoques de ração e variedade do bode (trocar o cavalo pelo bode)."),
 (74,"MECANISMO DO PROBLEMA — Market test (Mark Hyman)","Seguir à risca as referências: jornais e revistas sobre colágeno 3, corpo cavernoso por dentro, microscópio, banners, post-its; cimento dentro da esponja (versão do Secom ficou mais forte que a Soda Horse); estoques de carne/comida com glifosato; esponja esquerda x direita; prova dos 60% de cimento; revistas dos casos do México e da Alemanha; b-roll de cimento com glifosato altíssimo; Viagra, testosterona e TRT."),
 (79,"MECANISMO DA SOLUÇÃO — Gupta na fazenda, mel, chifre e óxido nítrico","Revelação do Gupta na fazenda de bodes falando para a câmera ('pensa comigo'); estoques de cavalo adaptados para bode; mel; planta de cárie/cariína; chifre e colágeno; exame dia 1 x dia 30; trocar 'Lexicon/Longhorn Pilot' por 'Hill Country Pilot' (voluntário 22); outros ingredientes; medidor de óxido nítrico (primeira medição rosa claro, toma Pycnogenol, segunda medição vermelho escuro)."),
 (83,"PRODUTO — Ligação do Al Pacino, Gerardo no quarto e o scan do Hyman","Al Pacino 'por ligação' (estoque de ligação + voz); Gerardo no quarto de frente para a câmera (depoimento); prova = exame/scan do Mark Hyman; geração da mulher (nome no doc) se gravando com o celular ou pau de selfie; b-rolls congruentes (parecidos com Al Pacino: não moreno, não tatuado); prova do bode no lugar do cavalo."),
 (87,"DEPOIMENTOS — Vídeo caseiro, teste da tira e Dr. Raymond (Caldwell Biosciences)","Depoimento 1 caseiro com o mesmo cara do vídeo 1 deitado; teste da tira/elástico (dia 1 solto, dia 5 apertando, dia 7 estourou); depoimento 2 com avatar e roupa idênticos; depoimentos sempre com b-rolls em quadradinhos dividindo a tela; Dr. Raymond com logo da Caldwell Biosciences no bolso; estoques de credibilidade/estudos; cara falando no centro com nome e idade ('vou tentar o truque do mel e do bode'), cara mais velho, vídeo passando embaixo."),
 (94,"BIG OFFER — Frasco, laboratório, celebridades com potes e abertura do Al Pacino","Começa com ele segurando o frasco para a câmera (histórias da indústria/fábrica); muitos b-rolls; laboratório com potes de Aeropulse; Dr. Oz com pote na mão; atriz exata com 2 potes; Mick Blue com pote; 6 potes na mesa do Harrison; Van Damme com pote; cara velho e ela; doutora com pote; 6 potes focados; grade de homens com pote; DMs enviadas ao Mark; abertura com Al Pacino anunciando promoção na casa dele com os potes na mesa (olhando para a câmera, estilo Elon); b-rolls da viagem/iate."),
 (99,"MOCKUPS, BÔNUS E PREÇO","Mockups com qualidade maior (os atuais parecem CD); John segurando o pote; bônus com referência e estilo base universais; duas mulheres revezando na copy; Hyman com paciente no laboratório; mockups dos bônus com preço: R$3.997, 'não mais de R$3.757'."),
 (102,"CLOSE — Depoimento final, Al Pacino fora de casa e Hyman","Depoimento final; close-up do Al Pacino direto para a câmera em outro cômodo/fora de casa (jardim, mesa com os frascos); Hyman com o último depoimento; vídeos de b-rolls nas cenas; cerca de 3 potes de Aeropulse na mesa com ela falando."),
 (104,"FAQ — Pop-up de mensagem no Instagram","Partes em negrito como pop-up/mockup de Instagram no rodapé (foto de perfil do cara mandando mensagem para o Hyman: 'olha essa mensagem que eu recebi'); ele responde em seguida de frente no podcast; encerramento ('qualquer dúvida me chamem e bora para cima')."),
]
def ts(ms): s=ms//1000; return f"{s//60}:{s%60:02d}"
starts=[b[0] for b in B]+[len(P)]
sumario=[]; blocos=[]
MAXS=50
for n,(i0,rot,desc) in enumerate(B,1):
    ps=P[i0:starts[n]]
    sumario.append({"bloco":rot.split(" — ")[0],"inicio":ps[0]['ts'],"fim":ts(ps[-1]['end_ms']),"descricao":(rot.split(" — ",1)[1]+". " if " — " in rot else "")+desc})
    minis=[];cur=[]
    for p in ps:
        if cur and (p['start_ms']-cur[0]['start_ms'])/1000>=MAXS: minis.append(cur);cur=[]
        cur.append(p)
    if cur: minis.append(cur)
    blocos.append({"n":n,"titulo":rot,"inicio":ps[0]['ts'],"fim":ts(ps[-1]['end_ms']),
                   "mini":[{"inicio":m[0]['ts'],"fim":ts(m[-1]['end_ms']),"prints":[],"paras":[{"ts":p['ts'],"texto":p['texto']} for p in m]} for m in minis]})
doc={"titulo":"GUIA DE VSL — GOAT HONEY RITUAL (Loom do Marcos) — Transcrição com minutagens + Sumário + Prints",
 "fonte":"Fonte: Loom 'Guia de VSL do GOAT HONEY RITUAL' (47:32, gravação de tela 1920x1028). Transcrição em português (AssemblyAI). Fala única do Marcos, sem marcação de personagens. Nomes normalizados onde o ASR errou: Mark Hyman (ASR: Raimann/Raimundo/Heimann), Soda Horse (ASR: Soda Ross/Rosa/Roça), Dr. Attia (ASR: Atcha), Al Pacino (ASR: Alpatino/Palpatine), baking soda, b-rolls, Pycnogenol. 'Aeropulse', 'Secom', 'Gerardo', 'Corey/Brandi/Kendra/Juliana/Noor/Core' mantidos como ouvidos.",
 "nota_prints":"Minutagens: cada parágrafo começa com [m:ss] do momento em que a fala acontece; cada trecho (x.y) traz o intervalo x → y. Prints: frames da tela do Loom nos momentos em que uma referência visual é mostrada, nomeados bNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "frames_dir":f"{W}/frames","img_width_in":2.35,"sumario":sumario,"blocos":blocos}
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(blocos),'blocos',sum(len(b['mini']) for b in blocos),'minis')
for s in sumario: print(f"{s['inicio']:>6} → {s['fim']:<6} {s['bloco']}")
