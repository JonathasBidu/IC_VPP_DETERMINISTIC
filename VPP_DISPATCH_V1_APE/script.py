from generator_scenarios import import_scenarios_from_pickle
from update_p_bm import update
from decompose_vetor import decompose
from optimizer_GA import solver
from vpp_initial_data import vpp_data
from plot import plot
from pathlib import Path

'''
    Este script tem a finalidade de simular uma Virtual Power Plant (VPP) e obter despachos otimizados visando o lucro.
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

# Carregar dados iniciais da VPP
data = vpp_data()
data['Nt'] = Nt
Nbm = data['Nbm']
Nbat = data['Nbat']

# Definindo a capacidade instalada das Usina Solares
while True:
    cap_pv = input('Insira a capacidade das Usinas Solares em p.u.: ')
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
    cap_wt = input('Insira a capacidade das Usinas Eólicas em p.u.: ')
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
    cap_load = input('Insira a capacidade das Cargas em p.u.: ')
    try:
        cap_load = float(cap_load)
        if cap_load > 0:
            break
        else:
            print('Insira um valor real positivo!')
    except ValueError as v:
        print('Insira um valor númerico válido!')

# Carregando os cenários de um aquivo pickle
path = Path(__file__).parent / "scenarios_with_PVGIS.pkl"
cenarios = import_scenarios_from_pickle(path)

# Processando os cenários e ajustando os dados
for cenario in cenarios:

    data['p_l'] = cenario['p_l']
    data['p_pv'] = cenario['p_pv']
    data['p_wt'] = cenario['p_wt']
    data['p_dl_ref'] = cenario['p_dl_ref']
    data['tau_pld'] = cenario['tau_pld']
    data['tau_dist'] = cenario['tau_dist']
    data['tau_dl'] = cenario['tau_dl']

# Ajustando as potências pelas capacidades instaladas
p_l = data['p_l'] * cap_load
p_pv = data['p_pv'] * cap_pv
p_wt = data['p_wt'] * cap_wt
p_dl_ref = data['p_dl_ref'] * cap_load

# Ajustando a capacidade das usinas de biomassa
cap_bm_max, cap_bm_min, cap_bm_med = update(Nt, p_l, p_dl_ref, p_pv, p_wt) 
# for i in range(Nbm):
#     data['p_bm_max'][i] = cap_bm_med

# print(data['p_bm_max'])
# print(data['p_bm_min'],'\n')

# Definindo o limite de corte de carga
while True:
    delta = input(f'Insira o limite inferior de corte de carga ((%) acima da referência) ou tecle enter para 100 %: ')
    print('')
    if delta == '':
        delta = 1.0
    try:
        delta = float(delta)
        if delta >= 0:
            break
        else:
            print('Insira um valor real e positivo')
    except ValueError as v:
        print(f'Insira um valor numérico e válido {v}')

# Ajustando a banda de carga
data['p_dl_max'] = data['p_dl_ref'] + data['p_dl_ref'] * delta
data['p_dl_min'] = data['p_dl_ref'] - data['p_dl_ref'] * delta

# Obtendo a solução do otimizador (GA)
res = solver(data)

x = res.X # Matriz de soluções ótimas

if x is not None:

    # Decompondo o vetor de soluções nas suas variáveis de decisão
    data['p_bm'], data['p_chg'], data['p_dch'], data['soc'], data['p_dl'], data['u_bm'], data['u_chg'], data['u_dch'], data['u_dl'] = decompose(x, data)

    # Gerando gráfico
    plot(data)

    # Exibindo o lucro obtido
    valor = res.F[0]
    valor = f'{valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

    print(f'\nO lucro obtido nessa simulação foi de {valor} R$\n')
    print(f'Nessa simulação as restrições foram violadas {res.CV[0]} vezes\n')
else:
    print('\nSolução não encontrada\n')
