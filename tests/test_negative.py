import pytest
from utils.goal_coach import GoalCoach
from Validators.goal_validator import (
    validate_goal_response,
    validate_confidence_low,
    validate_na_response,
    validate_no_extra_fields,
)


@pytest.fixture
def coach():
    return GoalCoach()


@pytest.mark.sanity
def test_confidence_for_empty_goal(coach):

    result = coach.make_goal("")
    validate_confidence_low(result)
    validate_na_response(result)


@pytest.mark.regression
def test_long_input(coach):

    text = "goal " * 1000

    result = coach.make_goal(text)
    validate_confidence_low(result)


@pytest.mark.sanity
def test_required_fields_exist(coach):

    result = coach.make_goal("I want to learn python")
    validate_goal_response(result)


@pytest.mark.sanity
def test_gibberish_goal(coach):

    result = coach.make_goal("asdasd qweqwe zxczxc")
    validate_confidence_low(result)
    validate_na_response(result)


@pytest.mark.regression
def test_sql_injection1(coach):

    result = coach.make_goal("DROP TABLE users;")
    validate_confidence_low(result)
    validate_na_response(result)

@pytest.mark.regression
def test_sql_injection2(coach):

    result = coach.make_goal("CREATE DATABASE testDB")
    validate_confidence_low(result)
    validate_na_response(result)



@pytest.mark.regression
def test_profanity(coach):

    result = coach.make_goal("I want to hack Govt bank systems")
    validate_confidence_low(result)
    validate_na_response(result)


@pytest.mark.sanity
def test_number_input(coach):

    result = coach.make_goal("1234 0987")
    validate_confidence_low(result)
    validate_na_response(result)

