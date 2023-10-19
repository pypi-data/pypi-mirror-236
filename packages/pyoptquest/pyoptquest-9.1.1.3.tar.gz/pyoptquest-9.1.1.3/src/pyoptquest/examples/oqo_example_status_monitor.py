from pyoptquest import OptQuestOptimizer


# optional function for tracking the status of the optimization (called every iteration)
def status_monitor(inputs, outputs, objectives, iteration, replication):
    print(f'--status monitor says hello from iteration {iteration} with objective value {objectives["y"]}')


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
    status_monitor=status_monitor,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=10)

print()

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
