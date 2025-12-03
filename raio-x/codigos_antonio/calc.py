import numpy as np

def interpolate_log_log(E_target, E1, mu1, E2, mu2):
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

# --- CÁLCULO PARA O RUBÍDIO (Z=37) ---

# 1. Defina a energia alvo
E_alvo = 1.72E-02  # 17.2 keV

# 2. Defina os pontos que cercam o alvo (lidos da sua imagem)
# Ponto 1 = Logo após o K-edge
E1 = 1.70384E-02
mu1 = 1.029E+02 # Valor APÓS o salto K

# Ponto 2 = O próximo ponto da tabela
E2 = 2.00000E-02
mu2 = 6.855E+01



# 3. Calcule
resultado_Rb = interpolate_log_log(E_alvo, E1, mu1, E2, mu2)

print(f"--- Cálculo para Rubídio (Z=37) ---")
print(f"Alvo: {E_alvo*1000:.1f} keV")
print(f"Intervalo de interpolação:")
print(f"  Ponto 1: E={E1} MeV, mu/rho={mu1} cm²/g")
print(f"  Ponto 2: E={E2} MeV, mu/rho={mu2} cm²/g")
print("---------------------------------")
print(f"\nResultado interpolado: {resultado_Rb:.3f} cm²/g")
