#!/usr/bin/env python3
"""Build the full local plotting atlas from registered libraries and selected originals."""
import argparse
import csv
import io
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import quote

import publication_gallery as gallery
import reference_library as library
from plot_families import GROUPS, LABELS, annotate
from template_groups import organize


def personal_records(folder, recipes):
    selections = gallery.read_json(folder / 'selected-plots.json')
    traces = gallery.read_json(folder / 'source-trace.json')
    selected_to_recipe = {sid:r for r in recipes for sid in r['selection_ids']}
    rows = []
    for selection in selections:
        sid = selection['id']
        trace = traces.get(sid, {})
        recipe = selected_to_recipe.get(sid, {})
        rows.append(annotate({**recipe, 'key':'personal/'+sid, 'selection_id':sid,
            'recipe_key':recipe.get('key', 'personal/'+sid), 'collection':'Personal',
            'library':'personal', 'title':selection['title'], 'project':selection['project'],
            'chart':recipe.get('chart',selection['type']), 'type':selection['type'],
            'task':recipe.get('task',library.task_for(selection['type'])),
            'languages':recipe.get('languages', ['native'] if trace.get('status')=='native' else []),
            'status':recipe.get('status',trace.get('status','pending')),
            'designs':recipe.get('designs',['unspecified']), 'inputs':recipe.get('inputs',[]),
            'source_trace':trace, 'source_selection':selection,
            'description':recipe.get('input_context',trace.get('note','')),
            'preview_path':str(folder/'source-previews'/f'{sid}.png')}))
    return rows


def build(output, personal=None, medbio_editions=None):
    # Import rendering dependencies only for gallery builds, not index/search commands.
    import pymupdf as fitz
    from PIL import Image

    output.mkdir(parents=True, exist_ok=True)
    previews = output/'previews'
    previews.mkdir(exist_ok=True)
    paths = gallery.library_paths()
    rows = library.load_index()
    recipes = [r for r in rows if r['collection']=='Custom']
    if personal:
        personal_rows = personal_records(personal, recipes)
        mapped = {r.get('recipe_key') for r in personal_rows}
        rows = [r for r in rows if r['collection']!='Custom' or r['key'] not in mapped] + personal_rows
    issues = []
    (output/'files').mkdir(exist_ok=True)
    linked = {}

    def local_link(path, label, kind='source'):
        path = Path(path)
        if not path.is_file():
            return None
        path=path.resolve()
        if path not in linked:
            target=output/'files'/f'{len(linked)+1:05d}-{path.name}'
            if target.is_symlink():target.unlink()
            target.symlink_to(path)
            linked[path]=quote(str(target.relative_to(output)),safe='/')
        return {'label':label, 'url':linked[path], 'kind':kind}

    def thumb(path, key):
        if not path or not Path(path).is_file():
            return None
        path = Path(path)
        name = re.sub(r'[^a-zA-Z0-9_-]', '-', key)+'.webp'
        dest = previews/name
        try:
            if path.suffix.lower()=='.pdf':
                with fitz.open(path) as document:
                    pixmap = document[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False)
                    im = Image.open(io.BytesIO(pixmap.tobytes('png')))
            else:
                im = Image.open(path)
            im.thumbnail((840,700))
            if im.mode=='RGBA' or 'transparency' in im.info:
                rgba=im.convert('RGBA')
                im=Image.new('RGB',rgba.size,'white')
                im.paste(rgba,mask=rgba.getchannel('A'))
            im.convert('RGB').save(dest,quality=88)
            return 'previews/'+name
        except (OSError, ValueError, RuntimeError) as error:
            issues.append({'key':key,'file':str(path),'error':str(error)})
            return None

    for r in rows:
        links = []
        image = None
        collection = r['collection']
        if collection=='Personal':
            image = Path(r.pop('preview_path'))
            trace = r['source_trace']
            links.append(local_link(image,'Selected original','image'))
            source = r['source_selection'].get('chosen_source',{})
            if source.get('path'):
                links.append(local_link(source['path'],'Original file','native'))
            if r.get('script'):
                links.append(local_link(gallery.SKILL/r['script'],'R recipe','code'))
            for item in trace.get('sources',[]):
                links.append(local_link(item['path'],Path(item['path']).name,'code'))
            for item in trace.get('inputs',[])+trace.get('native_files',[]):
                path=Path(item['path'])
                links.append(local_link(path if path.is_absolute() else personal/path,item['label'],'data'))
            if r['source_selection'].get('paper'):
                links.append({'label':'Paper','url':r['source_selection']['paper'],'kind':'paper'})
            r['display_status'] = {'verified':'Source code traced','partial':'Version check pending',
                'pending':'Source code pending','native':'Native source'}.get(trace.get('status'),'Source code pending')
        elif collection=='Publication':
            folder = gallery.panel_folder(r,paths)
            if folder and folder.is_dir():
                context = gallery.read_json(folder/'context.json',{})
                image = folder/context.get('source_reference_file','original.png')
                links.append(local_link(image,'Published panel','image'))
                for language,script in [('R','adapt.R'),('python','adapt.py')]:
                    links.append(local_link(folder/language/script,language+' adapter','code'))
                    links.append(local_link(folder/language/'adapt.png',language+' render','image'))
                links.append(local_link(folder/'adapt-data/schema.json','Input schema','data'))
                for item in r.get('inputs',[]):
                    links.append(local_link(folder/'adapt-data'/item['file'],item['file'],'data'))
                r['current_review'] = gallery.review_status(folder)
                r['display_status'] = 'Reviewed reproduction' if all(r['current_review'].values()) else 'Review refresh needed'
                if context.get('status') == 'source-extracted':
                    r['display_status'] = 'Original reference · crop reviewed' if context.get('review',{}).get('crop_visual_review') == 'pass' else 'Original reference · crop review pending'
            else:
                r['display_status'] = 'Source library unavailable'
            if r.get('doi'):
                links.append({'label':'Paper','url':'https://doi.org/'+r['doi'],'kind':'paper'})
            for item in r.get('source_evidence',{}).get('author_code',[]):
                links.append({'label':'Author code','url':item['url'],'kind':'code'})
            r['description'] = r.get('description',r.get('example_basis','Published-panel reproduction.'))
        elif collection in ['MedBioinform','Prism']:
            root = paths.get(r['library'])
            if root:
                folder = root/r['directory']
                if collection=='Prism':
                    links.append(local_link(folder,'Native Prism project','native'))
                else:
                    for name in r.get('scripts',[]):
                        links.append(local_link(folder/name,name,'code'))
                    candidates=[folder/name for name in r.get('previews',[])]
                    candidates=sorted(candidates,key=lambda p:('snipaste' in p.name.lower() or 'screenshot' in p.name.lower(),p.suffix.lower()=='.pdf'))
                    image=next((p for p in candidates if p.is_file()),None)
                    for item in r['inputs']:
                        links.append(local_link(folder/item['file'],item['file'],'data'))
            r['display_status'] = 'Native project' if collection=='Prism' and any(links) else 'Source recipe' if any(links) else 'Source library unavailable'
            r['description'] = r.get('review_note','')
        elif collection in ['Custom','Worked example']:
            image = gallery.SKILL/r['preview'] if r.get('preview') else None
            links.append(local_link(gallery.SKILL/r['script'],'R source','code'))
            if r.get('directory'):
                for name in ['example.csv','replacement.csv','README.md','preview.pdf','plot.rds','estimates.csv'] + [item['file'] for item in r.get('inputs',[])]:
                    kind='native' if name=='plot.rds' else 'image' if name=='preview.pdf' else 'data'
                    links.append(local_link(gallery.SKILL/r['directory']/name,name,kind))
            r['display_status'] = r.get('display_status', 'Reviewed example' if collection=='Worked example' else 'Source code traced')
        elif collection=='External code':
            links=[{'label':'Example and code','url':r['source_url'],'kind':'source'},
                   {'label':'Plotting code','url':r['code_url'],'kind':'code'},
                   {'label':'Full source gallery','url':r['gallery_url'],'kind':'gallery'}]
            r['display_status']='External code checked'
        r['links'] = list({(link['url'],link['kind']):link for link in links if link}.values())
        r['thumbnail'] = thumb(image,r['key']) if image else r.get('preview_url')
        r['preview_note'] = 'Native Prism file; preview available in Prism.' if collection=='Prism' else 'Open the source for the full example.'

    records = [annotate(r) for r in rows]
    if medbio_editions:
        originals={r['key']:r for r in records}
        replaced=gallery.read_json(library.ASSETS/'native-source-adaptations.json',{}).get('replaced_editions',{})
        for edition in gallery.read_json(medbio_editions/'manifest.json')['records']:
            if edition['key'] in replaced:continue
            original=originals[edition['original_key']]
            folder=medbio_editions/edition['directory']
            rendered=gallery.read_json(folder/'render-status.json',{}).get('rendered',False)
            qa=gallery.read_json(folder/'verification.json',{})
            synthetic=gallery.read_json(folder/'synthetic.json',{})
            r={**original,**edition,'collection':'MedBioinform compact','languages':['R'],
               'display_status':('Layout reviewed' if qa.get('visual_reviewed') else 'Rendered; layout review needed') if rendered else 'Layout source prepared; render pending',
               'description':'Appearance edition of '+original['title']+'. '+ ' '.join(edition.get('notes',[])),
               'links':list(original['links']),'edition':dict(edition['edition'])}
            if synthetic:
                r['title']=r['title'].replace(' · compact','')+' · synthetic demo'
                r['data_basis']='synthetic'
                r['synthetic']=synthetic
                r['description']='Synthetic-data demonstration. '+synthetic['adaptation']
                r['display_status']='Synthetic demo · '+('layout reviewed' if qa.get('visual_reviewed') else 'review pending') if rendered else 'Synthetic demo · render pending'
            for path,label,kind in [(folder/'source-edited.R','Edited R source','code'),
                                    (folder/'source-synthetic.R','Synthetic plotting source','code'),
                                    (folder/'synthetic-data.R','Synthetic data generator','code'),
                                    (folder/'synthetic.json','Synthetic data notes','data'),
                                    (folder/'template.R','Run edition','code'),
                                    (medbio_editions/'medbio_layout.R','R layout helper','code'),
                                    (folder/'layout.R','Font and area settings','settings'),
                                    (folder/'plot-native.rds','Native R plot','native'),
                                    (folder/'figures/compact.pdf','Compact PDF','image'),
                                    (folder/'figures/compact.png','Compact PNG','image'),
                                    (folder/'source_data/plot-data.rds','Direct plotting data','data'),
                                    (folder/'verification.json','Size and font checks','data'),
                                    (folder/'render.log','Render log','data'),
                                    (folder/'README.md','Edition notes','data')] + [(q,q.stem.replace('-',' '),'data') for q in sorted((folder/'source_data').glob('*.csv'))] + [(q,'Synthetic inputs: '+q.name,'data') for q in sorted((folder/'synthetic-inputs').glob('*')) if q.is_file()]:
                if not rendered and (kind in ['native','image'] or 'source_data' in path.parts):continue
                link=local_link(path,label,kind)
                if link:r['links'].append(link)
            if rendered and (folder/'layout-measured.csv').is_file():
                measured=next(csv.DictReader((folder/'layout-measured.csv').open()))
                r['edition'].update({k:float(v) for k,v in measured.items()})
            r['edition']['render_note']='Rendered and visually reviewed at the saved size.' if qa.get('visual_reviewed') else qa.get('review_note','Rendered from source; layout review pending.') if rendered else edition['edition']['render_note']
            if synthetic:r['edition']['render_note']='Synthetic data. '+r['edition']['render_note']
            r['verification']=qa
            r['thumbnail']=thumb(folder/'figures/compact.png',r['key']) if rendered else None
            r['preview_note']=r['edition']['render_note']
            records.append(r)
    template_groups=organize(records)
    archives=library.load_archives()
    for r in archives:
        r['display_status']='Archived implementation'
        r['thumbnail']=thumb(gallery.SKILL/r['preview'],r['key']) if r.get('preview') else None
        r['description']=r.get('retirement_reason',r.get('review_note',''))
        r['links']=[link for link in [local_link(gallery.SKILL/r['script'],'Archived R source','code') if r.get('script') else None,
                    local_link(gallery.SKILL/r['preview'],'Archived preview','image') if r.get('preview') else None] if link]
    organize(archives)
    counts = dict(Counter(r['collection'] for r in records))
    external = gallery.read_json(library.ASSETS/'code-galleries.json',{})
    used_recipe_keys={r.get('recipe_key',r['key']) for r in records if r['collection'] in ['Personal','Custom']}
    recipe_groups={r['template_group'] for r in records if r.get('recipe_key',r['key']) in {x['key'] for x in recipes}}
    summary = {'entries':len(records),'archived':len(archives),'collections':counts,
        'template_groups':len(template_groups),
        'cross_collection_groups':sum(len(g['source_collections'])>1 for g in template_groups),
        'medbio_editions':sum(r['collection']=='MedBioinform compact' for r in records),
        'medbio_synthetic':sum(r['collection']=='MedBioinform compact' and r.get('data_basis')=='synthetic' for r in records),
        'medbio_rendered':sum(r['collection']=='MedBioinform compact' and bool(r['thumbnail']) for r in records),
        'medbio_reviewed':sum(r['collection']=='MedBioinform compact' and r.get('verification',{}).get('visual_reviewed',False) for r in records),
        'families':len({r['family'] for r in records}),
        'personal_originals':sum(r['collection']=='Personal' for r in records),
        'personal_source_recipes':len({r['key'] for r in recipes}&used_recipe_keys),
        'personal_recipe_groups':len(recipe_groups),'external_galleries':len(external.get('galleries',[])),
        'previews':sum(bool(r['thumbnail']) for r in records),
        'preview_issues':issues,'statuses':dict(Counter(r['display_status'] for r in records))}
    database = {'schema_version':2,'built_on':date.today().isoformat(),'scope':'All indexed plotting entries, selected originals and supplied compact editions.',
        'summary':summary,'families':LABELS,'merge_groups':GROUPS,
        'template_groups':template_groups,'galleries':external.get('galleries',[]),'records':records,
        'archives':archives}
    # Inventory every linked source after local links resolve; keep render review separate.
    from audit_template_sources import audit
    scan_input=output/'database.json'
    scan_input.write_text(json.dumps(database,ensure_ascii=False))
    source_audit=audit(scan_input,output/'source-audit.json')
    source_reviews={r['key']:r for r in source_audit['records']}
    for r in records:
        scanned=source_reviews[r['key']]
        r['code_review']={k:scanned[k] for k in ['state','source_files','candidate_lines','bounded_domain_lines']}
        r['code_review']['date']=source_audit['date']
        r['code_review']['scope']='Native replacement tests' if scanned['state']=='native-verified' else 'Static source inventory; adaptation review remains specific to new data'
    summary['source_audit']=source_audit['summary']
    (output/'database.json').write_text(json.dumps(database,ensure_ascii=False,indent=2)+'\n')
    fields=['key','title','collection','family','plot_group','template_group','recipe_key','display_status','data_basis','languages','source_url','code_url','code_links','native_links']
    with (output/'database.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for record in records:
            writer.writerow({**{k:'; '.join(record[k]) if isinstance(record.get(k),list) else record.get(k,'') for k in fields},
                             'code_links':'; '.join(l['url'] for l in record['links'] if l['kind']=='code'),
                             'native_links':'; '.join(l['url'] for l in record['links'] if l['kind']=='native')})
    with (output/'templates.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['id','title','representative','variant_count','collections','members'])
        writer.writeheader()
        for group in template_groups:
            writer.writerow({**{k:group[k] for k in ['id','title','representative']},
                             'variant_count':len(group['members']),
                             'collections':'; '.join(group['collections']),'members':'; '.join(group['members'])})
    payload=json.dumps(database,ensure_ascii=False).replace('<','\\u003c')
    page=(gallery.SKILL/'assets/template-database/index.html').read_text().replace('__DATABASE__',payload)
    (output/'index.html').write_text(page)
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--personal-dir',type=Path,help='Private curated-library folder with selected-plots.json and source-trace.json')
    parser.add_argument('--medbio-editions',type=Path,help='Local compact editions folder with manifest.json')
    args=parser.parse_args()
    build(args.output.resolve(),args.personal_dir.resolve() if args.personal_dir else None,
          args.medbio_editions.resolve() if args.medbio_editions else None)
