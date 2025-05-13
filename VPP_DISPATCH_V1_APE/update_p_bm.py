import numpy as np

'''
    Atualiza os limites máximo, mínimo e médio da potência de uma usina de biomassa
    com base na curva de duração das cargas e da geração renovável.

    Argumentos:
    - Nt: número de instantes de tempo (ex: 24 horas)
    - p_l: matriz de perfis de carga não despachável [Nl x Nt]
    - p_dl_ref: matriz de perfis de carga despachável de referência [Ndl x Nt]
    - p_pv: matriz de geração solar fotovoltaica [Npv x Nt]
    - p_wt: matriz de geração eólica [Nwt x Nt]

    Retorna:
    - c_bm_max: capacidade máxima da usina de biomassa
    - c_bm_min: capacidade mínima da usina de biomassa
    - c_bm_med: capacidade média da usina de biomassa
'''

def update(Nt, p_l, p_dl_ref, p_pv, p_wt):

    import matplotlib.pyplot as plt

    # Empilhando cargas: não-despacháveis + despacháveis
    x_1 = np.concatenate((p_l, p_dl_ref), axis=0)  # [Nl+Ndl x Nt]
    x_2 = np.concatenate((p_pv, p_wt), axis=0)     # [Npv+Nwt x Nt]

    # Somando a carga e geração em cada instante de tempo
    x_1 = np.sum(x_1, axis=0)  # [Nt] – soma das cargas
    x_2 = np.sum(x_2, axis=0)  # [Nt] – soma das gerações

    # Inicializando curvas de duração
    d_1 = np.zeros(Nt)  # curva de duração da demanda
    d_2 = np.zeros(Nt)  # curva de duração da geração

    # Calculando as curvas de duração da carga e geração
    for pos, xi in enumerate(x_1):
        d_1[pos] = np.sum(x_1 >= xi)

    for pos, xi in enumerate(x_2):
        d_2[pos] = np.sum(x_2 >= xi)

    # Ordenando as curvas
    idx_1 = np.argsort(d_1)
    d_ord_1 = np.sort(d_1)
    idx_2 = np.argsort(d_2)
    d_ord_2 = np.sort(d_2)

    # Determinando capacidades de operação da usina de biomassa
    c_bm_max = max(x_1)  # potência máxima necessária
    c_bm_min = min(x_1)  # potência mínima necessária
    c_bm_med = (c_bm_max - c_bm_min) / 2 + c_bm_min  # média

    # Gerando o gráfico de curva de duração
    plt.figure(figsize=(10, 5))
    plt.plot(d_ord_1, x_1[idx_1])
    plt.plot(d_ord_2, x_2[idx_2])
    plt.title('Gráfico de duração de cargas')
    plt.xlabel('Duração (tempo com valor ≥ x)')
    plt.ylabel('Potência [pu]')
    plt.legend(['Demanda (Carga total)', 'Geração renovável'])
    plt.tight_layout()
    plt.show()

    return c_bm_max, c_bm_min, c_bm_med
