"""Compose the source-linked EGFR lesson from registered generated icons."""
from pathlib import Path
import json,math,base64,shutil
import xml.etree.ElementTree as ET
ET.register_namespace('','http://www.w3.org/2000/svg')
P=Path(__file__).resolve().parent
L=P.parents[1]/'skills/scientific-visual-explainer/assets/biomed-icons'
icons=json.loads((L/'egfr-imagegen/manifest.json').read_text())
for icon in icons:
    root=ET.parse(L/icon['file']).getroot()
    icon['body']=''.join(ET.tostring(c,encoding='unicode') for c in root if c.tag.endswith('g'))
    icon['original_uri']='data:image/png;base64,'+base64.b64encode((L/icon['provenance']['source']).read_bytes()).decode()
    icon['svg_uri']='data:image/svg+xml;base64,'+base64.b64encode((L/icon['file']).read_bytes()).decode()
byid={i['id']:i for i in icons}
def point(id,name):return byid[id]['anchors'][name]['point']
def contact(id,name,c,s):
    q=point(id,name);return[c[i]+(q[i]-80)*s for i in (0,1)]
def dock_center(id,name,target,s):
    q=point(id,name);return[target[i]-(q[i]-80)*s for i in (0,1)]
membrane=300;sr=2.8;sg=.85;sk=1.05;sf=1.15
receptor=[260,membrane-(point('egfr-ig','membrane')[1]-80)*sr]
tail=contact('egfr-ig','pY-tail',receptor,sr)
grb=dock_center('grb2-ig','SH2',tail,sg)
grb_sh3=contact('grb2-ig','SH3-right',grb,sg)
ras_y=membrane+12-(point('ras-ig','membrane')[1]-80)*sk
ras_port_y=ras_y+(point('ras-ig','SOS-contact')[1]-80)*sk
ss=(grb_sh3[1]-ras_port_y)/(point('sos1-ig','GRB2-contact')[1]-point('sos1-ig','RAS-exchange')[1])
sos=dock_center('sos1-ig','GRB2-contact',grb_sh3,ss)
sos_contact=contact('sos1-ig','RAS-exchange',sos,ss)
ras=dock_center('ras-ig','SOS-contact',sos_contact,sk)
raf=dock_center('raf-ig','RAS-binding',contact('ras-ig','RAF-contact',ras,sk),sf)
def entity(id,icon,label,x,y,scale,**extra):return dict(id=id,icon=icon,label=label,slot=x/100-1,zone='cytosol',row=0,scale=scale,**extra)
# Dedicated zones keep these explicit author positions independent of entity names.
entities=[
 entity('r1','egfr-ig','EGFR',260,0,sr,surfaceAnchor='membrane'),
 entity('r2','egfr-ig','EGFR',430,0,sr,surfaceAnchor='membrane',flipY=True,angle=math.pi),
 entity('l1','egf-ig','EGF',150,0,.6),entity('l2','egf-ig','EGF',620,0,.6),
 entity('grb','grb2-ig','GRB2',790,0,sg),
 entity('sos','sos1-ig','SOS1',850,0,ss),entity('ras','ras-ig','RAS',ras[0],0,sk,surfaceAnchor='membrane'),
 entity('raf','raf-ig','RAF1',1030,0,sf),entity('mek','mek-ig','MEK1/2',735,0,1.05),entity('erk','erk-ig','ERK1/2',925,0,1.05)]
zones={'surface':membrane,'ligand':90,'adaptor':520,'ras':ras[1],'raf':570,'mek':720,'erk':915}
for e in entities:
    e['zone']='surface' if e['id'] in ['r1','r2'] else 'ligand' if e['id'] in ['l1','l2'] else 'adaptor' if e['id'] in ['grb','sos'] else e['id']
events=[
 dict(id='bind-a',kind='dock',actor='l1',port='receptor-contact',target='r1',targetPort='EGF-binding',approach=[[135,154]],duration=4,title='EGF 结合',caption='每个 EGF 与一个 EGFR 的胞外区域结合；两个配体位于受体对的外侧。',source='ogiso'),
 dict(id='bind-b',kind='dock',actor='l2',port='receptor-contact',target='r2',targetPort='EGF-binding',approach=[[550,154]],duration=4,title='第二个 EGF 结合',caption='展示配体结合的 2:2 EGF–EGFR 状态。',source='ogiso',silent=True),
 dict(id='dimer',kind='dock',actor='r2',port='dimer-arm',target='r1',targetPort='dimer-arm',after=['bind-a','bind-b'],duration=5,title='EGFR 二聚',caption='胞外 domain II 的二聚化臂使两个受体形成接触。胞内激活依赖非对称激酶二聚体。',source='zhang'),
 dict(id='phospho-a',kind='state',actor='r1',target='r1',state='pY',after=['dimer'],duration=2,title='尾部磷酸化',caption='激酶激活与尾部酪氨酸磷酸化建立胞内衔接蛋白的结合位点。',source='zhang'),
 dict(id='phospho-b',kind='state',actor='r2',target='r2',state='pY',after=['dimer'],duration=2,title='尾部磷酸化',caption='用代表性 pY 标记表示受体尾部的磷酸化状态。',source='zhang',silent=True),
 dict(id='recruit',kind='dock',actor='grb',port='SH2',target='r1',targetPort='pY-tail',after=['phospho-a'],approach=[[290,600]],duration=6,title='募集 GRB2–SOS1',caption='GRB2 的 SH2 接触受体 pY；SH3 携带的 SOS1 随复合物一起到达膜附近。',source='grb2'),
 dict(id='exchange',kind='reaction',actor='ras',port='SOS-contact',target='sos',targetPort='RAS-exchange',stateTarget='ras',state='GTP',after=['recruit'],duration=6,title='RAS 核苷酸交换',caption='SOS1 促进 GDP 释放并允许 GTP 结合，增加活性 RAS–GTP。GDP 并未被磷酸化成 GTP。',source='sos'),
 dict(id='raf-recruit',kind='dock',actor='raf',port='RAS-binding',target='ras',targetPort='RAF-contact',after=['exchange'],duration=5,title='募集 RAF1',caption='RAS–GTP 与 RAF1 的调控区域结合，使 RAF1 到达膜上。',source='rasraf'),
 dict(id='raf-active',kind='state',actor='raf',target='raf',state='active',after=['raf-recruit'],duration=2,title='RAF 激活',caption='膜上的 RAF 激活步骤在这里合并表示；RAF 二聚调控及相关辅因子未逐一展开。',source='rafreg'),
 dict(id='mek-p',kind='reaction',actor='mek',port='RAF-substrate',target='raf',targetPort='MEK-substrate',stateTarget='mek',state='pS/pS',after=['raf-active'],duration=6,title='RAF → MEK',caption='活性 RAF 磷酸化并激活 MEK；短暂接触结束后，MEK 保留活化状态。',source='rafmek'),
 dict(id='erk-p',kind='reaction',actor='erk',port='MEK-substrate',target='mek',targetPort='ERK-substrate',stateTarget='erk',state='pT/pY',after=['mek-p'],duration=6,title='MEK → ERK',caption='MEK 在 ERK 激活环的 Thr 与 Tyr 上磷酸化，完成这条主干级联。',source='mekerK')]
model=dict(title='EGF–EGFR–RAS–RAF–MEK–ERK core cascade',
 layout=dict(width=1180,height=1090,pitch=100,membraneY=membrane,zones=zones),entities=entities,events=events,
 initialLinks={'sos':dict(port='GRB2-contact',target='grb',targetPort='SH3-right')},initialStates={'ras':'GDP'},
 scope='Evidence-linked canonical core. Teaching order, proportions and timing; selected regulation steps are collapsed.',
 surfaceEntities=['r1','r2','ras'],expectedSOSScale=ss,
 calibratedFinal={'receptor':receptor,'GRB2':grb,'SOS1':sos,'RAS':ras,'RAF1':raf})
(P/'mechanism.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
engine=(P.parent/'biomedical-manim/domain-motion.js').read_text()
refs=json.loads((P/'references.json').read_text())
data=json.dumps(dict(model=model,icons=icons,references=refs),ensure_ascii=False).replace('</','<\\/')
html=(P/'preview-template.html').read_text().replace('/*ENGINE*/',engine).replace('/*DATA*/','const DATA='+data+';').replace('/*ARROWS*/',(L.parents[1]/'scripts/mechanism-arrows.js').read_text()).replace('/*ICON_STYLE*/',(L.parents[1]/'scripts/mechanism-icons.js').read_text()).replace('/*ANNOTATIONS*/',(L.parents[1]/'scripts/mechanism-annotations.js').read_text())
(P/'preview.html').write_text(html)
(L.parent/'egfr-generated.html').write_text(html)
(P.parent/'biomedical-manim/output/egfr-generated.html').write_text(html)
shutil.copy2(P/'mechanism.json',L/'egfr-imagegen/mechanism-example.json')
print(json.dumps({'icons':len(icons),'entities':len(entities),'SOS_scale':ss,'calibrated_RAS':ras,'calibrated_RAF':raf},indent=2))
