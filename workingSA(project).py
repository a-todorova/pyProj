import numpy as np
import matplotlib.pyplot as plt
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.visualization.scatter import Scatter
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling

#Adjusted original code
'''
class MOK(Problem):
    def __init__(self,
                 n_items,  # number of items that can be picked up
                 W,  # weights for each item
                 P,  # profit of each item
                 C,  # maximum capacity
                 ):
        super().__init__(n_var=n_items, n_obj=2, n_ieq_constr=1, xl=0, xu=1, vtype=bool)

        self.W = W
        self.P = P
        self.C = C

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = - np.sum(self.P * x, axis=1)
        f2 = np.sum(x, axis=1)

        out["F"] = np.column_stack([f1, f2])
        out["G"] = (np.sum(self.W * x, axis=1) - self.C)

'''


# define the multi-objective knapsack problem
class MultiObjectiveKnapsack(Problem):
    def __init__(self, num_items, weights, values, max_weight):
        super().__init__(n_var=num_items, n_obj=2, n_constr=1, xl=0, xu=1, type_var=np.bool_)
        self.weights = weights
        self.values = values
        self.max_weight = max_weight

    def _evaluate(self, x, out, *args, **kwargs):
        # Objective 1: Maximize value
        f1 = np.sum(self.values * x, axis=1)

        # Objective 2: Minimize weight
        f2 = np.sum(self.weights * x, axis=1)

        # Constraint: Weight must not exceed the max_weight
        g1 = f2 - self.max_weight

        # set objectives and constraints
        out["F"] = np.column_stack([-f1, f2])  # Maximizing f1, so use -f1 for minimization
        out["G"] = g1

# Problem setup
num_items = 100  # Number of items
weights = np.random.randint(1, 20, num_items)  # Random weights for items
values = np.random.randint(1, 20, num_items)  # Random values for items
max_weight = 300  # Maximum weight capacity of the knapsack

#problem = MultiObjectiveKnapsack(num_items, weights, values, max_weight)
problem = MultiObjectiveKnapsack(num_items, weights, values, max_weight)

# set NSGA-II algorithm
algorithm = NSGA2(pop_size=100,
                  sampling=IntegerRandomSampling(),
                  crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                  mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
                  eliminate_duplicates=True,)

# termination condition after n generations
termination = get_termination("n_gen", 10)

# Optimize the problem
res = minimize(problem, algorithm, termination, pf=problem.pareto_front(), seed=1, verbose=True)

# Plot the graph
Scatter(title="Results for Multi-objective Knapsack Problem (terminal)").add(res.F).show()

# cant see graph (from terminal), so save it as png
#plot = Scatter(title="Result for Multi-objective Knapsack Problem")
#plot.add(res.F)
print(res.F, res.G)
#plot.save("result.png")
