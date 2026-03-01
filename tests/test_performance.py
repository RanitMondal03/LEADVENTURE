import time
import pytest
from utils.goal_coach import GoalCoach
from Validators.goal_validator import assert_response_time


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.regression
def test_response_time(coach):

    start = time.time()

    response = coach.make_goal("I want to learn Piano")

    end = time.time()

    duration = end - start

    assert response is not None
    assert_response_time(duration, max_time=10)

    print(f"START TIME IS {start} ------ END TIME IS {end}")
    print(f"TOTAL TIME IS {duration}")

