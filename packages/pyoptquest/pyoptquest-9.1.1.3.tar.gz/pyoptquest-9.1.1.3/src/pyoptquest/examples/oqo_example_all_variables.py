import numpy as np

from pyoptquest import OptQuestOptimizer

# define the input(s)
search_space = {
    'continuous_var': {'type': 'continuous', 'min': -5, 'max': 5},
    'discrete_var': {'type': 'discrete', 'min': -1.5, 'max': 4.5, 'step': 1.5},
    'integer_var': {'type': 'integer', 'min': -3, 'max': 3},
    'binary_var': {'type': 'binary'},
    'enumeration_var1': {'type': 'enumeration', 'values': [1, 2, 3]},
    'enumeration_var2': {'type': 'enumeration', 'values': np.array([1, 2, 3])},
    'enumeration_var3': {'type': 'enumeration', 'values': '1, 2, 3'},
    'permutation_grp_A': {'type': 'permutation', 'elements': ['one', 'two', 'three']},
    'permutation_grp_B': {'type': 'permutation', 'elements': 3}
}

# define the objective(s)
objectives = {
    'y': {'type': 'min', 'expression': 'pow(continuous_var, 2)'}
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    license_id=999999999,  # this license only allows 7 variables
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=10)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
