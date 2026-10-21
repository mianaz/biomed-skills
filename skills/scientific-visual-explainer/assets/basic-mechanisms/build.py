"""Embed the basic-mode symbols, scene models and shared renderer into offline HTML."""
from pathlib import Path
import json
f=Path(__file__).resolve().parent
library=f.parent/'biomed-icons'
icons=json.loads((library/'generic-primitives/manifest.json').read_text())
icons=[e for e in icons if e.get('status')!='archived']
for e in icons:e['svg']=(library/e['file']).read_text()
page=(f/'template.html').read_text().replace('/*ICON_DATA*/',json.dumps(icons,ensure_ascii=False)).replace('/*MODEL_DATA*/',(f/'models.json').read_text()).replace('/*RUNTIME*/',(f/'player.js').read_text())
(f/'index.html').write_text(page)
print('Built three basic mechanism figures and animations.')
