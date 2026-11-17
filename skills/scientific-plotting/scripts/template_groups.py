"""Group matching chart structures across collections, retaining every source variant."""
import re
from collections import defaultdict

from plot_families import LABELS


# Source-code inspection resolves misleading folder names in the MedBioinform series.
MEDBIO = {
    '01':'correlation-pies', '02':'scatter-sized', '03':'kaplan-meier',
    '04':'feature-embedding', '05':'embedding-composite', '06':'composition-enrichment',
    '07':'heatmap-enrichment', '08':'polar-volcano', '09':'annotated-heatmap',
    '10':'violin', '11':'embedding-composite', '12':'embedding-composite', '13':'embedding-contours',
    '14':'embedding', '15':'raincloud', '16':'dot-matrix', '17':'heatmap-composite',
    '18':'split-violin', '19':'composition-composite', '20':'stacked-bars', '21':'dot-matrix',
    '22':'polar-volcano', '23':'trajectory-heatmap', '24':'density',
    '25':'feature-density', '26':'correlation-heatmap', '27':'feature-density',
    '28':'heatmap-enrichment', '29':'circular-heatmap', '30':'dot-matrix',
    '31':'enrichment-dots', '32':'radial-bars', '33':'enrichment-rings',
    '34':'enrichment-lollipop', '35':'chord', '36':'enrichment-bars',
    '37':'diverging-lollipop', '38':'gsea-profile', '39':'ridgeline',
    '40':'diverging-lollipop', '41':'gsea-profile', '42':'gsea-heatmap',
    '43':'diverging-bars', '44':'enrichment-bars', '45':'enrichment-bars',
    '46':'enrichment-bars', '47':'correlation-network', '48':'ma',
    '49':'pca', '50':'venn', '51':'volcano', '52':'annotated-heatmap',
    '53':'boxplot', '54':'enrichment-dots', '55':'boxplot', '56':'ma',
    '57':'raincloud', '58':'enrichment-ratio', '59':'volcano', '60':'volcano',
    '61':'stacked-bars', '62':'rotated-volcano', '63':'split-volcano',
    '64':'diverging-lollipop', '65':'diverging-lollipop', '66':'split-cell-heatmap',
    '67':'regression', '68':'regression-marginals', '69':'enrichment-lollipop',
    '70':'composition-composite', '71':'diverging-bars', '72':'enrichment-dots',
    '73':'violin', '74':'embedding-composite', '75':'volcano-gsea', '76':'volcano',
    '77':'dot-matrix', '78':'enrichment-lollipop', '79':'enrichment-tree',
    '80':'scatter-sized', '81':'annotated-heatmap', '82':'split-violin',
    '83':'ridgeline', '84':'ridgeline'
}

SPECIAL = {
    'correlation-pies':('Correlation matrices with pie glyphs','correlation-heatmap'),
    'feature-embedding':('Embeddings colored by a continuous feature','embedding'),
    'embedding-contours':('Embeddings with group outlines','embedding'),
    'embedding-composite':('Embeddings with summary panels','embedding'),
    'pca':('PCA scores and biplots','embedding'),
    'feature-density':('Feature-density maps on embeddings','embedding'),
    'composition-enrichment':('Composition with enrichment summaries','stacked-bars'),
    'composition-composite':('Composition bars with category comparisons','stacked-bars'),
    'heatmap-enrichment':('Heatmaps with linked enrichment panels','annotated-heatmap'),
    'heatmap-composite':('Heatmaps with linked quantitative tracks','annotated-heatmap'),
    'trajectory-heatmap':('Trajectory heatmaps with expression profiles','annotated-heatmap'),
    'circular-heatmap':('Circular heatmaps','continuous-heatmap'),
    'split-cell-heatmap':('Heatmaps with two values per cell','continuous-heatmap'),
    'binary-heatmap':('Binary and categorical matrices','continuous-heatmap'),
    'confusion-matrix':('Confusion matrices','calibration'),
    'correlation-network':('Correlation matrices with network links','correlation-heatmap'),
    'enrichment-dots':('Enrichment dots: effect, size and significance','dot-matrix'),
    'enrichment-lollipop':('Pathway lollipops and comet plots','lollipop'),
    'diverging-lollipop':('Diverging lollipop plots','lollipop'),
    'diverging-bars':('Diverging effect and enrichment bars','enrichment-bars'),
    'radial-bars':('Radial bar plots','radar'),
    'enrichment-rings':('Concentric enrichment summaries','enrichment'),
    'gsea-profile':('GSEA running-score curves','enrichment'),
    'gsea-heatmap':('GSEA curves with linked expression heatmaps','enrichment'),
    'enrichment-tree':('Enrichment trees with linked bars','tree'),
    'polar-volcano':('Circular volcano plots by group','volcano'),
    'rotated-volcano':('Rotated volcano plots','volcano'),
    'split-volcano':('Split volcano plots with central labels','volcano'),
    'volcano-gsea':('Volcano plots with linked GSEA curves','volcano'),
    'split-violin':('Split and mirrored violins','violin'),
    'regression-marginals':('Regression with marginal distributions','regression'),
    'scatter-marginals':('Scatter with marginal distributions','scatter'),
    'scatter-matrix':('Scatterplot matrices','scatter'),
    'scatter-sized':('Scatter with color and size encodings','scatter'),
    'qq':('Quantile–quantile plots','scatter'),
    'metaprofile-heatmap':('Genomic metaprofiles with linked heatmaps','genomic-tracks'),
    'mass-spectrum':('Mass spectra','line'),
    'tree-bars':('Trees with linked quantitative bars','tree'),
    'matrix-scatter':('Dot matrices with linked scatter panels','dot-matrix'),
    'sunburst':('Sunburst hierarchies','tree'),
    'treemap':('Treemaps','tree'),
    'roc':'ROC curves', 'pr':'Precision–recall curves',
}
SPECIAL['roc']=(SPECIAL['roc'],'roc-pr')
SPECIAL['pr']=(SPECIAL['pr'],'roc-pr')


def group_for(record):
    key=record.get('original_key',record['key'])
    if key.startswith('medbio/'):
        return MEDBIO[key.split('/')[-1]]
    text=' '.join(str(record.get(k,'')) for k in ['chart','title']).lower().replace('_',' ')
    family=record['family']
    if family=='ternary':return 'ternary'
    patterns=[
        ('raincloud',r'rain.?cloud|cloud.?rain|云雨'),
        ('point-interval',r'beeswarm.*interval'),
        ('ranked-scores',r'ranked.enhancer signal'),
        ('tree-bars',r'(?:phylogeny|tree).*(?:gene.family bars|linked bars)'),
        ('matrix-scatter',r'dot.matrix and scatter'),
        ('polar-volcano',r'(?:circular|polar|环形).*volcano|volcano.*(?:circular|polar)'),
        ('volcano-gsea',r'volcano.*gsea'),
        ('gsea-heatmap',r'gsea.*heatmap'),
        ('metaprofile-heatmap',r'(?:metaprofile|gene.body).*heatmap'),
        ('trajectory-heatmap',r'(?:trajectory|pseudotime).*heatmap|heatmap.*density profiles'),
        ('heatmap-composite',r'heatmap.*linked quantitative tracks'),
        ('heatmap-enrichment',r'(?:heatmap|matrix).*marginal enrichment|heatmap.*pathway summary'),
        ('circular-heatmap',r'(?:circular|concentric).*(?:heatmap|matrix|expression)'),
        ('split-cell-heatmap',r'triangular matrix|split.cell'),
        ('correlation-heatmap',r'correlation (?:heatmap|matri)|correlat.*heatmap'),
        ('confusion-matrix',r'confusion'),
        ('scatter-matrix',r'scatterplot matrix|scatter.*matrix|pairplot'),
        ('qq',r'q.?q |quantile.quantile'),
        ('scatter-marginals',r'scatter.*marginal'),
        ('regression-marginals',r'(?:regression|correlation).*marginal'),
        ('scatter-sized',r'scatter.*(?:size encoding|marker.size|bubble)'),
        ('mass-spectrum',r'mass spectrum'),
        ('flow',r'flow.cytometry|flow cytometr|\bfacs\b'),
        ('split-violin',r'(?:split|half|mirrored|butterfly).*violin|violin.*(?:split|half)'),
        ('raincloud',r'raincloud|云雨'),
        ('roc-pr',r'roc.*precision.recall'),
        ('pr',r'precision.recall'),
        ('roc',r'\broc\b'),
        ('enrichment-dots',r'enrichment.*(?:dot|bubble)|(?:dot|bubble).*enrichment'),
        ('gsea-profile',r'gsea.*(?:profile|curve|enrichment plot)|running.score'),
        ('enrichment-lollipop',r'(?:enrichment|pathway).*lollipop'),
        ('diverging-lollipop',r'diverging.*lollipop|lollipop.*diverging'),
        ('enrichment-bars',r'(?:enrichment|ontology|pathway).*(?:bar|interval)'),
        ('radial-bars',r'radial.*bar|circular.*bar'),
        ('diverging-bars',r'diverging.*bar'),
        ('sunburst',r'sunburst'), ('treemap',r'treemap'),
        ('pca',r'\bpca\b|principal.component'),
        ('embedding-contours',r'(?:umap|embedding).*(?:contour|outline|hull)'),
        ('embedding-composite',r'(?:umap|embedding).*(?:proportion|fraction|dendrogram|hierarchy|summary)'),
        ('feature-embedding',r'(?:feature|expression).*(?:umap|embedding)|(?:umap|embedding).*feature'),
        ('stacked-area',r'stacked.*(?:area|density profile)|streamgraph'),
    ]
    for group,pattern in patterns:
        if re.search(pattern,text):return group
    if re.search(r'stacked.*time.course.*line|stacked.*line plots',text):return 'line'
    # These words describe panels or biology as well as pairing; geometry comes first.
    if family in ['paired','tree','genomic-tracks']:
        if re.search(r'heatmap|matri',text):
            return 'annotated-heatmap' if re.search(r'annotat|split|cluster|dendro',text) else 'continuous-heatmap'
        if re.search(r'stack|composition',text):return 'stacked-bars'
        if 'violin' in text:return 'violin'
        if 'box' in text:return 'boxplot'
        if 'scatter' in text:return 'scatter'
        if 'bar' in text and 'paired-point' not in text:return 'mean-bars'
    if family=='mean-bars' and not re.search(r'\bbar\b|\bbars\b',text):return 'point-interval'
    if family=='plain-bars' and re.search(r'individual|observation|error|points|scatter',text):return 'mean-bars'
    if family=='density' and 'box' in text:return 'boxplot'
    if family=='enrichment' and re.search(r'gsea|enrichment plot',text):return 'gsea-profile'
    if family=='continuous-heatmap' and re.search(r'binary|categorical|contingency',text):return 'binary-heatmap'
    if family=='line' and re.search(r'uncertainty|confidence|ribbon',text):return 'line-ribbon'
    return family


def describe(group):
    return SPECIAL.get(group,(LABELS[group],group)) if group in LABELS else SPECIAL[group]


def organize(records):
    groups=defaultdict(list)
    for record in records:
        group=group_for(record)
        title,family=describe(group)
        record.update(plot_group=group,plot_group_title=title,family=family,family_title=LABELS[family])
        groups[group].append(record)
    result=[]
    priority={'MedBioinform compact':0,'Personal':1,'Custom':1,'Worked example':2,
              'MedBioinform':3,'External code':4,'Publication':5,'Prism':6}
    for group,items in groups.items():
        representative=min(items,key=lambda r:(
            not bool(r.get('thumbnail')),
            not any(l['kind']=='code' for l in r.get('links',[])),
            not r.get('review',{}).get('native_controls',False),
            (8 if r['collection']=='MedBioinform compact' and not r.get('verification',{}).get('visual_reviewed') else priority.get(r['collection'],9)),
            r.get('data_basis')=='synthetic',
            len(r.get('title','')),r['key']))
        title,family=describe(group)
        result.append({'id':group,'title':title,'family':family,
                       'representative':representative['key'],
                       'members':[r['key'] for r in items],
                       'collections':sorted({r['collection'] for r in items}),
                       'source_collections':sorted({r['collection'].replace('MedBioinform compact','MedBioinform') for r in items}),
                       'basis':'Shared chart geometry. Labels, facets, annotations, inputs and implementations remain linked as variants.'})
    return sorted(result,key=lambda g:g['title'].lower())
