# PASSO 8. Legenda PNG a partir de regimes.py.
# Uso: python 8_gerar_legenda.py <saida.png>
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regimes import M
hat={'hatch':'///','cross':'xx','dots':'..','solid':None}
rows=[]
for r in ['Interdito','Condicionado','Permitido','Informativo']:
    rows.append(('H',r)); rows+=[('L',k,v) for k,v in M.items() if v[0]==r]
fig,ax=plt.subplots(figsize=(11,0.28*len(rows)+1.2)); ax.set_xlim(0,10); ax.set_ylim(-len(rows)-2,1); ax.axis('off')
ax.text(0,1,'PDM Abrantes 2026 - regime para implantação de parque eólico (RPDM Aviso 23477/2026 + RJREN DL 166/2008)',fontsize=10,weight='bold',va='center')
for i,row in enumerate(rows):
    y=-i-0.3
    if row[0]=='H': ax.text(0,y,row[1].upper(),fontsize=10,weight='bold',va='center'); continue
    k,(reg,base,c,p)=row[1],row[2]
    if p=='line': ax.plot([0.1,0.6],[y,y],color=c,lw=2.5)
    elif p=='point': ax.plot(0.35,y,'o',color=c,ms=7)
    else: ax.add_patch(Rectangle((0.1,y-0.35),0.5,0.7,facecolor=c,edgecolor='#333',hatch=hat.get(p),lw=0.5))
    ax.text(0.8,y,k.split('/',1)[1]+f'  ({k.split("/")[0]})',fontsize=7.5,va='center')
    ax.text(6.6,y,base,fontsize=6.5,va='center',color='#444')
ax.text(0,-len(rows)-1.2,'Sobreposições: aplica-se sempre o regime mais restritivo. EEM = Estrutura Ecológica Municipal (P1.2).\n'
 'Leitura estrita do regulamento; os pontos marcados "confirmar com a CM" e o alcance do art. 42.º b) a infraestruturas devem ser validados com a Câmara/CCDR.',fontsize=7,va='center',color='#333')
plt.savefig(sys.argv[1],dpi=150,bbox_inches='tight')
