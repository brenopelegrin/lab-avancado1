import LabIFSC2 as lab
from LabIFSC2 import Medida
import matplotlib.pyplot as plt


distancias=2*lab.arrayM([472,743,1003,1276],"cm",5)
tempos=lab.arrayM([26,50,72,88],"ns",1)

unidade_distancia="m"
unidade_tempo="ns"

plt.style.use("ggplot")
figure,axis=plt.subplots()
reta=lab.regressao_linear(tempos,distancias)
x_values=lab.linspaceM(min(lab.nominais(tempos,unidade_tempo)),
                     max(lab.nominais(tempos,unidade_tempo)),100,unidade_tempo,0)
axis.set_xlabel(f"Tempo ({unidade_tempo})")
axis.set_ylabel(f"Distância ({unidade_distancia})")
axis.set_title(f"Medição da velocidade da luz (c={reta.a:m/s})")
axis.scatter(lab.nominais(tempos,unidade_tempo),
             lab.nominais(distancias,unidade_distancia),
             label="Medições experimentais")


axis.plot(lab.nominais(x_values,unidade_tempo),reta.amostrar(x_values,unidade_distancia),
             label=f"Ajuste linear",color="blue",linestyle="dashed")

axis.legend(loc="upper center", bbox_to_anchor=(0.5, -0.5), fancybox=True, shadow=True)
figure.savefig("pulsos.png")