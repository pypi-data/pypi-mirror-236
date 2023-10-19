from pyoptquest import OptQuestOptimizer

# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10},
    'y': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective
objectives = {
    'obj': {'type': 'min', 'expression': 'pow(x-2,2) + pow(y+3,2)'}
}

# suggested runs
suggested_runs = {'x': [1, 1.5, 2.5, 3], 'y': [-4, -3.5, -2.5, -2]}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar',
    setup_log='setup.xml')

opt.search(n_iter=100, suggested_runs=suggested_runs, solutions_log='solutions.csv')

print('search data:')
print(opt.search_data)
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)

