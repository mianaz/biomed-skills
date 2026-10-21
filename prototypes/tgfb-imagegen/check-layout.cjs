const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const motion=require('../biomedical-manim/domain-motion.js');require('../../skills/scientific-visual-explainer/scripts/mechanism-annotations.js');require('../../skills/scientific-visual-explainer/scripts/mechanism-arrows.js');const scene=require('./scene.js');
const model=JSON.parse(fs.readFileSync(path.join(__dirname,'mechanism.json'))),catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/catalog.json'))).icons;
const frames=[],states={},geometry={},passageErrors=[];let membraneError=0;
for(const condition of ['normal','alk5-blocked','smad3-2SA']){
 const core=motion.make(scene.condition(model,condition),catalog);geometry[condition]=core.checks();assert.equal(geometry[condition].errors.length,0);
 for(let k=0;k<=Math.round(core.duration*10);k++){
  const f=core.frame(k/10),notes=scene.notes(core,f);for(const id of ['r1a','r1b','r2a','r2b'])membraneError=Math.max(membraneError,Math.abs(core.anchor(id,'membrane',f.poses[id]).point[1]-330));
  const importEvent=core.events.find(e=>e.id==='import');if(importEvent&&f.t>=importEvent.start&&f.t<=importEvent.end){
   for(const id of ['sa','sb','s4']){const p=f.poses[id],radius=70*p.s;if(p.c[1]+radius>1000&&p.c[1]-radius<1280&&(p.c[0]-radius<490||p.c[0]+radius>710))passageErrors.push([f.t,id]);}
   for(const b of notes.badges)if(b.id.startsWith('s')&&b.y+b.r>1000&&b.y-b.r<1280&&(b.x-b.r<490||b.x+b.r>710))passageErrors.push([f.t,b.id]);
  }
  frames.push({condition,t:k/10,...f,notes,routes:notes.routes});
 }
 states[condition]=core.frame(core.duration).states;
}
assert.ok(membraneError<1e-5);assert.equal(passageErrors.length,0);assert.equal(states.normal.sa,'pS2');assert.equal(states.normal.sb,'pS2');assert.equal(states.normal.rna,'transcribed');assert.equal(states['alk5-blocked'].r1a,'GS-P');assert.equal(states['alk5-blocked'].sa,undefined);assert.equal(states['alk5-blocked'].rna,undefined);assert.equal(states['smad3-2SA'].sa,'2SA');assert.equal(states['smad3-2SA'].rna,undefined);
const pairs=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/tgfb-imagegen/interfaces.json'))).pairs,byid=Object.fromEntries(catalog.map(x=>[x.id,x])),entities=Object.fromEntries(model.entities.map(e=>[e.id,e]));let maxContourGap=0,matchedSamples=0;
const world=(id,q,f)=>{const p=f.poses[id],x=(q[0]-80)*p.s,y=(q[1]-80)*p.s*p.fy,c=Math.cos(p.a),s=Math.sin(p.a);return[p.c[0]+c*x-s*y,p.c[1]+s*x+c*y]};
for(const f of frames)for(const c of [...f.contacts,...Object.entries(f.links).map(([actor,e])=>({actor,...e}))]){
 const a=byid[entities[c.actor].icon].anchors[c.port],b=byid[entities[c.target].icon].anchors[c.targetPort];if(!a.interface||a.interface.id!==b.interface?.id)continue;const pair=pairs.find(p=>p.id===a.interface.id);
 const curve=(id,port,t,z)=>{const icon=byid[entities[id].icon],a=icon.anchors[port],o=a.interface.framePoint,n=a.normal,v=[-n[1],n[0]],index=pair.sides.findIndex(s=>s.icon===icon.id&&(s.port===port||s.duplicatePorts?.includes(port))),direction=index===0?1:-1;return world(id,o.map((x,i)=>x+(v[i]*t+n[i]*z*direction)/f.poses[id].s),f)};
 pair.profileSamples.t.forEach((t,k)=>{if(Math.abs(t)>pair.halfWidth)return;const z=pair.profileSamples.z[k],p=curve(c.actor,c.port,t,z),q=curve(c.target,c.targetPort,t,z),r=curve(c.target,c.targetPort,-t,z);maxContourGap=Math.max(maxContourGap,Math.min(Math.hypot(p[0]-q[0],p[1]-q[1]),Math.hypot(p[0]-r[0],p[1]-r[1])));matchedSamples++});
}
assert.ok(maxContourGap<1e-5);
const html=fs.readFileSync(path.join(__dirname,'preview.html'),'utf8');for(const b of html.matchAll(/<script>([\s\S]*?)<\/script>/g))new Function(b[1]);
fs.writeFileSync(path.join(__dirname,'qa/layout-frames.json'),JSON.stringify(frames));fs.writeFileSync(path.join(__dirname,'qa/model-check.json'),JSON.stringify({samples:frames.length,membraneError,states,geometry,passageErrors,maxContourGap,matchedSamples},null,2)+'\n');console.log(JSON.stringify({samples:frames.length,membraneError,passageErrors,maxContourGap,matchedSamples,duration:58}));
