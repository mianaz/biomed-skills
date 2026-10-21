from pathlib import Path
import json,xml.etree.ElementTree as E,re,subprocess,sys
f=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(f.parents[2]/'scripts/fit_interfaces.py'),str(f)],check=True)
S='{http://www.w3.org/2000/svg}';E.register_namespace('',S[1:-1]);manifest=json.loads((f/'manifest.json').read_text());seams=json.loads((f/'domain-seams.json').read_text())
for e in manifest:
 id=e['id'];p=f/(id+'.svg');root=E.parse(p).getroot();art=root.find(S+'g');group=E.Element(S+'g',{'id':id+'-structural-seams','data-part':'structural-seams','fill':'none','stroke':'#3D5963','stroke-width':str(1.1/e['contour_refinement']['scale_at_assembly']),'stroke-linecap':'round','clip-path':'url(#'+id+'-colors-clip)'})
 if id=='akt1-ig':
  tail=root.find('.//'+S+'g[@id="akt1-ig-regulatory-tail"]/'+S+'path');pieces=['M'+d for d in tail.get('d').split('M')[1:]]
  neck=[d for d in pieces if max(list(map(float,re.findall(r'-?\d+(?:\.\d+)?',d)))[1::2])<90]
  tail.set('d',' '.join(d for d in pieces if d not in neck));g=E.SubElement(art.find('.//'+S+'g[@id="akt1-ig-kinase"]'),S+'path',{'d':' '.join(neck),'fill':e['palette']['kinase']})
 s=e['source_to_svg']['scale'];tx,ty=e['source_to_svg']['translate'];inner=E.SubElement(group,S+'g',{'transform':f'translate({tx} {ty}) scale({s*1254/1280})','stroke-width':str(1.1/(s*1254/1280*e['contour_refinement']['scale_at_assembly']))})
 for d in seams.get(id,[]):E.SubElement(inner,S+'path',{'d':d})
 art.insert(len(art)-1,group);E.ElementTree(root).write(p,encoding='unicode',xml_declaration=True)
 e['parts']=[k for k in e['palette'] if k!='outline']+['structural-seams','outline'];e['parts_note']='Semantic fill regions plus curated domain seams and one continuous body outline. They support recoloring; independently moving domains requires rigging the shared contour.'
 e['scope']='Domain-level educational schematic; contacts and residue anchors are illustrative, not atomic positions.'+(' One mTOR module; a complete mTORC1 dimer is not represented.' if id=='mtor-ig' else '')
(f/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
c=f.parent/'catalog.json';cat=json.loads(c.read_text());by={e['id']:e for e in manifest};cat['icons']=[by.get(e['id'],e) for e in cat['icons']];c.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
