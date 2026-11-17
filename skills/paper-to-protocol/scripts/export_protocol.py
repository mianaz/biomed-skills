#!/usr/bin/env python3
"""Export a sourced Labmate recipe as Markdown, printable HTML and an import file."""
import argparse
import copy
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re


def export(recipe, output):
    recipe = copy.deepcopy(recipe)
    for key in ('id', 'name', 'ref', 'status'):
        if not isinstance(recipe.get(key), str) or not recipe[key].strip():
            raise ValueError(f'{key} must be a nonempty string')
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', recipe['id']):
        raise ValueError('id must contain only letters, digits, underscores or hyphens')
    if recipe.get('category') != 'protocol':
        raise ValueError('category must be protocol')
    steps = recipe.get('detailedSteps')
    if not isinstance(steps, list) or not steps or not any(not s.get('isHeader') for s in steps if isinstance(s, dict)):
        raise ValueError('detailedSteps must contain at least one action')
    for step in steps:
        if not isinstance(step, dict) or not isinstance(step.get('en'), str) or not step['en'].strip():
            raise ValueError('each step needs nonempty en text')
        if not step.get('isHeader') and (not isinstance(step.get('source'), str) or not step['source'].strip()):
            raise ValueError('each action needs a source locator or explicit proposed/user-supplied label')
    materials = recipe.get('materials', [])
    if not isinstance(materials, list) or any(not isinstance(m, dict) or not isinstance(m.get('name'), str) or not m['name'].strip() for m in materials):
        raise ValueError('materials must be objects with a nonempty name')
    stops = recipe.get('safeStops', [])
    if not isinstance(stops, list):
        raise ValueError('safeStops must be an array')
    for stop in stops:
        index = stop.get('afterStep') if isinstance(stop, dict) else None
        if type(index) is not int or not 0 <= index < len(steps) or steps[index].get('isHeader'):
            raise ValueError('safe stop must point to an action using its zero-based detailedSteps index')
        if not isinstance(stop.get('note'), dict) or not isinstance(stop['note'].get('en'), str) or not stop['note']['en'].strip():
            raise ValueError('safe stop needs note.en')
    for key in ('usage', 'notes'):
        if not isinstance(recipe.get(key), dict) or not isinstance(recipe[key].get('en'), str):
            raise ValueError(f'{key} needs an en string')
    recipe['_isCustom'] = True
    recipe.setdefault('components', [])
    # Both languages display readable text even when no translation was requested.
    recipe['briefSteps'] = [{'en': s['en'], 'zh': s.get('zh') or s['en']} for s in steps if not s.get('isHeader')]
    md = [f"# {recipe['name']}", '', f"Status: {recipe['status']}", '', recipe['usage']['en'], '', f"Source: {recipe['ref']}", '']
    if recipe.get('doi'):
        md += [f"DOI: {recipe['doi']}", '']
    md += ['## Materials and equipment', '']
    for m in materials:
        md += ['- ' + ' '.join(str(m.get(k, '')) for k in ('name', 'amount', 'unit', 'note')).strip()]
    md += ['', '## Procedure', '']
    number = 0
    for i, step in enumerate(steps):
        if step.get('isHeader'):
            md += [f"### {step['en']}", '']
            continue
        number += 1
        extra = '; '.join(str(step[k]) for k in ('time', 'temp') if step.get(k))
        text = step['en'] + (f' ({extra})' if extra else '')
        # Labmate renders en/zh but does not render custom source fields.
        for lang in ('en', 'zh'):
            base = text if lang == 'en' else (step.get(lang) or text)
            step[lang] = f"{base} [Source: {step['source']}]"
        md += [f'{number}. {text}', f"   Source: {step['source']}", '']
        for stop in stops:
            if stop['afterStep'] == i:
                md += [f"   Stop/storage: {stop['note']['en']}", '']
    md += ['## Notes, adaptations and unresolved details', '', recipe['notes']['en'], '']
    markdown = '\n'.join(md)
    html = ['<!doctype html><html lang="en"><meta charset="utf-8">', f"<title>{escape(recipe['name'])}</title>", '<style>body{font:12pt Arial,sans-serif;line-height:1.45;max-width:180mm;margin:18mm auto;color:#111}h1{font-size:22pt}h2{font-size:16pt}h3{font-size:13pt}h1,h2,h3{break-after:avoid}p{white-space:pre-wrap;overflow-wrap:anywhere}.step{break-inside:avoid} @media print{@page{size:auto;margin:16mm}body{margin:0;max-width:none}}</style><body>']
    for block in markdown.strip().split('\n\n'):
        if block.startswith('#'):
            level = len(block) - len(block.lstrip('#'))
            html.append(f'<h{level}>{escape(block[level:].strip())}</h{level}>')
        else:
            html.append(f'<p class="step">{escape(block)}</p>')
    html.append('</body></html>')
    recipe['notes']['en'] = f"Status: {recipe['status']}\n" + recipe['notes']['en']
    recipe['notes'].setdefault('zh', recipe['notes']['en'])
    recipe['usage'].setdefault('zh', recipe['usage']['en'])
    payload = {'schemaVersion': 3, 'exportedAt': datetime.now(timezone.utc).isoformat(), 'data': {'labmate_customProtocols': [recipe]}}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    files = {'protocol.md': markdown, 'protocol.html': '\n'.join(html), 'labmate-import.json': json.dumps(payload, ensure_ascii=False, indent=2) + '\n'}
    for name, content in files.items():
        if (output / name).exists():
            raise FileExistsError(f'{output / name} exists; choose a new output directory')
    for name, content in files.items():
        (output / name).write_text(content, encoding='utf-8')
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('protocol', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    export(json.loads(args.protocol.read_text(encoding='utf-8')), args.output)
    print(f'Written protocol.md, protocol.html and labmate-import.json to {args.output}')
