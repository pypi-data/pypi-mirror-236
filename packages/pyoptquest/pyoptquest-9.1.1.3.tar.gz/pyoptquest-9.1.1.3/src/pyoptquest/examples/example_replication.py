import traceback
import pyoptquest

# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'../optquest.jar')


def Evaluate(sol):
    global optimization
    global var1
    global var2
    global var3
    global obj

    # get the values OptQuest provides for this run
    val1 = sol.GetVariableValue(var1)
    val2 = sol.GetVariableValue(var2)
    val3 = sol.GetVariableValue(var3)

    replication = sol.GetReplication()

    objectiveValue = abs(val1 - 5) + abs(val2 - 50) + abs(val3 - 100)
    if (replication > 1):
        objectiveValue = objectiveValue * replication/10
     # set objective(s)
    sol.SetObjectiveValue(obj, objectiveValue)
    print('obj =', objectiveValue, ' iteration ', sol.GetIteration(), ' replication ', sol.GetReplication())


def MonitorStatus(sol):
    # Optional function for tracking the status of optimization.
    # Must have the call signature (sol)
    # This example uses a global to access the optimization object
    global optimization
    global obj
    try:
        if (sol.IsLastReplication()):
            objectiveValue = sol.GetObjectiveValue(obj)
            print('   Mean = ', objectiveValue)
    except Exception:
        print('Exception in MonitorStatus')
        print("".join(traceback.TracebackException.from_exception(Exception).format()))


# define variables
var1 = pyoptquest.COptQuestDiscreteVariable('var1', 1.0, 1000.0, 1.0)
var2 = pyoptquest.COptQuestDiscreteVariable('var2', 1.0, 1000.0, 1.0)
var3 = pyoptquest.COptQuestDiscreteVariable('var3', 1.0, 1000.0, 1.0)

# define objective(s)
obj = pyoptquest.COptQuestUserControlledObjective()
obj.SetMinimize()

evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate, MonitorStatus)  # initialize the optimizer with the evaluator
# creates the optimization object
optimization = pyoptquest.COptQuestOptimization(evaluator)  # initialize the optimizer with the evaluator

# set up the optimization
optimization.SetLicenseID(999999999)  # trial license
optimization.AddVariable(var1)
optimization.AddVariable(var2)
optimization.AddVariable(var3)
optimization.AddObjective(obj)

# set stopping condition and optimize
optimization.SetMaximumIterations(25)
optimization.SetUseReplications(True)
optimization.SetMinimumReplications(6)
optimization.Optimize()

# get best solution and print things out
sol = optimization.GetBestSolution()

# print out results
print('Best Solution is at iteration ', sol.GetIteration())
print('var1=', sol.GetVariableValue(var1))
print('var2=', sol.GetVariableValue(var2))
print('var3=', sol.GetVariableValue(var3))
print('obj=', sol.GetObjectiveValue())
