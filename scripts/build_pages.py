#!/usr/bin/env python3
"""Build the public demo site from tracked skills and explicit teaching examples."""
from pathlib import Path
import html
import json
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ROOT / 'site', OUT)
showcase = json.loads((ROOT / 'site/showcase.json').read_text())
tracked = subprocess.check_output(['git', 'ls-files', '-z', 'skills'], cwd=ROOT).decode().split('\0')
old_pages = ('jinek2012', 'causal-models', 'biomed-icon-library', 'icon-atlas-template')
web_files = [name for name in filter(None, tracked)
             if not any(name.endswith('/' + old + '.html') for old in old_pages)
             and '/examples/gallery/' not in name]
for name in web_files:
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
for name in ['LICENSE', 'README.md']:
    shutil.copy2(ROOT / name, OUT / name)
version = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())['version']
commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip()
catalog = json.loads((ROOT / 'site/catalog.json').read_text())
assert {item['id'] for item in catalog} == {p.parent.name for p in (OUT / 'skills').glob('*/SKILL.md')}
groups = {'writing': '故事与写作', 'figures': '绘图与组图', 'reading': '论文与机制', 'protocols': '方法与交付'}
cards, guides = [], []
for index, item in enumerate(catalog, 1):
    name = item['id']
    cards.append(f'''<a class="skill-card" href="#skill/{name}" data-group="{item['group']}">
<div class="card-head"><span>{groups[item['group']]}</span><span>{index:02}</span></div>
<h3>{html.escape(item['title'])}</h3><span class="skill-id">{name}</span>
<p>{html.escape(item['summary'])}</p><span class="card-foot">输入 · 提示词 · 示例 · 文件 <span>↗</span></span></a>''')
    guide = OUT / f'examples/skills/{name}.md'
    guide.parent.mkdir(parents=True, exist_ok=True)
    guide.write_text(f"# {item['title']}\n\n`{name}`\n\n{item['summary']}\n\n## 输入\n\n" + '\n'.join('- ' + s for s in item['inputs']) + '\n\n## 提示词\n\n' + item['prompt'] + '\n\n## 工作步骤\n\n' + '\n'.join(f'{i}. {s}' for i, s in enumerate(item['steps'], 1)) + '\n\n## 交付物\n\n' + '\n'.join('- ' + s for s in item['outputs']) + '\n\n## 具体示例\n\n' + item['example'] + '\n\n研究案例为虚构教学内容；实际机制演示的文献来源见演示内部。\n\n' + f'[完整技能](https://github.com/mianaz/biomed-skills/blob/main/skills/{name}/SKILL.md)\n')
    guides.append(f'<li><a href="examples/skills/{name}.md">{html.escape(item["title"])}</a></li>')
for script, fixture, destination in [
    ('paper-evidence-map/scripts/render_map.py', 'paper-evidence-map/assets/example.json', 'evidence'),
    ('paper-to-protocol/scripts/export_protocol.py', 'paper-to-protocol/assets/example.json', 'protocol'),
]:
    subprocess.run([sys.executable, str(ROOT / 'skills' / script), str(ROOT / 'skills' / fixture), str(OUT / 'examples' / destination)], check=True)
shutil.copy2(ROOT / 'skills/paper-evidence-map/assets/example.json', OUT / 'examples/evidence/graph.json')
plot_cards = []
for stem, title, description in [
    ('groups', '独立组与计划比较', '每组 6 个独立单位 · 均值与 SD · Welch / Holm'),
    ('paired', '保留供者配对', '按 ID 匹配 · 显示个体变化 · 配对比较'),
    ('trajectory', '时间轨迹与重复单位', '显示个体和组轨迹 · 数据与分析说明随图保存'),
]:
    files = [('pdf', 'PDF'), ('rds', 'RDS'), ('_source.csv', '数据'), ('_caption.txt', '图注')]
    if stem != 'trajectory':
        files.append(('_statistics.csv', '统计'))
    links = ''.join(f'<a download href="examples/tidyplots/{stem}{suffix if suffix.startswith("_") else "." + suffix}">{label} ↓</a>' for suffix, label in files)
    plot_cards.append(f'<article class="plot-card"><a href="examples/tidyplots/{stem}.pdf"><img src="examples/tidyplots/{stem}.png" alt="{title}的实际 R 绘图导出" loading="lazy"></a><div class="plot-meta"><h3>{title}</h3><p>{description}</p><div class="file-links">{links}<a href="skills/scientific-plotting-tidyplots/examples/run.R" download>R 源码 ↓</a></div></div></article>')
icons_root = ROOT / 'skills/scientific-visual-explainer/assets/biomed-icons'
icon_catalog = json.loads((icons_root / 'catalog.json').read_text())
assert icon_catalog['version'] == showcase['visual_revision']
current_icons = [icon for icon in icon_catalog['icons'] if icon['category'] in showcase['icon_families']]
current_icons.sort(key=lambda icon: showcase['icon_families'].index(icon['category']))
icon_cards = []
for icon in current_icons:
    generated = icon['provenance']['mode'] == 'built-in-imagegen-traced'
    base = 'skills/scientific-visual-explainer/assets/biomed-icons/'
    raster = icon['provenance']['source'] if generated else icon['preview']
    raster_label = '原始生成图' if generated else 'PNG 预览'
    anchors = ', '.join(icon['anchors'])
    icon_cards.append(f"""<article class="current-icon-card"><span class="small-label">{html.escape(icon['category'])} · v{showcase['visual_revision']}</span><h2>{html.escape(icon.get('label_zh', icon['label']))}</h2><span class="skill-id">{html.escape(icon['id'])}</span><div class="icon-comparison"><figure><img loading="lazy" src="{base + raster}" alt="{html.escape(icon['label'])}{raster_label}"><figcaption>{raster_label}</figcaption></figure><figure><img loading="lazy" src="{base + icon['file']}" alt="{html.escape(icon['label'])}当前 SVG"><figcaption>当前可编辑 SVG</figcaption></figure></div><p>{html.escape(icon.get('description_zh', icon.get('description', '')))}</p><details><summary>部件、锚点与适用范围</summary><p>{html.escape(anchors)}</p><p>{html.escape(icon.get('scope', 'Teaching schematic.'))}</p></details><div class="file-links"><a download href="{base + icon['file']}">SVG ↓</a><a download href="{base + raster}">{raster_label} ↓</a><a href="{base + icon['category']}/manifest.json">来源与元数据 ↗</a></div></article>""")
(OUT / 'examples/current-icons.json').write_text(json.dumps({'version': showcase['visual_revision'], 'icons': current_icons}, ensure_ascii=False, indent=2) + '\n')
icons_page = (OUT / 'icons.html').read_text().replace('{{VISUAL_REVISION}}', showcase['visual_revision']).replace('{{ICON_COUNT}}', str(len(current_icons))).replace('{{ICON_CARDS}}', ''.join(icon_cards))
(OUT / 'icons.html').write_text(icons_page)
p = OUT / 'index.html'
text = p.read_text().replace('{{VERSION}}', version).replace('{{COMMIT}}', commit).replace('{{SKILL_CARDS}}', '\n'.join(cards)).replace('{{NOSCRIPT_GUIDES}}', ''.join(guides)).replace('{{PLOT_CARDS}}',''.join(plot_cards)).replace('{{FIRST_CASE}}', html.escape(catalog[0]['example']))
text = text.replace('</main>', '<script type="application/json" id="catalog-data">' + json.dumps(catalog, ensure_ascii=False).replace('</', '<\\/') + '</script></main>')
p.write_text(text)
(OUT / '.nojekyll').touch()
(OUT / 'downloads').mkdir()
with zipfile.ZipFile(OUT / f'downloads/biomed-skill-{version}.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    for name in filter(None, tracked):
        bundle.write(ROOT / name, name)
    bundle.write(ROOT / 'LICENSE', 'LICENSE')
    bundle.write(ROOT / 'README.md', 'README.md')
with zipfile.ZipFile(OUT / 'downloads/current-examples.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    assets = ROOT / 'skills/scientific-visual-explainer/assets'
    for name in ['tgfb-generated.html', 'egfr-generated.html', 'tgfb-storyboard.md']:
        bundle.write(assets / name, 'mechanisms/' + name)
    for family in showcase['icon_families']:
        for source in sorted((icons_root / family).rglob('*')):
            if source.is_file():
                bundle.write(source, 'icons/' + source.relative_to(icons_root).as_posix())
    bundle.writestr('icons/current-icons.json', json.dumps({'version': showcase['visual_revision'], 'icons': current_icons}, ensure_ascii=False, indent=2))
    for source in sorted((ROOT / 'site/examples/tidyplots').iterdir()):
        bundle.write(source, 'plots/outputs/' + source.name)
    plotting = ROOT / 'skills/scientific-plotting'
    for name in ['scripts/compact.R', 'examples/groups.csv', 'examples/paired.csv', 'examples/trajectory.csv']:
        bundle.write(plotting / name, 'plots/scientific-plotting/' + name)
    for name in ['scripts/tidyplots.R', 'examples/run.R']:
        bundle.write(ROOT / 'skills/scientific-plotting-tidyplots' / name, 'plots/scientific-plotting-tidyplots/' + name)
    bundle.write(ROOT / 'LICENSE', 'LICENSE')
    bundle.writestr('README.md', f"""# Current showcase examples

Mechanism assets: v{showcase['visual_revision']}, continuous contours and unified scene line weights.
Open mechanisms/tgfb-generated.html or mechanisms/egfr-generated.html directly.
The HTML files embed their SVGs, model, runtime and source references.
icons/ contains the {len(current_icons)} editable SVG assets used by the current showcase,
including 18 native generic primitives and 24 generated-and-traced mechanism assets.
Native primitives include vector source and PNG previews; generated assets retain
original PNGs and prompts. Every family includes metadata. Geometry is illustrative.
Open icons/generic-primitives/preview.html for the generic picker and label editor.
The TGFbeta lesson also embeds its nuclear-pore support artwork.

plots/outputs/ contains the current synthetic teaching plots, source tables,
statistics and editable R objects. With the R dependencies installed, rerun:

    Rscript --vanilla plots/scientific-plotting-tidyplots/examples/run.R new-plots

Keep both plotting directories together. The complete skill installation is a
separate download. All plotting data are synthetic teaching examples.
""")
print(f'Built {len(catalog)} skill guides, current mechanism demos, a {len(current_icons)}-icon gallery and downloadable suite: {OUT}')
