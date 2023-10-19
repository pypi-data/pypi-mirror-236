from pyoptquest import OptQuestOptimizer


def simulation(inputs):
    # get inputs from OptQuestOptimizer
    x = inputs['x']

    # run the "simulation"
    y = x**2

    # create dict to hold return values from the simulation
    outputs = {'y': y}
    return outputs


# define the input(s)
search_space = {
    'x': {'type': 'continuous', 'min': -10, 'max': 10}
}

# specify the output(s) of the simulation evaluator (the output(s) of the simulation() function)
output_space = ['y']

# define the objective(s)
objectives = {
    'obj': {'type': 'min', 'expression': 'y'}  # minimize the output "y"
}

# define the optimization
opt = OptQuestOptimizer(
    search_space,
    objectives,
    evaluator=simulation,
    output_space=output_space,
    license_id=999999999,
    optquest_jar=r'../OptQuest.jar')
opt.search(n_iter=10)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
