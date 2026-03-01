import pytest
from utils.goal_coach import GoalCoach
from Validators.goal_validator import validate_goal_response


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.smoke
def test_valid_goal(coach):

    result = coach.make_goal("I want to improve in Maths")

    validate_goal_response(result)