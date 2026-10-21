/* Scene policy; geometry and annotation rendering reuse the shared helpers. */
(function(root){
const smooth=u=>{u=Math.max(0,Math.min(1,u));return u*u*(3-2*u)};
function condition(model,name){const m=JSON.parse(JSON.stringify(model));
 if(name==='alk5-blocked'){m.events=m.events.filter(e=>['ligand-bind','pair-II','pair-Ia','pair-Ib','gs-a','gs-b'].includes(e.id));m.events.push({id:'blocked',kind:'state',actor:'r1a',target:'r1a',duration:2,after:['gs-a','gs-b'],state:'GS-P',title:'ALK5 催化活性阻断',caption:'GS 区仍可被受体 II 磷酸化，但 ALK5 不能向 SMAD3 传递磷酸化；P 圆圈不是整个通路已经激活的替代符号。',source:'gs'});}
 if(name==='smad3-2SA'){m.events=m.events.filter(e=>['ligand-bind','pair-II','pair-Ia','pair-Ib','gs-a','gs-b','phos-a','phos-b'].includes(e.id));for(const e of m.events)if(e.id.startsWith('phos-'))e.state='2SA';m.events.push({id:'mutant',kind:'state',actor:'sa',target:'sa',duration:2,after:['phos-b'],state:'2SA',title:'SMAD3 的 C 端位点突变',caption:'此教学对照保留受体激活和底物接触，但不生成 SMAD3 C 端 P 标记，也不进入后续三聚体与转录步骤。',source:'smad-p'});}
 return m;
}
function notes(core,f){const p=f.poses,texts=[],lines=[],routes=[];
 const text=(id,value,x,y,anchor='middle',size=26,color='#304F59',opacity=1)=>texts.push({id,text:value,x,y,anchor,size,color,opacity});
 const opacity=id=>{const moving=f.active.some(e=>f.t>e.start&&f.t<e.end&&(e.id==='import'&&['sa','sb','s4'].includes(id)||e.id==='dna-bind'&&['sa','sb','s4'].includes(id)||e.actor===id&&['reaction','dock','move'].includes(e.kind)));return moving||id==='s4'&&f.active.some(e=>e.kind==='dock'&&e.target==='s4'&&f.t<e.end)?0:1};
 for(const id of ['r2a','r2b','r1a','r1b']){
  const typeI=id.startsWith('r1'),left=id.endsWith('a'),x=p[id].c[0]+(typeI?(left?-22:22):(left?-90:100)),y=typeI?610:580;
  const shown=f.active.some(e=>e.kind==='reaction'||e.kind==='dock'&&e.target==='s4')?0:1;
  text(id,typeI?'ALK5':'RII',x,y,typeI?'middle':left?'end':'start',26,'#304F59',shown);
  if(shown)lines.push({id:id+'-label',a:[p[id].c[0],typeI?435:545],b:[x,y-29],color:'#BACBCB'});
 }
 text('ligand','TGFβ1 dimer',p.ligand.c[0],p.ligand.c[1]-80,'middle',28);
 for(const id of ['sa','sb']){
  const linked=f.links[id]?.target==='s4';
  text(id,'SMAD3',p[id].c[0]+(linked?(id==='sa'?-70:70):0),p[id].c[1]+(linked?5:-70),linked?(id==='sa'?'end':'start'):'middle',26,'#304F59',opacity(id));
  if(f.states[id]==='2SA')text(id+'-mutant','2SA',p[id].c[0],p[id].c[1]+85,'middle',24,'#9D665E');
 }
 text('s4','SMAD4',p.s4.c[0],p.s4.c[1]+(f.links.s4?.target==='dna'?176:-70),'middle',26,'#304F59',opacity('s4'));
 text('npc','Nuclear pore',850,1148,'start',26,'#7B969D');
 text('dna','Response element',850,1590,'start',26,'#7B969D');
 if(f.amounts.rna>.05)text('rna','Target-gene RNA',1000,1845,'middle',28,'#304F59',f.amounts.rna);
 const marks=[...['r1a','r1b'].map(entity=>({entity,state:'GS-P',anchor:'GS',offsets:[[core.anchor(entity,'GS',p[entity]).normal[0]*34,0]]})),...['sa','sb'].map(entity=>({entity,state:'pS2',offsets:[[-18,60],[18,60]]}))];
 const phos=root.MechanismAnnotations.phosphorylation(core,f,marks);texts.push(...phos.texts);
 for(const[id,src,srcPort,dst,dstPort]of [['gs-left','r2a','GS-activation','r1a','GS'],['gs-right','r2b','GS-activation','r1b','GS']])routes.push({id,...root.MechanismArrows.route(core.anchor(src,srcPort,p[src]),core.anchor(dst,dstPort,p[dst]),f.states[dst]==='GS-P')});
 for(const[id,src,dst]of [['phos-left','r1a','sa'],['phos-right','r1b','sb']]){const a=core.anchor(src,'SMAD-substrate',p[src]),b=core.anchor(dst,'co-SMAD-left',p[dst]),distance=Math.hypot(a.point[0]-b.point[0],a.point[1]-b.point[1]);routes.push({id,...root.MechanismArrows.route(a,b,f.active.some(e=>e.kind==='reaction'&&e.actor===dst)&&distance<180&&Math.abs(a.point[1]-b.point[1])<12)});}
 if(f.states.rna==='transcribed'){
  routes.push({id:'nuclear-flow',d:'M 600 620 L 600 1400',opacity:.55,start:[600,620],end:[600,1400],direction:[0,1]});
  const a={point:[800,1695],normal:[1,0]},b={point:[905,1735],normal:[-1,0]};routes.push({id:'rna-flow',...root.MechanismArrows.route(a,b,true)});
 }
 return {texts,badges:phos.badges,lines,routes,nucleotides:[]};
}
root.TgfbScene={condition,notes};if(typeof module!=='undefined')module.exports=root.TgfbScene;
})(typeof window==='undefined'?globalThis:window);
