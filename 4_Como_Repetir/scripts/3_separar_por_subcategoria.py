import json, glob, os, re, unicodedata, shutil
import geopandas as g
# PASSO 3. Um shapefile por subcategoria, em Ordenamento/ e Condicionantes/, com nomes sem acentos.
# Uso: python 3_separar_por_subcategoria.py PDM_Abrantes.json <pasta camadas_originais> <pasta 1_Shapefiles>
import sys
J, S, O = sys.argv[1], sys.argv[2], sys.argv[3]
shutil.rmtree(O, ignore_errors=True)
d=json.load(open(J, encoding="utf-8")); L={l['id']:l for l in d['layers']}
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
    src=glob.glob(f'{S}/{k:03d}_*.shp')
    if not src: continue   # ex.: 089 (PIF cortada), substituída pela 145 completa
    x=g.read_file(src[0])
    gt=L[k]['geom']; suf={'esriGeometryPolyline':' (linhas)','esriGeometryPoint':' (pontos)'}.get(gt,'')
    base=clean(L[k]['name'])
    inc=' - INCOMPLETO' if d['data'][str(k)].get('exceededTransferLimit') and k!=145 else ''
    if k in SPLIT:
        x['SUBCAT']=SPLIT[k](x)
        for v,grp in x.groupby('SUBCAT'):
            f=os.path.join(folder, pre+clean(v)+inc+'.shp'); grp.to_file(f, encoding='utf-8'); print(os.path.relpath(f,O), len(grp))
    else:
        f=os.path.join(folder, pre+base+suf+inc+'.shp')
        if os.path.exists(f): f=f[:-4]+f' {k}.shp'
        x.to_file(f, encoding='utf-8'); print(os.path.relpath(f,O), len(x))

# nomes sem acentos (o Windows estraga-os dentro de zips)
def a(t): return unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
for dd,dirs,files in os.walk(O, topdown=False):
    for x in files+dirs:
        if a(x)!=x: os.rename(os.path.join(dd,x),os.path.join(dd,a(x)))
