import numpy as np
from pyoptquest import OptQuestOptimizer


def ackley_function(inputs):
    x = inputs["x1"]
    y = inputs["x2"]

    a1 = -20 * np.exp(-0.2 * np.sqrt(0.5 * (x * x + y * y)))
    a2 = -np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    score = a1 + a2 + 20
    return -score


def trace_steps():
    best = None

    def print_iteration(inputs, outputs, objectives, iteration, replication):
        nonlocal best
        if best is None or objectives['objective'] > best:
            best = objectives['objective']
        print(iteration, inputs["x1"], inputs["x2"], objectives['objective'], best)

    return print_iteration


search_space = {
    "x1": np.arange(-100, 101, 0.1),
    "x2": np.arange(-100, 101, 0.1),
}

opt = OptQuestOptimizer(
    search_space,
    status_monitor=trace_steps(),
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(ackley_function, n_iter=10)

print()

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
