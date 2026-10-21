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
tracked = subprocess.check_output(['git', 'ls-files', '-z', 'skills'], cwd=ROOT).decode().split('\0')
for name in filter(None, tracked):
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
gallery = ''.join(f'<figure><a href="skills/scientific-plotting/examples/gallery/{name}.png"><img src="skills/scientific-plotting/examples/gallery/{name}.png" alt="{title}合成数据示例" loading="lazy"></a><figcaption>{title} · 合成数据</figcaption></figure>' for name, title in [('independent','独立组'),('paired','配对'),('repeated','重复测量'),('dose_response','剂量反应'),('survival','存活曲线'),('heatmap','热图')])
p = OUT / 'index.html'
text = p.read_text().replace('{{VERSION}}', version).replace('{{COMMIT}}', commit).replace('{{SKILL_CARDS}}', '\n'.join(cards)).replace('{{NOSCRIPT_GUIDES}}', ''.join(guides)).replace('{{PLOT_CARDS}}',''.join(plot_cards)).replace('{{GALLERY}}', gallery).replace('{{FIRST_CASE}}', html.escape(catalog[0]['example']))
text = text.replace('</main>', '<script type="application/json" id="catalog-data">' + json.dumps(catalog, ensure_ascii=False).replace('</', '<\\/') + '</script></main>')
p.write_text(text)
(OUT / '.nojekyll').touch()
(OUT / 'downloads').mkdir()
with zipfile.ZipFile(OUT / f'downloads/biomed-skill-{version}.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
    for name in filter(None, tracked):
        bundle.write(ROOT / name, name)
    bundle.write(ROOT / 'LICENSE', 'LICENSE')
    bundle.write(ROOT / 'README.md', 'README.md')
print(f'Built {len(catalog)} skill guides, 7 demos and downloadable suite: {OUT}')
