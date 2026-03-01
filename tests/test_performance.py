import time
import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.regression
def test_response_time(coach):

    start = time.time()

    response = coach.make_goal("I want to learn Piano")
    assert response is not None

    end = time.time()

    assert end - start < 10

    print(f"START TIME IS {start}    ------     END TIME IS  {end}")
    print(f"TOTAL TIME IS {end-start}")

