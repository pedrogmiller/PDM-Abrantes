// PASSO 1. Correr na Consola do DevTools (F12), com o visualizador MuniSIG de Abrantes aberto. Descarrega PDM_Abrantes.json.
// TOKEN: Network > um pedido "export" > Payload > token. Área: EPSG:3763 (xmin,ymin,xmax,ymax).
// ===== EDITAR ESTAS DUAS LINHAS =====
const TOKEN='COLA_AQUI';                       // DevTools > Network > pedido "export" > Payload > token
const AREA=[12237,-28202,16397,-25509];        // xmin,ymin,xmax,ymax em EPSG:3763 (PT-TM06)
// =====================================
(async()=>{
const tok=TOKEN;
const base='https://sig.cm-abrantes.pt/arcgis/rest/services/PMOTs/PDM_2026/MapServer';
const T='&token='+encodeURIComponent(tok);
const L=await (await fetch(base+'/layers?f=json'+T)).json();
if(L.error){console.log('ERRO',JSON.stringify(L));return;}
const out={layers:L.layers.map(l=>({id:l.id,name:l.name,type:l.type,geom:l.geometryType,parent:l.parentLayer,fields:(l.fields||[]).map(f=>f.name),renderer:l.drawingInfo&&l.drawingInfo.renderer})),data:{}};
const g=AREA.join(',');
for(const l of L.layers){ if(l.type!=='Feature Layer')continue;
 const q=base+'/'+l.id+'/query?where=1%3D1&geometry='+g+'&geometryType=esriGeometryEnvelope&inSR=3763&outSR=3763&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&f=json'+T;
 try{const r=await (await fetch(q)).json(); if(r.features&&r.features.length) out.data[l.id]=r; console.log(l.id,l.name,r.features?r.features.length:JSON.stringify(r.error));}catch(err){console.log(l.id,err)}
}
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'}));a.download='PDM_Abrantes.json';a.click();
})();
