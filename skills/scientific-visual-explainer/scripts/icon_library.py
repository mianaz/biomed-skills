"""Search the packaged icons and an optional, local reference-derived registry."""
from pathlib import Path
import argparse
import json

SKILL = Path(__file__).resolve().parents[1]
PACKAGE = SKILL.parents[1]
ICON_ROOT = SKILL / 'assets' / 'biomed-icons'


def load_library(include_archived=False):
    assets = []
    for icon in json.loads((ICON_ROOT / 'catalog.json').read_text())['icons']:
        assets.append({**icon, 'key': 'core:' + icon['id'], 'collection': 'core',
                       'file': str((ICON_ROOT / icon['file']).relative_to(PACKAGE)),
                       'status': icon.get('status', 'registered')})
    local = ICON_ROOT / 'local-registry.json'
    if local.exists():
        assets.extend(json.loads(local.read_text())['assets'])
    return [a for a in assets if include_archived or a['status'] != 'archived']


def search(assets, query):
    terms = query.casefold().split()
    return [a for a in assets if all(t in ' '.join(str(a.get(k, '')) for k in
            ('id', 'key', 'label', 'label_zh', 'category', 'family', 'keywords', 'aliases')).casefold() for t in terms)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--collection', choices=['core', 'accepted', 'downloads'])
    parser.add_argument('--include-archived', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    results = search(load_library(args.include_archived), args.query)
    if args.collection:
        results = [a for a in results if a['collection'] == args.collection]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for a in results:
            print(f"{a['key']}\t{a['status']}\t{a.get('label_zh', a['label'])}\t{PACKAGE / a['file']}")
