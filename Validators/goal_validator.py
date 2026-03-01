def validate_goal_response(result):

    assert "refined_goal" in result
    assert "key_results" in result
    assert "confidence_score" in result

    assert isinstance(result["key_results"], list)

    assert 1 <= result["confidence_score"] <= 10
    assert 3 <= len(result["key_results"]) <= 5