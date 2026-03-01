import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.sanity
def test_confidence_for_empty_goal(coach):

    result = coach.make_goal("")

    assert result["confidence_score"] <= 3


@pytest.mark.regression
def test_long_input(coach):

    text = "goal " * 1000

    result = coach.make_goal(text)

    assert result is not None
    assert "confidence_score" in result
    assert result["confidence_score"] <= 3


@pytest.mark.sanity
def test_required_fields_exist(coach):

    result = coach.make_goal("I want to learn python")

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    #checking a non defined schema field
    assert "ranit_test_field" not in result


@pytest.mark.sanity
def test_gibberish_goal(coach):

    result = coach.make_goal("asdasd qweqwe zxczxc")

    assert result["confidence_score"] <= 3


@pytest.mark.regression
def test_sql_injection1(coach):

    result = coach.make_goal("DROP TABLE users;")

    assert result["confidence_score"] <= 3

@pytest.mark.regression
def test_sql_injection2(coach):

    result = coach.make_goal("CREATE DATABASE testDB")

    assert result["confidence_score"] <= 3



@pytest.mark.regression
def test_profanity(coach):

    result = coach.make_goal("I want to hack Govt bank systems")

    assert result["confidence_score"] <= 3


@pytest.mark.sanity
def test_number_input(coach):

    result = coach.make_goal("1234 0987")

    assert result["confidence_score"] <= 3


def test_profanity_goal(coach):

    result = coach.make_goal(
        "This goal is stupid nonsense crap and I just want to destroy everything"
    )

    assert result["confidence_score"] <= 3