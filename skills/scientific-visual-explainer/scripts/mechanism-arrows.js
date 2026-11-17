/* Draw causal connectors between separated contact surfaces. */
(function(root){
function route(a,b,active){
 const dx=b.point[0]-a.point[0],dy=b.point[1]-a.point[1],distance=Math.hypot(dx,dy);
 if(!active||distance<=40)return {d:'',opacity:0};
 const u=[dx/distance,dy/distance];
 if(a.normal[0]*u[0]+a.normal[1]*u[1]<=0||b.normal[0]*u[0]+b.normal[1]*u[1]>=0)return {d:'',opacity:0};
 const start=a.point.map((v,i)=>v+16*u[i]),end=b.point.map((v,i)=>v-12*u[i]);
 const t=Math.min(1,(distance-40)/35),opacity=.8*t*t*(3-2*t);
 return {d:`M ${start[0]} ${start[1]} L ${end[0]} ${end[1]}`,opacity,start,end,direction:u};
}
root.MechanismArrows={route};
if(typeof module!=='undefined')module.exports=root.MechanismArrows;
})(typeof window==='undefined'?globalThis:window);
