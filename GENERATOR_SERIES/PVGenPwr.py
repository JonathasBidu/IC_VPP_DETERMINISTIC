import numpy as np
from scipy.optimize import root

"""
    Calcula a potência máxima de geração fotovoltaica (MPPT).
    Parâmetros:
    - G: Irradiância solar (W/m^2).
    - T: Temperatura ambiente (K).
    - Np: Número de células em paralelo.
    - Ns: Número de células em série.
    Retorna uma tupla (Pmpp, Vmpp, Impp) com a potência máxima, tensão e corrente correspondentes. 
"""

def PVGenPwr(G: float, T: float, Np: int, Ns: int)-> tuple:
    kB = 1.380649e-23 # Constante de Boltzmann 
    q = 1.60217663e-19 # Carga do elementar
    # Parametros das células fotovoltaícas
    K0 = -5.729e-7
    K1 = -0.1098
    K2 = 44.5355
    K3 = -1.264e4
    K4 = 11.8003
    K5 = -7.3174e3
    K6 = 2.0000
    K7 = 0.0000
    K8 = 1.47
    K9 = 1.6126e3
    K10 = -4.474e-3
    K11 = 2.303e6
    K12 = -2.812e-2

    # Paramêtros do modelo de diodo
    Iph = K0 * G * (1 + K1 * T) # Corrente 
    Is1 = K2 * (T**3) * np.exp(K3 / T) # Corrente de saturação 1
    Is2 = K4 * (T ** (3/ 2)) * np.exp(K5 / T) # Corrente de saturação 2
    A = K6 + K7 * T # Fator de idealidade https://en.wikipedia.org/wiki/Shockley_diode_equation

    # Cálculo da resitência em paralelo
    Rp = K11 * np.exp(K12 * T) 
    
    # Cálculo da resistência em série
    if G == 0:
         # Para G == 0 tem se Iph = 0, Rs = inf e portanto I = 0 para qualquer V. Não é possível determinar o valor de V a partir do modelo sem o diodo apenas. Por outro lado a potência produzida pelas células fotovoltaicas será sempre nula.
        # Potência máxima
        Pmpp = 0.0
        # Tensão correspondente a maior potência
        Vmpp = None
        # Corrente correspondente a maior potência
        Impp = 0.0
    else:
        Rs = K8 + (K9 / G) + (K10 * T) 
        # Modelo do sistema fotovoltaico
        def f(V: float, I: float)-> float:
            I1a = (V * q) / (Ns * kB * T) # primeira parcela do primeiro termo
            I1b = (I * Rs * q) / (Np * kB * T) # segunda parcela do segundo termo
            I1c = np.exp(I1a) # exponencial da primeira parcela
            I1d = np.exp(I1b) # exponecial da segunda parcela
            I2a = (V * q) / (Ns * A * kB * T) # primeira parcela do segundo termo
            I2b = (I * Rs * q) / (Np * A * kB * T) # segunda parcela do segundo termo
            I2c = np.exp(I2a) # exponecial da primeira parcela do seggundo termo
            I2d = np.exp(I2b) # exponecial da segunda parcela do segundo termo
            I1 = Is1 * ((I1c * I1d) - 1) # Primeira parcela 
            I2 = Is2 * ((I2c * I2d) - 1) # Segunda parcela
            I3 = (((V / Ns) + (I / Np) * Rs) / Rp) # terceira parcela 
            I4 = Iph - I1 - I2 - I3 # Equação principal
            return Np * I4

        # Modelo de circuito aberto do sistema fotovoltaico V = Voc, I = 0.0
        def Foc(Voc: float)-> float:
            return f(Voc, 0.0) 

        """
            *** Método 'lm' (Levenberg-Marquardt)
             método 'lm' é uma técnica de otimização não linear frequentemente utilizada para encontrar os parâmetros que minimizam a soma dos quadrados dos resíduos entre uma função modelada e os dados observados.

            *** Descrição
            O método 'lm' utiliza a abordagem de Levenberg-Marquardt para encontrar uma solução eficiente para problemas de otimização não linear. Ele combina métodos de descida do gradiente e Gauss-Newton, adaptando-se dinamicamente durante o processo iterativo para otimizar a convergência.

            *** Funcionamento
             1.Inicialização: O método inicia com uma estimativa inicial dos parâmetros a serem otimizados.
             2.Iteração: Utiliza uma combinação ponderada de descida do gradiente e Gauss-Newton para ajustar iterativamente os          parâmetros.
             3.Adaptação Dinâmica: A técnica ajusta dinamicamente a ponderação entre os métodos, favorecendo um ou outro com base no progresso da otimização.

            *** Parâmetros
            *Função a ser otimizada: Deve ser fornecida a função que calcula os resíduos a serem minimizados.
            *Parâmetros iniciais: Lista dos valores iniciais para os parâmetros a serem otimizados.
            *Limites dos parâmetros: Pode ser especificado um intervalo permitido para cada parâmetro.
            *Tolerância: Define a precisão desejada para a solução, indicando a convergência.
            *Método de Jacobiano: Define como o Jacobiano (derivadas parciais) é calculado, com opções como '2-point', '3-point', ou fornecendo uma função.
        """
        method = 'lm'

        # Obtendo V 
        result = root(Foc, 0.0, method = method)
        Voc = result.x

        # Algoritmo MPPT
        N = 1000
        # Criando um vetor de tensão igualmente espaçado desde 0.0 até Voc com N = 1000 espaços
        v = np.linspace(0.0, Voc, N).flatten()
        # Criando um vetor de corrente com as mesmas carcterísticas de v porém com elementos zero
        i = np.zeros_like(v)
        # Criando um vetor potência com as mesmas carcterísticas de v porém com elementos zero
        p = np.zeros_like(v)

        # Obtendo os primeiros elementos dos vetores
        def F(x):
            return f(v[0], x)

        x = root(F, 0.0, method = method).x
        i[0] = x
        p[0] = v[0] * i[0]

        # Obtendo os demais elementos dos vetores
        for j in range(1, N):
            def F(x):
                return f(v[j], x)

            x = root(F, 0.0, method = method).x
            i[j] = x
            p[j] = v[j] * i[j]

            if abs(p[j]) < abs(p[j - 1]):
                break

        # Obtendo o índice do maior valor encontrado
        max_j = np.argmax(p)
        # Potência máxima
        Pmpp = p[max_j]
        # Tensão correspondente a maior potência
        Vmpp = v[max_j]
        # Corrente correspondente a maior potência
        Impp = i[max_j]
    return (Pmpp, Vmpp, Impp)


# import numpy as np
# from scipy.optimize import root

# def PVGenPwr(G: float, T: float, Np: int, Ns: int) -> tuple:
#     kB = 1.380649e-23  # Constante de Boltzmann 
#     q = 1.60217663e-19  # Carga do elétron

#     # Parâmetros das células fotovoltaicas
#     K0 = -5.729e-7
#     K1 = -0.1098
#     K2 = 44.5355
#     K3 = -1.264e4
#     K4 = 11.8003
#     K5 = -7.3174e3
#     K6 = 2.0000
#     K7 = 0.0000
#     K8 = 1.47
#     K9 = 1.6126e3
#     K10 = -4.474e-3
#     K11 = 2.303e6
#     K12 = -2.812e-2

#     # Parâmetros do modelo de diodo
#     Iph = K0 * G * (1 + K1 * T)  # Corrente de fotocorrente
#     Is1 = K2 * (T**3) * np.exp(K3 / T)  # Corrente de saturação 1
#     Is2 = K4 * (T ** (3 / 2)) * np.exp(K5 / T)  # Corrente de saturação 2
#     A = K6 + K7 * T  # Fator de idealidade

#     # Cálculo da resistência em paralelo
#     Rp = K11 * np.exp(K12 * T) 

#     # Cálculo da resistência em série
#     if G == 0:
#         # Para G == 0, Iph = 0, Rs = inf, I = 0 para qualquer V. A potência máxima é 0.
#         Pmpp = 0.0
#         Vmpp = None
#         Impp = 0.0
#     else:
#         Rs = K8 + (K9 / G) + (K10 * T)

#         # Modelo do sistema fotovoltaico
#         def f(V: float, I: float) -> float:
#             I1a = (V * q) / (Ns * kB * T)
#             I1b = (I * Rs * q) / (Np * kB * T)
#             I1c = np.exp(I1a)
#             I1d = np.exp(I1b)
#             I2a = (V * q) / (Ns * A * kB * T)
#             I2b = (I * Rs * q) / (Np * A * kB * T)
#             I2c = np.exp(I2a)
#             I2d = np.exp(I2b)
#             I1 = Is1 * (I1c * I1d - 1)
#             I2 = Is2 * (I2c * I2d - 1)
#             I3 = (V / Ns + I / Np * Rs) / Rp
#             I4 = Iph - I1 - I2 - I3
#             return Np * I4

#         # Modelo de circuito aberto do sistema fotovoltaico
#         def Foc(Voc: float) -> float:
#             return f(Voc, 0.0) 

#         # Encontrando Voc usando o método 'lm' (Levenberg-Marquardt)
#         result = root(Foc, 0.0, method='lm')
#         Voc = result.x[0]

#         # Algoritmo MPPT
#         N = 1000
#         v = np.linspace(0.0, Voc, N)
#         i = np.zeros_like(v)
#         p = np.zeros_like(v)

#         # Obtendo os valores de corrente para cada tensão
#         def F(x, V):
#             return f(V, x)

#         i[0] = root(lambda x: F(x, v[0]), 0.0, method='lm').x[0]
#         p[0] = v[0] * i[0]

#         for j in range(1, N):
#             i[j] = root(lambda x: F(x, v[j]), 0.0, method='lm').x[0]
#             p[j] = v[j] * i[j]
            
#             if p[j] < p[j - 1]:
#                 break

#         max_j = np.argmax(p)
#         Pmpp = p[max_j]
#         Vmpp = v[max_j]
#         Impp = i[max_j]

#     return Pmpp, Vmpp, Impp