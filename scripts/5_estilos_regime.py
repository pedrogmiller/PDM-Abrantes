import geopandas as g, os, sys
R='/mnt/project-files/Amarvento/PDM/por_subcategoria'
# nome: (regime, base, cor, padrão)   padrão: solid | hatch (diagonal) | cross | dots
M={
# ---------- INTERDITO (vermelhos) ----------
'Ordenamento/P1.1 - Espaco florestal de protecao':('Interdito','RPDM art. 97.º (só infraestruturas públicas; confirmar com a CM)','#b2182b','solid'),
'Ordenamento/P1.2 - REN - AIV':('Interdito','RJREN Anexo II (renováveis não compatíveis) + RPDM art. 42.º b)','#67001f','hatch'),
'Ordenamento/P1.2 - REN - AEREHS':('Interdito','RPDM art. 42.º b): EEM, interditos aterros/escavações','#e7298a','hatch'),
'Ordenamento/P1.2 - REN - AEIPRA':('Interdito','RPDM art. 42.º b): EEM, interditos aterros/escavações','#f4a6a6','hatch'),
'Ordenamento/P1.2 - REN - Cursos de agua':('Interdito','RPDM art. 42.º b): EEM, interditos aterros/escavações','#ce1256','cross'),
'Ordenamento/P1.2 - RAN - RAN':('Interdito','RPDM art. 42.º b): EEM, interditos aterros/escavações','#fb6a4a','hatch'),
'Ordenamento/P1.2 - ERPVA - Areas de baixas aluvionares':('Interdito','RPDM art. 42.º b): EEM, interditos aterros/escavações','#a50f15','cross'),
'Ordenamento/P1.3.1 - Areas de Instabilidade de Vertentes':('Interdito','RJREN Anexo II (renováveis não compatíveis); RPDM art. 45.º','#7f0000','solid'),
'Condicionantes/P2.1 - Areas de Instabilidade de Vertentes':('Interdito','RJREN Anexo II (renováveis não compatíveis)','#d7301f','solid'),
'Condicionantes/P2.1 - Escarpas':('Interdito','RJREN Anexo I (escarpas integram a AIV) + Anexo II','#4d0013','solid'),
'Condicionantes/P2.2 - Sobreiros':('Condicionado','DL 169/2001 (DIUP); dentro da EEM interdito (art. 42.º c)','#e0a800','dots'),
# ---------- CONDICIONADO (amarelos) ----------
'Ordenamento/P1.1 - Espaco agricola de producao':('Condicionado','RPDM art. 86.º + regime RAN','#fee391','solid'),
'Ordenamento/P1.1 - Rede eletrica e respetiva Zona de Servidao':('Condicionado','RPDM art. 37.º; servidão elétrica','#bf9b00','hatch'),
'Ordenamento/P1.1 - Rede Eletrica (linhas)':('Condicionado','RPDM art. 37.º; servidão elétrica','#8c6d00','line'),
'Ordenamento/P1.3.2 - rede primaria de faixas de gestao de combustivel (provisoria)':('Condicionado','DL 82/2021 (parecer ICNF)','#fec44f','solid'),
'Ordenamento/P1.3.2 - Perigosidade Alta':('Condicionado','RPDM art. 56.º; DL 82/2021','#ffd92f','solid'),
'Ordenamento/P1.3.2 - Perigosidade Muito Alta':('Condicionado','RPDM art. 56.º; DL 82/2021','#d4a017','solid'),
'Ordenamento/P1.3.3 - RedeEletrica (linhas)':('Condicionado','RPDM art. 57.º; servidão elétrica','#8c6d00','line'),
'Condicionantes/P2.1 - Areas Estrategicas de Infiltracao e de Protecao e Recarga de Aquiferos':('Condicionado','RJREN Anexo II II-f (comunicação prévia CCDR)','#fff7bc','hatch'),
'Condicionantes/P2.1 - Areas de Elevado Risco de Erosao Hidrica do Solo':('Condicionado','RJREN Anexo II II-f (comunicação prévia CCDR)','#e6c200','hatch'),
'Condicionantes/P2.1 - Cursos de Agua e Respetivos Leitos e Margens':('Condicionado','RJREN Anexo II II-f (comunicação prévia CCDR)','#c9a800','cross'),
'Condicionantes/P2.1 - Cursos de Agua (linhas)':('Condicionado','RJREN Anexo II II-f (comunicação prévia CCDR)','#c9a800','line'),
'Condicionantes/P2.2 - Dominio Publico Hidrico':('Condicionado','Lei 54/2005 (título de utilização APA)','#ffeda0','solid'),
'Condicionantes/P2.2 - Dominio Publico Hidrico (linhas)':('Condicionado','Lei 54/2005 (título de utilização APA)','#e0b000','line'),
'Condicionantes/P2.2 - Reserva Agricola Nacional (RAN)':('Condicionado','DL 73/2009 (parecer ERRA)','#f0e442','solid'),
'Condicionantes/P2.2 - Oliveiras':('Condicionado','DL 120/86 (autorização de arranque)','#7a8c00','dots'),
'Condicionantes/P2.2 - Rede Primaria de Faixas de Gestao de Combustivel (Provisoria)':('Condicionado','DL 82/2021 (parecer ICNF)','#fec44f','solid'),
'Condicionantes/P2.2 - Perigosidade Alta':('Condicionado','DL 82/2021','#ffd92f','solid'),
'Condicionantes/P2.2 - Perigosidade Muito Alta':('Condicionado','DL 82/2021','#d4a017','solid'),
'Condicionantes/P2.2 - Pontos de Agua (pontos)':('Condicionado','DFCI (manter acesso)','#b38f00','point'),
'Condicionantes/P2.2 - Rede Viaria Fundamental (linhas)':('Condicionado','DFCI (manter rede)','#806600','line'),
'Condicionantes/P2.3 - Linhas de muito Alta Tensao, Alta Tensao e Media Tensao (linhas)':('Condicionado','Servidão elétrica','#8c6d00','line'),
# ---------- PERMITIDO (verdes) ----------
'Ordenamento/P1.1 - Espaco florestal de producao':('Permitido','RPDM arts. 68.º/8, 79.º, 94.º (compensação florestal)','#74c476','solid'),
'Ordenamento/P1.3.2 - Perigosidade Baixa':('Permitido','—','#c7e9c0','solid'),
'Ordenamento/P1.3.2 - Perigosidade Media':('Permitido','—','#a1d99b','solid'),
'Ordenamento/P1.3.2 - Perigosidade Muito Baixa':('Permitido','—','#31a354','solid'),
'Condicionantes/P2.2 - Perigosidade Baixa':('Permitido','—','#c7e9c0','solid'),
'Condicionantes/P2.2 - Perigosidade Media':('Permitido','—','#a1d99b','solid'),
'Condicionantes/P2.2 - Perigosidade Muito Baixa':('Permitido','—','#31a354','solid'),
# ---------- INFORMATIVO (cinzentos) ----------
'Ordenamento/P1.3.2 - Degradacao e Contaminacao das Aguas Superficiais':('Informativo','Sem restrição específica identificada','#969696','hatch'),
'Ordenamento/P1.3.2 - Degradacao e Contaminacao das Aguas Superficiais (linhas)':('Informativo','Sem restrição específica identificada','#737373','line'),
'Ordenamento/P1.3.2 - Degradacao e Contaminacao dos Aquiferos':('Informativo','Sem restrição específica identificada','#bdbdbd','hatch'),
'Ordenamento/P1.3.2 - Degradacao e Contaminacao dos Solos':('Informativo','Sem restrição específica identificada','#d9d9d9','cross'),
'Ordenamento/P1.3.2 - Erosao Hidrica dos Solos':('Informativo','Sem restrição específica identificada','#a0a0a0','dots'),
}
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
