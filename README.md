# PDM-Abrantes

Plano Diretor Municipal de Abrantes (PDM 2026) em shapefiles editáveis, com cada subcategoria classificada como **interdita, condicionada ou permitida** para a implantação de uma infrastrutura de producao de Energia Renovavel (e.g. eólico, solar) (Regulamento do PDM + RJREN). Área atual: Herdade da Lampreia (4 prédios + 200 m).

Fonte: MuniSIG de Abrantes, serviço `PMOTs/PDM_2026/MapServer` (polígonos originais da Câmara, não vectorização de imagens). Coordenadas: **EPSG:3763 (PT-TM06/ETRS89)**.

## Como repetir para outro terreno de Abrantes

Não é preciso programar. Guia com todos os cliques e erros comuns: **[4_Como_Repetir/](4_Como_Repetir/)**.

1. **Uma vez só:** instala o **VS Code** do Company Portal ou pela **Microsoft Store** e d~faz download deste repositório (**Code > Download ZIP**).
2. **No browser:** abre o MuniSIG de Abrantes e **localiza o terreno**, enquadrando-o no ecrã com a margem que quiseres. F12 > Console > cola `4_Como_Repetir/scripts/1_extrair_tudo.js`: propõe o token e a área visível, carregas OK e descarrega `PDM_Abrantes.json`.
3. **No computador:** duplo clique em `4_Como_Repetir/PROCESSAR.bat` (ou corre `scripts/processar.py` no VS Code) e escolhe esse ficheiro. Sai uma pasta com os shapefiles coloridos, o KMZ e a legenda.

## O que está no repositório

| Pasta | Para quê |
|---|---|
| **`1_Shapefiles/`** | **O resultado principal.** Um shapefile por subcategoria, em `Ordenamento/` e `Condicionantes/`, já com cores (`.qml`, o QGIS aplica sozinho) e campos `REGIME` e `BASE` (artigo). |
| `2_Google_Earth/` | O mesmo num KMZ com cores, organizado por regime (o Google Earth ignora os `.qml`). |
| `3_Legenda_e_Regras/` | Legenda, matriz de regime com os artigos e a imagem da linha das renováveis da tabela do RJREN. |
| `Bibliografia/` | As leis usadas, em PDF: Regulamento do PDM de Abrantes (Aviso 23477/2026), RJREN (consolidado e DL 166/2008 original, com a tabela do Anexo II), sobreiro (DL 169/2001), Domínio Público Hídrico (Lei 54/2005), RAN (DL 73/2009), oliveiras (DL 120/86) e SGIFR (DL 82/2021). |
| `4_Como_Repetir/` | Guia passo a passo e scripts. |
| `_tecnico/` | Para validar ou refazer: camadas tal como vieram do servidor, JSON originais, PIF generalizada e agregados para o `gerar_implantacao.py`. |

## Cores

![Legenda](3_Legenda_e_Regras/Legenda_regime.png)

- **Vermelhos = interdito.** **Amarelos = condicionado** (ultrapassável com título, parecer, DIUP ou comunicação prévia). Verdes = permitido. Cinzentos = informativo.
- Onde as camadas se sobrepõem, vale a mais restritiva.
- Sobreiros: condicionado (DIUP, DL 169/2001), mas interdito dentro da Estrutura Ecológica Municipal (RPDM art. 42.º c).
- Espaço Florestal de Proteção (art. 97.º) e o alcance do art. 42.º b) a infraestruturas são leituras estritas, a confirmar com a Câmara/CCDR.

## Limitações
- RSLEAT (linhas elétricas) e Portaria 419/2012 (REN) foram citados de memória, sem o texto no repositório; estão marcados com ⚠ na matriz.
- Só o PDM. Rede Natura, servidões aeronáuticas e outras restrições fora do PDM não estão incluídas.
- Os polígonos são inteiros (não recortados pela área pedida).
- A perigosidade de incêndio em `1_Shapefiles/` está generalizada (manchas < 500 m² absorvidas pela vizinha) para se ler bem no mapa. Para medir áreas usa a original exata, `_tecnico/camadas_originais/145_PIF_Abrantes_2025.shp`.
