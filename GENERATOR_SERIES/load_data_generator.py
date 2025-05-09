import numpy as np
import pandas as pd
from pathlib import Path
from generate_MPLRegressor import generate_MPL

"""
    Script para geração de séries de carga a partir de um histórico de dados a carga refere-se a carga total de um alimentador
    de de dist. Fonte dos dados: Light S.A (Artigo JCAE 2020 PLANCAP)
    Link análise estatística -> https://www.mathworks.com/help/econ/infer-residuals.html
"""
def load_data():

    # Caminho da base de dados'    
    while True:
        aux = int(input('Digite o valor 1 para o arquivo Bandeira ou 2 para o arquivo Dafeira: '))
        if aux == 1:
            path = Path(__file__).parent / 'DATA_BASE' / 'Bandeira_load.txt'
            break
        elif aux == 2:
            path = Path(__file__).parent / 'DATA_BASE' / 'Dafeira_load.TXT'
            break
        else:
            print('Favor inserir o valor 1, para o arquivo Bandeira ou tecle, para o arquivo Dafeira!')


    load_Table = pd.read_csv(path, delimiter = '\t', header = None)
    # convertendo as séries em objeto numpy
    load_tsdata = load_Table.to_numpy()

    # fatiando a série em intervalo de 4 em 4 (cada dado equivale a 15 minutos)
    hourly_tsdata = load_tsdata[::4]

    # Importando a função generate_MPLRegressor onde, uma lista deverá ser fornecida em seu argumento, e está retornará o modelo(net_n), o lag(p_n), as saídas esperadas(Y_n), e a saída obtidas pelo modelo de previsão MLPRegressor(Yhat_n)
    p, Mdl, Y, Yhat = generate_MPL(hourly_tsdata)

    # definindo um intervalo de horas
    Npoints = 8760
    T = len(hourly_tsdata)
    pred_hourly_tsdata_2 = np.zeros(Npoints)
    pred_hourly_tsdata_2[:p] = hourly_tsdata[:p].flatten()

    if Npoints < Yhat.shape[0]:
        pred_hourly_tsdata_2[p: T] = Yhat[p: Npoints]
    else:
        pred_hourly_tsdata_2[p: T] = Yhat

    t = T
    while t < Npoints:
        aux = np.array(pred_hourly_tsdata_2[t - p: t])
        aux = aux.reshape(-1, p)
        pred_hourly_tsdata_2[t] = Mdl.predict(aux)[0]
        t += 1

    while True:
        n = input('Insira a quantidade de séries desejada ou tecle enter para 11: ')
        if n == '':
            n = 11
            break
        try:
            n = int(n)
            if n > 0:
                n = n
                break
            else:
                print("Insira um valor numérico válido!")
        except ValueError:
            print('Insira um valor numérico válido!')

    pred_hourly_tsdata_2 = pred_hourly_tsdata_2.flatten()
    load_hourly_tsdata = np.zeros((n, Npoints))
    load_hourly_tsdata[0,:] = pred_hourly_tsdata_2

    for i in range(n):
        delta_2 = 0.05 * pred_hourly_tsdata_2 * np.random.randn(Npoints)
        load_hourly_tsdata[i, :] = pred_hourly_tsdata_2 + delta_2

    load_hourly_tsdata = np.sqrt(3) * 13.8e3 * load_hourly_tsdata


    return load_hourly_tsdata

if __name__ == '__main__':

    import matplotlib.pyplot as plt    

    while True:
        N = input('Digite a quantidade de Cargas desejadas ou tecle enter para 3: ')
        if N == '':
            N = 2
            break
        try:
            N = int(N)
            if N > 0:
                break
            else:
                print('Insira um valor numérico válido')
        except ValueError as v:
            print(f'Insira um valor numérico válido\nERRO, {v}')

    save_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'dload_hourly_series.xlsx'

    with pd.ExcelWriter(save_path) as writer:
        for i in  range(N):
            load_hourly_tsdata = load_data()
            load_horly_series_df = pd.DataFrame(load_hourly_tsdata)
            load_horly_series_df.to_excel(writer, sheet_name = f'Carga {i + 1}', header = None, index = False)
    
    print('FIM')