"""Group named component parts and add Morph with a Fade fallback. Requires lxml.

python finish_figure_pptx.py draft.pptx deck.pptx --morph
Microsoft schema: https://learn.microsoft.com/en-us/openspecs/office_standards/ms-pptx/a54fd7b7-04d6-4d16-bbdd-b20b2b99578c
"""
import argparse
from pathlib import Path
import zipfile
from lxml import etree as E

P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
MC='http://schemas.openxmlformats.org/markup-compatibility/2006'
MORPH='http://schemas.microsoft.com/office/powerpoint/2015/09/main'
NS={'p':P,'a':A}


def finish(source, target, morph=False):
    with zipfile.ZipFile(source) as zin, zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data=zin.read(info.filename)
            if info.filename.startswith('ppt/slides/slide') and info.filename.endswith('.xml'):
                root=E.fromstring(data); tree=root.find('p:cSld/p:spTree',NS)
                next_id=max(int(n.get('id')) for n in root.findall('.//p:cNvPr',NS))+1
                groups={}
                for node in list(tree):
                    prop=node.find('.//p:cNvPr',NS)
                    identity=prop.get('name','') if prop is not None else ''
                    if prop is not None and not identity.startswith('!!'):identity=prop.get('descr','')
                    if identity.startswith('!!'):
                        prop.set('name',identity)
                        name=identity.rsplit('/',1)[0]
                        groups.setdefault(name,[]).append(node)
                for name,parts in groups.items():
                    group=E.Element(f'{{{P}}}grpSp'); nv=E.SubElement(group,f'{{{P}}}nvGrpSpPr')
                    E.SubElement(nv,f'{{{P}}}cNvPr',id=str(next_id),name=name);next_id+=1
                    E.SubElement(nv,f'{{{P}}}cNvGrpSpPr');E.SubElement(nv,f'{{{P}}}nvPr')
                    properties=E.SubElement(group,f'{{{P}}}grpSpPr'); xfrm=E.SubElement(properties,f'{{{A}}}xfrm')
                    positions=[p.find('.//a:xfrm',NS) for p in parts]
                    xs=[int(p.find('a:off',NS).get('x')) for p in positions]
                    ys=[int(p.find('a:off',NS).get('y')) for p in positions]
                    right=max(x+int(p.find('a:ext',NS).get('cx')) for x,p in zip(xs,positions))
                    bottom=max(y+int(p.find('a:ext',NS).get('cy')) for y,p in zip(ys,positions))
                    for tag,attrs in [('off',{'x':min(xs),'y':min(ys)}),('ext',{'cx':max(1,right-min(xs)),'cy':max(1,bottom-min(ys))}),('chOff',{'x':min(xs),'y':min(ys)}),('chExt',{'cx':max(1,right-min(xs)),'cy':max(1,bottom-min(ys))})]:
                        E.SubElement(xfrm,f'{{{A}}}{tag}',**{k:str(v) for k,v in attrs.items()})
                    at=list(tree).index(parts[0]);tree.insert(at,group)
                    for part in parts:group.append(part)
                if morph and info.filename!='ppt/slides/slide1.xml':
                    for old in root.findall('p:transition',NS):root.remove(old)
                    alternate=E.Element(f'{{{MC}}}AlternateContent',nsmap={'mc':MC,'p159':MORPH})
                    choice=E.SubElement(alternate,f'{{{MC}}}Choice',Requires='p159')
                    transition=E.SubElement(choice,f'{{{P}}}transition',spd='slow')
                    E.SubElement(transition,f'{{{MORPH}}}morph',option='byObject')
                    fallback=E.SubElement(alternate,f'{{{MC}}}Fallback')
                    E.SubElement(E.SubElement(fallback,f'{{{P}}}transition',spd='slow'),f'{{{P}}}fade')
                    before=root.find('p:timing',NS)
                    if before is None:before=root.find('p:extLst',NS)
                    root.insert(list(root).index(before) if before is not None else len(root),alternate)
                data=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
            zout.writestr(info,data)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('target',type=Path);p.add_argument('--morph',action='store_true')
    args=p.parse_args()
    if args.source.resolve()==args.target.resolve():raise ValueError('Use a separate output file.')
    args.target.parent.mkdir(parents=True,exist_ok=True)
    finish(args.source,args.target,args.morph)
