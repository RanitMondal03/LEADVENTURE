import pytest
from utils.goal_coach import GoalCoach
from Validators.goal_validator import assert_valid_goal_schema


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.smoke
def test_schema_validation(coach):

    result = coach.make_goal("I want to improve in MATHS")

    assert_valid_goal_schema(result)