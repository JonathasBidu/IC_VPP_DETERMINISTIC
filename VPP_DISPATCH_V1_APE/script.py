from generator_scenarios import import_scenarios_from_pickle
from decompose_vetor import decompose
from vpp_initial_data import vpp_data
from optimizer_GA import solver
from update_p_bm import update
from pathlib import Path
from plot import plot
import numpy as np

'''
    Este script simula uma Virtual Power Plant (VPP) e otimiza o despacho de energia para maximizar o lucro.

    A VPP é composta por usinas solares, eólicas, e de biomassa, considerando demandas de carga, geração renovável, e tarifas. A otimização é realizada utilizando um Algoritmo Genético (GA), respeitando as restrições de capacidade das usinas e das cargas.

    -> Funcionalidade:
        1. Entrada de Parâmetros: O usuário define o período da simulação, capacidades das usinas solares, eólicas e de carga, e o limite de corte de carga.
        2. Carregamento de Cenários: O script carrega dados de cenários (perfis de carga, geração renovável, e tarifas) de um arquivo pickle.
        3. Ajuste das Potências: As potências de carga e geração são ajustadas conforme as capacidades instaladas.
        4. Atualização da Biomassa: Calcula os limites de potência para a usina de biomassa e gera uma curva de duração das cargas (Opcional).
        5. Otimização do Despacho: O Algoritmo Genético é usado para otimizar o despacho de energia, maximizando o lucro.
        6. Resultados: Exibe o lucro obtido e gera gráficos das durações das cargas e do despacho otimizado.

    -> Entradas:
        - Nt: Número de períodos de simulação.
        - cap_pv: Capacidade das Usinas Solares em p.u.
        - cap_wt: Capacidade das Usinas Eólicas em p.u.
        - cap_load: Capacidade das Cargas em p.u.
        - delta: Limite percentual de corte de carga.

    -> Saídas:
        - Lucro: Lucro obtido com a operação da VPP.
        - Gráficos: Curvas de duração das cargas e despacho otimizado.

    -> Dependências:
        - generator_scenarios: Carrega cenários de um arquivo pickle.
        - decompose_vetor: Decomposição do vetor de soluções.
        - vpp_initial_data: Dados iniciais da VPP.
        - optimizer_GA: Otimização do despacho de energia.
        - update_p_bm: Atualização dos limites da usina de biomassa.
        - plot: Geração de gráficos de resultados.

'''

# Definindo o período da simulação da VPP
while True:
    Nt = input('Insira o período da simulação ou tecle enter para 24h: ')
    if Nt == '':
        Nt = 24
        break
    try:
        Nt = int(Nt)
        if Nt > 0:
            break
        else:
            print('Insira um valor inteiro e positivo')
    except ValueError as v:
        print(f'Insira um valor inteiro e positivo! {v}')

# Definindo a capacidade instalada das Usina Solares
while True:
    cap_pv = input('Insira a capacidade das Usinas Solares em p.u. ou tecle enter para 2.75 p.u.: ')
    if cap_pv == '':
        cap_pv = 2.75
    try:
        cap_pv = float(cap_pv)
        if cap_pv > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo a capacidade instalada das Usina Eólicas
while True:
    cap_wt = input('Insira a capacidade das Usinas Eólicas em p.u. ou tecle enter para 10.0 p.u.: ')
    if cap_wt == '':
        cap_wt = 10.0     
    try:
        cap_wt = float(cap_wt)
        if cap_wt > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo a capacidade instalada das Cargas
while True:
    cap_load = input('Insira a capacidade das Cargas em p.u. ou tecle enter para 1 p.u.: ')
    if cap_load == '':
        cap_load = 1.0
    try:
        cap_load = float(cap_load)
        if cap_load > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Definindo o limite de corte de carga
while True:
    delta = input(f'Insira o limite inferior e superior de corte de carga ((%) acima  e abaixo da referência) ou tecle enter para 20 %: ')
    print('')
    if delta == '':
        delta = 0.2
    try:
        delta = float(delta)
        if delta >= 0:
            break
        else:
            print('Insira um valor real e positivo')
    except ValueError as v:
        print(f'Insira um valor numérico e válido {v}')

# Carregamento de dados iniciais da VPP
data = vpp_data()
data['Nt'] = Nt
Nbm = data['Nbm']
Nbat = data['Nbat']

# Carregando os cenários de um arquivo pickle contendo perfis de carga, geração renovável
# e tarifas aplicáveis (PLD, distribuidora e compensação por corte de carga)
path = Path(__file__).parent / "scenarios_with_PVGIS.pkl"
cenarios = import_scenarios_from_pickle(path)

# Sorteando aleatoriamente um índice de cenário dentre os disponíveis
idx = np.random.choice(len(cenarios))
# Selecionando o cenário correspondente ao índice sorteado
cenario = cenarios[idx]
# Atribuindo os dados do cenário ao dicionário 'data':
data['p_l'] = cenario['p_l']                 # perfil de carga
data['p_pv'] = cenario['p_pv']               # geração fotovoltaica
data['p_wt'] = cenario['p_wt']               # geração eólica
data['p_dl_ref'] = cenario['p_dl_ref']       # carga deslocável de referência
data['tau_pld'] = cenario['tau_pld']         # tarifa PLD
data['tau_dist'] = cenario['tau_dist']       # tarifa da distribuidora
data['tau_dl'] = cenario['tau_dl']           # tarifa de corte de carga

# Ajustando as potências pelas capacidades instaladas (em p.u)
p_l = data['p_l'] * cap_load
p_pv = data['p_pv'] * cap_pv
p_wt = data['p_wt'] * cap_wt
p_dl_ref = data['p_dl_ref'] * cap_load

#  Definindo banda de corte de carga baseado no percentual fornecido
data['p_dl_max'] = data['p_dl_ref'] + data['p_dl_ref'] * delta
data['p_dl_min'] = data['p_dl_ref'] - data['p_dl_ref'] * delta

# Gerando curva de duração de carga para análise visual da biomassa
cap_bm_max, cap_bm_min, cap_bm_med = update(Nt, p_l, p_dl_ref, p_pv, p_wt) 

# Resolvendo o problema de otimização com Algoritmo Genético
res = solver(data)

x = res.X # Matriz a solução ótima

if x is not None:

    # Decompondo o vetor de soluções nas variáveis de decisão
    data['p_bm'], data['p_chg'], data['p_dch'], data['soc'], data['p_dl'], data['u_bm'], data['u_chg'], data['u_dch'], data['u_dl'] = decompose(x, data)

    # Gerando gráfico
    plot(data)

    # Exibindo o lucro obtido
    valor = res.F[0]
    valor = f'{valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

    print(f'\nO lucro obtido nessa simulação foi de {valor} R$\n')
    # print(f'Nessa simulação as restrições foram violadas {res.CV[0]} vezes\n')
else:
    print('\nSolução não encontrada\n')
