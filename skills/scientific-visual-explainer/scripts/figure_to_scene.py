"""Import flat SVG groups or annotated raster parts into one editable scene.

python figure_to_scene.py figure.svg --annotations plan.json --output scene.json
Requires svgelements for SVG; Pillow for raster parts. Semantics come from the
annotations, not from path tracing. The original figure stays in the scene.
"""
import argparse
import base64
import io
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def data_uri(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def svg_entities(source, annotations):
    from svgelements import SVG, Path as SVGPath, Shape, Text, Move, Line, Close, CubicBezier, QuadraticBezier, Color
    root = ET.fromstring(source)
    unsupported = {'script', 'foreignObject', 'image', 'use', 'style', 'clipPath', 'mask', 'filter', 'linearGradient', 'radialGradient', 'pattern', 'marker', 'animate', 'animateTransform', 'set'}
    for node in root.iter():
        if node.tag.split('}')[-1] in unsupported or any(k.startswith('on') or k.endswith('href') or 'url(' in v for k,v in node.attrib.items()):
            raise ValueError('SVG uses unsupported active/referenced artwork. Export these components as transparent assets and use raster annotations.')
    opacity_by_id = {}
    def identify(node, parent_opacity=1):
        style = dict(item.strip().split(':',1) for item in node.get('style','').split(';') if ':' in item)
        if node.get('stroke-dasharray',style.get('stroke-dasharray','none'))!='none' or node.get('fill-rule',style.get('fill-rule','nonzero'))!='nonzero':
            raise ValueError('SVG dash patterns/even-odd fills need expanded paths or separate transparent component assets.')
        opacity = parent_opacity * float(node.get('opacity',style.get('opacity',1)))
        if 'id' not in node.attrib:node.set('id',f'figure-part-{len(opacity_by_id)}')
        opacity_by_id[node.get('id')] = opacity
        for child in node:identify(child,opacity)
    identify(root)
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    # svgelements resolves the root viewBox and inherited transforms into pixels.
    drawing = SVG.parse(io.StringIO(ET.tostring(root,encoding='unicode')), on_error='raise')
    width, height = float(drawing.width), float(drawing.height)
    specifications = annotations.get('entities')
    if specifications is None:
        specifications = [{'id': n.id, 'source_id': n.id} for n in drawing if getattr(n, 'id', None)]
    if not specifications:
        raise ValueError('No named SVG groups found. Add IDs or supply entities with source_id in the annotation file.')
    def leaves(node):
        if isinstance(node, list):
            return [part for child in node for part in leaves(child)]
        return [node]

    selected = set()
    entities = []
    paint_order = {id(n):i for i,n in enumerate(drawing.elements())}
    entity_order = {}
    for spec in specifications:
        source_id = spec.get('source_id', spec['id'])
        source_node = next((n for n in drawing.elements() if getattr(n, 'id', None) == source_id), None)
        if source_node is None:
            raise ValueError(f'SVG source_id not found: {source_id}')
        nodes = leaves(source_node)
        parts = []
        for node in nodes:
            if not isinstance(node, (Shape, Text)):
                continue
            # Never duplicate a child selected again through a nested group.
            if id(node) in selected:
                raise ValueError(f'Overlapping entity selections at {source_id}; choose disjoint groups.')
            selected.add(id(node))
            if isinstance(node, Text):
                matrix = node.transform
                if abs(matrix.b) + abs(matrix.c) > 1e-7:
                    raise ValueError('Rotated/skewed SVG text needs an explicit unrotated label or an asset.')
                x, y = matrix.point_in_matrix_space((node.x + node.dx, node.y + node.dy))
                size = float(node.font_size) * abs(matrix.d)
                text = str(node.text or '')
                tw = max(size * 1.2, len(text) * size * .8 + size * .3)
                anchor = node.anchor or 'start'
                left = x - tw * {'start': 0, 'middle': .5, 'end': 1}.get(anchor, 0)
                parts.append({'type': 'text', 'text': text, 'x': x, 'y': y,
                              'fontSize': size, 'fontFamily': node.font_family or 'Arial',
                              'fontWeight': node.font_weight, 'fontStyle': node.values.get('font-style','normal'),
                              'anchor': anchor, 'fill': 'none' if node.fill.value is None else node.fill.hex[:7],
                              'opacity': opacity_by_id[node.id] * Color(node.values.get('fill','black')).opacity * float(node.values.get('fill-opacity',1)),
                              'bbox': [left, y - size, tw, size * 1.3]})
                continue
            path = SVGPath(node)
            path.reify()
            path.approximate_arcs_with_cubics()
            bounds = path.bbox()
            if bounds is None:
                continue
            commands = []
            for segment in path:
                if isinstance(segment, Move):
                    commands.append({'moveTo': {'x': segment.end.x, 'y': segment.end.y}})
                elif isinstance(segment, Close):
                    commands.append({'close': {}})
                elif isinstance(segment, Line):
                    commands.append({'lineTo': {'x': segment.end.x, 'y': segment.end.y}})
                elif isinstance(segment, CubicBezier):
                    commands.append({'cubicBezTo': {'x1': segment.control1.x, 'y1': segment.control1.y,
                                                  'x2': segment.control2.x, 'y2': segment.control2.y,
                                                  'x': segment.end.x, 'y': segment.end.y}})
                elif isinstance(segment, QuadraticBezier):
                    commands.append({'quadBezTo': {'x1': segment.control.x, 'y1': segment.control.y,
                                                 'x': segment.end.x, 'y': segment.end.y}})
            fill = 'none' if node.fill.value is None else node.fill.hex[:7]
            stroke = 'none' if node.stroke.value is None else node.stroke.hex[:7]
            parts.append({'type': 'path', 'd': path.d(), 'commands': commands,
                          'fill': fill, 'stroke': stroke, 'strokeWidth': float(node.implicit_stroke_width),
                          'linecap': node.values.get('stroke-linecap','butt'), 'linejoin': node.values.get('stroke-linejoin','miter'),
                          'opacity': opacity_by_id[node.id],
                          'fillOpacity': Color(node.values.get('fill','black')).opacity * float(node.values.get('fill-opacity',1)) if fill!='none' else 0,
                          'strokeOpacity': Color(node.values.get('stroke','none')).opacity * float(node.values.get('stroke-opacity',1)) if stroke!='none' else 0,
                          'bbox': [bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]]})
        if not parts:
            raise ValueError(f'No supported artwork in {source_id}')
        entity_order[spec['id']] = min(paint_order[id(n)] for n in nodes if isinstance(n,(Shape,Text)))
        xs = [p['bbox'][0] for p in parts]; ys = [p['bbox'][1] for p in parts]
        right = max(p['bbox'][0] + p['bbox'][2] for p in parts)
        bottom = max(p['bbox'][1] + p['bbox'][3] for p in parts)
        entities.append({'label': source_id, 'kind': 'unclassified', **spec,
                         'bbox': [min(xs), min(ys), right-min(xs), bottom-min(ys)],
                         'parts': parts, 'asset_mode': 'native-paths-and-text'})
    supported = {id(n) for n in drawing.elements() if isinstance(n, (Shape, Text))}
    if supported - selected:
        raise ValueError('Some visible SVG artwork is not assigned to an entity. Include context/background groups too.')
    entities.sort(key=lambda e:entity_order[e['id']])
    return width, height, entities


def raster_entities(path, annotations):
    from PIL import Image
    original = Image.open(path).convert('RGBA')
    entities = []
    for spec in annotations.get('entities', []):
        x, y, w, h = spec['bbox']
        if spec.get('asset'):
            part = Image.open(path.parent / spec['asset']).convert('RGBA')
            mode = 'provided-raster-part'
        elif spec.get('mask'):
            mask = Image.open(path.parent / spec['mask']).convert('L')
            if mask.size != original.size:
                raise ValueError('A raster mask must use the original image dimensions.')
            part = original.copy(); part.putalpha(mask)
            part = part.crop((x, y, x+w, y+h))
            mode = 'masked-source-part'
        elif spec.get('crop') is True:
            part = original.crop((x, y, x+w, y+h))
            mode = 'rectangular-source-crop'
        else:
            raise ValueError(f'{spec["id"]}: supply asset/mask, or explicitly set crop:true for a rectangular crop.')
        buffer = io.BytesIO(); part.save(buffer, format='PNG')
        entity = {'label': spec['id'], 'kind': 'unclassified', **spec, 'asset_mode': mode,
                  'parts': [{'type': 'image', 'href': data_uri(buffer.getvalue(), 'image/png'), 'bbox': [x,y,w,h]}]}
        for text in spec.get('texts', []):
            entity['parts'].append({'type': 'text', 'fontFamily': 'Arial', 'anchor': 'start', 'fill': '#243e44', **text})
        entities.append(entity)
    if not entities:
        raise ValueError('Raster input needs component annotations; automatic OCR/segmentation is not provided by this importer.')
    return *original.size, entities


def import_figure(path, annotations):
    path = Path(path)
    raw = path.read_bytes()
    if path.suffix.lower() == '.svg':
        width, height, entities = svg_entities(raw.decode(), annotations)
        source = {'svg': raw.decode(), 'file': path.name, 'mode': 'native-svg'}
    else:
        width, height, entities = raster_entities(path, annotations)
        mime = 'image/png' if path.suffix.lower() == '.png' else 'image/jpeg'
        source = {'href': data_uri(raw, mime), 'file': path.name, 'mode': 'annotated-raster'}
    ids = [e['id'] for e in entities]
    if len(set(ids)) != len(ids):
        raise ValueError('Entity IDs must be unique.')
    if not all(math.isfinite(v) and v > 0 for v in [width, height]):
        raise ValueError('The figure needs finite, positive dimensions.')
    return {'schema': 'biomed-figure-scene/1', 'title': annotations.get('title', path.stem),
            'scope': annotations.get('scope', 'Imported artwork; biological meaning awaits annotation.'),
            'timing_basis': annotations.get('timing_basis', 'pedagogical'),
            'canvas': {'width': width, 'height': height}, 'source': source,
            'entities': entities, 'relations': annotations.get('relations', []),
            'events': annotations.get('events', []), 'sources': annotations.get('sources', [])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('figure', type=Path)
    parser.add_argument('--annotations', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    plan = json.loads(args.annotations.read_text()) if args.annotations else {}
    scene = import_figure(args.figure, plan)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scene, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(scene["entities"])} components → {args.output}')
