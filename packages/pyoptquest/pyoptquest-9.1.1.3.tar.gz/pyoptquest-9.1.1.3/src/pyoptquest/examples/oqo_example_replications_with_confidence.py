import random

from pyoptquest import OptQuestOptimizer


# optional function for tracking the status of the optimization, called every iteration/replication
def status_monitor(inputs, outputs, objectives, iteration, replication):
    print(f'--executing {iteration}, replication {replication}')


# return a random number close to 1 so that a random number of replications are called for by OptQuest
def objective_evaluator(dec_var_values, output_values):
    return 1 + (random.random() - 0.5) * 0.2


# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10}
}

# define the objective(s)
objectives = {
    'y': {'type': 'min', 'evaluator': objective_evaluator, 'confidence': 5, 'error': 0.04}  # confidence 5 means 99% confidence interval
}

# define the optimization
opt = OptQuestOptimizer(search_space, objectives,
                        status_monitor=status_monitor,
                        license_id=999999999,
                        optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=2, replications=(5, 20))

print()

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
