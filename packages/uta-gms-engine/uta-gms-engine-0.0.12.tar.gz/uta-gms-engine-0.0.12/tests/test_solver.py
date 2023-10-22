import pytest

from src.utagmsengine.solver import Solver
from src.utagmsengine.dataclasses import Preference, Indifference, Criterion


@pytest.fixture()
def performance_table_dict_dummy():
    return {
        'A': {'g1': 26.0, 'g2': 40.0, 'g3': 44.0},
        'B': {'g1': 2.0, 'g2': 2.0, 'g3': 68.0},
        'C': {'g1': 18.0, 'g2': 17.0, 'g3': 14.0},
        'D': {'g1': 35.0, 'g2': 62.0, 'g3': 25.0},
        'E': {'g1': 7.0, 'g2': 55.0, 'g3': 12.0},
        'F': {'g1': 25.0, 'g2': 30.0, 'g3': 12.0},
        'G': {'g1': 9.0, 'g2': 62.0, 'g3': 88.0},
        'H': {'g1': 0.0, 'g2': 24.0, 'g3': 73.0},
        'I': {'g1': 6.0, 'g2': 15.0, 'g3': 100.0},
        'J': {'g1': 16.0, 'g2': 9.0, 'g3': 0.0},
        'K': {'g1': 26.0, 'g2': 17.0, 'g3': 17.0},
        'L': {'g1': 62.0, 'g2': 43.0, 'g3': 0.0}
    }


@pytest.fixture()
def preferences_dummy():
    return [Preference(superior='G', inferior='F'), Preference(superior='F', inferior='E')]


@pytest.fixture()
def indifferences_dummy():
    return [Indifference(equal1='D', equal2='G')]


@pytest.fixture()
def criterions_dummy():
    return [Criterion(criterion_id='g1', gain=True), Criterion(criterion_id='g2', gain=True), Criterion(criterion_id='g3', gain=True)]


@pytest.fixture()
def number_of_points_dummy():
    return [3, 3, 3]


@pytest.fixture()
def hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B'], 'K': ['C'], 'L': ['J'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def representative_value_function_dict_dummy():
    return {'E': 0.0, 'J': 0.0, 'C': 0.25, 'F': 0.25, 'L': 0.25, 'B': 0.5, 'H': 0.5, 'K': 0.5, 'A': 0.75, 'D': 0.75, 'G': 0.75, 'I': 0.75}


@pytest.fixture()
def predefined_hasse_diagram_dict_dummy():
    return {'A': ['F', 'K'], 'C': ['J'], 'D': ['G'], 'F': ['E', 'J'], 'G': ['B', 'D', 'F', 'H', 'K'], 'I': ['B', 'J'], 'K': ['C'], 'L': ['C', 'E'], 'B': [], 'E': [], 'H': [], 'J': []}


@pytest.fixture()
def ranking_dict_dummy():
    return {'B': 0.0, 'E': 0.0, 'H': 0.0, 'I': 0.0, 'A': 0.5, 'C': 0.5, 'F': 0.5, 'J': 0.5, 'K': 0.5, 'L': 0.5, 'D': 1.0, 'G': 1.0}


@pytest.fixture()
def predefined_linear_segments_ranking_dict_dummy():
    return {'J': 0.21243561290322582, 'E': 0.23637411, 'C': 0.40256550451612905, 'L': 0.41313716433333336, 'F': 0.47213700000000003, 'K': 0.543835190967742, 'H': 0.584198, 'B': 0.6107524516129033, 'I': 0.6638613548387097, 'D': 0.7079016300000001, 'G': 0.7079016300000001, 'A': 0.8604244123010754}


def test_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy
    )

    assert hasse_diagram_list == hasse_diagram_dict_dummy


def test_get_representative_value_function_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        representative_value_function_dict_dummy
):
    solver = Solver(show_logs=True)

    representative_value_function_dict = solver.get_representative_value_function_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy
    )

    assert representative_value_function_dict == representative_value_function_dict_dummy


def test_get_ranking_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        ranking_dict_dummy,
):
    solver = Solver(show_logs=True)

    ranking = solver.get_ranking_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy
    )

    assert ranking == ranking_dict_dummy


def test_predefined_get_ranking_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        number_of_points_dummy,
        predefined_linear_segments_ranking_dict_dummy
):
    solver = Solver(show_logs=True)

    ranking_predefined_number_of_linear_segments = solver.get_ranking_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        number_of_points_dummy
    )

    assert ranking_predefined_number_of_linear_segments == predefined_linear_segments_ranking_dict_dummy


def test_predefined_get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        number_of_points_dummy,
        predefined_hasse_diagram_dict_dummy
):
    solver = Solver(show_logs=True)

    hasse_diagram_list = solver.get_hasse_diagram_dict(
        performance_table_dict_dummy,
        preferences_dummy,
        indifferences_dummy,
        criterions_dummy,
        number_of_points_dummy
    )

    assert hasse_diagram_list == predefined_hasse_diagram_dict_dummy
