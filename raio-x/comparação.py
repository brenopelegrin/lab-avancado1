from tools import * 
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd 

plt.style.use("ggplot")
fig,ax=plt.subplots(figsize=(5,5),dpi=150)
ax.grid(True)
ax.set_xlabel("Número atômico (Z)")
ax.set_ylabel(r"Coeficiente de absorção ($\frac{\mu}{\rho}$)")

fig.tight_layout()
df_exp = pd.read_excel('mu_over_rho_experimental.xlsx', header=1)
ax.scatter(df_exp['n_atomico'], df_exp['mu_over_rho'],  label='Experimental', color='C0')


ax.legend()
fig.savefig("comparacao.png")