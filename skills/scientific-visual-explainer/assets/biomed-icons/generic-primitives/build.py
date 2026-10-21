"""Native, editable schematic primitives; no image tracing or copied source artwork."""
from pathlib import Path
import json,math
import xml.etree.ElementTree as E
import cairosvg
F=Path(__file__).resolve().parent
S='http://www.w3.org/2000/svg';E.register_namespace('',S)
C={'outline':'#3D5963','protein':'#69ADB5','ligand':'#E4BE78','nucleic':'#B2A6CD','membrane':'#B3D7CC','interior':'#EDF5F1'}
visual=[{'url':'https://www.biorender.com/template/blank-pathway-linear','inspection':'Public lightbox visually inspected for simple protein nodes and fork/cup receptor conventions; no artwork copied.'},{'url':'https://www.biorender.com/template/rna-secondary-structures','inspection':'Public lightbox visually inspected for single-strand, duplex and hairpin notation; original geometry authored below.'}]
items=[]
def anchor(p,n=(0,-1),kind='binding'):return {'point':p,'normal':list(n),'kind':kind}
def add(id,label,zh,description,parts,anchors,group='proteins',refs=(),label_box=None):
 root=E.Element('{'+S+'}svg',{'viewBox':'0 0 160 160','width':'160','height':'160','role':'img'});E.SubElement(root,'{'+S+'}title').text=label
 E.SubElement(root,'{'+S+'}desc').text=description
 for role,content in parts:
  g=E.SubElement(root,'{'+S+'}g',{'id':id+'-'+role,'data-part':role,'stroke':C['outline'],'stroke-width':'1.6','stroke-linejoin':'round','stroke-linecap':'round'})
  for tag,attrs in content:E.SubElement(g,'{'+S+'}'+tag,{k:str(v) for k,v in attrs.items()})
 svg=E.tostring(root,encoding='unicode');(F/(id+'.svg')).write_text(svg+'\n');cairosvg.svg2png(bytestring=svg.encode(),write_to=str(F/'previews'/(id+'.png')),output_width=480,output_height=480)
 e={'id':id,'label':label,'label_zh':zh,'category':'generic-primitives','group':group,'file':f'generic-primitives/{id}.svg','preview':f'generic-primitives/previews/{id}.png','description':description,'description_zh':description,'parts':[p[0] for p in parts],'anchors':anchors,'scope':'Generic diagram symbol; identity and state come from the consuming figure. Shape does not encode resolved structure or a specific receptor family.','provenance':{'mode':'original-vector','source':'generic-primitives/build.py','license':'MIT','construction':'Native SVG geometry; PNG is a raster preview of this SVG.'},'visual_references':visual,'scientific_references':[{'url':u,'inspection':'Primary structure-record metadata read for strand topology; coordinates and artwork not copied.'} for u in refs]}
 e['palette']={k:v for k,v in C.items() if v in svg}
 e['primary_color']=C['nucleic' if group=='nucleic-acids' else 'membrane' if group=='compartments' else 'ligand' if group=='ligands' else 'protein']
 if label_box:e['label_box']=label_box
 items.append(e)
def rect(x,y,w,h,r,fill):return ('rect',dict(x=x,y=y,width=w,height=h,rx=r,fill=C[fill]))
def path(d,fill='protein',**kw):return ('path',dict(d=d,fill=C.get(fill,fill),**kw))
def circle(x,y,r,fill):return ('circle',dict(cx=x,cy=y,r=r,fill=C[fill]))
def line(x1,y1,x2,y2,**kw):return ('line',dict(x1=x1,y1=y1,x2=x2,y2=y2,**kw))
ports={'top':anchor([80,54]),'bottom':anchor([80,106],(0,1)),'left':anchor([20,80],(-1,0)),'right':anchor([140,80],(1,0))}
add('generic-protein-rounded','Rounded protein','圆角矩形蛋白','用圆角矩形表示任意蛋白；名称由图中的独立标签指定。',[('body',[rect(20,54,120,52,13,'protein')])],ports,label_box=[27,61,106,38])
add('generic-protein-capsule','Capsule protein','胶囊形蛋白','两端半圆的通用蛋白节点，适合较短的名称。',[('body',[rect(20,54,120,52,26,'protein')])],ports,label_box=[38,61,84,38])
add('generic-protein-circle','Circular protein','圆形蛋白','圆形通用蛋白节点，可添加独立名称与状态标记。',[('body',[circle(80,80,43,'protein')])],{'top':anchor([80,37]),'right':anchor([123,80],(1,0)),'bottom':anchor([80,123],(0,1))},label_box=[48,63,64,34])
add('generic-protein-domains','Two-domain protein','双结构域蛋白','两个相连分区，可用于标出不同功能域。',[('connector',[rect(65,71,30,18,8,'protein')]),('domain-A',[rect(18,48,57,64,17,'protein')]),('domain-B',[rect(85,48,57,64,17,'ligand')])],{'left':anchor([18,80],(-1,0)),'right':anchor([142,80],(1,0))},label_box=[24,63,112,34])
add('generic-protein-complex','Protein complex','蛋白复合物','两种相邻蛋白组成的通用复合物占位图。',[('protein-A',[rect(18,48,70,48,13,'protein')]),('protein-B',[rect(72,70,70,48,13,'ligand')])],{'left':anchor([18,72],(-1,0)),'right':anchor([142,94],(1,0))})
add('generic-ligand-circle','Circular ligand','圆形配体','圆形配体，可与杯形受体组合。',[('ligand',[circle(80,80,36,'ligand')])],{'receptor':anchor([80,116],(0,1)),'top':anchor([80,44])},'ligands',label_box=[56,67,48,26])
add('generic-ligand-triangle','Triangular ligand','圆角三角配体','朝下的三角配体，可嵌入 Y 型受体的分叉处。',[('ligand',[path('M38 56H122Q134 56 126 64L86 104Q80 110 74 104L34 64Q26 56 38 56Z','ligand')])],{'receptor':anchor([80,107],(0,1))},'ligands',label_box=[57,63,46,22])
add('generic-ligand-diamond','Diamond ligand','圆角菱形配体','用不同配体形状区分通路中的输入信号。',[('ligand',[path('M74 35Q80 29 86 35L125 74Q131 80 125 86L86 125Q80 131 74 125L35 86Q29 80 35 74Z','ligand')])],{'receptor':anchor([80,128],(0,1))},'ligands',label_box=[54,67,52,26])
y='M72 139V87Q72 82 68 78L34 48Q28 42 34 36L39 31Q44 26 50 32L80 61L110 32Q116 26 122 32L128 38Q134 44 128 50L92 82Q88 86 88 92V139Q88 146 80 146Q72 146 72 139Z'
add('generic-receptor-y','Y receptor','Y 型受体','分叉的膜受体示意，受体身份由图中的标签指定。',[('receptor',[path(y)])],{'ligand':anchor([80,61]),'membrane':anchor([80,105],kind='membrane'),'cytoplasmic':anchor([80,146],(0,1))},'receptors')
u='M48 31Q42 31 42 37V50Q42 81 73 87V139Q73 146 80 146Q87 146 87 139V87Q118 81 118 50V37Q118 31 112 31Q106 31 106 37V49A26 26 0 0 1 54 49V37Q54 31 48 31Z'
add('generic-receptor-cup','Cup receptor','杯形受体','U 形结合口连接跨膜杆，可接纳圆形配体。',[('receptor',[path(u)])],{'ligand':anchor([80,75]),'membrane':anchor([80,105],kind='membrane'),'cytoplasmic':anchor([80,146],(0,1))},'receptors')
add('generic-receptor-single','Single-pass receptor','单杆膜受体','圆角胞外头部与单根跨膜杆相连的通用受体。',[('receptor',[path('M59 25H101Q114 25 114 38V64Q114 77 101 77H88V139Q88 146 80 146Q72 146 72 139V77H59Q46 77 46 64V38Q46 25 59 25Z')])],{'ligand':anchor([80,25]),'membrane':anchor([80,105],kind='membrane'),'cytoplasmic':anchor([80,146],(0,1))},'receptors')
add('generic-receptor-pair','Paired receptors','成对膜受体','两根并列受体杆，用于示意受体配对；具体组成由图注说明。',[('receptor-A',[path('M36 28H60Q70 28 70 38V67Q70 77 56 77V138Q56 145 49 145Q42 145 42 138V77Q27 77 27 67V38Q27 28 36 28Z')]),('receptor-B',[path('M100 28H124Q134 28 134 38V67Q134 77 120 77V138Q120 145 113 145Q106 145 106 138V77Q91 77 91 67V38Q91 28 100 28Z')])],{'membrane':anchor([81,105],kind='membrane'),'left-ligand':anchor([48,28]),'right-ligand':anchor([112,28])},'receptors')
# Broad colored strokes are RNA backbones, not outer silhouette outlines.
wave='M17 88C33 45 49 45 65 88S97 131 113 88S137 45 143 72'
add('generic-rna-wave','Single-stranded RNA','单链 RNA 波浪线','一条连续波浪线，用于表示单链 RNA。',[('backbone',[path(wave,'none',stroke=C['outline'],**{'stroke-width':8}),path(wave,'none',stroke=C['nucleic'],**{'stroke-width':4.8})])],{'five-prime':anchor([17,88],(-1,0),'endpoint'),'three-prime':anchor([143,72],(1,0),'endpoint')},'nucleic-acids')
add('generic-rna-comb','Single-strand RNA comb','单链 RNA 梯齿线','一条骨架带单侧短齿，短齿表示未配对的碱基。',[('bases',[line(x,87,x,63,stroke=C['outline'],**{'stroke-width':2.8}) for x in range(27,139,14)]),('backbone',[rect(17,85,126,7,3.5,'nucleic')])],{'five-prime':anchor([17,88.5],(-1,0),'endpoint'),'three-prime':anchor([143,88.5],(1,0),'endpoint')},'nucleic-acids')
add('generic-rna-duplex','Double-stranded RNA ladder','双链 RNA 梯子','两条平行骨架与中间横档表示双链 RNA；横档为碱基配对示意。',[('base-pairs',[line(x,62,x,98,stroke=C['outline'],**{'stroke-width':2.4}) for x in range(28,140,14)]),('strand-A',[rect(17,57,126,7,3.5,'nucleic')]),('strand-B',[rect(17,96,126,7,3.5,'protein')])],{'strand-A-5':anchor([17,60.5],(-1,0),'endpoint'),'strand-A-3':anchor([143,60.5],(1,0),'endpoint'),'strand-B-3':anchor([17,99.5],(-1,0),'endpoint'),'strand-B-5':anchor([143,99.5],(1,0),'endpoint')},'nucleic-acids',refs=['https://www.rcsb.org/structure/1RNA'])
hairpin='M58 141V79C19 45 47 17 80 17S141 45 102 79V141'
add('generic-rna-hairpin','RNA hairpin','RNA 发夹','一条 RNA 在顶部成环，茎部包含配对横档，底部保留两个端点。',[('base-pairs',[line(59,y,101,y,stroke=C['outline'],**{'stroke-width':2.4}) for y in range(87,139,12)]),('backbone',[path(hairpin,'none',stroke=C['outline'],**{'stroke-width':8}),path(hairpin,'none',stroke=C['nucleic'],**{'stroke-width':4.8})])],{'five-prime':anchor([58,141],(0,1),'endpoint'),'three-prime':anchor([102,141],(0,1),'endpoint'),'loop':anchor([80,17])},'nucleic-acids',refs=['https://www.rcsb.org/structure/1ZIH'])
# A short bilayer and a bilayer vesicle retain heads toward the aqueous sides.
heads=[];tails=[]
for x in range(24,142,16):
 heads.extend([circle(x,58,6,'membrane'),circle(x,102,6,'membrane')]);tails.extend([line(x-2,64,x-4,78),line(x+2,64,x+4,78),line(x-2,96,x-4,82),line(x+2,96,x+4,82)])
add('generic-membrane','Membrane segment','膜片段','两层亲水头部朝外，疏水尾部朝向膜内部；可在组图中重复铺排。',[('tails',tails),('heads',heads)],{'midplane':anchor([80,80],kind='membrane'),'left-edge':anchor([18,80],(-1,0),'layout'),'right-edge':anchor([142,80],(1,0),'layout')},'compartments')
heads=[];tails=[]
for i in range(16):
 a=2*math.pi*i/16;n=(math.cos(a),math.sin(a));q=(-n[1],n[0]);pt=lambda r,t=0:(80+n[0]*r+q[0]*t,80+n[1]*r+q[1]*t)
 for r in [58,39]:heads.append(circle(*pt(r),4,'membrane'))
 for t in [-1.4,1.4]:tails.extend([line(*pt(54,t),*pt(49,t)),line(*pt(43,t),*pt(47,t))])
add('generic-vesicle','Membrane vesicle','膜囊泡','环形双层膜包围内腔，适合表示通用运输囊泡。',[('lumen',[circle(80,80,36,'interior')]),('tails',tails),('heads',heads)],{'cargo':anchor([80,80],kind='layout'),'membrane':anchor([80,31.5],kind='membrane'),'surface':anchor([80,18])},'compartments')
(F/'manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
cat_path=F.parent/'catalog.json';cat=json.loads(cat_path.read_text());cat['icons']=[e for e in cat['icons'] if e['category']!='generic-primitives']+items;cat_path.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(items)} native generic icons and PNG previews.')
