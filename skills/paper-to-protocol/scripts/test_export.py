"""Run with python3 scripts/test_export.py."""
import copy
import json
from pathlib import Path
import tempfile
from export_protocol import export

example = json.loads((Path(__file__).resolve().parents[1] / 'assets/example.json').read_text())
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    payload = export(example, root / 'valid')
    assert set(payload['data']) == {'labmate_customProtocols'}
    recipe = payload['data']['labmate_customProtocols'][0]
    assert recipe['id'] == example['id'] and recipe['_isCustom']
    assert len(recipe['briefSteps']) == 2
    assert recipe['safeStops'][0]['afterStep'] == 2
    assert 'Source: Teaching example, instruction 1' in recipe['detailedSteps'][1]['en']
    assert '2. Save an unchanged' in (root / 'valid/protocol.md').read_text()
    unsafe = copy.deepcopy(example)
    unsafe['name'] = '<script>alert(1)</script>'
    export(unsafe, root / 'escaped')
    assert '<script>' not in (root / 'escaped/protocol.html').read_text()
    invalid = copy.deepcopy(example)
    invalid['safeStops'][0]['afterStep'] = 0
    try:
        export(invalid, root / 'invalid')
    except ValueError:
        pass
    else:
        raise AssertionError('A section header cannot be a safe-stop action')
    assert 'Source:' not in example['detailedSteps'][1]['en']
print('Protocol export check passed')
