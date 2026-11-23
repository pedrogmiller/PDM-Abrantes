import geopandas as g, os, zipfile, html, sys
SC=sys.argv[1]; R='/mnt/project-files/Amarvento/PDM/por_subcategoria'
ns={}; exec(open(SC+'/estilos.py').read().split('def rgb')[0],ns); M=ns['M']
def abgr(h,a): h=h.lstrip('#'); return f'{a:02x}{h[4:6]}{h[2:4]}{h[0:2]}'
def coords(r): return ' '.join(f'{x:.6f},{y:.6f}' for x,y in r.coords)
def poly(p):
    s='<Polygon><outerBoundaryIs><LinearRing><coordinates>'+coords(p.exterior)+'</coordinates></LinearRing></outerBoundaryIs>'
    for i in p.interiors: s+='<innerBoundaryIs><LinearRing><coordinates>'+coords(i)+'</coordinates></LinearRing></innerBoundaryIs>'
    return s+'</Polygon>'
def geom(gm):
    t=gm.geom_type
    if t=='Polygon': return poly(gm)
    if t=='LineString': return '<LineString><tessellate>1</tessellate><coordinates>'+coords(gm)+'</coordinates></LineString>'
    if t=='Point': return f'<Point><coordinates>{gm.x:.6f},{gm.y:.6f}</coordinates></Point>'
    return '<MultiGeometry>'+''.join(geom(x) for x in gm.geoms)+'</MultiGeometry>'
order={'Interdito':0,'Condicionado':1,'Permitido':2,'Informativo':3}
out=['<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>PDM Abrantes 2026 – regime de implantação (Amarvento)</name>']
folders={}
for i,(k,(reg,base,cor,pat)) in enumerate(M.items()):
    sid=f's{i}'; line=pat in('line',)
    out.append(f'<Style id="{sid}"><LineStyle><color>{abgr(cor,255)}</color><width>{3 if line else 1}</width></LineStyle><PolyStyle><color>{abgr(cor,150)}</color></PolyStyle><IconStyle><color>{abgr(cor,255)}</color><scale>0.6</scale></IconStyle></Style>')
    d=g.read_file(f'{R}/{k}.shp').to_crs(4326); d['geometry']=d.geometry.simplify(0.000005)
    name=k.split('/')[1]
    pm=''.join(f'<Placemark><name>{html.escape(name)}</name><description>{html.escape(reg+" – "+base)}</description><styleUrl>#{sid}</styleUrl>{geom(gm)}</Placemark>' for gm in d.geometry if gm is not None and not gm.is_empty)
    folders.setdefault(reg,[]).append((k.split('/')[0],f'<Folder><name>{html.escape(name)}</name>{"<visibility>0</visibility>" if reg in ("Permitido","Informativo") else ""}{pm}</Folder>'))
for reg in sorted(folders,key=order.get):
    vis='' if reg in ('Interdito','Condicionado') else '<visibility>0</visibility>'
    out.append(f'<Folder><name>{reg.upper()}</name>{vis}')
    for grp in ('Ordenamento','Condicionantes'):
        sub=[f for gname,f in folders[reg] if gname==grp]
        if sub: out.append(f'<Folder><name>{grp}</name>'+''.join(sub)+'</Folder>')
    out.append('</Folder>')
out.append('</Document></kml>')
p='/mnt/project-files/Amarvento/PDM/PDM_Abrantes_regime_Amarvento.kmz'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z: z.writestr('doc.kml',''.join(out))
print(os.path.getsize(p)//1024,'KB')
