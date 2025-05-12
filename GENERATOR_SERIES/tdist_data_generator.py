import numpy as np

"""
    Script para geração da série horária de tarifas de energia da distribuidora (TDist).
    
    Premissas:
    - Tarifas com periodização horária (tarifa branca)
    - Considera dias úteis apenas (sem diferenciação para finais de semana ou feriados)
    - Horários definidos conforme padrão da Enel (março de 2021):
        - Ponta: 18h00 às 20h59
        - Intermediário: 16h00 às 17h59 e 21h00 às 21h59
        - Fora de Ponta: 22h00 às 15h59
    - Valores das tarifas:
        - Ponta: R$1,33333/kWh
        - Intermediária: R$0,88020/kWh
        - Fora de Ponta: R$0,57060/kWh
    
    Fonte: https://www.reclameaqui.com.br/enel-distribuicao-rio/tarifa-branca_tXRUzcJG6p-KOBAL/
"""

def tdist_generator():
    """
    Gera uma série horária de tarifas da distribuidora (TDist) para um ano inteiro (8760 horas).
    """
    horas_ano = 8760  # Total de horas em um ano (365 dias x 24h)
    
    # Inicializa vetor de zeros para armazenar as tarifas por hora
    TDist_hourly_series = np.zeros(horas_ano)

    # Valores das tarifas (em R$/kWh)
    PONTA = 1.33333
    INTERMEDIARIA = 0.88020
    FORA_PONTA = 0.57060

    # Loop ao longo de cada hora do ano
    for t in range(horas_ano):
        h = t % 24  # Determina a hora do dia (0 a 23), com base no índice t

        # Define a tarifa de acordo com o horário
        if 0 <= h < 16:
            tarifa = FORA_PONTA
        elif 16 <= h < 18:
            tarifa = INTERMEDIARIA
        elif 18 <= h < 21:
            tarifa = PONTA
        elif 21 <= h < 22:
            tarifa = INTERMEDIARIA
        else:
            tarifa = FORA_PONTA

        # Armazena o valor da tarifa no vetor
        TDist_hourly_series[t] = tarifa

    # Retorna o vetor como matriz de 1 linha e 8760 colunas
    return TDist_hourly_series.reshape((1, horas_ano))


# Executa a função principal quando o script for executado diretamente
if __name__ == '__main__':
    from pathlib import Path
    import pandas as pd

    # Define o caminho do arquivo de saída na pasta 'GENERATED_SERIES'
    save_path = (Path(__file__).parent.parent / 'GENERATED_SERIES' / 'TDist_hourly_series.csv').resolve()

    # Gera a série de tarifas
    TDist_hourly_series = tdist_generator()

    # Salva a série como arquivo CSV (valores separados por ponto e vírgula, sem cabeçalho ou índice)
    pd.DataFrame(TDist_hourly_series).to_csv(save_path, sep=';', index=False, header=False)

    print('Série horária de tarifas salva com sucesso.')
