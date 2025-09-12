import pandas as pd
import matplotlib.pyplot as plt
import LabIFSC2 as lab
import numpy as np
from scipy.optimize import curve_fit

df=pd.read_csv("1/dados_1.csv")
df.drop(columns=["Unnamed: 0","Unnamed: 1",
                 "Unnamed: 2","Unnamed: 5","label1"],
                 inplace=True)
voltagem_scale=5e-2
time_scale=100e-9/len(df)
voltagem=df["label2"].to_numpy()*lab.Medida(voltagem_scale,"V",0)
tempo=lab.arrayM([x*time_scale for x in range(len(df))],"s",0)
unidade_tempo="ns"
unidade_voltagem="mV"
plt.style.use("ggplot")

plt.plot(lab.nominais(tempo,unidade_tempo),
            lab.nominais(voltagem,unidade_voltagem),label="Sinal medido")

def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return (A1 * np.exp(-((x - mu1) ** 2) / (2 * sigma1 ** 2)) +
            A2 * np.exp(-((x - mu2) ** 2) / (2 * sigma2 ** 2)))
p0=np.array([50,35,10,50,60,10])
popt,pcov=curve_fit(double_gaussian,
                    lab.nominais(tempo,unidade_tempo),
          lab.nominais(voltagem,unidade_voltagem),p0=p0)
gaussian_1=lambda x: popt[0] * np.exp(-((x - popt[1]) ** 2) / (2 * popt[2] ** 2))
gaussian_2=lambda x: popt[3] * np.exp(-((x - popt[4]) ** 2) / (2 * popt[5] ** 2))

plt.plot(lab.nominais(tempo,unidade_tempo),
         gaussian_1(lab.nominais(tempo,unidade_tempo)),
         label="Gaussiana 1",linestyle="dashed",color="green")
plt.plot(lab.nominais(tempo,unidade_tempo),
         gaussian_2(lab.nominais(tempo,unidade_tempo)),
         label="Gaussiana 2",linestyle="dashed")
print((popt[4]-popt[1]))
plt.plot(lab.nominais(tempo,unidade_tempo),
         double_gaussian(lab.nominais(tempo,unidade_tempo),*popt),
         label="Soma das gaussianas",linestyle="dashed")
plt.xlabel(f"Tempo ({unidade_tempo})")
plt.ylabel(f"Voltagem ({unidade_voltagem})")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, fancybox=True, shadow=True)
plt.title("Decomposição do sinal em duas gaussianas")
plt.savefig("deconvolucao.png", bbox_inches='tight',pad_inches=0.5,dpi=300)
