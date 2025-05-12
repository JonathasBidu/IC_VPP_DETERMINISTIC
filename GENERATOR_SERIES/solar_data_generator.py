from pathlib import Path
import numpy as np
import pandas as pd
from PVGenPwr import PVGenPwr

"""
    Script de Geração e Visualização de Séries de Potência Fotovoltaica

    Este script:
        1. Lê dados de irradiância (W/m²) e temperatura (°C) de um arquivo Excel para várias localidades.
        2. Gera séries sintéticas de potência usando um modelo simplificado de painel fotovoltaico.
        3. Salva os resultados por localidade em um novo arquivo Excel.
        4. Exibe um gráfico de 24 horas com uma série aleatória para cada localidade.

    Requisitos:
        - Um módulo chamado `PVGenPwr` com a função `Pmmp, Vmmp, Immp = PVGenPwr(G, T, Np, Ns)`
        - Arquivo de entrada: `DATA_BASE/solar_hourly_series.xlsx` com colunas: [Irradiância, Temperatura]
"""


# Caminho do arquivo Excel com as séries climáticas
path = Path(__file__).parent / 'DATA_BASE' / 'solar_hourly_series.xlsx'

# Definindo o horizonte de Previsão (Npoints)
while True:
    Npoints = input('Insira o intervalo em horas desejado ou tecle enter para 168 horas(1 semana): ')
    if Npoints == '':
        Npoints = 168
        break
    try:
        Npoints = int(Npoints)
        if Npoints > 0:
            Npoints = Npoints
            break
        else:
            print('Digite um valor numérico válido')
    except ValueError:
        print('Digite um valor numérico válido')

# Definindo o número (n) de séries desejadas
while True:
    n = input('Digite a quantidade de séries desejada ou tecle enter para 11: ')
    if n == '':
        n = 11
        break
    try:
        n = int(n)
        if n > 0:
            n = n
            break
        else:
            print('Insira um valor numérico válido')
    except ValueError:
        print('insira um valor numérico válido') 

# quantidade de módulos em paralelo
Np = 400
# quantidade de módulos em série
Ns = 2000

# Obtendo os sheets(abas da planilha)
sheets = pd.ExcelFile(path)

# Criando o writer para o arquivo de saída
save_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'PVsystem_hourly_series.xlsx'

with pd.ExcelWriter(save_path) as writer:

    # Iterando sobre as abas da planilha
    for sheet in sheets.sheet_names:

        # Obtendo a série da região i
        solar_tsdata = pd.read_excel(path, sheet_name = sheet)

        # Criando uma matriz temporária de irradiância e temperatura
        irradiance_hourly_series = np.zeros((n, Npoints))
        temperature_hourly_series = np.zeros((n, Npoints))

        # Extração das séries em blocos
        for i in range(n):
            inicio = Npoints * i
            fim = Npoints * (i+1)
            irradiance_hourly_series[i, :] = solar_tsdata.iloc[inicio: fim, 0].values
            temperature_hourly_series[i, :] = solar_tsdata.iloc[inicio: fim, 1].values

        PVpwr_irradiance_hourly_series = np.zeros_like(irradiance_hourly_series)

        # Cálculo da potência via modelo PVGenPwr
        for s in range(n):
            for time in range(Npoints):
                T = temperature_hourly_series[s, time] + 273.15  # graus Kelvin
                G = irradiance_hourly_series[s, time]
                Pmmp, Vmmp, Immp = PVGenPwr(G, T, Np, Ns)
                PVpwr_irradiance_hourly_series[s, time] = Pmmp
                print(s, time)
        print(fim)

        PVpwr_hourly_series_pd = pd.DataFrame(PVpwr_irradiance_hourly_series)
        PVpwr_hourly_series_pd.to_excel(writer, sheet_name = sheet, index = False, header = None)

print("\nSéries geradas e exportadas com sucesso!")

# Teste de uso
if __name__ == '__main__':

    import matplotlib.pyplot as plt

    path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'PVsystem_hourly_series.xlsx'

    sheets = pd.ExcelFile(path)
  
    for sheet in sheets.sheet_names:

        PVpwr_irradiance_hourly_series = pd.read_excel(path, sheet_name = sheet)
        PVpwr_irradiance_hourly_series = PVpwr_irradiance_hourly_series.to_numpy()  
        idx = np.random.choice(PVpwr_irradiance_hourly_series.shape[0])

        plt.title('PVsystem')
        plt.plot(PVpwr_irradiance_hourly_series[idx, 0:24])
        plt.legend(['Angra dos Reis', 'Niterói', 'Búzios', 'Itaocara'])
        plt.xlabel('Hora')
        plt.ylabel('Carga')

    plt.show()
    