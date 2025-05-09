import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

'''
    Este Script coleta dados de irradiação solar (G(i)) e temperatura (T2m) de cidades, ex: (Angra dos Reis, Niterói, Búzios e Itaocara) para visualização e armazenamento em uma planilha Excel,
    organizada em abas por cidade. A primeira semana (168 horas) dos dados de irradiação e temperatura
    é visualizada por meio de gráficos.
    fonte: https://pvgis.com/pt/pvgis-5-3

'''

# Obtendo os caminhos das bases de dados
path = Path(__file__).parent

# Caminho para séries de Irradiância e Temperatura da cidade de Angra dos Reis
path_1 = path / "DATA_BASE" / "solar_time_series_angra_dos_reis.csv"

# Caminho para séries de Irradiância e Temperatura da cidade de Niterói
path_2 = path / "DATA_BASE" / "solar_time_series_niteroi.csv"

# Caminho para séries de Irradiância e Temperatura da cidade de Búzios 
path_3 = path / "DATA_BASE" / "solar_time_series_buzios.csv"

# Caminho para séries de Irradiância e Temperatura da cidade de Itaocara
path_4 = path / "DATA_BASE" / "solar_time_series_itaocara.csv"

# Obtendo os dados de irradiâcia e temperatura
angra_tsdata = pd.read_csv(path_1, sep = ',', skiprows = 10, nrows = 8760, usecols = ['G(i)', 'T2m'])
niteroi_tsdata = pd.read_csv(path_2, sep = ',', skiprows = 10, nrows = 8760, usecols = ['G(i)', 'T2m'])
buzios_tsdata = pd.read_csv(path_3, sep = ',', skiprows = 10, nrows = 8760, usecols = ['G(i)', 'T2m'])
itaocara_tsdata = pd.read_csv(path_4, sep = ',', skiprows = 10, nrows = 8760, usecols = ['G(i)', 'T2m'])

# gráfico da irradiânica nas primeiras 168 horas (1 semana)
plt.figure(figsize = (10, 5))
plt.title('Irradiância')
plt.plot(buzios_tsdata.to_numpy()[: 168, 0])
plt.plot(niteroi_tsdata.to_numpy()[: 168, 0])
plt.plot(angra_tsdata.to_numpy()[: 168, 0])
plt.plot(itaocara_tsdata.to_numpy()[: 168, 0])
plt.xlabel('hora')
plt.ylabel('Magnitude')
plt.legend(['Búzios', 'Niterói', 'Angra', 'Itaocara'])
plt.show()

# gráfico da temperatura das primeiras 168 horas (1 semana)
plt.figure(figsize = (10, 5))
plt.title('Temperatura')
plt.plot(buzios_tsdata.to_numpy()[: 168, 1])
plt.plot(niteroi_tsdata.to_numpy()[: 168, 1])
plt.plot(angra_tsdata.to_numpy()[: 168, 1])
plt.plot(itaocara_tsdata.to_numpy()[: 168, 1])
plt.xlabel('hora')
plt.ylabel('Magnitude')
plt.legend(['Búzios', 'Niterói', 'Angra', 'Itaocara'])
plt.show()

# Direcionando o caminho onde o arquivo será salvo
output_path = Path(__file__).parent / 'DATA_BASE' /'solar_hourly_series.xlsx'

# Criando uma planilha do tipo xlsx
with pd.ExcelWriter(output_path) as writer:
    angra_time_series = pd.DataFrame(angra_tsdata)
    niteroi_time_series = pd.DataFrame(niteroi_tsdata)
    buzio_time_series = pd.DataFrame(buzios_tsdata)
    itaocara_time_series = pd.DataFrame(itaocara_tsdata)
    angra_time_series.to_excel(writer, sheet_name = 'Angra dos Reis', index = False, header = None)
    niteroi_time_series.to_excel(writer, sheet_name = 'Niterói', index = False, header = None)
    buzio_time_series.to_excel(writer, sheet_name = 'Búzios', index = False, header = None)
    itaocara_time_series.to_excel(writer, sheet_name = 'Itaocara', index = False, header = None)