/* Shared entity/anchor choreography. Biology and timing live in the model. */
(function(root){
const mix=(a,b,u)=>a.map((v,i)=>v+(b[i]-v)*u), smooth=u=>{u=Math.max(0,Math.min(1,u));return u*u*(3-2*u)},rot=(p,a)=>[p[0]*Math.cos(a)-p[1]*Math.sin(a),p[0]*Math.sin(a)+p[1]*Math.cos(a)];
function along(points,u){const lengths=points.slice(1).map((p,i)=>Math.hypot(p[0]-points[i][0],p[1]-points[i][1]));let d=u*lengths.reduce((a,b)=>a+b,0),k=0;while(k<lengths.length-1&&d>lengths[k])d-=lengths[k++];return mix(points[k],points[k+1],lengths[k]?d/lengths[k]:1);}
function schedule(events){const done={},pending=[...events],out=[];while(pending.length){const k=pending.findIndex(e=>(e.after||[]).every(id=>done[id]));if(k<0)throw Error('Missing or cyclic event dependency');const e=pending.splice(k,1)[0],start=Math.max(0,...(e.after||[]).map(id=>done[id].end))+(e.delay||0);done[e.id]={...e,start,end:start+e.duration};out.push(done[e.id]);}return out.sort((a,b)=>a.start-b.start||a.id.localeCompare(b.id));}
function make(model,icons){
 const catalog=Object.fromEntries(icons.map(x=>[x.id,x])),entities=Object.fromEntries(model.entities.map(x=>[x.id,x])),events=schedule(model.events),duration=Math.max(...events.map(e=>e.end));
 const layout=model.layout||{},maxSlot=Math.max(1,...model.entities.map(e=>e.slot||0)),width=layout.width||(maxSlot+2)*260,height=layout.height||900,membraneY=layout.membraneY||230;
 const position=e=>[(e.slot+1)*(layout.pitch||260),(layout.zones?.[e.zone]??(e.zone==='surface'?membraneY:e.zone==='opposed'?-25:440))+(e.row||0)*(layout.rowPitch||200)];
 const bases=Object.fromEntries(model.entities.map(e=>{const icon=catalog[e.icon];if(!icon)throw Error('Missing icon '+e.icon);const p={c:position(e),a:e.angle||0,s:e.scale||.8,fy:e.flipY?-1:1};if(e.zone==='surface'&&e.surfaceAnchor){const v=rot(icon.anchors[e.surfaceAnchor].point.map((v,i)=>(v-80)*p.s*(i?p.fy:1)),p.a);p.c[1]-=v[1];}return[e.id,p];}));
 function anchor(id,name,p){const a=catalog[entities[id].icon].anchors[name];if(!a)throw Error('Missing anchor '+id+':'+name);const q=rot(a.point.map((v,i)=>(v-80)*p.s*(i?p.fy:1)),p.a);return {point:p.c.map((v,i)=>v+q[i]),normal:rot([a.normal[0],a.normal[1]*p.fy],p.a)};}
 function dock(id,port,target,targetPort,poses){const a=catalog[entities[id].icon].anchors[port],b=anchor(target,targetPort,poses[target]),p={...poses[id]};p.a=Math.atan2(b.normal[1],b.normal[0])+Math.PI-Math.atan2(a.normal[1]*p.fy,a.normal[0]);p.a=poses[id].a+Math.atan2(Math.sin(p.a-poses[id].a),Math.cos(p.a-poses[id].a));const v=rot(a.point.map((v,i)=>(v-80)*p.s*(i?p.fy:1)),p.a);p.c=b.point.map((x,i)=>x-v[i]);return p;}
 function frame(t){t=Math.max(0,Math.min(duration,t));const poses=Object.fromEntries(Object.entries(bases).map(([k,v])=>[k,{...v,c:[...v.c]}])),links={...(model.initialLinks||{})},states={...(model.initialStates||{})},contacts=[],amounts=Object.fromEntries(model.entities.map(e=>[e.id,e.hidden?0:1]));let active=[];
 const settle=()=>{for(let k=0;k<model.entities.length;k++){let changed=false;for(const [id,l] of Object.entries(links)){const next=dock(id,l.port,l.target,l.targetPort,poses);if(Math.hypot(...next.c.map((v,i)=>v-poses[id].c[i]))>1e-8)changed=true;poses[id]=next;}if(!changed)break;}};
 settle();
 for(const e of events){if(t<e.start)continue;const u=Math.min(1,(t-e.start)/e.duration);if(u<1)active.push(e);const prior={...poses[e.actor],c:[...poses[e.actor].c]};const oldLink=links[e.actor];
 if(e.kind==='dock'){const dest=dock(e.actor,e.port,e.target,e.targetPort,poses);poses[e.actor]={...dest,c:e.approach?along([prior.c,...e.approach,dest.c],smooth(u/.7)):mix(prior.c,dest.c,smooth(u/.7)),a:prior.a+(dest.a-prior.a)*smooth(u/.7)};if(u>=.7){links[e.actor]=e;contacts.push({event:e.id,actor:e.actor,port:e.port,target:e.target,targetPort:e.targetPort});}}
 if(e.kind==='reaction'){delete links[e.actor];const dest=dock(e.actor,e.port,e.target,e.targetPort,poses);const amount=u<.32?smooth(u/.32):u<.7?1:1-smooth((u-.7)/.3);poses[e.actor]={...dest,c:e.approach?along([prior.c,...e.approach,dest.c],amount):mix(prior.c,dest.c,amount),a:prior.a+(dest.a-prior.a)*amount};if(u>=.32&&u<=.7)contacts.push({event:e.id,actor:e.actor,port:e.port,target:e.target,targetPort:e.targetPort});if(u>=.55)states[e.stateTarget||e.target]=e.state;if(u===1&&oldLink)links[e.actor]=oldLink;}
 if(e.kind==='move'||e.kind==='release'){
 delete links[e.actor];const point=q=>q.entity?anchor(q.entity,q.anchor,poses[q.entity]).point.map((v,i)=>v+(q.offset?.[i]||0)):position(q);const route=[prior.c,...(e.via||[]).map(point),e.to?point(e.to):bases[e.target].c];
 const lengths=route.slice(1).map((p,i)=>Math.hypot(p[0]-route[i][0],p[1]-route[i][1]));let distance=smooth(u)*lengths.reduce((a,b)=>a+b,0),k=0;
 while(k<lengths.length-1&&distance>lengths[k])distance-=lengths[k++];poses[e.actor].c=mix(route[k],route[k+1],lengths[k]?distance/lengths[k]:1);
 }
 if(e.kind==='produce'){amounts[e.actor]=smooth(u);if(e.attach){const a=anchor(e.target,e.targetPort,poses[e.target]);if(e.port)poses[e.actor]=dock(e.actor,e.port,e.target,e.targetPort,poses);else poses[e.actor].c=a.point;}}
 if(e.state&&e.kind!=='reaction'&&u>=.7)states[e.stateTarget||e.target||e.actor]=e.state;
 settle();
 }
 if(!active.length)active=[events.filter(e=>e.start<=t).at(-1)||events[0]];
 const focusIds=new Set(active.flatMap(e=>[e.actor,e.target]).filter(id=>entities[id]));for(const id of [...focusIds]){let p=id;while(links[p]){p=links[p].target;focusIds.add(p);}}for(const[id,l]of Object.entries(links))if(focusIds.has(l.target))focusIds.add(id);
 const boxes=[...focusIds].map(id=>{const p=poses[id],r=(entities[id].cameraRadius||100)*p.s;return[p.c[0]-r,p.c[1]-r,p.c[0]+r,p.c[1]+r];});const b=[Math.min(...boxes.map(x=>x[0]))-50,Math.min(...boxes.map(x=>x[1]))-45,Math.max(...boxes.map(x=>x[2]))+50,Math.max(...boxes.map(x=>x[3]))+45];const w=Math.max(440,b[2]-b[0]),h=Math.max(330,b[3]-b[1]);
 return{t,poses,links,states,contacts,amounts,active,focusIds:[...focusIds],camera:[(b[0]+b[2]-w)/2,(b[1]+b[3]-h)/2,w,h]};
 }
 function checks(){const errors=[];let count=0,maxGap=0,maxNormalError=0;for(let t=0;t<=duration;t+=.25){const f=frame(t);count++;for(const c of f.contacts){if(f.links[c.actor]?.id!==c.event&&!f.active.some(e=>e.id===c.event&&e.kind==='reaction'))continue;const a=anchor(c.actor,c.port,f.poses[c.actor]),b=anchor(c.target,c.targetPort,f.poses[c.target]);const gap=Math.hypot(...a.point.map((v,i)=>v-b.point[i]));maxGap=Math.max(maxGap,gap);maxNormalError=Math.max(maxNormalError,Math.hypot(a.normal[0]+b.normal[0],a.normal[1]+b.normal[1]));if(gap>1e-5)errors.push({t,event:c.event,gap});}for(const p of Object.values(f.poses))if(![...p.c,p.a,p.s].every(Number.isFinite))errors.push({t,kind:'invalid pose'});}return{samples:count,maxGap,maxNormalError,errors};}
 return{model,entities,catalog,events,duration,width,height,membraneY,bases,anchor,frame,checks};
}
root.DomainMotion={make,schedule};if(typeof module!=='undefined')module.exports=root.DomainMotion;
})(typeof window==='undefined'?globalThis:window);
