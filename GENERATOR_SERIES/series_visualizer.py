# from matplotlib import pyplot as plt
# from pathlib import Path
# import pandas as pd
# import numpy as np

"""

    Script de Visualização de Séries Horárias de Potência Fotovoltaica

    Este script realiza a leitura e visualização de séries horárias de potência (em kW) 
    geradas por sistemas fotovoltaicos em quatro localidades do estado do Rio de Janeiro:
    - Niterói
    - Búzios
    - Itaocara
    - Angra dos Reis

    Os dados foram extraídos do PVGIS e estão no formato CSV. Cada arquivo possui 8760 valores
    correspondentes a cada hora do ano.

    Etapas realizadas pelo script:
    1. Leitura dos arquivos de entrada.
    2. Extração das séries de potência (coluna 'P').
    3. Armazenamento dos dados em um dicionário.
    4. Plotagem das 504 primeiras horas para comparação visual.

"""

# path = Path(__file__).parent

# path_1 = path / 'DATA_BASE' /'solar_time_series_niteroi.csv'
# path_2 = path / 'DATA_BASE' /'solar_time_series_buzios.csv'
# path_3 = path / 'DATA_BASE' /'solar_time_series_itaocara.csv'
# path_4 = path / 'DATA_BASE' /'solar_time_series_angra_dos_reis.csv'

# solar_tsdata_niteroi = pd.read_csv(path_1, sep = ',', skiprows = 10, nrows = 8760)
# solar_tsdata_buzios = pd.read_csv(path_2, sep = ',', skiprows = 10, nrows = 8760)
# solar_tsdata_itaocara = pd.read_csv(path_3, sep = ',', skiprows = 10, nrows = 8760)
# solar_tsdata_angra = pd.read_csv(path_4, sep = ',', skiprows = 10, nrows = 8760)

# PVsytemPwr_niteroi = solar_tsdata_niteroi['P'].to_numpy()
# PVsytemPwr_buzios = solar_tsdata_buzios['P'].to_numpy()
# PVsytemPwr_itaocara = solar_tsdata_itaocara['P'].to_numpy()
# PVsytemPwr_angra = solar_tsdata_angra['P'].to_numpy()



# x = np.arange(504)


# plt.figure(figsize = (15, 5))
# plt.plot(x, PVsytemPwr_niteroi[: 504,])
# plt.plot(x, PVsytemPwr_buzios[: 504,])
# plt.plot(x, PVsytemPwr_itaocara[: 504,])
# plt.plot(x, PVsytemPwr_angra[: 504,])
# plt.title('PVPwrsystem')
# plt.ylabel('Potência kW')
# plt.xlabel('Hora')
# plt.legend(['Niterói', 'Búzios', 'Itaocara', 'Angra'])
# plt.show()

from matplotlib import pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np

# Caminho base do projeto (pasta onde está este script)
path = Path(__file__).parent

# Dicionário contendo nomes das localidades e caminhos dos arquivos CSV
files = {
    'Niterói': path / 'DATA_BASE' / 'solar_time_series_niteroi.csv',
    'Búzios': path / 'DATA_BASE' / 'solar_time_series_buzios.csv',
    'Itaocara': path / 'DATA_BASE' / 'solar_time_series_itaocara.csv',
    'Angra dos Reis': path / 'DATA_BASE' / 'solar_time_series_angra_dos_reis.csv'
}

# Dicionário para armazenar as séries de potência de cada localidade
power_data = {}

# Leitura dos dados CSV
for name, filepath in files.items():
    try:
        # Lê apenas 8760 linhas após o cabeçalho (10 linhas de metadados)
        df = pd.read_csv(filepath, sep=',', skiprows=10, nrows=8760)
        power_data[name] = df['P'].to_numpy()

        # Verificação simples de integridade
        if len(power_data[name]) < 504:
            print(f"Atenção: Série de {name} possui menos de 504 pontos!")
    except Exception as e:
        print(f"Erro ao ler dados de {name}: {e}")

# Vetor de tempo (horas) para as primeiras 504 horas
x = np.arange(504)

# Plotagem das séries
plt.figure(figsize=(15, 5))

for name, series in power_data.items():
    plt.plot(x, series[:504], label=name)

plt.title('Potência Fotovoltaica - Primeiras 504 Horas do Ano')
plt.xlabel('Hora')
plt.ylabel('Potência (kW)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
