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
fig, ax = plt.subplots(figsize=(5,5),dpi=150)
ax.grid(True)
n = 1 
lambda_Mo_Ka = 0.071 

for filename in files:
        x,y=read_file(os.path.join(directory, filename))
        line, = ax.plot(x, y, 
                        label="Desacoplado" if "desacop" in filename else "Acoplado")
        peak_index=np.argmax(y)
        peak_x = x[peak_index]
        peak_y = y[peak_index]
        ax.scatter(peak_x, peak_y,marker="X", color=line.get_color())

        theta_rad = np.deg2rad(peak_x/2)
        d = (n * lambda_Mo_Ka) / (2 * np.sin(theta_rad))
        print(f"File: {filename}, Peak Angle (theta): {peak_x:.2f} degrees, Calculated d: {d:.4f} nm")


ax.set_xlabel("Ângulo (graus)")
ax.set_ylabel("Contagem")
ax.legend()
fig.tight_layout()
fig.savefig("acoplado_desacoplado_picos.png")
