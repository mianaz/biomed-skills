"""Lay out registered assets with measured bounds and fixed physical dimensions."""
from pathlib import Path
import argparse
import copy
import json
import math
import textwrap
import unicodedata
import xml.etree.ElementTree as ET
from icon_library import PACKAGE, load_library

NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)


def layout(keys, labels, kind='workflow', columns=2):
    library={a['key']:a for a in load_library()}
    assets=[library[k] for k in keys]
    cjk=lambda s:any(unicodedata.east_asian_width(c) in 'WF' for c in s)
    wrapped=[textwrap.wrap(s,10 if cjk(s) else 16,break_long_words=cjk(s)) or [''] for s in labels]
    font=3.9  # mm: 11.06 pt at the saved physical size
    cell=max(20,max(sum(1 if unicodedata.east_asian_width(c) in 'WF' else .52 for c in line)*font for lines in wrapped for line in lines))
    gap=5; margin=4; icon_height=23
    columns=len(keys) if kind in ['workflow','comparison'] else min(columns,len(keys))
    rows=2 if kind=='comparison' else math.ceil(len(keys)/columns)
    label_height=max(map(len,wrapped))*font*1.2
    row_height=icon_height+2+label_height+4
    width=2*margin+columns*cell+(columns-1)*gap
    height=2*margin+rows*row_height
    svg=ET.Element(f'{{{NS}}}svg',viewBox=f'0 0 {width:.4f} {height:.4f}',width=f'{width:.4f}mm',height=f'{height:.4f}mm')
    placed=[]
    chosen=list(enumerate(assets))*2 if kind=='comparison' else list(enumerate(assets))
    for index,(source_index,a) in enumerate(chosen):
        row,col=divmod(index,columns)
        x=margin+col*(cell+gap);y=margin+row*row_height
        file=a.get('reference_vector',a['file']) if kind=='comparison' and row==0 else a['file']
        source=ET.parse(PACKAGE/file).getroot()
        bounds=a.get('content_bounds')
        if not bounds:
            vx,vy,vw,vh=map(float,source.get('viewBox','0 0 160 160').split())
            bounds=[vx,vy,vx+vw,vy+vh]
        x0,y0,x1,y1=bounds
        scale=min(cell/(x1-x0),icon_height/(y1-y0))
        tx=x+(cell-(x1-x0)*scale)/2-x0*scale
        ty=y+(icon_height-(y1-y0)*scale)/2-y0*scale
        group=ET.SubElement(svg,f'{{{NS}}}g',{'data-asset':a['key'],'transform':f'translate({tx:.6f} {ty:.6f}) scale({scale:.6f})'})
        ids={n.get('id'):f'item-{index}-{n.get("id")}' for n in source.iter() if n.get('id')}
        for node in source.iter():
            if node.get('id'):node.set('id',ids[node.get('id')])
            for attribute,value in list(node.attrib.items()):
                for old,new in ids.items():
                    value=value.replace(f'url(#{old})',f'url(#{new})')
                    if value=='#'+old:value='#'+new
                node.set(attribute,value)
        for node in source:group.append(copy.deepcopy(node))
        baseline=y+icon_height+2+font
        for line_no,line in enumerate(wrapped[source_index]):
            label=ET.SubElement(svg,f'{{{NS}}}text',x=str(x+cell/2),y=str(baseline+line_no*font*1.2),
                attrib={'text-anchor':'middle','font-family':'Arial','font-size':str(font),'fill':'#2e3440'})
            label.text=line
        placed.append({'key':a['key'],'row':row,'column':col,'transform':[tx,ty,scale],
                       'cell_mm':[x,y,cell,icon_height],'label_baseline_mm':baseline,'file':file})
    if kind=='workflow':
        for col in range(columns-1):
            x=margin+(col+1)*cell+col*gap+1;y=margin+icon_height/2
            ET.SubElement(svg,f'{{{NS}}}path',d=f'M{x} {y}h{gap-2}m-1 -1l1 1l-1 1',
                fill='none',stroke='#779cad',attrib={'stroke-width':'.35','stroke-linejoin':'round'})
    return ET.tostring(svg,encoding='unicode'),{'kind':kind,'canvas_mm':[width,height],
        'font_pt':font/25.4*72,'gap_mm':gap,'placements':placed}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('scene',type=Path,help='JSON with assets: [{key, label}], kind and optional columns')
    p.add_argument('--out',required=True,type=Path)
    args=p.parse_args();spec=json.loads(args.scene.read_text())
    svg,geometry=layout([a['key'] for a in spec['assets']],[a['label'] for a in spec['assets']],spec.get('kind','workflow'),spec.get('columns',2))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(svg)
    args.out.with_suffix('.layout.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n')
    print(args.out)
