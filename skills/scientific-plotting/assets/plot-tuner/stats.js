window.TunerStats=(()=>{
 const mean=x=>x.reduce((a,b)=>a+b,0)/x.length;
 const variance=x=>{const m=mean(x);return x.reduce((a,b)=>a+(b-m)**2,0)/(x.length-1);};
 function csv(text){
  const separator=text.split(/\r?\n/)[0].includes('\t')?'\t':',';const rows=[];let row=[],field='',quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}else if(c===separator&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(field);if(row.some(x=>x.trim()))rows.push(row);row=[];field='';}else field+=c;}
  if(quoted)throw Error('CSV 引号未闭合');row.push(field);if(row.some(x=>x.trim()))rows.push(row);
  if(rows.length<2)throw Error('CSV 至少需要表头和一行数据');const head=rows.shift().map(x=>x.replace(/^\uFEFF/,'').trim());return rows.map(r=>Object.fromEntries(head.map((h,i)=>[h,(r[i]??'').trim()])));
 }
 function observations(rows){return rows.map((r,i)=>{if(r.group==null||r.group==='')throw Error(`第 ${i+1} 行缺少 group`);let value=null;if(r.value!==''&&r.value!=null&&r.value!=='NA'){value=Number(r.value);if(!Number.isFinite(value))throw Error(`第 ${i+1} 行 value 无效`);}return{group:String(r.group),value,id:r.id==null||r.id===''?null:String(r.id)};});}
 function test(rows,a,b,method='welch'){
  let ra=rows.filter(r=>r.group===a),rb=rows.filter(r=>r.group===b),x,y,omitted=0;
  if(method==='paired'){
   const collect=rs=>{const m=new Map();for(const r of rs){if(!r.id)throw Error('配对检验需要每行的 id');if(m.has(r.id))throw Error('同组内 id 重复，请先汇总技术重复');m.set(r.id,r.value);}return m;};
   const left=collect(ra),right=collect(rb);const ids=[...left.keys()].filter(k=>right.has(k)&&left.get(k)!=null&&right.get(k)!=null);x=ids.map(k=>left.get(k));y=ids.map(k=>right.get(k));omitted=ra.length+rb.length-2*ids.length;
  }else{x=ra.filter(r=>r.value!=null).map(r=>r.value);y=rb.filter(r=>r.value!=null).map(r=>r.value);omitted=ra.length+rb.length-x.length-y.length;}
  if(x.length<2||y.length<2)throw Error('每组至少需要两个有效独立单位；配对检验至少需要两对');
  let se,df,effect=mean(x)-mean(y);
  if(method==='paired'){const diff=x.map((v,i)=>v-y[i]);se=Math.sqrt(variance(diff)/diff.length);df=diff.length-1;}
  else if(method==='student'){df=x.length+y.length-2;const pooled=((x.length-1)*variance(x)+(y.length-1)*variance(y))/df;se=Math.sqrt(pooled*(1/x.length+1/y.length));}
  else{const vx=variance(x)/x.length,vy=variance(y)/y.length;se=Math.sqrt(vx+vy);df=(vx+vy)**2/(vx*vx/(x.length-1)+vy*vy/(y.length-1));}
  if(!Number.isFinite(se)||se<=10*Number.EPSILON*Math.max(Math.abs(mean(x)),Math.abs(mean(y))))throw Error('数据变化不足，无法计算可靠的 t 检验');
  const t=effect/se,p=2*jStat.studentt.cdf(-Math.abs(t),df),critical=jStat.studentt.inv(.975,df);
  return{group1:a,group2:b,method,n1:x.length,n2:y.length,omitted,statistic:t,df,effect,ci_low:effect-critical*se,ci_high:effect+critical*se,p_value:p,alternative:'two.sided'};
 }
 function adjust(p,method='holm'){
  const n=p.length,order=p.map((value,i)=>({value,i})).sort((a,b)=>a.value-b.value),out=Array(n);let running=method==='BH'?1:0;
  if(method==='none')return[...p];
  if(method==='BH'){for(let k=n-1;k>=0;k--){running=Math.min(running,order[k].value*n/(k+1));out[order[k].i]=Math.min(1,running);}}
  else for(let k=0;k<n;k++){running=Math.max(running,order[k].value*(n-k));out[order[k].i]=Math.min(1,running);}return out;
 }
 return{csv,observations,test,adjust};
})();
