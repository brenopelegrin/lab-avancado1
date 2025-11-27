import matplotlib.pyplot as plt
import scipy as sci
import numpy as np
import os
from tools import *
directory = "/workspaces/lab-avancado1/raio-x/breno_e_vinicius/bv-lambdamin-sem-zr"
files = [x for x in os.listdir(directory) if x.endswith(".dat")]
files.sort()
plt.style.use("ggplot")
fig, ax = plt.subplots(figsize=(10, 8),dpi=150)
ax.grid(True)
lambda_min = [(9.28, 165.75),
              (10.36, 105.89),
              (10.52, 68.90),
              (12.08, 50.53),
              (13.37, 28.05),
              (14.86, 17.32),
              (17.05, 9.61),
              (18.69,4.00)]
for (x,y) in lambda_min:
    ax.scatter(2*d*np.sin(np.deg2rad(x+0.5)/2)*1e12, y, color="black",marker="x",s=100)
ax.scatter([], [], color="black", marker="x", label="λ min")
lambda_min.sort(reverse=True)
voltagem_marcador={
    1:12.64,
    2:14.36,
    3:16.28,
    4:17.99,
    5:19.67,
    6:21.58,
    7:23.03,
    8:25.69
}

for file in files:
    x,y=read_file(os.path.join(directory, file))
    ax.plot(degree_to_lambda(x)*1e12, y, label=file.replace(".dat", ""))
ax.set_xlabel("Lambda (pm)")
ax.set_ylabel("Contagem")
ax.set_yscale("log")
ax.legend()
fig.savefig("espectros.png")

fig,ax=plt.subplots()
voltagens=[]
lambdas_min=[]

for i in range(1,len(voltagem_marcador)+1):
    voltagens.append(voltagem_marcador[i]*1e3*np.sqrt(2))
    lambdas_min.append(degree_to_lambda(lambda_min[i-1][0]))

voltagens=np.array(voltagens)
voltagens*=1e-3
lambdas_min=np.array(lambdas_min)    
lambdas_min*=1e12
ax.scatter(1/voltagens, lambdas_min, color="red", label="Dados experimentais")
popt, pcov = sci.optimize.curve_fit(lambda x, a: a / x, voltagens, lambdas_min)
x_fit = np.linspace(min(voltagens), max(voltagens), 100)
y_fit = popt[0] / x_fit
y_esperado=1239.8/x_fit
ax.plot(1/x_fit, y_fit, label=f"Ajuste: λ = {popt[0]:.3e} / V", color="blue")
ax.plot(1/x_fit, y_esperado, label="Teórico: λ = 1.238e+03 / V", color="green", linestyle="--")
ax.legend()

ax.grid(True)
ax.set_xlabel("1/V (1/kV)")
ax.set_ylabel("Lambda min (pm)")
fig.savefig("duane_hunt.png")
