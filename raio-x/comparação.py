from tools import * 
import numpy as np
import matplotlib.pyplot as plt
import os
import json 
import pandas as pd 
from compton_data import compton_dict

# CPK colors for elements, you can extend this dictionary as needed
element_colors = {
    'H': 'whitesmoke', 'He': 'lightcyan', 'Li': 'violet', 'Be': 'darkseagreen',
    'B': 'lightsalmon', 'C': 'black', 'N': 'blue', 'O': 'red', 'F': 'limegreen',
    'Ne': 'cyan', 'Na': 'darkviolet', 'Mg': 'forestgreen', 'Al': 'darkgray',
    'Si': 'khaki', 'P': 'orange', 'S': 'yellow', 'Cl': 'green', 'Ar': 'aqua',
    'K': 'purple', 'Ca': 'darkgreen', 'Sc': 'lightgray', 'Ti': 'gray',
    'V': 'silver', 'Cr': 'gainsboro', 'Mn': 'rebeccapurple', 'Fe': 'darkorange',
    'Co': 'fuchsia', 'Ni': 'darkgreen', 'Cu': 'chocolate', 'Zn': 'dimgray',
    'Ga': 'darkkhaki', 'Ge': 'gray', 'As': 'violet', 'Se': 'darkorange',
    'Br': 'darkred', 'Kr': 'deepskyblue', 'Rb': 'indigo', 'Sr': 'firebrick',
    'Y': 'lightcyan', 'Zr': 'palegreen', 'Nb': 'lightslategray', 'Mo': 'mediumaquamarine',
    'Tc': 'dimgray', 'Ru': 'lightseagreen', 'Rh': 'lightcoral', 'Pd': 'darkslategray',
    'Ag': 'lightgray', 'Cd': 'darkgoldenrod', 'In': 'indigo', 'Sn': 'slategray',
    'Sb': 'rosybrown', 'Te': 'olivedrab', 'I': 'darkviolet', 'Xe': 'cornflowerblue',
    # Add other elements as needed
}


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
fig,ax=plt.subplots(figsize=(6,6),dpi=150)
ax.grid(True)
ax.set_xlabel("Número atômico (Z)")
ax.set_ylabel(r"Coeficiente de absorção ($\frac{\mu}{\rho}$)")

fig.tight_layout()
df_exp = pd.read_excel('mu_over_rho_experimental.xlsx', header=1)

# Plot each experimental point individually
for index, row in df_exp.iterrows():
    element_symbol = row['elemento'] # Assumes a column named 'elemento' with the symbol (e.g., 'Cu')
    atomic_number = row['n_atomico']
    mu_rho = row['mu_over_rho']
    color = element_colors.get(element_symbol, 'C0') # Default to 'C0' if not in dict
    ax.scatter(atomic_number, 
               mu_rho,  
               color=color,
               s=20, # Increased size for better visibility
               edgecolors='black', # Add edge for contrast
               zorder=3) # Plot on top of the NIST line
    ax.text(atomic_number + 0.5, 
            mu_rho, element_symbol, 
            verticalalignment='center',
            color="blue")


E_k_alpha=17479*1e-6
with open('scraper/nist_attenuation_coeffs_20251127_155618.json', 'r') as f:
    data = json.load(f)

teorico_nist_data = {
    1: 0.373, 2: 0.203, 3: 0.202, 4: 0.265, 5: 0.386, 6: 0.606, 7: 0.889 , 8: 1.284, 9: 1.713 , 10: 2.457,
    11: 3.170, 12: 4.277, 13: 5.339, 14: 6.934, 15: 8.311, 16: 10.406, 17: 11.991, 18: 13.348, 19: 16.876, 20: 20.123,
    21: 21.668, 22: 24.321, 23: 27.065, 24: 31.126, 25: 34.316, 26: 39.035, 27: 42.502, 28: 48.672 , 29: 50.983, 30: 55.993,
    31: 59.009, 32: 63.339, 33: 68.334, 34: 71.866,  35: 78.181, 36: 81.966, 37: 88.005, 38:93.723, 39:100.467, 40:16.979, # <-- K-edge shift
    41: 18.430 , 42:19.690,43:21.224, 44: 22.563, 45: 24.276, 46 : 25.641, 47 : 27.610, 48:28.862, 49: 30.716, 50: 32.239,
    51: 34.049, 52: 35.132, 53: 38.149, 54: 39.765, 55: 42.288, 56: 43.998, 57: 46.683, 58: 49.555, 59: 52.729, 60: 55.047,
    61: 58.466, 62: 60.049, 63:63.245, 64: 65.008, 65: 68.308, 66: 70.869, 67: 74.000, 68: 77.267, 69: 80.893, 70: 83.448,
    71: 87.213,72: 90.243, 73: 93.819, 74: 97.301, 75: 101.019, 76: 103.851, 77: 107.718, 78: 111.289, 79: 115.630, 80: 118.934,
    81: 122.371, 82: 126.232, 83: 130.852, 84:136.650, 85: 130.784, 86: 87.401, 87: 91.012, 88:  93.878, 89: 106.248, 90:105.998 ,
    91: 105.008, 92: 106.439
}

Z_values=np.array([x for x in range(1,93)])
mu_over_rho_values=[]
for Z in Z_values:
    """     data_element=data[str(Z).zfill(2)]
    energies=data_element["energy_MeV"]
    mu_values=data_element["mu_en_rho_cm2_g"]
    energies = np.array(energies)
    mu_over_rho = np.array(mu_values)
    idx = (np.abs(energies - E_k_alpha)).argmin()
    mu=interpolate_log_log_antonio(E_k_alpha, 
                                   energies[idx-1], 
                                   mu_over_rho[idx-1], 
                                   energies[idx], 
                                   mu_over_rho[idx]) """
    mu_over_rho_values.append(teorico_nist_data[Z])

for i, Z in enumerate(Z_values):
    if Z in compton_dict:
        if i==1:
            ax.scatter(Z, compton_dict[Z], color='red', s=10,label='Compton',alpha=0.4)
        else:
            ax.scatter(Z, compton_dict[Z], color='red', s=10,alpha=0.4)
ax.scatter(Z_values, mu_over_rho_values, label='NIST', color='black',s=10,alpha=0.4)
ax.plot(Z_values, mu_over_rho_values, color='black',linewidth=0.5,linestyle='dashed')
ax.legend()

fig.savefig("comparacao.png")