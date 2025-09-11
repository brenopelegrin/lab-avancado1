import pandas as pd
import matplotlib.pyplot as plt
import LabIFSC2 as lab
voltagem_scale=5e-2
time_scale=1e-10
df=pd.read_csv("1/dados_1.csv")
df.drop(columns=["Unnamed: 0","Unnamed: 1",
                 "Unnamed: 2","Unnamed: 5","label1"],
                 inplace=True)
voltagem=df["label2"].to_numpy()*lab.Medida(voltagem_scale,"V",0)
tempo=lab.arrayM([x*time_scale for x in range(len(df))],"s",0)
unidade_tempo="ns"
unidade_voltagem="mV"
plt.style.use("ggplot")
plt.plot(lab.nominais(tempo,unidade_tempo),
            lab.nominais(voltagem,unidade_voltagem))

plt.xlabel(f"Tempo ({unidade_tempo})")
plt.ylabel(f"Voltagem ({unidade_voltagem})")
plt.savefig("deconvolucao.png")
