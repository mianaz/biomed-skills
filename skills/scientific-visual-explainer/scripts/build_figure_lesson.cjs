// Build one offline lesson and bake the same state evaluator for Manim.
const fs=require('node:fs'),path=require('node:path');
require('./domain-motion.js');const FigureScene=require('./figure-scene.js');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Usage: node build_figure_lesson.cjs scene.json lesson.html');
const scene=JSON.parse(fs.readFileSync(input,'utf8')),engine=FigureScene.make(scene);
const template=fs.readFileSync(path.join(__dirname,'../assets/figure-to-scene/lesson-template.html'),'utf8');
const safe=JSON.stringify(scene).replace(/</g,'\\u003c');
const html=template.replace('/*SCENE_DATA*/',()=>`const SCENE=${safe};`).replace('/*SCENE_ENGINE*/',()=>fs.readFileSync(path.join(__dirname,'domain-motion.js'),'utf8')+'\n'+fs.readFileSync(path.join(__dirname,'figure-scene.js'),'utf8'));
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,html);
const fps=30,samples=Array.from({length:Math.ceil(engine.duration*fps)+1},(_,i)=>engine.frame(Math.min(engine.duration,i/fps)));
fs.writeFileSync(output.replace(/\.html$/,'')+'.frames.json',JSON.stringify({fps,duration:engine.duration,frames:samples}));
const stamp=t=>{const ms=Math.round(t*1000);return `${String(Math.floor(ms/3600000)).padStart(2,'0')}:${String(Math.floor(ms/60000)%60).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')}.${String(ms%1000).padStart(3,'0')}`};
const captions=samples.filter((f,i)=>!i||f.caption!==samples[i-1].caption);
const cues=captions.map((f,i)=>`${stamp(f.t)} --> ${stamp(captions[i+1]?.t??engine.duration)}\n${FigureScene.esc(f.caption)}\n`);
fs.writeFileSync(output.replace(/\.html$/,'')+'.vtt','WEBVTT\n\n'+cues.join('\n'));
console.log(`${scene.entities.length} components; ${engine.events.length} events; ${engine.duration}s → ${output}`);
