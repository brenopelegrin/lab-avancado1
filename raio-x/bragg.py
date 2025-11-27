import matplotlib.pyplot as plt
import os 
from tools import *

directory="/workspaces/lab-avancado1/raio-x/breno_e_vinicius/bv-lif-bragg1"
files = [x for x in os.listdir(directory) if x.endswith(".dat")]
files.sort()
plt.style.use("ggplot")
fig, ax = plt.subplots(figsize=(5,5),dpi=150)
ax.grid(True)
for filename in files:
    x,y=read_file(os.path.join(directory, filename))
    ax.plot(x, y, 
            label="Desacoplado" if "desacop" in filename else "Acoplado")

ax.set_xlabel("Ângulo (graus)")
ax.set_ylabel("Contagem")
ax.legend()
fig.tight_layout()
fig.savefig("bragg-espectros.png")
