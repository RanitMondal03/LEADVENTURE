import pytest
from unittest.mock import patch
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    return GoalCoach()


# simulate bug in API response
@pytest.mark.smoke
def test_valid_goal_with_bug(coach):

    bug_response = {
        "refined_goal": "test",
        "key_results": [],
        "confidence_score": 50   # BUG (invalid)
    }

    with patch.object(GoalCoach, "make_goal", return_value=bug_response):

        result = coach.make_goal("I want to improve in Maths")

        # same checks as your real test
        assert result["confidence_score"] <= 10
        assert "refined_goal" in result
        assert "key_results" in result
        assert "confidence_score" in result
        assert isinstance(result["key_results"], list)
        assert 1 <= result["confidence_score"] <= 10