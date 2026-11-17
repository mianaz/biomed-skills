/* Imported figures share scheduling with the existing domain-motion engine. */
(function(root){
 const smooth=u=>{u=Math.max(0,Math.min(1,u));return u*u*(3-2*u)};
 function make(scene){
  const ids=new Set(scene.entities.map(e=>e.id)),events=root.DomainMotion.schedule(scene.events);
  if(new Set(events.map(e=>e.id)).size!==events.length)throw Error('Duplicate event ID');
  for(const r of scene.relations||[])if(!ids.has(r.from)||!ids.has(r.to))throw Error('Unknown relation endpoint');
  for(const e of events){
   if(!ids.has(e.actor))throw Error('Unknown actor: '+e.actor);
   if(!['move','reveal','highlight','state'].includes(e.kind))throw Error('Unsupported imported-figure event: '+e.kind);
   if(!(e.duration>0))throw Error('Event duration must be positive: '+e.id);
   if(e.kind==='move'&&![e.to,...(e.via||[])].every(p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite)))throw Error('Move needs finite [dx,dy] offsets: '+e.id);
   if(e.kind==='state'&&!scene.entities.find(x=>x.id===e.actor).parts.some(p=>p.type==='path'&&p.fill!=='none'))throw Error('State recoloring needs native filled paths; use a separate state badge for raster parts.');
  }
  const duration=Math.max(0,...events.map(e=>e.end));
  function frame(t){
   t=Math.max(0,Math.min(duration,t));
   const poses=Object.fromEntries(scene.entities.map(e=>[e.id,{dx:0,dy:0,opacity:e.hidden?0:1,fill:null,highlight:false}]));
   for(const e of events){
    if(t<e.start)continue;
    const p=poses[e.actor],u=smooth((t-e.start)/e.duration);
    if(e.kind==='move'){
     const route=[[p.dx,p.dy],...(e.via||[]),e.to],lengths=route.slice(1).map((b,i)=>Math.hypot(b[0]-route[i][0],b[1]-route[i][1]));
     let distance=u*lengths.reduce((a,b)=>a+b,0),i=0;
     while(i<lengths.length-1&&distance>lengths[i])distance-=lengths[i++];
     const v=lengths[i]?distance/lengths[i]:1;
     [p.dx,p.dy]=route[i].map((a,k)=>a+(route[i+1][k]-a)*v);
     for(const id of e.carry||[]){if(!poses[id])throw Error('Unknown carried object: '+id);Object.assign(poses[id],{dx:p.dx,dy:p.dy})}
    }
    if(e.kind==='reveal')p.opacity=u;
    if(e.kind==='state'&&u>=.5)p.fill=e.fill;
    if(e.kind==='highlight'&&t<e.end)p.highlight=true;
   }
   const active=events.filter(e=>e.start<=t&&t<e.end);
   const current=events.filter(e=>e.start<t&&t<=e.end).at(-1)||events.filter(e=>e.end<=t).at(-1)||events[0];
   return{t,poses,active:active.map(e=>e.id),caption:current?.caption||scene.scope,source:current?.source||''};
  }
  const keyframes=new Set([0,...events.map(e=>e.end)]);
  for(const e of events.filter(e=>e.kind==='highlight'))keyframes.add(e.start+e.duration/2);
  // Morph moves in straight lines; preserve every routed bend as a slide state.
  for(const e of events.filter(e=>e.kind==='move'&&e.via?.length)){
   const p=frame(e.start).poses[e.actor],points=[[p.dx,p.dy],...e.via,e.to];
   const lengths=points.slice(1).map((b,i)=>Math.hypot(b[0]-points[i][0],b[1]-points[i][1]));
   const total=lengths.reduce((a,b)=>a+b,0);let distance=0;
   for(const length of lengths.slice(0,-1)){distance+=length;if(total)keyframes.add(e.start+e.duration*(.5-Math.sin(Math.asin(1-2*distance/total)/3)))}
  }
  return{scene,events,duration,frame,keyframes:[...keyframes].sort((a,b)=>a-b)};
 }
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
 function partSvg(p,pose){
  if(p.type==='path')return `<path d="${esc(p.d)}" fill="${esc(pose.fill&&p.fill!=='none'?pose.fill:p.fill)}" stroke="${esc(p.stroke)}" stroke-width="${p.strokeWidth}" opacity="${p.opacity??1}" fill-opacity="${p.fillOpacity??1}" stroke-opacity="${p.strokeOpacity??1}" stroke-linejoin="${esc(p.linejoin||'miter')}" stroke-linecap="${esc(p.linecap||'butt')}"/>`;
  if(p.type==='text')return `<text x="${p.x}" y="${p.y}" font-family="${esc(p.fontFamily)}" font-size="${p.fontSize}" font-weight="${p.fontWeight||400}" font-style="${esc(p.fontStyle||'normal')}" text-anchor="${p.anchor}" fill="${esc(p.fill)}" opacity="${p.opacity??1}">${esc(p.text)}</text>`;
  return `<image href="${esc(p.href)}" x="${p.bbox[0]}" y="${p.bbox[1]}" width="${p.bbox[2]}" height="${p.bbox[3]}" preserveAspectRatio="none"/>`;
 }
 function svg(scene,frame,selected=''){
  const art=scene.entities.map(e=>{const p=frame.poses[e.id],b=e.bbox;
   return `<g data-entity="${esc(e.id)}" transform="translate(${p.dx} ${p.dy})" opacity="${p.opacity}">${e.parts.map(x=>partSvg(x,p)).join('')}${selected===e.id||p.highlight?`<rect x="${b[0]-5}" y="${b[1]-5}" width="${b[2]+10}" height="${b[3]+10}" fill="none" stroke="#246963" stroke-width="2"/>`:''}</g>`;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${scene.canvas.width} ${scene.canvas.height}" role="img" aria-label="${esc(scene.title)}">${art}</svg>`;
 }
 root.FigureScene={make,svg,esc};if(typeof module!=='undefined')module.exports=root.FigureScene;
})(typeof window==='undefined'?globalThis:window);
