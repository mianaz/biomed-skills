"""Measure the rendered SVG curves, not only the shared-interface metadata."""
from pathlib import Path
import json,re,math,io
import xml.etree.ElementTree as E
import numpy as np,cv2,cairosvg
from PIL import Image
from shapely import LineString,Point
from shapely.affinity import affine_transform
P=Path(__file__).resolve().parent;L=P.parents[1]/'skills/scientific-visual-explainer/assets/biomed-icons';S='{http://www.w3.org/2000/svg}'
icons={e['id']:e for e in json.loads((L/'catalog.json').read_text())['icons']};curves={};qa=[]
for e in icons.values():
 if not e.get('contour_refinement'):continue
 root=E.parse(L/e['file']).getroot();group=next(g for g in root.iter() if g.get('id')==e['id']+'-outline');path=next(group.iter(S+'path'));tokens=re.findall(r'[MCZ]|[-+]?\d*\.?\d+(?:e[-+]?\d+)?',path.get('d'));rings=[];ring=[];i=0;angle=0;segments=[]
 while i<len(tokens):
  op=tokens[i];i+=1
  if op=='M':p=np.array(list(map(float,tokens[i:i+2])));i+=2;ring=[p];segments=[]
  elif op=='C':
   c1,c2,end=np.array(list(map(float,tokens[i:i+6]))).reshape(3,2);i+=6;segments.append([p,c1,c2,end]);u=np.linspace(0,1,10)[:,None];ring.extend((1-u)**3*p+3*(1-u)**2*u*c1+3*(1-u)*u*u*c2+u**3*end);p=end
  else:
   rings.append(LineString(ring))
   for a,b in zip(segments,segments[1:]+segments[:1]):
    v=a[3]-a[2];w=b[1]-b[0]
    if np.linalg.norm(v)*np.linalg.norm(w)>1e-8:angle=max(angle,math.degrees(math.acos(np.clip(np.dot(v,w)/(np.linalg.norm(v)*np.linalg.norm(w)),-1,1))))
 curves[e['id']]=rings
 im=np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=E.tostring(root),output_width=640,output_height=640))).convert('RGBA'));mask=(im[:,:,3]>128).astype('uint8');n,labels,stats,centers=cv2.connectedComponentsWithStats(mask);components=sum(stats[1:,4]>16)
 qa.append({'icon':e['id'],'closedRings':len(rings),'maxJoinAngleDegrees':angle,'renderedBodyComponentsAbove1SquareUnit':int(components),'outerWeights':sorted({float(n.get('data-line-weight')) for n in group.iter() if n.get('data-line-weight')})})

matches=[]
for name in ['tgfb-imagegen','egfr-imagegen']:
 folder=P.parent/name;model=json.loads((folder/'mechanism.json').read_text());entities={e['id']:e for e in model['entities']};frames=json.loads((folder/'qa/layout-frames.json').read_text());pairs={q['id']:q for q in json.loads((L/name/'interfaces.json').read_text())['pairs']};seen=set()
 for f in frames:
  for c in [*f['contacts'],*({'actor':actor,**e} for actor,e in f['links'].items())]:
   key=tuple(c.get(k) for k in ['actor','port','target','targetPort'])
   if key in seen:continue
   src,port,dst,target_port=key;a=icons[entities[src]['icon']]['anchors'][port];b=icons[entities[dst]['icon']]['anchors'][target_port]
   if not a.get('interface') or a['interface']['id']!=b.get('interface',{}).get('id'):continue
   seen.add(key);s=f['poses'][src];d=f['poses'][dst]
   def world(q,p):
    c,z=math.cos(p['a']),math.sin(p['a']);ss=p['s'];fy=p['fy'];A=[c*ss,-z*ss*fy,z*ss,c*ss*fy];return affine_transform(q,[*A,p['c'][0]-80*(A[0]+A[1]),p['c'][1]-80*(A[2]+A[3])])
   src_lines=[world(q,s) for q in curves[entities[src]['icon']]];dst_lines=[world(q,d) for q in curves[entities[dst]['icon']]]
   c0,z0=math.cos(s['a']),math.sin(s['a']);n=np.array([c0*a['normal'][0]-z0*a['normal'][1]*s['fy'],z0*a['normal'][0]+c0*a['normal'][1]*s['fy']]);v=np.array([-n[1],n[0]]);o=np.array(world(Point(a['point']),s).coords[0]);half=pairs[a['interface']['id']]['halfWidth'];gaps=[]
   for t in np.linspace(-half,half,31):
    q=o+t*v;ray=LineString([q-n*25,q+n*25]);zs=[]
    for lines in [src_lines,dst_lines]:
     pts=[]
     for line in lines:
      cut=line.intersection(ray)
      if cut.is_empty:continue
      points=[cut] if cut.geom_type=='Point' else list(cut.geoms)
      pts.extend(np.dot(np.array(point.coords[0])-q,n) for point in points)
     if not pts:raise ValueError((key,t,'no outline intersection'))
     zs.append(min(pts,key=abs))
    gaps.append(abs(zs[0]-zs[1]))
   matches.append({'lesson':name,'contact':key,'maxActualOutlineGap':max(gaps)})
report={'icons':qa,'contacts':matches,'scope':'Actual SVG cubic outlines and rendered connectivity; schematic geometry.'};(P/'qa/contour-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'icons':len(qa),'maxJoinAngleDegrees':max(x['maxJoinAngleDegrees'] for x in qa),'nonSingleBodies':[x['icon'] for x in qa if x['renderedBodyComponentsAbove1SquareUnit']!=1],'worstActualOutlineGap':max(x['maxActualOutlineGap'] for x in matches),'contacts':matches},indent=2))
assert all(x['renderedBodyComponentsAbove1SquareUnit']==1 for x in qa)
assert max(x['maxJoinAngleDegrees'] for x in qa)<.15
assert max(x['maxActualOutlineGap'] for x in matches)<.6
