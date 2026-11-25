import json, re, glob, os, importlib.util, shutil
from PIL import Image
W='VSL-Pipeline-DIVINE'
doc=json.load(open(f'{W}/doc.json'))
def tosec(t): m,s=t.split(':'); return int(m)*60+int(s)
# --- translation ---
pt={}
for f in sorted(glob.glob('pt_dv/pt_*.txt')):
    txt=open(f).read()
    for m in re.finditer(r'^### (\d+)\.(\d+)\.(\d+) \[[^\]]*\][^\n]*\n(.*?)(?=^### |\Z)',txt,flags=re.M|re.S):
        pt[(int(m[1]),int(m[2]),int(m[3]))]=m[4].strip()
missing=[];ratios=[]
for b in doc['blocos']:
    for k,m in enumerate(b['mini'],1):
        for j,x in enumerate(m['falas']):
            key=(b['n'],k,j)
            if key in pt and pt[key]:
                x['pt']=pt[key]; ratios.append((key,len(x['pt'])/max(1,len(x['en']))))
            else: missing.append(key)
print('pt missing',missing)
bad=[(k,round(r,2)) for k,r in ratios if r<0.85 or r>1.4]
print('ratio outliers',bad)
# --- picks ---
picks=[]
for f in sorted(glob.glob('picks_dv/p*.py')):
    spec=importlib.util.spec_from_file_location('p',f); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    picks+=mod.PICKS
picks.sort(key=lambda p:p[0])
secs=[p[0] for p in picks]; dups=[s for s in set(secs) if secs.count(s)>1]
print('dup secs',dups)
badslug=[p[1] for p in picks if not re.fullmatch(r'[a-z0-9_]+',p[1])]
print('bad slugs',badslug)
minis=[]
for b in doc['blocos']:
    for k,m in enumerate(b['mini'],1):
        m['prints']=[]; minis.append((tosec(m['inicio']),tosec(m['fim']),b['n'],m))
os.makedirs(f'{W}/frames',exist_ok=True)
for f in glob.glob(f'{W}/frames/*.jpg'): os.remove(f)
unassigned=[]
for sec,slug,leg in picks:
    tgt=None
    for a,z,n,m in minis:
        if a<=sec<=z: tgt=(n,m,sec); break
    if tgt is None:
        prev=[(a,z,n,m) for a,z,n,m in minis if z<sec]
        if prev:
            a,z,n,m=prev[-1]; tgt=(n,m,z)
        else: unassigned.append(sec); continue
    n,m,ts=tgt
    fn=f"b{n:02d}_{slug}_{ts//3600:02d}-{(ts%3600)//60:02d}-{ts%60:02d}.jpg"
    im=Image.open(f'{W}/full/{sec:05d}.jpg'); im.save(f'{W}/frames/{fn}',quality=88)
    m['prints'].append({"arquivo":fn,"legenda":leg})
print('unassigned',unassigned)
empty=[(b['n'],k) for b in doc['blocos'] for k,m in enumerate(b['mini'],1) if not m['prints']]
print('minis sem print',empty)
json.dump(doc,open(f'{W}/doc.json','w'),ensure_ascii=False,indent=1)
print(len(picks),'prints',len(os.listdir(f'{W}/frames')),'files')
