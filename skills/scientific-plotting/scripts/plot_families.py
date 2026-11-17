"""Browsing families; original implementations and review states stay separate."""
import json
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/template-database'
GROUPS = json.loads((ASSETS / 'groups.json').read_text())['groups']
GROUP_BY_KEY = {key: group for group in GROUPS for key in group['members']}
VISUAL_FAMILIES = json.loads((ASSETS / 'visual-families.json').read_text())['records']

LABELS = {
    'mean-bars': 'Mean bars, intervals and observations',
    'grouped-bars': 'Grouped and factorial bars', 'plain-bars': 'Bars and ranked values',
    'ranked-scores':'Ranked scores', 'genetic-construct':'Genetic constructs',
    'paired': 'Paired observations', 'point-interval': 'Points and uncertainty intervals',
    'boxplot': 'Boxplots', 'violin': 'Violin and box overlays',
    'raincloud': 'Raincloud distributions', 'ridgeline': 'Density ridges',
    'ecdf': 'Cumulative distributions', 'histogram': 'Histograms',
    'density': 'Density curves', 'strip': 'Strip and beeswarm plots',
    'scatter': 'Scatter plots', 'regression': 'Association and fitted trends',
    'hexbin': 'Binned density maps', 'density-2d': 'Density contours',
    'continuous-heatmap': 'Continuous heatmaps', 'annotated-heatmap': 'Annotated and split heatmaps',
    'correlation-heatmap': 'Correlation matrices', 'dot-matrix': 'Dot and bubble matrices',
    'oncoprint': 'Alteration matrices', 'volcano': 'Volcano plots',
    'ma': 'MA plots', 'enrichment-bars': 'Enrichment and NES bars',
    'gsea-arrows': 'GSEA bars with direction arrows', 'enrichment-ratio': 'NES and gene-ratio overlays',
    'enrichment': 'Enrichment profiles and maps', 'forest': 'Forest plots',
    'line': 'Lines and trajectories', 'line-ribbon': 'Lines with uncertainty bands',
    'dose-response': 'Dose-response curves', 'kaplan-meier': 'Kaplan–Meier survival',
    'cumulative-incidence': 'Cumulative incidence', 'stacked-bars': 'Stacked composition bars',
    'stacked-area': 'Stacked area and stream plots', 'pie': 'Pie and donut charts',
    'waffle': 'Waffle charts', 'ternary': 'Ternary plots', 'alluvial': 'Alluvial and Sankey flows',
    'chord': 'Chord diagrams', 'network': 'Networks', 'upset': 'UpSet intersections',
    'venn': 'Venn diagrams', 'embedding': 'Embeddings and projections',
    'spatial': 'Spatial maps', 'genomic-tracks': 'Genomic tracks and gene structures',
    'manhattan': 'Manhattan plots', 'tree': 'Trees and hierarchies',
    'roc-pr': 'ROC and precision–recall', 'calibration': 'Calibration and model diagnostics',
    'flow': 'Flow cytometry', 'dynamics': 'Vector fields and dynamics',
    'radar': 'Radar and radial summaries', 'lollipop': 'Lollipop and ranked effects',
    'other': 'Other specialized plots'
}

CUSTOM = {
    'ternary-ar-neuro':'ternary',
    'pygo2-gsea-highlight-arrows':'gsea-arrows', 'pygo2-gsea-category-arrows':'gsea-arrows',
    'pygo2-arrow-volcano':'volcano', 'klf4-regulatory-volcano':'volcano',
    'gsea-arrow-fdr-fixed':'gsea-arrows', 'gsea-arrow-fdr-top5':'gsea-arrows',
    'gsea-arrow-database-top10':'gsea-arrows', 'gsea-nes-ratio-overlay':'enrichment-ratio',
    'pathway-specimen-heatmap':'annotated-heatmap','promoter-beta-heatmap':'annotated-heatmap',
    'program-ecdf':'ecdf','binary-alluvial':'alluvial','rppa-landscape':'plain-bars',
    'alteration-frequency':'plain-bars','captured-fraction-bars':'plain-bars',
    'paired-promoter-beeswarm':'paired','wnt-grouped-bars':'grouped-bars',
    'malignant-density':'ridgeline','bootstrap-ridgeline':'ridgeline',
    'dnpc-box-rug':'boxplot','scop-module-violin':'violin','scop-tcell-violin':'violin',
    'exhaustion-violin-box':'violin','scop-celltype-umap':'embedding','scop-feature-umap':'embedding'
}

RULES = [
    ('cumulative-incidence', r'competing|cumulative incidence'),
    ('roc-pr', r'\broc\b|precision.?recall|\bauroc\b'),
    ('calibration', r'calibration|confusion|diagnostic'),
    ('kaplan-meier', r'kaplan|survival|生存'),
    ('dose-response', r'dose.?response|ic50|ec50|dose.combination'),
    ('flow', r'flow cytometr|facs|flow histogram'),
    ('paired', r'\bpaired\b|before.?after|matched.observation|配对'),
    ('volcano', r'volcano|火山'), ('ma', r'\bma plot\b|\bmaplot\b'),
    ('oncoprint', r'oncoprint|oncoplot|alteration matrix|mutation landscape'),
    ('manhattan', r'manhattan'), ('genomic-tracks', r'genomic|chromatin|genome|gene track|gene structure|coverage track'),
    ('correlation-heatmap', r'correlat.*heatmap|correlogram|correlation matrix|相关.*热图'),
    ('upset', r'upset|intersection'), ('venn', r'venn|veen'),
    ('chord', r'chord'), ('alluvial', r'alluvial|sankey|桑基'),
    ('forest', r'forest|森林'), ('ecdf', r'ecdf|cumulative.*(?:distribut|frequency)'),
    ('raincloud', r'raincloud|云雨'), ('ridgeline', r'ridge|山峰'),
    ('violin', r'violin|提琴'), ('boxplot', r'boxplot|box plot|box and|box-and|箱线'),
    ('stacked-area', r'stacked area|streamgraph|stream chart'),
    ('stacked-bars', r'stacked|composition.*bar|proportion.*bar|堆叠'),
    ('pie', r'\bpie\b|donut|doughnut'), ('waffle', r'waffle'), ('ternary', r'ternary'),
    ('tree', r'dendro|phylogen|hierarch|\btree\b|treemap|sunburst'),
    ('radar', r'radar|spider|radial'), ('network', r'network|connectivity|网络'),
    ('embedding', r'umap|t.?sne|embedding|\bpca\b|principal component|coordinate map'),
    ('spatial', r'spatial|tissue map'), ('dynamics', r'vector.field|quiver|phase portrait|velocity|streamline'),
    ('dot-matrix', r'dot.?plot|dot matrix|bubble|气泡'),
    ('annotated-heatmap', r'annotat.*(?:heatmap|matrix)|split.*heatmap|specimen.*heatmap|complexheatmap'),
    ('continuous-heatmap', r'heatmap|heat map|matrix|matrices|热图'),
    ('gsea-arrows', r'(?:gsea|enrichment).*arrow'),
    ('enrichment-ratio', r'(?:nes|enrichment).*ratio.*(?:overlay|line)'),
    ('enrichment-bars', r'(?:gsea|nes|enrichment|富集).*bar|diverging'),
    ('enrichment', r'enrichment|gsea|富集'),
    ('hexbin', r'hexbin|hexagonal|binned|2d bin'),
    ('density-2d', r'contour|2d density|density 2d|two.dimensional density'),
    ('histogram', r'histogram|直方'), ('density', r'density|密度'),
    ('strip', r'strip|beeswarm|swarm'), ('lollipop', r'lollipop|棒棒糖'),
    ('regression', r'regression|fitted|correlation|相关|线性拟合'),
    ('line-ribbon', r'confidence band|error envelope|uncertainty band|ribbon|ci band'),
    ('line', r'line|trajectory|longitudinal|time.course|growth curve|trend|profile'),
    ('grouped-bars', r'grouped.*bar|factor.*bar|多组.*柱'),
    ('mean-bars', r'bar.*(?:point|scatter|error|interval|mean)|mean.*bar'),
    ('plain-bars', r'bar|柱'), ('point-interval', r'errorbar|interval|point.range'),
    ('scatter', r'scatter|散点')
]

TASK_FAMILY = {'matrix':'continuous-heatmap','enrichment':'enrichment','association':'scatter',
    'group-comparison':'point-interval','time-course':'line','effect-estimates':'forest',
    'distribution':'density','composition':'stacked-bars','prediction':'calibration',
    'genomic':'genomic-tracks','hierarchy':'tree','intersection':'upset',
    'survival':'kaplan-meier','dose-response':'dose-response','network':'network',
    'flow':'flow','embedding':'embedding','spatial':'spatial','dynamics':'dynamics'}

def family_for(record):
    if record['key'] in VISUAL_FAMILIES:
        return VISUAL_FAMILIES[record['key']]
    if record.get('family') in LABELS:
        return record['family']
    recipe = record.get('recipe_key', record['key']).split('/')[-1]
    if recipe in CUSTOM:
        return CUSTOM[recipe]
    text = ' '.join(str(record.get(k, '')) for k in ['chart', 'title', 'type']).lower().replace('_', ' ')
    for family, pattern in RULES:
        if re.search(pattern, text):
            return family
    return TASK_FAMILY.get(record.get('task'), 'other')

def annotate(record):
    family = family_for(record)
    group = GROUP_BY_KEY.get(record.get('recipe_key', record['key']))
    return {**record, 'family':family, 'family_title':LABELS[family],
            'template_group':group['id'] if group else record.get('recipe_key',record['key'])}
