import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    """Fixture to provide a fresh GoalCoach instance for each test."""
    return GoalCoach()


@pytest.mark.smoke
def test_valid_goal(coach):

    result = coach.make_goal("I want to improve in marks in Maths")
    assert result["confidence_score"] <= 10

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    assert isinstance(result["key_results"], list)
    assert 1 <= result["confidence_score"] <= 10


@pytest.mark.sanity
def test_key_results_count(coach):

    result = coach.make_goal("I want to get fit")
    print(result)


    assert 3 <= len(result["key_results"]) <= 5


@pytest.mark.sanity
def test_confidence_for_nonsense(coach):

    result = coach.make_goal("asdfghjkl qwerty 123")

    assert result["confidence_score"] <= 3


@pytest.mark.sanity
def test_empty_input(coach):

    result = coach.make_goal("")

    assert result["confidence_score"] <= 3


@pytest.mark.smoke
def test_multiple_inputs(coach):

    goals = [
        "increase revenue",
        "learn python",
        "be better",
    ]

    for g in goals:
        result = coach.make_goal(g)
        assert "refined_goal" in result