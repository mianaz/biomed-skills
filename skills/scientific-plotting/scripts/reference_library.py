#!/usr/bin/env python3
"""Search original-source recipes, published panels, R recipes and Prism templates."""
import argparse
import base64
import csv
import html
import json
import re
from pathlib import Path
import publication_gallery as gallery
from plot_families import annotate

ASSETS = gallery.SKILL / 'assets/reference-library'
EXTERNAL = ASSETS / 'external.json'
CURATION = ASSETS / 'curation.json'
TASKS = gallery.TASKS + ['effect-estimates']


def task_for(title):
    text = title.lower().replace('_', ' ')
    for words, task in [
        (['roc', 'precision recall', 'calibration'], 'prediction'),
        (['生存', 'survival', 'kaplan'], 'survival'),
        (['forest', '森林'], 'effect-estimates'),
        (['热图', 'heatmap', 'matrix'], 'matrix'),
        (['umap', 'featureplot', 'pca', 'cellplot', 'plot1cell', 'scanpy', 'galaxy'], 'embedding'),
        (['比例', '堆叠', 'stacked', 'composition', 'pie', 'donut'], 'composition'),
        (['富集', 'enrichment', 'kegg', 'gsea', 'gsva', '火山', 'volcano', 'maplot', 'ma plot', '棒棒糖'], 'enrichment'),
        (['venn', 'upset'], 'intersection'),
        (['提琴', '箱线', '云雨', '山峰', '密度', 'violin', 'boxplot', 'histogram', 'density', 'beeswarm', 'swarm'], 'distribution'),
        (['dose', 'ic50', 'ec50'], 'dose-response'),
        (['line', 'growth', 'seahorse', 'waveform', 'time series', '拟时序'], 'time-course'),
        (['bar', '柱状'], 'group-comparison'),
        (['相关', 'correlation', '线性拟合', 'regression', 'scatter'], 'association'),
        (['细胞互作', 'network', 'chord'], 'network'),
    ]:
        if any(w in text for w in words):return task
    return 'unclassified'


def index_external(medbio, prism):
    records = []
    for folder in sorted(medbio.iterdir()):
        if not folder.is_dir() or not re.match(r'(?!00_)\d+_', folder.name):continue
        scripts = list(folder.glob('*.R')) + list(folder.glob('*.r'))
        source = '\n'.join(p.read_text(errors='replace') for p in scripts)
        inputs = []
        for p in sorted(folder.iterdir()):
            if p.suffix.lower() not in ['.csv','.tsv','.txt','.rds','.rdata','.xlsx','.xls']:continue
            columns = []
            if p.suffix.lower() in ['.csv','.tsv']:
                with p.open(errors='replace') as stream:
                    columns = next(csv.reader(stream, delimiter='\t' if p.suffix.lower()=='.tsv' else ','), [])
            inputs.append({'file':p.name,'columns':columns,'row_unit':'Requires recipe-specific inspection'})
        packages = sorted(set(re.findall(r'(?:library|require)\(\s*[\"\x27]?([\w.]+)',source)))
        records.append({'key':'medbio/'+folder.name.split('_')[0], 'collection':'MedBioinform',
            'library':'medbio', 'directory':folder.name, 'title':folder.name,
            'task':task_for(folder.name), 'chart':folder.name, 'languages':['R'],
            'designs':['unspecified'], 'input_kind':'unspecified', 'inputs':inputs,
            'contract_reviewed':False, 'scripts':[p.name for p in scripts], 'packages':packages,
            'previews':[p.name for p in folder.iterdir() if p.suffix.lower() in ['.png','.pdf','.tif','.tiff','.jpg']],
            'status':'reference', 'review_note':'Source files and CSV headers inventoried; analysis and native inputs need inspection.',
            'layout':{'tested_placements':[]}, 'source_evidence':{},
            'license':'Source collection terms must be checked before redistribution.'})
    rows = {}
    for line in (gallery.SKILL.parent/'graphpad-prism/references/template_catalog.md').read_text().splitlines():
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if len(cells)==4 and cells[1].endswith('.pzf'):rows[cells[1]]=cells
    for p in sorted(prism.glob('*.pzf')):
        row=rows.get(p.name, ['',p.name,'Filename lead; native table needs inspection','Unknown'])
        records.append({'key':'prism/'+p.name.split('.')[0], 'collection':'Prism',
            'library':'prism','directory':p.name,'title':p.name,'task':task_for(p.name+' '+row[2]),
            'chart':row[2], 'languages':['prism'], 'designs':['unspecified'], 'input_kind':'unspecified',
            'inputs':[{'file':p.name,'columns':[],'row_unit':row[3]}], 'contract_reviewed':False,
            'native_table':{'catalog_description':row[3],'verified':False},
            'status':'reference','review_note':'Native file present; table, analyses and replacement behavior need Prism inspection.',
            'layout':{'tested_placements':[]},'source_evidence':{},'previews':[],
            'license':'Source collection terms must be checked before redistribution.'})
    return {'schema_version':1,'indexed_on':'2026-10-26','records':records}


def load_index():
    records=[]
    overrides=gallery.read_json(CURATION,{})
    code_reviews=gallery.read_json(ASSETS/'implementation-review.json',{}).get('records',{})
    for p in gallery.load_catalog(gallery.CATALOG)['panels']:
        r={**p,'collection':'Publication','title':p['chart'], 'contract_reviewed':bool(p['inputs']),
           'input_kind':'unspecified','layout':{'tested_placements':[]},
           'review_note':'Current source, code and replacement review required before staging.'}
        if 'forest' in r['chart'].lower():r['task']='effect-estimates'
        r.update(overrides.get(r['key'],{}))
        records.append(r)
    records.extend(gallery.read_json(EXTERNAL,{'records':[]})['records'])
    records.extend(gallery.read_json(ASSETS/'code-galleries.json',{'records':[]})['records'])
    records.extend(gallery.read_json(ASSETS/'worked-examples.json',{'records':[]})['records'])
    records.extend(gallery.read_json(ASSETS/'representative-examples.json',{'records':[]})['records'])
    records.extend(gallery.read_json(ASSETS/'native-source-adaptations.json',{'records':[]})['records'])
    records.extend(gallery.read_json(gallery.SKILL/'assets/custom-library/catalog.json',{'records':[]})['records'])
    for r in records:
        r.update(overrides.get(r['key'],{}))
        review = code_reviews.get(r['key'])
        if review:r['code_review'] = review
    return [annotate(r) for r in records]


def load_archives():
    paths = [ASSETS/'worked-examples.json', ASSETS/'representative-examples.json', ASSETS/'native-source-adaptations.json',
             gallery.SKILL/'assets/custom-library/catalog.json']
    return [annotate(r) for path in paths
            for r in gallery.read_json(path,{}).get('superseded_records',[])]


def recommend(records, task, design='unspecified', language='R', query='', kind='unspecified',
              columns=None, chart=None, width_mm=None, limit=3, collection=None, paths=None):
    candidates=[];leads=[]
    terms=set(re.findall(r'[\w]+',query.lower()))
    for r in records:
        if r['status']=='superseded':continue
        if task not in r.get('tasks',[r['task']]) or language not in r['languages']:continue
        if collection and r['collection']!=collection:continue
        if chart and chart.lower() not in r['chart'].lower():continue
        if r['collection']=='Publication' and not chart and not r['automatic_candidate']:continue
        missing=[]
        known=[x for x in r['designs'] if x!='unspecified']
        if design!='unspecified' and design not in known:
            if known:continue
            missing.append('Study-design support needs inspection')
        if kind!='unspecified' and r['input_kind']!=kind:
            if r['input_kind']!='unspecified':continue
            missing.append('Input value type needs inspection')
        if columns is not None:
            required={c for t in r['inputs'] for c in t['columns']}
            if not r['contract_reviewed']:missing.append('Required columns need recipe-specific mapping')
            elif not required.issubset(columns):continue
        ready=r['status']=='reviewed'
        if r.get('code_review',{}).get('state')=='source-adaptation':
            ready=False
            missing.append('Source-bound coordinates or labels need adaptation to the current data; inspect the code-review record')
        if r['collection']=='Publication' and paths is not None:
            folder=gallery.panel_folder(r,paths)
            ready=ready and bool(folder and all(gallery.review_status(folder).values()))
            if not folder:missing.append('Connect the source library to check current files')
        if not ready:missing.append(r['review_note'])
        haystack=' '.join([r['title'],r['chart'],r.get('method',''),r.get('description',''),
                           ' '.join(c for t in r['inputs'] for c in t['columns'])]).lower()
        matches=sorted(t for t in terms if t in haystack)
        tested=r['layout'].get('tested_placements',[])
        fits=width_mm is not None and any(t['width_mm']<=width_mm and t.get('passed') for t in tested)
        layout_note='Verified at this width or smaller' if fits else 'Requested placement needs a render check' if width_mm else 'Set the intended placement before adapting'
        priority=-1 if r['collection']=='Custom' and r['status'] in ['reviewed','source-traced'] else gallery.source_priority(r) if r['collection']=='Publication' else 3
        provenance=gallery.source_label(r) if r['collection']=='Publication' else r['review_note']
        result={**r,'source_priority':priority,'matched_terms':matches,'checks_needed':missing,
                'layout_note':layout_note,'reason':provenance+'. '+('Relevant terms: '+', '.join(matches)+'. ' if matches else '')+layout_note+'.'}
        score=(priority,-len(matches),not fits,len(r['inputs']),r['key'])
        (leads if missing else candidates).append((score,result))
    return {'task':task,'design':design,'language':language,'input_kind':kind,
        'ranking_basis':'Scientific compatibility first. Personal source recipes retain their source and adaptation review states; published sources retain their author-code and data evidence. Query fit and tested placement break ties.',
        'candidates':[r for _,r in sorted(candidates,key=lambda x:x[0])[:limit]],
        'references':[r for _,r in sorted(leads,key=lambda x:x[0])[:limit]],
        'eligible_count':len(candidates),'reference_count':len(leads)}


def write_preview(result,paths,destination):
    cards=[]
    for r in result['candidates'] or result['references']:
        pictures=[]
        if r['collection']=='Publication':
            folder=gallery.panel_folder(r,paths)
            if folder:
                ctx=gallery.read_json(folder/'context.json',{})
                for label,p in [('Original',folder/ctx.get('source_reference_file','original.png')),
                                ('Reproduction',folder/result['language']/'adapt.png')]:
                    pictures.append('<figure><figcaption>'+label+'</figcaption>'+gallery.preview_image(p)+'</figure>')
        elif r['collection'] in ['Worked example','Custom'] and r.get('preview'):
            p=gallery.SKILL/r['preview']
            pictures.append(gallery.preview_image(p))
        elif r.get('preview_url'):
            pictures.append('<img loading="lazy" src="'+html.escape(r['preview_url'],quote=True)+'" alt="'+html.escape(r['title'],quote=True)+'">')
        elif r['library'] in paths:
            root=paths[r['library']]/r['directory']
            png=next((p for p in r.get('previews',[]) if Path(p).suffix.lower() in ['.png','.jpg']),None)
            if png:pictures.append(gallery.preview_image(root/png))
        links=''
        if r.get('source_url'):
            links='<a href="'+html.escape(r['source_url'],quote=True)+'">Source example</a> · <a href="'+html.escape(r['code_url'],quote=True)+'">Plotting code</a>'
        if r.get('doi'):links=f'<a href="https://doi.org/{html.escape(r["doi"],quote=True)}">Paper</a>'
        for a in r.get('source_evidence',{}).get('author_code',[]):
            links+=' · <a href="'+html.escape(a['url'],quote=True)+'">Author code</a>'
        if r['collection']=='Custom' and r.get('script'):
            source=gallery.SKILL/r['script']
            pictures.append('<details><summary>Verbatim original plotting code</summary><pre>'+html.escape(source.read_text())+'</pre></details>')
        cards.append('<article><h2>'+html.escape(r['key']+' · '+r['title'])+'</h2><p>'+html.escape(r['reason'])+'</p>'+links+
            '<p>'+html.escape('; '.join(r['checks_needed']))+'</p><div class="images">'+''.join(pictures)+'</div><details><summary>Inputs, provenance and review</summary><pre>'+html.escape(json.dumps(r,ensure_ascii=False,indent=2))+'</pre></details></article>')
    template=(gallery.SKILL/'assets/publication-gallery/preview.html').read_text()
    page=template.replace('{{task}}',html.escape(result['task']+' · '+result['design']))
    page=page.replace('{{route}}',html.escape(result['ranking_basis']))
    page=page.replace('{{cards}}',''.join(cards) or '<article>No compatible indexed template. Use the standard scientific plotting route.</article>')
    destination.parent.mkdir(parents=True,exist_ok=True);destination.write_text(page)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    index=sub.add_parser('index');index.add_argument('--medbio',type=Path,required=True);index.add_argument('--prism',type=Path,required=True)
    index.add_argument('--output',type=Path,default=EXTERNAL)
    register=sub.add_parser('register');register.add_argument('--id',choices=['medbio','prism'],required=True);register.add_argument('--path',type=Path,required=True)
    dump=sub.add_parser('dump');dump.add_argument('--output',type=Path,required=True)
    search=sub.add_parser('recommend');search.add_argument('--task',choices=TASKS,required=True)
    search.add_argument('--design',choices=['independent','paired','repeated','nested','supplied-results','unspecified'],default='unspecified')
    search.add_argument('--language',choices=['R','python','prism'],default='R');search.add_argument('--query',default='')
    search.add_argument('--kind',choices=['observations','estimates','matrix','curve','unspecified'],default='unspecified')
    search.add_argument('--columns',help='Comma-separated required input column names after mapping; exact names, across input tables.')
    search.add_argument('--chart');search.add_argument('--width-mm',type=float);search.add_argument('--limit',type=int,default=3)
    search.add_argument('--collection',choices=['Custom','Publication','MedBioinform','Prism','Worked example','External code']);search.add_argument('--html',type=Path)
    args=parser.parse_args()
    if args.action=='index':
        result=index_external(args.medbio,args.prism);args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Indexed',len(result['records']),'templates');return
    if args.action=='register':
        path=args.path.expanduser().resolve()
        if not path.is_dir():parser.error('Library path must be an existing directory.')
        config=gallery.read_json(gallery.CONFIG,{'libraries':{}});config['libraries'][args.id]=str(path)
        gallery.CONFIG.parent.mkdir(parents=True,exist_ok=True);gallery.CONFIG.write_text(json.dumps(config,indent=2)+'\n');print('Registered',args.id);return
    records=load_index()
    if args.action=='dump':
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps({'schema_version':1,'records':records},ensure_ascii=False,indent=2)+'\n');print('Exported',len(records),'records');return
    if args.limit<1:parser.error('--limit must be positive.')
    result=recommend(records,args.task,args.design,args.language,args.query,args.kind,
        set(args.columns.split(',')) if args.columns else None,args.chart,args.width_mm,args.limit,args.collection,gallery.library_paths())
    if args.html:write_preview(result,gallery.library_paths(),args.html)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
