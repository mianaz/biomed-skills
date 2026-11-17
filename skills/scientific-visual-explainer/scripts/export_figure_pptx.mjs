// Native paths and text from the same frame() used by the HTML lesson.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const require=createRequire(import.meta.url);
require('./domain-motion.js');const FigureScene=require('./figure-scene.js');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node export_figure_pptx.mjs scene.json output/deck.pptx');
const {Presentation,PresentationFile}=await import(process.env.ARTIFACT_TOOL_MODULE?pathToFileURL(process.env.ARTIFACT_TOOL_MODULE).href:'@oai/artifact-tool');
const scene=JSON.parse(await fs.readFile(input,'utf8')),engine=FigureScene.make(scene);
const presentation=Presentation.create({slideSize:{width:1280,height:720}});
const scale=Math.min(1120/scene.canvas.width,450/scene.canvas.height),ox=(1280-scene.canvas.width*scale)/2,oy=115;
const buildDir=path.join(path.dirname(output),'.figure-build');await fs.mkdir(buildDir,{recursive:true});
function text(slide,name,value,box,size,align='left',color='#243e44',options={}){
 const shape=slide.shapes.add({geometry:'textbox',name,position:box,fill:'none',line:{fill:'none',width:0}});
 shape.text=value;shape.text.style={typeface:'Arial',fontSize:size,color,alignment:align,verticalAlignment:'middle',wrap:'none',...options};shape.text.insets=0;return shape;
}
for(const [index,t] of engine.keyframes.entries()){
 const frame=engine.frame(t),slide=presentation.slides.add();slide.background.fill='#ffffff';
 const event=engine.events.filter(e=>e.start<t&&t<e.end).at(-1)||engine.events.filter(e=>e.end<=t).at(-1);
 text(slide,'title',event?.title||scene.title,{left:64,top:28,width:1152,height:54},36);
 text(slide,'caption',event?.caption||scene.scope,{left:64,top:580,width:1152,height:62},22);
 text(slide,'timing',`${index+1}/${engine.keyframes.length} · ${t.toFixed(1)} s · ${scene.timing_basis}`,{left:64,top:665,width:1152,height:28},16);
 for(const entity of scene.entities){
  const pose=frame.poses[entity.id];if(pose.opacity===0)continue;
  for(const [j,part] of entity.parts.entries()){
   const name=`!!${entity.id}/part-${j}`,b=part.bbox;
   if(part.type==='text'){
    text(slide,name,part.text,{left:ox+(b[0]+pose.dx)*scale,top:oy+(b[1]+pose.dy)*scale,width:b[2]*scale,height:b[3]*scale},part.fontSize*scale,{start:'left',middle:'center',end:'right'}[part.anchor],`${part.fill}/${Math.round(pose.opacity*(part.opacity??1)*100)}`,{typeface:part.fontFamily,bold:(part.fontWeight||400)>=600,italic:part.fontStyle==='italic'});
   }else if(part.type==='path'){
    const width=Math.max(1,b[2]),height=Math.max(1,b[3]);
    const commands=part.commands.map(command=>Object.fromEntries(Object.entries(command).map(([kind,coords])=>[kind,Object.fromEntries(Object.entries(coords).map(([key,value])=>[key,value-(key.startsWith('x')?b[0]:b[1])]))])));
    const fill=pose.fill&&part.fill!=='none'?pose.fill:part.fill;
    const alpha=(part.opacity??1)*pose.opacity;
    slide.shapes.add({geometry:'custom',name,
     position:{left:ox+(b[0]+pose.dx)*scale,top:oy+(b[1]+pose.dy)*scale,width:width*scale,height:height*scale},
    fill:fill==='none'?'none':`${fill}/${Math.round(alpha*(part.fillOpacity??1)*100)}`,
     line:{fill:part.stroke==='none'?'none':`${part.stroke}/${Math.round(alpha*(part.strokeOpacity??1)*100)}`,width:part.strokeWidth*scale},
     customPaths:[{width,height,commands}]});
   }else{
    const image=slide.images.add({dataUrl:part.href,alt:name,fit:'contain',position:{left:ox+(b[0]+pose.dx)*scale,top:oy+(b[1]+pose.dy)*scale,width:b[2]*scale,height:b[3]*scale}});
    image.name=name;
   }
  }
  if(pose.highlight){const b=entity.bbox;slide.shapes.add({geometry:'rect',name:`!!${entity.id}/highlight`,position:{left:ox+(b[0]+pose.dx-5)*scale,top:oy+(b[1]+pose.dy-5)*scale,width:(b[2]+10)*scale,height:(b[3]+10)*scale},fill:'none',line:{fill:'#246963',width:2*scale}})}
 }
 slide.speakerNotes.text=[event?.caption||scene.scope,event?.source?'Source: '+event.source:'',`Teaching time: ${t.toFixed(1)} s (${scene.timing_basis}).`,event?scene.scope:'',...scene.sources.map(s=>`${s.url||s.file||s.id}: ${s.role||''}`)].filter(Boolean).join('\n\n');
 const png=await presentation.export({slide,format:'png',scale:1});
 await fs.writeFile(path.join(buildDir,`slide-${index+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const draft=path.join(buildDir,'draft.pptx');await(await PresentationFile.exportPptx(presentation)).save(draft);
const patcher=path.join(path.dirname(fileURLToPath(import.meta.url)),'finish_figure_pptx.py');
execFileSync(process.env.SCENE_PYTHON||'python3',[patcher,draft,output,'--morph'],{stdio:'inherit'});
await fs.writeFile(path.join(buildDir,'keyframes.json'),JSON.stringify(engine.keyframes));
console.log(`${engine.keyframes.length} slides → ${output}`);
