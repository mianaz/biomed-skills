"""Native matplotlib export and reproducible SVG object editing for Plot Tuner."""
from copy import deepcopy
from io import StringIO
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
PT = 72 / 25.4
ET.register_namespace('', SVG)
LEAVES = {'text','path','polyline','polygon','line','rect','circle','ellipse','use','image'}


def style(node, patch=None):
    result = dict(field.strip().split(':', 1) for field in node.get('style','').split(';') if ':' in field)
    result = {k.strip():v.strip() for k,v in result.items()}
    result.update(patch or {})
    node.set('style',';'.join(f'{k}:{v}' for k,v in result.items()))
    return result


def number(value, default=0):
    match = re.match(r'[-+\d.eE]+', str(value or ''))
    return float(match[0]) if match else default


def model(root, prefix, owners):
    parent = {child:node for node in root.iter() for child in node}
    elements, groups, counters = [], {}, {}
    for node in root.iter():
        tag = node.tag.split('}')[-1]
        ancestry, p = [], parent.get(node)
        while p is not None:
            ancestry.insert(0,p)
            p = parent.get(p)
        if tag not in LEAVES or any(p.tag.split('}')[-1] in {'defs','clipPath','mask','marker','pattern'} for p in ancestry):
            continue
        chain = [*ancestry,node]
        inherited = {}
        group_ids = []
        for p in chain:
            owner = p.get('data-tuner-owner')
            if owner:
                inherited.update(owners.get(owner,{}))
                group_ids.append(owner)
            group = p.get('data-tuner-group')
            if group:
                group_ids.append(group)
        role = inherited.get('role','text' if tag=='text' else 'graphic')
        if role=='axis': role='text-tick' if tag=='text' else 'axis-line'
        if tag=='text' and role=='axis-line': role='text-tick'
        if tag=='use' and role=='data-line': role='data-point'
        n = lambda key:number(node.get(key))
        cx,cy = n('x'),n('y')
        if tag in ('circle','ellipse'): cx,cy=n('cx'),n('cy')
        if tag=='rect': cx,cy=cx+n('width')/2,cy+n('height')/2
        if tag=='line': cx,cy=(n('x1')+n('x2'))/2,(n('y1')+n('y2'))/2
        if tag in ('polyline','polygon'):
            v=[float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:e[-+]?\d+)?',node.get('points',''),re.I)]
            if v: cx,cy=(min(v[::2])+max(v[::2]))/2,(min(v[1::2])+max(v[1::2]))/2
        if tag=='path' and inherited.get('anchor'): cx,cy=inherited['anchor']
        transform=node.get('transform','')
        shift=re.search(r'translate\(\s*([-\d.e+]+)[,\s]+([-\d.e+]+)',transform,re.I)
        if shift: cx+=float(shift[1]);cy+=float(shift[2])
        rotation=re.search(r'rotate\(\s*([-\d.e+]+)',transform,re.I)
        rotation=float(rotation[1]) if rotation else 0
        s=style(node)
        font=number(s.get('font-size')) or number(re.search(r'([\d.]+)px',s.get('font',''))[1] if re.search(r'([\d.]+)px',s.get('font','')) else 11)
        owner_key=next((p.get('data-tuner-owner') for p in reversed(chain) if p.get('data-tuner-owner')),prefix)
        part=counters.get(owner_key,0);counters[owner_key]=part+1
        key=f'{owner_key}:node{part}'
        size=inherited.get('size_mm',2)
        node.attrib.update({'data-tuner-id':key,'data-tuner-leaf':'1','data-tuner-role':role,'data-tuner-cx':str(cx),'data-tuner-cy':str(cy),'data-tuner-size':str(size)})
        e={'id':key,'kind':'text' if tag=='text' else 'shape','tag':tag,'role':role,'label':''.join(node.itertext()) if tag=='text' else f'{role} {len(elements)+1}',
           'groups':list(dict.fromkeys(group_ids)),'anchor':[cx,cy],'angle_deg':rotation,'text_anchor':s.get('text-anchor',node.get('text-anchor','start')),'font_pt':font,'font_family':'Arial','stroke_mm':number(s.get('stroke-width'),.7)/PT,'size_mm':size,
           'fill':s.get('fill',node.get('fill','#000000' if tag=='text' else 'none')),'stroke':s.get('stroke',node.get('stroke','none')),
           'parent_transform':' '.join(p.get('transform','') for p in ancestry)}
        elements.append(e)
        for key in e['groups']:
            if key not in groups: groups[key]={**owners.get(key,{'id':key,'label':key,'role':'group'}),'id':key,'kind':'group','members':[]}
            groups[key]['members'].append(e['id'])
    return ET.tostring(root,encoding='unicode'),[*groups.values(),*elements]


def plot_tuner_export(figures,directory='plot-tuner',source_file='plot.py',object_name='fig',stat_data=None,stat_object=None):
    import matplotlib as mpl
    from matplotlib.text import Text
    if not isinstance(figures,dict): figures={'panel1':figures}
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    panels,left,canvas_height=[],5,0
    for name,fig in figures.items():
        fig.canvas.draw()
        width,height=fig.get_size_inches()*25.4
        owners,originals={},[]
        prefix=f'{name}/plot'
        def register(artist,key,role,label,group=None):
            originals.append((artist,artist.get_gid()));artist.set_gid(key)
            box=artist.get_window_extent(fig.canvas.get_renderer())
            anchor=[(box.x0+box.width/2)/fig.dpi*72,(fig.get_size_inches()[1]*fig.dpi-box.y0-box.height/2)/fig.dpi*72]
            if not all(math.isfinite(v) for v in anchor): anchor=[0,0]
            owners[key]={'id':key,'role':role,'label':label,'group':group,'anchor':anchor}
        known={}
        for i,ax in enumerate(fig.axes):
            known.update({ax.title:(f'ax{i}-title','text-title'),ax.xaxis.label:(f'ax{i}-xlabel','text'),ax.yaxis.label:(f'ax{i}-ylabel','text')})
            for j,tick in enumerate(ax.get_xticklabels()):known[tick]=(f'ax{i}-xtick{j}','text-tick')
            for j,tick in enumerate(ax.get_yticklabels()):known[tick]=(f'ax{i}-ytick{j}','text-tick')
            for j,text in enumerate(ax.texts):known[text]=(f'ax{i}-annotation{j}','text')
        for i,text in enumerate(t for t in fig.findobj(Text) if t.get_text() and t.get_visible()):
            key,role=known.get(text,(f'text{i}','text'))
            register(text,f'{prefix}:{key}',role,text.get_text())
        for i,ax in enumerate(fig.axes):
            for axis,side,label in [(ax.xaxis,'bottom','X 坐标轴'),(ax.yaxis,'left','Y 坐标轴')]:
                key=f'{prefix}:axis{i}-{side}';register(axis,key,'axis-line',f'{label} {i+1}',key)
                owners[key]['role']='axis'
            for side,spine in ax.spines.items():
                group=f'{prefix}:axis{i}-'+('bottom' if side in ('bottom','top') else 'left')
                register(spine,f'{prefix}:spine{i}-{side}','axis-line','轴线',group)
            for j,line in enumerate(ax.get_lines()):
                key=f'{prefix}:line{i}-{j}';register(line,key,'data-line',line.get_label() if not line.get_label().startswith('_') else f'曲线系列 {j+1}',key)
                owners[key]['size_mm']=line.get_markersize()/PT
            for j,collection in enumerate(ax.collections):
                key=f'{prefix}:points{i}-{j}';register(collection,key,'data-point',f'点系列 {j+1}',key)
                sizes=collection.get_sizes() if hasattr(collection,'get_sizes') else []
                owners[key]['size_mm']=math.sqrt(sizes[0])/PT if len(sizes) else 2
            for j,patch in enumerate(ax.patches):
                key=f'{prefix}:bar{i}-{j}';group=f'{prefix}:bars{i}';register(patch,key,'data-bar',f'条形 {j+1}',group)
                owners.setdefault(group,{'id':group,'role':'series','label':f'条形系列 {i+1}'})
            for j,line in enumerate([*ax.get_xgridlines(),*ax.get_ygridlines()]): register(line,f'{prefix}:grid{i}-{j}','grid','网格')
        for i,legend in enumerate([*fig.legends,*[ax.get_legend() for ax in fig.axes if ax.get_legend()]]):
            key=f'{prefix}:legend{i}';register(legend,key,'legend','图例',key)
        buffer=StringIO()
        with mpl.rc_context({'svg.fonttype':'none'}): fig.savefig(buffer,format='svg')
        root=ET.fromstring(buffer.getvalue())
        for node in root.iter():
            key=node.get('id','')
            if key in owners:
                owner=owners[key];node.set('data-tuner-owner',key)
                # Axis groups supply membership; leaf text retains its own role.
                if owner.get('group'): node.set('data-tuner-group',owner['group'])
                node.set('data-tuner-role','axis-line' if owner['role']=='axis' else owner['role'])
                if owner.get('group'):
                    group=owners.get(owner['group'],owner);node.set('data-tuner-group-label',group['label']);node.set('data-tuner-group-role','axis' if 'axis' in owner['group'] else 'series' if owner['role'].startswith('data') else owner['role'])
            if key and key not in owners:
                new=f'{name}_{key}'
                for item in root.iter():
                    for attr,value in list(item.attrib.items()): item.set(attr,f'#{new}' if value==f'#{key}' else value.replace(f'url(#{key})',f'url(#{new})'))
                node.set('id',new)
        svg,elements=model(root,prefix,owners)
        for artist,gid in originals: artist.set_gid(gid)
        legend_items=[]
        from matplotlib.colors import to_hex
        for ax in fig.axes:
            handles,labels=ax.get_legend_handles_labels()
            for handle,label in zip(handles,labels):
                paint=handle.get_color() if hasattr(handle,'get_color') else handle.get_facecolor() if hasattr(handle,'get_facecolor') else '#1f78b4'
                legend_items.append({'label':label,'color':to_hex(paint)})
        region=None
        if fig.axes:
            box=fig.axes[0].get_position();ax=fig.axes[0]
            ticks=ax.get_xticks();labels=[t.get_text() for t in ax.get_xticklabels()]
            positions=[ax.transData.transform((x,0))[0]/fig.dpi*25.4 for x in ticks]
            region={'x':box.x0*width,'y':(1-box.y1)*height,'width':box.width*width,'height':box.height*height,'x_labels':labels,'x_positions':positions}
        panels.append({'id':name,'name':name,'x':left,'y':5,'width':float(width),'height':float(height),'region':region,'legend_items':legend_items,
                       'layers':[{'id':prefix,'role':'plot','x':0,'y':0,'width':float(width),'height':float(height),'svg':svg,'elements':elements}]})
        left+=float(width)+5;canvas_height=max(canvas_height,float(height)+10)
    if stat_data:
        stat_data={key:[{'group':str(r['group']),'value':float(r['value']) if r.get('value') is not None and math.isfinite(float(r['value'])) else None,'id':str(r['id']) if r.get('id') is not None else None} for r in (rows.to_dict('records') if hasattr(rows,'to_dict') else rows)] for key,rows in stat_data.items()}
    project={'schema':'bioinfospace.plot-tuner/2','editor_version':3,'engine':'matplotlib','name':Path(source_file).name,'source_file':source_file,'object_name':object_name,
             'canvas':{'width':left,'height':canvas_height},'stat_data':stat_data,'stat_object':stat_object,'panels':panels}
    (directory/'project.json').write_text(json.dumps(project,ensure_ascii=False,indent=2))
    return project


def extend_operations(layer,operations,panel,settings):
    operations=deepcopy(operations);known={o['id'] for o in operations};metadata={e['id']:e for e in layer['elements']}
    preset=settings.get('styles',{}).get(panel['id'],{});colors=preset.get('colors') or [];sources=preset.get('source_colors') or []
    for e in layer['elements']:
        if e['kind']=='group' or e['id'] in known:continue
        op={'id':e['id']};dx=dy=0
        if preset.get('theme') not in (None,'original'):
            if e['role']=='grid' or e['role']=='axis-line' and preset['theme']=='minimal':op['hidden']=True
            if e['role']=='background':op['fill']='#ffffff'
            if e['role']=='axis-line' and preset['theme']=='prism':op['stroke_mm']=.35
            if e['kind']=='text':op['font_family']='Arial'
        if colors:
            primary=e['stroke'] if e['role']=='data-line' else e['fill'] if e['fill'] not in ('none','#ffffff','#FFFFFF') else e['stroke']
            source=primary[:7].lower()
            if source in sources:op['color']=colors[sources.index(source)%len(colors)]
            else:
                for paint in ('fill','stroke'):
                    source=e[paint][:7].lower()
                    if source in sources:op[paint]=colors[sources.index(source)%len(colors)]
        for key in [*e.get('groups',[]),e['id']]:
            edit=settings['elements'].get(key)
            if not edit:continue
            dx+=edit.get('dx_mm',0);dy+=edit.get('dy_mm',0);op.update(edit)
            if 'font_pt' in edit and e['kind']=='text' and key!=e['id']:
                font=max((metadata[i]['font_pt'] for i in metadata.get(key,{}).get('members',[]) if metadata[i]['kind']=='text'),default=e['font_pt'])
                op['font_pt']=edit['font_pt']*e['font_pt']/font
        if dx:op['dx_mm']=dx
        if dy:op['dy_mm']=dy
        if e['kind']!='text':op.pop('font_pt',None);op.pop('text_anchor',None)
        if e['role']=='axis-line' and 'angle_deg' not in settings['elements'].get(e['id'],{}):op.pop('angle_deg',None)
        if len(op)>1:operations.append(op)
    return operations


def apply_operations(svg,layer,operations):
    meta={e['id']:e for e in layer['elements']}
    parent={child:node for node in svg.iter() for child in node}
    nodes={n.get('data-tuner-id'):n for n in svg.iter() if n.get('data-tuner-id')}
    for op in operations:
        node=nodes.get(op['id'])
        if node is None: continue
        e=meta[op['id']];s={}
        if op.get('hidden'): s['display']='none'
        if op.get('color'):
            if e['kind']=='text': s['fill']=op['color']
            else:
                for paint in ('fill','stroke'):
                    if e[paint]!='none': s[paint]=op['color']
        for key in ('fill','stroke','opacity'):
            if key in op: s[key]=op[key]
        if 'stroke_mm' in op and e['kind']!='text': s['stroke-width']=op['stroke_mm']*PT
        if e['kind']=='text':
            if op.get('text_anchor'):s['text-anchor']=op['text_anchor'];node.set('text-anchor',op['text_anchor'])
            for key in ('font_family','font_weight','font_style'):
                if op.get(key): s[key.replace('_','-')]=op[key]
            if 'font_pt' in op: s['font-size']=str(op['font_pt'])+'px'
            if 'text' in op:
                for child in list(node): node.remove(child)
                node.text=op['text']
            if any(k in op for k in ('font_pt','font_family','font_weight','font_style','text')):
                node.attrib.pop('textLength',None);node.attrib.pop('lengthAdjust',None)
        if op.get('size_mm') and e['role']=='data-point':s['stroke-width']=op.get('stroke_mm',e.get('stroke_mm',number(style(node).get('stroke-width'),.7)/PT))*PT/(op['size_mm']/e['size_mm'])
        style(node,s)
        cx,cy=e['anchor'];dx,dy=op.get('dx_mm',0)*PT,op.get('dy_mm',0)*PT
        angle=op.get('angle_deg',e['angle_deg'])-e['angle_deg']
        size=op.get('size_mm',e['size_mm'])/e['size_mm'] if e['role']=='data-point' else 1
        sx=(op.get('bar_width_pct',100)/100 if e['role']=='data-bar' else 1)*size
        transform=f'translate({dx} {dy}) rotate({angle} {cx} {cy}) translate({cx} {cy}) scale({sx} {size}) translate({-cx} {-cy}) '
        if op.get('before_svg'):
            p=parent[node];p.insert(list(p).index(node),ET.fromstring(op['before_svg']))
        if dx or dy:
            transform+=e.get('parent_transform','')+' ';parent[node].remove(node)
            detached=next((n for n in svg if n.get('data-tuner-detached') is not None),None)
            if detached is None:detached=ET.SubElement(svg,f'{{{SVG}}}g',{'class':'svglite','data-tuner-detached':''})
            detached.append(node)
        node.set('transform',transform+node.get('transform',''))
    return svg


def recompute_statistics(project,settings):
    annotations=[a for a in settings.get('annotations',[]) if a['type']=='stat']
    if not annotations: return []
    families={}
    for a in annotations:
        if a.get('method') in ('welch','student','paired'):
            from scipy import stats
            rows=(project.get('stat_data') or {}).get(a['panel']) if a.get('data_source')=='project' else settings.get('stat_sources',{}).get(a.get('source_key'),{}).get('rows')
            if not rows: raise ValueError('The fresh plot export has no linked statistics data')
            x=[r for r in rows if r['group']==a['group1']];y=[r for r in rows if r['group']==a['group2']]
            if a['method']=='paired':
                if any(not r.get('id') for r in x+y) or len({str(r['id']) for r in x})!=len(x) or len({str(r['id']) for r in y})!=len(y):raise ValueError('Paired data require unique IDs within each group')
                left={str(r['id']):r['value'] for r in x};right={str(r['id']):r['value'] for r in y}
                ids=[k for k in left if k in right and left[k] is not None and right[k] is not None]
                xx=[left[k] for k in ids];yy=[right[k] for k in ids];r=stats.ttest_rel(xx,yy)
            else:
                xx=[r['value'] for r in x if r['value'] is not None];yy=[r['value'] for r in y if r['value'] is not None]
                r=stats.ttest_ind(xx,yy,equal_var=a['method']=='student')
            if not math.isfinite(r.pvalue): raise ValueError('The new data do not support the saved statistical test')
            interval=r.confidence_interval()
            a.update(p_value=float(r.pvalue),statistic=float(r.statistic),df=float(r.df),n1=len(xx),n2=len(yy),omitted=len(x)+len(y)-len(xx)-len(yy),effect=sum(xx)/len(xx)-sum(yy)/len(yy),ci_low=float(interval.low),ci_high=float(interval.high))
        families.setdefault(a['family'],[]).append(a)
    for family in families.values():
        method=family[0].get('adjustment','holm')
        if method=='provided': continue
        order=sorted(range(len(family)),key=lambda i:family[i]['p_value']);running=1 if method=='BH' else 0
        if method=='none':
            for a in family:a['p_adjusted']=a['p_value']
        elif method=='BH':
            for k in reversed(range(len(order))):
                a=family[order[k]];running=min(running,a['p_value']*len(order)/(k+1));a['p_adjusted']=running
        else:
            for k,i in enumerate(order):
                a=family[i];running=max(running,a['p_value']*(len(order)-k));a['p_adjusted']=min(1,running)
    return annotations


def stat_label(a):
    p=a['p_adjusted'] if a.get('use_adjusted') else a['p_value']
    if a.get('display')=='stars': return '****' if p<.0001 else '***' if p<.001 else '**' if p<.01 else '*' if p<.05 else 'ns'
    return ('adjusted P' if a.get('use_adjusted') else 'P')+(' < 0.0001' if p<.0001 else f' = {p:.3g}')


def plot_tuner_render(directory='plot-tuner',settings=None):
    import cairosvg
    import csv
    directory=Path(directory);project=json.loads((directory/'project.json').read_text())
    if settings is None:settings=directory/'tuner.json'
    if not isinstance(settings,dict):settings=json.loads(Path(settings).read_text())
    settings=deepcopy(settings);statistics=recompute_statistics(project,settings)
    canvas=settings['canvas'];root=ET.Element(f'{{{SVG}}}svg',{'width':f'{canvas["width"]}mm','height':f'{canvas["height"]}mm','viewBox':f'0 0 {canvas["width"]} {canvas["height"]}'})
    ET.SubElement(root,f'{{{SVG}}}rect',{'width':'100%','height':'100%','fill':'white'})
    for panel in project['panels']:
        box=settings['panels'].get(panel['id'],panel)
        for original in panel['layers']:
            layer=deepcopy(original);layer.update(settings['layers'].get(layer['id'],{}));svg=ET.fromstring(layer['svg'])
            if 'operations' in settings: apply_operations(svg,layer,extend_operations(layer,settings['operations'].get(layer['id'],[]),panel,settings))
            else:
                # Legacy settings address text groups exported by the earlier helper.
                for node in svg.iter():
                    edit=settings['elements'].get(node.get('data-tuner-id'))
                    if not edit:continue
                    if 'font_pt' in edit:
                        for text in ([node] if node.tag==f'{{{SVG}}}text' else node.iter(f'{{{SVG}}}text')):style(text,{'font-size':f'{edit["font_pt"]}px'});text.attrib.pop('textLength',None)
                    node.set('transform',f'translate({edit.get("dx_mm",0)*PT} {edit.get("dy_mm",0)*PT}) '+node.get('transform',''))
            sx,sy=box['width']/panel['width'],box['height']/panel['height']
            svg.attrib.update({'x':str(box['x']+layer['x']*sx),'y':str(box['y']+layer['y']*sy),'width':str(layer['width']*sx),'height':str(layer['height']*sy),'overflow':'visible'});root.append(svg)
        for overlay in settings.get('overlays',[]):
            if overlay['panel_id']!=panel['id']:continue
            svg=ET.fromstring(overlay['svg']);svg.attrib.update({k:str(box[k]) for k in ('x','y','width','height')});root.append(svg)
    by_id={a['id']:a for a in statistics}
    for node in root.iter():
        if node.get('data-stat-id') in by_id:node.text=stat_label(by_id[node.get('data-stat-id')])
    output=directory/'tuned.svg';ET.ElementTree(root).write(output,encoding='utf-8',xml_declaration=True)
    cairosvg.svg2pdf(url=str(output),write_to=str(directory/'tuned.pdf'))
    cairosvg.svg2png(url=str(output),write_to=str(directory/'tuned.png'),output_width=round(canvas['width']/25.4*600),output_height=round(canvas['height']/25.4*600))
    if statistics:
        fields=['id','panel','group1','group2','method','provided_method','n1','n2','statistic','df','effect','ci_low','ci_high','p_value','p_adjusted','adjustment','family','data_source','source_name','alternative','omitted']
        with (directory/'tuned-statistics.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(statistics)
    return output
