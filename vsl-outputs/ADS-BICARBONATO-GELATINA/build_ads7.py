import json, re
from PIL import Image
def load(n):
    S=json.load(open(f'VSL-Pipeline-{n}/sentences.json')); return {s['i']:s for s in S}
FIX={'V02':{4:"The real version of the trick costs $3,000 and a private consultation with Dr. Kylie Sakaida, nutritionist to the stars in Hollywood, and requires the correct order and exact timing to go from XL to S in less than 3 months.",5:None,
            7:"In celebration of more than 70,000 women losing at least 9 pounds with this bariatric shot recipe, the short video of Dr. Kylie's original recipe, who has already helped names like Oprah, Kelly Clarkson, and Melissa McCarthy lose weight, is completely free for the next 20 minutes.",8:None,
            9:"Click learn more now and copy the correct recipe before it goes offline.",17:"Your body enters high-speed burn mode 24 hours a day."},
     'V01':{16:"Everything I'd been trying, the diets, the shots, the programs, were only ever hitting the surface."},
     'V04':{7:"Keto, low-carb, pink salt, fasting: none of it stuck."}}
def chunk(n,spk,idx,by):
    parts=[]
    for i in idx:
        t=FIX.get(n,{}).get(i,by[i]['text']) if i in FIX.get(n,{}) else by[i]['text']
        if t is not None: parts.append(t)
    return {"spk":spk,"start":by[idx[0]]['start_ms'],"end":by[idx[-1]]['end_ms'],"en":' '.join(parts)}
def ts(ms): s=ms//1000; return f"{s//60}:{s%60:02d}"
ADS=[]
b=load('V01'); S1="APRESENTADORA (UGC, loira, cozinha)"
ADS.append({"n":1,"W":"VSL-Pipeline-V01","titulo":"AD 01 — video-03-09-2026 (1:38) — 'Meu corpo depois de 6 semanas de bicarbonato' (células travadas, reset alcalino)",
 "chunks":[chunk('V01',S1,list(range(0,10)),b),chunk('V01',S1,list(range(10,18)),b),chunk('V01',S1,list(range(18,24)),b),chunk('V01',S1,list(range(24,31)),b)],
 "pt":["Este é o meu corpo depois de 2 anos de restrição calórica. Este é o meu corpo depois de 8 meses nas injeções. Este é o meu corpo depois de só 6 semanas usando bicarbonato de sódio toda manhã. Aqui está exatamente o que aconteceu. Eu tinha 43 anos e vinha carregando o mesmo peso teimoso havia bem mais de uma década. Eu achava que estava fazendo tudo certo. Eu era consistente. Eu estava gastando o dinheiro. Eu estava seguindo as instruções à risca. Por que o meu corpo ainda não respondia?",
  "Então um médico que uma amiga me indicou me disse uma coisa que me deixou paralisada. O peso não veio de comer demais. Não veio de me mexer de menos. Ele está travado. As suas células entram num estado de bloqueio quando o seu ambiente interno fica ácido demais. E, uma vez travadas, nada que você faça por fora consegue chegar ao nível onde o verdadeiro sinal de liberação mora. Tudo o que eu vinha tentando, as dietas, as injeções, os programas, só atingia a superfície. O que eu precisava era de algo que mudasse o ambiente de dentro.",
  "É aí que entra o bicarbonato de sódio. A combinação certa com 2 outros ingredientes de cozinha cria um reset alcalino que chega direto às células. Quando o ambiente muda, as células saem do bloqueio e o corpo começa a responder em todos os lugares certos. Isso significa ir diminuindo a barriga, o pescoço e os braços depois de anos de luta. Um copo disso toda manhã me tomava uns 30 segundos. Aqui está por que é a melhor coisa que eu já tentei.",
  "Com 6 semanas, as minhas roupas estavam vestindo diferente. No mês 3, as pessoas perguntavam o que eu tinha mudado. Mais de 90.000 pessoas já usaram isso depois que todo o resto falhou com elas. A rotina exata com as instruções reais está no vídeo da próxima página. Você não precisa de um fim de semana livre para começar, e não tem nada para comprar para começar. É só assistir ao vídeo e testar você mesma. Toque abaixo agora mesmo."],
 "prints":[(0,"antes_2_anos_restricao","Abertura: mulher gorda de top cinza (antes) com a apresentadora em PIP; 'THIS IS MY BODY AFTER TWO YEARS OF CALORIE RESTRICTION'"),
  (3,"antes_8_meses_injecoes","Mulher de top preto; 'THIS IS MY BODY AFTER EIGHT MONTHS ON THE SHOTS'"),
  (5,"depois_6_semanas_bicarbonato","Mulher magra de top lilás; 'THIS IS MY BODY AFTER JUST SIX WEEKS OF USING BAKING SODA'"),
  (10,"mulher_cozinha_i_was_43","Apresentadora (loira, camiseta branca) na cozinha; 'I WAS 43'"),
  (14,"mulher_a_decade","Apresentadora; 'SAME STUBBORN WEIGHT FOR WELL OVER A DECADE'"),
  (19,"mulher_following_instructions","Apresentadora gesticulando; 'I WAS FOLLOWING THE INSTRUCTIONS EXACTLY'"),
  (23,"medico_jaleco_doctor_referred","Médico de jaleco desfocado; 'THEN A DOCTOR A FRIEND REFERRED'"),
  (27,"omelete_weight_didnt_come_from_eating","Prato com omelete; 'THE WEIGHT DIDN'T COME FROM EATING'"),
  (30,"mulher_correndo_not_moving","Mulher correndo na estrada; 'MOVING ENOUGH. IT'S LOCKED'"),
  (32,"celulas_lockdown_state","Ilustração de células; 'YOUR CELLS GO INTO A LOCKDOWN STATE'"),
  (34,"estomago_too_acidic","Ilustração do esôfago/estômago; 'WHEN YOUR INTERNAL ENVIRONMENT BECOMES TOO ACIDIC'"),
  (37,"balanca_ponteiro_lock","Ponteiro de balança; 'AND ONCE THEY LOCK, NOTHING YOU DO ON THE OUTSIDE'"),
  (43,"mulher_the_diets_the_shots","Apresentadora; 'THE DIETS, THE SHOTS, THE PROGRAMS WERE ONLY EVER HITTING THE SURFACE'"),
  (49,"bancada_bragg_bicarbonato_limao","Bancada com vinagre Bragg, bicarbonato e limão; 'THAT COULD SHIFT THE INSIDE ENVIRONMENT'"),
  (51,"copo_bicarbonato_thats_where","Mexendo o copo com bicarbonato; 'THAT'S WHERE BAKING SODA COMES IN'"),
  (53,"espremendo_limao_right_combo","Espremendo limão no copo; 'THE RIGHT COMBO WITH TWO OTHER KITCHEN INGREDIENTS'"),
  (58,"animacao_homem_gordo_magro","Animação do homem gordo virando magro; 'REACHES THE CELLS DIRECTLY... ONCE THE ENVIRONMENT SHIFTS'"),
  (62,"animacao_cells_lockdown","Animação do corpo; 'THE CELLS COME OUT OF LOCKDOWN... IN ALL THE RIGHT PLACES'"),
  (64,"barriga_chipping_away","Mulher gorda apertando a barriga; 'THAT MEANS CHIPPING AWAY AT THE BELLY'"),
  (67,"costas_neck_and_arms","Mulher de costas; 'NECK AND ARMS AFTER YEARS OF STRUGGLE'"),
  (71,"mulher_lilas_one_glass_30_seconds","Mulher magra de top lilás; 'ONE GLASS OF THIS EVERY MORNING TOOK ME ABOUT 30 SECONDS'"),
  (75,"mulher_six_weeks_in","Apresentadora; 'SIX WEEKS IN MY CLOTHES WERE FITTING DIFFERENTLY'"),
  (78,"mulher_by_month_three","Apresentadora; 'BY MONTH THREE PEOPLE WERE ASKING WHAT I CHANGED'"),
  (80,"mulher_over_90000_people","Apresentadora; 'OVER 90,000 PEOPLE HAVE ALREADY USED THIS'"),
  (84,"bancada_mel_limao_directions","Bancada com mel, limão e canela; 'THE EXACT ROUTINE WITH THE REAL DIRECTIONS ARE ON THE VIDEO'"),
  (89,"pegando_pote_nothing_to_buy","Mão pegando o pote na bancada; 'DON'T NEED A FREE WEEKEND... NOTHING TO BUY TO START'"),
  (93,"mulher_just_watch_the_video","Apresentadora apontando; 'JUST WATCH THE VIDEO AND TRY IT YOURSELF'"),
  (96,"mulher_tap_below_right_now","Apresentadora; 'TAP BELOW RIGHT NOW'")]})
b=load('V02'); S2="DR. OZ (avatar, 'LIVE' no Instagram)"
ADS.append({"n":2,"W":"VSL-Pipeline-V02","titulo":"AD 02 — video-17-09-2026 (2:13) — Dr. Oz (avatar) ao vivo: 'a última vez' da receita de bicarbonato com limão (XL → XS)",
 "chunks":[chunk('V02',S2,list(range(0,6)),b),chunk('V02',S2,list(range(6,14)),b),chunk('V02',S2,list(range(14,20)),b),chunk('V02',S2,list(range(20,27)),b)],
 "pt":["Esta é a última vez que eu vou soltar de graça a receita do truque do bicarbonato com limão, e quem começar hoje vai precisar renovar o guarda-roupa até segunda-feira. Eu aposto um milhão de dólares que você vai estar usando um biquíni XS até setembro se preparar a receita na ordem correta, e é isso que separa quem sai do XL de quem não vê os números da balança caírem. Então preste atenção pelos próximos 30 segundos, porque eu juro que é a última vez que vou falar disso no meu perfil. Sério, se você está tomando o shot de bicarbonato há pelo menos 5 dias e não precisou correr para a loja comprar uma calça nova tamanho M, você provavelmente caiu em alguma versão falsa que estão espalhando por aí na internet. A versão real do truque custa $3.000 e uma consulta particular com a Dra. Kylie Sakaida, nutricionista das estrelas de Hollywood, e exige a ordem correta e o tempo exato para ir do XL ao S em menos de 3 meses.",
  "Antes de continuar, um aviso sério. Em comemoração a mais de 70.000 mulheres que perderam pelo menos 9 libras com esta receita de shot bariátrico, o vídeo curto da receita original da Dra. Kylie, que já ajudou nomes como Oprah, Kelly Clarkson e Melissa McCarthy a emagrecer, está totalmente de graça pelos próximos 20 minutos. Clique em Saiba Mais agora e copie a receita correta antes que ela saia do ar. A Oprah vai me matar por revelar isso, mas foi esta receita de shot de bicarbonato que ela usou para ir do XL ao M depois dos 70. É impossível você não acordar 3 libras mais magra amanhã se fizer esta receita do jeito certo hoje. A combinação desta receita é mais poderosa do que um caminhão de Ozempic. Prepare-se para chorar de alegria no dia em que conseguir vestir XS pela primeira vez em anos.",
  "Eu aposto $1 milhão em dinheiro que você vai sair do XL em no máximo 5 dias com este truque do shot de bicarbonato. Esta receita liga o modo turbo do metabolismo e é até 18 vezes mais forte do que o cardio na esteira. O resultado? O seu corpo entra em modo de queima em alta velocidade 24 horas por dia. Você vai precisar comer McDonald's todo dia só para não ficar magra demais. Para assistir ao vídeo completo com o passo a passo, clique no link abaixo.",
  "Este vídeo da receita já foi banido 7 vezes da internet, e eu suspeito que sejam os fabricantes do Mounjaro. Se ainda estiver disponível quando você clicar, agradeça e assista. Pode ser a sua última chance de ver de graça. No vídeo, você vai descobrir a ordem correta para preparar a receita em casa e o tempo específico para ver a sua calça XL escorregando antes que setembro de 2026 termine. Clique no botão abaixo, assista agora e prepare o seu primeiro shot hoje. Se você já tentou de tudo e nunca conseguiu emagrecer, esta é a sua chance. Clique em Saiba Mais e esteja pronta para perder pelo menos 3 libras amanhã de manhã."],
 "prints":[(0,"dr_oz_live_bicarbonato_gelo","Abertura: Dr. Oz (avatar) em 'LIVE' no Instagram ('Dr.oz', 1.554 espectadores) segurando a caixa de bicarbonato Arm & Hammer, tigela de gelo à frente e comentários rolando"),
  (7,"dr_oz_abrindo_caixa","Dr. Oz abrindo a caixa de bicarbonato"),
  (10,"dr_oz_closeup_caixa","Dr. Oz em close com a caixa; 'I bet a million dollars that you will be wearing an XS bikini'"),
  (25,"dr_oz_fake_version","Dr. Oz; 'you probably fell for some fake version'"),
  (35,"dr_oz_3000_dollars","Dr. Oz; 'The real version of the trick costs $3,000'"),
  (47,"dr_oz_serious_warning","Dr. Oz; 'Before continuing, a serious warning'"),
  (62,"dr_oz_click_learn_more","Dr. Oz; 'Click learn more now and copy the correct recipe'"),
  (66,"dr_oz_oprah_gonna_kill_me","Dr. Oz; 'Oprah is gonna kill me for revealing this'"),
  (83,"dr_oz_1_million_cash","Dr. Oz; 'I bet $1 million in cash'"),
  (98,"dr_oz_mcdonalds_every_day","Dr. Oz; 'You will need to eat McDonald's every day'"),
  (103,"dr_oz_banned_7_times","Dr. Oz; 'This recipe video has already been banned 7 times'"),
  (120,"dr_oz_click_the_button_below","Dr. Oz; 'Click the button below, watch now'"),
  (128,"dr_oz_ultimo_frame","Dr. Oz; 'Click Learn more and be ready to lose at least 3 pounds'"),
  (130,"cartela_click_the_button_below","Cartela 'CLICK THE BUTTON BELOW' com setas vermelhas (CTA final)")]})
b=load('V03'); S3="MULHER (UGC, blusa branca e legging cinza)"
ADS.append({"n":3,"W":"VSL-Pipeline-V03","titulo":"AD 03 — video-06-10-2026 (1:15) — [ESPANHOL] Gelatina bariátrica: 'que lipo que nada' (legendas com grafia alterada)","lang":"ES",
 "chunks":[chunk('V03',S3,list(range(0,9)),b),chunk('V03',S3,list(range(9,15)),b),chunk('V03',S3,list(range(15,21)),b)],
 "pt":["Preparei este truque da gelatina bariátrica e agora não consigo parar de perder peso. Ai, mas é que não existe um estudo que comprove a eficácia da gelatina bariátrica na hora certa. Por favor, mulher. Depois de 2 gestações, uma cesárea e um parto normal, olha como ficou esta barriga. Antes deste truque eu não tinha nem coragem de colocar um topzinho assim, jamais. E agora você vai me perguntar: você fez lipo, amiga? Que lipo que nada! Eu não fiz nada nem me matei na academia. Isto aqui é para nós, as simples mortais que não temos $1.000 para gastar todo mês em Ozempic ou Mounjaro.",
  "Então, o que a gente faz? Usa a cabeça. É só uma mistura específica de gelatina caseira que tem um efeito parecido com o de uma cirurgia bariátrica, tomada exatamente do jeito certo todos os dias em jejum. Só lembre de fazer este truque antes de tomar o seu café da manhã normal. Leva menos de 30 segundos para preparar e custa centavos. Quero ver você testar isso por 7 dias e não voltar aqui para me dizer que a sua cintura não desinchou e afinou em uma única semana.",
  "Vai lá fazer, mulher, é incrivelmente fácil. Deixei o link com o vídeo curto onde mostram o passo a passo exato de como preparar no botão que está aqui embaixo. Só preste muita atenção em como se faz e assista até o final. Sinceramente, estou tendo que controlar o meu marido, porque ele já está falando em ter um terceiro filho desde que viu como a minha cintura voltou a ficar. Clique no botão abaixo, vai ver o vídeo e depois me agradece. Tchau, tchau."],
 "prints":[(0,"gelatina_po_vermelho_tigela","Abertura: despejando gelatina em pó vermelha numa tigela; legenda 'preparé este truc0 de la gelatina' (grafia alterada para burlar moderação)"),
  (2,"gelatina_b4r1atr1c4","Tigela; legenda 'b4r1atr1c4 y ahora no puedo parar de p3rder p3so'"),
  (4,"mulher_blusa_branca_ay_pero","Mulher (UGC, blusa branca, legging cinza) com caneta na mão; 'ay pero... un estudio'"),
  (6,"caixa_jello_morango","Caixa de Jell-O de morango sobre a mulher; 'la efectividad de la gelatina b4r1atr1c4 a la hora correcta'"),
  (12,"mulher_mira_esta_barriga","Mulher mostrando a barriga; 'mira cómo quedó esta barriga'"),
  (14,"foto_antes_cadeira","Foto 'antes' (mulher sentada, mais gorda) em PIP; 'antes de este truc0'"),
  (16,"foto_antes_top","Foto 'antes' de top preto; 'un topcito así jamás'"),
  (20,"print_mensagem_bicarbonato","Print de mensagem de seguidora ('Estoy haciendo el truco del bicarbonato...'); 'qué lipo ni qué nada'"),
  (21,"mulher_print_no_me_he_hecho_nada","Mulher com print de mensagem; 'yo no me he hecho nada ni me he matado en el gimnasio'"),
  (26,"print_1000_dolares","Print de mensagem; legenda '$1.000'"),
  (28,"mulher_os3mp1c_monj4ro","Mulher; legenda 'para gastar todos los meses en os3mp1c o monj4ro'"),
  (32,"print_2_meses_resultados","Print de mensagem ('Ya llevo tomando 2 meses y sí, ¡veo resultados!'); 'una mezcla específica de gelatina casera'"),
  (37,"mulher_forma_correcta","Mulher; 'b4r1atr1c4 tomada exactamente de la forma correcta'"),
  (41,"mulher_antes_del_desayuno","Mulher; 'de hacer este truc0 antes de tomar tu desayuno normal'"),
  (44,"mulher_30_segundos_centavos","Mulher; 'toma menos de 30 segundos prepararla y cuesta centavos'"),
  (50,"mulher_cintura_se_desinflo","Mulher; 'tu cintura no se desinfló y se afinó en una sola semana'"),
  (55,"jello_pote_cool_whip","Caixa de Jell-O e pote de Cool Whip; 'es increíblemente fácil'"),
  (57,"colher_po_passo_a_passo","Colher com pó e caixa de Jell-O; 'donde muestran el paso a paso'"),
  (61,"tigela_bicarbonato_boton_abajo","Tigela com pó branco; 'en el botón que está aquí abajo'"),
  (64,"despejando_po_gelatina_vermelha","Despejando pó na gelatina vermelha; 'sinceramente estoy teniendo que controlar a mi esposo'"),
  (68,"gelatina_rosa_espumando","Gelatina rosa espumando na jarra medidora; 'desde que vio cómo me volvió a quedar la cintura'"),
  (71,"jarra_haz_clic_boton","Jarra medidora; 'haz clic en el botón de abajo'"),
  (74,"mulher_chao_chao","Mulher acenando; 'chao chao'")]})
b=load('V04'); S4="MULHER 50+ (UGC, cozinha, voz em off)"
ADS.append({"n":4,"W":"VSL-Pipeline-V04","titulo":"AD 04 — video-13-11-2026 (1:10) — 'Mães, nunca misturem bicarbonato com estas 3 coisas' (limão, gelo e o 3º ingrediente)",
 "chunks":[chunk('V04',S4,list(range(0,5)),b),chunk('V04',S4,list(range(5,11)),b),chunk('V04',S4,list(range(11,16)),b)],
 "pt":["Mães, nunca misturem bicarbonato de sódio com estas 3 coisas, a não ser que estejam prontas para comprar um guarda-roupa inteiro novo. Assistam até o fim. Esta era eu antes, no meu peso máximo, e esta sou eu agora. Sem dietas malucas, sem programas caros, só isto. O 1 é limão, o 2 é gelo e o 3 é o que toda versão da internet deixa de fora.",
  "Eu vivia vendo isso no meu feed, e toda versão pulava o 3º ingrediente. Então a minha irmã me mandou a versão com a proporção real. Keto, low-carb, sal rosa, jejum: nada disso pegou. Mas isto? Libra após libra, semana após semana, e o peso não voltou. A minha fome diminuiu e os meus jeans foram de apertados a confortáveis a caindo.",
  "A minha irmã não me reconheceu no Dia de Ação de Graças. Agora ela também faz toda noite. Leva menos de um minuto com 3 coisas que já estão na minha cozinha, e custa uns $2, então ninguém nunca vai fazer um comercial disso. Eu salvei o clipe curto com as quantidades exatas. Toque em Saiba Mais e assista antes de testar."],
 "prints":[(0,"bicarbonato_limao_colheres","Abertura: caixa de Arm & Hammer, limão e colheres medidoras na bancada; 'Moms, never mix baking soda with these 3 things'"),
  (3,"despejando_bicarbonato_copo","Despejando bicarbonato no copo com limão e gelo"),
  (5,"espremendo_limao_copo","Espremendo limão no copo; 'Watch till the end'"),
  (7,"celular_foto_antes","Celular com foto 'antes' (mulher gorda); 'This was me before at my heaviest'"),
  (10,"mulher_50_copo_this_is_me_now","Mulher 50+ (camiseta verde) erguendo o copo; 'and this is me now'"),
  (16,"rodela_limao_copo_gelo","Colocando rodela de limão no copo com gelo; '1 is lemon'"),
  (19,"geladeira_gelo","Pegando gelo na geladeira; '2 is ice'"),
  (21,"colheres_medidoras_3_ingredientes","Três colheres medidoras com pós; '3 is the one every version online leaves out'"),
  (25,"mexendo_jarra_branca","Mexendo a mistura branca na jarra; 'every version skipped the 3rd ingredient'"),
  (33,"armario_potes_sal_rosa","Armário com potes (sal rosa, pó branco); 'Keto, low-carb, pink salt, fasting'"),
  (38,"despejando_forma_gelo","Despejando a mistura na forma de gelo azul; 'Pound after pound, week after week'"),
  (44,"forma_gelo_freezer","Forma de gelo no freezer; 'my jeans went from tight to comfortable'"),
  (50,"cubos_mistura_copo","Desenformando os cubos no copo; 'My sister didn't recognize me at Thanksgiving'"),
  (55,"copo_limao_mexendo","Mexendo o copo com rodela de limão; 'Takes less than a minute with 3 things already in my kitchen'"),
  (59,"caixa_bicarbonato_copo_2_dollars","Caixa de bicarbonato ao lado do copo; 'it costs about $2'"),
  (64,"mulher_50_copo_tap_learn_more","Mulher 50+ com o copo; 'Tap Learn More and watch it before you try it'")]})
b=load('V05'); S5="MULHER (UGC, jaqueta preta, à mesa)"
ADS.append({"n":5,"W":"VSL-Pipeline-V05","titulo":"AD 05 — 1 Facebook.mp4 (2:00) — [ESPANHOL] 'Meu marido me chamou de iludida': a receita viral da gelatina (89 → 65 kg)","lang":"ES",
 "chunks":[chunk('V05',S5,list(range(0,10)),b),chunk('V05',S5,list(range(10,17)),b),chunk('V05',S5,list(range(17,28)),b)],
 "pt":["O meu marido me chamou de iludida quando eu contei para ele sobre a receita viral da gelatina, mas ficou com ciúme quando me viu na praia usando o mesmo biquíni que eu usava aos 23 anos. Primeiro, você vai pegar uns 200 mililitros de água fria, acrescenta a gelatina e coloca numa tigela, ok? Agora, adicione o suco de meio limão. Ingredientes que todo mundo tem em casa, né? Mas preste muita atenção, porque esta é a chave. Comer gelatina com limão e outros 2 ingredientes simples não funcionou comigo no começo. Foi só quando eu passei de 89 para 65 quilos que entendi o segredo. Eu só precisava de um pequeno ajuste na minha rotina e bum. Os resultados foram tão rápidos que, no aniversário do meu sobrinho, a minha cunhada me perguntou baixinho se eu tinha feito lipo ou alguma cirurgia secreta. Este é o método caseiro que salvou o meu corpo.",
  "Desde o meio do ano, este estranho truque da gelatina viralizou nas redes sociais porque está ajudando milhares de mulheres a derreter gordura de forma acelerada. Eu guardei este segredo por um tempo porque queria ter certeza, mas, quando vi que tanto eu quanto o meu marido perdemos tamanhos em poucas semanas e os nossos exames médicos saíram perfeitos, soube que tinha que compartilhar. Na verdade, foi ele quem me convenceu. Ele viu no noticiário e me pediu para a gente testar. Honestamente, eu não acreditava que fosse funcionar, mas não tinha nada a perder. E hoje estou feliz por ter feito. Finalmente podemos voltar a aproveitar as nossas comidas caseiras, como umas tortillas gostosas ou um bom prato de arroz, sem sentir culpa nem medo da balança.",
  "Este truque da gelatina já saiu em várias reportagens de saúde, mas talvez você tenha perdido. Por sorte, eu guardei o vídeo exato que me ensinou a fazer em casa. Para ver a receita passo a passo, é só tocar no botão abaixo que diz 'mais informações'. Mas eu te aviso, a indústria farmacêutica odeia isto. É uma receita que gera os mesmos resultados daqueles tratamentos de clínicas de luxo, mas sem gastar milhares de pesos e sem dor. É natural, seguro e ataca a raiz da gordura acumulada. Se este vídeo apareceu para você, tome como um sinal. Toque no botão abaixo, assista ao vídeo curto e copie a receita antes que apaguem. Ah, e o vídeo também revela 3 alimentos supostamente saudáveis que na verdade estão te engordando, incluindo um que você come no café da manhã. Eu fiquei em choque. Clique em 'mais informações' e assista agora."],
 "prints":[(0,"mulher_praia_biquini_mi_esposo","Abertura: mulher gorda de costas na praia, de biquíni azul; 'MI ESPOSO ME ILUSA CUANDO LE'"),
  (5,"mulher_praia_celoso","Mulher na praia tirando a blusa; 'CELOSO CUANDO ME USANDO EL MISMO BIKINI'"),
  (8,"mulher_jaqueta_preta_primero","Mulher (UGC, jaqueta preta) à mesa; 'PRIMERO VAS A TOMAR UNOS 200 ML'"),
  (10,"despejando_agua_tigela","Despejando água fria na tigela; 'DE AGUA FRÍA'"),
  (15,"gelatina_vermelha_leite","Despejando gelatina vermelha na panela com líquido branco; 'JUGO DE MEDIO LIMÓN'"),
  (18,"mulher_presta_mucha_atencion","Mulher à mesa; 'PERO PRESTA MUCHA ATENCIÓN PORQUE ESTA ES LA CLAVE'"),
  (25,"mulher_pase_de_89_a_65","Mulher; 'PASÉ DE 89 A 65'"),
  (27,"despejando_po_rosa_gelatina","Despejando pó rosa na gelatina vermelha; 'EL SECRETO: SOLO NECESITABA UN PEQUEÑO AJUSTE'"),
  (33,"mulher_cumpleanos_cunada","Mulher gesticulando; 'CUMPLEAÑOS DE MI... MI CUÑADA ME... LIPO O ALGUNA'"),
  (42,"batendo_gelatina_fouet","Batendo a gelatina vermelha com fouet; 'ESTE EXTRAÑO TRUCO DE LA GELATINA VIRAL'"),
  (46,"gelatina_rosa_panela_derretir","Gelatina rosa espumando na panela; 'A MILES DE MUJERES A DERRETIR GRASA'"),
  (49,"despejando_creme_branco","Despejando creme branco na gelatina; 'ACELERADA GUARDÉ'"),
  (51,"mulher_queria_estar_segura","Mulher; 'QUERÍA ESTAR SEGURA QUE TANTO YO... BAJAMOS TALLAS'"),
  (57,"gelatina_rosa_blocos_brancos","Blocos brancos na gelatina rosa; 'MÉDICOS SALIERON PERFECTOS, QUE COMPARTIRLO'"),
  (63,"despejando_gelatina_rosa_forma","Despejando a gelatina rosa na forma; 'HONESTAMENTE YO NO CREÍA QUE FUERA A FUNCIONAR'"),
  (66,"gelatina_rosa_filme_plastico","Cobrindo a forma com filme plástico; 'NADA QUE PERDER... POR FIN PODEMOS'"),
  (72,"mulher_tortillas_plato_arroz","Mulher; 'COMIDAS CASERAS COMO TORTILLAS O UN BUEN PLATO DE ARROZ'"),
  (78,"mulher_reportajes_de_salud","Mulher; 'HA SALIDO EN REPORTAJES DE SALUD'"),
  (85,"mulher_boton_de_abajo_mas_informacion","Mulher com as mãos juntas; 'PARA VER LA... BOTÓN DE ABAJO QUE DICE MÁS INFORMACIÓN'"),
  (90,"mulher_farmaceutica_odia_esto","Mulher; 'PERO TE ADVIERTO, FARMACÉUTICA ODIA ESTO'"),
  (93,"cortando_gelatina_faca","Cortando a gelatina rosa com faca; 'QUE GENERA LOS RESULTADOS QUE ESOS TRATAMIENTOS DE CLÍNICAS DE LUJO'"),
  (99,"bloco_gelatina_natural_seguro","Levantando um bloco de gelatina rosa; 'ES NATURAL, SEGURO Y ATACA LA GRASA ACUMULADA'"),
  (104,"colher_gelatina_si_este_video","Colher cortando o bloco de gelatina no prato; 'SI ESTE VIDEO APARECIÓ PARA TI, TÓMALO COMO UNA SEÑAL'"),
  (108,"prato_gelatina_copia_la_receta","Prato com gelatina; 'CORTO Y COPIA LA RECETA ANTES BORREN'"),
  (110,"mulher_ah_y_el_video","Mulher à mesa; 'AH Y EL VIDEO... SUPUESTAMENTE... REALIDAD TE ESTÁN'"),
  (117,"mulher_haz_clic_mas_informacion","Mulher; 'YO QUEDÉ EN SHOCK. HAZ CLIC EN MÁS INFORMACIÓN Y'")]})
blocos=[]; falantes=[]
for ad in ADS:
    C=ad['chunks']; assert len(C)==len(ad['pt']),(ad['n'],len(C),len(ad['pt']))
    falas=[]
    for c,p in zip(C,ad['pt']):
        falas.append({"falante":c['spk'],"ts":ts(c['start']),"en":c['en'],"pt":p})
        if c['spk'] not in falantes: falantes.append(c['spk'])
    prints=[]
    for s,sl,l in ad['prints']:
        assert re.fullmatch(r'[a-z0-9_]+',sl),sl
        arq=f"ad{ad['n']:02d}_{sl}_00-{s//60:02d}-{s%60:02d}.jpg"
        Image.open(f"{ad['W']}/full/{s:05d}.jpg").convert('RGB').save(f'VSL-Pipeline-ADS7/frames/{arq}','JPEG',quality=88)
        prints.append({"ts":ts(s*1000),"legenda":l,"arquivo":arq})
    bl={"n":ad['n'],"titulo":ad['titulo'],"inicio":"0:00","fim":ts(C[-1]['end']),"falas":falas,"prints":prints}
    if ad.get('lang')=='ES': bl["rotulo_original"]="Transcrição original (espanhol)"
    blocos.append(bl)
doc={"titulo":"ADS — pasta Drive (5 anúncios: bicarbonato e gelatina) — Transcrição original + Tradução PT-BR + Prints",
 "fonte":"Fonte: pasta do Drive com 5 vídeos (video-03-09, 17-09, 06-10 e 13-11-2026, mais '1 Facebook.mp4', colocado por último por não ter data). Transcrição: AssemblyAI (speaker labels), falantes conferidos pelos frames. ADs 01, 02 e 04 em inglês; ADs 03 e 05 em espanhol (coluna 'Transcrição original'). Tradução fiel: nomes, marcas, valores (dólares, pesos), libras e quilos mantidos como falados. AD 02: 'live' simulada no Instagram com avatar do Dr. Oz (nome de usuário 'Dr.oz', 1.554 espectadores, comentários rolando), quadro praticamente estático; cita uma 'Dra. Kylie Sakaida'. AD 03: as legendas queimadas usam grafia alterada (truc0, b4r1atr1c4, p3rder p3so, os3mp1c, monj4ro) para burlar a moderação; a transcrição segue o áudio normal. AD 04: narração em off sobre b-roll do preparo, a mulher só aparece com o copo no início e no fim.",
 "nota_prints":"Minutagens: cada trecho traz o [m:ss] em que começa. Prints: frames dos momentos em que muda a cena, o lettering ou aparece a prova, com legenda descrevendo a imagem e o texto queimado no vídeo, nomeados adNN_descricao_HH-MM-SS.jpg na pasta frames/.",
 "falantes":falantes,"blocos":blocos}
json.dump(doc,open('VSL-Pipeline-ADS7/doc.json','w'),ensure_ascii=False,indent=1)
print(len(blocos),'ads',sum(len(b['falas']) for b in blocos),'trechos',sum(len(b['prints']) for b in blocos),'prints')
for bl in blocos:
    for f in bl['falas']:
        r=len(f['pt'])/max(1,len(f['en']))
        if r<0.85 or r>1.45: print('ratio',bl['n'],f['ts'],round(r,2))
