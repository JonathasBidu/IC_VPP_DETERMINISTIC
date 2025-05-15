from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from objetive_function import obj_function
from ieq_constraints import ieq_constr
from eq_constraints import eq_constr
from get_limits import bounds
from pymoo.optimize import minimize

from pymoo.config import Config
Config.warnings['not_compiled'] = False

'''
    Este script implementa um otimizador baseado no Algoritmo Genético (GA) para maximizar o lucro de uma Virtual Power Plant (VPP).

    -> Parâmetros de Entrada:
        - data (dict): Dicionário com os dados iniciais e projeções temporais da VPP:
            - Nt: Número de períodos de simulação.
            - Ndl: Quantidade de cargas despacháveis.
            - Nbm: Quantidade de usinas de biomassa (UBTM).
            - Nbat: Quantidade de armazenadores de energia.

    -> Processo:
        1. Definição do Problema: O problema é modelado como um problema de otimização interira mista de múltiplas variáveis, com variáveis contínuas (potências, carga, e tarifas) e variáveis inteiras (estados de operação).
        2. Restrições: São aplicadas restrições de igualdade e desigualdade, incluindo capacidade de geração, estados de carga e operação das usinas.
        3. Função Objetivo: A função objetivo busca maximizar o lucro da VPP, calculando os custos e receitas de operação.
        4. Otimização: O GA é utilizado para encontrar as soluções ótimas, considerando penalidades para restrições violadas.

    -> Saída:
        - res (Result): Resultado da otimização contendo as variáveis de decisão otimizadas (potências, estados de carga, etc.) e o valor da função objetivo (lucro).

    -> Dependências:
        - pymoo: Framework de otimização para resolução de problemas de otimização de múltiplos objetivos.
        - objetive_function: Função objetivo para cálculo do lucro.
        - ieq_constr: Restrições de desigualdade.
        - eq_constr: Restrições de igualdade.
        - get_limits: Função para obter os limites das variáveis de decisão.
'''

def solver(data: dict):

    # Parâmetros iniciais da VPP
    Nt = data['Nt'] # Período da simulação da VPP
    Ndl = data['Ndl'] # Quantidade de cargas despacháveis da VPP
    Nbm = data['Nbm'] # Quantidade de UBTMs da VPP
    Nbat = data['Nbat'] # Quantidade de armazenadores da VPP

    # Variáveis reais: p_bm, p_chg, p_dch, soc, p_dl
    Nr = (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nbat * Nt) + (Nt * Ndl)
    # Variáveis inteiras: u_bm, u_chg, u_dch, u_dl
    Ni = (Nt * Nbm) + (Nt * Nbat) + (Nt * Nbat) + (Nt * Ndl)
    # Definido a quantidade de variáveis
    nvars = Nr + Ni

    # Definindo a quantidade de restrições de igualdade da VPP
    Nsoc = (Nbat * Nt) # Quantidade restrições de igualdade do estado de carga dos armazenadores da VPP
    c_eq = Nsoc # Total de restrições de igualdade da VPP

    # Definindo a quantidade de restrições de desigualdades da VPP
    Nbmc =(Nbm * Nt) + (Nbm * Nt) + (Nbm * (Nt - 1)) + (Nbm * (Nt - 1)) # Quantidade de restrições de desigualdade da VPP
    Nbatc = (Nbat * Nt) + (Nbat * Nt) + (Nbat * Nt) # Quantidade de restrições de desigualdade dos armazenadores da VPP
    Ndlc = (Ndl * Nt) + (Ndl * Nt)# Quantidade de restrições de desigualdade das cargas despacháveis da VPP
    c_ieq = Nbmc + Nbatc + Ndlc # Total de restrições de desigualdade da VPP

    # Obtendo os limites superior (ub) e inferior (lb) das variáveis de decisão
    ub, lb = bounds(data)

    # Criando uma classe que define o problema
    class MyProblem(ElementwiseProblem):

        def __init__(self, data: dict, **kwargs):
            super().__init__(data, **kwargs)
            self.data = data # Atribuindo o dicionário data a classe

        def _evaluate(self, x, out, *args, **kwargs):

            out['F'] = - obj_function(x, self.data)
            out['G'] = ieq_constr(x, self.data)
            out['H'] = eq_constr(x, self.data)

    # Instanciando a classe problema
    problem = MyProblem(data,
                        n_obj = 1,
                        n_var = nvars,
                        n_eq_constr = c_eq,
                        n_ieq_constr = c_ieq,
                        xu = ub,
                        xl = lb
                        )
    
    from pymoo.termination.ftol import SingleObjectiveSpaceTermination
    from pymoo.constraints.as_penalty import ConstraintsAsPenalty
    from pymoo.termination.robust import RobustTermination
    from pymoo.termination.default import DefaultSingleObjectiveTermination
    from pymoo.constraints.eps import AdaptiveEpsilonConstraintHandling

    # Aplicando penalidades as restrições do problema
    problem = ConstraintsAsPenalty(problem, penalty = 100.0)

    # Definindo o algoritmo 
    # algorithm = GA(pop_size = 100, eliminate_duplicates = True)
    algorithm = AdaptiveEpsilonConstraintHandling(GA(pop_size = 50, eliminate_duplicates = True), perc_eps_until = 0.5)

    # Definindo quando o algoritmo deve parar
    # termination = RobustTermination(SingleObjectiveSpaceTermination(tol = 0.1), period = 15)
    # termination = DefaultSingleObjectiveTermination(xtol = 0.01, cvtol = 0.01, ftol = 0.01, period = 15)
    # termination = SingleObjectiveSpaceTermination()
    termination = ('n_gen', 50)

    res = minimize(problem,
                   algorithm,
                   termination,
                   return_least_infeasible = True,
                   seed = 1,
                   verbose = True,
                   progress = True
                   )


    return res
