#!/usr/bin/env python3
"""Render an explicit project inventory as an offline HTML dashboard."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('manifest', type=Path)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
record = json.loads(args.manifest.read_text())
output = args.output.resolve()
marker = '<!-- research-project-dashboard -->'
if output.exists() and marker not in output.read_text():
    raise ValueError('Existing HTML is manually owned. Update it directly or choose a preview filename.')


def esc(value):
    return html.escape(str(value), quote=True)


def href(value):
    parts = urlsplit(value)
    if parts.scheme and parts.scheme != 'file':
        if parts.scheme not in ('https', 'http', 'zotero', 'obsidian'):
            raise ValueError(f'Unsupported link scheme: {parts.scheme}')
        return esc(value)
    path = Path(unquote(parts.path))
    target = path if path.is_absolute() else output.parent / path
    if not target.exists():
        raise FileNotFoundError(target)
    base = target.as_uri() if path.is_absolute() else quote(unquote(parts.path), safe='/')
    return esc(base + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else ''))


def link(label, path):
    return f'<a href="{href(path)}">{esc(label)} ↗</a>'


artifacts = record['artifacts']
ids = [a['id'] for a in artifacts]
if len(ids) != len(set(ids)):
    raise ValueError('Artifact IDs must be unique.')
cards = []
for item in artifacts:
    if item['status'] not in ('current', 'draft', 'superseded', 'failed'):
        raise ValueError(f"Unknown artifact status: {item['status']}")
    image = f'<a href="{href(item["path"])}"><img loading="lazy" src="{href(item["thumbnail"])}" alt="{esc(item["title"])}"></a>' if item.get('thumbnail') else '<div class="file-preview">DOCUMENT / DATA</div>'
    links = [link('Open result', item['path'])] + [link(v['label'], v['href']) for v in item.get('links', [])]
    parts = urlsplit(item['path'])
    if not parts.scheme or parts.scheme == 'file':
        folder = str(Path(unquote(parts.path)).parent)
        links.append(link('Directory', folder + '/'))
    cards.append(f'''<article class="artifact" data-status="{esc(item['status'])}" data-kind="{esc(item['kind'])}">
      <div class="preview">{image}</div><div class="card-body"><div class="meta">{esc(item['id'])} · {esc(item['kind'])} <span class="badge">{esc(item['status'])}</span></div>
      <h3>{esc(item['title'])}</h3><p>{esc(item['summary'])}</p><div class="links">{' '.join(links)}</div>
      <p class="path">{esc(item['path'])}</p></div></article>''')

tasks = []
for task in record.get('tasks', []):
    tasks.append(f'''<tr><td>{esc(task['id'])}<br><strong>{link(task['title'], task['source'])}</strong><p>{esc(task['purpose'])}</p></td>
    <td>{esc(task['status'])}<br>{esc(task['owner'])}</td><td>{esc(task['timing'])}<p>{esc(task['dependency'])}</p></td></tr>''')

values = {key: esc(record[key]) for key in ('title', 'updated', 'question', 'finding', 'next_decision', 'coverage')}
values.update(cards='\n'.join(cards), tasks='\n'.join(tasks) or '<tr><td colspan="3">See the linked project records for tasks and scheduling.</td></tr>',
              sources=' '.join(link(v['label'], v['href']) for v in record.get('sources', [])),
              count=str(len(artifacts)),
              kinds=''.join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in sorted({v['kind'] for v in artifacts})))
template = (Path(__file__).resolve().parents[1] / 'assets/dashboard.html').read_text()
page = re.sub(r'\{\{(\w+)\}\}', lambda match: values[match[1]], template)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(page)
print(f'Wrote {output}; {len(artifacts)} artifact records; local targets checked.')
