from utils.goal_coach import GoalCoach


coach = GoalCoach()


def test_valid_goal():

    result = coach.make_goal("I want to improve in marks in Maths")
    assert result["confidence_score"] <= 10

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    assert isinstance(result["key_results"], list)
    assert 1 <= result["confidence_score"] <= 10


def test_key_results_count():

    result = coach.make_goal("I want to get fit")
    print(result)


    assert 3 <= len(result["key_results"]) <= 5


def test_confidence_for_nonsense():

    result = coach.make_goal("asdfghjkl qwerty 123")

    assert result["confidence_score"] <= 3


def test_empty_input():

    result = coach.make_goal("")

    assert result["confidence_score"] <= 3


def test_multiple_inputs():

    goals = [
        "increase revenue",
        "learn python",
        "be better",
    ]

    for g in goals:
        result = coach.make_goal(g)
        assert "refined_goal" in result