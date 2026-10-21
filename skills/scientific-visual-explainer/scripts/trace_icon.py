"""Convert a generated PNG into palette-controlled SVG and optional library entry.

python trace_icon.py icon.png library/family/icon.svg --spec icon.json --register library
Requires Pillow, NumPy and vtracer. The spec supplies palette roles and source-pixel anchors.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import vtracer

NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
S='{'+NS+'}'

def trace_icon(image_path, output, spec):
    image_path,output=Path(image_path),Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    im=Image.open(image_path).convert('RGBA');pixels=np.asarray(im)
    visible=pixels[:,:,3]>=128
    roles=list(spec['palette']);colors=list(spec['palette'].values())
    palette=np.array([[int(c[k:k+2],16) for k in (1,3,5)] for c in colors],dtype=float)
    distances=((pixels[:,:,:3,None].astype(float)-palette.T[None,None,:,:])**2).sum(axis=2)
    flat=palette[distances.argmin(axis=2)].astype('uint8')
    trace_input=image_path.with_name(image_path.stem+'-trace-input.png')
    Image.fromarray(np.dstack([flat,visible.astype('uint8')*255])).save(trace_input)
    vtracer.convert_image_to_svg_py(str(trace_input),str(output),colormode='color',hierarchical='stacked',
        mode='spline',filter_speckle=24,color_precision=8,layer_difference=1,corner_threshold=60,
        length_threshold=4,max_iterations=10,splice_threshold=45,path_precision=2)
    traced=ET.parse(output).getroot()
    x0,y0,x1,y1=Image.fromarray(visible.astype('uint8')*255).getbbox()
    scale=136/max(x1-x0,y1-y0);tx=80-(x0+x1)*scale/2;ty=80-(y0+y1)*scale/2
    root=ET.Element(S+'svg',viewBox='0 0 160 160',width='160',height='160',role='img')
    ET.SubElement(root,S+'title').text=spec['label']
    art=ET.SubElement(root,S+'g',id=spec['id']+'-art',transform=f'translate({tx} {ty}) scale({scale})')
    for i,path in enumerate(traced.findall(S+'path')):
        rgb=np.array([int(path.get('fill')[j:j+2],16) for j in (1,3,5)])
        k=int(((palette-rgb)**2).sum(axis=1).argmin());part=roles[k]
        path.set('fill',colors[k]);path.set('data-original-fill',colors[k])
        group=ET.SubElement(art,S+'g',id=f'{spec["id"]}-{part}-{i}',**{'data-part':part})
        group.append(path)
    ET.ElementTree(root).write(output,encoding='unicode',xml_declaration=True)
    anchors={name:dict(point=[a['point'][0]*scale+tx,a['point'][1]*scale+ty],
                      normal=a['normal'],kind=a.get('kind','binding')) for name,a in spec['anchors'].items()}
    entry={k:v for k,v in spec.items() if k not in ['palette','anchors']}
    entry.update(file=output.name,parts=roles,anchors=anchors,palette=spec['palette'],
        source_to_svg={'scale':scale,'translate':[tx,ty]},
        parts_note='Color-assisted semantic fill groups; shared outline paths retain paint order. Curate extra motion parts separately.')
    return entry

def register(entry,output,library):
    output,library=Path(output).resolve(),Path(library).resolve()
    entry['file']=str(output.relative_to(library))
    manifest=output.parent/'manifest.json'
    family=json.loads(manifest.read_text()) if manifest.exists() else []
    family=[x for x in family if x['id']!=entry['id']]+[entry]
    manifest.write_text(json.dumps(family,ensure_ascii=False,indent=2)+'\n')
    catalog_file=library/'catalog.json';catalog=json.loads(catalog_file.read_text())
    catalog['icons']=[x for x in catalog['icons'] if x['id']!=entry['id']]+[entry]
    catalog_file.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image');parser.add_argument('output');parser.add_argument('--spec',required=True)
    parser.add_argument('--register',metavar='LIBRARY')
    args=parser.parse_args();spec=json.loads(Path(args.spec).read_text())
    entry=trace_icon(args.image,args.output,spec)
    if args.register:register(entry,args.output,args.register)
    else:Path(args.output).with_suffix('.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n')
    print(entry['id']+': '+str(args.output))
