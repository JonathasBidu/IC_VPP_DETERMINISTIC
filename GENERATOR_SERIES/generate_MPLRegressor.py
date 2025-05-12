import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

"""
    Função para construção de um modelo preditivo usando uma Rede Neural do tipo MLP (Multi-Layer Perceptron)
    para séries temporais.

    Parãmetros:
        - Z: Lista ou vetor 1D com a série temporal.
        - p: Número de defasagens (lags) a serem usadas como entrada. Default: 2

    Retorno:
        - p: Lag utilizado
        - model: Objeto MLP treinado
        - Y: Série original (a partir da posição p)
        - Yhat: Série predita pelo modelo
"""
def generate_MLP(Z: list)-> tuple:

    while True:
        p = input('Insira o número de lags ou tecle enter para 2: ')
        if p == '':
            p = 2
            break
        try:
            p = int(p)
            if p > 0:
                p = p
                break
            else:
                print('Insira um valor numérico válido!')
        except ValueError as v:
            print(f'Insira um valor numérico válido! {v}')

    # Obtendo o tamanho do vetor Z
    N = len(Z)
    # Iniciando a matriz de entrada "X" e o vetor de saída "Y" que será utilizado no modelo a seguir
    X = np.zeros((N - p, p))
    Y = np.zeros((N - p, ))

    # separando os dados de entrada e os dados de saída para o modelo de RNA que será implementado a seguir.
    # Entrada = y(t) para y(t-p), t = p + 1 : T
    # Saída = y(t + 1), t = p + 1 : T
    for k in range(p, N):
        X[k - p, : ] = Z[k - p : k].flatten()
        Y[k - p] = Z[k]   
    
    """
    Criando a arquitetura RNA atravéz do modelo MPLRegressor onde, MPL(Multi-Layer Perception) modelo de multi-camadas de neurônios Perception e Regressor é uma classe da biblioteca sklearn que utiliza a regressão e o solucionador "adam" para ajustar os pesos e bias. 
    *** Método 'adam' (Adaptive Moment Estimation)

    Descrição:
    O método 'adam' é um otimizador amplamente utilizado em algoritmos de aprendizado de máquina, especialmente em redes neurais. Ele combina características de otimizadores de momento e taxa de aprendizado adaptativa para eficientemente minimizar a soma dos quadrados dos resíduos entre uma função modelada e os dados observados.

    Funcionamento:
    1. Inicialização: O método inicia com uma estimativa inicial dos parâmetros a serem otimizados.
    2. Iteração: Utiliza uma combinação adaptativa de descida do gradiente e algoritmo de momento para ajustar iterativamente os parâmetros.
    3. Taxa de Aprendizado Adaptativa: A técnica ajusta dinamicamente a taxa de aprendizado para cada parâmetro, proporcionando convergência eficiente.

    Parâmetros:
    - Função a ser otimizada: Deve ser fornecida a função que calcula os resíduos a serem minimizados.
    - Parâmetros iniciais: Lista dos valores iniciais para os parâmetros a serem otimizados.
    - Limites dos parâmetros: Pode ser especificado um intervalo permitido para cada parâmetro.
    - Tolerância: Define a precisão desejada para a solução, indicando a convergência.
    - Beta1 e Beta2: Parâmetros que controlam as médias móveis exponenciais de gradientes e quadrados de gradientes, respectivamente.
    - Epsilon: Pequeno valor adicionado para evitar divisões por zero na adaptação da taxa de aprendizado.

    Nota: O método 'adam' é particularmente eficaz em problemas de grande escala e variabilidade na escala dos gradientes.
    """

    model = MLPRegressor(hidden_layer_sizes = (100, 100, 50),
                        solver = 'adam',
                        max_iter = 10000,
                        learning_rate = 'adaptive',
                        learning_rate_init = 0.01,
                        tol = 1e-4,
                        alpha = 1e-4
                        # verbose = True
                        )
    
    # treinando o modelo onde, X é a matriz de entrada e Y é a matriz de saída
    model.fit(X, Y)
    # obtendo a previsão 
    Yhat = model.predict(X)
    # performace do modelo
    perf = mean_squared_error(Y, Yhat)
    # Obtendo coeficiente de determinação R² da previsão, R² é uma métrica que varia de 0 a 1, quanto mais próximo de 1 indica um ajuste melhor do modelo
    metric = model.score(X, Y)
    print(f'O desempenho do modelo em termos de erro médio quadrático foi: {perf:.3f}')
    print(f'O ajuste geral do modelo aos dados usando o coeficiênte de determinação R² foi: {metric:.3f}')

    return p, model, Y, Yhat