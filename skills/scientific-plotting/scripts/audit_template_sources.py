#!/usr/bin/env python3
"""Inventory source-code reuse risks; static findings are leads, not render reviews."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

PATTERNS = {
    'fixed_axis': r'\b(?:limits|breaks|xlim|ylim|set_xlim|set_ylim|set_xticks|set_yticks)\s*(?:=|\()\s*(?:c\s*\(|\[)\s*(-?[\d.eE+]+(?:\s*,\s*-?[\d.eE+]+)+)\s*[)\]]',
    'fixed_annotation': r'(?<![\w.])(?:annotate|geom_text|geom_label|geom_segment|ax\.text|ax\.annotate)\s*\(.*?\b(?:x|y|xend|yend)\s*=\s*-?\d',
    'positional_matrix_slice': r'\[\s*,\s*\d+\s*:\s*\d+\s*\]',
    'named_group_patch': r'\bifelse\([^\n]*(?:\$group|\$condition|\$treatment)\s*==\s*[\x27\x22]',
    'absolute_data_offset': r'\b(?:max|min)\([^\n]*?\)\s*[+-]\s*\d+(?:\.\d+)?',
    'literal_stat_label': r'\b(?:label|annotation|pval)\s*(?:<-|=)\s*[\x27\x22](?:\*+|P\s*[<=>]\s*0\.|[<=>]\s*0\.)',
}


def scan_file(path):
    findings = []
    for number, line in enumerate(Path(path).read_text(errors='replace').splitlines(), 1):
        code = line.strip()
        if not code or code.startswith('#'):
            continue
        for kind, pattern in PATTERNS.items():
            match = re.search(pattern, code, re.I)
            if not match:
                continue
            # Probability and correlation domains are scientific bounds.
            if kind == 'fixed_axis':
                values = [float(x.strip()) for x in match.group(1).split(',')]
                if min(values) >= -1 and max(values) <= 1:
                    kind = 'bounded_domain'
            findings.append({'line': number, 'kind': kind, 'code': code[:360]})
    return findings


def audit(database, output):
    database = Path(database)
    db = json.loads(database.read_text())
    cache = {}
    records = []
    for record in db['records']:
        sources = []
        for link in record.get('links', []):
            if link['kind'] != 'code' or not link['url'].startswith('files/'):
                continue
            path = (database.parent / unquote(link['url'])).resolve()
            if not path.is_file() or path.suffix.lower() not in ['.r', '.py']:
                continue
            if path.name in ['medbio_layout.R', 'layout.R', 'synthetic-data.R']:
                continue
            if path not in cache:
                cache[path] = scan_file(path)
            sources.append({'file': str(path), 'label': link['label'], 'url': link['url'],
                            'findings': cache[path]})
        optimized = record.get('review', {}).get('native_controls', False)
        findings = [x for source in sources for x in source['findings']]
        risks = [x for x in findings if x['kind'] != 'bounded_domain']
        state = ('native-verified' if optimized else 'native-project' if record['collection'] == 'Prism'
                 else 'source-adaptation' if risks else 'source-inspection' if sources else 'source-unavailable')
        records.append({'key': record['key'], 'state': state, 'source_files': len(sources),
                        'candidate_lines': len(risks), 'bounded_domain_lines': len(findings) - len(risks),
                        'sources': sources})
    result = {'date': '2026-11-05',
              'scope': 'All indexed entries; available local R/Python code scanned. Native verification is separate from static source inventory.',
              'limitations': 'Candidate lines can encode intentional publication geometry or valid study choices. Inspect the linked source and current inputs before adaptation; a clean scan does not establish adaptability.',
              'summary': {'entries': len(records), 'unique_scripts': len(cache),
                          'entries_with_local_code': sum(bool(r['sources']) for r in records),
                          'states': dict(Counter(r['state'] for r in records))},
              'records': records}
    Path(output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.database, args.output)['summary']))
