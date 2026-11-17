"""Render the baked shared timeline with Manim; no biological rules live here.

python render_figure_manim.py scene.json lesson.frames.json --output lesson.mp4
Requires Manim Community and NumPy. Raster parts are embedded PNGs.
"""
import argparse
import base64
import json
from pathlib import Path
import tempfile
import numpy as np
from manim import Scene, Group, SVGMobject, ImageMobject, Text, Rectangle, UpdateFromAlphaFunc, tempconfig, WHITE, VMobject


def render(scene, timeline, output):
    width,height=scene['canvas']['width'],scene['canvas']['height']
    scale=min(12.6/width,5.4/height)
    frames=timeline['frames']
    def point(x,y):return np.array([(x-width/2)*scale,(height/2-y)*scale,0.])
    class ImportedFigure(Scene):
        def construct(self):
            bodies={};bases={};colored={};halos={};halo_bases={};styles={};images={}
            for entity_index,entity in enumerate(scene['entities']):
                parts=[];colored[entity['id']]=[]
                for j,part in enumerate(entity['parts']):
                    b=part['bbox']
                    if part['type']=='text':
                        item=Text(part['text'],font=part['fontFamily'],font_size=part['fontSize']*scale*48,color=part['fill'],weight='BOLD' if part.get('fontWeight',400)>=600 else 'NORMAL',slant='ITALIC' if part.get('fontStyle')=='italic' else 'NORMAL')
                        item.move_to(point(b[0]+b[2]/2,b[1]+b[3]/2)).set_opacity(part.get('opacity',1))
                    elif part['type']=='path':
                        # Individual paths keep native contours; the shared SVG stays editable.
                        svg=f'<svg xmlns="http://www.w3.org/2000/svg"><path d="{part["d"]}" fill="{part["fill"]}" stroke="{part["stroke"]}" stroke-width="{part["strokeWidth"]}" stroke-linejoin="{part.get("linejoin","miter")}" stroke-linecap="{part.get("linecap","butt")}" opacity="{part.get("opacity",1)}" fill-opacity="{part.get("fillOpacity",1)}" stroke-opacity="{part.get("strokeOpacity",1)}"/></svg>'
                        file=Path(tmp)/f'{entity_index}-{j}.svg';file.write_text(svg)
                        item=SVGMobject(str(file),height=None,width=None)
                        item.scale(scale).move_to(point(b[0]+b[2]/2,b[1]+b[3]/2))
                        if part['fill']!='none':colored[entity['id']].append(item)
                    else:
                        file=Path(tmp)/f'{entity_index}-{j}.png';file.write_bytes(base64.b64decode(part['href'].split(',')[1]))
                        item=ImageMobject(str(file)).stretch_to_fit_width(b[2]*scale).stretch_to_fit_height(b[3]*scale)
                        item.move_to(point(b[0]+b[2]/2,b[1]+b[3]/2))
                    parts.append(item)
                body=Group(*parts)
                styles[entity['id']]=[(m,m.get_fill_opacity(),m.get_stroke_opacity()) for m in body.family_members_with_points() if isinstance(m,VMobject)]
                images[entity['id']]=[m for m in parts if isinstance(m,ImageMobject)]
                bodies[entity['id']]=body;bases[entity['id']]=body.get_center().copy();self.add(body)
                b=entity['bbox'];halo=Rectangle(width=(b[2]+10)*scale,height=(b[3]+10)*scale,color='#246963',stroke_width=2)
                halo.move_to(point(b[0]+b[2]/2,b[1]+b[3]/2));halo_bases[entity['id']]=halo.get_center().copy()
                halo.set_opacity(0);halos[entity['id']]=halo;self.add(halo)
            heading=Text(scene['title'],font='Arial',font_size=30,color='#243e44').move_to([0,3.4,0]);self.add(heading)
            caption=Text(frames[0]['caption'],font='Arial',font_size=21,color='#243e44').move_to([0,-3.25,0])
            if caption.width>12.8:caption.scale_to_fit_width(12.8)
            self.add(caption);previous=[None]
            def apply(_,alpha):
                sample=alpha*(len(frames)-1);i=min(int(sample),len(frames)-1);j=min(i+1,len(frames)-1);u=sample-i
                a,b=frames[i],frames[j]
                for id,body in bodies.items():
                    p,q=a['poses'][id],b['poses'][id]
                    dx=p['dx']+(q['dx']-p['dx'])*u;dy=p['dy']+(q['dy']-p['dy'])*u
                    body.move_to(bases[id]+np.array([dx*scale,-dy*scale,0]))
                    opacity=p['opacity']+(q['opacity']-p['opacity'])*u
                    for item,fill_alpha,stroke_alpha in styles[id]:item.set_fill(opacity=fill_alpha*opacity).set_stroke(opacity=stroke_alpha*opacity)
                    for item in images[id]:item.set_opacity(opacity)
                    halos[id].move_to(halo_bases[id]+np.array([dx*scale,-dy*scale,0])).set_opacity(p['opacity'] if p['highlight'] else 0)
                    if p['fill']:
                        for item in colored[id]:item.set_fill(p['fill'])
                if previous[0]!=a['caption']:
                    replacement=Text(a['caption'],font='Arial',font_size=21,color='#243e44')
                    if replacement.width>12.8:replacement.scale_to_fit_width(12.8)
                    caption.become(replacement.move_to([0,-3.25,0]));previous[0]=a['caption']
            apply(None,0)
            if timeline['duration']>0:self.play(UpdateFromAlphaFunc(Group(*bodies.values(),*halos.values(),caption),apply),run_time=timeline['duration'],rate_func=lambda u:u)
            else:self.wait(1)
    output=Path(output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp, tempconfig({'background_color':WHITE,'pixel_width':1280,'pixel_height':720,'frame_rate':timeline['fps'],'frame_width':14.2222222222,'frame_height':8,'output_file':str(output),'media_dir':str(output.parent/'.manim-media'),'disable_caching':True}):
        ImportedFigure().render()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('scene',type=Path);p.add_argument('frames',type=Path);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();render(json.loads(args.scene.read_text()),json.loads(args.frames.read_text()),args.output)
