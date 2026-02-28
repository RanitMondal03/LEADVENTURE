import time
import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    """Fixture to provide a fresh GoalCoach instance for each test."""
    return GoalCoach()


@pytest.mark.regression
def test_response_time(coach):

    start = time.time()

    response = coach.make_goal("Improve sales")


    end = time.time()

    assert end - start < 10

    print(f"START TIME IS {start}    ------     END TIME IS  {end}")
    print(f"TOTAL TIME IS {end-start}")

