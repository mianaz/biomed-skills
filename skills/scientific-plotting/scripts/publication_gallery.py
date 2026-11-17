#!/usr/bin/env python3
"""Index local publication panels, find suitable encodings, and copy a template."""
import argparse
import base64
import html
import json
import re
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CATALOG = SKILL / 'assets/publication-gallery/catalog.json'
DESIGN_SUPPORT = SKILL / 'assets/publication-gallery/design-support.json'
SOURCE_EVIDENCE = SKILL / 'assets/publication-gallery/source-evidence.json'
CONFIG = Path.home() / '.config/biomed-skills/publication-gallery.json'
TASKS = ['group-comparison', 'distribution', 'association', 'time-course',
         'dose-response', 'survival', 'matrix', 'enrichment', 'composition',
         'embedding', 'spatial', 'hierarchy', 'flow', 'genomic', 'network',
         'dynamics', 'intersection', 'prediction']
REVIEW_FIELDS = ['visually_reviewed', 'style_reviewed', 'code_second_reviewed',
                 'data_replacement_passed']


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def classify(chart, panel):
    text = chart.lower().replace('_', ' ')
    overrides = {
        'D06-p08': 'group-comparison', 'D11-p02': 'group-comparison',
        'D11-p03': 'group-comparison', 'D11-p04': 'group-comparison',
        'D26-p03': 'distribution', 'D32-p05': 'association',
        'D28-p02': 'association', 'D28-p03': 'hierarchy', 'D36-p04': 'matrix',
    }
    if panel in overrides:
        return overrides[panel]
    for words, task in [
        (['roc curve', 'roc trajector', 'precision recall', 'calibration', 'confusion matric', 'prediction matric', 'predicted correlation'], 'prediction'),
        (['vector field', 'vector-field', 'streamline', 'phase portrait', 'velocity', 'quiver', 'acceleration curvature'], 'dynamics'),
        (['upset', 'venn', 'intersection'], 'intersection'),
        (['network', 'chord', 'connectivity'], 'network'),
        (['spatial'], 'spatial'), (['dendrogram', 'sunburst', 'hierarchical clustering'], 'hierarchy'),
        (['phylogen', 'tree'], 'hierarchy'),
        (['umap', 'embedding', 'pca', 't-sne', 'principal component', 'coordinate map'], 'embedding'),
        (['genomic', 'genome track', 'chromatin', 'metaprofile', 'oncoprint', 'oncoplot', 'coverage track'], 'genomic'),
        (['kaplan', 'survival'], 'survival'), (['dose response', 'dose-response', 'dose combination'], 'dose-response'),
        (['flow cytometry', 'flow histogram'], 'flow'),
        (['longitudinal', 'trajector', 'line plot', 'line-profile', 'decay curve', 'developmental profile', 'regulon response', 'differentiation response'], 'time-course'),
        (['stacked', 'proportion', 'composition', 'pie', 'sankey', 'alluvial'], 'composition'),
        (['volcano', 'enrichment'], 'enrichment'), (['heatmap', 'dot plot', 'matrix', 'matrices', 'bubble', 'radar', 'concentric expression'], 'matrix'),
        (['violin', 'box', 'beeswarm', 'distribution', 'ridge', 'density', 'strip plot', 'quantile-quantile', 'histogram'], 'distribution'),
        (['bar', 'errorbar'], 'group-comparison'), (['scatter', 'forest'], 'association'),
        (['interval', 'coefficient'], 'association'),
    ]:
        if any(word in text for word in words):
            return task
    return 'unclassified'


def review_status(folder):
    review = read_json(folder / 'adapt-review.json', {})
    checks = {key: review.get(key) is True for key in REVIEW_FIELDS}
    checks['accepted'] = review.get('verdict') == 'pass'
    # New batches keep rendered review, source review and execution evidence separate.
    names = ['visual-review.json', 'code-review-2.json', 'replacement-check.json']
    if any((folder / name).exists() for name in names):
        passed = []
        root = folder.parents[1]
        for name in names:
            evidence = read_json(folder / name, {})
            current = True
            for item in evidence.get('observed_files', evidence.get('tested_files', [])):
                path = root / item['file']
                if not path.is_file() or path.stat().st_mtime_ns != item['mtime_ns']:
                    current = False
            if name == 'visual-review.json':
                context = read_json(folder / 'context.json', {})
                reference = (folder / context.get('source_reference_file', 'original.png')).resolve()
                observed = {(root / item['file']).resolve() for item in evidence.get('observed_files', [])}
                current = current and reference in observed
            passed.append(evidence.get('status') == 'pass' and current)
        checks = dict(zip(REVIEW_FIELDS, [passed[0], passed[0], passed[1], passed[2]]))
        checks['accepted'] = all(passed)
    return checks


def make_record(root, entry, library_id):
    panel = entry['id']
    folder = root / 'panels' / panel
    context = read_json(folder / 'context.json', entry)
    method = read_json(folder / 'method.json', {})
    schema = read_json(folder / 'adapt-data/schema.json', {})
    raw_inputs = schema.get('inputs', schema.get('tables', {}))
    if isinstance(raw_inputs, list):
        raw_inputs = {item.get('filename', item.get('file')): item for item in raw_inputs}
    inputs = [{'file': name, 'columns': [column['name'] if isinstance(column, dict) else column
                                       for column in item.get('columns', [])],
               'row_unit': item.get('row_unit', item.get('role', item.get('purpose', 'See input guide.')))}
              for name, item in raw_inputs.items()]
    chart = context.get('chart_type', entry.get('chart_type', ''))
    support = schema.get('design_support', context.get('design_support',
        read_json(DESIGN_SUPPORT, {}).get(f'{library_id}/{panel}', {})))
    task = support.get('task', context.get('task', classify(chart, panel)))
    if task not in TASKS:
        task = 'unclassified'
    checks = review_status(folder)
    languages = [lang for lang, script in [('R', 'adapt.R'), ('python', 'adapt.py')]
                 if (folder / lang / script).exists() and (folder / lang / 'adapt.png').exists()]
    ready = all(checks.values()) and len(languages) == 2 and bool(inputs)
    decorative = any(word in chart.lower() for word in ['radar', 'pie', 'sunburst', 'bubble chart'])
    return {
        'key': f'{library_id}/{panel}', 'library': library_id, 'panel': panel,
        'directory': f'panels/{panel}', 'journal': context.get('journal', entry.get('journal')),
        'doi': context.get('doi', entry.get('doi')), 'figure': str(context.get('figure', entry.get('figure', ''))),
        'source_panel': context.get('original_panel', entry.get('panel', '')),
        'chart': chart, 'task': task,
        'omit_panel_letter': context.get('omit_panel_letter', False),
        'labels': [label['text'] for label in context.get('native_labels', [])
                   if re.search('[a-zA-Z]', label.get('text', ''))],
        'method': method.get('method_family', schema.get('method', entry.get('method_family', chart))),
        'designs': list(dict.fromkeys(support.get('designs', []) + ['unspecified'])),
        'design_basis': support.get('basis', 'Design compatibility is unreviewed; inspect the input contract before adapting this visual reference.'),
        'design_sources': support.get('sources', []),
        'inputs': inputs, 'languages': languages, 'review': checks,
        'status': 'reviewed' if ready else 'pending',
        'automatic_candidate': ready and task != 'unclassified' and not decorative,
        'example_basis': context.get('data_basis', method.get('input_basis',
                            'Image-derived display estimates; not recovered experimental observations.')),
        'author_code': [{key: source[key] for key in ['url', 'commit', 'path', 'mapping_basis', 'figure', 'panel_match_status']
                         if key in source} for source in context.get('author_code', [])],
        'analysis': 'Display supplied values or upstream results; run new analyses in the shared plotting workflow.',
        'input_note': schema.get('input_role', schema.get('replacement_guidance', method.get('interpretation', 'Read the input guide and method record.'))),
    }


def load_catalog(path):
    catalog = read_json(path, {'schema_version': 1, 'panels': []})
    evidence = read_json(SOURCE_EVIDENCE, {})
    for record in catalog['panels']:
        if record['key'] in evidence:
            record['source_evidence'] = evidence[record['key']]
    return catalog


def source_priority(record):
    evidence = record.get('source_evidence', {})
    code = evidence.get('author_code_verified') is True
    data = evidence.get('source_data_verified') is True
    return 0 if code and data else 1 if code else 2 if data else 3


def source_label(record):
    return ['Verified source data + panel-mapped author code',
            'Panel-mapped author code; current data mapping unverified',
            'Verified source data; author code mapping unverified',
            'Visual reproduction; source-data/code verification pending'][source_priority(record)]


def library_paths(explicit=None, library_id=None):
    paths = read_json(CONFIG, {}).get('libraries', {})
    if explicit:
        paths[library_id] = str(Path(explicit).expanduser().resolve())
    return {key: Path(value).expanduser().resolve() for key, value in paths.items()}


def panel_folder(record, paths):
    root = paths.get(record['library'])
    if root is None:
        return None
    root = root.resolve()
    folder = (root / record['directory']).resolve()
    folder.relative_to(root)
    return folder


def recommend(catalog, task, design, query='', language='R', limit=3, chart=None):
    terms = set(re.findall(r'[a-z0-9]+', query.lower()))
    candidates = []
    for record in catalog['panels']:
        if record['task'] != task or design not in record['designs']:
            continue
        if language not in record['languages'] or record['status'] != 'reviewed':
            continue
        if chart:
            if chart.lower() not in record['chart'].lower():
                continue
        elif not record['automatic_candidate']:
            continue
        text = ' '.join([record['chart'], record['method'], record['input_note'],
                         ' '.join(record.get('labels', [])),
                         ' '.join(column for table in record['inputs'] for column in table['columns'])]).lower()
        matched = sorted(terms & set(re.findall(r'[a-z0-9]+', text)))
        candidates.append((len(matched), record, matched))
    candidates.sort(key=lambda item: (source_priority(item[1]), -item[0], len(item[1]['inputs']), item[1]['key']))
    standard = {'paired': 'Matched points with connecting lines; analyze within-unit differences.',
                'repeated': 'Preserve unit IDs and actual times; fit the supported repeated-measure model first.'}.get(
                    design, 'Choose the encoding and analysis from the shared analysis-to-chart and statistics references.')
    if language == 'prism':
        standard = 'Use graphpad-prism and a verified native template; these R/Python sources are visual references.'
    return {'task': task, 'design': design, 'language': language,
            'ranking_basis': 'Filter task, design, format and review first. Among compatible publications prefer verified source data plus panel-mapped author code, then panel-mapped author code, then verified data, then other reproductions. Break ties by query match and fewer input tables.',
            'standard_route': standard,
            'candidates': [{**record, 'matched_terms': matched, 'source_priority': source_priority(record),
                            'reason': f"{source_label(record)}. Matches {task}. {record.get('design_basis', 'Inspect design compatibility in the input contract.')} " +
                                      ('Relevant fields: ' + ', '.join(matched) + '.' if matched else 'Inspect the listed input contract before choosing.')}
                           for _, record, matched in candidates[:limit]]}


def preview_image(path):
    if not path.exists():
        return '<p>Local preview unavailable</p>'
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f'<img src="data:image/png;base64,{encoded}" alt="Panel preview">'


def write_preview(result, paths, destination):
    cards = []
    for record in result['candidates']:
        folder = panel_folder(record, paths)
        images = '<p>Connect the local library to display original and replica images.</p>'
        if folder:
            context = read_json(folder / 'context.json', {})
            original = preview_image(folder / context.get('source_reference_file', 'original.png'))
            replica = preview_image(folder / result['language'] / 'adapt.png')
            images = f"""<div class="images">
              <figure><figcaption>Original</figcaption>{original}</figure>
              <figure><figcaption>{html.escape(result['language'])}</figcaption>{replica}</figure>
            </div>"""
        title = html.escape(record['key'] + ' · ' + record['chart'])
        reason = html.escape(record['reason'])
        doi = html.escape(record['doi'], quote=True)
        citation = html.escape(record['journal'] + ' · ' + record['doi'])
        contract = html.escape(json.dumps(record, ensure_ascii=False, indent=2))
        cards.append(f"""<article><h2>{title}</h2><p>{reason}</p>
          <a href="https://doi.org/{doi}">{citation}</a>{images}
          <details><summary>Input contract and review</summary><pre>{contract}</pre></details>
        </article>""")
    template = (SKILL / 'assets/publication-gallery/preview.html').read_text()
    page = template.replace('{{task}}', html.escape(result['task'] + ' · ' + result['design']))
    page = page.replace('{{route}}', html.escape(result['standard_route']))
    page = page.replace('{{cards}}', ''.join(cards) or '<article>No reviewed publication template matches. Use the standard route above.</article>')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page)


def stage(record, root, destination, language):
    folder = panel_folder(record, {record['library']: root})
    if record['status'] != 'reviewed' or not all(review_status(folder).values()):
        raise ValueError('Current panel review is incomplete; use it as a reference only.')
    script = 'adapt.R' if language == 'R' else 'adapt.py'
    if not (folder / language / script).is_file():
        raise ValueError('Selected language source is unavailable.')
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(folder / 'adapt-data', destination / 'adapt-data')
    (destination / language).mkdir()
    shutil.copy2(folder / language / script, destination / language / script)
    context = read_json(folder / 'context.json', {})
    reference = folder / context.get('source_reference_file', 'original.png')
    if reference.exists():
        shutil.copy2(reference, destination / 'original.png')
    shutil.copy2(folder / 'method.json', destination / 'method.json')
    (destination / 'template.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    (destination / 'USE.md').write_text(
        f"# {record['key']}\n\nSource: https://doi.org/{record['doi']} (figure {record['figure']}, panel {record['source_panel']}).\n\n"
        f"Input provenance: {record.get('example_basis', 'Read the input guide for source provenance.')}\n"
        'Replace the inputs using adapt-data/README.md and schema.json. Compute supported statistics separately.\n'
        'Replace source significance labels, intervals, groups and units with your own results before presenting a new figure.\n'
        'Apply the project palette and Arial/effective-size rules unless original-style replication was requested.\n'
        f'Run from this folder: `{destination}`. The script reads `adapt-data/` relative to this folder.\n'
        'Keep the final plotting inputs and plot object, then inspect the exported figure at its intended placement.\n')
    return {'directory': str(destination), 'working_directory': str(destination),
            'command': ['Rscript' if language == 'R' else 'python3', str(destination / language / script)],
            'next': 'Replace example inputs and annotations, then run the command and inspect the export.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    index = sub.add_parser('index', help='Add or refresh a library in a metadata-only catalog.')
    index.add_argument('--library', type=Path, required=True)
    index.add_argument('--id', required=True)
    index.add_argument('--catalog', type=Path, required=True)
    register = sub.add_parser('register', help='Save a local library path outside the skill package.')
    register.add_argument('--library', type=Path, required=True)
    register.add_argument('--id', required=True)
    search = sub.add_parser('recommend')
    search.add_argument('--task', choices=TASKS, required=True)
    search.add_argument('--design', choices=['independent', 'paired', 'repeated', 'unspecified'], default='unspecified')
    search.add_argument('--query', default='')
    search.add_argument('--language', choices=['R', 'python', 'prism'], default='R')
    search.add_argument('--limit', type=int, default=3)
    search.add_argument('--chart', help='Use a named chart style, including reference-only layouts.')
    search.add_argument('--html', type=Path)
    copy = sub.add_parser('stage', help='Copy reviewed code and example inputs to a new work folder.')
    copy.add_argument('key')
    copy.add_argument('--language', choices=['R', 'python'], default='R')
    copy.add_argument('--output', type=Path, required=True)
    show = sub.add_parser('show')
    show.add_argument('key')
    for command in [search, copy, show]:
        command.add_argument('--catalog', type=Path, default=CATALOG)
        command.add_argument('--library', type=Path, help='Override the selected local library path.')
    args = parser.parse_args()
    if args.action == 'register':
        root = args.library.expanduser().resolve()
        if not (root / 'manifest.json').exists():
            parser.error('Library needs manifest.json and a panels directory.')
        config = read_json(CONFIG, {'libraries': {}})
        config['libraries'][args.id] = str(root)
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        CONFIG.write_text(json.dumps(config, indent=2) + '\n')
        result = {'registered': args.id, 'config': str(CONFIG)}
    elif args.action == 'index':
        root = args.library.resolve()
        manifest = read_json(root / 'manifest.json')
        entries = manifest if isinstance(manifest, list) else manifest['panels']
        records = [make_record(root, entry, args.id) for entry in entries]
        # Only this namespace is refreshed; other libraries remain intact.
        catalog = load_catalog(args.catalog)
        catalog['panels'] = [item for item in catalog['panels'] if item['library'] != args.id] + records
        args.catalog.parent.mkdir(parents=True, exist_ok=True)
        args.catalog.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
        result = {'indexed': len(records), 'reviewed': sum(item['status'] == 'reviewed' for item in records), 'catalog': str(args.catalog)}
    else:
        catalog = load_catalog(args.catalog)
        if args.action == 'recommend':
            if args.limit < 1:
                parser.error('--limit must be positive.')
            result = recommend(catalog, args.task, args.design, args.query, args.language, args.limit, args.chart)
            paths = library_paths(args.library, result['candidates'][0]['library'] if result['candidates'] else None)
            for item in result['candidates']:
                folder = panel_folder(item, paths)
                item['local_available'] = bool(folder and (folder / 'adapt-data/schema.json').exists())
            if args.html:
                write_preview(result, paths, args.html)
        else:
            record = next((item for item in catalog['panels'] if item['key'] == args.key), None)
            if record is None:
                parser.error('Unknown panel key. Search the catalog first.')
            if args.action == 'show':
                result = record
            else:
                root = library_paths(args.library, record['library']).get(record['library'])
                if root is None:
                    parser.error('Connect this library with register or --library before staging.')
                result = stage(record, root, args.output.resolve(), args.language)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
