const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const motion=require('../biomedical-manim/domain-motion.js');
const arrows=require('../../skills/scientific-visual-explainer/scripts/mechanism-arrows.js');
const model=JSON.parse(fs.readFileSync(path.join(__dirname,'mechanism.json')));
const icons=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/manifest.json')));
const core=motion.make(model,icons),pairs=[['raf-mek','raf','MEK-substrate','mek','RAF-substrate'],['mek-erk','mek','ERK-substrate','erk','MEK-substrate']];
const frames=[];
for(let t=0;t<=core.duration;t+=.25){const f=core.frame(t),routes=[];for(const[id,source,port,target,targetPort]of pairs){const a=core.anchor(source,port,f.poses[source]),b=core.anchor(target,targetPort,f.poses[target]);const r=arrows.route(a,b,Boolean(f.states[source]));if(r.d){assert.ok(r.d.includes(' L '));assert.ok(a.normal[0]*r.direction[0]+a.normal[1]*r.direction[1]>0);assert.ok(b.normal[0]*r.direction[0]+b.normal[1]*r.direction[1]<0);assert.ok(Math.abs(Math.hypot(r.start[0]-a.point[0],r.start[1]-a.point[1])-16)<1e-8);assert.ok(Math.abs(Math.hypot(r.end[0]-b.point[0],r.end[1]-b.point[1])-12)<1e-8)}routes.push({id,source,target,...r})}frames.push({t,poses:f.poses,routes})}
const same={point:[0,0],normal:[0,1]};assert.equal(arrows.route(same,same,true).d,'');assert.equal(arrows.route(same,{point:[100,100],normal:[0,-1]},false).d,'');
assert.equal(arrows.route({point:[0,0],normal:[0,-1]},{point:[100,100],normal:[0,1]},true).d,'');
const html=fs.readFileSync(path.join(__dirname,'preview.html'),'utf8');for(const block of html.matchAll(/<script>([\s\S]*?)<\/script>/g))new Function(block[1]);
assert.match(html,/markerUnits="userSpaceOnUse"/);assert.match(html,/markerWidth="12"/);
fs.writeFileSync(path.join(__dirname,'qa/arrow-frames.json'),JSON.stringify(frames));
console.log(JSON.stringify({samples:frames.length,directionAndPadding:'passed',hiddenAtContact:true,hiddenWhenInactive:true,arrowheadUnits:'userSpaceOnUse',htmlScriptSyntax:'passed'}));
