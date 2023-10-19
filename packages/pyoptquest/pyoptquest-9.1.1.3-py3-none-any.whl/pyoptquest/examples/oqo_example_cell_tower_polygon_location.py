from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from pyoptquest import OptQuestOptimizer


def point_inside_polygon(inputs):
    x = inputs['lat']
    y = inputs['lon']
    polygon = Polygon([(45.12, -94.53),
                       (45.1, -94.3),
                       (45.09, -94.2),
                       (44.9, -94.2),
                       (44.88, -94.38),
                       (44.93, -94.7)])
    return polygon.contains(Point(x, y))


# the solution space is a dict
search_space = {
    'lat': {'type': 'discrete', 'min': 44.88, 'max': 45.12, 'step': 0.1},
    'lon': {'type': 'discrete', 'min': -94.7, 'max': -94.2, 'step': 0.1},
}

# dict of objectives (one evaluator objective, one string objective)
objectives = {
    'coverage': {'type': 'max', 'expression': 'abs(lat + lon) * 4'}
}

constraints = {
    'inside': {'evaluator': point_inside_polygon}
}

# do optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    constraints=constraints,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=25)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
