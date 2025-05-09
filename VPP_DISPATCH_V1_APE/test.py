# from pymoo.algorithms.soo.nonconvex.ga import GA
# from pymoo.problems import get_problem
# from pymoo.optimize import minimize
# from pymoo.termination.cv import ConstraintViolationTermination
# from pymoo.termination.robust import RobustTermination

# problem = get_problem("g5")
# algorithm = GA(pop_size=100)

# res = minimize(problem,
#                algorithm,
#                RobustTermination(ConstraintViolationTermination(), period=30),
#                return_least_infeasible=True,
#                seed=1,
#                verbose=True)

# print(res.CV[0])
# print(res.F[0])
# print(res.X)

# from pymoo.algorithms.moo.nsga2 import NSGA2
# from pymoo.problems import get_problem
# from pymoo.optimize import minimize
# from pymoo.visualization.scatter import Scatter

# problem = get_problem("zdt6")

# algorithm = NSGA2(pop_size=100)

# res = minimize(problem,
#                algorithm,
#                ("n_gen", 300),
#                seed=1,
#                progress=True)

# plot = Scatter()
# plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
# plot.add(res.F, facecolor="none", edgecolor="red")
# plot.show()

# from pymoo.algorithms.soo.nonconvex.ga import GA
# from pymoo.problems import get_problem
# from pymoo.optimize import minimize
# from pymoo.termination.default import DefaultSingleObjectiveTermination

# problem = get_problem("g5")
# algorithm = GA(pop_size=100)
# termination = DefaultSingleObjectiveTermination()

# res = minimize(problem,
#                algorithm,
#                termination,
#                return_least_infeasible=True,
#                pf=None,
#                seed=1,
#                verbose=True)

# print("n_gen: ", res.algorithm.n_gen)
# print("CV: ", res.CV[0])
# print("F: ", res.F[0])

# from pymoo.algorithms.soo.nonconvex.pso import PSO
# from pymoo.optimize import minimize
# from pymoo.problems.single import Sphere
# from pymoo.termination.fmin import MinimumFunctionValueTermination

# problem = Sphere()

# algorithm = PSO()

# termination = MinimumFunctionValueTermination(1e-5)

# res = minimize(problem,
#                algorithm,
#                termination,
#                pf=problem.pareto_front(),
#                seed=1,
#                verbose=True)

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.termination.ftol import SingleObjectiveSpaceTermination
from pymoo.termination.robust import RobustTermination

problem = get_problem("rastrigin")
algorithm = GA(pop_size=100)
termination = RobustTermination(SingleObjectiveSpaceTermination())

res = minimize(problem,
               algorithm,
               termination,
               pf=problem.pareto_front(),
               seed=1,
               verbose=True)

print(res.opt.get("F"))