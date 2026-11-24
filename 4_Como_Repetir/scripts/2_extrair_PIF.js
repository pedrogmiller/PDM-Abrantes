// PASSO 2. A perigosidade de incêndio (camada 145) tem mais de 2000 polígonos: este script pede-a por blocos. Descarrega PIF_Abrantes.json.
// ===== EDITAR ESTAS DUAS LINHAS =====
const TOKEN='COLA_AQUI';                       // DevTools > Network > pedido "export" > Payload > token
const AREA=[12237,-28202,16397,-25509];        // xmin,ymin,xmax,ymax em EPSG:3763 (PT-TM06)
// =====================================
(async()=>{
const tok=TOKEN;
const base='https://sig.cm-abrantes.pt/arcgis/rest/services/PMOTs/PDM_2026/MapServer/145/query';
const feats={}; let n=0;
async function get(x0,y0,x1,y1,d){
 const q=base+'?where=1%3D1&geometry='+[x0,y0,x1,y1].join(',')+'&geometryType=esriGeometryEnvelope&inSR=3763&outSR=3763&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&f=json&token='+encodeURIComponent(tok);
 const r=await (await fetch(q)).json();
 if(r.error){console.log('ERRO',JSON.stringify(r.error));return;}
 if(r.exceededTransferLimit && d<8){const mx=(x0+x1)/2,my=(y0+y1)/2;
  for(const b of [[x0,y0,mx,my],[mx,y0,x1,my],[x0,my,mx,y1],[mx,my,x1,y1]]) await get(...b,d+1); return;}
 for(const f of r.features) feats[f.attributes.OBJECTID]=f; n++;
 console.log('bloco',n,'total',Object.keys(feats).length);
}
await get(...AREA,0);
const out={layer:145,features:Object.values(feats)};
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'}));a.download='PIF_Abrantes.json';a.click();
console.log('FEITO',out.features.length);
})();
