import pytest
from utils.goal_coach import GoalCoach
from utils.ai_client import AIClient


@pytest.fixture
def coach():
    return GoalCoach()


#key_results Length Incorrect
@pytest.mark.regression
def test_insufficient_key_results(coach):
    mock_response = '''{
  "refined_goal": "Get fit",
  "key_results": ["run daily"],
  "confidence_score": 8
}'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("get fit")
    
    assert len(result["key_results"]) >= 3, "key_results must have at least 3 items"



#key_results Length Incorrect
@pytest.mark.regression
def test_excessive_key_results(coach):
    """Bug 2 variant: AI returns more than 5 key_results."""
    mock_response = '''{
  "refined_goal": "Get fit",
  "key_results": ["run", "walk", "swim", "cycle", "stretch", "meditate"],
  "confidence_score": 8
}'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("get fit")
    
    assert len(result["key_results"]) <= 5, "key_results must have at most 5 items"


@pytest.mark.regression
def test_confidence_too_high(coach):
    mock_response = '''{
  "refined_goal": "Improve sales",
  "key_results": ["increase revenue", "boost team", "client retention"],
  "confidence_score": 15
}'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("improve sales")
    
    assert 1 <= result["confidence_score"] <= 10, \
        f"confidence_score must be 1-10, got {result['confidence_score']}"


@pytest.mark.regression
def test_confidence_too_low(coach):
    mock_response = '''{
  "refined_goal": "Improve sales",
  "key_results": ["increase revenue", "boost team", "client retention"],
  "confidence_score": 0
}'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("improve sales")
    
    assert 1 <= result["confidence_score"] <= 10, \
        f"confidence_score must be 1-10, got {result['confidence_score']}"



@pytest.mark.regression
def test_api_failure_handling(coach):
    call_count = [0]

    def failing_send_prompt(prompt, retries=1):
        call_count[0] += 1
        if call_count[0] < retries:
            raise Exception("Simulated API 429 - rate limit")
        return '''{
  "API rate limit has exceded "
}'''

    coach.ai.send_prompt = failing_send_prompt

    result = coach.make_goal("test goal")
    assert "refined_goal" in result



@pytest.mark.regression
def test_missing_env_variables(monkeypatch, coach):
    monkeypatch.setenv("HUGGINGFACE_API_KEY", "")
    monkeypatch.delenv("AI_BASE_URL", raising=False)
    monkeypatch.setenv("AI_MODEL", "test-model")
    
    with pytest.raises(ValueError, match="AI_BASE_URL"):
        AIClient()

    result = coach.make_goal("Learn Yoga")



@pytest.mark.regression
def test_json_Schema(coach):
    mock_response = '''```json
{
  "refined_goal": "Improve sales and revenue",
  "key_results": ["increase revenue", "boost team", "client retention"],
  "confidence_score": 7
}
```'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("improve sales")
    
    assert result["refined_goal"] == "Improve sales and revenue"
    assert len(result["key_results"]) == 3
    assert result["confidence_score"] == 7


@pytest.mark.regression
def test_json_code_with_extra_whitespace(coach):
    mock_response = '''```json

{
  "refined_goal": "Complete project",
  "key_results": ["fix bugs", "add features", "write docs"],
  "confidence_score": 6
}

```'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("complete maths project")
    
    assert "refined_goal" in result
    assert isinstance(result["key_results"], list)
    assert 3 <= len(result["key_results"]) <= 5
    assert result["confidence_score"] == 6




@pytest.mark.regression
def test_bug_security_sql_injection(coach):
    malicious_inputs = [
        "DROP TABLE users;",
        "'; DELETE FROM users; --",
        "CREATE DATABASE testDB"
    ]
    
    for sql in malicious_inputs:
        result = coach.make_goal(sql)
        assert result["confidence_score"] <= 3
        assert result["key_results"] == 'NA'
        assert result["refined_goal"] == 'NA'


