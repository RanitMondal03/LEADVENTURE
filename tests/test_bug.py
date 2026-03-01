from Validators.goal_validator import (
    assert_valid_goal_schema,
    validate_goal_response,
validate_na_response
)

from Validators.fake_response import (
    wrong_type_response,
    missing_field_response,
    too_many_key_results,
    too_few_key_results,
    invalid_confidence,
gibberish_response
)


def test_bug_wrong_type():

    result = wrong_type_response()

    assert_valid_goal_schema(result)


def test_bug_missing_field():

    result = missing_field_response()

    assert_valid_goal_schema(result)


def test_bug_too_many_results():

    result = too_many_key_results()

    validate_goal_response(result)


def test_bug_too_few_results():

    result = too_few_key_results()

    validate_goal_response(result)


def test_bug_invalid_confidence():

    result = invalid_confidence()

    validate_goal_response(result)


def test_gibberish_response():
    result = gibberish_response()
    validate_na_response(result)