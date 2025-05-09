# import pandas as pd
# import numpy as np
# from matplotlib import pyplot as plt
# from pathlib import Path

# path = Path(__file__).parent.parent

# # Caminho para séries eólicas
# path_1 = path /'GENERATED_SERIES'/ 'WTGsystem_hourly_series.xlsx'
# files = pd.ExcelFile(path_1) # Abas presentes no arquivo .xlsx

# # Plot das séries eólicas
# for sheet_name in files.sheet_names:

#     df = pd.read_excel(files, sheet_name = sheet_name, header = None)
#     m, _ = df.shape
#     idx = np.random.choice(m)
#     title = f'Usina {sheet_name}'

#     plt.figure(figsize = (10, 5))
#     plt.plot(df.iloc[idx, :])
#     plt.title(title)
#     plt.xlabel('Hora')
#     plt.ylabel('Potência em MW')
#     plt.show()

# # Caminho para séries eólicas
# path_2 = path /'GENERATED_SERIES'/ 'PVsystem_hourly_series.xlsx'
# files = pd.ExcelFile(path_2) # Abas presentes no arquivo .xlsx

# # Plot das séries eólicas
# for sheet_name in files.sheet_names:

#     df = pd.read_excel(files, sheet_name = sheet_name, header = None)
#     m, _ = df.shape
#     idx = np.random.choice(m)
#     title = f'Usina {sheet_name}'

#     plt.figure(figsize = (10, 5))
#     plt.plot(df.iloc[idx, :].values * 1e2)
#     plt.title(title)
#     plt.xlabel('Hora')
#     plt.ylabel('Potência em MW')
#     plt.show()

from matplotlib import pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np

path = Path(__file__).parent

path_1 = path / 'DATA_BASE' /'solar_time_series_niteroi.csv'
path_2 = path / 'DATA_BASE' /'solar_time_series_buzios.csv'
path_3 = path / 'DATA_BASE' /'solar_time_series_itaocara.csv'
path_4 = path / 'DATA_BASE' /'solar_time_series_angra_dos_reis.csv'

solar_tsdata_niteroi = pd.read_csv(path_1, sep = ',', skiprows = 10, nrows = 8760)
solar_tsdata_buzios = pd.read_csv(path_2, sep = ',', skiprows = 10, nrows = 8760)
solar_tsdata_itaocara = pd.read_csv(path_3, sep = ',', skiprows = 10, nrows = 8760)
solar_tsdata_angra = pd.read_csv(path_4, sep = ',', skiprows = 10, nrows = 8760)

PVsytemPwr_niteroi = solar_tsdata_niteroi['P'].to_numpy()
PVsytemPwr_buzios = solar_tsdata_buzios['P'].to_numpy()
PVsytemPwr_itaocara = solar_tsdata_itaocara['P'].to_numpy()
PVsytemPwr_angra = solar_tsdata_angra['P'].to_numpy()



x = np.arange(504)


plt.figure(figsize = (15, 5))
plt.plot(x, PVsytemPwr_niteroi[: 504,])
plt.plot(x, PVsytemPwr_buzios[: 504,])
plt.plot(x, PVsytemPwr_itaocara[: 504,])
plt.plot(x, PVsytemPwr_angra[: 504,])
plt.title('PVPwrsystem')
plt.ylabel('Potência kW')
plt.xlabel('Hora')
plt.legend(['Niterói', 'Búzios', 'Itaocara', 'Angra'])
plt.show()

