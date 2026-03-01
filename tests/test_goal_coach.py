import pytest
from utils.goal_coach import GoalCoach
from Validators.goal_validator import validate_goal_response


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.smoke
def test_valid_goal(coach):

    result = coach.make_goal("I want to improve in marks in Maths")

    validate_goal_response(result)


@pytest.mark.sanity
def test_key_results_count(coach):

    result = coach.make_goal("I want to get fit and ripped")

    validate_goal_response(result)


@pytest.mark.smoke
def test_multiple_inputs(coach):

    goals = [
        "increase revenue",
        "learn python",
        "be better",
    ]

    for g in goals:
        result = coach.make_goal(g)

        validate_goal_response(result)