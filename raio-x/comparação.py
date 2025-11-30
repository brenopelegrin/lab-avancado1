from tools import * 
import numpy as np
import matplotlib.pyplot as plt
import os
import json 
import pandas as pd 

def interpolate_log_log_antonio(E_target, E1, mu1, E2, mu2):
    """
    Executa a interpolação log-log para encontrar mu_target.
    """
    log_E_target = np.log(E_target)
    log_E1 = np.log(E1)
    log_E2 = np.log(E2)
    log_mu1 = np.log(mu1)
    log_mu2 = np.log(mu2)

    log_mu_target = log_mu1 + (log_mu2 - log_mu1) * (log_E_target - log_E1) / (log_E2 - log_E1)

    return np.exp(log_mu_target)



plt.style.use("ggplot")
fig,ax=plt.subplots(figsize=(5,5),dpi=150)
ax.grid(True)
ax.set_xlabel("Número atômico (Z)")
ax.set_ylabel(r"Coeficiente de absorção ($\frac{\mu}{\rho}$)")

fig.tight_layout()
df_exp = pd.read_excel('mu_over_rho_experimental.xlsx', header=1)
ax.scatter(df_exp['n_atomico'], 
           df_exp['mu_over_rho'],  
           label='Experimental', 
           color='C0',
           s=10)
E_k_alpha=17479*1e-6
with open('scraper/nist_attenuation_coeffs_20251127_155618.json', 'r') as f:
    data = json.load(f)

Z_values=np.array([x for x in range(1,93)])
mu_over_rho_values=[]
for Z in Z_values:
    data_element=data[str(Z).zfill(2)]
    energies=data_element["energy_MeV"]
    mu_values=data_element["mu_en_rho_cm2_g"]
    energies = np.array(energies)
    mu_over_rho = np.array(mu_values)
    idx = (np.abs(energies - E_k_alpha)).argmin()
    mu=interpolate_log_log_antonio(E_k_alpha, 
                                   energies[idx-1], 
                                   mu_over_rho[idx-1], 
                                   energies[idx], 
                                   mu_over_rho[idx])
    mu_over_rho_values.append(mu)

ax.scatter(Z_values, mu_over_rho_values, label='NIST', color='black',s=10)
ax.plot(Z_values, mu_over_rho_values, color='black',linewidth=0.5,linestyle='dashed')
ax.legend()

fig.savefig("comparacao.png")