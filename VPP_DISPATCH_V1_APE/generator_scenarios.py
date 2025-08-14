from load_projections import projections
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pickle

'''
    Este script tem como objetivo gerar, salvar e carregar cenários de operação 
    de uma Virtual Power Plant (VPP), a partir de projeções temporais de:

        - Potência gerada por usinas solares (PV) e eólicas (WT);
        - Cargas despacháveis (DL) e não despacháveis (NL);
        - Tarifas de energia:
            - Distribuidora;
            - PLD (Preço de Liquidação de Diferenças);
            - Compensação por corte de carga.

    Funcionalidades disponíveis:

    ------------------------------------------------------------------------
    1. [create_scenarios]

        Gera múltiplos cenários de operação para diferentes anos, mantendo 
        fixo o mesmo dia e hora do ano. Cada cenário corresponde a um ano 
        aleatório entre 2013 e 2023.

        Parâmetros:
            - Ns (int): Quantidade de cenários a serem gerados.
            - data (dict): Dicionário com os parâmetros iniciais da VPP, 
              incluindo o número de horas (Nt) do intervalo de simulação.

        Retorno:
            - scenarios (list[dict[str, np.ndarray]]): 
                Lista contendo dicionários com as séries temporais 
                para cada cenário.

    ------------------------------------------------------------------------
    2. [save_scenarios_to_pickle]

        Salva os cenários gerados em um arquivo .pkl.

        Parâmetros:
            - scenarios (list[dict[str, np.ndarray]]): 
                Lista de cenários gerados pela função `create_scenarios`.
            - path (Path): 
                Caminho completo para o arquivo onde os dados serão salvos.

        Retorno:
            - None

    ------------------------------------------------------------------------
    3. [import_scenarios_from_pickle]

        Importa cenários previamente salvos em formato .pkl.

        Parâmetros:
            - path (Path): 
                Caminho do arquivo .pkl com os cenários salvos.

        Retorno:
            - scenarios (list[dict[str, np.ndarray]]): 
                Lista de dicionários com os dados de cada cenário importado.
'''

# def create_scenarios(Ns: int, data: dict) -> list[dict[str, np.ndarray]]:

#     Nt = data['Nt']
#     Npoints = 8760  # Total de horas em um ano
#     base_year = 2013
#     total_years = 11  # De 2013 até 2023

#     # Sorteia um único dia e hora (fixo para todos os cenários)
#     max_start_day = (Npoints - Nt) // 24
#     begin = np.random.randint(0, max_start_day) * 24
#     end = begin + Nt

#     scenarios = []

#     for n in range(Ns):

#         idx = np.random.choice(total_years)  # idx de 0 a 10
#         year = base_year + idx

#         # Data real da simulação
#         selected_date = datetime(year, 1, 1) + timedelta(hours = begin)
#         print(f"Cenário para {selected_date.strftime('%d/%m/%Y')} às {selected_date.strftime('%H:%M')}")

#         # Projeções para o ano escolhido (linha = idx)
#         p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl = projections(data, begin, end, idx)

#         scenario = {
#             'p_l': p_l,
#             'p_pv': p_pv,
#             'p_wt': p_wt,
#             'p_dl_ref': p_dl_ref,
#             'tau_pld': tau_pld,
#             'tau_dist': tau_dist,
#             'tau_dl': tau_dl
#         }
#         scenarios.append(scenario)

#     return scenarios

# from datetime import datetime, timedelta
# import numpy as np

# def create_scenarios(Ns: int, data: dict, season: str) -> list[dict[str, np.ndarray]]:
#     Nt = data['Nt']
#     Npoints = 8760  # Total de horas em um ano
#     base_year = 2013
#     total_years = 11  # De 2013 até 2023

#     # Mapeamento dos meses por estação (hemisfério sul)
#     season_months = {
#         'verao': [12, 1, 2],      # dezembro, janeiro, fevereiro
#         'outono': [3, 4, 5],      # março, abril, maio
#         'inverno': [6, 7, 8],     # junho, julho, agosto
#         'primavera': [9, 10, 11]  # setembro, outubro, novembro
#     }

#     if season not in season_months:
#         raise ValueError(f"Estação inválida: {season}. Use: verao, outono, inverno ou primavera.")

#     scenarios = []

#     for n in range(Ns):
#         idx = np.random.choice(total_years)
#         year =  2023 #base_year + idx

#         mes = np.random.choice(season_months[season])

#         ano_inicio = year 

#         hora_inicio = (datetime(ano_inicio, mes, 1) - datetime(ano_inicio, 1, 1)).days * 24
#         begin = hora_inicio
#         end = begin + Nt

#         if end > Npoints:
#             begin = Npoints - Nt
#             end = Npoints

#         selected_date_start = datetime(ano_inicio, 1, 1) + timedelta(hours=begin)
#         selected_date_end = selected_date_start + timedelta(hours=Nt - 1)

#         print(f"Cenário {n+1} → {season.title()} ({year}): início {selected_date_start.strftime('%d/%m/%Y %H:%M')} - fim {selected_date_end.strftime('%d/%m/%Y %H:%M')}\n")

#         p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl = projections(data, begin, end, idx)

#         scenario = {
#             'p_l': p_l,
#             'p_pv': p_pv,
#             'p_wt': p_wt,
#             'p_dl_ref': p_dl_ref,
#             'tau_pld': tau_pld,
#             'tau_dist': tau_dist,
#             'tau_dl': tau_dl,
#             'ano': year,
#             'mes': mes,
#             'inicio': selected_date_start,
#             'fim': selected_date_end
#         }

#         scenarios.append(scenario)

#     return scenarios

from datetime import datetime, timedelta
import numpy as np

def create_scenarios(Ns: int, data: dict, season: str) -> list[dict[str, np.ndarray]]:
    Nt = data['Nt']
    Npoints = 8760  # Total de horas em um ano
    year = 2015     # Ano fixo
    idx = 2         # Índice do ano de 2015 no conjunto de dados

    # Mapeamento dos meses por estação (hemisfério sul)
    season_months = {
        'verao': [12, 1, 2],
        'outono': [3, 4, 5],
        'inverno': [6, 7, 8],
        'primavera': [9, 10, 11]
    }

    if season not in season_months:
        raise ValueError(f"Estação inválida: {season}. Use: verao, outono, inverno ou primavera.")

    scenarios = []

    for n in range(Ns):
        mes = np.random.choice(season_months[season])

        hora_inicio = (datetime(year, mes, 1) - datetime(year, 1, 1)).days * 24
        begin = hora_inicio
        end = begin + Nt

        if end > Npoints:
            begin = Npoints - Nt
            end = Npoints

        selected_date_start = datetime(year, 1, 1) + timedelta(hours=begin)
        selected_date_end = selected_date_start + timedelta(hours=Nt - 1)

        print(f"Cenário {n+1} → {season.title()} (2015): início {selected_date_start.strftime('%d/%m/%Y %H:%M')} - fim {selected_date_end.strftime('%d/%m/%Y %H:%M')}\n")

        p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl = projections(data, begin, end, idx)

        scenario = {
            'p_l': p_l,
            'p_pv': p_pv,
            'p_wt': p_wt,
            'p_dl_ref': p_dl_ref,
            'tau_pld': tau_pld,
            'tau_dist': tau_dist,
            'tau_dl': tau_dl,
            'ano': year,
            'mes': mes,
            'inicio': selected_date_start,
            'fim': selected_date_end
        }

        scenarios.append(scenario)

    return scenarios



# Função para salvar os cenários em formato .pkl
def save_scenarios_to_pickle(scenarios: list[dict[str, np.ndarray]], path: Path) -> None:
    with open(path, 'wb') as file:
        pickle.dump(scenarios, file)

# Função para carregar os cenários de um arquivo .pkl
def import_scenarios_from_pickle(path: Path) -> list[dict[str, np.ndarray]]:

    with open(path, 'rb') as file:
        scenarios = pickle.load(file)
    return scenarios

# Teste de uso   
if __name__ == '__main__':

    from vpp_initial_data import vpp_data
    from matplotlib import pyplot as plt

    data = vpp_data()
    data['Nt'] = 24

    # Definindo uma quantidade de cenários
    while True:
        Ns = input('Insira a quantidade de cenários desejado ou tecle enter para 11 cenários: ')
        if Ns == '':
            Ns = 11
            break
        try:
            Ns = int(Ns)
            if Ns > 0:
                Ns = Ns
                break
            else:
                print('Insira um valor inteiro e positivo!')
        except ValueError as v:
            print(f'Informe um valor numérico válido! {v}\n')

    # # Gerando uma quantidade de Ns cenários
    # scenarios = create_scenarios(Ns, data)

    # # Salvando os Ns cenários em um arquivo .pkl
    # path = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
    # save_scenarios_to_pickle(scenarios, path)

    # Carregando os cenários do arquivo .pkl  
    path_cenarios = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
    cenarios = import_scenarios_from_pickle(path_cenarios)

    idx = np.random.choice(11)
    
    # Plotando o primeiro cenário e visualizar a potência solar (p_pv) para verificar as séries temporais
    scenario_example = cenarios[idx]  # Pega o primeiro cenário gerado
    
    # Plotando a série temporal de p_pv (potência gerada por usinas solares)
    plt.figure(figsize=(10, 6))
    
    # Plotando todas as usinas solares (todas as linhas de p_pv)
    for i in range(scenario_example['p_pv'].shape[0]):  # Percorrendo as Npv usinas solares
        plt.plot(scenario_example['p_pv'][i], label=f'Usina Solar {i+1}')
    
    # Personalizando o gráfico
    plt.title('Série Temporal de Potência Gerada por Usinas Solares (p_pv)')
    plt.xlabel('Horas')
    plt.ylabel('Potência (kW)')
    plt.legend()
    plt.grid(True)
    
    # Exibindo o gráfico
    plt.show()
