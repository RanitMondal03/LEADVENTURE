import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    """Fixture to provide a fresh GoalCoach instance for each test."""
    return GoalCoach()


# -----------------------------
# BUG 1 - nonsense input should have low confidence
# -----------------------------
def test_confidence_for_nonsense(coach):

    result = coach.make_goal("asdfghjkl qwerty 123")


    assert result["confidence_score"] <= 3


# -----------------------------
# BUG 2 - empty input should not give high confidence
# -----------------------------
def test_confidence_for_empty(coach):

    result = coach.make_goal("")

    assert result["confidence_score"] <= 3


# -----------------------------
# BUG 3 - very long input should not crash
# -----------------------------
def test_long_input(coach):

    text = "goal " * 1000

    result = coach.make_goal(text)

    assert result is not None
    assert "confidence_score" in result
    assert result["confidence_score"] <= 3



# -----------------------------
# BUG 4 - response must contain required fields
# -----------------------------
def test_required_fields_exist(coach):

    result = coach.make_goal("I want to learn python")

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result
    assert "test_field" not in result

