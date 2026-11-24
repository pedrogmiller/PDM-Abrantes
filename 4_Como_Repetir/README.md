# Como repetir para outro terreno de Abrantes

Não é preciso saber programar. São dois passos: um no browser e um duplo clique.

**Uma vez só (preparação):** instala o Python em <https://www.python.org/downloads/>. No instalador, **marca a opção "Add python.exe to PATH"**. Depois descarrega este repositório: botão verde **Code > Download ZIP** e descompacta.

## Antes: a área
A área é um retângulo em **EPSG:3763 (PT-TM06)**: `xmin, ymin, xmax, ymax`.
No QGIS: carrega os prédios, junta 200 m de margem (Vetor > Geoprocessamento > Buffer) e vê a extensão em Propriedades da camada > Informação, com o projeto em EPSG:3763.
Exemplo (Amarvento): `12237,-28202,16397,-25509`.

## Passo 1. No browser (Chrome ou Edge): descarregar o PDM
1. Abre o visualizador MuniSIG da Câmara de Abrantes e liga qualquer camada do PDM 2026.
2. Carrega em **F12**. No painel que abre, separador **Network**. Faz um pequeno zoom no mapa.
3. Na lista aparecem pedidos chamados `export?...` (qualquer um serve). Clica num > separador **Payload** > copia o valor de **`token`**.
4. Abre `scripts/1_extrair_tudo.js` com o Bloco de Notas, seleciona tudo e copia.
5. No mesmo painel F12, separador **Console**: cola e carrega Enter. Se o Chrome pedir, escreve primeiro `allow pasting` e Enter.
6. Aparecem duas janelas: cola o **token** na primeira e a **área** na segunda.
7. Espera pela linha `FEITO` (alguns minutos). O ficheiro `PDM_Abrantes.json` fica nas Transferências.

## Passo 2. No computador: duplo clique em `PROCESSAR.bat`
Abre uma janela para escolheres o `PDM_Abrantes.json`. Depois gera tudo sozinho e abre a pasta `resultado_PDM_Abrantes`, ao lado do ficheiro:

| Pasta / ficheiro | O que é |
|---|---|
| `1_Shapefiles/` | Um shapefile por subcategoria, já com cores no QGIS |
| `2_Google_Earth/PDM_regime.kmz` | O mesmo para o Google Earth |
| `Legenda_regime.png` | Legenda |
| `_tecnico/camadas_originais/` | As camadas tal como vieram do servidor (para validar) |

A primeira vez demora mais (instala o que precisa). No Mac usa `PROCESSAR.command`.

## Se aparecer `em falta [...]`
O terreno novo tem subcategorias que não existiam em Amarvento e que ainda não têm regime (interdito, condicionado, permitido). Ficam sem cor. Abre `scripts/regimes.py` com o Bloco de Notas, copia uma linha parecida, muda o nome, o regime, o artigo e a cor (confirma o regime no Regulamento, em `3_Legenda_e_Regras/`) e corre o `PROCESSAR.bat` de novo.

## Problemas comuns
| Mensagem | O que fazer |
|---|---|
| `Invalid Token` ou `Token expirado` | O token expira. Copia outro (Passo 1, ponto 3) e cola o script de novo |
| "O Windows protegeu o computador" | Clica em **Mais informações > Executar mesmo assim** (aparece por o ficheiro vir da internet) |
| `Falta o Python` | Instala o Python e marca "Add python.exe to PATH" |
| Uma camada aparece como `INCOMPLETA` | A área é demasiado grande. Divide-a em duas |
| Cores aleatórias no Google Earth | Usa o KMZ, não os shapefiles |

## Para quem programa
`PROCESSAR.bat` chama `scripts/processar.py`, que corre os passos 2 a 7 (cada script pode ser corrido sozinho; o uso está na primeira linha de cada um):
`2_json_para_shapefiles` > `3_separar_por_subcategoria` > `4_generalizar_PIF` (manchas < 500 m² absorvidas pela vizinha) > `5_aplicar_cores` (campos REGIME/BASE + .qml) > `6_gerar_kmz_google_earth` > `7_gerar_legenda`. A classificação está em `scripts/regimes.py`.
