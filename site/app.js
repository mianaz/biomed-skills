const demos = {
  tgfb: {title:'从受体磷酸化到核内转录',type:'机制教学 · 文献来源',description:'观察两对受体、两个磷酸化 SMAD3 与一个 SMAD4 的组装、核孔通行和转录响应。',features:['正常信号、ALK5 阻断、SMAD3 2SA','58 秒可寻址时间轴','独立 SVG 图标与磷酸化标记'],scope:'示意比例、界面和时间用于教学；每幕附来源。不是原子结构或实测动力学。',url:'skills/scientific-visual-explainer/assets/tgfb-generated.html',source:'skills/scientific-visual-explainer/assets/biomed-icons/tgfb-imagegen/mechanism-example.json'},
  egfr: {title:'把结合、交换与激酶反应分开看',type:'机制教学 · 文献来源',description:'从 EGF 结合到 EGFR 二聚化，继续观察 GRB2–SOS1、RAS 核苷酸交换和 RAF–MEK–ERK 反应。',features:['正常与激酶阻断条件','8 个生成后转为路径的 SVG 组分','锚点、配对轮廓、可编辑状态标记'],scope:'图形界面与教学时间线为示意；表达、结合、磷酸化和核苷酸交换以不同状态表示。',url:'skills/scientific-visual-explainer/assets/egfr-generated.html',source:'skills/scientific-visual-explainer/assets/biomed-icons/egfr-imagegen/mechanism-example.json'},
  icons: {title:'当前机制资产：16 个图标',type:'当前资产 · v0.7',description:'只展示当前生成并转为可编辑路径的 EGF–ERK、TGFβ–SMAD 与 DNA/RNA 图标。原始生成图与最新 SVG 并排检查。',features:['与当前机制演示共享 SVG 源文件','16 个图标，三个当前生成家族','可下载 SVG、原始生成图和锚点目录'],scope:'形态、比例与接触轮廓用于机制教学；部件与来源见图标记录。',url:'icons.html',source:'examples/current-icons.json'},
};
const $ = selector => document.querySelector(selector);
const escapeHTML = text => String(text).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let selectedDemo = 'tgfb';
function loadDemo(){
  const demo=demos[selectedDemo];
  $('#demo-stage').replaceChildren(Object.assign(document.createElement('iframe'), {src:demo.url,title:demo.title,loading:'lazy'}));
}
$('#load-demo').addEventListener('click',loadDemo);
document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click',()=>{
  selectedDemo=button.dataset.demo;
  const demo=demos[selectedDemo];
  document.querySelectorAll('[data-demo]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-pressed',String(item===button));});
  $('#demo-title').textContent=demo.title;$('#demo-type').textContent=demo.type;$('#demo-description').textContent=demo.description;$('#demo-scope').textContent=demo.scope;
  $('#demo-features').innerHTML=demo.features.map(item=>`<li>${escapeHTML(item)}</li>`).join('');
  $('#demo-open').href=demo.url;$('#demo-source').href=demo.source;
  loadDemo();
}));
let category='all';
function filterSkills(){
  const query=$('#skill-search').value.trim().toLowerCase();let count=0;
  document.querySelectorAll('.skill-card').forEach(card=>{const show=(category==='all'||card.dataset.group===category)&&card.textContent.toLowerCase().includes(query);card.hidden=!show;if(show)count++;});
  $('#skill-count').textContent=`显示 ${count} 项技能`;$('#no-skills').hidden=count>0;
}
$('#skill-search').addEventListener('input',filterSkills);
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{category=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-pressed',String(item===button));});filterSkills();}));
const catalog=JSON.parse(document.querySelector('#catalog-data').textContent);
const dialog=$('#skill-dialog');
function openGuide(){
  if(!location.hash.startsWith('#skill/'))return;
  const skill=catalog.find(item=>item.id===location.hash.slice(7));if(!skill)return;
  $('#guide-content').innerHTML=`<h2 id="guide-title">${escapeHTML(skill.title)}</h2><div class="guide-label">${skill.id}</div><p>${escapeHTML(skill.summary)}</p><h3>准备什么输入</h3><ul>${skill.inputs.map(item=>`<li>${escapeHTML(item)}</li>`).join('')}</ul><h3>复制这段提示词</h3><pre id="guide-prompt">${escapeHTML(skill.prompt)}</pre><button class="copy" id="copy-prompt">复制提示词</button><h3>工作怎样推进</h3>${skill.steps.map((item,index)=>`<div class="guide-step"><span>0${index+1}</span><p>${escapeHTML(item)}</p></div>`).join('')}<h3>交付哪些文件</h3><div class="guide-files">${skill.outputs.map(item=>`<span>${escapeHTML(item)}</span>`).join('')}</div><h3>具体示例</h3><p class="preserve">${escapeHTML(skill.example)}</p><p class="synthetic-note">写作与研究示例中的 Protein X、数值和实验均为虚构教学内容。机制演示的真实文献来源与读取范围记录在各演示内部。</p><div class="guide-actions">${(skill.downloads||[]).map(item=>`<a download href="${item.path}">${escapeHTML(item.label)} ↓</a>`).join('')}<a href="${skill.source}">打开示例或参考文件 ↗</a><a href="examples/skills/${skill.id}.md" download>下载本页指南 ↓</a><a href="https://github.com/mianaz/biomed-skills/blob/main/skills/${skill.id}/SKILL.md" target="_blank" rel="noopener">完整 SKILL.md ↗</a></div>`;
  if(!dialog.open)dialog.showModal();
  $('#copy-prompt').addEventListener('click',()=>copyText(skill.prompt));dialog.scrollTop=0;
}
window.addEventListener('hashchange',()=>{if(location.hash.startsWith('#skill/'))openGuide();else if(dialog.open)dialog.close();});
$('#close-guide').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{if(location.hash.startsWith('#skill/'))history.replaceState(null,'','#skills');});
dialog.addEventListener('click',event=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();}});
openGuide();
document.querySelectorAll('[data-case]').forEach(button=>button.addEventListener('click',()=>{const skill=catalog.find(item=>item.id===button.dataset.case);document.querySelectorAll('[data-case]').forEach(item=>{item.classList.toggle('active',item===button);item.setAttribute('aria-pressed',String(item===button));});$('#case-id').textContent=skill.id;$('#case-title').textContent=skill.title;$('#case-example').textContent=skill.example;$('#case-guide').href='#skill/'+skill.id;}));
async function copyText(text){
  try{await navigator.clipboard.writeText(text);$('#toast').textContent='已复制';}catch{$('#toast').textContent='请选中文本并复制';}
  $('#toast').style.display='block';setTimeout(()=>$('#toast').style.display='none',2200);
}
$('[data-copy="install"]').addEventListener('click',()=>copyText('claude plugin marketplace add mianaz/biomed-skills\nclaude plugin install biomed-skill@biomed-skill'));
