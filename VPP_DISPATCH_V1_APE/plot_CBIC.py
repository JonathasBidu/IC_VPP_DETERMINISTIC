import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8

def plot(data: dict) -> None:
    # Ajuste original para formato mais horizontal, só como referência
    FIG_WIDTH = 3.37
    FIG_HEIGHT = 2.5

    # Nt = data['Nt']
    Nl = data['Nl']
    Ndl = data['Ndl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Nbm = data['Nbm']
    Nbat = data['Nbat']

    p_bm = data['p_bm'][:, :24]
    print(p_bm.shape)
    p_bm_max = data['p_bm_max']
    p_bm_min = data['p_bm_min']
    u_bm = data['p_bm']

    p_l = data['p_l'][:, :24]
    p_dch = data['p_dch'][:, :24]
    p_chg = data['p_chg'][:, :24]
    u_dch = data['u_dch'][:, :24]
    u_chg = data['u_chg'][:, :24]
    u_dl = data['u_dl'][:, :24]

    t = np.arange(24)
    labels = ['UBTM1', 'UBTM2', 'UBTM3']
    colors = ['royalblue', 'salmon', 'mediumseagreen']

    # Biomassa
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.stackplot(t, p_bm[0, :], p_bm[1, :], p_bm[2, :], labels=labels, colors=colors)
    plt.title('Potência das Usinas de Biomassa')
    plt.xlabel('Hora')
    plt.ylabel('Potência em (MW)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    # FVs e EOs
    p_wt = data['p_wt'][:, :24]
    p_pv = data['p_pv'][:, :24]

    labels = ['EO 1', 'EO 2', 'FV 1', 'FV 2', 'FV 3', 'FV 4']
    colors = ['royalblue', 'seagreen', 'gold', 'darkorange', 'orangered', 'chocolate']  

    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.stackplot(t, p_wt[0, :], p_wt[1, :], p_pv[0, :], p_pv[1, :], p_pv[2, :], p_pv[3, :], labels=labels, colors=colors)
    plt.title('Potência das Usinas Eólicas e Solares')
    plt.xlabel('Hora')
    plt.ylabel('Potência em (MW)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    # Armazenamento
    soc = data['soc'][:, :24]
    soc_max = data['soc_max']
    labels = ['SAE 1', 'SAE 2']
    colors = ['lightskyblue', 'lightgreen']

    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.stackplot(t, soc[0, :], soc[1, :],labels=labels, colors=colors)
    plt.plot(t, np.ones(24)*soc_max[0], '--k', label = 'max SAE 1')
    plt.plot(t, np.ones(24)*soc_max[0] + np.ones(24)*soc_max[1], '--k', label = 'max SAE 2')
    plt.title('Estado de carga (SoC) das Baterias')
    plt.xlabel('Hora')
    plt.ylabel('Carga em MW')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

    # Cargas Despacháveis
    p_dl_ref = data['p_dl_ref'][:, :24]
    p_dl_max = data['p_dl_max'][:, :24]
    p_dl_min = data['p_dl_min'][:, :24]
    p_dl = data['p_dl'][:, :24]
    
    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.plot(t, p_dl_ref[0, :], 'k', label='ref')
    plt.plot(t, p_dl_max[0, :], '--b',label='max')
    plt.plot(t, p_dl_min[0, :], '--b',label='min')
    plt.plot(t, p_dl[0, :], 'r',label='desp')
    plt.title('Cargas Despacháveis no período de um dia')
    plt.ylabel('CD 1 (MW)')
    plt.grid(True, linestyle ='--', alpha = 0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.plot(t, p_dl_ref[1, :], 'k',label='ref')
    plt.plot(t, p_dl_max[1, :], '--b',label='max')
    plt.plot(t, p_dl_min[1, :], '--b',label='min')
    plt.plot(t, p_dl[1, :], 'r',label='desp')
    plt.xlabel('Hora')
    plt.ylabel('CD 2 (MW)')
    plt.grid(True, linestyle ='--', alpha = 0.3)
    plt.tight_layout()
    plt.show()

    # Potência Líquida
    p_liq = np.zeros(24)

    for t in range(24):
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
        for i in range(Nbat):
            p_liq[t] += p_dch[i, t] * u_dch[i, t] - p_chg[i, t] * u_chg[i, t]

    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT), dpi = 410)
    plt.plot(p_liq, 'r', label = "Potência Líquida")
    plt.axhline(0, color = 'gray', linestyle = '--', alpha = 0.8)
    plt.title('Potência Líquida')
    plt.xlabel('Hora')
    plt.ylabel('Potência (MW)')
    plt.legend(loc = 'upper left')
    plt.tight_layout()
    plt.show()
