import time
from pyoptquest import OptQuestOptimizer


# represents a large simulation running for one second
def sleep_evaluator(inputs):
    time.sleep(1)
    return {}


# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective(s)
objectives = {
    'y': {'type': 'min', 'expression': 'pow(x - pi, 2)'}
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    evaluator=sleep_evaluator,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=100, parallel_evaluators=20)  # increasing parallel_evaluators will decrease the optimization time

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
