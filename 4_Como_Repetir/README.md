# Como repetir para outro terreno de Abrantes

Tempo: cerca de 30 minutos. Precisas de Chrome (ou Edge) e de Python 3 com `geopandas` e `matplotlib` (`pip install geopandas matplotlib`).

## 0. Definir a área
A área é um retângulo em **EPSG:3763 (PT-TM06)**: `xmin, ymin, xmax, ymax`.
No QGIS: carrega os prédios, junta 200 m de margem (Vetor > Geoprocessamento > Buffer) e vê a extensão em Propriedades da camada > Informação, com o projeto em EPSG:3763.
Exemplo (Amarvento): `12237,-28202,16397,-25509`.

## 1. Copiar o token do visualizador
1. Abre o visualizador MuniSIG da Câmara de Abrantes e liga qualquer camada do PDM 2026.
2. F12 para abrir o DevTools > separador **Network**. Limpa a lista (ícone 🚫).
3. Faz um pequeno zoom no mapa. Aparecem pedidos chamados `export?...` (se aparecerem vários, qualquer um serve).
4. Clica num deles > separador **Payload** > copia o valor de **`token`**.

O token expira ao fim de algum tempo. Se um script disser `Invalid Token` (erro 498/499), repete este passo.

## 2. Descarregar o PDM
1. Abre `scripts/1_extrair_PDM.js` num editor de texto e muda só as duas linhas do topo: `TOKEN` (o que copiaste) e `AREA`.
2. No DevTools, separador **Console**, cola o script todo e carrega Enter. Se o Chrome pedir, escreve `allow pasting` primeiro.
3. Vais ver uma linha por camada (número, nome, n.º de polígonos). No fim descarrega `PDM_Abrantes.json`.

## 3. Descarregar a perigosidade de incêndio
O servidor só devolve 2000 polígonos por pedido e a PIF tem muitos mais. `scripts/2_extrair_PIF.js` divide a área em blocos até caber.
Muda `TOKEN` e `AREA` da mesma forma, cola na Console e espera pela linha `FEITO`. Descarrega `PIF_Abrantes.json`.

## 4. Converter, separar e colorir
Coloca os dois JSON na pasta `scripts/` e corre, por esta ordem:
```
python 3_json_para_shapefiles.py PDM_Abrantes.json PIF_Abrantes.json saida/camadas_originais
python 4_separar_por_subcategoria.py PDM_Abrantes.json saida/camadas_originais saida/1_Shapefiles
python 5_generalizar_PIF.py saida/camadas_originais saida/1_Shapefiles
python 6_aplicar_cores.py saida/1_Shapefiles
python 7_gerar_kmz_google_earth.py saida/1_Shapefiles saida/PDM_regime.kmz
python 8_gerar_legenda.py saida/Legenda_regime.png
```

| Passo | O que faz |
|---|---|
| 3 | Um shapefile por camada do servidor (`camadas_originais`), incluindo a PIF completa |
| 4 | Um shapefile por subcategoria, em `Ordenamento/` e `Condicionantes/`, nomes sem acentos |
| 5 | PIF legível: manchas < 500 m² passam para a classe vizinha (o original exato fica em `camadas_originais`) |
| 6 | Campos `REGIME` e `BASE` + ficheiro `.qml` de cores ao lado de cada shapefile |
| 7 | KMZ com as mesmas cores para o Google Earth |
| 8 | Legenda PNG |

## 5. Subcategorias novas
A classificação (interdito, condicionado, permitido) está em `scripts/regimes.py`, uma linha por subcategoria com o artigo do RPDM/RJREN e a cor.
Se o passo 6 escrever `em falta [...]`, o terreno novo tem subcategorias que não existiam em Amarvento: acrescenta uma linha para cada uma (confirma o regime no Regulamento, em `3_Legenda_e_Regras/`) e corre os passos 6 a 8 de novo.

## Problemas comuns
- **`Invalid Token`**: o token expirou. Copia-o outra vez (passo 1).
- **Uma camada aparece como `INCOMPLETO`**: tem mais de 2000 polígonos. Adapta `2_extrair_PIF.js` mudando o número da camada (145) no endereço.
- **Nomes estranhos no Windows**: os scripts já tiram os acentos; não renomeies à mão.
- **Cores aleatórias no Google Earth**: usa o KMZ, não os shapefiles.
