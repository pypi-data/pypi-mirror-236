import pyoptquest
import random


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

    # Use a random number to get some variability
    objectiveValue = val1 + val2 + val3 + (random.random() * replication)
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
            objectiveValue = sol.GetObjectiveValue()
            print('   Mean at iteration ', sol.GetIteration(), ' is ', objectiveValue)
    except:
        print('Exception in MonitorStatus')


# define variables
var1 = pyoptquest.COptQuestDiscreteVariable('var1', 1.0, 1000.0, 1.0)
var2 = pyoptquest.COptQuestDiscreteVariable('var2', 1.0, 1000.0, 1.0)
var3 = pyoptquest.COptQuestDiscreteVariable('var3', 1.0, 1000.0, 1.0)

# define objective(s)
obj = pyoptquest.COptQuestUserControlledObjective()
obj.SetMinimize()
# confidence level 80%, error .05
obj.SetReplicationConfidence(1, 1, .05)

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
optimization.SetMaximumReplications(10)

optimization.Optimize()

# get best solution and print things out
sol = optimization.GetBestSolution()

# print out results
print('Best Solution is at iteration ', sol.GetIteration())
if (sol.SolutionMetConfidence()):
    print('Best solution met confidence.  Ran ', sol.GetReplicationCount(), ' replications')
else:
    print('Best solution did not meet confidence.  Ran ', sol.GetReplicationCount(), ' replications')

print('obj=', sol.GetObjectiveValue())
