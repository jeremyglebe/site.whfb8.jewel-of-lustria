from pathlib import Path
from lxml import html
root=Path(__file__).parent/'docs'; failures=[]
for p in root.glob('*.html'):
 d=html.fromstring(p.read_bytes()); ids=d.xpath('//@id')
 if len(ids)!=len(set(ids)):failures.append((p.name,'duplicate IDs'))
 if len(d.xpath('//main'))!=1:failures.append((p.name,'expected one main'))
 if not d.xpath('//html[@lang="en"]'):failures.append((p.name,'missing language'))
 for a in d.xpath('//a[@href]'):
  href=a.get('href')
  if href.startswith(('https:','http:','mailto:')):continue
  target,_,frag=href.partition('#'); f=root/target if target else p
  if not f.exists():failures.append((p.name,href,'missing file'));continue
  if frag and frag not in html.fromstring(f.read_bytes()).xpath('//@id'):failures.append((p.name,href,'missing anchor'))
print(f'Checked {len(list(root.glob("*.html")))} pages.');print('Failures:',failures)
assert not failures
