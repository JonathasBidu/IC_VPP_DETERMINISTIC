import numpy as np
import scipy.stats as stats
from WTGenPwr import WTGenPwr

''' 
    Script para geração de séries de vento a partir da obtenção dos fatores C e k junto ao CRESESB.
    Suposição: Vento tem distribuição de Weibull com fator de k e fator de escala C:f(v)=(k/C)(v/C)^(k-1)exp(-(v/C)^k) onde, v é a velocidade do vento e 
    f a função densidade de probabilidade de v.
    Fonte da obtenção dos fatores C e K: https://cresesb.cepel.br/index.php?section=atlas_eolico

    - Parâmetros de entrada (scale: list|np.ndarray, shape: list|np.ndarray, n: int):

        - scale: fator de escala da distribuição de Weibull
        - shape: fator k da distribuição de Weibull
        - n: Quantidade de usinas e cidades 

    - Retorna: -> WTGpwr_hourly_series
        
        - WTGpwr_hourly_series: Arquivo excel contendo séries históricas de um período de um ano de n cidades distintas dispostas em abas diferentes.

'''

def wind_data_generation(scale: list| np.ndarray, shape: list| np.ndarray, Npoints: int, n: int)-> np.ndarray:
        
    # Definir os parâmetros de distribuição de velocidade do vento
    wind_hourly_series = np.zeros((n, Npoints))

    dim = Npoints // 4 

    for s in range(n):
        for trimestre in range(4):
            inicio = dim * trimestre
            fim = dim * (trimestre + 1)
            a = scale[trimestre]
            b = shape[trimestre]
            wind_hourly_series[s, inicio: fim] = stats.weibull_min.rvs(b, scale = a, size = dim)

    # Parâmetros da eólica utilizados como padrão
    print('Parâmetros da UG Eólica')
    cut_in_speed = float(input('Velocidade de cut_in da turbina(m/s)[2.2]: ') or 2.2)
    cut_out_speed = float(input('Velocidade de cut_out da turbina(m/s)[25.0]: ') or 25.0)
    nom_speed = float(input('Velocidade nominal da turbina(m/s)[12.5]: ') or 12.5)
    nom_pwr = float(input('Potência nominal da turbina(W)[10MW]: ') or 10*1e6)
    Nwtg = int(input('Número de turbinas eólicas[1]: ') or 1)

    # Gerar séries temporais de potência eólica
    WTGpwr_hourly_series = np.zeros_like(wind_hourly_series)
    for s in range(n):
        for time in range(Npoints):
            speed = wind_hourly_series[s, time]
            Pwtg = WTGenPwr(speed, cut_in_speed, cut_out_speed, nom_speed, nom_pwr, Nwtg)
            WTGpwr_hourly_series[s, time] = Pwtg

    return WTGpwr_hourly_series

if __name__ == '__main__':

    import pandas as pd
    from pathlib import Path
    
    while True:
        Nwt = input('Digite a quantidade de usinas ou tecle enter para 3 usinas: ')
        if Nwt == '':
            Nwt = 3
            break
        try:
            Nwt = int(Nwt)
            if Nwt > 0:
                break
            else:
                print('Insira um valor numérico válido, inteiro e maior que zero.')
        except ValueError as v:
            print(f'Insira um valor numérico válido\nERRO, {v}')

    # Definindo um intervalo em horas
    while True:
        Npoints = input('Digite o intervalo de horas desejado ou tecle enter para 8760 horas: ')
        if Npoints == '':
            Npoints = 8760
            break
        try:
            Npoints = int(Npoints)
            if Npoints > 0:
                Npoints = Npoints
                break
            else:
                print('Insira um valor numérrico válido')
        except ValueError:
            print('Insira um valor numérico válido')

    # Definindo a quantidade de séries por usinas
    while True:
        n = input('Insira a quantidade de séries desejadas por cidade ou tecle enter para 11: ')
        if n == '':
            n = 11
            break
        try:
            n = int(n)
            if n > 0:
                n = n
                break
            else:
                print('Insira um valor numérico válido!')
        except ValueError:
            print('Insira um valor numérico válido!')
    
    #   Fatores C e k da Região de Maricá: 
    #   Para uma localização {Latitude:22,9191°  S, Longitude:42,8183° O}
    #   o valor de C e k para cada periodo do ano são:
    #       Periodo    |    C    |    k
    #       Dez-Fev    |  5.65   |  1.95
    #       Mar-Mai    |  5.37   |  1.88
    #       Jun-Ago    |  6.22   |  2.01
    #       Set-Nov    |  5.64   |  2.02
    #   Logo, pode-se adotar para scale e shape:
    #       scale = [5.65, 5.37, 6.22, 5.64]
    #       shape = [1.95, 1.88, 2.01, 2.02]

    #   Fatores C e k da Região de Búzios:	
    #   Para uma localização {Latitude:22,7481°  S, Longitude:41,8813° O}
    #   o valor de C e k para cada periodo do ano são:
    #       Periodo    |    C    |    k
    #       Dez-Fev    |  8.46   |  2.01  
    #       Mar-Mai    |  7.35   |  2.12
    #       Jun-Ago    |  8.42   |  2.40
    #       Set-Nov    |  8.38   |  2.25
    #   Logo, pode-se adotar para scale e shape:
    #       scale = [8.46, 7.35, 8.42, 8.38]
    #       shape = [2.01, 2.12, 2.40, 2.25]

    #   Fatores C e k da Região de Angra dos Reis: 	 
    #   Para uma localização {Latitude:23,01°  S, Longitude:44,3184° O}
    #   o valor de C e k para cada periodo do ano são:
    #       Periodo    |    C    |    k
    #       Dez-Fev    |  3.90   |  1.70  
    #       Mar-Mai    |  3.93   |  1.78
    #       Jun-Ago    |  5.15   |  1.87
    #       Set-Nov    |  4.54   |  1.92
    #   Logo, pode-se adotar para scale e shape:
    #       scale = [3.90, 3.93, 5.15, 4.54]
    #       shape = [1.70, 1.78, 1.87, 1.92]

    # Fatores C e K da Região de Volta Redonda:
    # Para uma localização {Latitude: 22,5252°  S, Longitude: 44,1038° O}
    #   o valor de C e k para cada periodo do ano são:
    #       Periodo    |    C    |    k
    #       Dez-Fev    |  3.27   |  1.80  
    #       Mar-Mai    |  3.00   |  1.80
    #       Jun-Ago    |  3.89   |  1.95
    #       Set-Nov    |  3.38   |  1.82
    #   Logo, pode-se adotar para scale e shape:
    #       scale = [3.27, 3.00, 3.89, 3.38]
    #       shape = [1.80, 1.80, 1.95, 1.82]

    # Fatores C e K da Região de Campos dos Goytacazes:
    # Para uma localização {Latitude: 21,7545°  S, Longitude: 41,3244° O}
    #   o valor de C e k para cada periodo do ano são:
    #       Periodo    |    C    |    k
    #       Dez-Fev    |  5.22   |  1.80  
    #       Mar-Mai    |  4.81   |  1.80
    #       Jun-Ago    |  5.35   |  1.95
    #       Set-Nov    |  5.64   |  1.82
    #   Logo, pode-se adotar para scale e shape:
    #       scale = [5.22, 4.81, 5.35, 5.64]
    #       shape = [2.26, 2.31, 2.31, 2.31]


    save_path = Path(__file__).parent.parent / 'GENERATED_SERIES' / 'WTGsystem_hourly_series.xlsx'

    with pd.ExcelWriter(save_path) as writer:
        for i in  range(Nwt):

            # Solicitando uma das regiões acima
            while True:
                regiao = input('escolha a região (1 para Maricá, 2 para Búzios, 3 para Campos dos Goytacazes, 4 para Volta Redonda ou 5 para Angra dos Reis): ')
                if regiao in ['1', '2', '3', '4', '5']:
                    regiao = int(regiao)
                    break
                else:
                    print('Escolha inválida. Digite 1, 2, 3, 4 ou 5.')
        
            if regiao == 1:
                # Maricá
                scale = [5.65, 5.37, 6.22, 5.64]
                shape = [1.95, 1.88, 2.01, 2.02]
                name = 'Maricá'
                
            elif regiao == 2:
                # Búzios
                scale = [8.46, 7.35, 8.42, 8.38]
                shape = [2.01, 2.12, 2.40, 2.25]
                name = 'Búzios'

            elif regiao == 3:
                # Campos dos goytacazes
                scale = [5.22, 4.81, 5.35, 5.64]
                shape = [2.26, 2.31, 2.31, 2.31]
                name = 'Campos dos Goytacazes'

            elif regiao == 4:
                # Volta Redonda
                scale = [3.27, 3.00, 3.89, 3.38]
                shape = [1.80, 1.80, 1.95, 1.82]
                name = 'Volta Redonda'

            else:
                # Angra dos Reis
                scale = [3.90, 3.93, 5.15, 4.54]
                shape = [1.70, 1.78, 1.87, 1.92]
                name = 'Angra dos Reis'

            WTG_horly_series = wind_data_generation(scale, shape, Npoints, n)
            WTG_horly_series_df = pd.DataFrame(WTG_horly_series)
            WTG_horly_series_df.to_excel(writer, sheet_name = name, header = None, index = False)
    
    print('FIM')