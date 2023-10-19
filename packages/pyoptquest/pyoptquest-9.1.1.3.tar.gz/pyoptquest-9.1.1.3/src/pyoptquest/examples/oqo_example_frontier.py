from matplotlib import pyplot as plt

from pyoptquest import OptQuestOptimizer

# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -2, 'max': 2}
}

# define the objective(s)
objectives = {
    'objective_1': {'type': 'min', 'expression': 'pow(x + 1, 2)'},
    'objective_2': {'type': 'min', 'expression': 'pow(x - 1, 2)'}
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')

# do the optimization
opt.search(n_iter=10)

# print results
print('Pareto front:')
print(opt.best_score)
print('Optimization time:', opt.optimization_time)

# plot results
fig, ax = plt.subplots()
ax.set_title('Pareto Frontier')
ax.set_xlabel('objective_1')
ax.set_ylabel('objective_2')
opt.search_data.plot(x='objective_1', y='objective_2', style='s', color='pink', ax=ax)  # all data
opt.best_score.plot(x='objective_1', y='objective_2', style='+', color='green', ax=ax)  # Pareto front
ax.legend(['all data', 'Pareto frontier'])
# label points on the Pareto frontier
for idx, (x_coord, y_coord) in enumerate(zip(opt.best_score['objective_1'], opt.best_score['objective_2'])):
    x = round(opt.best_score["x"][idx], 2)
    ax.annotate(text=str(f'$x={x}$'), xy=(x_coord + 0.2, y_coord))
plt.show()
