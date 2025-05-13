from decompose_vetor import decompose
import numpy as np

"""
    Descrição da Função:
    Esta função contém o cálculo da função objetivo do modelo da VPP, para uso em um ga(genetic algorithm | algoritmo genético).

    Parâmetros:
    - x: vetor de variáveis
    - vpp_data: estrutura de dicionário contendo os parâmetros da VPP. Possui os seguintes atributos:
        - Nt: número de instantes de simulação
        - Nbm: número de usinas biomassa
        - Ndl: número de cargas despacháveis
        - Nbat: número de baterias
        - Nwt: número de geradores eólicos
        - Npv: número de usinas solares
        - p_l: potência das cargas, dimensão ((Nl*Nt), 1)
        - p_pv: potência das UG solares FV, dimensão ((Npv*Nt), 1)
        - p_wt: potência das UG eólicas, dimensão ((Nwt*Nt), 1)
        - p_bm_min: potência mínima biomassa, dimensão (Nbm, 1)
        - p_bm_max: potência máxima biomassa, dimensão (Nbm, 1)
        - p_bm_rup: potência máxima ramp up biomassa, dimensão (Nbm, 1)
        - p_bm_rdown: potência máxima ramp down biomassa, dimensão (Nbm, 1)
        - eta_chg: rendimento carga bateria, dimensão (Nbat, 1)
        - eta_dch: rendimento descarga bateria, dimensão (Nbat, 1)
        - soc_min: SoC mínimo bateria, dimensão (Nbat, 1)
        - soc_max: SoC máximo bateria, dimensão (Nbat, 1)
        - p_bat_max: potência máxima carga/descarga bateria, dimensão (Nbat, 1)
        - p_dl_min: potência mínima despachável carga, dimensão (Ndl, 1)
        - p_dl_max: potência máxima despachável carga, dimensão (Ndl, 1)
        - tau_dl: compensação por corte, dimensão (Ndl, 1)
        - tau_pld: PLD, dimensão (Nt, 1)
        - tau_dist: tarifa distribuidora
        - kappa_pv: custo unitário ger. solar
        - kappa_wt: custo unitário ger. eólica
        - kappa_bm: custo unitário ger. biomassa
        - kappa_bm_start: custo unitário partida ger. biomassa
        - kappa_bat: custo baterias

    Retorna:
        - fval: O lucro obtido na operação da VPP(Virtual Power Plant)
"""

def obj_function(x, vpp_data) -> np.float64:

    # Definindo a potência aparente base (1MVA)
    S_base = 1E6

    # Dados e projeções iniciais da VPP
    Nt = vpp_data['Nt']
    Nbm = vpp_data['Nbm']
    Ndl = vpp_data['Ndl']
    Nl = vpp_data['Nl']
    Nbat = vpp_data['Nbat']
    Npv = vpp_data['Npv']
    Nwt = vpp_data['Nwt']
    p_pv = vpp_data['p_pv']
    p_wt = vpp_data['p_wt']
    p_l = vpp_data['p_l']
    tau_pld = vpp_data['tau_pld']
    tau_dist = vpp_data['tau_dist']
    tau_dl = vpp_data['tau_dl']
    kappa_pv = vpp_data['kappa_pv']
    kappa_wt = vpp_data['kappa_wt']
    kappa_bm = vpp_data['kappa_bm']
    kappa_bat = vpp_data['kappa_bat']
    kappa_bm_start = vpp_data['kappa_bm_start']

    # Decompondo o vetor x em suas variáveis 
    p_bm, p_chg, p_dch, soc, p_dl, u_bm, u_chg, u_dch, u_dl = decompose(x, vpp_data)
        
    # Calculando a Potência líquida
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
            p_liq[t] -= p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]
    
    # Obtendo a potência exportada e a potência importada
    p_exp = np.maximum(0, p_liq) 
    p_imp = np.maximum(0, -p_liq)

    # Normalizando as tarifas da distribuidora, PLD e de compensação para p.u./h
    tau_pld_pu = tau_pld / S_base
    tau_dist_pu = tau_dist / S_base
    tau_dl_pu = tau_dl / S_base


    # Receita com excedente de energia
    R = 0
    for t in range(Nt):
        R += p_exp[t] * tau_pld_pu[t]

    # Despesa com importação de energia com a comportação de energia
    D = 0
    
    # Importação de energia da distribuidora
    for t in range(Nt):
        D += p_imp[t] * tau_dist_pu[t] 

    # Custos de geração solar fotovoltaica
    Cpv = 0
    for t in range(Nt):
        for i in range(Npv):
            Cpv += p_pv[i, t] * kappa_pv[i]

    # Custos de geração Eólica
    Cwt = 0
    for t in range(Nt):
        for i in range(Nwt):
            Cwt += p_wt[i, t] * kappa_wt[i]

    # Custos de geração biomassa (custo linear)
    Cbm = 0
    for t in range(Nt):
        for i in range(Nbm):
            Cbm += p_bm[i, t] * u_bm[i, t] * kappa_bm[i]

    #  custo de partida
    # for t in range(1, Nt):
    #     for i in range(Nbm):
    #         Cbm += (u_bm[i, t] - u_bm[i, t - 1]) * kappa_bm_start[i]

    # Custo de partida da biomassa (ligando de 0 → 1)
    for t in range(1, Nt):  # começa de 1 para ter t-1
        for i in range(Nbm):
            if u_bm[i, t] > u_bm[i, t - 1]:
                Cbm += kappa_bm_start[i]


    # Custo de controle carga despachada
    Cdl = 0
    for t in range(Nt):
        for i in range(Ndl):
            Cdl += p_dl[i, t] * u_dl[i, t] * tau_dl_pu[t]

    # Custo da bateria
    Cbat = 0
    for t in range(Nt):
        for i in range(Nbat):
            Cbat += (p_chg[i, t] * u_chg[i, t] + p_dch[i, t] * u_dch[i, t]) * kappa_bat[i]

    # Despesa total
    D = D + Cpv + Cwt + Cbm + Cdl + Cbat
    fval = R - D
    
    return fval

# Test de uso
if __name__ == '__main__':

    from vpp_initial_data import vpp_data
    from decompose_vetor import decompose
    from generator_scenarios import import_scenarios_from_pickle
    from pathlib import Path

    data = vpp_data()

    # Parâmetros iniciais de VPP
    data['Nt'] = 24
    Nt = data['Nt'] # Período de simulação da VPP
    Nbm = data['Nbm'] # Quantidade de usinas de biomassa da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # Variáveis reais: p_bm, p_chg, p_dch, soc, p_dl
    Nr = (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras: u_bm, u_chg, u_dch, u_dl
    Ni = (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)
    
    # Gerando um população inicial para teste
    x = np.random.rand(Nr + Ni)

    # Obtendo as projeções temporais iniciais a partir de um cenário gerado anteriormente
    path = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
    cenarios = import_scenarios_from_pickle(path)

    # Acrescentando as projeções ao dicionário data
    for cenario in cenarios:

        data['p_pv'] = cenario['p_pv']
        data['p_wt'] = cenario['p_wt']
        data['p_l'] = cenario['p_l']
        data['tau_pld'] = cenario['tau_pld']
        data['tau_dist'] = cenario['tau_dist']
        data['tau_dl'] = cenario['tau_dl']

    fval = obj_function(x, data)

    print(f' O valor da função objetivo é {fval:.2f}\n')