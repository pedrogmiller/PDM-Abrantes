// Para camadas com mais de 2000 polígonos (ex.: PIF, camada 145): divide a área em quadrantes até caber.
(async()=>{
const tok='COLA_AQUI';
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
await get(12237,-28202,16397,-25509,0);
const out={layer:145,features:Object.values(feats)};
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'}));a.download='PIF_Abrantes_Amarvento.json';a.click();
console.log('FEITO',out.features.length);
})();
