# PASSO 5. Perigosidade de incêndio: a original tem milhares de manchas minúsculas.
# Para visualização, as manchas < MIN m² passam para a classe vizinha com maior fronteira comum.
# O original exato fica em camadas_originais/145_PIF_Abrantes_2025.shp (usar esse para medir áreas).
# Uso: python 5_generalizar_PIF.py <pasta camadas_originais> <pasta 1_Shapefiles> [MIN m², por defeito 500]
import sys, os, geopandas as g
S, O = sys.argv[1], sys.argv[2]; MIN = float(sys.argv[3]) if len(sys.argv) > 3 else 500
G = g.read_file(f'{S}/145_PIF_Abrantes_2025.shp')[['Perigosida','gridcode','geometry']]; G['geometry'] = G.buffer(0)
for it in range(6):
    G = G.reset_index(drop=True); small = G[G.area < MIN]
    if small.empty: break
    s = g.sjoin(small[['geometry']], G[['Perigosida','gridcode','geometry']], predicate='intersects')
    s = s[s.index != s.index_right]
    s['L'] = [small.geometry[i].boundary.intersection(G.geometry[j].boundary).length for i, j in zip(s.index, s.index_right)]
    best = s[s.L > 0.01].sort_values('L').groupby(level=0).tail(1)
    G.loc[best.index, 'Perigosida'] = best.Perigosida.values; G.loc[best.index, 'gridcode'] = best.gridcode.values
    G = G.dissolve(by=['Perigosida','gridcode'], as_index=False).explode(index_parts=False)
G = G.reset_index(drop=True); G['area_m2'] = G.area.round(0)
print('polígonos depois de generalizar:', len(G))
for sec, fold in [('P1.3.2','Ordenamento'), ('P2.2','Condicionantes')]:
    os.makedirs(f'{O}/{fold}', exist_ok=True)
    for v, grp in G.groupby('Perigosida'):
        v = v.replace('é','e')
        grp.to_file(f'{O}/{fold}/{sec} - Perigosidade {v}.shp', encoding='utf-8')
