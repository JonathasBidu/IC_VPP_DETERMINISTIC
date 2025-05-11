import numpy as np
import pandas as pd
from pathlib import Path
from generate_MPLRegressor import generate_MPL

"""
    Script para geração de séries sintéticas de carga elétrica com base em dados históricos reais.
    
    A carga analisada representa o perfil total de demanda de um alimentador de distribuição,
    conforme registrado pela concessionária Light S.A.

    Os dados originais são descritos no artigo publicado no JCAE 2020 (projeto PLANCAP).
    
    A modelagem estatística e a previsão das séries são realizadas por meio de um modelo 
    MLP Regressor (Multi-Layer Perceptron), ajustado com base no histórico horário obtido a partir
    de medições em intervalos de 15 minutos.

    Para mais informações sobre análise de resíduos e validação de modelos, consulte:
    https://www.mathworks.com/help/econ/infer-residuals.html
"""

def load_data():
    # Caminho da base de dados
    while True:
        aux = int(input('Digite o valor 1 para o arquivo Bandeira ou 2 para o arquivo Dafeira: '))
        if aux == 1:
            path = Path(__file__).parent / 'DATA_BASE' / 'Bandeira_load.txt'
            break
        elif aux == 2:
            path = Path(__file__).parent / 'DATA_BASE' / 'Dafeira_load.TXT'
            break
        else:
            print('Favor inserir o valor 1 para o arquivo Bandeira ou 2 para o arquivo Dafeira!')

    # Lê o arquivo de carga
    load_table = pd.read_csv(path, delimiter='\t', header=None)
    load_tsdata = load_table.to_numpy()

    # Converte a série de 15 min para horária (média de 4 em 4 pontos)
    hourly_tsdata = load_tsdata[::4]

    # Geração do modelo de previsão usando MLP
    p, mdl, Y, Yhat = generate_MPL(hourly_tsdata)

    # Definindo o número de pontos de previsão
    Npoints = 8760
    T = len(hourly_tsdata)
    pred_hourly_tsdata = np.zeros(Npoints)
    pred_hourly_tsdata[:p] = hourly_tsdata[:p].flatten()

    if Npoints < Yhat.shape[0]:
        pred_hourly_tsdata[p: T] = Yhat[p: Npoints]
    else:
        pred_hourly_tsdata[p: T] = Yhat

    t = T
    while t < Npoints:
        aux = np.array(pred_hourly_tsdata[t - p: t])
        aux = aux.reshape(-1, p)
        pred_hourly_tsdata[t] = mdl.predict(aux)[0]
        t += 1

    # Número de séries desejadas
    while True:
        n = input('Insira a quantidade de séries desejada ou tecle enter para 11: ')
        if n == '':
            n = 11
            break
        try:
            n = int(n)
            if n > 0:
                break
            else:
                print("Insira um valor numérico válido!")
        except ValueError:
            print('Insira um valor numérico válido!')

    # Adicionando ruído para gerar séries distintas
    pred_hourly_tsdata = pred_hourly_tsdata.flatten()
    load_hourly_tsdata = np.zeros((n, Npoints))
    load_hourly_tsdata[0, :] = pred_hourly_tsdata

    for i in range(1, n):
        delta = 0.05 * pred_hourly_tsdata * np.random.randn(Npoints)
        load_hourly_tsdata[i, :] = pred_hourly_tsdata + delta

    # Convertendo para potência aparente trifásica (VA) com base em tensão de 13,8 kV
    S_base = np.sqrt(3) * 13.8e3
    load_hourly_tsdata *= S_base

    return load_hourly_tsdata

# Execução principal
if __name__ == '__main__':

    # Quantidade de cargas a serem geradas
    while True:
        N = input('Digite a quantidade de cargas desejadas ou tecle enter para 3: ')
        if N == '':
            N = 3
            break
        try:
            N = int(N)
            if N > 0:
                break
            else:
                print('Insira um valor numérico válido!')
        except ValueError as v:
            print(f'Insira um valor numérico válido.\nERRO: {v}')

    save_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'load_hourly_series.xlsx'

    with pd.ExcelWriter(save_path) as writer:
        for i in range(N):
            load_hourly_tsdata = load_data()
            load_hourly_tsdata = load_hourly_tsdata / np.max(load_hourly_tsdata)
            load_hourly_series_df = pd.DataFrame(load_hourly_tsdata)
            load_hourly_series_df.to_excel(writer, sheet_name=f'Carga {i + 1}', header=None, index=False)

    print('FIM')
