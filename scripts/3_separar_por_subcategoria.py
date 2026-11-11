import json, glob, os, re, unicodedata, shutil
import geopandas as g
J='/mnt/project-files/PDM_Abrantes_Amarvento.json'; S='/mnt/project-files/Amarvento/PDM/camadas_originais'; O='/mnt/project-files/Amarvento/PDM/por_subcategoria'
shutil.rmtree(O, ignore_errors=True)
d=json.load(open(J)); L={l['id']:l for l in d['layers']}
def chain(i):
    out=[]; l=L[i]
    while l.get('parent') and l['parent'].get('id',-1)>=0: l=L[l['parent']['id']]; out.append(l['name'].strip())
    return list(reversed(out))
def clean(s, n=100):
    s=s.replace('Recursos Naturais / Recursos Hídricos','Recursos Hídricos').replace(' (Cursos de Água, Albufeiras e Lagoas)','').replace('Ran','RAN').replace('Aeipra','AEIPRA').replace('Aerehs','AEREHS').replace('Aiv','AIV')
    s=re.sub(r'[\\/:*?"<>|]+',' ',s); return re.sub(r'\s+',' ',s).strip()[:n]
SPLIT={70:lambda x:x.Atributo3.str.capitalize(), 73:lambda x:x.Atributo2+' - '+x.Atributo3.str.capitalize(), 89:lambda x:'Perigosidade '+x.Perigosida, 145:lambda x:'Perigosidade '+x.Perigosida}
names={}
for k in d['data']:
    k=int(k); c=chain(k)
    if c[0]=='Elementos Base': continue
    sec=next((p for p in c if re.match(r'P\d',p)), c[-1])
    folder=os.path.join(O, c[0]); pre=sec.split()[0]+' - '
    os.makedirs(folder, exist_ok=True)
    src=glob.glob(f'{S}/{k:03d}_*.shp')[0]; x=g.read_file(src)
    gt=L[k]['geom']; suf={'esriGeometryPolyline':' (linhas)','esriGeometryPoint':' (pontos)'}.get(gt,'')
    base=clean(L[k]['name'])
    inc=' - INCOMPLETO' if d['data'][str(k)].get('exceededTransferLimit') else ''
    if k in SPLIT:
        x['SUBCAT']=SPLIT[k](x)
        for v,grp in x.groupby('SUBCAT'):
            f=os.path.join(folder, pre+clean(v)+inc+'.shp'); grp.to_file(f, encoding='utf-8'); print(os.path.relpath(f,O), len(grp))
    else:
        f=os.path.join(folder, pre+base+suf+inc+'.shp')
        if os.path.exists(f): f=f[:-4]+f' {k}.shp'
        x.to_file(f, encoding='utf-8'); print(os.path.relpath(f,O), len(x))
