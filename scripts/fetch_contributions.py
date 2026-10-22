"""Fetch public GitHub contribution cells; fail without replacing valid prior data."""
from html.parser import HTMLParser
from pathlib import Path
from datetime import date
import json,re,urllib.request,sys,os
ROOT=Path(__file__).resolve().parents[1]
class CalendarParser(HTMLParser):
 def __init__(self):super().__init__();self.cells={};self.tips={};self.tip=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('td','rect') and 'data-date' in a and 'data-level' in a:self.cells[a.get('id',a['data-date'])]={'date':a['data-date'],'level':int(a['data-level'])}
  if tag=='tool-tip':self.tip=a.get('for');self.tips[self.tip]=''
 def handle_data(self,s):
  if self.tip:self.tips[self.tip]+=s
 def handle_endtag(self,tag):
  if tag=='tool-tip':self.tip=None
 def days(self):
  days=[]
  for key,cell in self.cells.items():
   tip=self.tips.get(key,'').strip();m=re.match(r'([\d,]+) contributions?\b',tip)
   if m:count=int(m[1].replace(',',''))
   elif tip.startswith('No contributions'):count=0
   else:raise ValueError('Unrecognized contribution tooltip; previous data preserved')
   date.fromisoformat(cell['date'])
   if cell['level'] not in range(5) or count<0:raise ValueError('Invalid contribution cell')
   days.append(dict(cell,count=count))
  days.sort(key=lambda x:x['date'])
  if len(days)<350 or len({x['date'] for x in days})!=len(days):raise ValueError('Incomplete calendar; previous data preserved')
  return days
if __name__=='__main__':
 username=os.environ.get('PROFILE_USERNAME','lightzealot')
 if not re.fullmatch(r'[A-Za-z0-9-]+',username):raise ValueError('Invalid username')
 if len(sys.argv)>1:html=Path(sys.argv[1]).read_text()
 else:
  req=urllib.request.Request(f'https://github.com/users/{username}/contributions',headers={'User-Agent':'github-profile-art','Accept-Language':'en-US,en;q=0.9'})
  with urllib.request.urlopen(req,timeout=30) as r:html=r.read().decode()
 p=CalendarParser();p.feed(html);days=p.days()
 dest=ROOT/'data/contributions.json';tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps({'username':username,'days':days},ensure_ascii=False,indent=2)+'\n');tmp.replace(dest)
 print(f'Validated {len(days)} days; {sum(x["count"] for x in days)} contributions')
