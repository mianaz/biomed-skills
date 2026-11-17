/* Native SVG element model and deterministic display edits. */
window.TunerScene=(()=>{
 const NS='http://www.w3.org/2000/svg',PT=72/25.4,leafTags='text,path,polyline,polygon,line,rect,circle,ellipse,use,image';
 const number=(v,d=0)=>Number.parseFloat(v) || d;
 const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
 const css=n=>Object.fromEntries((n.getAttribute('style')||'').split(';').filter(x=>x.includes(':')).map(x=>{const i=x.indexOf(':');return[x.slice(0,i).trim(),x.slice(i+1).trim()];}));
 const setStyle=(n,patch)=>{const s={...css(n),...patch};n.setAttribute('style',Object.entries(s).filter(([,v])=>v!=null).map(([k,v])=>`${k}:${v}`).join(';'));};
 const color=c=>{if(!c)return'none';c=c.trim().toLowerCase();if(c==='black')return'#000000';if(c==='white')return'#ffffff';if(/^#[0-9a-f]{6}/.test(c))return c.slice(0,7);if(/^#[0-9a-f]{3}$/.test(c))return'#'+[...c.slice(1)].map(x=>x+x).join('');const a=c.match(/^rgba?\(([^)]+)\)/);if(a)return'#'+a[1].split(',').slice(0,3).map(x=>Math.round(Number(x)).toString(16).padStart(2,'0')).join('');return c;};
 function clean(source){
  const doc=new DOMParser().parseFromString(source,'image/svg+xml');if(doc.querySelector('parsererror')||doc.documentElement.localName!=='svg')throw Error('SVG 格式无法读取');
  doc.querySelectorAll('script,foreignObject,iframe,object,embed,audio,video,animate,set').forEach(n=>n.remove());
  for(const n of doc.querySelectorAll('*')){
   for(const a of [...n.attributes])if(/^on/i.test(a.name)||(/(?:^|:)href$/.test(a.name)&&! /^(#|data:image\/(png|jpeg|webp);base64,)/i.test(a.value))||(/url\(/i.test(a.value)&&!/^url\(\s*#[\w:./+=%-]+\s*\)$/.test(a.value)))n.removeAttribute(a.name);
   if(n.localName==='style'){if(/@|url\(\s*['"]?(?!#)/i.test(n.textContent))n.remove();else n.textContent=n.textContent.replace(/([^{}]+)\{/g,(_,s)=>s.split(',').map(x=>'svg[data-tuner-scope] '+x.replace(/svg\[data-tuner-scope\]\s*/g,'').trim()).join(',')+'{');}
  }
  doc.documentElement.setAttribute('data-tuner-scope','');return doc.documentElement;
 }
 function anchor(n){
  if(n.hasAttribute('data-tuner-cx'))return[number(n.getAttribute('data-tuner-cx')),number(n.getAttribute('data-tuner-cy'))];
  const a=k=>number(n.getAttribute(k)),tag=n.localName;
  if(tag==='circle'||tag==='ellipse')return[a('cx'),a('cy')];
  if(tag==='rect')return[a('x')+a('width')/2,a('y')+a('height')/2];
  if(tag==='line')return[(a('x1')+a('x2'))/2,(a('y1')+a('y2'))/2];
  if(tag==='polyline'||tag==='polygon'){const v=(n.getAttribute('points')||'').match(/[-+]?\d*\.?\d+(?:e[-+]?\d+)?/gi)?.map(Number)||[];const x=v.filter((_,i)=>i%2===0),y=v.filter((_,i)=>i%2);return x.length?[(Math.min(...x)+Math.max(...x))/2,(Math.min(...y)+Math.max(...y))/2]:[0,0];}
  let x=a('x'),y=a('y');const t=(n.getAttribute('transform')||'').match(/translate\(\s*([-\d.e+]+)[,\s]+([-\d.e+]+)/i);if(t){x+=Number(t[1]);y+=Number(t[2]);}return[x,y];
 }
 function normalize(layer){
  const svg=clean(layer.svg),old=new Map((layer.elements||[]).map(e=>[e.id,e])),original=new Map([...svg.querySelectorAll('[data-tuner-id]')].map(n=>[n,n.getAttribute('data-tuner-id')]));
  const counters=new Map(),groups=new Map(),elements=[],nodes=[...svg.querySelectorAll(leafTags)].filter(n=>!n.closest('defs,clipPath,mask,marker,pattern'));
  const group=(id,label,role)=>{if(!groups.has(id))groups.set(id,{id,label:label||id,role:role||'group',kind:'group',members:[]});return groups.get(id);};
  nodes.forEach((n,i)=>{
   const owners=[],ancestry=[];let ownerKey;let role=n.getAttribute('data-tuner-role'),name=n.getAttribute('data-tuner-label');
   for(let p=n;p&&p!==svg;p=p.parentElement){ancestry.unshift(p);const owner=p.getAttribute('data-tuner-owner');if(owner){ownerKey ||= owner;owners.push(owner);const o=old.get(owner);group(owner,o?.label,o?.role);}const previous=original.get(p);if(previous&&!/:(svg|node)\d+$/.test(previous)){const o=old.get(previous);owners.push(previous);group(previous,o?.label,o?.role);}const g=p.getAttribute('data-tuner-group');if(g){owners.push(g);group(g,p.getAttribute('data-tuner-group-label'),p.getAttribute('data-tuner-group-role'));}role ||= p.getAttribute('data-tuner-role');}
   ownerKey ||= owners[0]||layer.id;const part=counters.get(ownerKey)||0;counters.set(ownerKey,part+1);const id=`${ownerKey}:node${part}`;
   const tag=n.localName,s=css(n),fill=color(s.fill||n.getAttribute('fill')||(tag==='text'?'black':tag==='line'||tag==='polyline'?'none':'none')),stroke=color(s.stroke||n.getAttribute('stroke')||'none');
   if(tag==='text')role=role?.startsWith('axis')?'text-tick':role||'text';
   else if(tag==='use'&&role==='data-line')role='data-point';
   role ||= tag==='circle'?'data-point':tag==='rect'&&n.getAttribute('width')?.endsWith('%')?'background':'graphic';
   const [cx,cy]=anchor(n),rotation=number((n.getAttribute('transform')||'').match(/rotate\(\s*([-\d.e+]+)/i)?.[1]);
   const e={id,kind:tag==='text'?'text':'shape',tag,role,label:name||(tag==='text'?n.textContent:({ 'data-point':'点','data-line':'曲线','data-bar':'条形','background':'背景','axis-line':'轴线','grid':'网格'}[role]||'图形')+` ${i+1}`),groups:[...new Set(owners)],anchor:[cx,cy],angle_deg:rotation,text_anchor:s['text-anchor']||n.getAttribute('text-anchor')||'start',fill,stroke,font_pt:number(s['font-size']||(s.font||'').match(/([\d.]+)px/)?.[1],11),font_family:(s['font-family']||(s.font||'').match(/px\s+(.+)$/)?.[1]||'Arial').replace(/["']/g,'').split(',')[0].trim(),font_style:s['font-style']||(/italic/.test(s.font||'')?'italic':'normal'),font_weight:s['font-weight']==='bold'||number(s['font-weight'])>=600||/bold/.test(s.font||'')?'bold':'normal',stroke_mm:number(s['stroke-width'],.7)/PT,size_mm:number(n.getAttribute('data-tuner-size'),tag==='circle'?aRadius(n)*2/PT:2),parent_transform:ancestry.slice(0,-1).map(p=>p.getAttribute('transform')||'').join(' ')};
   n.setAttribute('data-tuner-id',id);n.setAttribute('data-tuner-leaf','1');n.setAttribute('data-tuner-role',role);elements.push(e);for(const g of e.groups)group(g).members.push(id);
  });
  const byId=new Map(elements.map(e=>[e.id,e]));
  for(const g of groups.values()){const members=g.members.map(id=>byId.get(id)),texts=members.filter(e=>e.kind==='text');g.has_text=!!texts.length;g.stroke_mm=Math.max(...members.filter(e=>e.kind==='shape'&&e.stroke!=='none').map(e=>e.stroke_mm),0)||.25;g.font_pt=Math.max(...texts.map(e=>e.font_pt),0)||11;g.font_family=texts[0]?.font_family||'Arial';g.font_weight=texts[0]?.font_weight||'normal';g.font_style=texts[0]?.font_style||'normal';const angles=[...new Set(texts.map(e=>e.angle_deg))];g.angle_deg=angles.length===1?angles[0]:null;const anchors=[...new Set(texts.map(e=>e.text_anchor))];g.text_anchor=anchors.length===1?anchors[0]:'';
   if(g.role==='group')g.role=old.get(g.id)?.role||'group';
   if(g.role==='legend'||g.id.includes(':legend')){g.role='legend';g.label='图例';}
   if(/axis[-_.]?(bottom|x)/i.test(g.id)){g.role='axis';g.label='X 坐标轴';}
   if(/axis[-_.]?(left|y)/i.test(g.id)){g.role='axis';g.label='Y 坐标轴';}
   if(g.label?.startsWith(layer.id))g.label='元素组';
  }
  layer.svg=new XMLSerializer().serializeToString(svg);layer.elements=[...groups.values(),...elements];return layer;
 }
 const aRadius=n=>number(n.getAttribute('r'),2);
 const palettes={Paired:['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a'],Set2:['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'],Dark2:['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02'],RdBu:['#2166ac','#67a9cf','#d1e5f0','#f7f7f7','#fddbc7','#ef8a62','#b2182b']};
 function palette(style,n){
  const base=palettes[style.palette];if(!base)return style.colors;if(style.palette!=='RdBu'&&n<=base.length)return base.slice(0,n);
  return Array.from({length:n},(_,i)=>{const at=n===1?(base.length-1)/2:i*(base.length-1)/(n-1),lo=Math.floor(at),hi=Math.min(base.length-1,lo+1),fraction=at-lo;return'#'+[1,3,5].map(k=>Math.round(parseInt(base[lo].slice(k,k+2),16)*(1-fraction)+parseInt(base[hi].slice(k,k+2),16)*fraction).toString(16).padStart(2,'0')).join('');});
 }
 function operations(layer,state,panel){
  const style=state.styles?.[panel.id]||{},all=layer.elements,lookup=new Map(all.map(e=>[e.id,e])),colors=panel.colors||[],mappedPalette=palette(style,colors.length);
  const ops=all.filter(e=>e.kind!=='group').map(e=>{
   const op={id:e.id},patch={};let dx=0,dy=0;
   if(style.theme&&style.theme!=='original'){
    if(e.role==='grid')patch.hidden=true;
    if(e.role==='background')patch.fill='#ffffff';
    if(e.role==='axis-line'&&style.theme==='minimal')patch.hidden=true;
    if(e.role==='axis-line'&&style.theme==='prism')patch.stroke_mm=.35;
    if(e.kind==='text'){patch.font_family='Arial';}
   }
   if(mappedPalette?.length){const source=e.role==='data-line'?e.stroke:e.fill!=='none'&&e.fill!=='#ffffff'?e.fill:e.stroke;const index=colors.indexOf(source);if(index>=0)patch.color=mappedPalette[index%mappedPalette.length];else for(const paint of ['fill','stroke']){const k=colors.indexOf(e[paint]);if(k>=0)patch[paint]=mappedPalette[k%mappedPalette.length];}}
   for(const id of [...e.groups,e.id]){const edit=state.elements[id];if(!edit)continue;dx+=edit.dx_mm||0;dy+=edit.dy_mm||0;Object.assign(patch,edit);if(edit.font_pt!=null&&e.kind==='text'&&id!==e.id)patch.font_pt=edit.font_pt*e.font_pt/(lookup.get(id)?.font_pt||e.font_pt);}
   patch.dx_mm=dx;patch.dy_mm=dy;
   if(e.kind!=='text'){delete patch.font_pt;delete patch.text_anchor;}
   if(patch.angle_deg!=null&&e.kind!=='text'&&e.role==='axis-line'&&state.elements[e.id]?.angle_deg==null)delete patch.angle_deg;
   Object.assign(op,patch);return op;
  }).filter(op=>Object.entries(op).some(([k,v])=>k!=='id'&&((k==='dx_mm'||k==='dy_mm')?v!==0:true)));
  const r=panel.region,first=all.find(e=>e.kind!=='group'&&e.role.startsWith('data-'));
  if(r&&first&&['minimal','bw'].includes(style.theme)){
   const lines=[];for(let i=0;i<=4;i++){const y=(r.y+r.height*i/4)*PT;lines.push(`<line x1="${r.x*PT}" x2="${(r.x+r.width)*PT}" y1="${y}" y2="${y}" style="stroke:#dedede;stroke-width:${.15*PT}px;fill:none"/>`);}if(style.theme==='bw')lines.push(`<rect x="${r.x*PT}" y="${r.y*PT}" width="${r.width*PT}" height="${r.height*PT}" fill="none" stroke="#333"/>`);
   const op=ops.find(o=>o.id===first.id)||{id:first.id};op.before_svg=`<g xmlns="${NS}" data-theme-grid="true" stroke="#dedede" stroke-width="${.15*PT}">${lines.join('')}</g>`;if(!ops.includes(op))ops.push(op);
  }
  return ops;
 }
 function apply(svg,layer,ops){
  const meta=new Map(layer.elements.map(e=>[e.id,e])),nodes=new Map([...svg.querySelectorAll('[data-tuner-id]')].map(n=>[n.dataset.tunerId,n]));
  for(const op of ops){
   const n=nodes.get(op.id);if(!n)continue;const e=meta.get(op.id),s={};
   if(op.hidden)s.display='none';
   if(op.color){if(e.kind==='text')s.fill=op.color;else{if(e.fill!=='none')s.fill=op.color;if(e.stroke!=='none')s.stroke=op.color;}}
   if(op.fill!=null)s.fill=op.fill;if(op.stroke!=null)s.stroke=op.stroke;if(op.stroke_mm!=null&&e.kind!=='text')s['stroke-width']=op.stroke_mm*PT;
   if(op.opacity!=null)s.opacity=op.opacity;if(op.size_mm&&e.role==='data-point')s['stroke-width']=(op.stroke_mm??e.stroke_mm)*PT/(op.size_mm/e.size_mm);
   if(e.kind==='text'){
    if(op.text_anchor){s['text-anchor']=op.text_anchor;n.setAttribute('text-anchor',op.text_anchor);}
    if(op.font_family)s['font-family']=op.font_family;if(op.font_weight)s['font-weight']=op.font_weight;if(op.font_style)s['font-style']=op.font_style;
    if(op.font_pt!=null)s['font-size']=op.font_pt+'px';if(op.font_pt!=null||op.font_family||op.font_weight||op.font_style){n.removeAttribute('textLength');n.removeAttribute('lengthAdjust');}
    if(op.text!=null){n.textContent=op.text;n.removeAttribute('textLength');n.removeAttribute('lengthAdjust');}
   }
   setStyle(n,s);if(op.before_svg){const doc=new DOMParser().parseFromString(op.before_svg,'image/svg+xml');n.before(doc.documentElement);}
   const [cx,cy]=e.anchor,dx=(op.dx_mm||0)*PT,dy=(op.dy_mm||0)*PT,angle=op.angle_deg==null?0:op.angle_deg-e.angle_deg,size=op.size_mm&&e.role==='data-point'?op.size_mm/e.size_mm:1,sx=(op.bar_width_pct&&e.role==='data-bar'?op.bar_width_pct/100:1)*size;
   let transform=`translate(${dx} ${dy}) rotate(${angle} ${cx} ${cy}) translate(${cx} ${cy}) scale(${sx} ${size}) translate(${-cx} ${-cy}) `;
   if(dx||dy){transform+=e.parent_transform+' ';let detached=svg.querySelector('[data-tuner-detached]');if(!detached){detached=document.createElementNS(NS,'g');detached.setAttribute('class','svglite');detached.setAttribute('data-tuner-detached','');svg.append(detached);}detached.append(n);}
   n.setAttribute('transform',transform+(n.getAttribute('transform')||''));
  }return svg;
 }
 function statLabel(a){const p=a.use_adjusted?a.p_adjusted:a.p_value;if(a.display==='stars')return p<.0001?'****':p<.001?'***':p<.01?'**':p<.05?'*':'ns';return`${a.use_adjusted?'adjusted P':'P'} ${p<.0001?'< 0.0001':'= '+Number(p.toPrecision(3))}`;}
 let measureContext;
 function textLines(a,width){
  const paragraphs=(a.text||'').split('\n');if(a.role!=='textbox')return paragraphs;
  if(measureContext===undefined)measureContext=typeof CanvasRenderingContext2D==='undefined'?null:document.createElement('canvas').getContext('2d');
  const size=a.font_pt||11;if(measureContext)measureContext.font=`${a.font_style||'normal'} ${a.font_weight||'normal'} ${size}px ${a.font_family||'Arial'}`;
  const measure=s=>measureContext?measureContext.measureText(s).width:[...s].reduce((n,c)=>n+size*(/[^\u0000-\u00ff]/.test(c)?1:.53),0);
  const lines=[];for(const paragraph of paragraphs){let line='';for(const word of paragraph.match(/\S+\s*|\s+/g)||['']){if(measure(line+word)>width*PT&&line){lines.push(line.trimEnd());line='';}if(measure(word)>width*PT){for(const c of word){if(measure(line+c)>width*PT&&line){lines.push(line);line='';}line+=c;}}else line+=word;}lines.push(line.trimEnd());}return lines;
 }
 function annotations(panel,state){
  const pt=25.4/72,out=[];
  for(const a of (state.annotations||[]).filter(a=>a.panel===panel.id&&!a.hidden)){
   const c=escape(a.color||'#222222'),f=escape(a.fill||'none'),font=(a.font_pt||11)*pt,sw=a.stroke_mm??.25,w=a.width??18,h=a.height??10;
   let content='';
   if(a.type==='text'){
    const lines=textLines(a,Math.max(2,w-2)),align=a.text_anchor||'start',tx=a.role==='textbox'?(align==='middle'?(w-2)/2:align==='end'?w-2:0):0;
    if((a.background&&a.background!=='none')||a.box_border)content+=`<rect x="-1" y="${-font}" width="${w}" height="${Math.max(h,lines.length*font*1.3)}" fill="${escape(a.background||'none')}" stroke="${a.box_border?c:'none'}" stroke-width="${sw}"/>`;
    content+=lines.map((s,i)=>`<text x="${tx}" text-anchor="${escape(align)}" y="${i*font*1.3}" fill="${c}" font-family="${escape(a.font_family||'Arial')}" font-size="${font}" font-weight="${a.font_weight||'normal'}" font-style="${a.font_style||'normal'}">${escape(s)}</text>`).join('');
   }else if(a.type==='rect')content=`<rect width="${w}" height="${h}" fill="${f}" stroke="${c}" stroke-width="${sw}"/>`;
   else if(a.type==='ellipse')content=`<ellipse cx="${w/2}" cy="${h/2}" rx="${w/2}" ry="${h/2}" fill="${f}" stroke="${c}" stroke-width="${sw}"/>`;
   else if(a.type==='line'||a.type==='arrow'){content=`<line x1="0" y1="0" x2="${w}" y2="${h}" stroke="${c}" stroke-width="${sw}"/>`;if(a.type==='arrow'){const angle=Math.atan2(h,w),len=2;content+=`<path d="M ${w-len*Math.cos(angle-.45)} ${h-len*Math.sin(angle-.45)} L ${w} ${h} L ${w-len*Math.cos(angle+.45)} ${h-len*Math.sin(angle+.45)}" fill="none" stroke="${c}" stroke-width="${sw}"/>`;}}
   else if(a.type==='legend')content=(a.items||[]).map((item,i)=>{const setting=state.styles?.[panel.id]||{},mappedPalette=palette(setting,panel.colors.length),index=panel.colors.indexOf(color(item.color));const paint=a.link_palette&&mappedPalette&&index>=0?mappedPalette[index%mappedPalette.length]:item.color;const y=i*(font*1.5);let mark=a.symbol==='line'?`<line x1="0" x2="4" y1="${y-font*.35}" y2="${y-font*.35}" stroke="${escape(paint)}" stroke-width=".4"/>`:a.symbol==='square'?`<rect x=".7" y="${y-font*.7}" width="2" height="2" fill="${escape(paint)}"/>`:`<circle cx="2" cy="${y-font*.35}" r=".8" fill="${escape(paint)}"/>`;return mark+`<text x="6" y="${y}" fill="${c}" font-family="${escape(a.font_family||'Arial')}" font-size="${font}">${escape(item.label)}</text>`;}).join('');
   else if(a.type==='stat')content=`<path data-annotation-part="bracket" transform="translate(${a.bracket_dx_mm||0} ${a.bracket_dy_mm||0}) rotate(${a.bracket_angle_deg||0} ${w/2} 0)" opacity="${a.bracket_opacity??1}" d="M 0 1.4 V 0 H ${w} V 1.4" fill="none" stroke="${c}" stroke-width="${sw}"/><text data-annotation-part="label" data-stat-id="${escape(a.id)}" transform="translate(${a.label_dx_mm||0} ${a.label_dy_mm||0}) rotate(${a.label_angle_deg||0} ${w/2} -1)" opacity="${a.label_opacity??1}" x="${w/2}" y="-1" text-anchor="${escape(a.text_anchor||'middle')}" fill="${escape(a.label_color||a.color||'#222222')}" font-family="${escape(a.font_family||'Arial')}" font-size="${font}">${escape(statLabel(a))}</text>`;
   out.push(`<g data-annotation="${escape(a.id)}" transform="translate(${a.x} ${a.y}) rotate(${a.angle_deg||0})" opacity="${a.opacity??1}">${content}</g>`);
  }
  return `<svg xmlns="${NS}" viewBox="0 0 ${panel.width} ${panel.height}" overflow="visible">${out.join('')}</svg>`;
 }
 function compile(project,state){const copy=structuredClone(state);copy.operations={};copy.overlays=[];
  for(const p of project.panels){if(copy.styles[p.id]){copy.styles[p.id].colors=palette(copy.styles[p.id],p.colors.length);copy.styles[p.id].source_colors=p.colors;}for(const l of p.layers)copy.operations[l.id]=operations(l,state,p);copy.overlays.push({panel_id:p.id,svg:annotations(p,state)});}return copy;
 }
 function composite(project,state){const svg=document.createElementNS(NS,'svg');for(const[k,v]of Object.entries({width:state.canvas.width+'mm',height:state.canvas.height+'mm',viewBox:`0 0 ${state.canvas.width} ${state.canvas.height}`}))svg.setAttribute(k,v);const bg=document.createElementNS(NS,'rect');for(const[k,v]of Object.entries({width:'100%',height:'100%',fill:'white'}))bg.setAttribute(k,v);svg.append(bg);
  for(const p of project.panels){const b=state.panels[p.id],ratio=b.width/p.width;for(const l of p.layers){const pos={...l,...state.layers[l.id]},image=apply(clean(l.svg),l,operations(l,state,p));for(const[k,v]of Object.entries({x:b.x+pos.x*ratio,y:b.y+pos.y*ratio,width:l.width*ratio,height:l.height*ratio,overflow:'visible'}))image.setAttribute(k,v);svg.append(image);}const overlay=clean(annotations(p,state));for(const[k,v]of Object.entries({x:b.x,y:b.y,width:b.width,height:b.height}))overlay.setAttribute(k,v);svg.append(overlay);}return svg;
 }
 return{NS,PT,escape,css,color,clean,normalize,operations,apply,annotations,compile,composite,palettes,palette,statLabel};
})();
