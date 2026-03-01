from jsonschema import validate, ValidationError


def validate_goal_response(result):
    """Basic schema validation used for normal cases."""
    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    assert isinstance(result["key_results"], list)

    assert 1 <= result["confidence_score"] <= 10
    assert 3 <= len(result["key_results"]) <= 5


def validate_confidence_low(result):
    """Assert that the confidence score is low (<=3)."""
    assert "confidence_score" in result
    assert result["confidence_score"] <= 3


def validate_na_response(result: object) -> None:

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    assert result["refined_goal"] == "NA"
    assert result["key_results"] == "NA"
    assert result["confidence_score"] <= 3


def validate_no_extra_fields(result, forbidden=None):
    if forbidden is None:
        forbidden = []
    for f in forbidden:
        assert f not in result




goal_schema = {
    "type": "object",
    "properties": {
        "refined_goal": {"type": "string"},
        "key_results": {
            "type": "array",
            "minItems": 3,
            "maxItems": 5,
            "items": {"type": "string"}
        },
        "confidence_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10
        }
    },
    "required": ["refined_goal", "key_results", "confidence_score"]
}


def assert_valid_goal_schema(result):

    try:
        validate(instance=result, schema=goal_schema)

    except ValidationError as e:
        raise AssertionError(
            f"\nSchema validation failed!\n"
            f"Field   : {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"Message : {e.message}\n"
            f"Expected: {e.schema}\n"
            f"Actual  : {e.instance}"
        )

def assert_response_time(duration, max_time=10):

    assert duration < max_time, (
        f"Response too slow! "
        f"Expected < {max_time}s but got {duration:.2f}s"
    )