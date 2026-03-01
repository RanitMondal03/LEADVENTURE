def wrong_type_response():
    return {
        "refined_goal": 123,
        "key_results": "not a list",
        "confidence_score": "high"
    }


def missing_field_response():
    return {
        "refined_goal": "test",
        "confidence_score": 5
    }


def too_many_key_results():
    return {
        "refined_goal": "test",
        "key_results": ["a", "b", "c", "d", "e", "f"],
        "confidence_score": 5
    }


def too_few_key_results():
    return {
        "refined_goal": "test",
        "key_results": ["a"],
        "confidence_score": 5
    }


def invalid_confidence():
    return {
        "refined_goal": "test",
        "key_results": ["a", "b", "c"],
        "confidence_score": 50
    }

def gibberish_response():
    return {
        "refined_goal": "This is a non gibberish statement",
        "key_results": ["non gibrish ", "ANCsdfds", "UGuhf"],
        "confidence_score": 10
    }