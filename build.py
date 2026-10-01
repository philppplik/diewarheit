import json,pathlib,shutil,html,datetime,sys,email.utils
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'site';OUT.mkdir(exist_ok=True)
BASE=ROOT/'base';data=json.loads((ROOT/'articles.json').read_text());h=html.escape
for p in BASE.iterdir():
 if p.is_file():shutil.copy(p,OUT/p.name)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
shell=BeautifulSoup((BASE/'drucker-meldet-sich-nach-14-jahren.html').read_text(),'html.parser')
notice='Satire: Handlung, Figuren, Ämter und Zitate sind frei erfunden. Der reale Nachrichtenanlass steht gesondert im Quellenkasten. KI-Illustration, kein Foto eines tatsächlichen Ereignisses.'
published=[a for a in data if a['status']=='published'];draft=not published
for a in data:
 p=BeautifulSoup(str(shell),'html.parser');url='https://diewarheit.de/'+a['slug'];p.title.string=a['title']+' | Satire | Die Warheit'
 for name,value in [('description',a['deck']+' Satire zum aktuellen Nachrichtenanlass.'),('robots','noindex,nofollow' if a['status']=='draft' else 'index,follow,max-image-preview:large')]:
  m=p.find('meta',attrs={'name':name})
  if not m:m=p.new_tag('meta');m['name']=name;p.head.append(m)
  m['content']=value
 p.find('link',rel='canonical')['href']=url
 if a['datePublished']:
  dt=datetime.datetime.fromisoformat(a['datePublished']);p.select_one('.meta span').string=f'Ausgabe Nr. 2 · {dt.day}.{dt.month:02}.{dt.year}'
 for prop,value in [('og:title',a['title']+' (Satire)'),('og:description',a['deck']+' Satire.'),('og:url',url),('og:image','https://diewarheit.de/'+a['image']),('og:type','article')]:
  m=p.find('meta',attrs={'property':prop})
  if not m:m=p.new_tag('meta');m['property']=prop;p.head.append(m)
  m['content']=value
 for m in p.find_all('script',type='application/ld+json'):m.decompose()
 schema={'@context':'https://schema.org','@type':'NewsArticle','headline':a['title'],'description':a['deck']+' Satire.','genre':'Satire','articleSection':a['section'],'inLanguage':'de-DE','mainEntityOfPage':url,'image':['https://diewarheit.de/'+a['image']],'author':{'@type':'Organization','name':'Redaktion Die Warheit','url':'https://diewarheit.de/ueber'},'publisher':{'@type':'Organization','name':'Die Warheit','url':'https://diewarheit.de'},'isAccessibleForFree':True,'citation':a['source']['url'],'articleBody':' '.join(a['paragraphs'])}
 if a['datePublished']:schema.update(datePublished=a['datePublished'],dateModified=a['dateModified'] or a['datePublished'])
 sc=p.new_tag('script',type='application/ld+json');sc.string=json.dumps(schema,ensure_ascii=False).replace('</','<\/');p.head.append(sc)
 for key,value in [('twitter:image','https://diewarheit.de/'+a['image']),('twitter:title',a['title']+' (Satire)'),('twitter:description',a['deck']+' Satire.')]:
  m=p.find('meta',attrs={'name':key})
  if not m:m=p.new_tag('meta');m['name']=key;p.head.append(m)
  m['content']=value
 stamp='Entwurf · noch nicht veröffentlicht' if not a['datePublished'] else datetime.datetime.fromisoformat(a['datePublished']).strftime('%d.%m.%Y')
 source=a['source'];main=f'<main id="main"><article class="art"><div class="kick">{h(a["section"])} · Satire</div><h1>{h(a["title"])}</h1><p class="deck">{h(a["deck"])}</p><div class="byl">Von der Redaktion Die Warheit · {stamp}</div><div class="notice">{notice}</div><figure class="news-image"><img src="/{a["image"]}" width="1536" height="864" alt="KI-Illustration zum Thema: {h(a["title"])}"><figcaption>KI-generierte redaktionelle Illustration. Kein tatsächliches Ereignis.</figcaption></figure><div class="body">'+''.join('<p>'+h(x)+'</p>' for x in a['paragraphs'])+f'</div><aside class="source-box"><h2>Der echte Nachrichtenanlass</h2><p>{h(source["fact"])}</p><a href="{h(source["url"])}">{h(source["title"])}</a><p>Quelle geprüft am 1. Oktober 2026. Die Satire darüber ist erfunden.</p></aside><p><a href="/">Zur Titelseite</a></p></article></main>'
 p.find('main').replace_with(BeautifulSoup(main,'html.parser'));(OUT/(a['slug']+'.html')).write_text(str(p))
# New issue from central data. Original front-page extras remain in their archive section.
p=BeautifulSoup((BASE/'index.html').read_text(),'html.parser')
# Masthead reflects latest actual publication, not the rebuild clock.
latest=max((a['datePublished'] for a in published),default=None)
if latest:
 dt=datetime.datetime.fromisoformat(latest);months=['','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];p.select_one('.meta span').string=f'Ausgabe Nr. 2 · {dt.day}. {months[dt.month]} {dt.year}'
def card(a,lead=False):
 return f'<article class="news-card"><div class="kick">{h(a["section"])} · Satire</div><a href="/{a["slug"]}"><img src="/{a["image"]}" alt="KI-Illustration" width="1536" height="864" loading="{ "eager" if lead else "lazy"}"><h{2 if lead else 3}>{h(a["title"])}</h{2 if lead else 3}></a><p>{h(a["deck"])}</p><small>KI-Illustration · '+('Entwurf' if a['status']=='draft' else h(a['datePublished'][:10]))+'</small></article>'
sections=list(dict.fromkeys(a['section'] for a in data))
new='<section class="new-issue wrap"><div class="issue-label">Neue Ausgabe · '+('Private Vorschau, nicht veröffentlicht' if draft else 'Satire mit echtem Nachrichtenanlass')+'</div><div class="issue-lead">'+card(data[0],True)+'<div>'+card(data[7])+card(data[10])+'</div></div><nav class="issue-nav" aria-label="Neue Rubriken">'+''.join(f'<a href="#rubrik-{i}">{h(s)}</a>' for i,s in enumerate(sections))+'</nav>'
for i,s in enumerate(sections):new+=f'<section id="rubrik-{i}"><h2 class="section-title">{h(s)}</h2><div class="news-grid">'+''.join(card(a) for a in data if a['section']==s)+'</div></section>'
new+='</section><div class="wrap"><h2 class="section-title">Aus dem Archiv und weitere Rubriken</h2></div>'
p.main.insert(0,BeautifulSoup(new,'html.parser'));(OUT/'index.html').write_text(str(p))
css='''\n.news-image{margin:30px 0}.news-image img,.news-card img{width:100%;height:auto;display:block;background:#f5f3ec}.news-image figcaption{font:12px/1.5 Arial;color:#666;margin-top:8px}.source-box{background:#f6f6f3;border-top:1px solid #222;padding:22px;margin:35px 0}.source-box h2{font-size:22px}.source-box p{font:15px/1.7 Arial}.issue-label{font:12px Arial;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid #222;padding:20px 0}.issue-lead{display:grid;grid-template-columns:2fr 1fr;gap:30px;padding:25px 0}.issue-lead>div{border-left:1px solid #ddd;padding-left:25px}.news-card h2{font-size:42px;line-height:1.08;margin:15px 0}.news-card h3{font-size:25px;line-height:1.15;margin:12px 0}.news-card p{font:16px/1.55 Georgia;margin:12px 0}.news-card small{font:11px Arial;color:#666}.news-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:25px;margin-bottom:30px}.section-title{border-top:2px solid #222;padding-top:15px;font:26px Georgia}.issue-nav{display:flex;flex-wrap:wrap;gap:18px;border-top:1px solid #aaa;border-bottom:1px solid #aaa;padding:15px 0;margin-bottom:30px}.issue-lead .news-card{margin-bottom:20px}.news-card a{color:inherit;text-decoration:none}.news-card a:hover{text-decoration:underline}.news-card{min-width:0}.new-issue{margin-bottom:40px}@media(max-width:700px){.issue-lead,.news-grid{grid-template-columns:1fr}.issue-lead>div{border:0;padding:0;display:grid;gap:22px}.news-card h2{font-size:32px}.news-grid{gap:30px}.source-box{padding:18px}.issue-nav{gap:15px}.news-card h3{font-size:27px}}\n'''
(OUT/'style.css').write_text((BASE/'style.css').read_text()+css)
# Only actual publications belong in news sitemap. Draft dates are never invented.
now=datetime.datetime.now(datetime.timezone.utc);recent=[]
for a in published:
 t=datetime.datetime.fromisoformat(a['datePublished']);
 if datetime.timedelta(0)<=now-t.astimezone(datetime.timezone.utc)<=datetime.timedelta(days=2):recent.append(a)
news='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
for a in recent:news+=f'<url><loc>https://diewarheit.de/{a["slug"]}</loc><news:news><news:publication><news:name>Die Warheit</news:name><news:language>de</news:language></news:publication><news:publication_date>{a["datePublished"]}</news:publication_date><news:title>{h(a["title"])}</news:title></news:news></url>'
(OUT/'news-sitemap.xml').write_text(news+'</urlset>')
# Append actual publications to existing general sitemap and RSS only on approved publication.
if published:
 sm=(BASE/'sitemap.xml').read_text().replace('</urlset>',''.join(f'<url><loc>https://diewarheit.de/{a["slug"]}</loc><lastmod>{a["dateModified"] or a["datePublished"]}</lastmod></url>' for a in published)+'</urlset>');(OUT/'sitemap.xml').write_text(sm)
 feed=(BASE/'feed.xml').read_text().replace('</channel>',''.join(f'<item><title>{h(a["title"])} (Satire)</title><link>https://diewarheit.de/{a["slug"]}</link><guid>https://diewarheit.de/{a["slug"]}</guid><description>{h(a["deck"])} Satire.</description><pubDate>{email.utils.format_datetime(datetime.datetime.fromisoformat(a["datePublished"]))}</pubDate></item>' for a in published)+'</channel>');(OUT/'feed.xml').write_text(feed)
(OUT/'robots.txt').write_text((BASE/'robots.txt').read_text()+'\nSitemap: https://diewarheit.de/news-sitemap.xml\n')
print('Built',len(data),'articles;',len(recent),'eligible news sitemap entries')
