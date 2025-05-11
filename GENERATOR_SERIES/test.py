from pathlib import Path
import pandas as pd
import numpy as np

'''
    Este script tem a finalidade de organizar séries históricas de potência de usinas solares 
'''
# Potência aparente de base é 1MW
S_base = 1e3

path = Path(__file__).parent

path_1 = path/ 'DATA_BASE' / 'hourly_data_Iguaba.csv'
path_2 = path/ 'DATA_BASE' / 'hourly_data_Angra.csv'
path_3 = path/ 'DATA_BASE' / 'hourly_data_Itaocara.csv'
path_4 = path/ 'DATA_BASE' / 'hourly_data_Buzios.csv'

tsdata_iguaba = pd.read_csv(path_1, sep = ',', skiprows = 10, nrows = 96360)
tsdata_angra = pd.read_csv(path_2, sep = ',', skiprows = 10, nrows = 96360)
tsdata_itaocara = pd.read_csv(path_3, sep = ',', skiprows = 10, nrows = 96360)
tsdata_buzios = pd.read_csv(path_4, sep = ',', skiprows = 10, nrows = 96360)


tsdata_iguaba = tsdata_iguaba['P'] / S_base
tsdata_angra = tsdata_angra['P'] / S_base
tsdata_itaocara = tsdata_itaocara['P'] / S_base
tsdata_buzios = tsdata_buzios['P'] / S_base

Npoits = 8760
Ns = tsdata_iguaba.shape[0] // Npoits


solar_hourly_series_iguaba = np.zeros((Ns, Npoits))
solar_hourly_series_angra = np.zeros((Ns, Npoits))
solar_hourly_series_itaocara = np.zeros((Ns, Npoits))
solar_hourly_series_buzios = np.zeros((Ns, Npoits))

for t in range(Ns):

    begin = t * Npoits
    end = (t + 1) * Npoits

    solar_hourly_series_iguaba[t, : ] = tsdata_iguaba[begin: end]
    solar_hourly_series_angra[t, : ] = tsdata_angra[begin: end]
    solar_hourly_series_itaocara[t, : ] = tsdata_itaocara[begin: end]
    solar_hourly_series_buzios[t, : ] = tsdata_buzios[begin: end]

from matplotlib import pyplot as plt


fig, ax = plt.subplots(ncols = 2, nrows = 2, figsize = (12, 7))

ax[0, 0].plot(solar_hourly_series_angra[0, :], 'r')
ax[0, 0].set_title('Usina de Angra')


ax[0, 1].plot(solar_hourly_series_buzios[0, :], 'b')
ax[0, 1].set_title('Usina de Búzios')

ax[1, 0].plot(solar_hourly_series_itaocara[0, :], 'k')
ax[1, 0].set_title('Usina de Itaocara')

ax[1, 1].plot(solar_hourly_series_iguaba[0, :], 'm')
ax[1, 1].set_title('Usina de Iguaba')

fig.suptitle('Séries Horárias de Usinas Solares (Ano 1)', fontsize=16)
plt.tight_layout()
plt.subplots_adjust(top=0.90)  # espaço para o suptitle
plt.show()
