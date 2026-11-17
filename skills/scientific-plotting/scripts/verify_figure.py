#!/usr/bin/env python3
"""Measure saved PDF/PNG/TIFF figures at their intended placement; write a JSON report."""
import argparse
import json
import math
from pathlib import Path
import re

import pymupdf
from PIL import Image


def placement(width, height, placed_width, placed_height=None):
    scale = placed_width / width
    final_height = placed_height if placed_height is not None else height * scale
    stretched = not math.isclose(scale, final_height / height, rel_tol=0.01)
    return min(scale, final_height / height), final_height, stretched


def check_pdf(path, width_mm, height_mm=None, floor_pt=10, family='Arial', bold='panel-letters', image_dpi=300):
    result = {'file':str(path),'format':'PDF','pages':[], 'failures':[], 'unchecked':[]}
    with pymupdf.open(path) as doc:
        if not doc.is_pdf:raise ValueError('File contents are not PDF')
        if not len(doc):result['failures'].append('PDF has no pages')
        for page in doc:
            width = page.rect.width * 25.4 / 72
            height = page.rect.height * 25.4 / 72
            scale, final_height, stretched = placement(width,height,width_mm,height_mm)
            if stretched:result['failures'].append(f'Page {page.number+1}: placement changes the aspect ratio')
            spans=[]
            # MuPDF resolves nested forms and text matrices, including rotated labels.
            for block in page.get_text('dict',clip=pymupdf.INFINITE_RECT())['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        if not span['text'].strip():continue
                        text=span['text'];font=span['font'];effective=span['size']*scale
                        problems=[]
                        if effective<=floor_pt:problems.append(f'effective size must exceed {floor_pt:g} pt')
                        clean_font=re.sub(r'^[A-Z]{6}\+','',font).lower()
                        if not clean_font.startswith(family.lower()):problems.append('font family mismatch')
                        if '\ufffd' in text or '\x00' in text:problems.append('unmapped glyph')
                        is_bold=bool(span['flags'] & 16) or 'bold' in clean_font
                        if is_bold and (bold=='none' or (bold=='panel-letters' and not re.fullmatch('[A-Za-z]',text.strip()))):
                            problems.append('bold outside the requested panel-letter rule')
                        bounds=pymupdf.Rect(span['bbox']) * page.rotation_matrix
                        if not (page.rect + (-.5,-.5,.5,.5)).contains(bounds):problems.append('text bounds cross the page edge')
                        spans.append({'text':text,'font':font,'native_pt':round(span['size'],3),
                                      'effective_pt':round(effective,3),'issues':problems})
                        if problems:result['failures'].append(f'Page {page.number+1}: {text!r}: '+ '; '.join(problems))
            if not spans:result['unchecked'].append(f'Page {page.number+1}: no extractable text; inspect raster or outlined labels')
            for font in page.get_fonts(full=True):
                if font[2]=='Type3':
                    result['unchecked'].append(f'Page {page.number+1}: inspect Type 3 glyphs and their native font metrics')
                elif font[0] and not doc.extract_font(font[0])[3]:
                    result['failures'].append(f'Page {page.number+1}: unembedded font {font[3]}')
            rasters=[]
            for img in page.get_image_info():
                a,b,c,d,_,_=img['transform']
                width_pt=math.hypot(a,b)*scale;height_pt=math.hypot(c,d)*scale
                dpi=min(img['width']*72/width_pt,img['height']*72/height_pt) if min(width_pt,height_pt)>0 else 0
                rasters.append({'pixels':[img['width'],img['height']],'effective_dpi':round(dpi,2)})
                if dpi<image_dpi-1:result['failures'].append(f'Page {page.number+1}: embedded raster {dpi:.1f} dpi < {image_dpi:g}')
            if rasters:result['unchecked'].append(f'Page {page.number+1}: inspect any text within raster layers; PDF spans cover vector text only')
            result['pages'].append({'page':page.number+1,'export_mm':[round(width,2),round(height,2)],
                'placed_mm':[width_mm,round(final_height,2)],'min_effective_pt':min((s['effective_pt'] for s in spans),default=None),
                'fonts':sorted(set(s['font'] for s in spans)),'spans':spans,'raster_layers':rasters})
    return result


def check_raster(path, width_mm, height_mm=None, min_dpi=600):
    result={'file':str(path),'pages':[],'failures':[],'unchecked':[]}
    expected={'.png':'PNG','.tif':'TIFF','.tiff':'TIFF'}[path.suffix.lower()]
    with Image.open(path) as img:
        result['format']=img.format
        if img.format!=expected:result['failures'].append(f'Extension says {expected}; decoded format is {img.format}')
        for i in range(getattr(img,'n_frames',1)):
            img.seek(i);img.load()
            if img.format=='TIFF' and 'jpeg' in str(img.info.get('compression','')).lower():
                result['failures'].append(f'Frame {i+1}: lossy JPEG compression in TIFF')
            w,h=img.size
            final_height=height_mm if height_mm is not None else width_mm*h/w
            dpi_x=w*25.4/width_mm;dpi_y=h*25.4/final_height
            if not math.isclose(dpi_x,dpi_y,rel_tol=.01):result['failures'].append(f'Frame {i+1}: placement changes the aspect ratio')
            if min(dpi_x,dpi_y)<min_dpi-1:result['failures'].append(f'Frame {i+1}: effective resolution {min(dpi_x,dpi_y):.1f} dpi < {min_dpi:g}')
            result['pages'].append({'page':i+1,'pixels':[w,h],'placed_mm':[width_mm,round(final_height,2)],
                'effective_dpi':[round(dpi_x,2),round(dpi_y,2)],
                'metadata_dpi':[float(v) for v in img.info['dpi']] if img.info.get('dpi') else None,
                'color_mode':img.mode,'compression':img.info.get('compression')})
    return result


def check_text_report(path, files, width_mm, family, floor_pt, bold):
    """Use the renderer's retained measurements without retaining its temporary PDF."""
    report = json.loads(Path(path).read_text())
    if report.get('schema') != 'biomed-export-1':
        raise ValueError('Unrecognized native export report')
    if not {Path(f).name for f in files} <= set(report['files']):
        raise ValueError('Text report belongs to different export files')
    font = report['font_check']
    if not font['text_runs'] or not font['page_bounds_pass']:
        raise ValueError('Reference text coverage or page bounds failed')
    effective = font['min_effective_pt'] * width_mm / report['placed_width_mm']
    failures = []
    if effective <= floor_pt:
        failures.append(f'Reference text effective size must exceed {floor_pt:g} pt')
    fonts = [re.sub(r'^[A-Z]{6}\+', '', f).lower() for f in font['fonts']]
    if any(not f.startswith(family.lower()) for f in fonts):
        failures.append('Reference font family mismatch')
    if bold == 'none' and any('bold' in f for f in fonts):
        failures.append('Reference contains bold text')
    for cell in report.get('heatmap_cells') or []:
        scale = width_mm / report['placed_width_mm']
        if min(cell['placed_width_mm'], cell['placed_height_mm']) * scale < 8 - .01:
            failures.append('Heatmap cells are below 8 mm at final placement')
    return dict(report=str(path), source=font['source'], min_effective_pt=effective,
                fonts=font['fonts'], failures=failures,
                scope='Native reference render; inspect final raster glyphs and layout visually')


def verify(files, width_mm, height_mm=None, floor_pt=10, family='Arial', bold='panel-letters',
           min_dpi=600, image_dpi=300, required=('png',), text_report=None):
    files=list(map(Path,files))
    results=[]
    for path in files:
        try:
            if not path.is_file():raise ValueError('Required file is missing')
            if path.suffix.lower()=='.pdf':r=check_pdf(path,width_mm,height_mm,floor_pt,family,bold,image_dpi)
            elif path.suffix.lower() in ['.png','.tif','.tiff']:r=check_raster(path,width_mm,height_mm,min_dpi)
            else:r={'file':str(path),'format':path.suffix[1:].upper(),'failures':[],
                    'unchecked':['Open this format in its native application; this helper measures PDF, PNG and TIFF']}
        except (OSError,ValueError,RuntimeError) as exc:
            r={'file':str(path),'format':None,'failures':[str(exc)],'unchecked':[]}
        results.append(r)
    found={(r['format'] or '').lower() for r in results}
    missing=[f for f in required if f not in found]
    failures=[problem for r in results for problem in r['failures']]+['Missing required format: '+f for f in missing]
    unchecked=[problem for r in results for problem in r['unchecked']]
    pdfs=[r for r in results if r['format']=='PDF']
    text_reference=None
    if text_report is None and files and len({str(f.with_suffix('')) for f in files})==1:
        candidate=files[0].with_name(files[0].stem+'_export.json')
        if candidate.exists():text_report=candidate
    if text_report is not None:
        try:
            text_reference=check_text_report(text_report,files,width_mm,family,floor_pt,bold)
            failures.extend(text_reference['failures'])
        except (OSError,ValueError,KeyError,TypeError) as exc:
            failures.append('Invalid text report: '+str(exc))
    elif not pdfs:
        unchecked.append('No native text measurements; inspect raster/outlined text at final size')
    if pdfs:
        reference=pdfs[0].get('pages',[])
        for r in results:
            if r is pdfs[0] or not r.get('pages'):continue
            if len(r['pages'])!=len(reference):failures.append(f'{r["file"]}: page/frame count differs from PDF companion')
            elif height_mm is None and any(abs(a['placed_mm'][1]-b['placed_mm'][1])>.5 for a,b in zip(reference,r['pages'])):
                failures.append(f'{r["file"]}: aspect ratio differs from PDF companion')
    return {'mechanical_status':'fail' if failures else 'review-needed' if unchecked else 'pass',
        'contract':{'placed_width_mm':width_mm,'placed_height_mm':height_mm,'font':family,
                    'font_floor_exclusive_pt':floor_pt,'raster_min_dpi':min_dpi,'embedded_image_min_dpi':image_dpi,'dpi_rounding_tolerance':1,'required_formats':list(required)},
        'failures':failures,'unchecked':unchecked,'files':results,'text_reference':text_reference,
        'manual_review':{'statistics':'pending','visual_inspection':'pending','native_editability_and_source_data':'pending'},
        'completion':'Complete the scientific and visual review in references/figure-verification.md.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--placed-width-mm',type=float,required=True)
    parser.add_argument('--placed-height-mm',type=float)
    parser.add_argument('--font',default='Arial')
    parser.add_argument('--floor-pt',type=float,default=10,help='Exclusive minimum; explicit dense-label exceptions need a separate review')
    parser.add_argument('--bold',choices=['none','panel-letters','any'],default='panel-letters')
    parser.add_argument('--min-dpi',type=float,default=600,help='Raster plot requirement; continuous-tone-only images can use 300')
    parser.add_argument('--image-min-dpi',type=float,default=300,help='Minimum for raster layers embedded in PDF; use 600 for line/label layers')
    parser.add_argument('--require',nargs='+',choices=['pdf','png','tiff','svg'],default=['png'])
    parser.add_argument('--text-report',type=Path,help='Native export measurements; defaults to the matching *_export.json for PNG-only output')
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    values=[a.placed_width_mm,a.floor_pt,a.min_dpi,a.image_min_dpi]+([a.placed_height_mm] if a.placed_height_mm is not None else [])
    if any(not math.isfinite(x) or x<=0 for x in values):parser.error('Dimensions and thresholds must be positive and finite')
    result=verify(a.files,a.placed_width_mm,a.placed_height_mm,a.floor_pt,a.font,a.bold,a.min_dpi,a.image_min_dpi,a.require,a.text_report)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(result['mechanical_status']+': '+str(a.output)+'; scientific and visual review still required')
    return 1 if result['failures'] else 2 if result['unchecked'] else 0


if __name__=='__main__':raise SystemExit(main())
