"""Native, editable schematic primitives; no image tracing or copied source artwork."""
from pathlib import Path
import json,math
import xml.etree.ElementTree as E
import cairosvg
F=Path(__file__).resolve().parent
S='http://www.w3.org/2000/svg';E.register_namespace('',S)
theme=json.loads((F.parents[1]/'basic-mechanisms/palettes.json').read_text())
C={k:next(p for p in theme['themes'] if p['id']==theme['default'])['colors'][k] for k in ['outline','protein','ligand','nucleic','membrane','interior']}
sources=json.loads((F/'references.json').read_text())
visual=[{'url':'https://www.biorender.com/template/blank-pathway-linear','usage':'Schematic reference; original vector geometry.'},{'url':'https://www.biorender.com/template/rna-secondary-structures','usage':'Schematic reference; original vector geometry.'}]
items=[]
def anchor(p,n=(0,-1),kind='binding'):return {'point':p,'normal':list(n),'kind':kind}
def add(id,label,zh,description,parts,anchors,group='proteins',refs=(),label_box=None):
 root=E.Element('{'+S+'}svg',{'viewBox':'0 0 160 160','width':'160','height':'160','role':'img'});E.SubElement(root,'{'+S+'}title').text=label
 E.SubElement(root,'{'+S+'}desc').text=description
 for role,content in parts:
  g=E.SubElement(root,'{'+S+'}g',{'id':id+'-'+role,'data-part':role,'stroke':C['outline'],'stroke-width':'1.6','stroke-linejoin':'round','stroke-linecap':'round'})
  for tag,attrs in content:E.SubElement(g,'{'+S+'}'+tag,{k:str(v) for k,v in attrs.items()})
 svg=E.tostring(root,encoding='unicode');(F/(id+'.svg')).write_text(svg+'\n');cairosvg.svg2png(bytestring=svg.encode(),write_to=str(F/'previews'/(id+'.png')),output_width=480,output_height=480)
 e={'id':id,'label':label,'label_zh':zh,'category':'generic-primitives','group':group,'file':f'generic-primitives/{id}.svg','preview':f'generic-primitives/previews/{id}.png','description':description,'description_zh':description,'parts':[p[0] for p in parts],'anchors':anchors,'scope':'Generic schematic symbol; identity, direction and state are separate figure annotations. Geometry and depicted counts are illustrative.','provenance':{'mode':'original-vector','source':'generic-primitives/build.py','license':'MIT','construction':'Native SVG geometry; PNG is a raster preview of this SVG.'},'visual_references':list(visual),'scientific_references':[{'url':u,'usage':'Schematic reference; original vector geometry.'} for u in refs]}
 e['palette_name']='Nord mist'
 e['visual_references']+=sources['visual_references'].get(group,[])
 e['scientific_references']+=sources['scientific_references'].get(id,[])
 e['palette']={k:v for k,v in C.items() if v in svg}
 e['primary_color']=C['nucleic' if group=='nucleic-acids' else 'membrane' if group=='compartments' else 'ligand' if group in ['ligands','small-molecules'] else 'protein']
 e['status']='archived' if id in ['generic-protein-rounded','generic-protein-circle','generic-protein-domains','generic-protein-complex','generic-receptor-single','generic-receptor-pair'] else 'current'
 e['basic_default']=e['status']=='current'
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
for kind,body,centers in [('y',y,(47,113)),('u',u,(53,107))]:
 add('generic-receptor-dimer-'+kind,kind.upper()+' receptor dimer',kind.upper()+' 型受体二聚体','两个'+kind.upper()+' 型受体单体并列组成二聚体，每个单体保留独立部件。',[(role,[path(body,transform=f'translate({x} 85) scale(.64) translate(-80 -80)',**{'stroke-width':2.5})]) for role,x in zip(['receptor-A','receptor-B'],centers)],{'membrane':anchor([80,101],kind='membrane'),'left-ligand':anchor([centers[0],85+((61 if kind=='y' else 75)-80)*.64]),'right-ligand':anchor([centers[1],85+((61 if kind=='y' else 75)-80)*.64]),'left-tail':anchor([centers[0],127.24],(0,1)),'right-tail':anchor([centers[1],127.24],(0,1))},'receptors')
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

# Generic extensions keep functional structures distinct from the capsule protein node.
def ellipse(x,y,rx,ry,fill,**kw):return ('ellipse',dict(cx=x,cy=y,rx=rx,ry=ry,fill=C.get(fill,fill),**kw))
ends={'left':anchor([18,80],(-1,0),'endpoint'),'right':anchor([142,80],(1,0),'endpoint')}
add('generic-dna-ladder','DNA ladder','DNA 双链梯子','两条骨架与配对横档；组图中单独标明 DNA 及链方向。',[('base-pairs',[line(x,58,x,102) for x in range(28,141,14)]),('strand-A',[rect(18,54,124,7,3.5,'nucleic')]),('strand-B',[rect(18,99,124,7,3.5,'protein')])],ends,'nucleic-acids')
a='M17 80C32 45 48 45 64 80S96 115 112 80S136 45 143 66';b='M17 80C32 115 48 115 64 80S96 45 112 80S136 115 143 94'
pairs=[]
for points in [[(17,80),(32,45),(48,45),(64,80)],[(64,80),(80,115),(96,115),(112,80)],[(112,80),(128,45),(136,45),(143,66)]]:
 for t in [.2,.4,.6,.8]:
  x,y=[sum(points[j][axis]*v for j,v in enumerate([(1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3])) for axis in [0,1]]
  pairs.append(line(round(x,2),round(y,2),round(x,2),round(160-y,2)))
add('generic-dna-helix','DNA double helix','DNA 双螺旋','两条反相起伏的骨架与贴合的配对横档表示 DNA 双螺旋。',[('pairs',pairs),('strand-A',[path(a,'none',stroke=C['nucleic'],**{'stroke-width':6})]),('strand-B',[path(b,'none',stroke=C['protein'],**{'stroke-width':6})])],ends,'nucleic-acids')
add('generic-gene-track','Promoter and gene','启动子与基因','启动子短块、基因长块和转录方向线；名称与调控关系由组图注明。',[('track',[line(17,90,143,90)]),('promoter',[rect(26,78,20,24,3,'ligand')]),('gene',[rect(60,78,73,24,3,'nucleic')]),('direction',[path('M45 61V46H92M84 38L92 46L84 54','none')])],{'promoter':anchor([36,78]),'transcript':anchor([142,90],(1,0),'output')},'nucleic-acids')
add('generic-mrna','Capped polyadenylated mRNA','带帽与尾的 mRNA','短帽、单链波浪骨架和末端小圆点表示成熟 mRNA；5′ 帽与 poly(A) 标签另加。并非所有 RNA 都有此结构。',[('cap',[circle(24,80,8,'ligand')]),('body',[path('M32 80C42 55 52 55 62 80S82 105 92 80S112 55 118 80','none',stroke=C['nucleic'],**{'stroke-width':5})]),('tail',[line(118,80,139,80)]+[circle(x,80,3,'nucleic') for x in [122,130,138]])],{'five-prime':anchor([16,80],(-1,0),'endpoint'),'three-prime':anchor([141,80],(1,0),'endpoint')},'nucleic-acids')
add('generic-nucleosome','Nucleosome','核小体','胶囊形组蛋白核心外绕一条连续 DNA 示意线，入口和出口可分别定位。',[('core',[rect(46,51,68,58,29,'protein')]),('DNA',[path('M17 99C34 103 37 91 48 83C65 70 104 70 112 57C127 34 30 30 43 58C49 71 106 82 115 96C129 119 46 132 44 107C42 88 126 72 143 79','none',stroke=C['nucleic'],**{'stroke-width':5})])],ends,'chromatin')
add('generic-chromatin','Chromatin beads','核小体串','三个独立胶囊核心与连续 DNA 线表示核小体串；数目只是图形示例。',[('cores',[rect(x,61,34,38,17,'protein') for x in [24,63,102]]),('DNA',[path('M14 93C23 92 22 70 32 69C64 52 62 109 41 110C22 111 54 57 76 69C98 80 97 112 80 111C60 108 100 55 118 69C147 91 139 110 121 108C107 105 133 79 146 81','none',stroke=C['nucleic'],**{'stroke-width':4})])],ends,'chromatin')
add('generic-ribosome','Ribosome','核糖体','上下两个圆角亚基夹住 mRNA 通路；肽链出口与 mRNA 入口分别保留锚点。',[('large-subunit',[rect(32,36,96,49,24.5,'protein')]),('small-subunit',[rect(43,96,74,27,13.5,'nucleic')]),('mRNA',[path('M17 90H143','none',stroke=C['nucleic'],**{'stroke-width':4})])],{'mRNA-in':anchor([17,90],(-1,0),'endpoint'),'mRNA-out':anchor([143,90],(1,0),'endpoint'),'peptide-exit':anchor([80,36])},'machinery')
add('generic-polyubiquitin','Polyubiquitin chain','多聚泛素链','四个小胶囊表示相连的 Ub 单元；链型和连接位点必须由外部标签指定。',[('links',[line(43,110,70,89),line(70,89,97,68),line(97,68,124,47)])]+[(f'Ub-{i+1}',[rect(x-17,y-10,34,20,10,'ligand')]) for i,(x,y) in enumerate([(36,116),(65,92),(94,68),(123,44)])],{'substrate':anchor([19,116],(-1,0)),'distal':anchor([140,44],(1,0))},'modifications')
add('generic-proteasome','Proteasome','蛋白酶体','轴向桶形核心与两端调节帽组成降解装置，入口与出口分别设置锚点。',[('core',[rect(48,45,64,70,10,'protein')]),('rings',[path('M48 65H112M48 95H112','none')]),('caps',[rect(39,27,82,23,11.5,'nucleic'),rect(39,110,82,23,11.5,'nucleic')]),('entry',[ellipse(80,35,14,4,'interior')])],{'entry':anchor([80,31]),'exit':anchor([80,133],(0,1),'output')},'machinery')
add('generic-peptide-fragments','Peptide fragments','降解肽片段','三个相互分离的短胶囊表示降解产物；完整蛋白仍使用统一胶囊节点。',[('fragment-A',[rect(26,50,48,16,8,'protein')]),('fragment-B',[rect(89,79,44,16,8,'protein')]),('fragment-C',[rect(43,110,39,16,8,'protein')])],{'center':anchor([80,80],kind='layout')},'modifications')
add('generic-ion-channel','Ion channel','离子通道','两侧竖直胶囊亚基围成开放孔道；膜中平面与孔道入口分别设置锚点。',[('subunit-A',[rect(39,29,31,102,15.5,'protein')]),('subunit-B',[rect(90,29,31,102,15.5,'protein')])],{'membrane':anchor([80,80],kind='membrane'),'outside':anchor([80,29]),'inside':anchor([80,131],(0,1))},'receptors')
add('generic-small-molecule','Small molecule','小分子','圆角六边形是小分子占位符；名称和药物作用关系由图中标签指定。',[('molecule',[path('M50 36Q53 31 59 31H101Q107 31 110 36L134 75Q137 80 134 85L110 124Q107 129 101 129H59Q53 129 50 124L26 85Q23 80 26 75Z','ligand')])],{'target':anchor([80,129],(0,1))},'small-molecules',label_box=[46,66,68,28])
for sign in ['positive','negative']:
 add('generic-ion-'+sign,sign.title()+' ion','正离子' if sign=='positive' else '负离子','圆圈内的电荷符号表示离子类别；元素名与价态由独立标签指定。',[('ion',[circle(80,80,31,'ligand')]),('charge',[line(67,80,93,80,**{'stroke-width':3})]+([line(80,67,80,93,**{'stroke-width':3})] if sign=='positive' else []))],{'center':anchor([80,80],kind='layout')},'small-molecules')
add('generic-nucleus','Nucleus with transport opening','带运输开口的细胞核','双层核膜在左侧留出明确通路；染色质与核仁为单独部件。',[('nucleoplasm',[ellipse(80,80,57,53,'interior',stroke='none')]),('envelope',[path('M29 101A57 53 0 1 0 29 59M35 99A51 47 0 1 0 35 61','none',**{'stroke-width':2.4})]),('nucleolus',[ellipse(98,66,13,10,'nucleic')])],{'import':anchor([26,80],(-1,0),'transport'),'interior':anchor([80,91],kind='layout')},'compartments')
add('generic-nuclear-pore','Nuclear pore cross-section','核孔截面','上下两层膜边缘与两侧胶囊组成简化核孔，中央保留运输通路。',[('envelope',[path('M17 59H51M109 59H143M17 101H51M109 101H143','none',stroke=C['membrane'],**{'stroke-width':6})]),('pore-left',[rect(49,49,20,62,10,'protein')]),('pore-right',[rect(91,49,20,62,10,'protein')])],{'cytoplasm':anchor([80,30]),'nucleoplasm':anchor([80,130],(0,1)),'midplane':anchor([80,80],kind='membrane')},'compartments')
add('generic-mitochondrion','Mitochondrion','线粒体','外膜包围带嵴的内膜；两层膜与基质可分别编辑。',[('matrix',[path('M20 78C20 34 74 21 117 38C157 53 150 115 108 127C61 140 20 117 20 78Z','interior')]),('inner-membrane',[path('M31 78C31 47 51 40 61 42C73 44 48 79 62 88C77 98 75 44 89 45C103 47 78 106 93 110C110 114 105 54 119 55C140 57 138 102 109 116C65 134 31 109 31 78Z','membrane')])],{'surface':anchor([80,31]),'matrix':anchor([80,80],kind='layout')},'compartments')
add('generic-er','Endoplasmic reticulum','内质网','连续的扁平膜囊和相连内腔；此符号不区分粗面与光面内质网。',[('cisternae',[path('M32 30Q19 30 19 44V116Q19 130 32 130H130Q141 130 141 120Q141 110 130 110H46V91H121Q132 91 132 81Q132 71 121 71H46V50H130Q141 50 141 40Q141 30 130 30Z','membrane')]),('lumen-guide',[path('M129 40H34V120H129M34 81H120','none',stroke=C['interior'],**{'stroke-width':4})])],{'entry':anchor([139,40],(1,0),'transport'),'exit':anchor([139,120],(1,0),'transport')},'compartments')
add('generic-golgi','Golgi stack','高尔基体','三个彼此分离的弯曲扁囊组成高尔基堆；运输囊泡由单独图标添加。',[(f'cisterna-{i}',[path(f'M{30-i*2} {42+i*30}Q80 {21+i*30} {130+i*2} {42+i*30}Q{138+i} {51+i*30} {128+i*2} {57+i*30}Q80 {38+i*30} {32-i*2} {57+i*30}Q{22-i} {51+i*30} {30-i*2} {42+i*30}Z','membrane')]) for i in range(3)],{'cis':anchor([80,31]),'trans':anchor([80,121],(0,1))},'compartments')
add('generic-endosome','Endosome','内体','单层限制膜围成内腔，内含可分别编辑的胶囊货物。',[('membrane',[path('M24 79C17 50 37 32 64 34C83 37 90 26 112 39C140 53 146 93 123 115C102 133 79 116 58 124C32 132 16 107 24 79Z','membrane')]),('lumen',[path('M33 79C26 55 43 43 65 44C84 47 94 37 109 48C132 60 135 91 116 106C99 121 79 107 59 115C38 122 25 102 33 79Z','interior')]),('cargo',[rect(47,65,38,18,9,'protein'),rect(83,89,34,16,8,'protein')])],{'surface':anchor([80,36]),'cargo':anchor([80,80],kind='layout')},'compartments')
add('generic-lysosome','Lysosome','溶酶体','单层膜包围水解腔，短胶囊表示腔内酶；pH 与具体酶名称由组图注明。',[('membrane',[circle(80,80,56,'membrane')]),('lumen',[circle(80,80,47,'interior')]),('enzymes',[rect(x,y,25,12,6,'protein') for x,y in [(51,51),(86,66),(49,91),(88,101)]])],{'surface':anchor([80,24]),'lumen':anchor([80,80],kind='layout')},'compartments')
add('generic-autophagosome','Autophagosome','自噬体','双层膜包围待转运货物，用两道独立膜轮廓区别于内体和溶酶体。',[('outer-membrane',[circle(80,80,59,'membrane')]),('intermembrane-space',[circle(80,80,51,'interior')]),('inner-membrane',[circle(80,80,45,'membrane')]),('lumen',[circle(80,80,38,'interior')]),('cargo',[rect(52,68,56,24,12,'protein')])],{'surface':anchor([80,21]),'cargo':anchor([80,80],kind='layout')},'compartments')
add('generic-lipid-droplet','Lipid droplet','脂滴','中性脂质核心外为单分子层；与囊泡的双分子层分开表示。',[('core',[circle(80,80,48,'ligand')]),('monolayer-heads',[circle(80+54*math.cos(i*math.pi/12),80+54*math.sin(i*math.pi/12),3.4,'membrane') for i in range(24)])],{'surface':anchor([80,22]),'core':anchor([80,80],kind='layout')},'compartments')
add('generic-cell','Cell outline','细胞轮廓','简洁细胞边界与独立核轮廓，适合作为位置概览；具体细胞类型由名称指定。',[('cytoplasm',[path('M21 87C15 51 36 25 73 24C101 18 141 39 140 77C147 114 111 137 76 134C44 142 17 117 21 87Z','interior')]),('nucleus',[ellipse(88,79,25,22,'nucleic')])],{'surface':anchor([80,24]),'cytoplasm':anchor([48,83],kind='layout'),'nucleus':anchor([88,79],kind='layout')},'compartments')

(F/'manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
cat_path=F.parent/'catalog.json';cat=json.loads(cat_path.read_text());cat['icons']=[e for e in cat['icons'] if e['category']!='generic-primitives']+items;cat_path.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(items)} native generic icons and PNG previews.')
