"""Three editable assemblies exercise the shared generic symbols at viewing size."""
from pathlib import Path
import json,re
F=Path(__file__).resolve().parent
icons={e['id']:e for e in json.loads((F/'manifest.json').read_text())}
colors=json.loads((F.parents[1]/'basic-mechanisms/palettes.json').read_text())['themes'][1]['colors']
def icon(name,x,y,s=1,key=None):
 e=icons['generic-'+name];raw=(F/Path(e['file']).name).read_text();raw=re.sub(r'<svg[^>]*>|</svg>','',raw).replace(e['id'],key or name)
 raw=raw.replace('stroke-width="1.6"',f'stroke-width="{1.6/s}"')
 return f'<g data-icon="{e["id"]}" transform="translate({x} {y}) scale({s}) translate(-80 -80)">{raw}</g>'
def text(x,y,s,size=20):
 font="Hiragino Sans GB,Microsoft YaHei,Noto Sans CJK SC,sans-serif" if re.search(r"[\u3400-\u9fff]",s) else "Arial,sans-serif"
 return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{colors["text"]}" font-family="{font}">{s}</text>'
def arrow(d):return f'<path d="{d}" fill="none" stroke="{colors["outline"]}" stroke-width="2.2" stroke-linejoin="round" marker-end="url(#arrow)"/>'
def protein(x,y,label,s=.8):return icon('protein-capsule',x,y,s,f'protein-{x}-{y}')+text(x,y+6,label,18)
def scene(id,body):return f'<svg id="{id}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 450" width="1000" height="450" role="img" aria-label="{id}"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{colors["outline"]}"/></marker></defs><rect width="1000" height="450" fill="white"/>{body}</svg>'
body=f'<rect x="25" y="50" width="375" height="330" rx="26" fill="{colors["interior"]}"/>'+text(75,186,'细胞核',17)+text(755,186,'细胞质',17)
body+=icon('chromatin',120,260,1.15)+icon('gene-track',310,260,1.15)+icon('mrna',510,260,1.15)+icon('ribosome',720,260,1.15)+protein(900,260,'Protein')+protein(310,95,'TF',.7)
body+=f'<path d="M202 260H228" stroke="{colors["outline"]}" stroke-width="2" stroke-dasharray="4 4"/>'+arrow('M393 260H427')+arrow('M596 260H632')+arrow('M807 260H840')+arrow('M310 120V196')
for x,label in [(120,'染色质'),(310,'启动子 / 基因'),(510,'成熟 mRNA'),(720,'翻译'),(900,'蛋白')]:body+=text(x,350,label)
body+=text(390,135,'转录调控',17)+text(500,416,'通用表达示例：染色质上下文、转录、RNA 输出与翻译',18)
expression=scene('expression',body)
body=protein(130,230,'Target')+protein(300,230,'Target',.9)+icon('polyubiquitin',385,170,.9)+f'<path d="M330 202V207" stroke="{colors["outline"]}" stroke-width="2"/>'+icon('proteasome',590,230,1.3)+icon('peptide-fragments',820,230,1.2)
body+=protein(300,75,'E3',.7)+arrow('M300 101V174')+arrow('M190 230H225')+arrow('M443 230H510')+arrow('M676 230H733')
for x,label in [(130,'底物蛋白'),(330,'带 Ub 链的底物'),(590,'蛋白酶体'),(820,'肽片段')]:body+=text(x,345,label)
body+=text(443,113,'Ub 链型另行标注',17)+text(500,416,'通用降解示例：具体链型、E3 与底物关系由证据指定',18)
degradation=scene('degradation',body)
body=icon('er',120,140,1.15)+icon('golgi',330,140,1.15)+icon('vesicle',550,140,.85)+icon('membrane',820,100,1.35)+icon('receptor-y',820,75,.9)+icon('endosome',820,320,.9)+icon('lysosome',550,320,.9)
body+=arrow('M206 140H238')+arrow('M424 140H483')+arrow('M618 140H715')+arrow('M820 208V252')+arrow('M747 320H626')+arrow('M895 320C965 320 970 210 886 185')
for x,y,label in [(120,238,'内质网'),(330,238,'高尔基体'),(550,238,'运输囊泡'),(940,160,'质膜'),(820,410,'内体'),(550,410,'溶酶体')]:body+=text(x,y,label)
body+=text(677,302,'分选',17)+text(940,365,'回收',17)
traffic=scene('traffic',body)
scenes=[('expression','染色质、RNA 与翻译',expression),('degradation','泛素标记与蛋白降解',degradation),('traffic','膜运输与回收',traffic)]
(F/'assemblies').mkdir(exist_ok=True)
for id,label,svg in scenes:(F/'assemblies'/f'{id}.svg').write_text(svg+'\n')
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nord generic 部件 · 三组组图检查</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f6f8;color:#2e3440;font:16px/1.7 Arial,sans-serif}main{max-width:1180px;margin:auto;padding:28px 24px}a{color:#3b617e}h1{font-size:30px}h2{font-size:22px}.stage{overflow:auto;background:white;border:1px solid #d8dee9;border-radius:8px}.stage svg{display:block;width:100%;min-width:900px;height:auto}article{margin:36px 0}.note{font-size:14px}button{font:inherit;background:white;border:1px solid #b8c2cc;border-radius:5px;padding:6px 12px;cursor:pointer}</style></head><body><main><a href="preview.html">← 38 个基础图标与标签编辑器</a><h1>同一套 Nord 部件，组成完整的图。</h1><p>胶囊保持蛋白身份；核酸、细胞器和装置使用各自的简洁符号。以下三图是通用组图示例，箭头表示所标注过程；具体因果关系由使用者的研究证据指定。</p>'''
for id,label,svg in scenes:page+=f'<article><h2>{label}</h2><div class="stage">{svg.replace("#arrow", "#"+id+"-arrow").replace("id=\"arrow\"", "id=\""+id+"-arrow\"")}</div><p><a href="assemblies/{id}.svg" download>下载完整可编辑 SVG ↓</a></p></article>'
page+='''<p class="note">组图参考：BioRender 的 <a href="https://www.biorender.com/template/central-dogma">Central Dogma</a>、<a href="https://www.biorender.com/template/ubiquitin-proteasome-system">Ubiquitin Proteasome System</a> 和 <a href="https://www.biorender.com/template/generic-endocytic-pathway">Generic Endocytic Pathway</a> 公开预览；细胞分区与膜拓扑另参考 <a href="https://doi.org/10.1038/s41580-018-0052-8">Giorgi 等的 Figure 1/2</a>。<a href="references.json">查看来源链接 →</a></p></main></body></html>'''
(F/'compositions.html').write_text(page)
print('Built three editable generic assemblies.')
