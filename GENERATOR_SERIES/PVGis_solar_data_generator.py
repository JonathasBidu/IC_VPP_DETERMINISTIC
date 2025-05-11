import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

'''
    Este script tem a finalidade de processar, organizar e visualizar as séries horárias de geração de energia 
    elétrica provenientes de sistemas fotovoltaicos, calculadas pelo PVGIS (Photovoltaic Geographical Information System) 
    para quatro localidades do estado do Rio de Janeiro: Angra dos Reis, Búzios, Iguaba Grande e Itaocara.

    Os dados foram obtidos diretamente da plataforma PVGIS (https://pvgis.com/pt/pvgis-5-3), que fornece estimativas de 
    desempenho de sistemas solares baseadas em dados climáticos históricos e modelos fotovoltaicos.

    O script realiza as seguintes etapas:
    - Leitura dos arquivos CSV contendo dados horários de potência de saída (em W), irradiância e temperatura.
    - Normalização da potência pela base de 1 kVA (S_base = 1e3).
    - Reorganização dos dados em matrizes onde cada linha representa um ano e cada coluna uma hora do ano.
    - Visualização gráfica da série horária do primeiro ano para cada usina.
    - Exportação das matrizes processadas para um arquivo Excel, separando cada localidade em uma planilha distinta.

    Essa rotina é útil para análises sazonais, comparações interanuais de produção e estudos de integração com o sistema elétrico.
'''
# A Potência de Base 1kVA 
S_base = 1e3

path = Path(__file__).parent

# Obtendo o caminho das séries PVGIS
path_1 = path / "DATA_BASE" / 'hourly_data_Angra.csv'
path_2 = path / "DATA_BASE" / 'hourly_data_Buzios.csv'
path_3 = path / "DATA_BASE" / 'hourly_data_Iguaba.csv'
path_4 = path / "DATA_BASE" / 'hourly_data_Itaocara.csv'

# Obtendo o DataFrame das séries de Irradiância, Temperatura e Potência do ano de 2013 à 2023
tsdata_angra = pd.read_csv(path_1, sep = ',', skiprows = 10, nrows = 96360)
tsdata_buzios = pd.read_csv(path_2, sep = ',', skiprows = 10, nrows = 96360)
tsdata_iguaba = pd.read_csv(path_3, sep = ',', skiprows = 10, nrows = 96360)
tsdata_itaocara = pd.read_csv(path_4, sep = ',', skiprows = 10, nrows = 96360)

# Obtendo apenas a coluna de Potência da série calculada pelo PVGIS
tsdata_angra = tsdata_angra['P'] / S_base
tsdata_buzios = tsdata_buzios['P'] / S_base
tsdata_iguaba = tsdata_iguaba['P'] / S_base
tsdata_itaocara = tsdata_itaocara['P'] / S_base

# Quantidade de horas no ano (Npoints) e quantidade anos (Ns)
Npoints = 8760
Ns = tsdata_iguaba.shape[0] // Npoints

# Iniciando as matrizes em linhas que correspondem aos anos e colunas as horas
PVSystem_hourly_series_iguaba = np.zeros((Ns, Npoints))
PVSystem_hourly_series_angra = np.zeros((Ns, Npoints))
PVSystem_hourly_series_itaocara = np.zeros((Ns, Npoints))
PVSystem_hourly_series_buzios = np.zeros((Ns, Npoints))

# Preenchendo as matrizes 
for t in range(Ns):

    begin = t * Npoints 
    end = (t + 1) * Npoints 
    PVSystem_hourly_series_iguaba[t, :] = tsdata_iguaba[begin: end]
    PVSystem_hourly_series_angra[t, :] = tsdata_angra[begin: end]
    PVSystem_hourly_series_itaocara[t, :] = tsdata_itaocara[begin: end]
    PVSystem_hourly_series_buzios[t, :] = tsdata_buzios[begin: end]

# Plotagem de uma linha das matrizes para verificação dos dados
fig, ax = plt.subplots(ncols = 2, nrows = 2, figsize = (12, 7))

ax[0, 0].plot(PVSystem_hourly_series_angra[0, :], 'r')
ax[0, 0].set_title('Usina de Angra')

ax[0, 1].plot(PVSystem_hourly_series_buzios[0, :], 'b')
ax[0, 1].set_title('Usina de Búzios')

ax[1, 0].plot(PVSystem_hourly_series_itaocara[0, :], 'k')
ax[1, 0].set_title('Usina de Itaocara')

ax[1, 1].plot(PVSystem_hourly_series_iguaba[0, :], 'm')
ax[1, 1].set_title('Usina de Iguaba')

fig.suptitle('Séries Horárias de Geração Solar (1º Ano – Potência em kVA)', fontsize=16)
plt.tight_layout()
plt.subplots_adjust(top = 0.90)  # espaço para o suptitle
plt.show()

# Teste de uso
if __name__ == '__main__':

    output_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'PVGISSystem_hourly_series.xlsx'

    # Criando uma planilha do tipo xlsx
    with pd.ExcelWriter(output_path) as writer:

        PVSystem_hourly_series_angra = pd.DataFrame(PVSystem_hourly_series_angra)
        PVSystem_hourly_series_buzios = pd.DataFrame(PVSystem_hourly_series_buzios)
        PVSystem_hourly_series_iguaba = pd.DataFrame(PVSystem_hourly_series_iguaba)
        PVSystem_hourly_series_itaocara = pd.DataFrame(PVSystem_hourly_series_itaocara)
        PVSystem_hourly_series_angra.to_excel(writer, sheet_name = 'Angra dos Reis', index = False, header = None)
        PVSystem_hourly_series_buzios.to_excel(writer, sheet_name = 'Búzios', index = False, header = None)
        PVSystem_hourly_series_iguaba.to_excel(writer, sheet_name = 'Iguaba Grande', index = False, header = None)
        PVSystem_hourly_series_itaocara.to_excel(writer, sheet_name = 'Itaocara', index = False, header = None)

print(f'Séries exportadas com sucesso!')
