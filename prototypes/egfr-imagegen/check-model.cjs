const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const DomainMotion=require('../biomedical-manim/domain-motion.js');
const model=JSON.parse(fs.readFileSync(path.join(__dirname,'mechanism.json')));
const icons=JSON.parse(fs.readFileSync(path.join(__dirname,'../../skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/manifest.json')));
const core=DomainMotion.make(model,icons),geometry=core.checks();
assert.equal(geometry.errors.length,0);
let membraneError=0,exchangeGap=0;
for(let t=0;t<=core.duration;t+=.25){const f=core.frame(t);for(const id of ['r1','r2','ras']){const point=core.anchor(id,'membrane',f.poses[id]).point;membraneError=Math.max(membraneError,Math.abs(point[1]-(id==='ras'?312:300)))}if(t>=17){const a=core.anchor('sos','RAS-exchange',f.poses.sos).point,b=core.anchor('ras','SOS-contact',f.poses.ras).point;exchangeGap=Math.max(exchangeGap,Math.hypot(a[0]-b[0],a[1]-b[1]))}}
assert.ok(membraneError<1e-5);assert.ok(exchangeGap<1e-5);
assert.equal(core.frame(0).links.sos.target,'grb');
const final=core.frame(core.duration);assert.equal(final.states.ras,'GTP');assert.equal(final.states.erk,'pT/pY');
assert.equal(final.links.sos.target,'grb');assert.equal(final.links.grb.target,'r1');assert.equal(final.links.raf.target,'ras');
const blocked=structuredClone(model);blocked.events=blocked.events.filter(e=>['bind-a','bind-b','dimer'].includes(e.id));
const stopped=DomainMotion.make(blocked,icons);const blockedFinal=stopped.frame(stopped.duration);
assert.equal(blockedFinal.states.ras,'GDP');assert.equal(blockedFinal.states.erk,undefined);
const report={samples:geometry.samples,maxContactGap:geometry.maxGap,maxNormalError:geometry.maxNormalError,maxMembraneError:membraneError,maxExchangeGap:exchangeGap,finalStates:final.states,blockedStates:blockedFinal.states};
fs.mkdirSync(path.join(__dirname,'qa'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'qa/model-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
