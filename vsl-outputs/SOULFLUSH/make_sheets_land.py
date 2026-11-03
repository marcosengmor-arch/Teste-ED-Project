import json, glob
from PIL import Image, ImageDraw, ImageFont
import sys; W=sys.argv[1] if len(sys.argv)>1 else "VSL-Pipeline-SODA-HORSE"
d = json.load(open(f'{W}/doc.json'))
def sec(ts): m,s=ts.split(':'); return int(m)*60+int(s)
def tsd(s): return f"{s//60}:{s%60:02d}"
cands = sorted(int(p.split('/')[-1][:5]) for p in glob.glob(f'{W}/cand/*.jpg'))
import os; os.makedirs(f'{W}/sheets', exist_ok=True)
COLS, CW, TH = 6, 320, 180
CH = TH+18
font = ImageFont.load_default()
sheets = []
for b in d['blocos']:
    s0, s1 = sec(b['inicio']), sec(b['fim'])
    cs = [c for c in cands if s0 <= c <= s1]
    for part in range(0, len(cs), 36):
        chunk = cs[part:part+36]
        rows = (len(chunk)+COLS-1)//COLS
        im = Image.new('RGB', (COLS*CW, rows*CH), 'white'); dr = ImageDraw.Draw(im)
        for k,c in enumerate(chunk):
            th = Image.open(f'{W}/cand/{c:05d}.jpg'); th.thumbnail((CW, TH))
            x, y = (k%COLS)*CW, (k//COLS)*CH
            im.paste(th, (x + (CW-th.width)//2, y))
            dr.rectangle([x, y+TH, x+CW, y+CH], fill='black'); dr.text((x+4, y+TH+2), f"{tsd(c)}  #{c}", fill='yellow', font=font)
        name = f"{W}/sheets/b{b['n']:02d}_{part//36+1}.jpg"; im.save(name, quality=80); sheets.append((name, len(chunk)))
for s in sheets: print(s)
print(len(sheets), "sheets")
