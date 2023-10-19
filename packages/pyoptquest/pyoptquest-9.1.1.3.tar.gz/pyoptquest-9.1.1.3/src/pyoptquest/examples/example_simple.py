import pyoptquest


# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'../optquest.jar')


def Evaluate(var1, var2, out_product, out_sum, obj):
    # The function evaluated each iteration for optimization
    # Must have the call signature (sol)
    # This is done as a nested fuction to show how state can be stored between calls
    _var1 = var1
    _var2 = var2
    _out_product = out_product
    _out_sum = out_sum
    _obj = obj

    def _Evaluate(sol):
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

        # set objective(s)
        sol.SetObjectiveValue(_obj, prod - bigger)
    return _Evaluate


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
evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate(var1, var2, out_product, out_sum, obj), MonitorStatus)

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
optimization.Optimize()

# get best solution and print things out
sol = optimization.GetBestSolution()

# print out results
print('var1=', sol.GetVariableValue(var1))
print('var2=', sol.GetVariableValue(var2))
print('out_product=', sol.GetVariableValue(out_product))
print('out_sum=', sol.GetVariableValue(out_sum))
print('obj=', sol.GetObjectiveValue())
