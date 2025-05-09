import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

path_1 = Path(__file__).parent / "DATA_BASE" / 'solar_time_series_angra_dos_reis.csv'
path_2 = Path(__file__).parent / "DATA_BASE" / 'solar_time_series_niteroi.csv'
path_3 = Path(__file__).parent / "DATA_BASE" / 'solar_time_series_itaocara.csv'
path_4 = Path(__file__).parent / "DATA_BASE" / 'solar_time_series_buzios.csv'

angra_tsdata = pd.read_csv(path_1, skiprows = 10, sep = ',', nrows = 8760)
niteroi_tsdata = pd.read_csv(path_2, skiprows = 10, sep = ',', nrows = 8760)
itaocara_tsdata = pd.read_csv(path_3, skiprows = 10, sep = ',', nrows = 8760)
buzios_tsdata = pd.read_csv(path_4, skiprows = 10, sep = ',', nrows = 8760)

angra_tsdata = angra_tsdata['P'].to_numpy()
niteroi_tsdata = niteroi_tsdata['P'].to_numpy()
itaocara_tsdata = itaocara_tsdata['P'].to_numpy()
buzios_tsdata= buzios_tsdata['P'].to_numpy()

Npoints = 8760

while True:

    N = input('Insira a quantidade de séries solar desejada ou tecle enter para 11 séries: ' )
    if N == '':
        N = 11
    try:
        N = int(N)
        if N > 0:
            break
        else:
            print('Insira um valor inteiro e positivo')
    except ValueError as v:
        print('Insira um valor numérico válido {v}')

PVSystem_hourly_series_angra = np.zeros((N, Npoints))
PVSystem_hourly_series_niteroi = np.zeros((N, Npoints))
PVSystem_hourly_series_itaocara = np.zeros((N, Npoints))
PVSystem_hourly_series_buzios = np.zeros((N, Npoints))

for i in range(N):
    for tsdata, output_array in [
        (angra_tsdata, PVSystem_hourly_series_angra),
        (niteroi_tsdata, PVSystem_hourly_series_niteroi),
        (itaocara_tsdata, PVSystem_hourly_series_itaocara),
        (buzios_tsdata, PVSystem_hourly_series_buzios),
    ]:
        # Ruído proporcional à geração original
        scale_mult = 0.03 * tsdata
        scale_add = 0.02 * np.max(tsdata)
        noise = np.random.normal(scale=1.0, size=8760) * (scale_mult + scale_add)

        # Aplica ruído apenas onde a geração original é positiva
        simulated = tsdata.copy()
        simulated[tsdata > 0] += noise[tsdata > 0]

        # Garante que não existam valores negativos
        simulated = np.clip(simulated, 0, None)

        output_array[i, :] = simulated


# Defina o intervalo desejado (por exemplo, uma semana: hora 168 a 336)
start = 168
end = 336

plt.figure(figsize=(14, 10))

# Angra dos Reis
plt.subplot(2, 2, 1)
plt.plot(PVSystem_hourly_series_angra[0, start:end], label='Simulada Angra')
plt.plot(angra_tsdata[start:end], label='Original Angra', linestyle='--')
plt.title('Angra dos Reis')
plt.legend()

# Niterói
plt.subplot(2, 2, 2)
plt.plot(PVSystem_hourly_series_niteroi[0, start:end], label='Simulada Niterói')
plt.plot(niteroi_tsdata[start:end], label='Original Niterói', linestyle='--')
plt.title('Niterói')
plt.legend()

# Itaocara
plt.subplot(2, 2, 3)
plt.plot(PVSystem_hourly_series_itaocara[0, start:end], label='Simulada Itaocara')
plt.plot(itaocara_tsdata[start:end], label='Original Itaocara', linestyle='--')
plt.title('Itaocara')
plt.legend()

# Búzios
plt.subplot(2, 2, 4)
plt.plot(PVSystem_hourly_series_buzios[0, start:end], label='Simulada Búzios')
plt.plot(buzios_tsdata[start:end], label='Original Búzios', linestyle='--')
plt.title('Búzios')
plt.legend()

plt.tight_layout()
plt.show()


# Teste de uso
if __name__ == '__main__':

    output_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'PVGISSystem_hourly_series.xlsx'

    # Criando uma planilha do tipo xlsx
    with pd.ExcelWriter(output_path) as writer:

        angra_time_series = pd.DataFrame(PVSystem_hourly_series_angra)
        niteroi_time_series = pd.DataFrame(PVSystem_hourly_series_niteroi)
        itaocara_time_series = pd.DataFrame(PVSystem_hourly_series_itaocara)
        buzios_time_series = pd.DataFrame(PVSystem_hourly_series_buzios)
        angra_time_series.to_excel(writer, sheet_name = 'Angra dos Reis', index = False, header = None)
        niteroi_time_series.to_excel(writer, sheet_name = 'Niterói', index = False, header = None)
        itaocara_time_series.to_excel(writer, sheet_name = 'Búzios', index = False, header = None)
        buzios_time_series.to_excel(writer, sheet_name = 'Itaocara', index = False, header = None)

