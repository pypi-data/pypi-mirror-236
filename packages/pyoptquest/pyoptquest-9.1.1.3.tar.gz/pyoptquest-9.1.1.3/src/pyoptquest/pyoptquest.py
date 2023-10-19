import logging
import queue
import sys
import threading
import time
import traceback

import pandas as pd

from inspect import signature

# prevent double initalization
initialized = False

# attach OptQuest JAR
COptQuestOptimizationEvaluator = None
COptQuestBinaryVariable = None
COptQuestConstraint = None
COptQuestContinuousVariable = None
COptQuestDesignVariable = None
COptQuestDiscreteVariable = None
COptQuestEnumerationVariable = None
COptQuestEquationSolver = None
COptQuestException = None
COptQuestExceptionLogger = None
COptQuestFrontierMultiObjective = None
COptQuestIntegerVariable = None
COptQuestMultiObjective = None
COptQuestObjective = None
COptQuestOptimization = None
COptQuestPermutationGroup = None
COptQuestPermutationVariable = None
COptQuestSingleObjective = None
COptQuestSolution = None
COptQuestStringConstraint = None
COptQuestStringObjective = None
COptQuestUserControlledObjective = None
COptQuestUserControlledVariable = None
COptQuestVariable = None
COptQuestSearchParameters = None


def InitializeOptQuest(path):
    global initialized
    if initialized:
        return True

    global COptQuestOptimizationEvaluator

    global COptQuestBinaryVariable
    global COptQuestConstraint
    global COptQuestContinuousVariable
    global COptQuestDesignVariable
    global COptQuestDiscreteVariable
    global COptQuestEnumerationVariable
    global COptQuestEquationSolver
    global COptQuestException
    global COptQuestExceptionLogger
    global COptQuestFrontierMultiObjective
    global COptQuestIntegerVariable
    global COptQuestMultiObjective
    global COptQuestObjective
    global COptQuestOptimization
    global COptQuestPermutationGroup
    global COptQuestPermutationVariable
    global COptQuestSingleObjective
    global COptQuestSolution
    global COptQuestStringConstraint
    global COptQuestStringObjective
    global COptQuestUserControlledObjective
    global COptQuestUserControlledVariable
    global COptQuestVariable
    global COptQuestSearchParameters

    try:
        import jnius_config
        jnius_config.set_classpath(path)
    except ValueError:
        logging.exception('failed to set pyjnius classpath')
        return False

    from jnius import autoclass, PythonJavaClass, java_method, JavaException

    class PyOptQuestEvaluator(PythonJavaClass):
        __javainterfaces__ = ['com/opttek/optquest/COptQuestOptimizationEvaluator']

        def __init__(self, Evaluate=None, MonitorStatus=None):
            self.CBEvaluate = Evaluate
            self.CBMonitorStatus = MonitorStatus

        @java_method('(Lcom/opttek/optquest/COptQuestSolution;)V')
        def Evaluate(self, sol):
            if self.CBEvaluate is not None:
                self.CBEvaluate(sol)

        @java_method('()V')
        def NullEvaluate(self):
            if self.CBEvaluate is not None:
                self.CBEvaluate(None)

        @java_method('(Lcom/opttek/optquest/COptQuestSolution;)V')
        def MonitorStatus(self, sol):
            if self.CBMonitorStatus is not None:
                self.CBMonitorStatus(sol)

    COptQuestOptimizationEvaluator = PyOptQuestEvaluator

    try:
        COptQuestOptimization = autoclass('com/opttek/optquest/COptQuestPythonOptimization')

        COptQuestBinaryVariable = autoclass('com/opttek/optquest/COptQuestBinaryVariable')
        COptQuestConstraint = autoclass('com/opttek/optquest/COptQuestConstraint')
        COptQuestContinuousVariable = autoclass('com/opttek/optquest/COptQuestContinuousVariable')
        COptQuestDesignVariable = autoclass('com/opttek/optquest/COptQuestDesignVariable')
        COptQuestDiscreteVariable = autoclass('com/opttek/optquest/COptQuestDiscreteVariable')
        COptQuestEnumerationVariable = autoclass('com/opttek/optquest/COptQuestEnumerationVariable')
        COptQuestEquationSolver = autoclass('com/opttek/optquest/COptQuestEquationSolver')
        COptQuestException = autoclass('com/opttek/optquest/COptQuestException')
        COptQuestExceptionLogger = autoclass('com/opttek/optquest/COptQuestExceptionLogger')
        COptQuestFrontierMultiObjective = autoclass('com/opttek/optquest/COptQuestFrontierMultiObjective')
        COptQuestIntegerVariable = autoclass('com/opttek/optquest/COptQuestIntegerVariable')
        COptQuestMultiObjective = autoclass('com/opttek/optquest/COptQuestMultiObjective')
        COptQuestObjective = autoclass('com/opttek/optquest/COptQuestObjective')
        COptQuestPermutationGroup = autoclass('com/opttek/optquest/COptQuestPermutationGroup')
        COptQuestPermutationVariable = autoclass('com/opttek/optquest/COptQuestPermutationVariable')
        COptQuestSingleObjective = autoclass('com/opttek/optquest/COptQuestSingleObjective')
        COptQuestSolution = autoclass('com/opttek/optquest/COptQuestSolution')
        COptQuestStringConstraint = autoclass('com/opttek/optquest/COptQuestStringConstraint')
        COptQuestStringObjective = autoclass('com/opttek/optquest/COptQuestStringObjective')
        COptQuestUserControlledObjective = autoclass('com/opttek/optquest/COptQuestUserControlledObjective')
        COptQuestUserControlledVariable = autoclass('com/opttek/optquest/COptQuestUserControlledVariable')
        COptQuestVariable = autoclass('com/opttek/optquest/COptQuestVariable')
        COptQuestSearchParameters = autoclass('com/opttek/optquest/COptQuestSearchParameters')

        # these lines cause the JNI to print out exceptions on its own
        # System = autoclass('java.lang.System')
        # COptQuestExceptionLogger.setLogStream(System.err)

        initialized = True
        return True
    except JavaException:
        logging.exception('Java exception occurred')
        return False


# OptQuestOptimizer implementation
class OptQuestOptimizer:
    def __init__(self, search_space, objectives=None, evaluator=None, output_space=None, constraints=None,
                 status_monitor=None, user_stop=None, license_id=0, optquest_jar='./', setup_log=None):
        """
        This class provides a Python-friendly API to the OptQuest engine. See README for examples and more info on defining an optimization.
        :param search_space: A dict of variable names; each mapped to a dict of their properties.
        :param objectives: A dict of objective names; each mapped to a dict of their properties.
        :param evaluator: A callback function that processes inputs and produces outputs.
        :param output_space: A dict of `evaluator` output names mapped to their respective values. Only necessary if an argument is passed for the `evaluator` parameter.
        :param constraints: A dict of constraint names; each mapped to a dict of their properties.
        :param status_monitor: A callback function for monitoring the progress of an optimization.
        :param user_stop: A callback function that can stop an optimization before completion.
        :param license_id: The ID number for your OptQuest license.
        :param optquest_jar: Path to an `OptQuest.jar` file (version 9.1.1.2 or higher.)
        """

        if output_space is None:
            output_space = []
            if evaluator is not None:
                print('Warning: The parameter "evaluator" was passed but "output_space" was not. The results of the evaluator will not be used.')

        self.__license_id = license_id
        self.__initialize_optquest(path=optquest_jar)
        self.__is_multi_objective = True if (objectives is not None) and (len(objectives) > 1) else False
        self.__user_evaluator = evaluator
        self.__status_monitor = status_monitor
        self.__user_stop = user_stop
        self.__search_parameters = COptQuestSearchParameters()
        self.__setup_log = setup_log

        self.__inferred_objective = False
        self.__stop_optimization = False

        # queues for parallel evaluators to get/put solutions from/to
        self.__unevaluated_queue = queue.Queue()
        self.__evaluated_queue = queue.Queue()

        # all results
        self.__search_data_list = []  # list of results, each result is a dict
        self.__best_search_data_list = []  # list of pareto frontier results, each result is a dict
        self.search_data = None  # pandas dataframe with results

        # results
        # if single objective, self.best_score is the single objective value
        # and self.best_para are the associated variable values
        # if multi-objective, self.best_score is a pandas dataframe containing the pareto frontier results
        # and self.best_para is the same dataframe
        self.best_score = None
        self.best_para = {}

        self.optimization_time = 0  # the time it took the optimization to complete

        # wrap calls to OptQuest with try-catch
        try:

            # define decision variable(s)
            self.__dec_vars = {}
            # also keep track of permutation variables
            self.__perm_vars = {}
            self.__perm_groups = {}
            # format for GFO compatibility
            for key in search_space:
                item = search_space[key]
                if type(item) is not dict:
                    item_iter = iter(item)
                    item_first = next(item_iter)
                    item_second = next(item_iter)
                    step_size = item_second - item_first
                    search_space[key] = {'type': 'discrete', 'min': min(item), 'max': max(item), 'step': step_size}

            for var_name in search_space.keys():
                new_var = None
                var_properties = search_space[var_name]

                # if no variable type given, set to 'continuous'
                var_type = var_properties['type'] if 'type' in var_properties else 'continuous'

                # create new variable of given variable type
                if var_type == 'continuous':
                    new_var = COptQuestContinuousVariable(var_name, var_properties['min'], var_properties['max'])
                    self.__dec_vars[var_name] = new_var
                elif var_type == 'discrete':
                    new_var = COptQuestDiscreteVariable(var_name, var_properties['min'], var_properties['max'],
                                                        var_properties['step'])
                    self.__dec_vars[var_name] = new_var
                elif var_type == 'integer':
                    new_var = COptQuestIntegerVariable(var_name, var_properties['min'], var_properties['max'])
                    self.__dec_vars[var_name] = new_var
                elif var_type == 'binary':
                    new_var = COptQuestBinaryVariable(var_name)
                    self.__dec_vars[var_name] = new_var
                elif var_type == 'enumeration':
                    new_var = COptQuestEnumerationVariable(var_name)
                    enumeration_values = var_properties["values"]
                    if isinstance(enumeration_values, str):
                        pass
                    elif isinstance(enumeration_values, list):
                        enumeration_values = ' '.join([str(val) for val in enumeration_values])
                    elif hasattr(enumeration_values, '__iter__'):
                        enumeration_values = ' '.join([str(val) for val in list(enumeration_values)])
                    else:
                        print(
                            f'cannot interpret enumeration values for "{var_name}", please use an iterable or a string of values (comma- or space-delimited)')
                        continue
                    new_var.AddEnumerationValues(enumeration_values)
                    self.__dec_vars[var_name] = new_var
                elif var_type == 'permutation':
                    perm_group_name = var_name
                    permutation_group_elements = var_properties['elements']
                    # user can pass a list of strings (as permutation variable names) or an int specifying number of permutation variables in group
                    if type(permutation_group_elements) is list and type(permutation_group_elements[0] is str):
                        # create and populate permutation group, add permutation variables to self.dec_vars
                        new_perm_group = COptQuestPermutationGroup()
                        for element in permutation_group_elements:
                            perm_var = COptQuestPermutationVariable(str(element))
                            new_perm_group.AddVariable(perm_var)
                            self.__dec_vars[element] = perm_var
                            self.__perm_vars[element] = perm_var
                        self.__perm_groups[perm_group_name] = new_perm_group
                    elif type(permutation_group_elements) is int:
                        # create and populate permutation group, add permutation variables to self.dec_vars
                        new_perm_group = COptQuestPermutationGroup()
                        for idx in range(1, permutation_group_elements + 1):
                            perm_var_name = f'{perm_group_name}({idx})'
                            perm_var = COptQuestPermutationVariable(perm_var_name)
                            new_perm_group.AddVariable(perm_var)
                            self.__dec_vars[perm_var_name] = perm_var
                            self.__perm_vars[perm_var_name] = perm_var
                        self.__perm_groups[perm_group_name] = new_perm_group
                    else:
                        print(
                            'WARNING: the "elements" property of a permutation group input variable must be a list of strings or an int.')
                        continue
                else:
                    print(f'Unknown variable type "{var_type}".')
                    continue

            # define output(s)
            self.__outputs = {}
            for output_name in output_space:
                new_output = COptQuestUserControlledVariable(output_name)

                self.__outputs[output_name] = new_output

            # define constraint(s)
            self.__constraints = {}
            self.__constraint_evaluators = {}
            if constraints is not None:
                for constraint_name in constraints.keys():
                    # constraints with evaluators aren't handled by the OptQuest JAR
                    if 'evaluator' in constraints[constraint_name].keys():
                        evaluator = constraints[constraint_name]['evaluator']
                        self.__constraint_evaluators[constraint_name] = evaluator
                    else:  # if 'expression' in constraints[constraint_name].keys()
                        new_constraint = COptQuestStringConstraint(constraint_name)
                        expression = constraints[constraint_name]['expression']
                        new_constraint.SetEquation(expression)
                        self.__constraints[constraint_name] = new_constraint

            # define objective(s)
            self.__objectives = {}
            self.__objective_properties = {}
            self.__objective_evaluators = {}
            if self.__is_multi_objective:
                self.__frontierMultiObjective = COptQuestFrontierMultiObjective()

            if objectives is not None:  # if not inferred objective
                self.__inferred_objective = False
                for objective_name in objectives.keys():
                    objective_properties = objectives[objective_name]
                    self.__objective_properties[objective_name] = objective_properties

                    if 'type' in objective_properties.keys():
                        objective_type = objective_properties['type']
                    else:
                        objective_type = 'max'

                    if 'expression' in objective_properties:
                        new_objective = COptQuestStringObjective(objective_properties['expression'])
                    else:
                        new_objective = COptQuestUserControlledObjective(objective_name)
                        self.__objective_evaluators[objective_name] = objective_properties['evaluator']

                    if objective_type == 'max':
                        new_objective.SetMaximize()
                    elif objective_type == 'min':
                        new_objective.SetMinimize()

                    self.__objectives[objective_name] = new_objective

                    if self.__is_multi_objective:
                        self.__frontierMultiObjective.AddObjective(new_objective)

            # set up evaluator
            self.__evaluator = COptQuestOptimizationEvaluator(self.__evaluation_workers_manager,
                                                              self.__status_monitor_wrapper)

            # create optimizer
            self.__optimization = COptQuestOptimization(self.__evaluator, self.__search_parameters)
            self.__optimization.SetLicenseID(self.__license_id)
            if setup_log is not None:
                self.__optimization.LogSetup(setup_log)
            # register input variables with optimization
            for dec_var in self.__dec_vars.values():
                self.__optimization.AddVariable(dec_var)
            # register permutation groups (input variable groups) with optimization
            for perm_group in self.__perm_groups.values():
                self.__optimization.AddPermutationGroup(perm_group)
            # register output variables with optimization
            for output in self.__outputs.values():
                self.__optimization.AddVariable(output)
            # register constraint(s) with optimization
            for constraint in self.__constraints.values():
                self.__optimization.AddConstraint(constraint)
            # register objective(s) with optimization
            if self.__is_multi_objective:
                self.__optimization.AddObjective(self.__frontierMultiObjective)
            elif self.__objectives is not None and len(self.__objectives) == 1:
                the_only_objective = list(self.__objectives.values())[0]
                self.__optimization.AddObjective(the_only_objective)
            else:
                self.__inferred_objective = True
        except Exception as e:
            print("".join(traceback.TracebackException.from_exception(e).format()))

    def __del__(self):
        if self.__setup_log is not None:
            self.__optimization.CloseLogSetupFile()

    def search(self, objective_evaluator=None, n_iter=None, replications=-1, parallel_evaluators=1, suggested_runs=None,
               solutions_log=None):
        """
        Begin searching for solutions. This method will start the optimizer and will run until the specified number of iterations is reached or if the user specified a `user_stop` callback function that stops the optimization.
        :param objective_evaluator: Only pass an argument for this parameter if no objectives were passed to the constructor. This argument should be a function that takes an input dict corresponding to the `search_space` constructor parameter and returns a single numerical value.
        :param n_iter: The total number of iterations to run over the search/input space.
        :param replications: The number of times each input iteration of should be repeated. Only useful for stochastic optimizations (i.e. if non-deterministic functions are involved.) An integer argument specifies the number of replications that should be done per iteration. A tuple argument specified the minimum and maximum range for the number of replications that should be done per iteration. See the README for more info.
        :param parallel_evaluators: The number of evaluators to run in parallel. This is only useful if an argument was passed for the `evaluator` constructor parameter.
        :param suggested_runs: A dict containing solutions to evaluate as the first iterations.
        :return: None
        """

        try:
            if solutions_log is not None:
                self.__optimization.LogSolutions(solutions_log)

            # GFO functionality (if no objective but evaluator is supplied)
            if self.__inferred_objective:
                if objective_evaluator is not None:
                    objective_name = 'objective'
                    new_objective = COptQuestUserControlledObjective(objective_name)
                    self.__objective_evaluators[objective_name] = objective_evaluator
                    new_objective.SetMaximize()
                    self.__objectives[objective_name] = new_objective
                    # register the objective with optquest
                    the_only_objective = list(self.__objectives.values())[0]
                    self.__optimization.AddObjective(the_only_objective)
                else:  # objective_evaluator is None
                    print('At least one objective must be defined, exiting optimization.')
                    return

            # add suggested simulation runs
            if suggested_runs is not None:
                suggested_runs_df = pd.DataFrame(suggested_runs)
                for _, row in suggested_runs_df.iterrows():
                    solution = self.__optimization.CreateSolution()
                    for var_name in suggested_runs_df.columns:
                        var = self.__optimization.GetVariable(var_name)
                        solution.SetVariableValue(var, row[var_name])
                    self.__optimization.AddSuggestedSolution(solution)

            # replications
            if type(replications) is tuple:
                self.__enable_variable_replications(min_reps=replications[0], max_reps=replications[1])
            elif replications > 1:
                self.__optimization.SetUseReplications(True)
                self.__optimization.SetMinimumReplications(replications)

            # stopping conditions
            if n_iter is not None:
                self.__optimization.SetMaximumIterations(n_iter)

            # parallel evaluation
            self.__optimization.SetEvaluate(parallel_evaluators)

            # Start all the evaluator threads, they will pump the unevaluated_queue pulling solutions to evaluate
            for i in range(parallel_evaluators):
                threading.Thread(target=self.__evaluation_worker, daemon=True).start()

            # do optimization
            start_time = time.time()
            self.__optimization.Optimize()
            end_time = time.time()
            self.optimization_time = end_time - start_time

            # terminate threads by passing None to queue
            for _ in range(parallel_evaluators):
                self.__unevaluated_queue.put(None)

            # create pandas dataframe with results
            self.search_data = pd.DataFrame(self.__search_data_list)

            # store best result(s)
            if self.__is_multi_objective:
                for solution in self.__optimization.GetPatternFrontier():
                    # get solution info
                    dec_var_values = {dec_var_name: solution.GetVariableValue(self.__dec_vars[dec_var_name]) for
                                        dec_var_name
                                        in self.__dec_vars.keys()}
                    output_values = {output_name: solution.GetVariableValue(self.__outputs[output_name]) for
                                        output_name
                                        in
                                        self.__outputs.keys()}
                    if not self.__is_multi_objective:
                        objective_values = {list(self.__objectives)[0]: solution.GetObjectiveValue()}
                    else:
                        objective_values = {
                            objective_name: solution.GetObjectiveValue(self.__objectives[objective_name]) for
                            objective_name in self.__objectives.keys()}
                    iteration = solution.GetIteration()
                    replication = solution.GetReplication()

                    self.__best_search_data_list.append(
                        {'iteration': iteration, 'replication': replication, 'feasible': solution.IsFeasible(),
                            **objective_values, **dec_var_values, **output_values})

                # create pandas dataframe with results
                self.best_score = pd.DataFrame(self.__best_search_data_list)
                self.best_para = self.best_score
            else:  # if single objective
                best_solution = self.__optimization.GetBestSolution()
                if best_solution is not None and best_solution.IsFeasible():
                    self.best_score = best_solution.GetObjectiveValue()
                    dec_var_values = {dec_var_name: best_solution.GetVariableValue(self.__dec_vars[dec_var_name])
                                        for
                                        dec_var_name
                                        in self.__dec_vars.keys()}
                    output_values = {output_name: best_solution.GetVariableValue(self.__outputs[output_name]) for
                                        output_name in
                                        self.__outputs.keys()}
                    self.best_para = {**dec_var_values, **output_values}
                else:
                    self.best_score = None
                    self.best_para = None

        except Exception as e:
            msg = "".join(traceback.TracebackException.from_exception(e).format())
            if 'The number of decision variables exceeds the demo limits of 7 variables.' in msg:
                print('OPTIMIZATION FAILED: The number of decision variables exceeds the demo license limits of 7 variables.'
                      'This optimization requires a developer license.', file=sys.stderr)
            else:
                print(msg, file=sys.stderr)
        self.__optimization.CloseSolutionLog()

    def stop_optimization(self):
        # terminate threads by passing None to queue
        for _ in range(self.__optimization.GetEvaluatorCount()):
            self.__unevaluated_queue.put(None)
        self.__optimization.CloseSolutionLog()
        self.__optimization.StopOptimization()

    def __enable_variable_replications(self, min_reps, max_reps, objectives_confidence_level=3, error_percent=0.05):
        """
        Allow OptQuest to execute a range of replications depending on if statistical confidence has been met.
        The minimum number of replications will be executed, and then more replications will be executed until
        either statistical confidence is met OR the maximum number of replications have been executed.

        :param min_reps: the minimum number of replications that will be executed
        :param max_reps: the maximum number of replications that may be executed
        :param objectives_confidence_level: the following "levels" correspond to the given confidence % e.g. (1-alpha)
            1 = 80%
            2 = 90%
            3 = 95%
            4 = 98%
            5 = 99%
            6 = 99.9%
        :param error_percent: the percentage as a value between 0 and 1
        :return: None
        """

        # wrap calls to OptQuest with try-catch
        try:
            # set replication confidence/error on objectives
            for objective_name in self.__objectives:
                objective = self.__objectives[objective_name]
                if 'confidence' in self.__objective_properties[objective_name]:
                    objectives_confidence_level = self.__objective_properties[objective_name]['confidence']
                if 'error' in self.__objective_properties[objective_name]:
                    error_percent = self.__objective_properties[objective_name]['error']
                objective.SetReplicationConfidence(1, objectives_confidence_level, error_percent)

            # set up replications
            self.__optimization.SetUseReplications(True)
            self.__optimization.SetMinimumReplications(min_reps)
            self.__optimization.SetMaximumReplications(max_reps)
        except Exception as e:
            print("".join(traceback.TracebackException.from_exception(e).format()))

    def __evaluation_workers_manager(self, solution):
        if solution is None:
            solution = self.__evaluated_queue.get()  # blocking
            logging.info('completed evaluation of iteration ' + str(solution.GetIteration()) + ' replication ' + str(
                solution.GetReplication()))
            self.__optimization.EvaluateComplete(solution)
        else:
            self.__unevaluated_queue.put(solution)

        # empty out the rest of the queue
        try:
            while not self.__evaluated_queue.empty():
                solution = self.__evaluated_queue.get_nowait()  # non-blocking
                logging.info('clearing completed evaluation of iteration ' + str(
                    solution.GetIteration()) + ' replication ' + str(solution.GetReplication()))
                self.__optimization.EvaluateComplete(solution)
        except queue.Empty:
            pass

    def __evaluation_worker(self):
        while not self.__stop_optimization:
            solution = self.__unevaluated_queue.get()  # blocking

            # None will be passed if optimization is complete to let the process handling this function call exit
            if solution is None:
                break

            logging.info('starting evaluation of iteration' + str(solution.GetIteration()))
            self.__do_evaluation(solution)

    def __do_evaluation(self, solution):
        try:
            # put non-permutation decision variable values into dictionary, keyed by name (permutation groups will be added instead)
            dec_var_values = {}
            # first handle non-permutation variables
            non_perm_dec_vars = [dec_var for dec_var in self.__dec_vars if dec_var not in self.__perm_vars]
            for dec_var_name in non_perm_dec_vars:
                dec_var_values[dec_var_name] = solution.GetVariableValue(self.__dec_vars[dec_var_name])
            # return each permutation group as an element in dec_var_values
            for perm_group_name, perm_group in self.__perm_groups.items():
                perm_group_values = []
                for perm_group_var in perm_group.getVariables().toArray():
                    perm_var_value = solution.GetVariableValue(perm_group_var)
                    perm_group_values.append(perm_var_value)
                dec_var_values[perm_group_name] = perm_group_values

            # run user-defined evaluate function
            output_values = {}
            if self.__user_evaluator is not None:
                output_values = self.__user_evaluator(dec_var_values)
            
            # set OptQuest output values
            for output_name in self.__outputs.keys():
                output = self.__outputs[output_name]
                output_value = output_values[output_name]
                if output_value is not None:
                    solution.SetVariableValue(output, output_value)
                else:
                    solution.RejectSolution()
                    self.__evaluated_queue.put(solution)
                    return

            # check if solution is valid (num_params==1 for inputs only, num_params==2 for inputs and outputs)
            for constraint_evaluator in self.__constraint_evaluators.values():
                num_params = len(signature(constraint_evaluator).parameters)
                if (num_params == 2 and constraint_evaluator(dec_var_values, output_values) is False) or (
                        num_params == 1 and constraint_evaluator(dec_var_values) is False):
                    solution.RejectSolution()
                    self.__evaluated_queue.put(solution)
                    return

            # set OptQuest user-controlled-objective values
            for objective_name in self.__objective_evaluators.keys():
                objective = self.__objectives[objective_name]
                # execute objective function (check if it wants 1 or 2 parameters)
                objective_evaluator = self.__objective_evaluators[objective_name]
                num_params = len(signature(objective_evaluator).parameters)
                if num_params == 1:
                    objective_value = objective_evaluator(dec_var_values)
                else:  # num_params == 2
                    objective_value = objective_evaluator(dec_var_values, output_values)
                if objective_value is not None:
                    solution.SetObjectiveValue(objective, objective_value)
                else:
                    solution.RejectSolution()
                    self.__evaluated_queue.put(solution)
                    return

            self.__evaluated_queue.put(solution)
        except Exception as e:
            print("".join(traceback.TracebackException.from_exception(e).format()))
            solution.RejectSolution()
            self.__evaluated_queue.put(solution)
            self.stop_optimization()


    def __status_monitor_wrapper(self, solution):
        # wrap calls to OptQuest with try-catch
        try:
            # get solution info
            dec_var_values = {dec_var_name: solution.GetVariableValue(self.__dec_vars[dec_var_name]) for dec_var_name in
                              self.__dec_vars.keys()}
            output_values = {output_name: solution.GetVariableValue(self.__outputs[output_name]) for output_name in
                             self.__outputs.keys()}
            if not self.__is_multi_objective:
                objective_values = {list(self.__objectives)[0]: solution.GetObjectiveValue()}
            else:
                objective_values = {objective_name: solution.GetObjectiveValue(self.__objectives[objective_name]) for
                                    objective_name in self.__objectives.keys()}
            iteration = solution.GetIteration()
            replication = solution.GetReplication()

        except Exception as e:
            print("".join(traceback.TracebackException.from_exception(e).format()))

        # store results after every iteration
        self.__search_data_list.append(
            {'iteration': iteration, 'replication': replication, 'feasible': solution.IsFeasible(), **objective_values,
             **dec_var_values, **output_values})

        # run user-defined status_monitor
        if self.__status_monitor is not None:
            self.__status_monitor(inputs=dec_var_values, outputs=output_values, objectives=objective_values,
                                  iteration=iteration, replication=replication)

        # check if user wants to stop the optimization
        if self.__user_stop is not None and self.__user_stop(inputs=dec_var_values, outputs=output_values,
                                                             objectives=objective_values, iteration=iteration,
                                                             replication=replication):
            self.__optimization.StopOptimization()
            self.__stop_optimization = True
            return

    def get__search_parameters(self):
        return self.__search_parameters

    @staticmethod
    def __initialize_optquest(path: str):
        if not InitializeOptQuest(path):
            logging.error('failed to initialize optquest, exiting')
            sys.exit(1)
