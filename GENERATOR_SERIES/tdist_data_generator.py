import numpy as np

# Este script gera tarifas de energia para distribuidora e consumidores
# Premissas:
    # Periodização horaria
    # Hora zero - 1o. registo dos dados
    # Desconsidera feriados e finais de semana
    # Horario de Ponta: 18h - 20h59 (dias uteis de segunda a sexta)
    # Horario Intermediário: 16h - 17h59 e 21h - 21h59h
    # Horario Fora de Ponta: 22h - 15h59h
    # Fonte: https://www.reclameaqui.com.br/enel-distribuicao-rio/tarifa-branca_tXRUzcJG6p-KOBAL/
    # Valor Enel Março 21
        # PONTA = R$1.33333
        # INTERMEDIÁRIA = R$0.88020
        # FORA PONTA = R$0.57060

def tdist_generator():

    horas_ano = 8760 # total de horas
    TDist_hourly_series = np.zeros(horas_ano)
    horas_dia = 24

    PONTA = 1.33333
    INTERMEDIARIA = 0.88020
    FORA_PONTA = 0.57060


    # Gerar a série horária de tarifas
    for t in range(horas_ano):
        h = t % 24  # Obter a hora do dia (0 - 23)
        if 0 <= h < 16:
            TDist_hourly_series[t] = FORA_PONTA
        elif 16 <= h < 18:
            TDist_hourly_series[t] = INTERMEDIARIA
        elif 18 <= h < 21:
            TDist_hourly_series[t] = PONTA
        elif 21 <= h < 22:
            TDist_hourly_series[t] = INTERMEDIARIA
        else:
            TDist_hourly_series[t] = FORA_PONTA
    
    TDist_hourly_series = TDist_hourly_series.reshape((1, horas_ano))

    return TDist_hourly_series

if __name__ == '__main__':

    from pathlib import Path
    import pandas as pd

    save_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'TDist_hourly_series.csv'

    TDist_hourly_series = tdist_generator()

    # Salvar o DataFrame em um arquivo CSV, Excel ou outro formato
    TDist_hourly_series_df = pd.DataFrame(TDist_hourly_series)
    TDist_hourly_series_df.to_csv(save_path, sep = ';', index = False, header = None)

    print('FIM')
 