import json, re, sys, os, unicodedata
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, Point, LinearRing
# PASSO 3. Converte os JSON do servidor em shapefiles (um por camada).
# Uso: python 3_json_para_shapefiles.py PDM_Abrantes.json PIF_Abrantes.json <pasta camadas_originais>
src, pif, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(outdir, exist_ok=True)
d = json.load(open(src))
L = {l['id']: l for l in d['layers']}
SKIP = {43, 45, 46, 48, 49}  # cartografia / limites administrativos
def poly(rings):
    outers, holes = [], []
    for r in rings:
        if len(r) < 4: continue
        lr = LinearRing(r)
        (holes if lr.is_ccw else outers).append(r)
    ps = [Polygon(o) for o in outers]
    for h in holes:
        hp = Polygon(h)
        for i, p in enumerate(ps):
            if p.contains(hp.representative_point()):
                ps[i] = Polygon(p.exterior.coords, list(map(lambda x: x.coords, p.interiors)) + [h]); break
    ps = [p.buffer(0) if not p.is_valid else p for p in ps]
    return ps[0] if len(ps) == 1 else MultiPolygon([g for p in ps for g in (p.geoms if hasattr(p, 'geoms') else [p])])
def geom(g):
    if 'rings' in g: return poly(g['rings'])
    if 'paths' in g:
        p = g['paths']; return LineString(p[0]) if len(p) == 1 else MultiLineString(p)
    return Point(g['x'], g['y'])
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')[:50]
for k, v in d['data'].items():
    k = int(k)
    if k in SKIP: continue
    l = L[k]
    rows, geoms = [], []
    for f in v['features']:
        if not f.get('geometry'): continue
        geoms.append(geom(f['geometry']))
        a = {kk[:10]: vv for kk, vv in f['attributes'].items() if 'Shape' not in kk and 'SHAPE' not in kk}
        rows.append(a)
    g = gpd.GeoDataFrame(rows, geometry=geoms, crs=3763)
    g['camada'] = l['name'][:254]
    name = f"{k:03d}_{slug(l['name'])}"
    g.to_file(f"{outdir}/{name}.shp", encoding='utf-8')
    print(name, len(g), '(INCOMPLETO)' if v.get('exceededTransferLimit') else '')

# Perigosidade de incêndio completa (substitui as camadas 089/145 cortadas nos 2000 polígonos)
import glob
for f in glob.glob(f"{outdir}/089_*")+glob.glob(f"{outdir}/145_*"): os.remove(f)
P = json.load(open(pif))
rows = [{k[:10]: v for k, v in f['attributes'].items() if 'Shape' not in k and 'SHAPE' not in k} for f in P['features']]
G = gpd.GeoDataFrame(rows, geometry=[poly(f['geometry']['rings']) for f in P['features']], crs=3763)
G.to_file(f"{outdir}/145_PIF_Abrantes_2025.shp", encoding='utf-8')
print('145_PIF_Abrantes_2025', len(G), 'completa')
