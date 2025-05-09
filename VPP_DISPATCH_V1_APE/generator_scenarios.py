from load_projections import projections
from pathlib import Path
import numpy as np
import pickle

'''
    Este script tem a finalidade de gerar, salvar e carregar cenários a partir de de projeções temporais de potências de usinas solares, eólicas e cargas despacháveis e não despacháveis, além de, séries temporais de tarifa de distribuidoras de energia, tarifa de Preço de Liquidação de Diferenças (PLD) e compesação de corte de carga.

    -> Função de geração de cenários [create_scenarios]: Esta função tem o objetivo de criar múltiplos cenários com combinações das projeções.
        - Parâmetros de entrada (Ns: int, data: dict).
            - (Ns: int): Quantidade de cenários desejado;

            - (data: dict): Dicionário contendo parâmetros iniciais e projeções temporais iniciais da VPP.

        - Retorna -> (scenarios: list[dict[str, np.ndarray]]):
            - (scenarios: dict): Uma lista de dicionários, onde cada dicionário corresponde a um cenário, resultado de n combinções das projeções temporais iniciais.        
        
    -> Função de salvamento dos cenários gerados [save_scenarios_to_pickle]: Esta função tem a finalidade de salvar em arquivo pickle os cenários gerados pela função create_scenarios.
        - Parâmetros de entrada (scenarios: list[dict[str, np.ndarray]], path: Path).
            - (scenarios: list[dict[str, np.ndarray]]): Uma lista de dicionários onde é atribuídos os cenários gerados na função create_scenarios
            - (path: Path): Caminho para o diretório onde será salvo os cenário(s)

        - Retorna -> (None): Não há retorno nessa função.

    -> Função de importação dos cenários [import_scenarios_from_pickle]: Esta função tem o objetivo de importar os cenários que foram salvos em um arquivo pickle (pkl).
        - Parâmetros de entrada (path: Path).
            - path: Caminho do arquivo pkl onde estão salvos os cenários gerados pela função create_scenarios

        - Retorna (scenarios: list[dict[str, np.ndarray]]):
            - (scenarios: list[dict[str, np.ndarray]]): Uma lista de dicionários, onde cada dicionário representa um cenário.    
'''

# Função para geração de Ns(quantidade de cenários) desejados
def create_scenarios(Ns: int, data: dict) -> list[dict[str, np.ndarray]]:

    scenarios = []
    for s in range(Ns):
        p_l, p_pv, p_wt, p_dl_ref, tau_pld, tau_dist, tau_dl = projections(data)
        scenario = {
            'p_l': p_l,
            'p_pv': p_pv,
            'p_wt': p_wt,
            'p_dl_ref': p_dl_ref,
            'tau_pld': tau_pld,
            'tau_dist': tau_dist,
            'tau_dl': tau_dl
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

    # Gerando uma quantidade de Ns cenários
    scenarios = create_scenarios(Ns, data)

    # Salvando os Ns cenários em um arquivo .pkl
    path = Path(__file__).parent / 'scenarios_with_PVGIS.pkl'
    save_scenarios_to_pickle(scenarios, path)

    # # Carregando os cenários do arquivo .pkl  
    # path_cenarios = Path(__file__).parent / 'Cenários.pkl'
    # cenarios = import_scenarios_from_pickle(path_cenarios)

    # print(type(cenarios))
    # # print(len(cenarios))

    # print(cenarios[0]['p_l'])

    # p_ls = []
    # tau_dist = []
    # p_pvs = []

    # for cenario in cenarios:
    #     p_ls.append(cenario['p_l'])
    #     tau_dist.append(cenario['tau_dist'])
    #     p_pvs.append(cenario['p_pv'])

  
    # Cl = 0
    # for cenario in range(Ns):
    #     for i in range(Nl):
    #         for t in range(Nt):
    #             Cl += p_ls[cenario][i, t] * tau_dist[cenario][t]

    # print(f'Cl = {Cl:.2f}')
    # print(type(Cl))