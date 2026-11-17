/* One pass keeps the original symbol colors mapped to the same semantic roles. */
function recolor(svg,id){const colors=PALETTES.themes.find(p=>p.id===id).colors,map=Object.fromEntries(Object.entries(PALETTES.roles).map(([role,hex])=>[hex,colors[role]]));return svg.replace(/#[0-9a-f]{6}\b/gi,hex=>map[hex.toLowerCase()]||hex)}
