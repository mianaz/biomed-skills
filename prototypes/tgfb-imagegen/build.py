"""Build the generated TGFbeta–SMAD3 nuclear lesson with the shared motion engine."""
from pathlib import Path
import json,math,base64,shutil
import xml.etree.ElementTree as E
E.register_namespace('','http://www.w3.org/2000/svg')
P=Path(__file__).resolve().parent;S=P.parents[1]/'skills/scientific-visual-explainer';L=S/'assets/biomed-icons';F=L/'tgfb-imagegen'
icons=json.loads((F/'manifest.json').read_text())
icons.extend(e for e in json.loads((L/'catalog.json').read_text())['icons'] if e['id'] in ['dna-ig','rna-ig','nuclear-pore-cutaway'])
for icon in icons:
 root=E.parse(L/icon['file']).getroot();icon['body']=''.join(E.tostring(g,encoding='unicode') for g in root if g.tag.endswith('g'))
 if icon.get('provenance',{}).get('mode')=='built-in-imagegen-traced':icon['original_uri']='data:image/png;base64,'+base64.b64encode((L/icon['provenance']['source']).read_bytes()).decode()
byid={i['id']:i for i in icons}
def a(i,n):return byid[i]['anchors'][n]['point']
def framepoint(i,n):return byid[i]['anchors'][n].get('interface',{}).get('framePoint',a(i,n))
sr=2.4;sl=3.3
IIy=330-(framepoint('tgfbr2-ig','membrane')[1]-framepoint('tgfbr2-ig','ligand')[1])*sr
Iy=IIy+(framepoint('tgfb1-ig','I-left')[1]-framepoint('tgfb1-ig','II-left')[1])*sl
si=(330-Iy)/(framepoint('tgfbr1-ig','membrane')[1]-framepoint('tgfbr1-ig','ligand')[1])
ligand_center=[240-(a('tgfb1-ig','II-left')[0]-80)*sl,330-(a('tgfbr2-ig','membrane')[1]-a('tgfbr2-ig','ligand')[1])*sr-(a('tgfb1-ig','II-left')[1]-80)*sl]
def contact(i,port,c,scale,mirror=False):
 q=a(i,port);return [c[0]+(q[0]-80)*scale*(-1 if mirror else 1),c[1]+(q[1]-80)*scale]
xII=ligand_center[0]+(a('tgfb1-ig','II-right')[0]-80)*sl
xIa=ligand_center[0]+(a('tgfb1-ig','I-left')[0]-80)*sl;xIb=ligand_center[0]+(a('tgfb1-ig','I-right')[0]-80)*sl
cyI=330-(a('tgfbr1-ig','membrane')[1]-80)*si
suba=contact('tgfbr1-ig','SMAD-substrate',[xIa,cyI],si);subb=contact('tgfbr1-ig','SMAD-substrate',[xIb,cyI],si,True)
q=a('smad3-ig','co-SMAD-left');desta=[suba[0]-(q[0]-80)*.65,suba[1]-(q[1]-80)*.65];destb=[subb[0]+(q[0]-80)*.65,subb[1]-(q[1]-80)*.65]
def ent(id,icon,label,x,y,scale,role,mirror=False,**extra):return dict(id=id,icon=icon,label=label,slot=x/100-1,zone=id,row=0,scale=scale,role=role,**(dict(angle=math.pi,flipY=True) if mirror else {}),**extra)
entities=[ent('r2a','tgfbr2-ig','TGFβRII',240,330,sr,'receptor',surfaceAnchor='membrane'),ent('r2b','tgfbr2-ig','TGFβRII',xII+130,330,sr,'receptor',True,surfaceAnchor='membrane'),ent('ligand','tgfb1-ig','TGFβ1 dimer',450,110,sl,'ligand'),ent('r1a','tgfbr1-ig','TGFβRI',xIa-35,330,si,'receptor',surfaceAnchor='membrane'),ent('r1b','tgfbr1-ig','TGFβRI',xIb+35,330,si,'receptor',True,surfaceAnchor='membrane'),ent('sa','smad3-ig','SMAD3',840,680,.65,'r-smad'),ent('sb','smad3-ig','SMAD3',1040,680,.65,'r-smad',True),ent('s4','smad4-ig','SMAD4',600,850,.65,'co-smad'),ent('npc','nuclear-pore-cutaway','Nuclear pore',600,1140,5,'pore'),ent('dna','dna-ig','Response element',685,1590,1.5,'dna'),ent('rna','rna-ig','Target-gene RNA',1000,1735,1.1,'rna',hidden=True)]
for e in entities:
 if e.get('surfaceAnchor'):e['zone']='surface'
zones={e['id']:y for e,y in zip(entities,[330,330,110,330,330,680,680,850,1140,1590,1735])};zones.update(surface=330,arrival=1400)
def ev(id,kind,actor,target,duration,title,caption,source,after=[],**extra):return dict(id=id,kind=kind,actor=actor,target=target,duration=duration,title=title,caption=caption,source=source,after=after,**extra)
events=[
 ev('ligand-bind','dock','ligand','r2a',4,'TGFβ1 识别受体 II','成熟 TGFβ1 二聚体先与受体 II 结合；潜伏复合物的释放在此合并。','receptor',port='II-left',targetPort='ligand'),
 ev('pair-II','dock','r2b','ligand',4,'配体组织受体对','第二个受体 II 结合配体另一端；两个受体始终保持跨膜位置。','assembly',['ligand-bind'],port='ligand',targetPort='II-right'),
 ev('pair-Ia','dock','r1a','ligand',4,'募集两个受体 I','两个受体 I 与配体–受体 II 复合物协同组装，形成 2:2 受体复合物。','assembly',['pair-II'],port='ligand',targetPort='I-left'),
 ev('pair-Ib','dock','r1b','ligand',4,'募集两个受体 I','展示第二个受体 I；顺序用于教学。','assembly',['pair-II'],port='ligand',targetPort='I-right',silent=True),
 ev('gs-a','state','r1a','r1a',2,'受体 I 的 GS 区磷酸化','受体 II 的激酶作用于受体 I 的 GS 调控区；P 圆圈代表该磷酸化状态。','gs',['pair-Ia','pair-Ib'],state='GS-P'),
 ev('gs-b','state','r1b','r1b',2,'受体 I 的 GS 区磷酸化','两个受体 I 分别保留代表性 GS 磷酸化标记。','gs',['pair-Ia','pair-Ib'],state='GS-P',silent=True),
 ev('phos-a','reaction','sa','r1a',6,'磷酸化第一个 SMAD3','受体 I 识别 SMAD3 的 MH2 区，磷酸化其 C 端；两个 P 圆圈表示 S423/S425。','smad-p',['gs-a','gs-b'],port='co-SMAD-left',targetPort='SMAD-substrate',stateTarget='sa',state='pS2',approach=[[desta[0]+22,590],[desta[0]+22,desta[1]]]),
 ev('phos-b','reaction','sb','r1b',6,'磷酸化第二个 SMAD3','第二个 SMAD3 获得相同的 C 端标记；反应结束后底物释放。','smad-p',['phos-a'],port='co-SMAD-left',targetPort='SMAD-substrate',stateTarget='sb',state='pS2',approach=[[1040,820],[720,820],[720,590],[destb[0]-22,590],[destb[0]-22,destb[1]]]),
 ev('trimer-a','dock','sa','s4',4,'磷酸化 SMAD3 结合 SMAD4','通过配对的 MH2 示意界面组装；P 圆圈随完整分子移动。','trimer',['phos-b'],port='co-SMAD-right',targetPort='co-SMAD-left',approach=[[480,650],[480,850]]),
 ev('trimer-b','dock','sb','s4',4,'形成 2:1 SMAD 三聚体','复合物包含两个磷酸化 SMAD3 与一个 SMAD4。两个配对界面使用同一套轮廓规则。','trimer',['trimer-a'],port='co-SMAD-right',targetPort='co-SMAD-right',approach=[[680,760],[680,850]]),
 ev('import','move','s4','npc',10,'完整复合物通过核孔','相连的三个组分与四个 P 标记一起通过核孔。图示合并核转运步骤，不指定唯一转运因子。','import',['trimer-b'],to=dict(slot=5,zone='arrival')),
 ev('dna-bind','dock','s4','dna',6,'核内结合响应元件','SMAD3/SMAD4 的 MH1 功能连接到 DNA；此处用一般双链 DNA 表示响应元件，未指定碱基序列。','dna',['import'],port='DNA-binding',targetPort='surface-contact',approach=[[440,1400],[440,1700],[604,1700]]),
 ev('transcribe','produce','rna','dna',5,'启动转录响应','与共调控因子协作后产生转录输出；这里合并表示共因子和 RNA 聚合酶。','transcription',['dna-bind'],stateTarget='rna',state='transcribed'),
 ev('hold','state','s4','s4',3,'信号已到达细胞核','受体、磷酸化状态、三聚体和核内响应共同构成完整主干。','transcription',['transcribe'],state='complex')]
model=dict(outputName='tgfb-smad',title='TGFβ1–ALK5–SMAD3/SMAD4 nuclear signaling',layout=dict(width=1180,height=2000,pitch=100,membraneY=330,zones=zones),entities=entities,events=events,initialStates={'r2a':'active','r2b':'active'},environment=dict(gate='npc',cargo=['sa','s4','sb'],transit='import',outerY=1000,innerY=1280,left=490,right=710),reviewTimes={'normal':[0,4,8,12,14,16,18,20,22,24,26,28,30,32,34,36,39,42,44,46,48,50,53,55,58],'alk5-blocked':[16],'smad3-2SA':[28]},scope='Canonical SMAD3 branch. Timings, scale and interface curves are teaching geometry; latent activation, SARA, feedback, explicit import factors and co-regulators are combined or omitted.')
(P/'mechanism.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
refs=json.loads((P/'references.json').read_text());data=json.dumps(dict(model=model,icons=icons,references=refs),ensure_ascii=False).replace('</','<\\/')
html=(P/'preview-template.html').read_text().replace('/*DATA*/','const DATA='+data+';').replace('/*ENGINE*/',(P.parent/'biomedical-manim/domain-motion.js').read_text()).replace('/*ARROWS*/',(S/'scripts/mechanism-arrows.js').read_text()).replace('/*ICON_STYLE*/',(L.parents[1]/'scripts/mechanism-icons.js').read_text()).replace('/*ANNOTATIONS*/',(S/'scripts/mechanism-annotations.js').read_text()).replace('/*SCENE*/',(P/'scene.js').read_text())
(P.parent/'biomedical-manim/output').mkdir(parents=True, exist_ok=True)
for out in [P/'preview.html',S/'assets/tgfb-generated.html',P.parent/'biomedical-manim/output/tgfb-generated.html']:out.write_text(html)
shutil.copy2(P/'mechanism.json',F/'mechanism-example.json');shutil.copy2(P/'scene.js',F/'scene.js')
print(json.dumps({'generatedIcons':8,'entities':len(entities),'RIIscale':sr,'RIscale':si,'assemblyX':[240,xIa,xIb,xII]},indent=2))
