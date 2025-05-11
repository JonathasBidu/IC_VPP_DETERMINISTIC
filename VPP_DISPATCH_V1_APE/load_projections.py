from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

'''
    Este script tem a finalidade de carregar as projeções temporais iniciais da VPP geradas por geradores de séries temporais.

    - Parâmetros de entrada (data: dict):
        - data: Dicionário contendo o parâmetros iniciais da VPP
            - Nt: Período de simulação da VPP;
            - Nl: Quantidade de cargas NÃO despacháveis da VPP;
            - Ndl: Quantidade de cargas despacháveis da VPP;
            - Npv: Quantidade de usinas solares (FVs) da VPP;
            - Nwt: Quantidade de usinas eólicas (EOs) da VPP;

    - Retorna uma tupla contendo diversos array: -> tuple[np.ndarray]: (p_l, p_pv, p_wt, p_dl_ref, p_dl_min, p_dl_max, tau_pld, tau_dist, tau_dl):
        - p_l: Potência das cargas NÃO despacháveis da VPP, shape (Nl, Nt);
        - p_pv: Potência das FVs da VPP, shape (Npv, Nt);
        - p_wt: Potência das EOs da VPP, shape (Npv, Nt);
        - p_dl_ref: Potência de referência das cargas despacháveis da VPP, shape (Ndl, Nt);
        - p_dl_min: Potência mínima das cargas despacháveis da VPP, shape (Ndl, Nt);
        - p_dl_max: Potência máxima das cargas despacháveis da VPP, shape (Ndl, Nt);
        - tau_pld: Tarifa de Preço de Liquidação de Diferença (PLD), shape(Nt,);
        - tau_dist: Tarifa da distribuidora, shape (Nt,);
        - tau_dl: Tarifa de compensação por corte de carga, shape (Nt,)

'''

def projections(data: dict)-> tuple[np.ndarray]:

    # Base em pu da potência aparente
    S_base = 1e6

    # Obtendo a ierarquia do caminho das projeções iniciais
    path = Path(__file__).parent.parent

    # Obtendo os parâmetros iniciais da VPP
    Nt = data['Nt']
    Nl = data['Nl']
    Ndl = data['Ndl']
    Npv = data['Npv']
    Nwt = data['Nwt']

    # Quantidade de dias no ano
    max_start_day = (8760 - Nt) // 24
    begin = np.random.choice(max_start_day) * 24
    end = begin + Nt  


    # Data base: 1º de janeiro de 2023
    start_date = datetime(2023, 1, 1)

    # Número de horas sorteadas (já está em begin)
    selected_date = start_date + timedelta(hours = begin)

    print(f"\nProjeções iniciadas em {selected_date.strftime('%d/%m/%Y')} às {selected_date.strftime('%H:%M')}\n")



    # Carregamento das projeções das cargas NÃO despacháveis
    path_1 = path / 'GENERATED_SERIES' / 'load_hourly_series.xlsx' # Caminho das cargas NÃO despacháveis
    files = pd.ExcelFile(path_1) # Abas presentes no arquivo .xlsx
    p_l = np.zeros((Nl, Nt)) # Iniciando a variável de potência das cargas NÃO despacháveis

    # Iterando sobre as abas do arquivo .xlsx
    for i, sheet in enumerate(files.sheet_names):

        load_hourly_series = pd.read_excel(path_1, header = None, sheet_name = sheet)
        m, _ = load_hourly_series.shape
        idx = np.random.choice(m)

        p_l[i, :] = load_hourly_series.iloc[idx, begin: end].values

    # Carregamento das projeções das cargas despacháveis
    path_2 = path / 'GENERATED_SERIES' / 'dload_hourly_series.xlsx' # Caminho das cargas despacháveis
    files = pd.ExcelFile(path_2) # Abas presentes no arquivo .xlsx
    p_dl_ref = np.zeros((Ndl, Nt)) # Iniciando a variável de potência das cargas despacháveis

    # Iterando sobre as abas do arquivo .xlsx
    for i, sheet in enumerate(files.sheet_names):

        dload_hourly_series = pd.read_excel(path_2, header = None, sheet_name = sheet)
        m, _ = dload_hourly_series.shape
        idx = np.random.choice(m)

        p_dl_ref[i, :] = dload_hourly_series.iloc[idx, begin: end].values

    # Carregamento das projeções das usinas solares (FVs)
    # path_3 = path / 'GENERATED_SERIES' / 'PVsystem_hourly_series.xlsx' # Caminho do arquivo das projeções das FVs

    path_3 = path / 'GENERATED_SERIES' / 'PVGISSystem_hourly_series.xlsx' # Caminho do arquivo das projeções das FVs
    files = pd.ExcelFile(path_3) # Abas presentes no arquivo .xlsx
    p_pv = np.zeros((Npv, Nt)) # Iniciando a variável de potência das FVs

    # Iterando sobre as abas do arquivo .xlsx
    for i, sheet in enumerate(files.sheet_names):

        PVsystem_hourly_series = pd.read_excel(path_3, header = None, sheet_name = sheet)
        m, _ = PVsystem_hourly_series.shape
        idx = np.random.choice(m)

        p_pv[i, :] = PVsystem_hourly_series.iloc[idx, begin: end].values

    # Carregamento das projeções das usinas eólicas (EOs)
    path_4 = path / 'GENERATED_SERIES' / 'WTGsystem_hourly_series.xlsx' # Caminho do arquivo das projeções das EOs
    files = pd.ExcelFile(path_4)  # Abas presentes no arquivo .xlsx
    p_wt = np.zeros((Nwt, Nt)) # Iniciando a variável de potência das EOs

    # Iterando sobre as abas do arquivo .xlsx
    for i, sheet in enumerate(files.sheet_names):
               
        WTGsystem_hourly_series = pd.read_excel(path_4, header = None, sheet_name = sheet)
        m, _ = WTGsystem_hourly_series.shape
        idx = np.random.choice(m)

        p_wt[i, :] = WTGsystem_hourly_series.iloc[idx, begin: end].values / S_base

    # Carregamento do Preço de Liquidação de Diferenças (PLD)
    path_5 = path / 'GENERATED_SERIES' / 'PLD_hourly_series.csv' # Caminho da projeção de PLD
    PLD_hourly_series = pd.read_csv(path_5, sep = ';', header = None)
    m, _ = PLD_hourly_series.shape
    idx = np.random.choice(m)
    tau_pld = PLD_hourly_series.iloc[idx, begin: end].to_numpy() # Inciando a variável de tarifa PLD

    # Carregamento das projeções de tarifa da distribuidora
    path_6 = path / 'GENERATED_SERIES' / 'TDist_hourly_series.csv' # Caminho da projeção de tarifa da distribuidora
    TDist_hourly_series = pd.read_csv(path_6, sep = ';', header = None)
    m, _ = TDist_hourly_series.shape
    idx = np.random.choice(m)
    tau_dist = TDist_hourly_series.iloc[idx, begin: end].to_numpy() # Iniciando a variável de tarifa da distribuidora
    tau_dl = 0.15 * TDist_hourly_series.iloc[0, begin: end].to_numpy() # Abatimento de 15% sobre o valor da tarifa

    return p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl

# Exemplo de uso
if __name__ == '__main__':

    from vpp_initial_data import vpp_data
    from matplotlib import pyplot as plt

    # Obtendo os parâmetros iniciais da VPP
    data = vpp_data()
    data['Nt'] = 24
    Nl = data['Nl']
    Npv = data['Npv']
    Nwt = data['Nwt']
    Ndl = data['Ndl']

    # Obtendo as projeções temporais iniciais
    p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl = projections(data)

    # Visualização das projeções iniciais
    # Carga NÃO despacháveis
    for i in range(Nl):

        title = f'Carga NÃO despachável {i + 1}'
        plt.figure(figsize = (10, 5))
        plt.plot(p_l[i, :], 'r')
        plt.title(title)
        plt.xlabel('Hora')
        plt.ylabel('Potência em p.u.')
        plt.show()

    # Visualização das projeções das cargas despacháveis
    for i in range(Ndl):

        title = f'Carga despachável {i + 1}'
        plt.figure(figsize = (10, 5))
        plt.plot(p_dl_ref[i, :], 'k')
        plt.title(title)
        plt.legend(['ref', 'max', 'min'])
        plt.xlabel('Hora')
        plt.ylabel('Potência em p.u.')
        plt.show()

    # Usina solar
    for i in range(Npv):

        title = f'usina solar {i + 1}'
        plt.figure(figsize = (10, 5))
        plt.plot(p_pv[i, :], 'r')
        plt.title(title)
        plt.xlabel('Hora')
        plt.ylabel('Potência em p.u.')
        plt.show()

    # Usina eólica
    for i in range(Nwt):

        title = f'usina eólica {i + 1}'
        plt.figure(figsize = (10, 5))
        plt.plot(p_wt[i, :], 'r')
        plt.title(title)
        plt.xlabel('Hora')
        plt.ylabel('Potência em p.u.')
        plt.show()
 
    plt.figure(figsize = (10, 5))
    plt.plot(tau_pld)
    plt.title('Preço de Liquidação de Diferença')
    plt.xlabel('Hora')
    plt.show()
        
    # Plotagem da projeção da Tarifa da distribuição e da compensação para o usuário
    plt.figure(figsize = (10, 4))
    plt.title('Tarifa da Distribuição e Compensação')
    plt.plot(tau_dist, 'b')
    plt.plot(tau_dl, 'r')
    plt.legend(['Dist', 'Desc 15%'])
    plt.show()