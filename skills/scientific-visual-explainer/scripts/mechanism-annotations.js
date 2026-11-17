/* Separate entity names, nucleotide states and phosphorylation badges. */
(function(root){
function phosphorylation(core,f,marks){
 const badges=[],texts=[];
 for(const m of marks){
  if(f.states[m.entity]!==m.state)continue;
  const a=m.anchor?core.anchor(m.entity,m.anchor,f.poses[m.entity]).point:f.poses[m.entity].c;
  m.offsets.forEach((offset,i)=>{const x=a[0]+offset[0],y=a[1]+offset[1],id=m.entity+'-P'+i;badges.push({id,x,y,r:15});
   if(m.sites?.[i])texts.push({id:id+'-site',text:m.sites[i],x,y:y+43,anchor:'middle',size:24,color:'#9D665E'});
  });
 }
 return {badges,texts};
}
function annotations(core,f,animate){
 const p=f.poses,texts=[],badges=[],lines=[];
 const text=(id,value,x,y,anchor='middle',size=28,color='#304F59')=>texts.push({id,text:value,x,y,anchor,size,color});
 const state=(id,value,x,y,anchor='start')=>text(id,value,x,y,anchor,24,'#9D665E');
 const badge=(id,x,y,site)=>{badges.push({id,x,y,r:15});if(site)state(id+'-site',site,x,y+43,'middle')};
 text('r1','EGFR',p.r1.c[0]-90,core.membraneY+101,'end');
 text('l1','EGF',p.l1.c[0]-52,p.l1.c[1]+7,'end');
 text('grb','GRB2',p.grb.c[0],p.grb.c[1]+65);
 text('sos','SOS1',p.sos.c[0]+27,p.sos.c[1]+112);
 text('ras','RAS',p.ras.c[0]+91,p.ras.c[1]+35,'start');
 text('raf','RAF1',Math.min(1160,p.raf.c[0]+200),p.raf.c[1]-20,'end');
 text('mek','MEK1/2',p.mek.c[0]-85,p.mek.c[1]+6,'end');
 text('erk','ERK1/2',p.erk.c[0]-85,p.erk.c[1]+6,'end');
 for(const id of ['r1','r2'])if(f.states[id]){
   const a=core.anchor(id,'pY-tail',p[id]).point;
   const x=a[0]+(id==='r1'?-48:-20),y=a[1]+(id==='r1'?-29:-40);
   badge(id+'-P',x,y);lines.push({id:id+'-P-leader',a:[x+(id==='r1'?14:-9),y+7],b:[a[0],a[1]-14]});
 }
 state('ras-state',f.states.ras||'GDP',p.ras.c[0]+91,p.ras.c[1]+68);
 if(f.states.raf)state('raf-state','active',p.raf.c[0]+120,p.raf.c[1]+22);
 for(const [id,sites]of [['mek',['S','S']],['erk',['T','Y']]])if(f.states[id]){
   badge(id+'-P1',p[id].c[0]+101,p[id].c[1]-9,sites[0]);
   badge(id+'-P2',p[id].c[0]+139,p[id].c[1]-9,sites[1]);
 }
 const ex=core.events.find(e=>e.id==='exchange'),u=ex?(f.t-ex.start)/ex.duration:-1,nucleotides=[];
 if(animate&&u>=0&&u<1){
   text('exchange','GDP out · GTP in',720,460,'start',24,'#607D83');
   const out=Math.min(1,u/.5),inside=Math.max(0,(u-.45)/.55);
   nucleotides.push({id:'gdp',x:p.ras.c[0]+70+105*out,y:p.ras.c[1]+25+135*(1-(1-out)**3),opacity:1-out*.8,color:'#E4BE78'});
   nucleotides.push({id:'gtp',x:p.ras.c[0]+175-113*inside,y:p.ras.c[1]-65+90*inside,opacity:Math.min(1,u*3),color:'#69ADB5'});
 }
 return {texts,badges,lines,nucleotides};
}
root.MechanismAnnotations={annotations,phosphorylation};
if(typeof module!=='undefined')module.exports=root.MechanismAnnotations;
})(typeof window==='undefined'?globalThis:window);
