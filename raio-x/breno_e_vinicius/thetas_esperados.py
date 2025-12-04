import matplotlib.pyplot as plt
import os 
import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).parent.parent)) 
from tools import *
from scipy.signal import find_peaks
import numpy as np

directory="."
files = [x for x in os.listdir(directory) if x.endswith(".dat")]
files.sort()
plt.style.use("ggplot")
n_values = np.array([1,2,3])

d_values = {
    "bv-espectro-kcl": 0.315,
    "bv-espectro-nacl": 0.282,
    "bv-lif-bragg2": 0.201,
}

lambda_Mo_Ka = 0.071 
lambda_Mo_kb=0.063229

exclusions = {"bv-lif-bragg1", "bv-lambdamin-sem-zr", "__pycache__"} 

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in exclusions]
    folder_name = os.path.basename(root)
    if folder_name not in d_values:
        continue
    d = d_values[folder_name]
    degree_bias=np.deg2rad(0.5)
    if folder_name in ["bv-espectro-kcl", "bv-espectro-nacl"]:
        degree_bias=0.0
    thetas_esperados_ka=np.arcsin(n_values*lambda_Mo_Ka/(2*d))+degree_bias
    thetas_esperados_kb=np.arcsin(n_values*lambda_Mo_kb/(2*d))+degree_bias
    for filename in files:
        if not filename.endswith(".dat"):
            continue
        full_path = os.path.join(root, filename)
        fig,ax=plt.subplots()
        x,y=read_file(full_path)
        ax.plot(x, y,label="Dados Experimentais",color="blue")
        for (index,theta) in enumerate(np.rad2deg(2*thetas_esperados_ka)):
            if theta<x.max():
                ax.axvline(theta, linestyle="--", color="green", label=f"Kα Ordem {n_values[index]}º")
        for (index,theta) in enumerate(np.rad2deg(2*thetas_esperados_kb)):
            if theta<x.max():
                ax.axvline(theta, linestyle=":", color="red", label=f"Kβ Ordem {n_values[index]}º")
        ax.set_xlabel("Ângulo (graus)")
        ax.set_ylabel("Contagem")
        ax.legend()
        fig.tight_layout()
        fig.savefig(full_path.replace(".dat","_thetas.png"))
        plt.close(fig)
