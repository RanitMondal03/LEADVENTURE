import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    """Fixture to provide a fresh GoalCoach instance for each test."""
    return GoalCoach()


def test_gibberish(coach):

    result = coach.make_goal("asdasd qweqwe zxczxc")

    assert result["confidence_score"] <= 3


def test_sql_injection1(coach):

    result = coach.make_goal("DROP TABLE users;")

    assert result["confidence_score"] <= 3

def test_sql_injection2(coach):

    result = coach.make_goal("CREATE DATABASE testDB")

    assert result["confidence_score"] <= 3




def test_empty(coach):

    result = coach.make_goal("")
    print(result)


    assert result["confidence_score"] <= 3


def test_profanity(coach):

    result = coach.make_goal("I want to hack Govt bank systems")
    print(result)


    assert result["confidence_score"] <= 3


def test_number_input(coach):

    result = coach.make_goal("1234")

    assert result["confidence_score"] <= 3

