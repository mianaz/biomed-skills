/* Run with jsdom available on NODE_PATH; the offline player itself has no dependencies. */
const fs=require('fs'),path=require('path'),{JSDOM}=require('jsdom');
const root=__dirname,dom=new JSDOM(fs.readFileSync(path.join(root,'index.html'),'utf8'),{runScripts:'dangerously',pretendToBeVisual:true}),w=dom.window,d=w.document;
const expected={cascade:{normal:5,block:2},import:{normal:8,block:3},convergence:{normal:7,block:6}},report=[];
for(const id of Object.keys(expected))for(const condition of ['normal','block']){
 d.querySelector('button[data-example="'+id+'"]').click();d.querySelector('#condition').value=condition;d.querySelector('#condition').dispatchEvent(new w.Event('change'));
 const svg=d.querySelector('#scene'),p=svg.querySelectorAll('[data-state="phosphorylated"]').length;
 if(p!==expected[id][condition])throw Error(id+' '+condition+': wrong P-state count');
 if([...svg.querySelectorAll('[data-protein]')].some(e=>e.dataset.icon!=='generic-protein-capsule'))throw Error('Non-capsule protein');
 const ids=[...svg.querySelectorAll('[id]')].map(e=>e.id);if(new Set(ids).size!==ids.length)throw Error('Duplicate SVG IDs');
 svg.setAttribute('width','1000');svg.setAttribute('height','650');fs.writeFileSync(path.join(root,'figures',id+'-'+condition+'.svg'),new w.XMLSerializer().serializeToString(svg));
 report.push({example:id,condition,phosphorylation_badges:p,protein_icon:'generic-protein-capsule',receptors:[...svg.querySelectorAll('[data-receptor]')].map(e=>e.dataset.receptor),time:svg.dataset.time});
}
const frames=[];w.requestAnimationFrame=f=>frames.push(f);w.performance.now=()=>0;d.querySelector('button[data-example="cascade"]').click();d.querySelector('#play').click();for(let i=1;i<=60;i++)frames.shift()(i*1000/60);const playbackTime=+d.querySelector('#scene').dataset.time;if(Math.abs(playbackTime-1)>.02)throw Error('Playback did not advance at 60 fps');
fs.writeFileSync(path.join(root,'state-check.json'),JSON.stringify({states:report,playback:{frames:60,fps:60,time:playbackTime}},null,2)+'\n');w.close();console.log('Exported six editable figures; all condition states and capsule identities passed.');
