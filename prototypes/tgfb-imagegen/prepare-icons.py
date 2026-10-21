"""Trace accepted built-in generated TGFbeta icons and curate source-pixel anchors."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;L=P.parents[1]/'skills/scientific-visual-explainer/assets/biomed-icons';F=L/'tgfb-imagegen'
sys.path.insert(0,str(L.parents[1]/'scripts'))
from trace_icon import trace_icon,register
refs={'receptor':'https://pubmed.ncbi.nlm.nih.gov/8047140/','assembly':'https://pubmed.ncbi.nlm.nih.gov/20207738/','smad':'https://pubmed.ncbi.nlm.nih.gov/15350224/','smad2':'https://doi.org/10.1074/jbc.272.44.28107'}
settings={
 'tgfb1-ig':('TGFβ1 dimer',{'outline':'#3D5963','subunit-a':'#E4BE78','subunit-b':'#B3D7CC'},'Mature ligand homodimer; latent-complex proteins omitted.'),
 'tgfbr2-ig':('TGFβRII',{'outline':'#3D5963','ectodomain-stalk':'#69ADB5','kinase':'#B2A6CD'},'Single-pass type II receptor with constitutive kinase activity; teaching domain proportions.'),
 'tgfbr1-ig':('TGFβRI / ALK5',{'outline':'#3D5963','ectodomain-stalk':'#69ADB5','GS-region':'#E4BE78','kinase':'#B2A6CD'},'Single-pass type I receptor, membrane-proximal GS region and Ser/Thr kinase.'),
 'smad3-ig':('SMAD3',{'outline':'#3D5963','MH1':'#69ADB5','MH2':'#B2A6CD','SSXS-tail':'#E4BE78'},'MH1, linker, MH2 and C-terminal phosphorylation tail; not a solved surface.'),
 'smad4-ig':('SMAD4',{'outline':'#3D5963','MH1':'#B3D7CC','MH2':'#69ADB5'},'Co-SMAD with MH1/linker/MH2; no R-SMAD SSXS activation motif.'),
 'smad2-ig':('SMAD2',{'outline':'#3D5963','MH1-insertion':'#D7E8EC','MH2':'#B2A6CD','SSXS-tail':'#E4BE78'},'SMAD2-specific MH1 insertion shown schematically; library extension, not the SMAD3 lesson actor.')}
specs=[]
for id,(label,palette,scope) in settings.items():
 im=Image.open(F/'sources'/f'{id}.png').convert('RGBA');a=np.asarray(im)[:,:,3]>128;x0,y0,x1,y1=Image.fromarray(a.astype('uint8')*255).getbbox();w=x1-x0;h=y1-y0
 def at(x,y,n,edge=True):
  px=x0+x*w;py=y0+y*h
  if edge and n[0]:
   row=a[int(round(py))];xs=np.where(row)[0];px=xs[-1] if n[0]>0 else xs[0]
  elif edge:
   col=a[:,int(round(px))];ys=np.where(col)[0];py=ys[-1] if n[1]>0 else ys[0]
  return dict(point=[float(px),float(py)],normal=n,kind='binding')
 if id=='tgfb1-ig':
  # Equal guide heights preserve both receptor membrane planes; paired curves refine each contact.
  anchors={'II-left':at(.10,.25,[0,1]),'II-right':at(.90,.25,[0,1]),'I-left':at(.35,.7,[0,1]),'I-right':at(.65,.7,[0,1])}
  for left,right in [('II-left','II-right'),('I-left','I-right')]:
   y=(anchors[left]['point'][1]+anchors[right]['point'][1])/2
   anchors[left]['point'][1]=anchors[right]['point'][1]=y
 elif id.startswith('tgfbr'):
  anchors={'ligand':at(.5,.1,[0,-1]),'membrane':at(.5,.365,[0,-1],False),'SMAD-substrate':at(.65,.77,[1,0]),'GS-activation':at(.5,.64,[1,0])}
  anchors['membrane']['kind']='membrane'
  if id=='tgfbr1-ig':anchors['GS']=at(.5,.55,[-1,0])
 else:
  anchors={'co-SMAD-right':at(.7,.64,[1,0]),'co-SMAD-left':at(.3,.64,[-1,0]),'receptor-docking':at(.3,.68,[-1,0]),'DNA-binding':at(.5,.05,[0,-1]),'center':at(.5,.5,[0,-1],False)}
  anchors['center']['kind']='center'
  if id!='smad4-ig':anchors['SSXS-tail']=at(.5,.98,[0,1])
 source='assembly' if id=='tgfb1-ig' else 'receptor' if id.startswith('tgfbr') else 'smad2' if id=='smad2-ig' else 'smad'
 spec=dict(id=id,label=label,label_zh=label,category='tgfb-imagegen',description=scope,palette=palette,anchors=anchors,scope=scope+' Contact contours are illustrative.',visual_references=[dict(url='https://www.biorender.com/template/tgf-beta-signaling-pathway',scope='Public full preview visually inspected; no artwork copied.')],scientific_references=[dict(url=refs[source],scope='Primary abstract and available figure captions read.')],provenance=dict(mode='built-in-imagegen-traced',source=f'tgfb-imagegen/sources/{id}.png',prompt='tgfb-imagegen/prompts.json',license='MIT',generator_model='tool-managed; identifier not exposed'))
 specs.append(spec);output=F/(id+'.svg');entry=trace_icon(F/'sources'/f'{id}.png',output,spec);register(entry,output,L)
(F/'specs.json').write_text(json.dumps(specs,indent=2,ensure_ascii=False)+'\n')
print('Registered six generated TGFbeta/SMAD icons.')
