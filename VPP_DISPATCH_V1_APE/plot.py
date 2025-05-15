import numpy as np
from matplotlib import pyplot as plt

'''
    Este script tem a finalidade de mostrar graficamente as projeções e os despachos otimizados de uma VPP.

        - Parâmetros de entrada:
            - (data: dict): dicionário contendo os parâmetros iniciais, as projeções temporais iniciais e os desapchos da solução ótima encotrada pelo otimizador (GA).
                - Nt: Período da simulação da VPP;
                - Nl: Quantidade de carga NÃO despachável da VPP;
                - Ndl: Quantidade de carga despachável da VPP;
                - Nbm: Quantidade de usinas de geração à biomassa (UBTMs) da VPP;
                - Nwt: Quantidade de usinas eólicas (EOs) da VPP;
                - Npv: Quantidade de usinas solares (FVs) da VPP;
                - Nbat: Quantidade de armazenadores (SAs) da VPP;

        - Retorna (None): Não há retorno nessa função.
'''

def plot(data: dict)-> None:

    # Potência aparente de base (1MVA)
    S_base = 1E6

    # Parâmetros iniciais da VPP
    Nt = data['Nt']
    Nl = data['Nl']
    Nbm = data['Nbm']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Ndl = data['Ndl']
    Nbat = data['Nbat']

    # Parâmetros das UBTMs
    p_bm = data['p_bm']
    p_bm_max = data['p_bm_max']
    p_bm_min = data['p_bm_min']
    u_bm = data['u_bm']

    # Parâmetros dos SAs
    p_dch = data['p_dch']
    p_chg = data['p_chg']
    u_dch = data['u_dch']
    u_chg = data['u_chg']
    soc = data['soc']
    soc_min = data['soc_min']
    soc_max = data['soc_max']
    p_bat_max = data['p_bat_max']

    # Cargas despachaveis        
    p_dl = data['p_dl']
    p_dl_ref = data['p_dl_ref']
    p_dl_min = data['p_dl_min']
    p_dl_max = data['p_dl_max']
    u_dl = data['u_dl']

    # Cargas não despacháveis
    p_l = data['p_l']

    # Projeções das FVs
    p_pv = data['p_pv']

    # Projeções das EOs
    p_wt = data['p_wt']

    # Vetor temporal do período da simulação
    t = np.arange(Nt)

    # Plotagem das UBMTs
    for i in range(Nbm):
        
        # title = f'Usina de Biomassa {i + 1}' 
        # plt.figure(figsize = (10, 5))
        # plt.step(t, p_bm[i, :], 'b')
        # plt.step(t, np.ones(Nt) * p_bm_max[i], '--r')
        # plt.step(t, np.ones(Nt) * p_bm_min[i] * u_bm[i, :], '--r')
        # plt.title(title)
        # plt.xlabel('Hora')
        # plt.ylabel('Potência em MW')
        # plt.legend(['p_bm', 'max', 'min'])
        # plt.show()

        # title = f'Estado da usina de Biomassa {i + 1}' 
        # plt.figure(figsize = (10, 5))
        # plt.bar(t, u_bm[i, :], color=['gray' if v == 0 else 'green' for v in u_bm[i, :]], width=1, edgecolor='black', align = 'edge')
        # plt.title(title)
        # plt.xlabel('Hora')
        # plt.yticks([0, 1], ['Off', 'On'])
        # plt.show()
        
        # Criação de uma figura com dois subgráficos (1 coluna, 2 linhas)
        fig, axs = plt.subplots(2, 1, figsize = (18, 8), sharex = True)

        # Gráfico de potência
        axs[0].step(t, p_bm[i, :], 'b', where = 'post', label = 'p_bm') 
        axs[0].step(t, np.ones(Nt) * p_bm_max[i], '--r', where = 'post', label = 'max')
        axs[0].step(t, p_bm_min[i] * u_bm[i, :], '--r', where = 'post', label = 'min')
        axs[0].set_ylabel('Potência MW')
        axs[0].set_title(f'Usina de Biomassa {i + 1}')
        axs[0].legend(loc = 'upper right', bbox_to_anchor = (1.1, 1))  

        # Gráfico de estado
        axs[1].bar(t, u_bm[i, :], color = ['gray' if v == 0 else 'green' for v in u_bm[i, :]],
                   width = 1, edgecolor = 'black', align = 'edge')
        axs[1].set_yticks([0, 1])
        axs[1].set_yticklabels(['Off', 'On'])
        axs[1].set_ylabel('Estado')
        axs[1].set_xlabel('Hora')

        # Ajuste do layout para evitar sobreposição
        plt.tight_layout()

        # Exibe os gráficos
        plt.show()

    # Potagem dos SAs
    for i in range(Nbat):

        title_name = f'Carga Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_chg[i, :] * u_chg[i, :], 'r')
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência em MW')
        plt.legend(['max', 'load'])
        plt.show()

        title_name = f'Descarga Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_bat_max[i] * np.ones(Nt), 'b--')
        plt.step(t, p_dch[i,:] * u_dch[i,:], 'r')
        plt.title(title_name)
        plt.xlabel('Hora')
        plt.ylabel('Potência em MW')
        plt.legend(['max', 'discharge'])
        plt.show()

        title_name = f'Soc Bateria {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, soc_min[i] * np.ones(Nt), 'b--')
        plt.plot(t, soc_max[i] * np.ones(Nt), 'b--')
        plt.step(t, soc[i,:], 'r')
        plt.title(title_name)        
        plt.xlabel('Hora')
        plt.ylabel('Carga em MW')
        plt.legend(['min', 'max', 'soc'])
        plt.show()

    # plotagem das cargas despacháveis
    for i in range(Ndl):

        title_name = f'Cargas despachaveis {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_dl_ref[i,:], 'r')
        plt.plot(t, p_dl_min[i,:], 'b--')
        plt.plot(t, p_dl_max[i,:], 'b--')
        plt.plot(t, p_dl[i,:], 'k')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.legend(['ref', 'min', 'max', 'desp'])
        plt.show()

    # Plotagem das FVs
    for i in range(Npv):

        title_name = f'Usina Solar FV {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_pv[i], 'r')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Plotagem das EOs
    for i in range(Nwt):

        title_name = f'Usina Eólica {i + 1}'
        plt.figure(figsize = (10, 4))
        plt.plot(t, p_wt[i], 'r')
        plt.title(title_name)
        plt.xlabel('hora')
        plt.ylabel('Potência em MW')
        plt.show()

    # Cálculo da potência líquida
    p_liq = np.zeros(Nt)
    for t in range(Nt):
        for i in range(Npv):
            p_liq[t] += p_pv[i, t] 
        for i in range(Nwt):
            p_liq[t] += p_wt[i, t] 
        for i in range(Nbm):
            p_liq[t] += p_bm[i, t] * u_bm[i, t] 
        for i in range(Nl):
            p_liq[t] -= p_l[i, t] 
        for i in range(Ndl):
            p_liq[t] -= p_dl[i, t] * u_dl[i, t] 
        # for i in range(Nbat):
        #     p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t] 
        for i in range(Nbat):
            p_liq[t] += p_dch[i, t] * u_dch[i, t] - p_chg[i, t] * u_chg[i, t]


    p_exp = np.maximum(0, p_liq)
    p_imp = np.maximum(0, - p_liq)

    # Plotagem Exportação versus Importação
    plt.figure(figsize = (10,5))
    plt.plot(p_exp, 'b')
    plt.plot(p_imp, 'r')
    plt.title('Exportação x Importação')
    plt.xlabel('Hora')
    plt.ylabel('Potência em MW')
    plt.legend(['Exportação', 'Importação'])
    plt.show()
