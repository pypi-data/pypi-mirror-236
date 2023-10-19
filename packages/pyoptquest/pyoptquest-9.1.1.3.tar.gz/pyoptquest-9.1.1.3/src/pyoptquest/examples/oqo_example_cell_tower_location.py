from pyoptquest import OptQuestOptimizer

# the solution space is a dict
search_space = {
    'lat': {'type': 'discrete', 'min': 41, 'max': 42, 'step': 0.1},
    'lon': {'type': 'discrete', 'min': -101, 'max': -100, 'step': 0.1},
}

# dict of objectives (one evaluator objective, one string objective)
objectives = {
    'coverage': {'type': 'max', 'expression': 'abs(lat + lon) * 4'}
}

# do optimization
opt = OptQuestOptimizer(
    search_space,
    objectives=objectives,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=25)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
