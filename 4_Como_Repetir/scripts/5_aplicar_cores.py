# PASSO 5. Escreve os campos REGIME e BASE e um .qml (cores para o QGIS) ao lado de cada shapefile.
# Uso: python 5_aplicar_cores.py <pasta 1_Shapefiles>
import geopandas as g, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regimes import M
R=sys.argv[1]
def rgb(h): h=h.lstrip('#'); return ','.join(str(int(h[i:i+2],16)) for i in (0,2,4))
def dark(h,f=0.6): h=h.lstrip('#'); return ','.join(str(int(int(h[i:i+2],16)*f)) for i in (0,2,4))
HEAD="<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n<qgis version=\"3.28.0\" styleCategories=\"Symbology\">\n <renderer-v2 type=\"singleSymbol\" symbollevels=\"0\" enableorderby=\"0\" forceraster=\"0\" referencescale=\"-1\">\n  <symbols>\n"
TAIL="  </symbols>\n </renderer-v2>\n</qgis>\n"
def opt(d): return '      <Option type="Map">\n'+''.join(f'       <Option name="{k}" value="{v}" type="QString"/>\n' for k,v in d.items())+'      </Option>\n'
def lay(cls,d): return f'    <layer class="{cls}" enabled="1" pass="0" locked="0">\n'+opt(d)+'    </layer>\n'
def qml(cor,pat):
    c=rgb(cor); o=dark(cor)
    if pat=='line':
        return HEAD+'   <symbol type="line" name="0" alpha="1" clip_to_extent="1" force_rhr="0">\n'+lay('SimpleLine',{'line_color':c+',255','line_width':'0.6','line_width_unit':'MM','line_style':'solid'})+'   </symbol>\n'+TAIL
    if pat=='point':
        return HEAD+'   <symbol type="marker" name="0" alpha="1" clip_to_extent="1" force_rhr="0">\n'+lay('SimpleMarker',{'color':c+',255','name':'circle','size':'3','outline_color':o+',255','outline_width':'0.3'})+'   </symbol>\n'+TAIL
    base=lay('SimpleFill',{'color':c+',140','style':'solid','outline_color':o+',255','outline_width':'0.3','outline_style':'solid'})
    extra={'hatch':'b_diagonal','cross':'diagonal_x','dots':'dense6'}.get(pat)
    if extra: base+=lay('SimpleFill',{'color':o+',255','style':extra,'outline_style':'no'})
    return HEAD+'   <symbol type="fill" name="0" alpha="1" clip_to_extent="1" force_rhr="0">\n'+base+'   </symbol>\n'+TAIL
missing=[]
for root,_,fs in os.walk(R):
    for f in fs:
        if not f.endswith('.shp'): continue
        k=os.path.relpath(os.path.join(root,f[:-4]),R)
        if k not in M: missing.append(k); continue
        reg,base,cor,pat=M[k]
        p=os.path.join(root,f); d=g.read_file(p); d['REGIME']=reg; d['BASE']=base[:254]; d.to_file(p,encoding='utf-8')
        open(p[:-4]+'.qml','w',encoding='utf-8').write(qml(cor,pat))
print('em falta',missing); print(len(M))
