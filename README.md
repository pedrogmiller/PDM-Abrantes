# PDM-Abrantes

Plano Diretor Municipal de Abrantes (PDM 2026) em formato vetorial, para a zona do parque eólico Amarvento (os 4 prédios contratualizados mais 200 m).

Fonte: MuniSIG de Abrantes, serviço ArcGIS `PMOTs/PDM_2026/MapServer`, consultado a 11/11/2026. São os polígonos originais da Câmara, não vectorização de imagens. Sistema de coordenadas: **EPSG:3763 (PT-TM06/ETRS89)**.

## Pastas
| Pasta | Conteúdo |
|---|---|
| `por_subcategoria/Ordenamento` | Um shapefile por subcategoria das plantas P1.1 a P1.3.3; o prefixo é o código da planta |
| `por_subcategoria/Condicionantes` | Um shapefile por subcategoria das plantas P2.1 (REN), P2.2 e P2.3 |
| `agregados/` | `PDM_ordenamento.shp`, `PDM_ordenamento_riscos_EEM.shp` e `PDM_condicionantes.shp`, com o campo `CLASSE`, para usar no `gerar_implantacao.py` |
| `camadas_originais/` | As 28 camadas tal como vieram do servidor (prefixo = n.º da camada), para validar as derivadas |
| `PIF/` | Perigosidade de incêndio completa: original exata e generalizada |
| `documentos/` | Regulamento do PDM (Aviso n.º 23477/2026/2) |
| `dados/original/` | A resposta original do servidor (Esri JSON, comprimida) |
| `mapas/` | Mapas de verificação |
| `Matriz_PDM_Abrantes_Amarvento.md` | Regime de cada camada (interdito, condicionado, permitido) com os artigos do RPDM e do RJREN, e o cruzamento com o layout |
| `cruzamento_*.csv` | m² afetados por camada e por turbina |
| `scripts/` | Como foi extraído e convertido |

Os polígonos são inteiros, não recortados pela área.

## Como repetir (ou fazer noutro concelho)
1. Abre o visualizador; em DevTools > Network, filtra por `MapServer` para descobrires o endereço do serviço.
2. Copia o `token` do Payload de um pedido `export`.
3. Cola `scripts/1_extrair_MuniSIG.js` (com o token e a área) na Consola dessa página. Descarrega um JSON.
4. `python scripts/2_json_para_shapefiles.py <json> <pasta>` e depois `scripts/3_separar_por_subcategoria.py`.
5. Camadas com mais de 2000 polígonos ficam cortadas: usa `scripts/4_extrair_camada_grande.js` (foi assim que se obteve a PIF completa, `dados/original/PIF_Abrantes_Amarvento.json.gz`).

## Limitações
- Fora do PDM (por exemplo Rede Natura e servidões aeronáuticas) não está incluído.

## Perigosidade de incêndio
Em `por_subcategoria/` está uma **versão generalizada** (manchas < 500 m² absorvidas pela classe vizinha com maior fronteira comum; 6 781 → 943 polígonos), para visualização. O original exato está em `dados/pif/145_PIF_Abrantes_2025.shp` e é o usado em `cruzamento_layout_PIF.csv`.

## Cores por regime (`por_subcategoria/`)
Cada shapefile tem ao lado um `.qml` com o mesmo nome, que o QGIS aplica automaticamente: vermelhos = interdito, amarelos = condicionado (pode ser ultrapassado com título, parecer, DIUP ou comunicação prévia), verdes = permitido, cinzentos = informativo. Tons e tramas diferentes distinguem as subcategorias dentro do mesmo regime. Cada camada tem os campos `REGIME` e `BASE` (artigo). Legenda em `mapas/Legenda_regime_por_subcategoria.png`. Quando duas camadas se sobrepõem, vale a mais restritiva.

Sobreiros: condicionado (DIUP, DL 169/2001), mas interdito dentro da Estrutura Ecológica Municipal (RPDM art. 42.º c). Espaço Florestal de Proteção (art. 97.º) e o alcance do art. 42.º b) a infraestruturas são leituras estritas, a confirmar com a Câmara/CCDR.

## Google Earth (`kmz/`)
O Google Earth ignora os `.qml`. Para ver as cores, abrir `kmz/PDM_Abrantes_regime_Amarvento.kmz`: pastas por regime (Permitido e Informativo desligados por defeito), com regime e artigo no clique de cada polígono. Scripts: `scripts/5_estilos_regime.py` (campos e .qml), `6_gerar_kmz_google_earth.py`, `7_gerar_legenda.py`.
