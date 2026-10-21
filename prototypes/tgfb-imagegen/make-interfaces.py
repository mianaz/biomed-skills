from pathlib import Path
import json
P=Path(__file__).resolve().parent;F=P.parents[1]/'skills/scientific-visual-explainer/assets/biomed-icons/tgfb-imagegen'
icons={x['id']:x for x in json.loads((F/'manifest.json').read_text())}
def pt(i,n):
 a=icons[i]['anchors'][n];return a.get('interface',{}).get('framePoint',a['point'])
sr=2.4;sl=3.3
ligand_II_y=330-(pt('tgfbr2-ig','membrane')[1]-pt('tgfbr2-ig','ligand')[1])*sr
ligand_I_y=ligand_II_y+(pt('tgfb1-ig','I-left')[1]-pt('tgfb1-ig','II-left')[1])*sl
si=(330-ligand_I_y)/(pt('tgfbr1-ig','membrane')[1]-pt('tgfbr1-ig','ligand')[1])
def side(i,port,shape,scale,part,duplicates=[]):return dict(icon=i,port=port,shape=shape,scale=scale,part=part,duplicatePorts=duplicates)
pairs=[dict(id='TGFB-RII',halfWidth=30,extent=35,depth=1,sides=[side('tgfb1-ig','II-left','tab',sl,'subunit-a',['II-right']),side('tgfbr2-ig','ligand','socket',sr,'ectodomain-stalk')]),dict(id='TGFB-RI',halfWidth=3,extent=8,depth=.7,sides=[side('tgfb1-ig','I-left','tab',sl,'subunit-a',['I-right']),side('tgfbr1-ig','ligand','socket',si,'ectodomain-stalk')]),dict(id='MH2-association',halfWidth=5,extent=11,depth=.25,profileShape='gentle',sides=[side('smad3-ig','co-SMAD-left','tab',.65,'MH2',['co-SMAD-right']),side('smad4-ig','co-SMAD-right','socket',.65,'MH2',['co-SMAD-left']),side('tgfbr1-ig','SMAD-substrate','socket',si,'kinase')])]
# Keep the duplicate contact colors consistent with their local ligand subunits.
pairs[0]['sides'][0]['duplicatePart']='subunit-b';pairs[1]['sides'][0]['duplicatePart']='subunit-b'
(F/'interfaces.json').write_text(json.dumps(dict(scope='Schematic interfaces at the specified assembly scales, not molecular surface reconstruction.',pairs=pairs),indent=2)+'\n')
print('RII scale',sr,'RI scale',si,'ligand scale',sl)
