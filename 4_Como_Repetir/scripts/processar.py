# Corre os passos 2 a 7 de seguida. É o que o PROCESSAR.bat chama.
# Uso: python processar.py [PDM_Abrantes.json]   (sem argumento abre uma janela para escolher o ficheiro)
import os, sys, runpy, subprocess, warnings
warnings.filterwarnings('ignore')
AQUI = os.path.dirname(os.path.abspath(__file__))

def escolher_ficheiro():
    try:
        import tkinter as tk; from tkinter import filedialog
        r = tk.Tk(); r.withdraw()
        return filedialog.askopenfilename(title='Escolhe o PDM_Abrantes.json descarregado do browser',
                                          filetypes=[('JSON', '*.json')])
    except Exception:
        return input('Caminho do PDM_Abrantes.json: ').strip().strip('"')

def passo(n, script, *args):
    print(f'\n=== Passo {n}: {script} ===')
    sys.argv = [script, *args]
    runpy.run_path(os.path.join(AQUI, script), run_name='__main__')

j = sys.argv[1] if len(sys.argv) > 1 else escolher_ficheiro()
if not j or not os.path.exists(j): sys.exit('Nenhum ficheiro escolhido.')
nome = os.path.splitext(os.path.basename(j))[0]
out = os.path.join(os.path.dirname(os.path.abspath(j)), 'resultado_' + nome)
cam, shp = os.path.join(out, '_tecnico', 'camadas_originais'), os.path.join(out, '1_Shapefiles')
passo(2, '2_json_para_shapefiles.py', j, cam)
passo(3, '3_separar_por_subcategoria.py', j, cam, shp)
if os.path.exists(os.path.join(cam, '145_PIF_Abrantes_2025.shp')):
    passo(4, '4_generalizar_PIF.py', cam, shp)
passo(5, '5_aplicar_cores.py', shp)
passo(6, '6_gerar_kmz_google_earth.py', shp, os.path.join(out, '2_Google_Earth', 'PDM_regime.kmz'))
passo(7, '7_gerar_legenda.py', os.path.join(out, 'Legenda_regime.png'))
print('\nFEITO. Resultado em:', out)
try:
    if os.name == 'nt': os.startfile(out)
    elif sys.platform == 'darwin': subprocess.run(['open', out])
except Exception: pass
