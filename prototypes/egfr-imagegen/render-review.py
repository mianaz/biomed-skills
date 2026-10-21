"""Render SVG timeline states and inspect actual silhouette and annotation bounds."""
from pathlib import Path
import copy,io,json,math,itertools,argparse
import xml.etree.ElementTree as E
import cairosvg
import numpy as np
from PIL import Image,ImageFont
parser=argparse.ArgumentParser();parser.add_argument('--lesson',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args()
P=args.lesson.resolve();L=P.parents[1]/'skills/scientific-visual-explainer/assets/biomed-icons'
S='{http://www.w3.org/2000/svg}';E.register_namespace('',S[1:-1])
model=json.loads((P/'mechanism.json').read_text());entities={e['id']:e for e in model['entities']};W=model['layout']['width'];H=model['layout']['height']
icons={e['id']:e for e in json.loads((L/'catalog.json').read_text())['icons'] if e['id'] in {x['icon'] for x in entities.values()}}
frames=json.loads((P/'qa/layout-frames.json').read_text())
roots={k:E.parse(L/v['file']).getroot() for k,v in icons.items()}
for k,r in roots.items():
 scale=next(e['scale'] for e in entities.values() if e['icon']==k)
 for n in r.iter():
  width=n.get('data-line-weight') or ('1.6' if n.get('stroke')=='#3D5963' else None)
  if width:n.set('stroke-width',str(float(width)/scale))
masks={k:np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=E.tostring(r),output_width=640,output_height=640))).convert('RGBA'))[:,:,3]>128 for k,r in roots.items()}
interiors={}
for k,r in roots.items():
 rgba=np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=E.tostring(r),output_width=640,output_height=640))).convert('RGBA'))
 interiors[k]=(rgba[:,:,3]>200)&(np.linalg.norm(rgba[:,:,:3].astype(float)-[61,89,99],axis=2)>50)
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf';fonts={n:ImageFont.truetype(fontpath,n) for n in [24,26,28]}
localbounds={}
for k,m in masks.items():
 y,x=np.where(m);localbounds[k]=[x.min()/4,y.min()/4,x.max()/4,y.max()/4]
def solid(points,id,f,interior=False):
 if f.get('amounts',{}).get(id,1)<.05:return np.zeros(len(points),dtype=bool)
 p=f['poses'][id];d=points-np.array(p['c']);c,s=math.cos(p['a']),math.sin(p['a'])
 local=np.c_[(c*d[:,0]+s*d[:,1])/p['s']+80,(-s*d[:,0]+c*d[:,1])/(p['s']*p['fy'])+80]
 q=np.rint(local*4).astype(int);valid=(q>=0).all(axis=1)&(q<640).all(axis=1)
 result=np.zeros(len(q),dtype=bool);q=q[valid];result[valid]=(interiors if interior else masks)[entities[id]['icon']][q[:,1],q[:,0]];return result

def box(n):
 a,b,c,d=fonts[n['size']].getbbox(n['text'],anchor='ls');w=fonts[n['size']].getlength(n['text']);x=n['x']-(w/2 if n['anchor']=='middle' else w if n['anchor']=='end' else 0)
 return [x+a,n['y']+b,x+c,n['y']+d]
def mesh(b,step=2):
 x,y=np.meshgrid(np.arange(b[0],b[2]+.01,step),np.arange(b[1],b[3]+.01,step));return np.c_[x.ravel(),y.ravel()]
errors=[];overlaps=[]
for f in frames:
 notes=f['notes'];texts=[n for n in notes['texts'] if n.get('opacity',1)>.05]
 bounds=[box(n) for n in texts]
 for n,b in zip(texts,bounds):
  if b[0]<0 or b[1]<0 or b[2]>W or b[3]>H:errors.append([f['condition'],f['t'],'outside',n['id']])
  points=mesh(b)
  for id in entities:
   if solid(points,id,f).sum()>1:errors.append([f['condition'],f['t'],'text/body',n['id'],id])
 for (a,b),(c,d) in itertools.combinations(zip(texts,bounds),2):
  if min(b[2],d[2])-max(b[0],d[0])>1 and min(b[3],d[3])-max(b[1],d[1])>1:errors.append([f['condition'],f['t'],'text/text',a['id'],c['id']])
 for n in notes['badges']:
  points=mesh([n['x']-15,n['y']-15,n['x']+15,n['y']+15]);points=points[np.linalg.norm(points-[n['x'],n['y']],axis=1)<15]
  for id in entities:
   if solid(points,id,f).sum()>1:errors.append([f['condition'],f['t'],'badge/body',n['id'],id])
 for n in notes['badges']+notes['nucleotides']:
  radius=n.get('r',6)
  for text,b in zip(texts,bounds):
   near=np.maximum(b[:2],np.minimum([n['x'],n['y']],b[2:]))
   if np.linalg.norm(near-[n['x'],n['y']])<radius-1:errors.append([f['condition'],f['t'],'glyph/text',n['id'],text['id']])
 for r in f['routes']:
  if not r['d']:continue
  a=np.array(r['start']);b=np.array(r['end']);u=np.array(r['direction']);v=np.array([-u[1],u[0]])
  pts=np.array([a+(b-a)*t+offset*v for t in np.linspace(0,1,101) for offset in [-1.25,0,1.25]])
  tri=np.array([b,b-12*u+6*v,b-12*u-6*v]);head=np.array([tri[0]*i/10+tri[1]*j/10+tri[2]*(10-i-j)/10 for i in range(11) for j in range(11-i)])
  pts=np.vstack([pts,head])
  for id in entities:
   if solid(pts,id,f).any():errors.append([f['condition'],f['t'],'arrow/body',r['id'],id])
  for n in notes['badges']:
   if (np.linalg.norm(pts-[n['x'],n['y']],axis=1)<n['r']-1).any():errors.append([f['condition'],f['t'],'arrow/badge',r['id'],n['id']])
  for n,bb in zip(texts,bounds):
   if ((pts[:,0]>bb[0])&(pts[:,0]<bb[2])&(pts[:,1]>bb[1])&(pts[:,1]<bb[3])).any():errors.append([f['condition'],f['t'],'arrow/text',r['id'],n['id']])
 # Measure filled-body penetration separately from shared outline seams.
 for a,b in itertools.combinations(entities,2):
  def worldbounds(id):
   p=f['poses'][id];x0,y0,x1,y1=localbounds[entities[id]['icon']];pts=np.array([[x0,y0],[x0,y1],[x1,y0],[x1,y1]])-80;pts*=p['s'];pts[:,1]*=p['fy'];c,s=math.cos(p['a']),math.sin(p['a']);pts=pts@np.array([[c,s],[-s,c]])+p['c'];return [*pts.min(axis=0),*pts.max(axis=0)]
  ba,bb=worldbounds(a),worldbounds(b);over=[max(ba[0],bb[0]),max(ba[1],bb[1]),min(ba[2],bb[2]),min(ba[3],bb[3])]
  if over[0]>=over[2] or over[1]>=over[3]:continue
  pts=mesh(over);area=int((solid(pts,a,f,True)&solid(pts,b,f,True)).sum())*4
  if area>24:overlaps.append([f['condition'],f['t'],a,b,area])
report={'samples':len(frames),'annotationOrArrowCollisions':errors,'actorFillOverlapAbove24sqUnits':overlaps,'inspection':'Local SVG render and actual silhouette masks; no live browser interaction.'}
(P/'qa/layout-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'samples':len(frames),'collisions':len(errors),'types':list({tuple(e[2:]) for e in errors}),'actorOverlaps':overlaps[:25]},indent=2))

html=(P/'preview-template.html').read_text();snippet=html[html.index('<svg id="figure"'):];base=E.fromstring(snippet[:snippet.index('</svg>')+6])
def find(root,id):return next(n for n in root.iter() if n.get('id')==id)
def addtext(parent,n):
 E.SubElement(parent,S+'text',{'x':str(n['x']),'y':str(n['y']),'text-anchor':n['anchor'],'font-size':str(n['size']),'fill':n.get('color','#304F59'),'data-note':n['id'],'opacity':str(n.get('opacity',1))}).text=n['text']
review=[]
for f in frames:
 if model.get('reviewTimes'):
  if f['t'] not in model['reviewTimes'].get(f['condition'],[]):continue
 else:
  if f['condition']=='normal' and f['t'] not in [0,2,4,7,9,11,14,17,19,21,23,26,28,30,32,33,35,36,38,39,40,42]:continue
  if f['condition']=='blocked' and f['t']!=9:continue
 root=copy.deepcopy(base);root.set('width','190mm');root.set('height',str(190*H/W)+'mm')
 actors=find(root,'actors')
 for id,e in entities.items():
  p=f['poses'][id];g=E.SubElement(actors,S+'g',{'data-entity':id,'opacity':str(f.get('amounts',{}).get(id,1)),'transform':f'translate({p["c"][0]} {p["c"][1]}) rotate({p["a"]*180/math.pi}) scale({p["s"]} {p["s"]*p["fy"]}) translate(-80 -80)'})
  for child in roots[e['icon']]:
   if child.tag!=S+'g':continue
   child=copy.deepcopy(child)
   for n in child.iter():
    for k,v in list(n.attrib.items()):
     if k=='id':n.set(k,id+'-'+v)
     elif 'url(#' in v:n.set(k,v.replace('url(#','url(#'+id+'-'))
   g.append(child)
 for r in f['routes']:
  n=find(root,r['id']);n.set('d',r['d']);n.set('opacity',str(r['opacity']))
 for n in f['notes']['texts']:addtext(find(root,'labels'),n)
 states=find(root,'states')
 for l in f['notes']['lines']:E.SubElement(states,S+'path',{'d':f'M{l["a"][0]} {l["a"][1]} L{l["b"][0]} {l["b"][1]}','stroke':'#B78D78','stroke-width':'1.4','fill':'none'})
 for n in f['notes']['badges']:
  g=E.SubElement(states,S+'g',{'data-phosphorylation':n['id']});E.SubElement(g,S+'circle',{'cx':str(n['x']),'cy':str(n['y']),'r':'15','fill':'#FBEBC4','stroke':'#B69A5B','stroke-width':'1.5'});addtext(g,dict(id=n['id'],text='P',x=n['x'],y=n['y']+8,size=24,anchor='middle',color='#85662E'))
 g=find(root,'exchange-glyphs');g.clear();g.set('id','exchange-glyphs')
 for n in f['notes']['nucleotides']:
  child=E.SubElement(g,S+'g',{'opacity':str(n['opacity'])});E.SubElement(child,S+'circle',{'cx':str(n['x']),'cy':str(n['y']),'r':'6','fill':n['color']})
 if f['condition']=='blocked':find(root,'blocked-mark').attrib.pop('style',None)
 else:root.remove(find(root,'blocked-mark'))
 name=f'{f["condition"]}-{f["t"]:g}';file=P/'qa'/f'review-{name}.svg';E.ElementTree(root).write(file,encoding='utf-8',xml_declaration=True)
 cairosvg.svg2png(bytestring=E.tostring(root),write_to=str(file.with_suffix('.png')),output_width=W,output_height=H)
 review.append((name,file.with_suffix('.png').name))
 if f['condition']=='normal' and f['t']==max(x['t'] for x in frames if x['condition']=='normal'):
  for folder,name in [(P/'output',model.get('outputName','egf-egfr-ras-erk')),(P/'qa',model.get('outputName','egfr')+'-static')]:
   E.ElementTree(root).write(folder/(name+'.svg'),encoding='utf-8',xml_declaration=True)
   cairosvg.svg2png(bytestring=E.tostring(root),write_to=str(folder/(name+'.png')),output_width=W,output_height=H)
   cairosvg.svg2pdf(bytestring=E.tostring(root),write_to=str(folder/(name+'.pdf')))
(P/'qa/animation-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Mechanism animation review</title><style>body{font:16px Arial;background:#f3f5f3;margin:24px}main{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}article{background:white;padding:16px;border-radius:12px}img{width:100%}h2{font-size:18px}</style><h1>Mechanism · complete animation review</h1><p>Normal pathway and mechanism controls. P circles indicate phosphorylation.</p><main>'+''.join(f'<article><h2>{name}</h2><img src="{file}"></article>' for name,file in review)+'</main>')
