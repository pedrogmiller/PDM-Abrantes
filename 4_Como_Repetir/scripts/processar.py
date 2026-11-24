# Corre os passos 2 a 7 de seguida. É o que o PROCESSAR.bat chama.
# Uso: python processar.py [PDM_Abrantes.json]
# Sem argumento usa o PDM_Abrantes*.json mais recente que encontrar nesta pasta (scripts),
# em 4_Como_Repetir ou nas Transferências; se não houver nenhum, abre uma janela para o escolher.
import os, sys, glob, runpy, subprocess, warnings, traceback
warnings.filterwarnings('ignore')
try: sys.stdout.reconfigure(errors='replace'); sys.stderr.reconfigure(errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))

def fim(msg=''):
    if msg: print(msg)
    try: input('\nCarrega Enter para fechar.')
    except Exception: pass
    sys.exit()

try:
    import geopandas, matplotlib  # noqa: F401
except ImportError:
    import subprocess
    print('A instalar as bibliotecas que faltam (geopandas, matplotlib). Só acontece da primeira vez, pode demorar uns minutos...')
    r = subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', 'geopandas', 'matplotlib'])
    if r != 0:
        fim('Não consegui instalar as bibliotecas. No terminal do VS Code escreve:\n'
            f'    & "{sys.executable}" -m pip install geopandas matplotlib\n'
            'e corre outra vez.')
    import site, importlib; importlib.reload(site); importlib.invalidate_caches()
    sys.path.insert(0, site.getusersitepackages())

def procurar_json():
    pastas = [AQUI, os.path.dirname(AQUI), os.path.join(os.path.expanduser('~'), 'Downloads'),
              os.path.join(os.path.expanduser('~'), 'Transferências')]
    fs = [f for d in pastas for f in glob.glob(os.path.join(d, 'PDM_Abrantes*.json'))]
    return max(fs, key=os.path.getmtime) if fs else None

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

j = sys.argv[1] if len(sys.argv) > 1 else (procurar_json() or escolher_ficheiro())
if not j or not os.path.exists(j): fim('Não encontrei o PDM_Abrantes.json. Copia-o para a pasta 4_Como_Repetir/scripts e corre outra vez.')
print('Ficheiro:', j)
nome = os.path.splitext(os.path.basename(j))[0]
out = os.path.join(os.path.dirname(os.path.abspath(j)), 'resultado_' + nome)
cam, shp = os.path.join(out, '_tecnico', 'camadas_originais'), os.path.join(out, '1_Shapefiles')
try:
    passo(2, '2_json_para_shapefiles.py', j, cam)
    passo(3, '3_separar_por_subcategoria.py', j, cam, shp)
    if os.path.exists(os.path.join(cam, '145_PIF_Abrantes_2025.shp')):
        passo(4, '4_generalizar_PIF.py', cam, shp)
    passo(5, '5_aplicar_cores.py', shp)
    passo(6, '6_gerar_kmz_google_earth.py', shp, os.path.join(out, '2_Google_Earth', 'PDM_regime.kmz'))
    passo(7, '7_gerar_legenda.py', os.path.join(out, 'Legenda_regime.png'))
except SystemExit: raise
except Exception:
    traceback.print_exc(); fim('\nERRO: copia o texto acima e envia-o.')
print('\nFEITO. Resultado em:', out)
try:
    if os.name == 'nt': os.startfile(out)
    elif sys.platform == 'darwin': subprocess.run(['open', out])
except Exception: pass
fim()
