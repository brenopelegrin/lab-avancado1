import LabIFSC2 as lab
from LabIFSC2 import Medida
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np 

distancias=2*lab.arrayM([0,472,743,1003,1276],"cm",5)
tempos=lab.arrayM([0,25,50,72,88],"ns",1)

unidade_distancia="m"
unidade_tempo="ns"

plt.style.use("ggplot")
figure,axis=plt.subplots()
a,pcov=curve_fit(lambda x,a: a*x,
                     lab.nominais(tempos,unidade_tempo),
                     lab.nominais(distancias,unidade_distancia))
c=Medida(a[0],f"{unidade_distancia}/{unidade_tempo}",np.sqrt(pcov[0][0]))
x_values=lab.linspaceM(min(lab.nominais(tempos,unidade_tempo)),
                     max(lab.nominais(tempos,unidade_tempo)),100,unidade_tempo,0)
axis.set_xlabel(f"Tempo de voo ({unidade_tempo})")
axis.set_ylabel(f"Distância ida e volta ({unidade_distancia})")
axis.set_title(f"Medição por pulsos c={c:km/s}")
axis.scatter(lab.nominais(tempos,unidade_tempo),
             lab.nominais(distancias,unidade_distancia),
             label="Medições experimentais")


axis.plot(lab.nominais(x_values,unidade_tempo),lab.nominais(x_values*c,unidade_distancia),
             label=f"Ajuste linear",color="blue",linestyle="dashed")

axis.legend(loc="upper center", bbox_to_anchor=(0.5, -0.5), fancybox=True, shadow=True)
figure.savefig("pulsos.png")