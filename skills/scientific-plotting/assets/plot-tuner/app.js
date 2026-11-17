const $=id=>document.getElementById(id),S=window.TunerScene,T=window.TunerStats,clone=x=>structuredClone(x);
let elementMap=new Map();
let project,state,selection,selected=[],past=[],future=[],drag,scale=Number($('zoom').value),toastTimer,frame;
let statsRows=[],statsResults=[],statsFileName='';
const note=text=>{$('status').textContent=text;$('status').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('status').classList.remove('visible'),2600);};
const panels=()=>project?.panels||[],panelById=id=>panels().find(p=>p.id===id),layers=()=>panels().flatMap(p=>p.layers),layerById=id=>layers().find(l=>l.id===id);
const elementById=id=>elementMap.get(id),annotationById=id=>state.annotations.find(a=>a.id===id);
const defaults=p=>({x:p.x,y:p.y,width:p.width,height:p.height});
const checkpoint=()=>{past.push(clone(state));if(past.length>40)past.shift();future=[];};
const change=action=>{if(!project)return;checkpoint();try{action();render();}catch(error){state=past.pop();note(error.message);render();}};
const activePanel=()=>panelById(selection?.panel||selected[0])||panels()[0];
const targets=()=>$('style-scope').value==='all'?panels():selected.length?selected.map(panelById):[activePanel()];
const newId=prefix=>prefix+(state.next_id++);
const textOf=e=>e.kind==='text'||(e.kind==='group'&&(e.has_text??e.members.some(id=>elementById(id)?.kind==='text')));
const selectedEdit=()=>{if(selection?.type!=='annotation')return state.elements[selection?.id]||{};const a=annotationById(selection.id),part=selection.part;return part?{...a,x:a[part+'_dx_mm']||0,y:a[part+'_dy_mm']||0,angle_deg:a[part+'_angle_deg']||0,color:a[part+'_color']||a.color,opacity:a[part+'_opacity']??1}:a;};
function openProject(data){
 data.stat_object=typeof data.stat_object==='string'?data.stat_object:null;if(data.stat_data&&!Object.keys(data.stat_data).length)data.stat_data=null;
 if(data.schema!=='bioinfospace.plot-tuner/2'||!['ggplot2','matplotlib'].includes(data.engine)||!Array.isArray(data.panels)||!data.panels.length||data.panels.length>32)throw Error('请打开绘图助手导出的 project.json');
 for(const p of data.panels){p.region={x:7,y:12,width:p.width-14,height:p.height-24,...p.region};p.layers.forEach(S.normalize);for(const l of p.layers)if(l.role==='legend'){const members=l.elements.filter(e=>e.kind!=='group').map(e=>e.id),id=l.id+':legend-block';l.elements.push({id,kind:'group',role:'legend',label:'图例',members,font_pt:Math.max(...l.elements.filter(e=>e.kind==='text').map(e=>e.font_pt),11)});l.elements.filter(e=>e.kind!=='group').forEach(e=>e.groups.push(id));}}
 elementMap=new Map(data.panels.flatMap(p=>p.layers).flatMap(l=>l.elements).map(e=>[e.id,e]));
 project=data;state=clone(data.settings||{schema:data.schema,canvas:data.canvas,panels:Object.fromEntries(data.panels.map(p=>[p.id,defaults(p)])),layers:{},elements:{}});
 state.styles||={};state.annotations||=[];state.stat_sources||={};state.next_id||=1;delete state.operations;delete state.overlays;
 for(const p of panels()){const b=state.panels[p.id];if(!b||![b.x,b.y,b.width,b.height].every(Number.isFinite)||b.width<=0||b.height<=0)throw Error('面板尺寸无效');p.colors=p.legend_items?.length?[...new Set(p.legend_items.map(x=>S.color(x.color)))]:[...new Set(p.layers.flatMap(l=>l.elements).filter(e=>e.kind!=='group'&&e.role.startsWith('data-')).map(e=>S.color(e.role==='data-line'?e.stroke:e.fill!=='none'&&e.fill!=='#ffffff'?e.fill:e.stroke)).filter(c=>c!=='none'))];}
 past=[];future=[];selected=[];selection=null;render();note('项目已打开 · 可从左侧选坐标轴或数据系列');
}
function selectPanel(id,multiple=false){selected=multiple?(selected.includes(id)?selected.filter(x=>x!==id):[...selected,id]):[id];selection={type:'panel',id,panel:id};}
function chooseElement(id,panel){selection={type:'element',id,panel};selected=[panel];}
function setSelection(type,id,panel){selection={type,id,panel};selected=[panel];$('pick-mode').value=type==='element'&&elementById(id)?.kind==='group'?'group':'element';render();}
function makeSelectionBox(){
 const old=$('paper').querySelector('.selection-box');old?.remove();if(!selection||selection.type==='panel')return;
 const selectedModel=selection.type==='element'?elementById(selection.id):null,members=new Set(selectedModel?.members||[selection.id]);
 const nodes=selection.type==='annotation'?[...$('paper').querySelectorAll('[data-annotation]')].filter(n=>n.dataset.annotation===selection.id).map(n=>selection.part?n.querySelector('[data-annotation-part="'+selection.part+'"]'):n).filter(Boolean):[...$('paper').querySelectorAll('[data-tuner-id]')].filter(n=>{return members.has(n.dataset.tunerId);});
 const rects=nodes.map(n=>n.getBoundingClientRect()).filter(r=>r.width||r.height);if(!rects.length)return;
 const r=$('paper').getBoundingClientRect(),x=Math.min(...rects.map(r=>r.left)),y=Math.min(...rects.map(r=>r.top)),right=Math.max(...rects.map(r=>r.right)),bottom=Math.max(...rects.map(r=>r.bottom));
 const box=document.createElement('div');box.className='selection-box';Object.assign(box.style,{left:x-r.left-3+'px',top:y-r.top-3+'px',width:right-x+6+'px',height:bottom-y+6+'px'});
 if(selection.type==='annotation'&&!selection.part){const handle=document.createElement('span');handle.className='annotation-handle';handle.dataset.annotationResize=selection.id;box.append(handle);}$('paper').append(box);
}
function render(){
 if(!project)return;$('paper').replaceChildren();Object.assign($('paper').style,{width:state.canvas.width*scale+'px',height:state.canvas.height*scale+'px'});$('paper').classList.toggle('bounds-off',!$('show-bounds').checked);
 for(const p of panels()){
  const b=state.panels[p.id],ratio=b.width/p.width,holder=document.createElement('div');holder.className='panel';holder.dataset.panel=p.id;holder.classList.toggle('selected',selected.includes(p.id));Object.assign(holder.style,{left:b.x*scale+'px',top:b.y*scale+'px',width:b.width*scale+'px',height:b.height*scale+'px'});
  const tag=document.createElement('button');tag.className='panel-tag';tag.dataset.move=p.id;tag.textContent=p.name;holder.append(tag);
  for(const l of p.layers){const pos={...l,...state.layers[l.id]},div=document.createElement('div');div.className='layer '+l.role;div.dataset.layer=l.id;Object.assign(div.style,{left:pos.x*ratio*scale+'px',top:pos.y*ratio*scale+'px',width:l.width*ratio*scale+'px',height:l.height*ratio*scale+'px'});
   const svg=S.apply(S.clean(l.svg),l,S.operations(l,state,p));
   for(const n of svg.querySelectorAll('[data-tuner-id]')){if(selection?.type==='element'&&n.dataset.tunerId===selection.id)n.classList.add('picked');
    if(['line','polyline','path'].includes(n.localName)&&S.css(n).display!=='none'){const hit=n.cloneNode(true);hit.classList.add('object-hit');hit.removeAttribute('data-tuner-id');hit.setAttribute('data-tuner-hit',n.dataset.tunerId);hit.setAttribute('style','fill:none;stroke:transparent;stroke-width:7px;pointer-events:stroke');n.before(hit);}}
   div.append(svg);holder.append(div);
  }
  const overlay=document.createElement('div');overlay.className='overlay';const svg=S.clean(S.annotations(p,state));svg.querySelectorAll('[data-annotation]').forEach(n=>n.classList.toggle('picked',selection?.type==='annotation'&&selection.id===n.dataset.annotation));overlay.append(svg);holder.append(overlay);
  const handle=document.createElement('span');handle.className='resize';handle.dataset.resize=p.id;holder.append(handle);$('paper').append(holder);
 }
 $('panel-list').replaceChildren();for(const p of panels()){const button=document.createElement('button');button.className='panel-row';button.classList.toggle('selected',selected.includes(p.id));button.textContent=p.name+'  '+state.panels[p.id].width.toFixed(1)+' mm';button.onclick=e=>{selectPanel(p.id,e.shiftKey);render();};$('panel-list').append(button);}
 $('project-name').textContent=project.name;$('engine').textContent=project.engine==='ggplot2'?'R / ggplot2':'Python / matplotlib';$('dimensions').textContent=`${state.canvas.width.toFixed(1)} × ${state.canvas.height.toFixed(1)} mm`;
 $('canvas-width').value=state.canvas.width;$('canvas-height').value=state.canvas.height;$('undo').disabled=!past.length;$('redo').disabled=!future.length;
 const p=activePanel(),style=state.styles[p.id]||{};$('theme').value=style.theme||'original';$('palette').value=style.palette||'original';
 renderTree();renderColors();inspect();audit();makeSelectionBox();
}
function renderTree(){
 const list=$('element-list'),filter=$('element-search').value.trim().toLowerCase();list.replaceChildren();let count=0;
 for(const p of panels()){
  const group=document.createElement('optgroup');group.label=p.name;
  const all=p.layers.flatMap(l=>l.elements),semantic=all.filter(e=>e.kind==='group'&&(e.role==='axis'||e.role==='series'||e.role==='legend'||e.role.startsWith('data-'))),texts=all.filter(e=>e.kind==='text'),shapes=all.filter(e=>e.kind==='shape');
  for(const e of [...semantic,...texts,...shapes]){if(count>=350)break;if(filter&&!`${e.label} ${e.role}`.toLowerCase().includes(filter))continue;const option=document.createElement('option');option.value=JSON.stringify(['element',e.id,p.id]);option.textContent=(e.kind==='group'?'▣ ':e.kind==='text'?'T ':'◇ ')+e.label;option.selected=selection?.id===e.id;if(state.elements[e.id]?.hidden)option.textContent='[隐藏] '+option.textContent;group.append(option);count++;}
  for(const a of state.annotations.filter(a=>a.panel===p.id)){if(filter&&!`${a.text||a.type}`.toLowerCase().includes(filter))continue;const option=document.createElement('option');option.value=JSON.stringify(['annotation',a.id,p.id]);option.textContent='＋ '+(a.type==='stat'?`${a.group1} / ${a.group2}`:a.text?.split('\n')[0]||{legend:'新增图例',rect:'矩形',ellipse:'椭圆',line:'直线',arrow:'箭头'}[a.type]);option.selected=selection?.id===a.id;group.append(option);}
  list.append(group);
 }
 if(!selection)list.selectedIndex=-1;
}
function renderColors(){
 const p=activePanel(),style=state.styles[p.id]||{},palette=S.palette(style,p.colors.length)||p.colors;$('palette-colors').replaceChildren();
 p.colors.forEach((original,i)=>{const row=document.createElement('label');row.className='palette-entry';const input=document.createElement('input');input.type='color';input.value=palette[i%palette.length]||original;input.setAttribute('aria-label',`颜色 ${i+1}`);input.onchange=()=>change(()=>{for(const target of targets()){const current=state.styles[target.id]||{},colors=[...(S.palette(current,target.colors.length)||target.colors)];const index=target.colors.indexOf(original);if(index>=0)colors[index]=input.value;state.styles[target.id]={...current,palette:'custom',colors};}});row.append(input,document.createTextNode(p.legend_items?.find(x=>S.color(x.color)===original)?.label||`颜色 ${i+1}`));$('palette-colors').append(row);});
}
function inspect(){
 $('inspector').hidden=!selection;if(!selection){$('selection-title').textContent='选择一个元素';$('selection-desc').textContent='点击画布，或从左侧元素列表选择。';return;}
 const {type,id}=selection,e=type==='element'?elementById(id):null,a=type==='annotation'?annotationById(id):null,edit=selectedEdit(),isText=!!(a&&['text','legend','stat'].includes(a.type)&&selection.part!=='bracket'||e&&textOf(e));
 $('selection-title').textContent=type==='panel'?panelById(id).name:a?(a.type==='stat'?`${a.group1} / ${a.group2}`:a.text?.split('\n')[0]||a.type):e.label;
 $('selection-desc').textContent=type==='panel'?'位置以画布左上角为原点。':a?(selection.part?'相对统计标注的独立位移；可用对象组模式移动整体。':'位置以所在面板左上角为原点。'):e.kind==='group'?'对象组：同时编辑该组的文字与图形。':'单个元素：位移相对原始位置，向右、向下为正。';
 $('item-x').value=type==='panel'?state.panels[id].x:a?edit.x:edit.dx_mm||0;$('item-y').value=type==='panel'?state.panels[id].y:a?edit.y:edit.dy_mm||0;
 $('text-controls').hidden=!isText;$('text-content').parentElement.hidden=!(a?.type==='text'||e?.kind==='text');$('text-content').value=a?.text??edit.text??e?.label??'';
 const nativeAnchor=e?.groups?.reduce((value,id)=>state.elements[id]?.text_anchor??value,e?.text_anchor);
 $('text-anchor').value=edit.text_anchor??nativeAnchor??e?.text_anchor??(a?.type==='stat'?'middle':'start');$('text-anchor-label').hidden=a?.type==='legend';$('anchor-hint').hidden=a?.type==='legend';$('anchor-hint').textContent=a?.role==='textbox'?'在文本框内沿文字方向对齐。':'沿文字方向对齐；旋转时固定所选对齐点。';
 const groupFont=e?.font_pt;
 $('font-size').value=edit.font_pt??groupFont??11;$('font-family').value=edit.font_family||e?.font_family||'Arial';$('font-weight').value=edit.font_weight||e?.font_weight||'normal';$('font-style').value=edit.font_style||e?.font_style||'normal';$('rotation').value=edit.angle_deg??e?.angle_deg??(e?.kind==='group'?'':0);$('rotation').placeholder=e?.kind==='group'?'混合原始角度':'';$('rotation').parentElement.hidden=!!e&&e.kind==='group'&&!isText;$('rotation').parentElement.childNodes[0].textContent=e?.kind==='group'?'文字旋转 ':'旋转 ';
 $('width-label').hidden=type!=='panel';$('panel-width').value=type==='panel'?state.panels[id].width:50;$('paint-controls').hidden=type==='panel';
 const members=e?.kind==='group'?e.members.map(elementById):e?[e]:[];
 const point=members.some(x=>x.role==='data-point'),bar=members.some(x=>x.role==='data-bar');
 $('point-label').hidden=!point;$('bar-label').hidden=!bar;$('point-size').value=edit.size_mm??members.find(x=>x.role==='data-point')?.size_mm??2;$('bar-width').value=edit.bar_width_pct??100;
 $('item-color').value=S.color(edit.color||e?.fill!=='none'&&e?.fill||e?.stroke||'#222222').match(/^#[0-9a-f]{6}$/i)?.[0]||'#222222';
 $('item-opacity').value=edit.opacity??1;$('stroke-width').value=edit.stroke_mm??e?.stroke_mm??.25;$('stroke-label').hidden=!!e&&e.kind==='text'||selection.part==='label';$('fill-label').hidden=type==='panel';$('item-fill').value=a?.type==='text'?a.background||'none':edit.fill||e?.fill||'none';
 $('object-dimensions').hidden=!a||selection.part==='label';$('object-width').value=a?.width??18;$('object-height').value=a?.height??10;
 $('legend-controls').hidden=a?.type!=='legend';$('legend-items').value=(a?.items||[]).map(x=>`${x.label} | ${x.color}`).join('\n');$('legend-symbol').value=a?.symbol||'circle';
 $('stat-controls').hidden=a?.type!=='stat';if(a?.type==='stat'){$('stat-display').value=a.display;$('stat-value').value=a.use_adjusted?'adjusted':'raw';$('stat-value').querySelector('[value=raw]').disabled=a.p_value==null;$('stat-summary').textContent=`${a.method==='provided'?(a.provided_method||'导入结果'):a.method} · ${a.group1} / ${a.group2}\nn = ${a.n1??'—'}, ${a.n2??'—'} · ${a.adjustment} · 本比较族 ${state.annotations.filter(x=>x.type==='stat'&&x.family===a.family).length} 项\nP = ${a.p_value??'未提供'}\n校正 P = ${a.p_adjusted}\n${a.source_name||'项目观测值'}`;}
 $('box-border-label').hidden=a?.role!=='textbox';$('box-border').checked=!!a?.box_border;$('item-hidden').checked=!!edit.hidden;$('bring-front').disabled=!a;$('send-back').disabled=!a;
}
function audit(){
 let minimum=Infinity;const changes=[];
 for(const p of panels()){const b=state.panels[p.id],ratio=b.width/p.width;for(const l of p.layers){const ops=new Map(S.operations(l,state,p).map(o=>[o.id,o]));for(const e of l.elements.filter(e=>e.kind==='text')){const op=ops.get(e.id)||{};if(!op.hidden)minimum=Math.min(minimum,(op.font_pt??e.font_pt)*ratio);}}
  if(JSON.stringify(b)!==JSON.stringify(defaults(p)))changes.push(`${p.name}：${b.x.toFixed(1)}, ${b.y.toFixed(1)} mm · ${b.width.toFixed(1)} × ${b.height.toFixed(1)} mm`);
  if(state.styles[p.id]&&Object.keys(state.styles[p.id]).length)changes.push(`${p.name}：${state.styles[p.id].theme||'原始样式'} / ${state.styles[p.id].palette||'原配色'}`);
 }
 for(const[id,edit]of Object.entries(state.elements))changes.push(`${(elementById(id)?.label||'元素').slice(0,24)}：${edit.font_pt?edit.font_pt+' pt · ':''}${edit.angle_deg!=null?edit.angle_deg+'° · ':''}位移 ${(edit.dx_mm||0).toFixed(1)}, ${(edit.dy_mm||0).toFixed(1)} mm${edit.hidden?' · 隐藏':''}`);
 for(const a of state.annotations){if(!a.hidden&&a.font_pt)minimum=Math.min(minimum,a.font_pt*state.panels[a.panel].width/panelById(a.panel).width);changes.push(`新增 ${a.type==='stat'?S.statLabel(a):a.text?.slice(0,20)||a.type}`);}
 const outside=panels().some(p=>{const b=state.panels[p.id];return b.x<0||b.y<0||b.x+b.width>state.canvas.width+.01||b.y+b.height>state.canvas.height+.01;});
 $('font-check').textContent=`最小有效字号 ${Number.isFinite(minimum)?minimum.toFixed(1):'—'} pt${minimum<8?' · 低于 8 pt':minimum<=10?' · 可再放大文字':' · 达到目标'}${outside?'。有面板超出画布。':''}`;$('font-check').classList.toggle('warn',minimum<=10||outside);
 $('changes').replaceChildren();for(const text of changes.length?changes:['尚无编辑']){const li=document.createElement('li');li.textContent=text;$('changes').append(li);}
}
function point(event){const b=$('paper').getBoundingClientRect();return{x:(event.clientX-b.left)/scale,y:(event.clientY-b.top)/scale};}
function start(event){
 if(!project||event.button!==0)return;const resize=event.target.closest('[data-resize]'),tag=event.target.closest('[data-move]'),annResize=event.target.closest('[data-annotation-resize]'),annotation=event.target.closest('[data-annotation]'),layerNode=event.target.closest('[data-layer]'),panelNode=event.target.closest('[data-panel]');
 if(annResize){selection={type:'annotation',id:annResize.dataset.annotationResize,panel:annotationById(annResize.dataset.annotationResize).panel};drag={type:'annotation-resize',id:selection.id,panel:selection.panel};}
 else if(resize||tag||$('pick-mode').value==='panel'&&panelNode){const id=(resize||tag)?.dataset[resize?'resize':'move']||panelNode.dataset.panel;if(event.shiftKey){selectPanel(id,true);render();return;}if(!selected.includes(id))selectPanel(id);else selection={type:'panel',id,panel:id};drag={type:resize?'resize':'panel',id,ids:[...selected]};}
 else if(annotation){const id=annotation.dataset.annotation;selection={type:'annotation',id,panel:panelNode.dataset.panel};const part=event.target.closest('[data-annotation-part]');if(part&&$('pick-mode').value==='element')selection.part=part.dataset.annotationPart;selected=[selection.panel];drag={...selection};}
 else if(layerNode){const native=event.target.closest('[data-tuner-id]'),hit=event.target.closest('[data-tuner-hit]'),id=native?.dataset.tunerId||hit?.dataset.tunerHit;if(!id)return;const e=elementById(id),layer=layerById(layerNode.dataset.layer);let target=id;if(event.altKey||$('pick-mode').value==='group'){const semantic=e.groups.map(elementById).find(g=>g?.role==='axis'||g?.role==='legend'||g?.role==='series'||g?.role?.startsWith('data-'));target=semantic?.id||e.groups[0]||id;}chooseElement(target,panelNode.dataset.panel);drag={...selection};}
 else{selection=null;selected=[];render();return;}
 drag.start=point(event);drag.before=clone(state);event.preventDefault();render();
}
function moving(event){
 if(!drag)return;const at=point(event),dx=at.x-drag.start.x,dy=at.y-drag.start.y,snap=$('snap').checked?Math.round:x=>Math.round(x*100)/100,before=drag.before;
 if(drag.type==='panel')for(const id of drag.ids){state.panels[id].x=snap(before.panels[id].x+dx);state.panels[id].y=snap(before.panels[id].y+dy);}
 if(drag.type==='resize'){const b=before.panels[drag.id],w=Math.max(10,snap(b.width+dx));state.panels[drag.id].width=w;state.panels[drag.id].height=b.height*w/b.width;}
 const ratio=drag.panel?state.panels[drag.panel].width/panelById(drag.panel).width:1;
 if(drag.type==='element'){const e=before.elements[drag.id]||{};state.elements[drag.id]={...e,dx_mm:snap((e.dx_mm||0)+dx/ratio),dy_mm:snap((e.dy_mm||0)+dy/ratio)};}
 if(drag.type==='annotation'){const a=annotationById(drag.id),old=before.annotations.find(a=>a.id===drag.id);if(drag.part){a[drag.part+'_dx_mm']=snap((old[drag.part+'_dx_mm']||0)+dx/ratio);a[drag.part+'_dy_mm']=snap((old[drag.part+'_dy_mm']||0)+dy/ratio);}else{a.x=snap(old.x+dx/ratio);a.y=snap(old.y+dy/ratio);}}
 if(drag.type==='annotation-resize'){const a=annotationById(drag.id),old=before.annotations.find(a=>a.id===drag.id);a.width=Math.max(.2,snap((old.width||18)+dx/ratio));a.height=Math.max(.2,snap((old.height||10)+dy/ratio));}
 if(!frame)frame=requestAnimationFrame(()=>{frame=null;render();});
}
function end(){if(!drag)return;if(frame){cancelAnimationFrame(frame);frame=null;}if(JSON.stringify(drag.before)!==JSON.stringify(state)){past.push(drag.before);future=[];}drag=null;render();}
$('paper').addEventListener('pointerdown',start);window.addEventListener('pointermove',moving);window.addEventListener('pointerup',end);window.addEventListener('pointercancel',end);
function editProperty(key,value){if(!selection)return;if(selection.type==='annotation'){const a=annotationById(selection.id),part=selection.part;const mapped=part?key==='x'?part+'_dx_mm':key==='y'?part+'_dy_mm':key==='angle_deg'?part+'_angle_deg':key==='opacity'?part+'_opacity':key==='color'&&part==='label'?'label_color':key:key;a[mapped]=value;}else if(selection.type==='element')state.elements[selection.id]={...state.elements[selection.id],[key]:value};}
for(const [control,axis]of [['item-x','x'],['item-y','y']])$(control).onchange=()=>change(()=>{const value=Number($(control).value);if(!Number.isFinite(value)||!selection)return;if(selection.type==='panel')state.panels[selection.id][axis]=value;else editProperty(selection.type==='annotation'?axis:axis==='x'?'dx_mm':'dy_mm',value);});
for(const [control,key]of [['font-size','font_pt'],['rotation','angle_deg'],['stroke-width','stroke_mm'],['point-size','size_mm'],['bar-width','bar_width_pct'],['item-opacity','opacity'],['object-width','width'],['object-height','height']])$(control).onchange=()=>change(()=>{const value=Number($(control).value);if(!Number.isFinite(value))throw Error('请输入有效数值');if((key==='font_pt'||key==='size_mm'||key==='width')&&value<=0)throw Error('尺寸必须大于零');editProperty(key,value);});
for(const[control,key]of [['text-content','text'],['font-family','font_family'],['font-weight','font_weight'],['font-style','font_style'],['text-anchor','text_anchor'],['item-color','color'],['legend-symbol','symbol'],['stat-display','display']])$(control).onchange=()=>change(()=>editProperty(key,$(control).value));
$('item-fill').onchange=()=>change(()=>{const value=$('item-fill').value.trim();if(value!=='none'&&!/^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(value))throw Error('填充请输入 none 或十六进制颜色');editProperty(selection.type==='annotation'&&annotationById(selection.id).type==='text'?'background':'fill',value);});
$('box-border').onchange=()=>change(()=>editProperty('box_border',$('box-border').checked));
$('item-hidden').onchange=()=>change(()=>editProperty('hidden',$('item-hidden').checked));
$('stat-value').onchange=()=>change(()=>editProperty('use_adjusted',$('stat-value').value==='adjusted'));
$('legend-items').onchange=()=>change(()=>{const items=$('legend-items').value.split('\n').filter(s=>s.trim()).map(line=>{const[label,color]=line.split('|').map(s=>s.trim());if(!label||!/^#[0-9a-f]{6}$/i.test(color))throw Error('图例每行输入：名称 | #颜色');return{label,color};});editProperty('items',items);editProperty('link_palette',false);});
$('panel-width').onchange=()=>change(()=>{const b=state.panels[selection.id],width=Number($('panel-width').value);if(width<10||width>1000)throw Error('面板宽度应在 10–1000 mm');b.height*=width/b.width;b.width=width;});
for(const[control,axis]of [['canvas-width','width'],['canvas-height','height']])$(control).onchange=()=>change(()=>{const value=Number($(control).value);if(value<10||value>2000)throw Error('画布尺寸应在 10–2000 mm');state.canvas[axis]=value;});
$('element-list').onchange=()=>{if($('element-list').value)setSelection(...JSON.parse($('element-list').value));};$('element-search').oninput=renderTree;
$('zoom').onchange=()=>{scale=Number($('zoom').value);render();};$('show-bounds').onchange=render;
$('undo').onclick=()=>{if(past.length){future.push(clone(state));state=past.pop();if(selection?.type==='annotation'&&!annotationById(selection.id))selection=null;render();}};$('redo').onclick=()=>{if(future.length){past.push(clone(state));state=future.pop();if(selection?.type==='annotation'&&!annotationById(selection.id))selection=null;render();}};
$('reset-item').onclick=()=>change(()=>{if(selection.type==='panel')state.panels[selection.id]=defaults(panelById(selection.id));else if(selection.type==='element')delete state.elements[selection.id];else{const a=annotationById(selection.id);Object.assign(a,{angle_deg:0,opacity:1,font_pt:11,color:'#222222',hidden:false});}});
function removeSelection(){if(!selection)return;change(()=>{if(selection.type==='annotation')state.annotations=state.annotations.filter(a=>a.id!==selection.id);else if(selection.type==='element')editProperty('hidden',true);selection=null;});}
$('delete-item').onclick=removeSelection;
for(const[id,front]of [['bring-front',true],['send-back',false]])$(id).onclick=()=>change(()=>{const a=annotationById(selection.id);state.annotations=state.annotations.filter(x=>x.id!==a.id);state.annotations[front?'push':'unshift'](a);});
for(const[control,axis]of [['align-left','x'],['align-top','y']])$(control).onclick=()=>{if(selected.length<2)return note('Shift + 点击选择至少两个面板');change(()=>{const value=Math.min(...selected.map(id=>state.panels[id][axis]));selected.forEach(id=>state.panels[id][axis]=value);});};
$('distribute').onclick=()=>{if(selected.length<3)return note('选择至少三个面板以水平等距');change(()=>{const boxes=selected.map(id=>state.panels[id]).sort((a,b)=>a.x-b.x),first=boxes[0],last=boxes.at(-1),gap=(last.x+last.width-first.x-boxes.reduce((n,b)=>n+b.width,0))/(boxes.length-1);let x=first.x;for(const b of boxes){b.x=x;x+=b.width+gap;}});};
for(const control of ['theme','palette'])$(control).onchange=()=>change(()=>{const value=$(control).value;for(const p of targets())state.styles[p.id]={...state.styles[p.id],[control]:value};});
function addObject(type){if(!project)return note('请先打开项目');change(()=>{const p=activePanel(),a={id:newId('a'),panel:p.id,type:['title','subtitle','textbox'].includes(type)?'text':type,role:type,x:p.region?.x||7,y:12,width:24,height:10,font_pt:type==='title'?13:11,font_family:'Arial',angle_deg:0,color:'#222222',fill:'none',stroke_mm:.25,opacity:1};
 if(a.type==='text'){a.text=type==='title'?'标题':type==='subtitle'?'副标题':'文本框';a.y=type==='title'?4:type==='subtitle'?9:20;a.background=type==='textbox'?'#ffffff':'none';}
 if(type==='legend'){a.link_palette=true;a.items=p.legend_items?.length?clone(p.legend_items):p.colors.map((color,i)=>({label:'系列 '+(i+1),color}));if(!a.items.length)a.items=[{label:'系列 1',color:'#1f78b4'}];a.symbol='circle';a.y=18;}
 if(type==='line'||type==='arrow')a.height=0;$('pick-mode').value='element';state.annotations.push(a);selection={type:'annotation',id:a.id,panel:p.id};selected=[p.id];});}
$('add-text').onclick=()=>addObject('textbox');$('add-object').onclick=()=>addObject($('add-kind').value);
function loadStatSource(){
 const p=panelById($('stats-panel').value);$('stats-error').textContent='';if($('stats-source').value==='project'){statsRows=T.observations(project.stat_data?.[p.id]||[]);statsResults=[];statsFileName='项目观测值';if(!statsRows.length)$('stats-source-info').textContent='此面板未关联观测数据。可导入 CSV，或用新版助手的 stat_data 参数关联。';else $('stats-source-info').textContent=`已关联 ${statsRows.length} 行观测值；每行对应一个观测单位；配对比较需提供 id。`;}
 else $('stats-source-info').textContent=$('stats-source').value==='results'?'结果表：group1、group2，以及 p_value 或 p_adjusted；method 可选。':'观测值：group、value；配对检验另需 id。每行应为一个独立生物学单位。';
 const groups=[...new Set(statsRows.map(r=>r.group))];for(const control of ['stats-a','stats-b']){$(control).replaceChildren();for(const group of groups){const option=document.createElement('option');option.value=group;option.textContent=group;$(control).append(option);}}$('stats-b').selectedIndex=Math.min(1,groups.length-1);
}
$('add-stat').onclick=()=>{if(!project)return note('请先打开项目');$('stats-panel').replaceChildren();for(const p of panels()){const option=document.createElement('option');option.value=p.id;option.textContent=p.name;$('stats-panel').append(option);}$('stats-panel').value=activePanel().id;$('stats-source').value=project.stat_data?.[activePanel().id]?.length?'project':'csv';statsRows=[];statsResults=[];statsFileName='';loadStatSource();$('stats-dialog').showModal();};
$('stats-panel').onchange=loadStatSource;$('stats-source').onchange=()=>{statsRows=[];statsResults=[];loadStatSource();};
$('stats-file').onchange=async event=>{const file=event.target.files[0];if(!file)return;$('stats-error').textContent='';try{if(file.size>25e6)throw Error('CSV 文件上限为 25 MB');const rows=T.csv(await file.text());statsFileName=file.name;if($('stats-source').value==='results'){statsResults=rows;statsRows=[];$('stats-source-info').textContent=`已读入 ${rows.length} 项统计结果：${file.name}`;}else{statsRows=T.observations(rows);statsResults=[];const groups=[...new Set(statsRows.map(r=>r.group))];for(const control of ['stats-a','stats-b']){$(control).replaceChildren();for(const g of groups){const option=document.createElement('option');option.value=g;option.textContent=g;$(control).append(option);}}$('stats-b').selectedIndex=Math.min(1,groups.length-1);$('stats-source-info').textContent=`${file.name} · ${statsRows.length} 行 · ${groups.length} 组`;}}catch(error){$('stats-error').textContent=error.message;}event.target.value='';};
$('stats-add').onclick=()=>{
 $('stats-error').textContent='';try{const p=panelById($('stats-panel').value),method=$('stats-method').value,adjust=$('stats-adjust').value,results=[],source=$('stats-source').value;
 if(source==='results'){
  if(!statsResults.length)throw Error('请先选择统计结果 CSV');for(const row of statsResults){const raw=row.p_value===''||row.p_value==null?null:Number(row.p_value),adj=row.p_adjusted===''||row.p_adjusted==null?null:Number(row.p_adjusted);if(!row.group1||!row.group2||raw==null&&adj==null||raw!=null&&(!Number.isFinite(raw)||raw<0||raw>1)||adj!=null&&(!Number.isFinite(adj)||adj<0||adj>1))throw Error('结果表的组名或 P 值无效');results.push({group1:row.group1,group2:row.group2,p_value:raw,p_adjusted:adj,method:'provided',provided_method:row.method||'导入结果',...Object.fromEntries(['n1','n2','effect','ci_low','ci_high','statistic','df'].filter(k=>row[k]!==''&&row[k]!=null).map(k=>{const n=Number(row[k]);if(!Number.isFinite(n))throw Error('结果表的 '+k+' 无效');return[k,n];})),alternative:row.alternative||'',adjustment:adj==null?adjust:'provided'});}
  if(results.some(r=>r.adjustment==='provided')&&!results.every(r=>r.adjustment==='provided'))throw Error('请为结果表的每项比较都提供 p_adjusted，或统一仅提供原始 p_value');
 }else{
  if(!statsRows.length)throw Error('请先关联或导入观测数据');const groups=[...new Set(statsRows.map(r=>r.group))],pairs=$('stats-all').checked?groups.flatMap((a,i)=>groups.slice(i+1).map(b=>[a,b])):[[$('stats-a').value,$('stats-b').value]];for(const[a,b]of pairs){if(!a||!b||a===b)throw Error('请选择两个不同的组');results.push({...T.test(statsRows,a,b,method),adjustment:adjust});}
 }
 if(!results.length)throw Error('没有可添加的比较');if(results[0].adjustment!=='provided'){const corrected=T.adjust(results.map(r=>r.p_value),adjust);results.forEach((r,i)=>r.p_adjusted=corrected[i]);}
 change(()=>{const family=newId('family');let key='';if(source==='csv'){key=newId('source');state.stat_sources[key]={name:statsFileName,rows:clone(statsRows)};}const region=p.region||{x:7,y:12,width:p.width-14,height:p.height-24};results.forEach((result,i)=>{const labels=region.x_labels||[],positions=region.x_positions||[],ia=labels.indexOf(result.group1),ib=labels.indexOf(result.group2),x1=ia>=0?positions[ia]:region.x+region.width*.2,x2=ib>=0?positions[ib]:region.x+region.width*.8;const a={id:newId('stat'),type:'stat',panel:p.id,...result,family,data_source:source==='project'?'project':source==='csv'?'csv':'provided',source_key:key,source_name:statsFileName||'项目观测值',display:$('stats-format').value,use_adjusted:result.p_adjusted!=null,x:Math.min(x1,x2),y:region.y+2+i*6,width:Math.abs(x2-x1),height:3,font_pt:11,font_family:'Arial',color:'#222222',stroke_mm:.25};state.annotations.push(a);selection={type:'annotation',id:a.id,panel:p.id};selected=[p.id];});});$('pick-mode').value='element';$('stats-dialog').close();
 }catch(error){$('stats-error').textContent=error.message;}
};
function download(name,content,type='application/json'){const url=URL.createObjectURL(new Blob([content],{type})),link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}
function replayCode(){const p=panels()[0],obj=project.object_name,dir='plot-tuner';if(!/^[A-Za-z_][\w.]*$/.test(obj))throw Error('绘图对象名需要是简单变量名');const stat=project.stat_object;if(stat&&!/^[A-Za-z_][\w.]*$/.test(stat))throw Error('统计数据对象名需要是简单变量名');
 if(project.engine==='ggplot2'){if(project.stat_data&&!stat)return`source("tuner.R")\n# 接在现有含 stat_data 的 plot_tuner_export(...) 调用之后\nplot_tuner_render("${dir}", "${dir}/tuner.json")\n`;return`source("tuner.R")\nplot_tuner_export(${obj}, "${dir}", width = ${p.width.toFixed(2)}, height = ${p.height.toFixed(2)},\n                  source_file = ${JSON.stringify(project.source_file)}, object_name = ${JSON.stringify(obj)}${stat?`,\n                  stat_data = ${stat}, stat_object = ${JSON.stringify(stat)}`:''})\nplot_tuner_render("${dir}", "${dir}/tuner.json")\n`;}
 if(project.stat_data&&!stat)return`from tuner import plot_tuner_render\n# Place after the existing export call that supplies stat_data.\nplot_tuner_render("${dir}", "${dir}/tuner.json")\n`;
 return`from tuner import plot_tuner_export, plot_tuner_render\nplot_tuner_export(${obj}, "${dir}", source_file=${JSON.stringify(project.source_file)}, object_name=${JSON.stringify(obj)}${stat?`, stat_data=${stat}, stat_object=${JSON.stringify(stat)}`:''})\nplot_tuner_render("${dir}", "${dir}/tuner.json")\n`;}
$('save').onclick=()=>{if(project)download('tuned-project.json',JSON.stringify({...project,settings:state},null,2));};
$('code').onclick=()=>{if(!project)return note('请先打开项目');try{$('replay-code').textContent=replayCode();$('settings-code').textContent=JSON.stringify(S.compile(project,state),null,2);$('code-dialog').showModal();}catch(error){note(error.message);}};
$('download-settings').onclick=()=>download('tuner.json',JSON.stringify(S.compile(project,state),null,2));$('download-code').onclick=()=>download(project.engine==='ggplot2'?'replay.R':'replay.py',replayCode(),'text/plain');
$('download-stats').onclick=()=>{const rows=state.annotations.filter(a=>a.type==='stat'),columns=['id','panel','group1','group2','method','provided_method','n1','n2','effect','ci_low','ci_high','statistic','df','p_value','p_adjusted','adjustment','family','data_source','source_name'];const quote=v=>'"'+String(v??'').replace(/"/g,'""')+'"';download('statistics.csv',[columns.join(','),...rows.map(r=>columns.map(k=>quote(r[k])).join(','))].join('\n'),'text/csv');};
$('copy-code').onclick=async()=>{try{await navigator.clipboard.writeText(replayCode());note('代码已复制');}catch{note('请下载重放代码，或在代码框中选取复制');}};
$('svg').onclick=()=>{if(project)download('tuned.svg',new XMLSerializer().serializeToString(S.composite(project,state)),'image/svg+xml');};
$('help').onclick=()=>$('help-dialog').showModal();document.querySelectorAll('dialog .close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
$('open').onchange=async event=>{const file=event.target.files[0];if(!file)return;try{if(file.size>25e6)throw Error('项目上限为 25 MB');openProject(JSON.parse(await file.text()));}catch(error){note(error.message);}event.target.value='';};
async function demo(name){try{const response=await fetch(name);if(!response.ok)throw Error('示例加载失败');openProject(await response.json());}catch(error){note(error.message);}}
$('demo').onchange=e=>{if(e.target.value)demo(e.target.value);};$('start-demo').onclick=()=>demo('demo-r.json');
window.addEventListener('keydown',event=>{if(/INPUT|TEXTAREA|SELECT/.test(event.target.tagName))return;if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();$(event.shiftKey?'redo':'undo').click();}if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='s'){event.preventDefault();$('save').click();}if(event.key==='Delete'||event.key==='Backspace'){event.preventDefault();removeSelection();}if(selection&&['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key)){event.preventDefault();change(()=>{const axis=event.key==='ArrowLeft'||event.key==='ArrowRight'?'x':'y',delta=(event.key==='ArrowLeft'||event.key==='ArrowUp'?-1:1)*(event.shiftKey?1:.2);if(selection.type==='panel')state.panels[selection.id][axis]+=delta;else{const key=selection.type==='annotation'?axis:axis==='x'?'dx_mm':'dy_mm';editProperty(key,(selectedEdit()[key]||0)+delta);}});}});
function linkedDemo(){if(location.hash==='#r')demo('demo-r.json');if(location.hash==='#python')demo('demo-python.json');}window.addEventListener('hashchange',linkedDemo);linkedDemo();
