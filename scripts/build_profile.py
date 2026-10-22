"""Generate original terminal artwork. Portrait requires Pillow; calendar is stdlib-only."""
from pathlib import Path
from html import escape
import json, os
ROOT=Path(__file__).resolve().parents[1]
STATIC=os.environ.get('STATIC')=='1'
def svg(w,h,body,title):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>text{{font-family:ui-monospace,DejaVu Sans Mono,monospace}}.reveal{{animation:appear .65s both;animation-delay:var(--delay,0s)}}@keyframes appear{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}@media(prefers-reduced-motion:reduce){{.reveal{{animation:none}}}}{' .reveal{animation:none}' if STATIC else ''}</style><rect width="{w}" height="{h}" rx="16" fill="#0d1117"/><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="#263342"/>{body}</svg>'''
def txt(x,y,s,size=14,color='#c9d1d9',extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'
def chrome(label,w):
 return ''.join(f'<circle cx="{24+i*17}" cy="24" r="4" fill="{c}"/>' for i,c in enumerate(['#ff6b6b','#f5c86b','#56d6ac']))+txt(84,29,label,11,'#8b949e')+f'<path d="M1 45H{w-1}" stroke="#263342"/>'
def card():
 body=chrome('andy@github: ~ / whoami',520)
 body+=txt(26,91,'ANDRÉS GÓMEZ',29,'#f0f6fc')+txt(26,119,'Ingeniero de sistemas',14,'#8b949e')
 rows=[('ENFOQUE','Ciberseguridad + IA'),('DESARROLLO','Aplicaciones para negocios'),('AUTOMATIZO','Procesos y tareas repetitivas'),('LAB','Linux · Docker · redes'),('IA LOCAL','Ollama · asistentes'),('COMPARTO','@andresgomez.ia')]
 for i,(k,v) in enumerate(rows):
  y=165+i*33
  body+=f'<g class="reveal" style="--delay:{.25+i*.13}s">'+txt(26,y,k,11,'#58d5e8')+txt(143,y,v,12)+'</g>'
 body+='<path d="M26 365H494" stroke="#263342"/>'+txt(26,394,'Soluciones útiles para problemas reales.',12,'#8b949e')
 (ROOT/'assets/info-card.svg').write_text(svg(520,420,body,'Andrés Gómez: ciberseguridad, inteligencia artificial y soluciones para negocios'),encoding='utf-8')
def portrait(source):
 from PIL import Image, ImageOps, ImageEnhance
 im=Image.open(source).convert('RGB'); im=ImageOps.grayscale(im);im=ImageOps.autocontrast(im,cutoff=2);im=ImageEnhance.Contrast(im).enhance(1.25).resize((68,58))
 ramp=' .,:;irsXA253hMHGS#9B&@'
 b=chrome('portrait --ascii',340)
 for y in range(im.height):
  line=''.join(ramp[round(im.getpixel((x,y))/255*(len(ramp)-1))] for x in range(im.width))
  b+=f'<g class="reveal" style="--delay:{y*.024}s">'+txt(20,67+y*5.5,line,7,'#b9d7de','xml:space="preserve" textLength="300" lengthAdjust="spacingAndGlyphs"')+'</g>'
 b+=txt(20,403,'LIGHTZEALOT / ANDY',10,'#58d5e8')
 (ROOT/'assets/portrait.svg').write_text(svg(340,420,b,'Retrato ASCII de Andrés Gómez, basado en su avatar de GitHub'),encoding='utf-8')
def calendar():
 d=json.loads((ROOT/'data/contributions.json').read_text());days=d['days']
 from datetime import date,timedelta
 first=date.fromisoformat(days[0]['date']);start=first-timedelta(days=(first.weekday()+1)%7)
 b=chrome('andy@github: ~ / activity --last-year',880)+txt(26,79,'ACTIVIDAD EN GITHUB',14,'#58d5e8')
 palette=['#17212d','#15444d','#1b707d','#2da6b8','#58d5e8']
 seen=set()
 for item in days:
  dt=date.fromisoformat(item['date']);delta=(dt-start).days;col,row=divmod(delta,7);x=42+col*15;y=111+row*15
  if dt.month not in seen and dt.day<=7:
   seen.add(dt.month);b+=txt(x,99,['','ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'][dt.month],9,'#8b949e')
  b+=f'<rect class="reveal" style="--delay:{(col+row)*.015:.3f}s" x="{x}" y="{y}" width="11" height="11" rx="2" fill="{palette[item["level"]]}"><title>{item["date"]}: {item["count"]} contribuciones</title></rect>'
 total=sum(x['count'] for x in days);active=sum(x['count']>0 for x in days)
 b+=txt(26,246,f'{total:,} contribuciones · {active} días con actividad',13)+txt(26,271,f'Datos públicos · {days[0]["date"]} → {days[-1]["date"]}',10,'#8b949e')
 b+=txt(691,246,'Menos',9,'#8b949e')
 for i,c in enumerate(palette):b+=f'<rect x="{727+i*16}" y="237" width="11" height="11" rx="2" fill="{c}"/>'
 b+=txt(812,246,'Más',9,'#8b949e')
 (ROOT/'assets/contributions.svg').write_text(svg(880,294,b,'Calendario de contribuciones reales de lightzealot en GitHub'),encoding='utf-8')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--portrait');p.add_argument('--calendar-only',action='store_true');a=p.parse_args()
 if not a.calendar_only:card()
 if a.portrait:portrait(a.portrait)
 calendar()
