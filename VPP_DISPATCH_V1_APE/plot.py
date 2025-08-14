import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch

# Estilo visual
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8

def plot(data: dict) -> None:
    FIG_WIDTH = 3.7   # polegadas
    FIG_HEIGHT = 2.5  # polegadas

    Nbm = data['Nbm']
    p_bm = data['p_bm'][:, :24]
    u_bm = data['u_bm'][:, :24]
    t = np.arange(24)

    labels = [f'UBTM{i+1}' for i in range(Nbm)]
    colors = ['royalblue', 'salmon', 'mediumseagreen']

    # Gráfico de potência das UBTMs
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.stackplot(t, *p_bm, labels=labels, colors=colors)
    plt.title('Potência das Usinas de Biomassa')
    plt.xlabel('Hora')
    plt.ylabel('Potência (MW)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig('grafico_biomassa.png', dpi = 410)
    plt.show()

    # # Gráfico dos estados ON/OFF das UBTMs (heatmap)
    # fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))  # ajustado
    # im = ax.imshow(u_bm, aspect='auto', cmap='Greens', interpolation='none', vmin=0, vmax=1)

    # ax.set_title('Estado das Usinas de Biomassa (ON/OFF)')
    # ax.set_xlabel('Hora')
    # ax.set_ylabel('Usinas')
    # ax.set_yticks(np.arange(Nbm))
    # ax.set_yticklabels(labels)
    # ax.set_xticks(np.arange(0, 24, 2))
    # ax.grid(False)

    # # Legenda manual
    # legend_elements = [
    #     Patch(facecolor='lightgreen', edgecolor='black', label='On'),
    #     Patch(facecolor='white', edgecolor='black', label='Off')
    # ]
    # ax.legend(handles=legend_elements, loc='upper right', fontsize=6, frameon=True)

    # plt.tight_layout()
    # plt.show()

    # Plotagem do Carregamento dos Armazenadores
    p_chg = data['p_chg']
    p_dch = data['p_dch']

    p_bat_max = data['p_bat_max']
    plt.figure(figsize = (12, 6), dpi = 100)
    plt.step(t, p_chg[0, :], where = 'mid', linewidth = 1.3, color = 'r', label = 'SAs 1')
    plt.step(t, p_chg[1, :], where = 'mid', linewidth = 1.3, color = 'b', label = 'SAs 2')
    plt.plot(t, p_bat_max[0] * np.ones(24), '--k', linewidth = 2, label= 'max')
    plt.title('Carregamento dos SAs 1 e 2 período de um dia')
    # plt.grid(True, linestyle = '--', alpha = 0.3)
    plt.xlabel('Hora')
    plt.ylabel('Potência em (MW)')
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plotagem do Descarregamento dos Armazenadores
    plt.figure(figsize = (12, 6), dpi=100)
    plt.step(t, p_dch[0, :], where = 'mid', linewidth = 1.3, color = 'r', label = 'SAs 1')
    plt.step(t, p_dch[1, :], where = 'mid', linewidth = 1.3, color = 'b', label = 'SAs 2')
    plt.plot(t, p_bat_max[0] * np.ones(24), '--k', linewidth = 2, label= 'max')
    plt.title('Descarregamento dos SAs 1 e 2 no período de um dia')
    # plt.grid(True, linestyle = '--', alpha = 0.3)
    plt.xlabel('Hora')
    plt.ylabel('Potência em (MW)')
    plt.tight_layout()
    plt.legend()
    plt.show()

    # FVs e EOs
    p_pv = data['p_pv'][:, :24]
    p_wt = data['p_wt'][:, :24]

    # Concatenar as EOs abaixo das FVs
    potencias = np.vstack((p_wt, p_pv))  # EOs primeiro, depois FVs

    # Labels na mesma ordem
    labels = ['EO 1', 'EO 2', 'FV 1', 'FV 2', 'FV 3', 'FV 4']
    # colors = ['lightgray', 'darkgray', 'gold', 'orange', 'darkorange', 'sandybrown']
    # colors = ['dodgerblue', 'mediumseagreen', 'gold', 'orange', 'darkorange', 'sandybrown']
    colors = ['royalblue', 'seagreen', 'gold', 'darkorange', 'orangered', 'chocolate']

    # Plotagem
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.stackplot(t, *potencias, labels=labels, colors=colors)
    plt.title('Potência das Usinas Eólicas e Solares', fontsize=8)
    plt.xlabel('Hora', fontsize=8)
    plt.ylabel('Potência (MW)', fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.show()


    # # Parâmetros das Cargas controláveis
    # p_dl = data['p_dl'][:, :24]
    # p_dl_ref = data['p_dl_ref'][:, :24]
    # p_dl_max = data['p_dl_max'][:, :24]
    # p_dl_min = data['p_dl_min'][:, :24]

    # # for i in range(Ndl):

    # #     title = f'Carga Despachável {i+1} no período de um dia'
        
    # #     plt.figure(figsize = (12, 6))
    # #     plt.plot(t, p_dl[i, :], 'r', label = 'desp')
    # #     plt.plot(t, p_dl_ref[i, :], 'k', label = 'ref')
    # #     plt.plot(t, p_dl_max[i, :], '--b', label = 'max')
    # #     plt.plot(t, p_dl_mabel='min')
    # ax.set_ylabel(f'CD{i+1} (MW)', fontsize=8)
    # ax.grid(True, linestyle='--', alpha=0.3)
    # ax.tick_params(labelsize=8)

    # axs[-1].set_xlabel('Hora', fontsize=8)  # Só no último eixo
    # fig.tight_layout(rect=[0, 0, 1, 0.97])  # Ajusta layout para não cortar o título
    # axs[0].legend(loc='upper right', fontsize=8)  # legenda só na primeira subplot

    # plt.show()

    # # Plotagem das cargas não despacháveis
    




    # # for i in range(Ndl):
    # #     ax = axs[i]
    # #     ax.plot(t, p_dl[i, :], 'r', label='desp')
    # #     ax.plot(t, p_dl_ref[i, :], 'k', label='ref')
    # #     ax.plot(t, p_dl_max[i, :], '--b', label='max')
    # #     ax.plot(t, p_dl_min[i, :], '--b', label='min')
    # #     ax.set_ylabel(f'CD{i+1} (MW)', fontsize=8)
    # #     ax.grid(True, linestyle='--', alpha=0.3)
    # #     ax.tick_params(labelsize=8)

    # # axs[-1].set_xlabel('Hora', fontsize=8)
    # # axs[0].legend(fontsize=8, loc='upper right')

    # # fig.tight_layout(rect=[0, 0, 1, 0.95])  # espaço para o título
    # # plt.show()
    # fig, axs = plt.subplots(Ndl, 1, figsize=(FIG_WIDTH, FIG_HEIGHT * Ndl), sharex=True)
    # fig.suptitle('Cargas Despacháveis no período de um dia', fontsize=8, y = 0.93)

    # for i in range(Ndl):
    #     ax = axs[i] if Ndl > 1 else axs  # Para o caso de Ndl = 1
    #     ax.plot(t, p_dl[i, :], 'r', label='desp')
    #     ax.plot(t, p_dl_ref[i, :], 'k', label='ref')
    #     ax.plot(t, p_dl_max[i, :], '--b', label='max')
    #     ax.plot(t, p_dl_min[i, :], '--b', l
    # u_dch = data['u_dch'][:, :24]
    # u_chg = data['u_chg'][:, :24]
    # soc = data['soc'][:, :24]
    # soc_min = data['soc_min']
    # soc_max = data['soc_max']
    # p_bat_max = data['p_bat_max']


    

    # # labels = ['SoC 1', 'SoC 2']

    # fig, axs = plt.subplots(2, 1, figsize=(FIG_WIDTH, 4.5), sharex=True)
    # fig.suptitle('Carregamento e Descarregamento dos Armazenadores (por SAEB)', fontsize=8, y = 0.92)

    # for i in range(2):  # Para SA1 e SA2
    #     axs[i].step(t, p_chg[i, :], where='mid', linewidth=1.3, color='royalblue', label='Carregamento')
    #     axs[i].step(t, p_dch[i, :], where='mid', linewidth=1.3, color='darkorange', label='Descarregamento')
    #     axs[i].plot(t, p_bat_max[i] * np.ones(24), '--k', linewidth=1.3, label='Potência Máx.')
    #     axs[i].set_ylabel(f'SAEB {i+1} (MW)', fontsize=8)
    #     axs[i].grid(True, linestyle='--', alpha=0.3)
    #     axs[i].tick_params(labelsize=8)
    #     # axs[0].legend(loc='upper right', fontsize=8)

    # axs[-1].set_xlabel('Hora', fontsize=8)  # Só no último eixo
    # fig.tight_layout(rect=[0, 0, 1, 0.97])  # Ajusta layout para não cortar o título
    # axs[0].legend(loc='upper right', fontsize=8)  # legenda só na primeira subplot

    # fig.tight_layout(rect=[0, 0, 1, 0.95])  # espaço para o título geral
    # plt.show()

    # FIG_WIDTH = 3.38
    # FIG_HEIGHT = 2.5    

    # # Plotagem dos níveis de energia dos SAs
    # # plt.figure(figsize = (FIG_WIDTH, FIG_HEIGHT))
    # # plt.plot(t, np.zeros(24) * soc_max[0], '--k', label = 'max')
    # # plt.plot(t, np.zeros(24) * soc_min[0], '--k', label = 'min')
    # # plt.stackplot(t, soc[0, :], soc[1, :], labels = labels)
    # # plt.title('SoC Baterias')
    # # plt.xlabel('Horas')
    # # plt.ylabel('Carga em (MW)')
    # # plt.grid(True, linestyle = '--', alpha = 0.3)
    # # plt.tight_layout()
    # # plt.legend()
    # # plt.show()
    # # --- Plotagem dos níveis de energia dos SAs (SoC) com tamanho ajustado ---
    # labels = ['SA 1', 'SA 2']
    # SoC_max_1 = np.full(24, soc_max[0])
    # SoC_max_2 = np.full(24, soc_max[1]) + SoC_max_1

    # plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

    # # plt.plot(t, soc_max[0] * np.ones(24), '--k', linewidth=1.3, label='max')
    # # plt.plot(t, soc_min[0] * np.ones(24), '--k', linewidth=1.3, label='min')
    # plt.stackplot(t, soc[0, :], soc[1, :], labels=labels, colors=['lightblue', 'lightgreen'])
    # plt.plot(t, SoC_max_1, '--k', label='Máx 1')
    # plt.plot(t, SoC_max_2, '--k', label='Máx 2')

    # plt.title('Estado de Carga (SoC) das Baterias', fontsize=8)
    # plt.xlabel('Hora', fontsize=8)
    # plt.ylabel('Carga (MW)', fontsize=8)
    # plt.xticks(fontsize=8)
    # plt.yticks(fontsize=8)
    # plt.grid(True, linestyle='--', alpha=0.3)
    # plt.legend(loc='upper right', fontsize=8)
    # plt.tight_layout()
    # plt.show()


    # # Parâmetros das FVs
    # p_pv = data['p_pv'][:, :24]

    # labels = ['FV 1', 'FV 2', 'FV 3', 'FV 4']

    # plt.figure(figsize = (12, 6))
    # plt.stackplot(t, p_pv[0, :], p_pv[1, :], p_pv[2, :], p_pv[3, :], labels = labels)
    # plt.title('Usinas Solares FVs 1, 2, 3 e 4 no período de um dia')
    # plt.xlabel('Hora')
    # plt.ylabel('Potência em (MW)')
    # plt.grid(True, linestyle = '--', alpha = 0.3)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    # # Parâmetros das EOs
    # p_wt = data['p_wt'][:, :24]

    # labels = ['EO 1', 'EO 2']

    # plt.figure(figsize = (12, 6))
    # plt.stackplot(t, p_wt[0, :], p_wt[1, :], labels = labels)
    # plt.title('Usinas Eólicas 1 e 2 no período de um dia')
    # plt.xlabel('Hora')
    # plt.ylabel('Potência em (MW)')
    # plt.grid(True, linestyle = '--', alpha = 0.3)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    # Parâmetros das FVs e EOs
    

    # # Parâmetros das cargas não controláveis
    # p_l = data['p_l'][:, :24]
    # u_dl = data['u_dl'][:, :24]

    # # Cálculo da potência líquida
    # p_liq = np.zeros(24)
    # for t in range(24):
    #     for i in range(Npv):
    #         p_liq[t] += p_pv[i, t] 
    #     for i in range(Nwt):
    #         p_liq[t] += p_wt[i, t] 
    #     for i in range(Nbm):
    #         p_liq[t] += p_bm[i, t] * u_bm[i, t] 
    #     for i in range(Nl):
    #         p_liq[t] -= p_l[i, t] 
    #     for i in range(Ndl):
    #         p_liq[t] -= p_dl[i, t] * u_dl[i, t] 
    #     # for i in range(Nbat):
    #     #     p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t] 
    #     for i in range(Nbat):
    #         p_liq[t] += p_dch[i, t] * u_dch[i, t] - p_chg[i, t] * u_chg[i, t]

    # t = np.arange(24)
    # plt.figure(figsize=(FIG_WIDTH, 2))
    # plt.plot(t, p_liq, 'r', label='Potência Líquida')
    # plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)

    # plt.title('Potência Líquida', fontsize=8, fontname='Times New Roman')
    # plt.xlabel('Hora', fontsize=8, fontname='Times New Roman')
    # plt.ylabel('Potência (MW)', fontsize=8, fontname='Times New Roman')
    # plt.xticks(fontsize=8, fontname='Times New Roman')
    # plt.yticks(fontsize=8, fontname='Times New Roman')
    # plt.grid(True, linestyle='--', alpha=0.3)
    # plt.legend(loc='upper left', fontsize=8)
    # plt.tight_layout()
    # plt.show()


    # p_exp = np.maximum(0, p_liq)
    # p_imp = np.maximum(0, - p_liq)

    # # # Plotagem Exportação versus Importação
    # # plt.figure(figsize = (10,5))
    # # plt.plot(p_exp, 'b')
    # # plt.plot(p_imp, 'r')
    # # plt.title('Exportação x Importação no período de um dia')
    # # plt.xlabel('Hora')
    # # plt.ylabel('Potência em MW')
    # # plt.legend(['Exportação', 'Importação'])
    # # plt.show()
    # plt.figure(figsize=(FIG_WIDTH, 2))  # altura menor para encaixar na coluna

    # plt.plot(p_exp, color='blue', label='Exportação', linewidth=1.5)
    # plt.plot(p_imp, color='red', label='Importação', linewidth=1.5)

    # plt.title('Exportação x Importação no período de um dia', fontsize=8, fontname='Times New Roman')
    # plt.xlabel('Hora', fontsize=8, fontname='Times New Roman')
    # plt.ylabel('Potência (MW)', fontsize=8, fontname='Times New Roman')

    # plt.xticks(fontsize=8, fontname='Times New Roman')
    # plt.yticks(fontsize=8, fontname='Times New Roman')

    # plt.legend(loc='upper right', fontsize=8)
    # plt.grid(True, linestyle='--', alpha=0.3)
    # plt.tight_layout()
    # plt.show()

