/* Use one visible outline weight at the consuming assembly scale. */
(function(root){
function style(svg,scale=1){for(const n of svg.querySelectorAll('[stroke]')){
 const width=n.getAttribute('data-line-weight')||(n.getAttribute('stroke')==='#3D5963'?'1.6':null);
 if(width)n.setAttribute('stroke-width',Number(width)/scale);
}return svg}
root.MechanismIcons={style};
})(typeof window==='undefined'?globalThis:window);
