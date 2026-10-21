const fs=require('fs'),path=require('path');
const motion=require('../biomedical-manim/domain-motion.js');
const annotations=require('../../skills/scientific-visual-explainer/scripts/mechanism-annotations.js');
const arrows=require('../../skills/scientific-visual-explainer/scripts/mechanism-arrows.js');
const model=JSON.parse(fs.readFileSync(path.join(__dirname,'mechanism.json')));
const icons=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/manifest.json')));
const frames=[];
for(const condition of ['normal','blocked']){
 const m=structuredClone(model);if(condition==='blocked')m.events=m.events.filter(e=>['bind-a','bind-b','dimer'].includes(e.id));
 const core=motion.make(m,icons);
 for(let t=0;t<=core.duration+.001;t+=.1){const f=core.frame(t),routes=[];
  for(const[id,source,port,target,targetPort]of [['raf-mek','raf','MEK-substrate','mek','RAF-substrate'],['mek-erk','mek','ERK-substrate','erk','MEK-substrate']])routes.push({id,...arrows.route(core.anchor(source,port,f.poses[source]),core.anchor(target,targetPort,f.poses[target]),Boolean(f.states[source]))});
  const notes=annotations.annotations(core,f,true);frames.push({condition,t:Math.round(t*10)/10,poses:f.poses,states:f.states,contacts:f.contacts,links:f.links,notes,routes});
 }
}
const interfaces=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/interfaces.json')));
const catalog=Object.fromEntries(icons.map(i=>[i.id,i])),entities=Object.fromEntries(model.entities.map(e=>[e.id,e]));
const world=(id,q,f)=>{const p=f.poses[id],x=(q[0]-80)*p.s,y=(q[1]-80)*p.s*p.fy,c=Math.cos(p.a),s=Math.sin(p.a);return[p.c[0]+c*x-s*y,p.c[1]+s*x+c*y]};
let maxContourGap=0,matchedSamples=0;
for(const f of frames){
 const contacts=[...f.contacts,...Object.entries(f.links).map(([actor,e])=>({actor,...e}))];
 for(const c of contacts){
  const a=catalog[entities[c.actor].icon].anchors[c.port],b=catalog[entities[c.target].icon].anchors[c.targetPort];
  if(!a.interface||a.interface.id!==b.interface?.id)continue;
  const pair=interfaces.pairs.find(i=>i.id===a.interface.id);
  const curve=(id,port,t,z)=>{const icon=catalog[entities[id].icon],anchor=icon.anchors[port],p=f.poses[id],side=pair.sides[0],direction=icon.id===side.icon&&port===side.port?1:-1,n=anchor.normal,v=[-n[1],n[0]],o=anchor.interface.framePoint;return world(id,o.map((x,i)=>x+(v[i]*t+n[i]*z*direction)/p.s),f)};
  for(let k=0;k<pair.profileSamples.t.length;k++){
   const t=pair.profileSamples.t[k],z=pair.profileSamples.z[k];if(Math.abs(t)>pair.halfWidth)continue;
   const p=curve(c.actor,c.port,t,z),q=curve(c.target,c.targetPort,t,z),r=curve(c.target,c.targetPort,-t,z);
   maxContourGap=Math.max(maxContourGap,Math.min(Math.hypot(p[0]-q[0],p[1]-q[1]),Math.hypot(p[0]-r[0],p[1]-r[1])));matchedSamples++;
  }
 }
}
if(maxContourGap>1e-5)throw Error('Mating contours do not coincide: '+maxContourGap);
fs.writeFileSync(path.join(__dirname,'qa/interface-check.json'),JSON.stringify({pairs:interfaces.pairs.length,matchedSamples,maxContourGap,scope:'Shared illustrative curves, not atomic structures.'},null,2)+'\n');
fs.writeFileSync(path.join(__dirname,'qa/layout-frames.json'),JSON.stringify(frames));
console.log(frames.length+' normal and kinase-block frames prepared.');
