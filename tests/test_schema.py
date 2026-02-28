
from jsonschema import validate, ValidationError
from utils.goal_coach import GoalCoach

coach = GoalCoach()


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


def test_schema_validation():
    result = coach.make_goal("I want to improve in sales")

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
def test_abcd():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'

    RESET = '\033[0m'

    print(BLACK + "black" + RESET)
    print(RED + "red" + RESET)
    print(GREEN + "green" + RESET)
    print(YELLOW + "yellow" + RESET)
    print(BLUE + "blue" + RESET)
    print(MAGENTA + "magenta" + RESET)
    print(CYAN + "cyan" + RESET)
    print(LIGHT_GRAY + "light gray" + RESET)
    print(DARK_GRAY + "dark gray" + RESET)
    print(BRIGHT_RED + "bright red" + RESET)
    print(BRIGHT_GREEN + "bright green" + RESET)
    print(BRIGHT_YELLOW + "bright yellow" + RESET)
    print(BRIGHT_BLUE + "bright blue" + RESET)
    print(BRIGHT_MAGENTA + "bright magenta" + RESET)
    print(BRIGHT_CYAN + "bright cyan" + RESET)
    print(WHITE + "white" + RESET)

