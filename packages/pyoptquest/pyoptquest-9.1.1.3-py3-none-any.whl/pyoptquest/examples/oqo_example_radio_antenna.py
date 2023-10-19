from numpy import arange
from math import exp, isnan
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from matplotlib import pyplot as plt
from pyoptquest import OptQuestOptimizer


# This is a more complex example that shows the power of OptQuest to do constrained optimization with


# A polygon where we are allowed to place radio antennas
polygon = Polygon([(45.12, -94.53), (45.1, -94.3), (45.09, -94.2), (44.9, -94.2), (44.88, -94.38), (44.93, -94.7)])

# An exclusion zone in the polygon where no antennas are allowed
exclusion_zone = Polygon([(44.95, -94.3), (45, -94.5), (45.05, -94.27), (45, -94.35)])

# bounding box of our polygon
(minx, miny, maxx, maxy) = polygon.bounds

# number of antennas we wish to place
n_antennas = 5

# set up the search space, the lat and lon of each antenna to place
search_space = {}
for i in range(n_antennas):
    search_space['lat{:d}'.format(i)] = {'type': 'discrete', 'min': minx, 'max': maxx, 'step': 0.01}
    search_space['lon{:d}'.format(i)] = {'type': 'discrete', 'min': miny, 'max': maxy, 'step': 0.01}

# set up the output space, that is the outputs of the model
# this is the cost to place all of the antenas
# the pairwise signal between each antenna
# the total_coverage of the region we're optimizing over
output_space = ['cost']
for i in range(n_antennas):
    for j in range(i+1, n_antennas):
        output_space.append('signal{:d}{:d}'.format(i, j))
output_space.append('total_coverage')


def all_antennas_inside_polygon(inputs):
    # constraint: all antennas need to be inside our polygon
    lat = [inputs['lat{:d}'.format(i)] for i in range(n_antennas)]
    lon = [inputs['lon{:d}'.format(i)] for i in range(n_antennas)]
    for i in range(5):
        if not polygon.contains(Point(lat[i], lon[i])):
            return False
    return True


def all_antennas_outside_exclusion(inputs):
    # constraint: no antenna can be in our exclusion zone
    lat = [inputs['lat{:d}'.format(i)] for i in range(n_antennas)]
    lon = [inputs['lon{:d}'.format(i)] for i in range(n_antennas)]
    for i in range(n_antennas):
        if exclusion_zone.contains(Point(lat[i], lon[i])):
            return False
    return True


def antennas_far_enough_apart(inputs):
    # constraint: no antenna can be too close to another one
    lat = [inputs['lat{:d}'.format(i)] for i in range(n_antennas)]
    lon = [inputs['lon{:d}'.format(i)] for i in range(n_antennas)]
    for i in range(n_antennas):
        pi = Point(lat[i], lon[i])
        for j in range(i+1, n_antennas):
            pj = Point(lat[j], lon[j])
            if pi.distance(pj) < 0.05:
                return False
    return True


def all_coverage_good(inputs):
    # constraint: make sure no one place has too small of coverage
    lat = [inputs['lat{:d}'.format(i)] for i in range(n_antennas)]
    lon = [inputs['lon{:d}'.format(i)] for i in range(n_antennas)]

    for i in range(n_antennas):
        pi = Point(lat[i], lon[i])
        for x in arange(minx, maxx, 0.01):
            for y in arange(miny, maxy, 0.01):
                pxy = Point(x, y)
                if exp(-pi.distance(pxy)/.1) < .005:
                    return False
    return True


def evaluate_antenna_placement(inputs):
    # run our evalautor, given locations of the antenna, this calculates the cost, signal, and coverage
    lat = [inputs['lat{:d}'.format(i)] for i in range(n_antennas)]
    lon = [inputs['lon{:d}'.format(i)] for i in range(n_antennas)]

    outputs = {}
    outputs['cost'] = 0
    center = polygon.centroid
    for i in range(n_antennas):
        pi = Point(lat[i], lon[i])
        outputs['cost'] += center.distance(pi)**2

    for i in range(n_antennas):
        pi = Point(lat[i], lon[i])
        for j in range(i+1, n_antennas):
            pj = Point(lat[j], lon[j])
            label = 'signal{:d}{:d}'.format(i, j)
            outputs[label] = exp(-pi.distance(pj)/.1)

    outputs['total_coverage'] = 0
    for x in arange(minx, maxx, 0.01):
        for y in arange(miny, maxy, 0.01):
            pxy = Point(x, y)
            coverage_at_xy = 0
            for i in range(n_antennas):
                pi = Point(lat[i], lon[i])
                coverage_at_xy += exp(-pi.distance(pxy)/.1)
            outputs['total_coverage'] += min(coverage_at_xy, 1)
    return outputs


def all_signals_good(inputs, outputs):
    # constraint: make sure no pairwise signal loss is too low
    for i in range(n_antennas):
        for j in range(i+1, n_antennas):
            label = 'signal{:d}{:d}'.format(i, j)
            if outputs[label] < .01:
                return False
    return True


# set up the two objectives we're tracking
objectives = {
    'coverage': {'type': 'max', 'expression': 'total_coverage'},
    'cost': {'type': 'min', 'expression': 'cost'}
}

# set up the constraints
constraints = {
    'inside': {'evaluator': all_antennas_inside_polygon},
    'outside': {'evaluator': all_antennas_outside_exclusion},
    'far_enough': {'evaluator': antennas_far_enough_apart},
    'coverage': {'evaluator': all_coverage_good},
    'signals': {'evaluator': all_signals_good}
}

# print out every successful iteration (ones that meet all constraints)


def status_monitor(inputs, outputs, objectives, iteration, replication):
    if not isnan(objectives['coverage']):
        print('iteration:', iteration)
        print('objectives:', objectives)
        print('inputs:', inputs)
        print('outputs:', outputs)
        print('---')


opt = OptQuestOptimizer(
    search_space,
    output_space=output_space,
    evaluator=evaluate_antenna_placement,
    objectives=objectives,
    constraints=constraints,
    status_monitor=status_monitor,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=1500)

print()

# print results
print('Pareto frontier:')
print(opt.best_score)
print('Optimization time:', opt.optimization_time)

# plot results
fig, ax = plt.subplots()
ax.set_title('coverage vs cost')
ax.set_xlabel('coverage')
ax.set_ylabel('cost')
opt.search_data.plot(x='coverage', y='cost', style='s', color='pink', ax=ax)  # all data
opt.best_score.plot(x='coverage', y='cost', style='+', color='green', ax=ax)  # Pareto front
ax.legend(['all data', 'Pareto frontier'])

print()

# plot a solution from the Pareto frontier
inputs = opt.best_score.iloc[0]
print('iteration:', inputs['iteration'])
print('coverage:', inputs['coverage'])
print('cost:', inputs['cost'])

lats = [inputs['lat0'], inputs['lat1'], inputs['lat2'], inputs['lat3'], inputs['lat4']]
lons = [inputs['lon0'], inputs['lon1'], inputs['lon2'], inputs['lon3'], inputs['lon4']]

fig2, ax2 = plt.subplots()
ax2.set_title('Antenna Configuration')
ax2.set_xlabel('longitude')
ax2.set_ylabel('latitude')
ax2.scatter(x=lats, y=lons, marker='x', color='dimgray')
ax2.plot(*polygon.exterior.xy, color='blue')
ax2.plot(*exclusion_zone.exterior.xy, color='red')
ax2.legend(['antenna locations', 'bounding region', 'exclusion zone'])
plt.show()
