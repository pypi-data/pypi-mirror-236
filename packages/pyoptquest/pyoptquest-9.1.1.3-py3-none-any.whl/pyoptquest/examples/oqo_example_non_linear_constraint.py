from asyncio import constants
from pyoptquest import OptQuestOptimizer

# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10},
    'y': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective(s)
objectives = {
    'z': {'type': 'min', 'expression': 'x * x + y * y'}
}

constraints = {
    'c1': {'expression': '(x+1)*(x+1)+(y+1)*(y+1)>3'},
    'c2': {'expression': '(x+1)*(x+1)+(y+1)*(y+1)<3.01'}
}


# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    constraints=constraints,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar',log='setup.xml')
opt.search(n_iter=1000000, log='solutions.xml')

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
