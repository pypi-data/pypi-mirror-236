from pyoptquest import OptQuestOptimizer


# function to evaluate the objective
def objective_evaluator(inputs):
    x = inputs['x']
    return x**2


# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective(s)
objectives = {
    'y': {'type': 'min', 'evaluator': objective_evaluator}  # specify the evaluator
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=10)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
