import traceback
import pyoptquest

# Tell pyoptquest where the jar is. This initializes the JVM and creates all COptQuestClasses
pyoptquest.InitializeOptQuest(r'../optquest.jar')


def Evaluate(sol):
    global optimization
    global varRisk1
    global varRisk2
    global varRisk3
    global avgRisk

    # get the values OptQuest provides for this run
    risk1 = sol.GetVariableValue(varRisk1)
    risk2 = sol.GetVariableValue(varRisk2)
    risk3 = sol.GetVariableValue(varRisk3)

    objectiveValue = (risk1 + risk2 + risk3)/3.0
    # set objective(s)
    sol.SetObjectiveValue(avgRisk, objectiveValue)


def MonitorStatus(sol):
    # Optional function for tracking the status of optimization.
    # Must have the call signature (sol)
    # This example uses a global to access the optimization object
    global optimization

    try:
        completedIterations = optimization.GetNumberofCompletedIterations()
        if (completedIterations % 10 == 0):
            print('Frontier after ', completedIterations, ' iterations')
            theFrontier = optimization.GetPatternFrontier()
            for sol in theFrontier:
                print('frontier solution at iteration ', sol.GetIteration())
            print('\n')
    except Exception:
        print('Exception in MonitorStatus')
        print("".join(traceback.TracebackException.from_exception(Exception).format()))


try:
    evaluator = pyoptquest.COptQuestOptimizationEvaluator(Evaluate, MonitorStatus)  # initialize the optimizer with the evaluator
    # creates the optimization object
    optimization = pyoptquest.COptQuestOptimization(evaluator)  # initialize the optimizer with the evaluator

    # define variables
    varRisk1 = pyoptquest.COptQuestContinuousVariable("risk1", 0.0, 1.0)
    varRisk2 = pyoptquest.COptQuestContinuousVariable("risk2", 0.0, 1.0)
    varRisk3 = pyoptquest.COptQuestContinuousVariable("risk3", 0.0, 1.0)

    varNPV1 = pyoptquest.COptQuestContinuousVariable("npv1", 250000.0, 1000000.0)
    varNPV2 = pyoptquest.COptQuestContinuousVariable("npv2", 250000.0, 1000000.0)
    varNPV3 = pyoptquest.COptQuestContinuousVariable("npv3", 250000.0, 1000000.0)

    optimization.AddVariable(varRisk1)
    optimization.AddVariable(varRisk2)
    optimization.AddVariable(varRisk3)
    optimization.AddVariable(varNPV1)
    optimization.AddVariable(varNPV2)
    optimization.AddVariable(varNPV3)

    # define objective(s)
    avgRisk = pyoptquest.COptQuestUserControlledObjective("Risk")
    avgRisk.SetMinimize()

    avgNPV = pyoptquest.COptQuestStringObjective()
    avgNPV.SetEquation('(npv1 + npv2 + npv3)/3.0')
    avgNPV.SetMaximize()

    frontier = pyoptquest.COptQuestFrontierMultiObjective()
    frontier.AddObjective(avgRisk)
    frontier.AddObjective(avgNPV)

    # set up the optimization
    optimization.SetLicenseID(999999999)  # trial license

    optimization.AddObjective(frontier)

    # set stopping condition and optimize
    optimization.SetMaximumIterations(50)
    optimization.Optimize()

    # print frontier points
    print('Optimization completed')
    theFrontier = optimization.GetPatternFrontier()
    for sol in theFrontier:
        print('frontier solution at iteration ', sol.GetIteration())
        risk = sol.GetObjectiveValue(avgRisk)
        npv = sol.GetObjectiveValue(avgNPV)
        print('When risk is ', risk, ' NPV is ', npv)

except Exception:
    print('Exception')
    print("".join(traceback.TracebackException.from_exception(Exception).format()))
