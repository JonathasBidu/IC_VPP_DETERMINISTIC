import matplotlib.pyplot as plt
import numpy as np

def plot(data):

    # Simulação de dados de 3 usinas por 24h
    t = np.arange(24)
    p_bm = data['p_bm']
    p_bm = p_bm[:, :24]
    # p_bm_max = [6, 6, 6]

    labels = ['UBTM1', 'UBTM2', 'UBTM3']
    cores = ['royalblue', 'salmon', 'mediumseagreen']

    plt.figure(figsize=(12, 6))
    plt.stackplot(t, *p_bm, labels=labels, colors=cores)
    # plt.hlines(p_bm_max[0], t[0], t[-1], linestyles='--', colors='darkred', label='p_bm_max')
    plt.xlabel('Hora')
    plt.ylabel('Potência (MW)')
    plt.title('Potência das Usinas de Biomassa - Gráfico de Áreas Empilhadas')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
