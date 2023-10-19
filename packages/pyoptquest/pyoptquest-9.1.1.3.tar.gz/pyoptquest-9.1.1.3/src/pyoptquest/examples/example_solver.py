import pyoptquest

# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'../optquest.jar')


def Evaluate(sol):
    iteration = sol.GetIteration()
    if (iteration % 100) == 0:
        print('Evaluating iteration ', iteration)


# define variables
x1 = pyoptquest.COptQuestContinuousVariable('x1', -10, 10)
x2 = pyoptquest.COptQuestContinuousVariable('x2', -10, 10)
x3 = pyoptquest.COptQuestContinuousVariable('x3', -10, 10)
x4 = pyoptquest.COptQuestContinuousVariable('x4', -10, 10)


# define objective(s)
obj = pyoptquest.COptQuestStringObjective()
obj.SetEquation('100 * pow(x2 - pow(x1,2),2) + pow(1-x1,2) + 90 * pow(x4 - pow(x3,2),2) + pow(1 - x3,2) + 10.1 * (pow(x2 - 1,2) + pow(x4 - 1,2)) + 19.8 * (x2 - 1) * (x4 - 1)')
obj.SetMinimize()


evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate)  # initialize the optimizer with the evaluator
# creates the optimization object
optimization = pyoptquest.COptQuestOptimization(evaluator)  # initialize the optimizer with the evaluator
# set up the optimization
optimization.SetLicenseID(999999999)  # trial license
optimization.AddVariable(x1)
optimization.AddVariable(x2)
optimization.AddVariable(x3)
optimization.AddVariable(x4)

optimization.AddObjective(obj)

# set stopping condition and optimize
optimization.SetMaximumIterations(500)
optimization.Optimize()

# get best solution and print things out
sol = optimization.GetBestSolution()

# print out results
# get best solution and print things out
sol = optimization.GetBestSolution()
print('Best solution at iteration ', sol.GetIteration())
print('x1=', sol.GetVariableValue(x1))
print('x2=', sol.GetVariableValue(x2))
print('x3=', sol.GetVariableValue(x3))
print('x4=', sol.GetVariableValue(x4))
print('obj=', sol.GetObjectiveValue())
