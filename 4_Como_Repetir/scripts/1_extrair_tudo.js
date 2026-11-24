// PASSO 1 (único passo no browser).
// Com o visualizador MuniSIG de Abrantes aberto: F12 > Console > colar este texto todo > Enter.
// Antes: no visualizador, enquadra no ecrã o terreno a analisar (com a margem que quiseres).
// Pergunta o token e a área (propõe os do último pedido "export" do mapa, ou seja, a vista atual) e descarrega PDM_Abrantes.json com todas as camadas do PDM 2026,
// incluindo as que têm mais de 2000 polígonos (pedidas por blocos, ex.: perigosidade de incêndio).
(async()=>{
const BASE='https://sig.cm-abrantes.pt/arcgis/rest/services/PMOTs/PDM_2026/MapServer';
// tenta ler o token e a vista atual do último pedido "export" que o mapa fez
let tok0='',area0='';
try{
  const u=performance.getEntriesByType('resource').map(r=>r.name).filter(n=>/MapServer\/export\?/.test(n)).pop();
  if(u){const p=new URL(u).searchParams; tok0=p.get('token')||'';
    const sr=(p.get('bboxSR')||'')+''; const b=p.get('bbox');
    if(b && /3763/.test(sr)) area0=b.split(',').map(v=>Math.round(+v)).join(',');}
}catch(e){}
const tok=(prompt('1/2  Token'+(tok0?' (já encontrado: carrega OK)':'\n(Network > pedido "export" > Payload > token)'),tok0)||'').trim();
if(!tok){console.log('Cancelado: falta o token.');return;}
const ar=(prompt('2/2  Área em EPSG:3763 (PT-TM06): xmin,ymin,xmax,ymax'+(area0?'\n(proposta = o que está visível no mapa)':'\nExemplo: 12237,-28202,16397,-25509'),area0)||'').split(/[,;\s]+/).filter(Boolean).map(Number);
if(ar.length!==4||ar.some(isNaN)||ar[0]>=ar[2]||ar[1]>=ar[3]){console.log('Área inválida. Exemplo: 12237,-28202,16397,-25509');return;}
const T='&token='+encodeURIComponent(tok);
const L=await (await fetch(BASE+'/layers?f=json'+T)).json();
if(L.error){console.log('ERRO: '+JSON.stringify(L.error)+'\nSe diz "Invalid Token", copia o token outra vez.');return;}
const out={layers:L.layers.map(l=>({id:l.id,name:l.name,type:l.type,geom:l.geometryType,parent:l.parentLayer,fields:(l.fields||[]).map(f=>f.name),renderer:l.drawingInfo&&l.drawingInfo.renderer})),area:ar,data:{}};
async function query(id,b){
  const q=BASE+'/'+id+'/query?where=1%3D1&geometry='+b.join(',')+'&geometryType=esriGeometryEnvelope&inSR=3763&outSR=3763&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&f=json'+T;
  return await (await fetch(q)).json();
}
async function todas(id,b,d,acc){            // divide em 4 enquanto o servidor cortar nos 2000
  const r=await query(id,b);
  if(r.error) throw new Error(JSON.stringify(r.error));
  if(r.exceededTransferLimit&&d<10){
    const mx=(b[0]+b[2])/2,my=(b[1]+b[3])/2;
    for(const s of [[b[0],b[1],mx,my],[mx,b[1],b[2],my],[b[0],my,mx,b[3]],[mx,my,b[2],b[3]]]) await todas(id,s,d+1,acc);
    return acc;
  }
  const oid=r.objectIdFieldName||'OBJECTID';
  for(const f of r.features||[]) acc.feats[f.attributes[oid]??JSON.stringify(f.geometry).slice(0,200)]=f;
  if(r.exceededTransferLimit) acc.cortada=true;
  return acc;
}
for(const l of L.layers){
  if(l.type!=='Feature Layer') continue;
  try{
    const acc=await todas(l.id,ar,0,{feats:{},cortada:false});
    const fs=Object.values(acc.feats);
    if(fs.length){out.data[l.id]={features:fs,exceededTransferLimit:acc.cortada};}
    console.log(l.id,l.name,fs.length,acc.cortada?'(INCOMPLETA: reduz a área)':'');
  }catch(e){console.log('ERRO na camada',l.id,l.name,e.message);if(/[Tt]oken/.test(e.message)){console.log('Token expirado: copia outro e volta a colar o script.');return;}}
}
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'}));a.download='PDM_Abrantes.json';a.click();
console.log('FEITO: '+Object.keys(out.data).length+' camadas em PDM_Abrantes.json (pasta Transferências).');
})();
