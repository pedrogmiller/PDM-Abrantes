# Como repetir para outro terreno de Abrantes

Não é preciso saber programar. Depois da preparação, são dois passos: um no browser e outro no computador.

## Preparação (uma vez só)
Num computador da empresa normalmente não se pode instalar programas "a cru". Usa o que a empresa disponibiliza:

1. **Python**, por uma destas vias (sem precisar de administrador):
   - **Microsoft Store:** procura "Python 3.12" (editor: Python Software Foundation) > Obter; ou
   - **Company Portal / Microsoft Store > Visual Studio Code.** Abre o VS Code > ícone dos quadrados à esquerda (Extensions) > instala **Python** (da Microsoft). Se o Python ainda não existir, o VS Code avisa e abre a Microsoft Store para o instalar.
2. **Este repositório:** botão verde **Code > Download ZIP** e descompacta numa pasta tua (por exemplo Documentos).

Para confirmar que o Python ficou instalado: abre o VS Code > menu **Terminal > New Terminal**, escreve `python --version` e Enter. Deve aparecer `Python 3.x`.

## Passo 1. No browser (Chrome ou Edge): localizar o terreno e descarregar o PDM
1. Abre o visualizador MuniSIG da Câmara de Abrantes. Na lista **Layers**, abre **Planos de Ordenamento do Território** e liga o **PDM 2026** (com Ordenamento e Condicionantes). Desliga o **ortofotomapa** e outras camadas pesadas: não entram no download e o mapa fica mais rápido.
   - Não é preciso escolher subcategorias: o script descarrega **todas** as camadas do PDM 2026, ligadas ou não. O PDM 2026 tem de estar ligado só para o script conseguir ler o token e a área do mapa.
2. **Localiza o terreno a analisar** (pesquisa por morada/freguesia ou navega no mapa) e faz zoom até ele **ocupar o ecrã, com a margem que quiseres à volta** (por exemplo 200 m). O que estiver visível é a área que vai ser descarregada. Faz isto **depois** de ligar as camadas: cada movimento do mapa gera um pedido novo, e o script usa o último, que é o da vista final.
3. Carrega em **F12** e, no painel que abre, vai ao separador **Console**.
4. Abre `scripts/1_extrair_tudo.js` com o Bloco de Notas, seleciona tudo (Ctrl+A), copia, cola na Console e carrega Enter. Se o Chrome pedir, escreve primeiro `allow pasting` e Enter.
5. Aparecem duas janelas, normalmente já preenchidas: o **token** e a **área visível**. Carrega OK nas duas.
6. Espera pela linha `FEITO` (alguns minutos). O ficheiro `PDM_Abrantes.json` fica nas Transferências.

**Se a janela do token vier vazia:** separador **Network** do mesmo painel, faz um pequeno zoom no mapa, clica num pedido `export?...` > separador **Payload** > copia o valor de **`token`** e cola-o na janela.
**Se a janela da área vier vazia** (ou quiseres uma área exata): escreve `xmin,ymin,xmax,ymax` em EPSG:3763. No QGIS tiras isto da extensão dos prédios com um buffer (Propriedades da camada > Informação). Exemplo (Amarvento): `12237,-28202,16397,-25509`.

## Passo 2. No computador: gerar os shapefiles
**Opção A, duplo clique:** abre a pasta `4_Como_Repetir` e faz duplo clique em `PROCESSAR.bat`.

**Opção B, pelo VS Code** (se o `.bat` estiver bloqueado):
1. VS Code > **File > Open Folder** > escolhe a pasta `4_Como_Repetir`.
2. Só da primeira vez: **Terminal > New Terminal**, escreve `python -m pip install geopandas matplotlib` e Enter. Espera que acabe.
3. Abre `scripts/processar.py` e carrega no **▶** (canto superior direito).

Nas duas opções abre-se uma janela para escolheres o `PDM_Abrantes.json`. Depois gera tudo sozinho e abre a pasta `resultado_PDM_Abrantes`, ao lado do ficheiro:

| Pasta / ficheiro | O que é |
|---|---|
| `1_Shapefiles/` | Um shapefile por subcategoria, já com cores no QGIS |
| `2_Google_Earth/PDM_regime.kmz` | O mesmo para o Google Earth |
| `Legenda_regime.png` | Legenda |
| `_tecnico/camadas_originais/` | As camadas tal como vieram do servidor (para validar) |

A primeira vez demora mais (instala o que precisa). No Mac usa `PROCESSAR.command`.

## Se aparecer `em falta [...]`
O terreno novo tem subcategorias que não existiam em Amarvento e que ainda não têm regime (interdito, condicionado, permitido). Ficam sem cor. Abre `scripts/regimes.py` com o Bloco de Notas, copia uma linha parecida, muda o nome, o regime, o artigo e a cor (confirma o regime no Regulamento, em `Bibliografia/`) e corre o Passo 2 de novo.

## Problemas comuns
| Mensagem | O que fazer |
|---|---|
| `Invalid Token` ou `Token expirado` | O token expira. Faz zoom no mapa (gera um token novo) e cola o script de novo |
| "O Windows protegeu o computador" | Clica em **Mais informações > Executar mesmo assim** (aparece por o ficheiro vir da internet) |
| `Falta o Python` | Instala o Python pela Microsoft Store ou pelo VS Code (ver Preparação) |
| `pip` falha ou demora muito (rede da empresa) | Pede à IT que libere `pypi.org` ou que instale `geopandas` e `matplotlib` |
| Uma camada aparece como `INCOMPLETA` | A área é demasiado grande. Divide-a em duas |
| Cores aleatórias no Google Earth | Usa o KMZ, não os shapefiles |

## Para quem programa
`PROCESSAR.bat` chama `scripts/processar.py`, que corre os passos 2 a 7 (cada script pode ser corrido sozinho; o uso está na primeira linha de cada um):
`2_json_para_shapefiles` > `3_separar_por_subcategoria` > `4_generalizar_PIF` (manchas < 500 m² absorvidas pela vizinha) > `5_aplicar_cores` (campos REGIME/BASE + .qml) > `6_gerar_kmz_google_earth` > `7_gerar_legenda`. A classificação está em `scripts/regimes.py`.
