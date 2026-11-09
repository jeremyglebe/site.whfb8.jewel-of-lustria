from lxml import html,etree
from pathlib import Path
from copy import deepcopy
import re,json,hashlib
ROOT=Path(__file__).parent; OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
SRC=ROOT/'source'
source=SRC/'drive-full-source.html'; doc=html.fromstring(source.read_bytes()); pages=doc.xpath('//body/div[@class="page"]')
# Author-requested faction grouping corrections, applied to the web adaptation.
for section in list(pages[50].xpath('./main/section')):
 heading=' '.join(section.xpath('./h2')[0].itertext()).strip()
 destination={'Ogre Kingdoms':44,'Halflings':42,'Albion':43}[heading]
 section.getparent().remove(section)
 target=pages[destination].xpath('./main')[0]
 if heading=='Halflings':
  target.insert(1,section)
  first=section.xpath('./p')[0]
  first.text='Halfling expeditions come from the Mootland within the Empire. '+(first.text or '')
 elif heading=='Ogre Kingdoms':
  target.append(section)
  first=section.xpath('./p')[0]
  first.text='An Ogre Kingdoms expedition typically comes from the eastern Ogre Kingdoms, even though Ogre mercenaries can be found elsewhere. '+(first.text or '')
 else:target.append(section)
pages[44].xpath('./header/h2')[0].text='The Eastern Kingdoms'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def text(e): return ' '.join(' '.join(e.itertext()).split())
def blocks(indices): return [deepcopy(pages[i]) for i in indices]
groups=[('expedition','Expedition construction',blocks([0])),('campaign','Campaign rules',blocks([1])),('terrain','Lustrian terrain',blocks([2])),('story','The story',blocks([3,4,5,6])),('first-blood','I · First Blood',blocks([7,8])),('star-charts','II · Star Charts of the Old Ones',blocks([9,10,11])),('jade-vein','III · Crossing the Jade Vein',blocks([12,13,14])),('veterans','Battle-Hardened Veterans',blocks([15])),('jungle-tyrant','IV · Slay the Jungle Tyrant!',blocks([16,17,18])),('locating-the-crater','V · Locating the Crater',blocks([25,31,32,33,34])),('crater-city','VI · The Final Clash',blocks(range(36,42))),('factions','The expeditions',blocks(range(42,50)))]
lay=html.fromstring((SRC/'05.Scenario.5.Layouts.html').read_bytes());groups[9][2].extend(deepcopy(x) for x in lay.xpath('//body/*'))
nav='<a class="brand" href="index.html">JEWEL <span>OF</span> LUSTRIA</a><nav aria-label="Main"><a href="story.html">Story</a><a href="index.html#battles">Battles</a><a href="campaign.html">Rules</a><a href="factions.html">Factions</a></nav>'
def wrap(title,content,aside=''):
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+' · Jewel of Lustria</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="sitebar">'+nav+'</header>'+content+'<footer>Jewel of Lustria · An expedition campaign for Warhammer Fantasy Battles<br><a href="sources.html">Source notes</a></footer></body></html>'
for key,title,parts in groups:
 toc=[]; chunks=[]; counts={}
 for part in parts:
  for el in part.xpath('.//*[@style]'):del el.attrib['style']
  for el in part.xpath('.//script'):el.getparent().remove(el)
  for el in part.xpath('.//main'):el.tag='div'
  for el in part.xpath('.//header/h1'):
   el.tag='p';el.set('class','eyebrow')
  for el in part.xpath('.//h2|.//h3'):
   label=text(el); ident=slug(label);counts[ident]=counts.get(ident,0)+1
   if counts[ident]>1:ident+='-'+str(counts[ident])
   el.set('id',ident)
   if el.tag=='h2':toc.append('<a href="#'+ident+'">'+label+'</a>')
  for table in part.xpath('.//table'):
   parent=table.getparent();idx=parent.index(table);parent.remove(table);sc=etree.Element('div',{'class':'table-scroll','tabindex':'0'});sc.append(table);parent.insert(idx,sc)
  chunks.append(etree.tostring(part,encoding='unicode',method='html'))
 notice=''
 idx=[g[0] for g in groups].index(key)
 pager='<nav class="pager" aria-label="Adjacent sections">'+('' if idx==0 else '<a href="'+groups[idx-1][0]+'.html">← '+groups[idx-1][1]+'</a>')+('' if idx==len(groups)-1 else '<a href="'+groups[idx+1][0]+'.html">'+groups[idx+1][1]+' →</a>')+'</nav>'
 body='<div class="reading-layout"><aside><details open><summary>On this page</summary>'+''.join(toc)+'</details><hr><a href="expedition.html">Build an expedition</a><a href="campaign.html">Campaign rules</a><a href="terrain.html">Terrain reference</a></aside><main id="main"><div class="page-heading"><p class="eyebrow">Jewel of Lustria</p><h1>'+title+'</h1></div>'+notice+''.join(chunks)+pager+'</main></div>'
 (OUT/(key+'.html')).write_text(wrap(title,body))
cards=''.join('<a class="battle-card" href="'+k+'.html"><span class="eyebrow">'+('Scenario '+str(i+1))+'</span><h3>'+t.split(' · ')[-1]+'</h3><span class="arrow">↗</span></a>' for i,(k,t,_) in enumerate([groups[j] for j in [4,5,6,8,9,10]]))
opening=''.join(etree.tostring(deepcopy(x),encoding='unicode',method='html') for x in pages[3].xpath('./main/section'))
home='<main id="main" class="home"><header class="campaign-heading"><h1>Jewel of Lustria</h1><a href="index.html#battles">Browse battles ↓</a></header><article class="campaign-opening"><h2>A Gift from the Stars</h2>'+opening+'<a class="continue-story" href="story.html#act-i-the-world-arrives-in-lustria">Continue to Act I →</a></article><section class="start-links" aria-label="Campaign reference"><a href="expedition.html">Expedition construction</a><a href="campaign.html">Campaign rules</a><a href="terrain.html">Terrain</a><a href="factions.html">Factions</a></section><section id="battles"><div class="section-heading"><h2>Battles</h2></div><div class="battle-grid">'+cards+'</div><a class="veteran" href="veterans.html">Between Acts I & II: Battle-Hardened Veterans →</a></section></main>'
(OUT/'index.html').write_text(wrap('The Jewel of Lustria',home))
notes='<main id="main" class="notes"><h1>Source notes</h1><p>This web edition preserves the campaign supplied by Jeremy in <a href="https://drive.google.com/file/d/1AjeoImMfX9zJI-XqKqllFq2IExX-WGfq/view">The Jewel of Lustria – Expedition Campaign</a>.</p><h2>Scenario V</h2><p>The source contains three versions. Following the author’s direction that earlier versions precede the final, this edition uses the last rules block: the six-turn race through a central Convergence Zone, with four initial defenses and three additional defenses per new branch. The identical narrative introduction is retained once. The superseded two-phase Gauntlet variants and their placeholder spell tables are not part of the playable reference.</p><p>The two track diagrams come from the original standalone 05.Scenario.5.Layouts.html, uploaded 11 April 2026, and illustrate the Convergence Zone layout.</p><h2>Editorial treatment</h2><p>Rules and narrative wording are preserved except for the author’s requested faction corrections: Ogre Kingdoms are grouped with the Eastern Kingdoms, Halflings with the Empire as inhabitants of the Mootland, and Albion with the Western Kingdoms. Page breaks, typography, navigation and table layout are adapted for the web. Scenario I and IV have different names in the narrative overview and detailed battle rules; both original wordings remain. No hex-map follow-up material is included.</p></main>'
(OUT/'sources.html').write_text(wrap('Source notes',notes))
(ROOT/'source-manifest.json').write_text(json.dumps([{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in SRC.glob('*.html')],indent=2))
print('Built',len(list(OUT.glob('*.html'))),'pages')
