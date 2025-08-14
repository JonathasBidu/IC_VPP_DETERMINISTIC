import numpy as np

def calculate(data: dict):

    Nt = 720
    
    Nl = data['Nl']
    Nbm = data['Nbm']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Ndl = data['Ndl']
    Nbat = data['Nbat']

    p_bm = data['p_bm']
    u_bm = data['u_bm']
    p_dch = data['p_dch']
    p_chg = data['p_chg']
    u_dch = data['u_dch']
    u_chg = data['u_chg']
    p_dl = data['p_dl']
    u_dl = data['u_dl']
    p_l = data['p_l']
    p_pv = data['p_pv']
    p_wt = data['p_wt']

    # Cálculo da potência líquida hora a hora
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
        for i in range(Nbat):
            p_liq[t] += p_dch[i, t] * u_dch[i, t] - p_chg[i, t] * u_chg[i, t]

    # Exportação e Importação
    p_exp = np.maximum(0, p_liq) # excedente
    p_imp = np.maximum(0, -p_liq) # déficit

    energia_exportada = np.sum(p_exp)
    energia_importada = np.sum(p_imp)

    print("=== RESUMO DE ENERGIA (Período Total da Simulação) ===")
    print(f"Energia Exportada:       {energia_exportada:.2f} MWh")
    print(f"Energia Importada:       {energia_importada:.2f} MWh")
