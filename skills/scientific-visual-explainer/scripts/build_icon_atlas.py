"""Bundle the canonical flat SVG family and shared animation demos as offline HTML."""
from pathlib import Path
import json, base64
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
P=Path(__file__).resolve().parent
LIB=P.parent/'assets/biomed-icons'
items=[]
for manifest in sorted(LIB.glob('*/manifest.json')):
    items.extend(json.loads(manifest.read_text()))
(LIB/'catalog.json').write_text(json.dumps({'version':'0.7','style':'STYLE.md','icons':items},ensure_ascii=False,indent=2)+'\n')
for item in items:
    item['svg']=(LIB/item['file']).read_text()
    item['uri']='data:image/svg+xml;base64,'+base64.b64encode(item['svg'].encode()).decode()
model=json.loads((P.parent/'assets/icon-atlas-model.json').read_text())
model['title']='Cargo enters. Its receptor returns.'
model['scope']='Generic selected recycling route, not all receptors. Schematic geometry and timing.'
for e in model['entities']:e['label']='Receptor' if e['kind']=='membrane_receptor' else 'Cargo'
for event in model['events']:
    event['title']=event['title'].replace('LDL','Cargo')
    event['caption']=event['caption'].replace('LDL','cargo').replace('Acidic conditions release cargo into the lumen.','Cargo separates from its receptor in the endosome.')
itemmap={x['id']:x for x in items}
def rig(id,scale):
    x=itemmap[id]
    uri=x['uri']
    if x.get('context_parts'):
        svg=ET.fromstring(x['svg'])
        for parent in svg.iter():
            for child in list(parent):
                if child.get('data-part') in x['context_parts']:parent.remove(child)
        uri='data:image/svg+xml;base64,'+base64.b64encode(ET.tostring(svg)).decode()
    anchors={k:v['point'] for k,v in x['anchors'].items()}
    for name,a in x['anchors'].items():
        if a['kind']=='binding' and 'binding' not in anchors:anchors['binding']=a['point']
    return dict(src=uri,viewBox=[0,0,160,160],contentBounds=[12,12,136,136],scale=scale,anchors=anchors)
rigs={'receptor':rig('single-pass-receptor',1.25),'ligand':rig('ligand',1.25),'lipid':rig('phospholipid',.22)}
rigs['lipid']['head']=itemmap['phospholipid']['anchors']['head']['point']
rigs['lipid']['tailTip']=itemmap['phospholipid']['anchors']['tail']['point']
rigs['lipid']['pitch']=8.1
runtime=(P/'asset-recycling.js').read_text()
data=json.dumps({'icons':items,'model':model,'rigs':rigs},ensure_ascii=False).replace('</',r'<\/')
template=(P.parent/'assets/icon-atlas-template.html').read_text().replace('/*ICON_DATA*/','const DATA='+data+';').replace('/*SHARED_RUNTIME*/',runtime).replace('{{ICON_COUNT}}',str(len(items))).replace('{{ICON_VERSION}}','0.7')
(P.parent/'assets/biomed-icon-library.html').write_text(template)
print(f'Built {len(items)} reusable icons and two demos: assets/biomed-icon-library.html')
