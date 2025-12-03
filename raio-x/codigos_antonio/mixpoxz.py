import numpy as np
import matplotlib.pyplot as plt
import re

# --- 1. Funções de Cálculo (sem alteração) ---

def calculate_mu_rho(I, sigma_I, I0, sigma_I0, x_mm, rho):
    """
    Calcula o coeficiente de atenuação de massa (mu/rho) e sua incerteza.
    A espessura x é convertida de mm para cm.
    """
    x_cm = x_mm / 10.0
    mu = -np.log(I / I0) / x_cm

    term_I = (sigma_I / I)**2
    term_I0 = (sigma_I0 / I0)**2
    sigma_mu = (1.0 / x_cm) * np.sqrt(term_I + term_I0)

    mu_rho = mu / rho
    sigma_mu_rho = sigma_mu / rho

    return mu_rho, sigma_mu_rho

def weighted_average(values, uncertainties):
    """
    Calcula a média ponderada e a incerteza da média.
    """
    weights = 1.0 / (uncertainties**2)
    weighted_mean = np.sum(values * weights) / np.sum(weights)
    sigma_weighted_mean = np.sqrt(1.0 / np.sum(weights))
    return weighted_mean, sigma_weighted_mean

# --- 2. Dados de Entrada e Processamento (sem alteração) ---

# Dicionário com informações dos materiais (Z, rho)
material_props = {
    'Al': {'Z': 13, 'rho': 2.70},
    'Fe': {'Z': 26, 'rho': 7.87},
    'Cu': {'Z': 29, 'rho': 8.96},
    'Zr': {'Z': 40, 'rho': 6.5},
    'Nb': {'Z': 41, 'rho': 8.57},
    'Mo': {'Z': 42, 'rho': 10.2},
    'Ag': {'Z': 47, 'rho': 10.49},
    'In': {'Z': 49, 'rho': 7.31},
    'Sn': {'Z': 50, 'rho': 7.3}, # Estanho (beta-estanho), Z=50
}

# --- Materiais do Grupo 1 (I0 comum) ---
I0_1 = 926.03
sigma_I0_1 = 1.40
data_grupo_1 = {
    'Al': (0.5, 500.7, 3.40),
    'Fe': (0.05, 235.87, 0.63),
    'Ag': (0.05, 280.7, 2.62),
    'Zr': (0.05, 561.73, 2.15),
    'Nb': (0.16, 293.5, 4.08),
    'Mo': (0.10, 156.5, 3.13),
}

exp_results = []
# print("Calculando mu/rho para o Grupo 1...") # Silenciado
for material, data in data_grupo_1.items():
    x_mm, I, sigma_I = data
    Z = material_props[material]['Z']
    rho = material_props[material]['rho']
    mu_rho, sigma_mu_rho = calculate_mu_rho(I, sigma_I, I0_1, sigma_I0_1, x_mm, rho)
    exp_results.append({
        'label': material,
        'Z': Z,
        'mu_rho': mu_rho,
        'sigma': sigma_mu_rho
    })

# --- Materiais do Grupo 2 (Cobre, Índio e Estanho) ---
I0_2 = 1008.66
sigma_I0_2 = 9.00
data_cu = [
    (0.06, 113.17, 4.64), (0.07, 72.33, 2.15), (0.12, 9.40, 0.65),
    (0.18, 1.43, 0.51), (0.24, 0.53, 0.12),
]
data_in = [
    (0.10, 143.83, 2.10), (0.20, 58.47, 1.30), (0.30, 6.53, 0.31),
]
data_sn = (0.12, 386.73, 4.38)

rho_cu = material_props['Cu']['rho']
cu_values = []
cu_sigmas = []
for data in data_cu:
    mu_rho, sigma_mu_rho = calculate_mu_rho(data[1], data[2], I0_2, sigma_I0_2, data[0], rho_cu)
    cu_values.append(mu_rho)
    cu_sigmas.append(sigma_mu_rho)
mean_cu, sigma_cu = weighted_average(np.array(cu_values), np.array(cu_sigmas))
exp_results.append({
    'label': 'Cu', 'Z': material_props['Cu']['Z'], 'mu_rho': mean_cu, 'sigma': sigma_cu
})

rho_in = material_props['In']['rho']
in_values = []
in_sigmas = []
for data in data_in:
    mu_rho, sigma_mu_rho = calculate_mu_rho(data[1], data[2], I0_2, sigma_I0_2, data[0], rho_in)
    in_values.append(mu_rho)
    in_sigmas.append(sigma_mu_rho)
mean_in, sigma_in = weighted_average(np.array(in_values), np.array(in_sigmas))
exp_results.append({
    'label': 'In', 'Z': material_props['In']['Z'], 'mu_rho': mean_in, 'sigma': sigma_in
})

rho_sn = material_props['Sn']['rho']
mean_sn, sigma_sn = calculate_mu_rho(data_sn[1], data_sn[2], I0_2, sigma_I0_2, data_sn[0], rho_sn)
exp_results.append({
    'label': 'Sn', 'Z': material_props['Sn']['Z'], 'mu_rho': mean_sn, 'sigma': sigma_sn
})
print("Cálculos experimentais concluídos.")

# --- 3. Dados Teóricos ---
# Dados tabelados (antigos, com inconsistências)
tabelado_data = {
    13: 5.3, 21: 21.1, 26: 38.3, 27: 41.6, 28: 47.4, 29: 49.7,
    30: 54.8, 31: 57.3, 32: 63.4, 33: 69.5, 34: 74.0, 35: 82.2,
    36: 88.1, 37: 94.4, 38: 101.2, 39: 108.9, 40: 17.2, 41: 18.7,
    42: 20.2, 47: 28.6, 49: 31.8, 2: 0.18, 3: 0.22, 4: 0.3,
    5: 0.45, 6: 0.7, 7: 1.1, 8: 1.5, 9: 1.93, 10: 2.67, 11: 3.36,
    12: 4.38, 14: 6.7, 15: 7.98, 16: 10.0, 17: 11.6, 18: 12.6,
    19: 16.7, 20: 19.9, 22: 23.7, 23: 26.5, 24: 30.4, 25: 33.5,
    44: 23.4, 45: 25.3, 46: 26.7, 48: 29.9, 50: 33.3, 51: 35.3,
    52: 36.1, 53: 39.2, 54: 41.3, 55: 43.3, 56: 45.2, 58: 52,
    73: 101, 74: 105, 76: 113, 77: 118, 78: 123, 79: 128, 80: 132,
    81: 136, 82: 141, 83: 145, 88: 172, 90: 143, 92: 153,
}

# Dados teóricos do NIST (Valores interpolados para 17.2 keV)
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

# Mapa de elementos para a tabela LaTeX
element_map = {
    1: ("Hidrogênio", "H"), 2: ("Hélio", "He"), 3: ("Lítio", "Li"), 4: ("Berílio", "Be"),
    5: ("Boro", "B"), 6: ("Carbono", "C"), 7: ("Nitrogênio", "N"), 8: ("Oxigênio", "O"),
    9: ("Flúor", "F"), 10: ("Neônio", "Ne"), 11: ("Sódio", "Na"), 12: ("Magnésio", "Mg"),
    13: ("Alumínio", "Al"), 14: ("Silício", "Si"), 15: ("Fósforo", "P"), 16: ("Enxofre", "S"),
    17: ("Cloro", "Cl"), 18: ("Argônio", "Ar"), 19: ("Potássio", "K"), 20: ("Cálcio", "Ca"),
    21: ("Escândio", "Sc"), 22: ("Titânio", "Ti"), 23: ("Vanádio", "V"), 24: ("Cromo", "Cr"),
    25: ("Manganês", "Mn"), 26: ("Ferro", "Fe"), 27: ("Cobalto", "Co"), 28: ("Níquel", "Ni"),
    29: ("Cobre", "Cu"), 30: ("Zinco", "Zn"), 31: ("Gálio", "Ga"), 32: ("Germânio", "Ge"),
    33: ("Arsênio", "As"), 34: ("Selênio", "Se"), 35: ("Bromo", "Br"), 36: ("Criptônio", "Kr"),
    37: ("Rubídio", "Rb"), 38: ("Estrôncio", "Sr"), 39: ("Ítrio", "Y"), 40: ("Zircônio", "Zr"),
    41: ("Nióbio", "Nb"), 42: ("Molibdênio", "Mo"), 43: ("Tecnécio", "Tc"), 44: ("Rutênio", "Ru"),
    45: ("Ródio", "Rh"), 46: ("Paládio", "Pd"), 47: ("Prata", "Ag"), 48: ("Cádmio", "Cd"),
    49: ("Índio", "In"), 50: ("Estanho", "Sn"), 51: ("Antimônio", "Sb"), 52: ("Telúrio", "Te"),
    53: ("Iodo", "I"), 54: ("Xenônio", "Xe"), 55: ("Césio", "Cs"), 56: ("Bário", "Ba"),
    57: ("Lantânio", "La"), 58: ("Cério", "Ce"), 59: ("Praseodímio", "Pr"), 60: ("Neodímio", "Nd"),
    61: ("Promécio", "Pm"), 62: ("Samário", "Sm"), 63: ("Európio", "Eu"), 64: ("Gadolínio", "Gd"),
    65: ("Térbio", "Tb"), 66: ("Disprósio", "Dy"), 67: ("Hôlmio", "Ho"), 68: ("Érbio", "Er"),
    69: ("Túlio", "Tm"), 70: ("Itérbio", "Yb"), 71: ("Lutécio", "Lu"), 72: ("Háfnio", "Hf"),
    73: ("Tântalo", "Ta"), 74: ("Tungstênio", "W"), 75: ("Rênio", "Re"), 76: ("Ósmio", "Os"),
    77: ("Irídio", "Ir"), 78: ("Platina", "Pt"), 79: ("Ouro", "Au"), 80: ("Mercúrio", "Hg"),
    81: ("Tálio", "Tl"), 82: ("Chumbo", "Pb"), 83: ("Bismuto", "Bi"), 84: ("Polônio", "Po"),
    85: ("Ástato", "At"), 86: ("Radônio", "Rn"), 87: ("Frâncio", "Fr"), 88: ("Rádio", "Ra"),
    89: ("Actínio", "Ac"), 90: ("Tório", "Th"), 91: ("Protactínio", "Pa"), 92: ("Urânio", "U")
}


# --- 4. Preparação para Plotagem (Funções Modificadas) ---

plt.style.use('dark_background')

# --- Preparar Dados Experimentais ---
exp_results.sort(key=lambda x: x['Z'])
Z_exp = [item['Z'] for item in exp_results]
y_exp = [item['mu_rho'] for item in exp_results]
y_err_exp = [item['sigma'] for item in exp_results]
labels_exp = [item['label'] for item in exp_results]

colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF', '#DA70D6', '#ADFF2F']
exp_color_map = {labels_exp[i]: colors[i % len(colors)] for i in range(len(labels_exp))}
exp_Z_to_label_map = {item['Z']: item['label'] for item in exp_results}

# --- Função para plotar pontos experimentais (MODIFICADA para triângulos) ---
def plot_experimental_points(ax):
    """Plota os pontos experimentais como triângulos coloridos."""
    for i in range(len(Z_exp)):
        z = Z_exp[i]
        y = y_exp[i]
        err = y_err_exp[i]
        label = labels_exp[i]
        color = exp_color_map[label]

        ax.errorbar(
            z, y, yerr=err, fmt='^', color=color, capsize=5, # <-- 'o' mudou para '^'
            markersize=8, label=f"{label} (Exp.)", zorder=10
        )
        ax.text(z + 0.6, y, label, color=color, fontsize=7, fontweight='bold',
                 va='center', ha='left', zorder=11)

# --- 5. Preparação dos Dados Teóricos para Plotagem (MODIFICADO) ---

# --- Preparar dados NIST ---
valid_nist = {z: y for z, y in teorico_nist_data.items() if y is not None}
nist_sorted = sorted(valid_nist.items())
# Listas para todos os pontos da linha
Z_nist = [item[0] for item in nist_sorted]
y_nist = [item[1] for item in nist_sorted]
Z_nist_cubed = [z**3 for z in Z_nist]

# Listas separadas para pontos 'medidos' vs 'outros'
Z_nist_medido, y_nist_medido, c_nist_medido = [], [], []
Z_nist_outros, y_nist_outros = [], []

for z, y in nist_sorted: # nist_sorted é [(z, y), ...]
    if z in exp_Z_to_label_map:
        Z_nist_medido.append(z)
        y_nist_medido.append(y)
        c_nist_medido.append(exp_color_map[exp_Z_to_label_map[z]])
    else:
        Z_nist_outros.append(z)
        y_nist_outros.append(y)

# --- Preparar dados Tabelados ---
valid_tabelado = {z: y for z, y in tabelado_data.items() if y is not None}
tabelado_sorted = sorted(valid_tabelado.items())
# Listas para todos os pontos da linha
Z_tabelado = [item[0] for item in tabelado_sorted]
y_tabelado = [item[1] for item in tabelado_sorted]
Z_tabelado_cubed = [z**3 for z in Z_tabelado]

# Listas separadas
Z_tab_medido, y_tab_medido, c_tab_medido = [], [], []
Z_tab_outros, y_tab_outros = [], []

for z, y in tabelado_sorted: # tabelado_sorted é [(z, y), ...]
    if z in exp_Z_to_label_map:
        Z_tab_medido.append(z)
        y_tab_medido.append(y)
        c_tab_medido.append(exp_color_map[exp_Z_to_label_map[z]])
    else:
        Z_tab_outros.append(z)
        y_tab_outros.append(y)


# --- 6. PLOTAGEM (MODIFICADO para 'loc=upper left') ---

# --- Gráfico 1: mu/rho vs Z^3 (NIST vs Tabelado, Sem Exp) ---
fig1, ax1 = plt.subplots(figsize=(14, 9))

# NIST: Linha tracejada vermelha com quadrados vermelhos
ax1.plot(Z_nist_cubed, y_nist, 'rs--', linewidth=1.2, markersize=5, label='Teórico (NIST)', fillstyle='full') # <-- MODIFICADO

# Tabelado: Linha tracejada verde com triângulos verdes
ax1.plot(Z_tabelado_cubed, y_tabelado, 'g^--', linewidth=1.2, markersize=5, label='Teórico (Tabelado)', fillstyle='full') # <-- MODIFICADO


# Configurações do Gráfico 1
ax1.set_xlabel('Número Atômico ao Cubo ($Z^3$)', fontsize=14, color='white')
ax1.set_ylabel('Coeficiente de Atenuação de Massa ($\mu / \\rho$) [cm²/g]', fontsize=14, color='white')
ax1.set_title('Coeficiente de Atenuação vs $Z^3$ (NIST vs Tabelado)', fontsize=16, color='white')
legend1 = ax1.legend(facecolor='black', edgecolor='white', fontsize=10, loc='upper left')
plt.setp(legend1.get_texts(), color='white')
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
max_y = max(max(y_nist, default=0), max(y_tabelado, default=0))
max_x = max(max(Z_nist_cubed, default=0), max(Z_tabelado_cubed, default=0))
ax1.set_ylim(0, max_y * 1.05)
ax1.set_xlim(0, max_x * 1.05)
fig1.tight_layout()


# --- Gráfico 2: mu/rho vs Z (NIST vs Tabelado, Sem Exp) ---
fig2, ax2 = plt.subplots(figsize=(14, 9))

# NIST: Linha tracejada vermelha com quadrados vermelhos
ax2.plot(Z_nist, y_nist, 'rs--', linewidth=1.2, markersize=5, label='Teórico (NIST)', fillstyle='full') # <-- MODIFICADO

# Tabelado: Linha tracejada verde com triângulos verdes
ax2.plot(Z_tabelado, y_tabelado, 'g^--', linewidth=1.2, markersize=5, label='Teórico (Tabelado)', fillstyle='full') # <-- MODIFICADO

# Configurações do Gráfico 2
ax2.set_xlabel('Número Atômico (Z)', fontsize=14, color='white')
ax2.set_ylabel('Coeficiente de Atenuação de Massa ($\mu / \\rho$) [cm²/g]', fontsize=14, color='white')
ax2.set_title('Coeficiente de Atenuação vs Z (NIST vs Tabelado)', fontsize=16, color='white')
legend2 = ax2.legend(facecolor='black', edgecolor='white', fontsize=10, loc='upper left')
plt.setp(legend2.get_texts(), color='white')
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')
ax2.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
ax2.set_xlim(0, 95)
ax2.set_ylim(0, max_y * 1.05)
fig2.tight_layout()


# --- Gráfico 3: mu/rho vs Z (Exp vs Tabelado) ---
fig3, ax3 = plt.subplots(figsize=(14, 9))

# Tabelado: Linha tracejada branca
ax3.plot(Z_tabelado, y_tabelado, 'w--', linewidth=1.2, label='Teórico (Tabelado)')
# Tabelado 'Outros': Triângulos brancos
ax3.plot(Z_tab_outros, y_tab_outros, 'w^', markersize=5, fillstyle='none') # 'none' para ver sobreposição
# Tabelado 'Medidos': Triângulos coloridos
for z, y, c in zip(Z_tab_medido, y_tab_medido, c_tab_medido):
    ax3.plot(z, y, '^', color=c, markersize=8, fillstyle='full', zorder=5) # Maiores para ver

# Experimental: Triângulos coloridos (com barras de erro)
plot_experimental_points(ax3)

# Configurações do Gráfico 3
ax3.set_xlabel('Número Atômico (Z)', fontsize=14, color='white')
ax3.set_ylabel('Coeficiente de Atenuação de Massa ($\mu / \\rho$) [cm²/g]', fontsize=14, color='white')
ax3.set_title('Coeficiente de Atenuação vs Z (Experimental vs Tabelado)', fontsize=16, color='white')
legend3 = ax3.legend(facecolor='black', edgecolor='white', fontsize=10, loc='upper left')
plt.setp(legend3.get_texts(), color='white')
ax3.tick_params(axis='x', colors='white')
ax3.tick_params(axis='y', colors='white')
ax3.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
ax3.set_xlim(0, 95)
max_y_exp = max(y_exp, default=0)
max_y_tab = max(y_tabelado, default=0)
ax3.set_ylim(0, max(max_y_exp, max_y_tab) * 1.05)
fig3.tight_layout()


# --- Gráfico 4: mu/rho vs Z (Exp vs NIST) ---
fig4, ax4 = plt.subplots(figsize=(14, 9))

# NIST: Linha tracejada branca
ax4.plot(Z_nist, y_nist, 'w--', linewidth=1.2, label='Teórico (NIST)')
# NIST 'Outros': Quadrados brancos
ax4.plot(Z_nist_outros, y_nist_outros, 'ws', markersize=5, fillstyle='none') # 'none' para ver sobreposição
# NIST 'Medidos': Quadrados coloridos
for z, y, c in zip(Z_nist_medido, y_nist_medido, c_nist_medido):
    ax4.plot(z, y, 's', color=c, markersize=8, fillstyle='full', zorder=5) # Maiores para ver

# Experimental: Triângulos coloridos (com barras de erro)
plot_experimental_points(ax4)

# Configurações do Gráfico 4
ax4.set_xlabel('Número Atômico (Z)', fontsize=14, color='white')
ax4.set_ylabel('Coeficiente de Atenuação de Massa ($\mu / \\rho$) [cm²/g]', fontsize=14, color='white')
ax4.set_title('Coeficiente de Atenuação vs Z (Experimental vs NIST)', fontsize=16, color='white')
legend4 = ax4.legend(facecolor='black', edgecolor='white', fontsize=10, loc='upper left')
plt.setp(legend4.get_texts(), color='white')
ax4.tick_params(axis='x', colors='white')
ax4.tick_params(axis='y', colors='white')
ax4.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
ax4.set_xlim(0, 95)
max_y_nist = max(y_nist, default=0)
ax4.set_ylim(0, max(max_y_exp, max_y_nist) * 1.05)
fig4.tight_layout()

# Exibir todos os gráficos
plt.show()


# --- 7. Geração da Tabela LaTeX (imprime no console) ---

print("\n" + "="*60)
print("     TABELA LATEX (Coeficientes NIST @ ~17.2 keV)")
print("="*60 + "\n")

latex_table_str_list = []
latex_table_str_list.append("\\begin{table}[h]")
latex_table_str_list.append("  \\centering")
latex_table_str_list.append("  \\caption{Coeficientes de Atenuação de Massa Teóricos (NIST) para $E \\approx 17.2$ keV.}")
latex_table_str_list.append("  \\label{tab:nist_coef}")
latex_table_str_list.append("  \\begin{tabular}{|c|c|c|c|}")
latex_table_str_list.append("    \\hline")
latex_table_str_list.append("    \\textbf{Nome} & \\textbf{Símbolo} & \\textbf{Z} & \\textbf{Coeficiente (cm$^{2}$/g)} \\\\")
latex_table_str_list.append("    \\hline")

for z in range(1, 93):
    nome, simbolo = element_map.get(z, ("Desconhecido", "??"))
    coef = teorico_nist_data.get(z)

    if coef is not None:
        coef_str = f"{coef:.3f}"
    else:
        coef_str = "N/D"

    latex_table_str_list.append(f"    {nome} & {simbolo} & {z} & {coef_str} \\\\")

latex_table_str_list.append("    \\hline")
latex_table_str_list.append("  \\end{tabular}")
latex_table_str_list.append("\\end{table}")

# Imprime a tabela no console
print("\n".join(latex_table_str_list))


# --- 8. Geração da Tabela LaTeX em PNG (MODIFICADO - Sem LaTeX) ---

print("\n" + "="*60)
print("     Gerando Tabela LaTeX em PNGs (Método Matplotlib)")
print("="*60 + "\n")
print("A tabela será dividida em 3 arquivos PNG (tabela_nist_parte1.png, ...)")

def save_table_as_png_plt(data, col_labels, filename, title_text):
    """
    Salva uma tabela em um arquivo PNG usando o plt.table()
    (Versão corrigida para evitar saída em branco)
    """
    try:
        # Número de linhas
        num_rows = len(data)

        # Altura da figura baseada no número de linhas
        # Aprox 0.35 polegadas por linha + 1.5 para o título/espaçamento
        fig_height = num_rows * 0.35 + 1.5

        fig, ax = plt.subplots(figsize=(8, fig_height), facecolor='white')

        # Esconde os eixos e o frame
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_frame_on(False)

        # Título
        # Usando r'' para string de formatação (para o LaTeX de $E \approx 17.2$ keV)
        ax.set_title(r'' + title_text, fontsize=14, loc='center', pad=20)

        # Cria a tabela
        table = ax.table(
            cellText=data,
            colLabels=col_labels,
            loc='center',
            cellLoc='center',
            colWidths=[0.3, 0.15, 0.1, 0.25] # Ajuste das larguras das colunas
        )

        # Formata as células
        for (i, j), cell in table.get_celld().items():
            if i == 0: # Linha do cabeçalho
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#E0E0E0') # Cor de fundo cinza claro
            cell.set_edgecolor('black') # Borda da célula
            cell.set_height(0.04) # Altura da célula

        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.8) # Escala as células para dar mais espaço vertical

        # Salva o arquivo
        # Removido bbox_inches='tight'
        fig.savefig(filename, dpi=200, facecolor='white')
        plt.close(fig)
        print(f"  Sucesso: Tabela salva em '{filename}'")

    except Exception as e:
        print(f"\n*** ERRO AO GERAR TABELA PNG PARA {filename} ***")
        print(f"  Erro: {e}")

# --- Preparando os dados para as tabelas ---
# Usando r'' para o LaTeX no cabeçalho da coluna
col_headers = ["Nome", "Símbolo", "Z", r"Coeficiente (cm$^{2}$/g)"]
table_title_base = "Coeficientes de Atenuação de Massa (NIST) para $E \\approx 17.2$ keV"

# Coleta todos os dados
all_data = []
for z in range(1, 93):
    nome, simbolo = element_map.get(z, ("???", "??"))
    coef = teorico_nist_data.get(z, 0.0)
    all_data.append([nome, simbolo, z, f"{coef:.3f}"])

# Divide em 3 partes
# Parte 1: Z=1 a 31 (31 linhas)
data_part1 = all_data[0:31]
# Parte 2: Z=32 a 62 (31 linhas)
data_part2 = all_data[31:62]
# Parte 3: Z=63 a 92 (30 linhas)
data_part3 = all_data[62:]

# Gera as 3 imagens PNG
save_table_as_png_plt(data_part1, col_headers, "tabela_nist_parte1.png", title_text=f"{table_title_base} (Parte 1 de 3)")
save_table_as_png_plt(data_part2, col_headers, "tabela_nist_parte2.png", title_text=f"{table_title_base} (Parte 2 de 3)")
save_table_as_png_plt(data_part3, col_headers, "tabela_nist_parte3.png", title_text=f"{table_title_base} (Parte 3 de 3)")

print("Geração de imagens da tabela concluída.")

# --- 9. CÁLCULO DA RAZÃO DOS COEFICIENTES ANGULARES (Borda K) ---

print("\n" + "="*60)
print("     CÁLCULO DA RAZÃO DOS COEFICIENTES ANGULARES (Z^3)")
print("="*60 + "\n")

# 1. Preparar os dados a partir do dicionário NIST
x_pre_borda, y_pre_borda = [], []  # Grupo 1 (Z <= 39)
x_pos_borda, y_pos_borda = [], []  # Grupo 2 (Z >= 40 e Z <= 84)

# Itera sobre os dados do NIST de Z=1 até Z=92
for z in range(1, 93):
    mu_rho = teorico_nist_data.get(z) # Usar .get() para evitar erro se Z não existir
    if mu_rho is not None:
        z_cubed = z**3

        if z <= 39: # "até o Ítrio"
            x_pre_borda.append(z_cubed)
            y_pre_borda.append(mu_rho)
        elif 40 <= z <= 84: # "a partir do Zircônio"
            # Paramos em Z=84 (Polônio) para evitar a queda da borda L,
            # que é visível no seu gráfico (linha vermelha) ~6.2e5.
            x_pos_borda.append(z_cubed)
            y_pos_borda.append(mu_rho)

# 2. Converter para arrays numpy
x1 = np.array(x_pre_borda)
y1 = np.array(y_pre_borda)
x2 = np.array(x_pos_borda)
y2 = np.array(y_pos_borda)

# 3. Realizar a Regressão Linear (np.polyfit)
# y = a*x + b. 'coefs[0]' é o coeficiente angular 'a'
try:
    coefs1 = np.polyfit(x1, y1, 1)
    coefs2 = np.polyfit(x2, y2, 1)

    a1 = coefs1[0] # Coeficiente angular do Grupo 1 (pré-borda)
    a2 = coefs2[0] # Coeficiente angular do Grupo 2 (pós-borda)

    # 4. Calcular a razão
    razao = a1 / a2

    print(f"Análise baseada nos dados 'Teórico (NIST)' @ ~17.2 keV:\n")
    print(f"  --- Grupo 1 (Z=1-39, 'pré-borda K') ---")
    print(f"  Coeficiente Angular (a1): {a1: .6e}")
    print(f"  Equação da Reta: y = {a1:.4e} * x + {coefs1[1]:.4f}\n")

    print(f"  --- Grupo 2 (Z=40-84, 'pós-borda K') ---")
    print(f"  Coeficiente Angular (a2): {a2: .6e}")
    print(f"  Equação da Reta: y = {a2:.4e} * x + {coefs2[1]:.4f}\n")

    print(f"  --- Razão dos Coeficientes ---")
    print(f"  Razão (a1 / a2): {razao:.4f}")
    print("\n" + "="*60)

except np.linalg.LinAlgError as e:
    print(f"Erro ao calcular a regressão linear: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

# --- FIM DO NOVO BLOCO ---
