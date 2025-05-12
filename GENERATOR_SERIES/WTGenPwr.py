def WTGenPwr(speed, cut_in_speed, cut_out_speed, nom_speed, nom_pwr, Nwtg):
    
    """
        Calcula a potência gerada por uma turbina eólica com base na velocidade do vento e parâmetros da turbina.
        
        Esta função segue o modelo de curva de potência de turbina eólica, considerando:
            - Velocidade do vento
            - Velocidades de corte (cut-in e cut-out)
            - Velocidade nominal e potência nominal
        
        A potência gerada pela turbina depende da velocidade do vento e da resposta dinâmica da turbina entre essas velocidades.

        Referência do modelo:
            - Hadayeghparast, S., SoltaniNejad Farsangi, A., & Shayanfar, H. (2019). 
            "Day-ahead stochastic multi-objective economic/emission operational scheduling of a large scale virtual power plant." 
            *Energy (Oxford, England), 172*, 630-646. 
            [DOI: 10.1016/j.energy.2019.01.143](https://doi.org/10.1016/j.energy.2019.01.143
        
        Parâmetros:
            speed (float): Velocidade do vento (em m/s).
            cut_in_speed (float): Velocidade de corte-in da turbina (em m/s), abaixo da qual a turbina não gera potência.
            cut_out_speed (float): Velocidade de corte-out da turbina (em m/s), acima da qual a turbina para de gerar potência.
            nom_speed (float): Velocidade nominal da turbina (em m/s), onde a turbina atinge sua potência máxima.
            nom_pwr (float): Potência nominal da turbina (em W), potência máxima gerada pela turbina.
            Nwtg (int): Número de turbinas eólicas no sistema.
        
        Retorna:
            float: Potência total gerada pelo sistema de turbinas eólicas (em W).
    """

    if speed < cut_in_speed:
        Pwtg = 0
    elif cut_in_speed <= speed < nom_speed:
        Pwtg = nom_pwr * ((speed - cut_in_speed) / (nom_speed - cut_in_speed))**3
    elif nom_speed <= speed < cut_out_speed:
        Pwtg = nom_pwr
    elif cut_out_speed <= speed:
        Pwtg = 0    

    return Nwtg * Pwtg