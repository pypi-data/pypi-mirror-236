import numpy as np
from pyoptquest import OptQuestOptimizer


def convex_function(inputs):
    score = -(inputs["x1"] * inputs["x1"] + inputs["x2"] * inputs["x2"])
    return score


search_space = {
    "x1": np.arange(-100, 101, 0.1),
    "x2": np.arange(-100, 101, 0.1),
}

opt = OptQuestOptimizer(
    search_space,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(convex_function, n_iter=300000)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
