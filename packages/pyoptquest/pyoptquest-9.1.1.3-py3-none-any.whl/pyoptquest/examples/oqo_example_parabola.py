from pyoptquest import OptQuestOptimizer

# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective(s)
objectives = {
    'y': {'type': 'min', 'expression': 'x * x'}
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search()

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
