from typing import List, Dict, Optional

from pulp import LpProblem

from .utils.solver_utils import SolverUtils
from .utils.dataclasses_utils import DataclassesUtils
from .dataclasses import Preference, Indifference, Criterion, DataValidator


class Solver:

    def __init__(self, show_logs: Optional[bool] = False):
        self.name = 'UTA GMS Solver'
        self.show_logs = show_logs

    def __str__(self):
        return self.name

    def get_hasse_diagram_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            number_of_points: Optional[List[int]] = None
    ) -> Dict[str, List[str]]:
        """
        Method for getting hasse diagram dict

        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param number_of_points: default None

        :return direct_relations:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        if number_of_points is None:
            necessary_preference = SolverUtils.get_necessary_relations(
                performance_table_list=refined_performance_table_dict,
                alternatives_id_list=alternatives_id_list,
                preferences=refined_preferences,
                indifferences=refined_indifferences,
                criteria=refined_gains,
                show_logs=self.show_logs
            )

            direct_relations: Dict[str, List[str]] = SolverUtils.calculate_direct_relations(necessary_preference)

            for alternatives_id in alternatives_id_list:
                if alternatives_id not in direct_relations.keys():
                    direct_relations[alternatives_id] = []
        else:
            necessary: Dict[str, List[str]] = {}
            for i in range(len(refined_performance_table_dict)):
                for j in range(len(refined_performance_table_dict)):
                    if i == j:
                        continue

                    problem: LpProblem = SolverUtils.calculate_solved_problem_with_predefined_number_of_characteristic_points(
                        performance_table_list=refined_performance_table_dict,
                        preferences=refined_preferences,
                        indifferences=refined_indifferences,
                        criteria=refined_gains,
                        number_of_points=number_of_points,
                        alternative_id_1=i,
                        alternative_id_2=j,
                        show_logs=self.show_logs
                    )

                    # if problem.variables()[0].varValue <= 0:
                    #     necessary.append([alternatives_id_list[i], alternatives_id_list[j]])
                    if problem.variables()[0].varValue <= 0:
                        if alternatives_id_list[i] not in necessary:
                            necessary[alternatives_id_list[i]] = []
                        necessary[alternatives_id_list[i]].append(alternatives_id_list[j])

            direct_relations: Dict[str, List[str]] = SolverUtils.calculate_direct_relations(necessary)

            for alternatives_id in alternatives_id_list:
                if alternatives_id not in direct_relations.keys():
                    direct_relations[alternatives_id] = []

        return direct_relations

    def get_representative_value_function_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
    ) -> Dict[str, float]:
        """
        Method for getting The Most Representative Value Function

        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects

        :return:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        refined_linear_segments: List[int] = DataclassesUtils.refine_linear_segments(
            criterions=criteria
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        problem: LpProblem = SolverUtils.calculate_the_most_representative_function(
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
            preferences=refined_preferences,
            indifferences=refined_indifferences,
            criteria=refined_gains,
            show_logs=self.show_logs
        )

        variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in problem.variables()}

        alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
            variables_and_values_dict=variables_and_values_dict,
            performance_table_list=refined_performance_table_dict,
            alternatives_id_list=alternatives_id_list,
        )

        return alternatives_and_utilities_dict

    def get_ranking_dict(
            self,
            performance_table_dict: Dict[str, Dict[str, float]],
            preferences: List[Preference],
            indifferences: List[Indifference],
            criteria: List[Criterion],
            number_of_points: Optional[List[int]] = None
    ) -> Dict[str, float]:
        """
        Method for getting ranking dict

        :param performance_table_dict:
        :param preferences: List of Preference objects
        :param indifferences: List of Indifference objects
        :param criteria: List of Criterion objects
        :param number_of_points: default None

        :return alternatives_and_utilities_dict:
        """
        DataValidator.validate_criteria(performance_table_dict, criteria)
        DataValidator.validate_performance_table(performance_table_dict)

        refined_performance_table_dict: List[List[float]] = DataclassesUtils.refine_performance_table_dict(
            performance_table_dict=performance_table_dict
        )

        refined_preferences: List[List[int]] = DataclassesUtils.refine_preferences(
            performance_table_dict=performance_table_dict,
            preferences=preferences
        )

        refined_indifferences: List[List[int]] = DataclassesUtils.refine_indifferences(
            performance_table_dict=performance_table_dict,
            indifferences=indifferences
        )

        refined_gains: List[bool] = DataclassesUtils.refine_gains(
            criterions=criteria
        )

        alternatives_id_list: List[str] = list(performance_table_dict.keys())

        if number_of_points is None:
            problem: LpProblem = SolverUtils.calculate_solved_problem(
                performance_table_list=refined_performance_table_dict,
                preferences=refined_preferences,
                indifferences=refined_indifferences,
                criteria=refined_gains,
                show_logs=self.show_logs
            )

            variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in
                                                           problem.variables()}

            alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
                variables_and_values_dict=variables_and_values_dict,
                performance_table_list=refined_performance_table_dict,
                alternatives_id_list=alternatives_id_list,
            )
        else:
            problem: LpProblem = SolverUtils.calculate_solved_problem_with_predefined_number_of_characteristic_points(
                performance_table_list=refined_performance_table_dict,
                preferences=refined_preferences,
                indifferences=refined_indifferences,
                criteria=refined_gains,
                number_of_points=number_of_points,
                show_logs=self.show_logs
            )

            variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in
                                                           problem.variables()}

            u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(refined_performance_table_dict)

            characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
                number_of_points, refined_performance_table_dict, u_list_dict
            )

            alternatives_and_utilities_dict: Dict[
                str, float] = SolverUtils.get_alternatives_and_utilities_using_interpolation_dict(
                variables_and_values_dict=variables_and_values_dict,
                performance_table_list=refined_performance_table_dict,
                characteristic_points=characteristic_points,
                alternatives_id_list=alternatives_id_list,
            )

        return alternatives_and_utilities_dict
