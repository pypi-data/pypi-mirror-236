from pyoptquest import OptQuestOptimizer


# function to evaluate the objective
def objective_evaluator(inputs):
    global opt
    x = inputs['x']
    print(x)
    # uncomment to show what happens when an un-caught exception happens
    # it should immediately stop the optimization
    # raise Exception("foo")

    # uncomment to show how you can stop the optimization manually and
    # tell optquest to gracefully shut down.  this would be something 
    # you could do if you caught your own exception
    # you can also return None without stopping the optimization and 
    # OptQuest will go on to the next solution
    # opt.stop_optimization()
    # return None

    # this is the happy path
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
    optquest_jar=r'OptQuest.jar')
opt.search(n_iter=10)

# print results
print('best score:', opt.best_score)
print('best parameters:', opt.best_para)
print('Optimization time:', opt.optimization_time)
