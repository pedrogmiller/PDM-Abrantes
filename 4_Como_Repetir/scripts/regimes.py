# Tabela de regime de cada subcategoria (RPDM Abrantes 2026 + RJREN), usada pelos passos 5, 6 e 7.
# Chave: "Pasta/nome do shapefile sem .shp" em 1_Shapefiles.
# Valor: (regime, base legal, cor hex, padrão)   regime: Interdito | Condicionado | Permitido | Informativo
#        padrão: solid | hatch (diagonal) | cross | dots | line | point
# Se o passo 5 disser "em falta", acrescenta aqui essas camadas.
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
