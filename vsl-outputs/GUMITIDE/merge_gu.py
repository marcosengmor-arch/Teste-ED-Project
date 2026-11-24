import json, re
W='VSL-Pipeline-GUMITIDE'
OFF=[0,1240000,2480000,3720000]
words=[]; dur=0
for p in range(4):
    d=json.load(open(f'VSL-Pipeline-GU_P{p+1}/transcricao_raw.json'))
    for w in d['words']:
        w=dict(w); w['start']+=OFF[p]; w['end']+=OFF[p]; w['speaker']=f"{p+1}{w['speaker']}"; words.append(w)
    dur=OFF[p]/1000+d.get('audio_duration',0)
raw={"words":words,"audio_duration":dur,"text":' '.join(w['text'] for w in words)}
json.dump(raw,open(f'{W}/transcricao_raw.json','w'),ensure_ascii=False)
sents=[]; cur=[]
for w in words:
    cur.append(w)
    if re.search(r'[.!?…]["\')]?$', w['text']) or len(cur)>60:
        sents.append(cur); cur=[]
if cur: sents.append(cur)
out=[]
for i,s in enumerate(sents):
    sp=[w['speaker'] for w in s]; spk=max(set(sp),key=sp.count)
    out.append({"i":i,"speaker":spk,"start_ms":s[0]['start'],"end_ms":s[-1]['end'],"text":' '.join(w['text'] for w in s)})
json.dump(out,open(f'{W}/sentences.json','w'),ensure_ascii=False)
with open(f'{W}/sentences.txt','w') as f:
    for s in out:
        t=s['start_ms']//1000; f.write(f"{s['i']:4d} [{t//60}:{t%60:02d}] {s['speaker']} {s['text']}\n")
print(len(out),'sentences',len(words),'words',dur,'s')
