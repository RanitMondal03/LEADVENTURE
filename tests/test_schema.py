
from jsonschema import validate, ValidationError
import pytest
from utils.goal_coach import GoalCoach


@pytest.fixture
def coach():
    return GoalCoach()


schema = {
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


@pytest.mark.smoke
def test_schema_validation(coach):
    result = coach.make_goal("I want to improve in MATHS")
    try:
        validate(instance=result, schema=schema)
    except ValidationError as e:
        assert False, (
            f"Schema validation failed!\n"
            f"Field   : {' -> '.join(str(p) for p in e.absolute_path)}\n"
            f"Message : {e.message}\n"
            f"Expected: {e.schema}\n"
            f"Actual  : {e.instance}"
        )


