# PDM-Abrantes

Plano Diretor Municipal de Abrantes (PDM 2026) em formato vetorial, para a zona do parque eólico Amarvento (os 4 prédios contratualizados mais 200 m).

Fonte: MuniSIG de Abrantes, serviço ArcGIS `PMOTs/PDM_2026/MapServer`, consultado a 11/11/2026. São os polígonos originais da Câmara, não vectorização de imagens. Sistema de coordenadas: **EPSG:3763 (PT-TM06/ETRS89)**.

## Pastas
| Pasta | Conteúdo |
|---|---|
| `por_subcategoria/Ordenamento` | Um shapefile por subcategoria das plantas P1.1 a P1.3.3; o prefixo é o código da planta |
| `por_subcategoria/Condicionantes` | Um shapefile por subcategoria das plantas P2.1 (REN), P2.2 e P2.3 |
| `agregados/` | `PDM_ordenamento.shp`, `PDM_ordenamento_riscos_EEM.shp` e `PDM_condicionantes.shp`, com o campo `CLASSE`, para usar no `gerar_implantacao.py` |
| `dados/original/` | A resposta original do servidor (Esri JSON, comprimida) |
| `mapas/` | Mapas de verificação |
| `scripts/` | Como foi extraído e convertido |

Os polígonos são inteiros, não recortados pela área.

## Como repetir (ou fazer noutro concelho)
1. Abre o visualizador; em DevTools > Network, filtra por `MapServer` para descobrires o endereço do serviço.
2. Copia o `token` do Payload de um pedido `export`.
3. Cola `scripts/1_extrair_MuniSIG.js` (com o token e a área) na Consola dessa página. Descarrega um JSON.
4. `python scripts/2_json_para_shapefiles.py <json> <pasta>` e depois `scripts/3_separar_por_subcategoria.py`.
5. Camadas com mais de 2000 polígonos ficam cortadas: usa `scripts/4_extrair_camada_grande.js`.

## Limitações
- **PIF 2025 (perigosidade de incêndio) está INCOMPLETA**, porque o servidor devolveu só 2000 polígonos (cerca de 38% da área). Ver `mapas/PIF_incompleto.png`.
- Fora do PDM (por exemplo Rede Natura e servidões aeronáuticas) não está incluído.
