import pyoptquest
import threading
import queue
import time
import random

# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'../optquest.jar')

# number of parallel evaluators to run
n_parallel = 10


def PEvaluate(var1, var2, out_product, out_sum, obj, unevaluated_queue, evaluated_queue):
    # The thread function that does the evaluation. There will be n_parallel instances of this function running concurrently
    _var1 = var1
    _var2 = var2
    _out_product = out_product
    _out_sum = out_sum
    _obj = obj

    def _Evaluate(sol):
        # This is the code that is eqivalent to sending the solution to a job manager
        # After a solution is pulled off of the queue, it's sent out for evaluatation
        # and when the evaluation returns, the evaluated soltion is put on the evaluated queue
        print("Starting", sol.GetIteration())

        # get the values OptQuest provides for this run
        val1 = sol.GetVariableValue(_var1)
        val2 = sol.GetVariableValue(_var2)

        # perform the simulation/evaluation with these values
        prod = val1 * val2
        if prod > 15:
            prod -= 2 * (prod - 15)
        if prod < -15:
            prod += 2 * (-15 - prod)

        # set outputs
        sol.SetVariableValue(_out_product, prod)
        sol.SetVariableValue(_out_sum, val1 + val2)

        bigger = max(abs(val1), abs(val2))

        # this part fakes a remote execution of some long running process
        # if this is really call to something, then in parallel mode, Python
        # needs to release the Global Interpreter Lock or else the multi-threadness of
        # Python doesn't actually work.  Most things in python work as you exepect them
        # to here, but just be aware that because of the GIL, Python isn't truely
        # concurrent.  Any type of async/await should be good for parallel I/O
        time.sleep(random.random())

        # set objective(s)
        sol.SetObjectiveValue(_obj, prod - bigger)
        print("Evaluated", sol.GetIteration())

        # Put the evaulated solution on the evaluated queue so that it can be
        # sent back to OptQuest
        evaluated_queue.put(sol)

    # Pump the unevaluated queue and get a solution to evaluate
    while True:
        sol = unevaluated_queue.get()
        _Evaluate(sol)


def Evaluate(sol):
    # The function that OptQuest calls to evaluate a soluiton
    global unevaluated_queue
    global evaluated_queue
    global optimization

    if sol is None:
        # If OptQuest passes in a null solution to Evaluate, we know that all of the parallel
        # evaluators are busy and we should block until a solution is ready to return to OptQuest
        # this waits on the evaluated_queue for an available solution and then sends it back
        # to OptQuest
        sol = evaluated_queue.get()
        print("Returning", sol.GetIteration())
        optimization.EvaluateComplete(sol)
    else:
        # If the solution is non-null, then we know we have a soluiton that we want to dispatch to
        # one of our parallel evaluators. So we just put it on a queue and one of the paralell
        # evaluators will take it
        unevaluated_queue.put(sol)

    # And now we go through the entire evaluated_queue and empty it, sending all evaluated
    # solutions back to OptQuest
    try:
        while True:
            # this will throw when the queue is empty and we'll exit.
            sol = evaluated_queue.get_nowait()
            print("Clearing", sol.GetIteration())
            optimization.EvaluateComplete(sol)
    except:
        return


def MonitorStatus(sol):
    # Optional function for tracking the status of optimization.
    # Must have the call signature (sol)
    # This example uses a global to access the optimization object
    global optimization
    iteration = sol.GetIteration()
    if (iteration % 50) == 0:
        print('Iteration=', sol.GetIteration(), optimization.GetBestSolution().GetObjectiveValue())


# define variables
var1 = pyoptquest.COptQuestContinuousVariable('var1', -5, 5)
var2 = pyoptquest.COptQuestContinuousVariable('var2', -5, 5)

# define outputs
out_product = pyoptquest.COptQuestUserControlledVariable('out_product')
out_sum = pyoptquest.COptQuestUserControlledVariable('out_sum')

# define objective(s)
obj = pyoptquest.COptQuestUserControlledObjective('obj')
obj.SetMaximize()

# create the object needed to callbacks for evaluation
evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate, MonitorStatus)

# creates the optimization object
optimization = pyoptquest.COptQuestOptimization(evaluator)  # initialize the optimizer with the evaluator

# set up the optimization
optimization.SetLicenseID(999999999)  # trial license
optimization.AddVariable(var1)
optimization.AddVariable(var2)
optimization.AddVariable(out_product)
optimization.AddVariable(out_sum)
optimization.AddObjective(obj)

# set stopping condition and optimize
optimization.SetMaximumIterations(300)
optimization.SetEvaluate(n_parallel)

# this queue will hold all solutions that are ready to be picked up by one of the parallel evaluators
unevaluated_queue = queue.Queue()

# this queue will hold all solutions that have been evaluated and are ready to go back to OptQuest
evaluated_queue = queue.Queue()

# Start all of the evaluator threads, they will pump the unevaluated_queue pulling solutions to evaluate
for i in range(n_parallel):
    threading.Thread(target=PEvaluate, args=(var1, var2, out_product, out_sum, obj, unevaluated_queue, evaluated_queue), daemon=True).start()

# Tell OptQuest to start the optimize loop, OptQuest will call Evaluate() which will put things on
# the unevaluated queue, one of the parallel evaluators will pop that, evaluate it and put it back on the
# evaluated queue.
optimization.Optimize()

# get best solution and print things out
sol = optimization.GetBestSolution()

# print out results
print('var1=', sol.GetVariableValue(var1))
print('var2=', sol.GetVariableValue(var2))
print('out_product=', sol.GetVariableValue(out_product))
print('out_sum=', sol.GetVariableValue(out_sum))
print('obj=', sol.GetObjectiveValue())
