import numpy as np
from decompose_vetor import decompose

"""
    Este script tem a finalidade de fornecer uma função de restrições de igualdades de uma VPP a um otimizador (GA), para que o mesmo encontre a solução ótima da função objetivo, sem que haja violação das restrições.

    - Parâmetros de entrada (x: np.ndarray, data: dict):
        - (data: dict): Dicionário contendo os parâmetros iniciais e projeções iniciais.
            - Parâmetros inicias da VPP
                - Nt: Período da simulação da VPP;
                - Nbat: Quantidade de armazenadores presentes na VPP;
                - eta_chg: Rendimento de carregamento dos armazenadores da VPP;
                - eta_dch: Rendimento de descarregamento dos armazenadores da VPP;

            - Projeções iniciais da VPP:
                - p_wt: Potência das usinas EOs, shape (Nwt, Nt);
                - p_pv: Potência das usinas FVs, shape (Npv, Nt);
                - p_l: Potência das cargas NÃO despacháveis, shape (Nl, Nt);

        - (x: np.ndarray): vetor de variáveis de decisão fornecidas pelo otimizador.            
            - Variáveis de decisão:
                - p_exp: Potência de exportação da VPP, shape (Nt,);
                - p_imp: Potência de importação da VPP, shape (Nt,);
                - p_bm: Potência das UBTMs da VPP, shape (Nbm, Nt);
                - p_dl: Potência das cargas despacháveis da VPP, shape (Ndl, Nt);
                - p_chg: Potência de carregamento dos armazenadores da VPP, shape (Nbat, Nt);
                - p_dch: Potência de descarga dos armazenadores da VPP, shape (Nbar, Nt)
                - soc: Estado de carga (SoC - State fo Charge) dos armazenadroes da VPP;

    - Retorna c_eq: -> np.ndarray
        c_eq: Vetor contendo todas as restrições de igualdade da VPP;
            - pwr_blc_constr: Vetor de restrições de igualdades do balanço de potência da VPP;
            - simult_constr: Vetor de restrições de simultaneidade de importação/exportação da VPP;
            - soc_constr: Vetor de restrições de igualdade do estado de carga da bateria;

"""

def eq_constr(x: np.ndarray, data: dict)-> np.ndarray:

    # Parâmetros iniciais da VPP:
    Nt = data['Nt'] # Período da simulação
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP
    eta_chg = data['eta_chg'] # Rendimento do carregamento da bateria
    eta_dch = data['eta_dch'] # Rendimento do descarregamento da bateria

    # Variáveis de decisão:
    p_bm, p_chg, p_dch, soc, p_dl, u_bm, u_chg, u_dch, u_dl = decompose(x, data)
      
    Nsoc = (Nbat * Nt) # Quantidade de restrições de igualdade de estado de carga
    soc_constr = np.zeros(Nsoc) # Vetor de restrições de igualdades do estado de carga (SoC) dos armazenadores
    k = 0
    for t in range(1, Nt): 
        for i in range(Nbat):
            soc_constr[k] = soc[i, t] - soc[i, t - 1] - (p_chg[i, t] * eta_chg[i]) + (p_dch[i, t] / eta_dch[i])
            k += 1

    # Vetor com todas as restrições de igualdade da VPP
    c_eq = soc_constr

    return c_eq

# exemplos de uso
if __name__ == '__main__':

    from vpp_initial_data import vpp_data
    from decompose_vetor import decompose
    from generator_scenarios import import_scenarios_from_pickle
    from pathlib import Path

    data = vpp_data()

    data['Nt'] = 24
    Nt = data['Nt']
    Ndl = data['Ndl']
    Nbm = data['Nbm']
    Nbat = data['Nbat']

    # Definindo a quantidade de variáveis reais (Nr) e variáveis inteiras (Ni)
    # p_bm, p_chg, p_dch, soc, p_dl
    Nr = (Nt * Nbm) + (Nt * Nbat) + (Nbat * Nt) + (Nbat * Nt) + (Ndl * Nt)
    # u_bm, u_chg, u_dch, u_dl
    Ni = (Nt * Nbm) + (Nt * Nbat) + (Nbat * Nt) + (Ndl * Nt)
    x = np.random.rand(Nr + Ni)


    path = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
    cenarios = import_scenarios_from_pickle(path)

    for cenario in cenarios:

        data['p_l'] = cenario['p_l']
        data['p_pv'] = cenario['p_pv']
        data['p_wt'] = cenario['p_wt']
    

    eq = eq_constr(x, data)

    print(f'eq shape {eq.shape} and type {type(eq)}\n{eq}\n')