"""Fair generated SVG silhouettes and splice shared contact curves into closed bodies.

Requires Pillow, NumPy, OpenCV, Shapely. Source PNGs and palette roles stay intact.
"""
from pathlib import Path
import argparse,json,math
import xml.etree.ElementTree as E
import numpy as np
import cv2
from PIL import Image
from shapely import Polygon,LineString,Point,make_valid,union_all
from shapely.ops import substring

S='{http://www.w3.org/2000/svg}';E.register_namespace('',S[1:-1])
p=argparse.ArgumentParser(description=__doc__);p.add_argument('family',type=Path);args=p.parse_args();family=args.family
manifest=json.loads((family/'manifest.json').read_text());icons={e['id']:e for e in manifest};K=8
spec=json.loads((family/'interfaces.json').read_text()) if (family/'interfaces.json').exists() else {'pairs':[]}

def polys(g):
    if g.geom_type=='Polygon':return [g]
    return [p for p in g.geoms if p.geom_type=='Polygon']

def controls(q):
    q=np.asarray(q);q=q[:-1] if np.linalg.norm(q[0]-q[-1])<1e-7 else q
    previous=q-np.roll(q,1,axis=0);following=np.roll(q,-1,axis=0)-q
    h0=np.maximum(np.linalg.norm(previous,axis=1),1e-8);h1=np.maximum(np.linalg.norm(following,axis=1),1e-8)
    tangent=(previous/h0[:,None]*h1[:,None]+following/h1[:,None]*h0[:,None])/(h0+h1)[:,None]
    handle=tangent*np.minimum(h0,h1)[:,None]/3
    return q,np.roll(q,-1,axis=0),q+handle,np.roll(q,-1,axis=0)-np.roll(handle,-1,axis=0)

def dense(q):
    a,b,c,d=controls(q);u=np.linspace(0,1,6,endpoint=False)[None,:,None]
    return ((1-u)**3*a[:,None,:]+3*(1-u)**2*u*c[:,None,:]+3*(1-u)*u*u*d[:,None,:]+u**3*b[:,None,:]).reshape(-1,2)

def maskshape(mask,hole_floor=.12):
    contours,h=cv2.findContours(mask.astype('uint8'),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);out=[]
    for i,c in enumerate(contours):
        if h[0,i,3]!=-1 or abs(cv2.contourArea(c))<K*K*.12:continue
        q=cv2.approxPolyDP(c,1.3,True)[:,0,:]/K
        if len(q)<4:continue
        holes=[];j=h[0,i,2]
        while j!=-1:
            r=cv2.approxPolyDP(contours[j],1.3,True)[:,0,:]/K
            if len(r)>=4 and abs(cv2.contourArea(contours[j]))>K*K*hole_floor:holes.append(dense(r))
            j=h[0,j,0]
        out.extend(polys(make_valid(Polygon(dense(q),holes))))
    merged=union_all(out)
    return union_all([Polygon(p.exterior,[h for h in p.interiors if Polygon(h).area>=hole_floor]) for p in polys(merged)])

bodies={};regions={};scales={};originals={};protected={e["id"]:set() for e in manifest}
for e in manifest:
    for a in e['anchors'].values():
        if 'interface' in a:a['point']=a['interface']['framePoint']
    im=Image.open(family.parent/e['provenance']['source']).convert('RGBA');s=e['source_to_svg']['scale'];tx,ty=e['source_to_svg']['translate']
    im=im.transform((160*K,160*K),Image.Transform.AFFINE,(1/(s*K),0,-tx/s,0,1/(s*K),-ty/s),Image.Resampling.BICUBIC)
    rgba=np.asarray(im);mask=cv2.GaussianBlur(rgba[:,:,3],(0,0),.75)>128
    palette=np.array([[int(v[k:k+2],16) for k in (1,3,5)] for v in e['palette'].values()]);labels=((rgba[:,:,:3,None].astype(float)-palette.T[None,None,:,:])**2).sum(2).argmin(2)
    colored=np.zeros_like(mask)
    for i in range(1,len(palette)):
        role_mask=(mask&(labels==i)).astype('uint8');distance=cv2.distanceTransform(role_mask,cv2.DIST_L2,5);colored|=(role_mask.astype(bool)&(distance>=min(3,float(distance.max())*.5)))
    _,nearest=cv2.distanceTransformWithLabels((~colored).astype('uint8'),cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
    labels=np.r_[0,labels[colored]][nearest]
    g=maskshape(mask,1.0 if e["id"]!="rna-ig" else float("inf"));bodies[e['id']]=g;originals[e['id']]=g
    regions[e['id']]={role:maskshape(mask&(labels==i)) for i,role in enumerate(e['palette']) if i}
    scales[e['id']]=1

# Normal-ray intersections use the fair body, not a pixel staircase.
def samples(side,ts,body=None):
    a=icons[side['icon']]['anchors'][side['port']];o=np.array(a['point']);n=np.array(a['normal']);v=np.array([-n[1],n[0]]);s=side['scale'];g=body if body is not None else originals[side['icon']];out=[]
    for t in ts:
        q=o+t/s*v;cut=g.boundary.intersection(LineString([q+n*30/s,q-n*55/s]))
        if cut.is_empty:raise ValueError(f'Contact window misses body: {side["icon"]} {side["port"]} t={t}')
        pts=[cut] if cut.geom_type in ['Point','LineString'] else list(cut.geoms)
        out.append(max(np.dot(np.array(c.coords[0])-q,n) for c in pts)*s)
    return np.array(out)

for pair in spec['pairs']:
    w=pair.get('extent',pair['halfWidth']*2.5);pair['extent']=w;ts=np.linspace(-w,w,81)
    c=[samples(side,ts) for side in pair['sides'][:2]];z=(c[0]-c[1][::-1])/2 if len(c)>1 else np.zeros_like(ts);z=(z+z[::-1])/2
    z=cv2.GaussianBlur(z[None,:],(0,0),2).ravel()
    if pair.get('profileShape')=='gentle':z[:]=z[40]
    z+=pair['depth']*.8*np.maximum(0,1-(ts/pair['halfWidth'])**2)**2
    pair['profileSamples']={'t':ts.tolist(),'z':z.tolist()}
    for j,side in enumerate(pair['sides']):
        for port in [side['port'],*side.get('duplicatePorts',[])]:
            id=side['icon'];scales[id]=side['scale'];a=icons[id]['anchors'][port];o=np.array(a['point']);n=np.array(a['normal']);v=np.array([-n[1],n[0]]);s=side['scale'];g=bodies[id]
            current={**side,'port':port};old=samples(current,ts,g);u=np.clip((abs(ts)-pair['halfWidth'])/(w-pair['halfWidth']),0,1);u=u*u*(3-2*u)
            desired=z*(1 if j==0 else -1)*(1-u)+old*u;boundary=o+(ts[:,None]*v+desired[:,None]*n)/s
            protected[id].update(tuple(np.round(q,5)) for q in boundary)
            components=polys(g);k=min(range(len(components)),key=lambda k:components[k].distance(Point(o)));part=components[k];edge=LineString(part.exterior.coords);lo,hi=[edge.project(Point(q)) for q in boundary[[0,-1]]]
            def arc(start,end):
                return list(substring(edge,start,end).coords) if start<=end else list(substring(edge,start,edge.length).coords)+list(substring(edge,0,end).coords)[1:]
            forward=arc(lo,hi);back=arc(hi,lo);mid=Point(o+old[40]/s*n)
            rest=back if LineString(forward).distance(mid)<LineString(back).distance(mid) else list(reversed(forward))
            # Replace the exterior arc itself. There is no rectangular patch or seam stroke.
            new=union_all(polys(make_valid(Polygon([*boundary,*rest[1:-1]],part.interiors))));components[k]=new;next_body=union_all(components)
            role=side.get('duplicatePart',side['part']) if port!=side['port'] else side['part'];regions[id][role]=regions[id][role].union(next_body.difference(g));bodies[id]=next_body
            a['interface']={'id':pair['id'],'shape':side['shape'],'halfWidth':pair['halfWidth']/s,'depth':pair['depth']/s,'profile':'continuous-body','framePoint':o.tolist(),'schematic':True}
            a['point']=(o+n*desired[40]/s).tolist()

# Chord-length cubic chains keep tangent directions continuous at joins.
def ringpath(q):
    a,b,c,d=controls(q);out=[f'M{a[0,0]:.5f} {a[0,1]:.5f}']
    for end,c1,c2 in zip(b,c,d):out.append(f'C{c1[0]:.5f} {c1[1]:.5f} {c2[0]:.5f} {c2[1]:.5f} {end[0]:.5f} {end[1]:.5f}')
    return ' '.join(out)+'Z'
def outlinepoints(ring,keep):
    q=np.asarray(ring.coords)[:-1];marks=[i for i,p in enumerate(q) if tuple(np.round(p,5)) in keep]
    if not marks:return np.asarray(LineString(np.vstack([q,q[0]])).simplify(.03).coords)
    out=[]
    for i,start in enumerate(marks):
        end=marks[(i+1)%len(marks)];arc=q[start:end+1] if end>start else np.vstack([q[start:],q[:end+1]])
        out.extend(list(LineString(arc).simplify(.03).coords)[:-1])
    return np.array(out)
def geometrypath(g,keep=None):
    parts=polys(g if keep else g.simplify(.03,preserve_topology=True))
    return ' '.join(ringpath(outlinepoints(p.exterior,keep) if keep else p.exterior.coords)+''.join(ringpath(h.coords) for h in p.interiors) for p in parts if p.area>.08)


report=[]
for e in manifest:
    id=e['id'];g=union_all(polys(bodies[id]));regions[id]={r:union_all(polys(q)) for r,q in regions[id].items()};root=E.Element(S+'svg',viewBox='0 0 160 160',width='160',height='160',role='img');E.SubElement(root,S+'title').text=e['label'];art=E.SubElement(root,S+'g',id=id+'-art');defs=E.SubElement(art,S+'defs');clip=E.SubElement(defs,S+'clipPath',id=id+'-colors-clip',clipPathUnits='userSpaceOnUse');E.SubElement(clip,S+'path',{'d':geometrypath(g,protected[id]),'fill-rule':'evenodd','clip-rule':'evenodd'});fills=E.SubElement(art,S+'g',{'clip-path':'url(#'+id+'-colors-clip)'})
    main=max(regions[id],key=lambda role:regions[id][role].area);color=e['palette'][main]
    base=E.SubElement(fills,S+'g',{'data-part':main,'id':id+'-body-fill'});E.SubElement(base,S+'path',{'d':geometrypath(g,protected[id]),'fill':color,'fill-rule':'evenodd','data-original-fill':color})
    for role,region in regions[id].items():
        shape=region.buffer(.35);color=e['palette'][role];group=E.SubElement(fills,S+'g',{'data-part':role,'id':id+'-'+role})
        E.SubElement(group,S+'path',{'d':geometrypath(shape),'fill':color,'data-original-fill':color,'fill-rule':'evenodd'})
    seen=LineString();seam_group=E.SubElement(fills,S+'g',{'id':id+'-domain-seams'})
    for role,region in regions[id].items():
        if role==main or region.is_empty:continue
        neighbors=union_all([q.boundary for r,q in regions[id].items() if r!=role and not q.is_empty]).buffer(.3)
        seam=region.boundary.intersection(neighbors).intersection(g.buffer(-.05)).difference(seen.buffer(.35));seen=seen.union(seam)
        lines=[seam] if seam.geom_type=='LineString' else [x for x in seam.geoms if x.geom_type=='LineString']
        for line in lines:
            if line.length<1:continue
            q=np.asarray(line.simplify(.04).coords);padded=np.vstack([q[0],q,q[-1]]);d=[f'M{q[0,0]:.5f} {q[0,1]:.5f}']
            for k in range(len(q)-1):
                c1=q[k]+(padded[k+2]-padded[k])/6;c2=q[k+1]-(padded[k+3]-padded[k+1])/6
                d.append(f'C{c1[0]:.5f} {c1[1]:.5f} {c2[0]:.5f} {c2[1]:.5f} {q[k+1,0]:.5f} {q[k+1,1]:.5f}')
            E.SubElement(seam_group,S+'path',{'d':' '.join(d),'fill':'none','stroke':e['palette']['outline'],'stroke-width':'1.1','stroke-linecap':'round','data-line-weight':'1.1'})
    outline=E.SubElement(art,S+'g',{'data-part':'outline','id':id+'-outline'});E.SubElement(outline,S+'path',{'d':geometrypath(g,protected[id]),'fill':'none','stroke':e['palette']['outline'],'stroke-width':'1.6','stroke-linecap':'round','stroke-linejoin':'round','data-line-weight':'1.6'})
    e['contour_refinement']={'method':'closed-cubic-body','outer_line':1.6,'inner_line':1.1,'scale_at_assembly':scales[id],'patches':False,'source_preserved':True}
    E.ElementTree(root).write(family/Path(e['file']).name,encoding='utf-8',xml_declaration=True)
    report.append({'icon':id,'body_components':len(polys(g)),'holes':sum(len(p.interiors) for p in polys(g)),'valid':g.is_valid,'bounds':list(g.bounds)})
(family/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
if spec['pairs']:(family/'interfaces.json').write_text(json.dumps(spec,indent=2)+'\n')
(family/'contour-check.json').write_text(json.dumps({'method':'Complete closed cubic silhouettes; no contact overlays or cutting clips.','icons':report},indent=2)+'\n')
p=family.parent/'catalog.json';catalog=json.loads(p.read_text());catalog['icons']=[icons.get(e['id'],e) for e in catalog['icons']];p.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,indent=2))
