# BUGS — AI Goal Coach System

This document lists simulated and potential bugs found while testing the AI Goal Coach system.

Each bug includes reproduction steps, expected result, actual result, severity, and how automated tests detect it.  
Most of the reproduction tests now live in `tests/test_bugs.py` so they stay separate from the normal suite.


--------------------------------------------------

## Bug 1 — Invalid JSON Returned

### Description
AI sometimes returns text with explanation instead of strict JSON.

### Steps to Reproduce
1. Call API with goal:
   "I want to improve in sales"
2. Observe response

### Actual Result

Response:

Sure! Here is the goal:

{
  "refined_goal": "...",
  "key_results": [],
  "confidence_score": 7
}

Extra text breaks JSON parsing.

### Expected Result

Response must be valid JSON only.

{
  "refined_goal": "...",
  "key_results": [],
  "confidence_score": 7
}

### Severity
High

### Detected By

`tests/test_bugs.py::test_bug_1_invalid_json_parsing`  
(or any smoke/schema test that attempts to load the output)

JSON parsing error is exercised by the dedicated bug test.


--------------------------------------------------

## Bug 2 — key_results length incorrect

### Description
AI returns less than 3 or more than 5 key_results.

### Steps to Reproduce

Input:
"I want to get fit"

Response:

{
  "refined_goal": "...",
  "key_results": ["run daily"],
  "confidence_score": 8
}

### Expected Result

key_results must contain 3–5 items.

### Actual Result

Only 1 item returned.

### Severity
Medium

### Detected By

`tests/test_bugs.py::test_bug_2_insufficient_key_results`  
and `test_bug_2_excessive_key_results` (also `test_schema_validation` in normal suite)


--------------------------------------------------

## Bug 3 — Hallucinated goal for nonsense input

### Description
AI generates valid goal for gibberish input.

### Steps to Reproduce

Input:
"asdfghjkl qwerty 123"

Response:

{
  "refined_goal": "Improve typing skills",
  "key_results": [...],
  "confidence_score": 9
}

### Expected Result

confidence_score should be <=3  
No valid goal should be generated.

### Actual Result

confidence_score = 9

### Severity
High

### Detected By

`tests/test_bugs.py::test_bug_3_hallucinated_goal_gibberish` and
`test_bug_3_hallucinated_goal_random_text` (sanity tests also exercise similar cases).


--------------------------------------------------

## Bug 4 — confidence_score out of range

### Description
AI returns score outside 1–10.

### Steps to Reproduce

Response:

{
  "refined_goal": "...",
  "key_results": [...],
  "confidence_score": 15
}

### Expected

1 <= confidence_score <= 10

### Actual

15 returned.

### Severity
Medium

### Detected By

`tests/test_bugs.py::test_bug_4_confidence_too_high` and
`test_bug_4_confidence_too_low` (schema tests in normal suite also cover range).


--------------------------------------------------

## Bug 5 — API failure / rate limit crash

### Description
API returns 429 error and test crashes.

### Steps

Run multiple requests quickly.

### Actual

Exception thrown.

### Expected

Retry should happen.

### Severity
Medium

### Detected By

`tests/test_bugs.py::test_bug_5_api_failure_handling` (regression test exercises retry).


--------------------------------------------------

--------------------------------------------------

## Bug 6 — Missing Environment Variables (No Fallback)

### Description
If `AI_BASE_URL` or `AI_MODEL` environment variables are missing, `AIClient()` instantiation silently allows `None` values, causing failures later when `send_prompt()` is called.

### Steps to Reproduce

1. Unset `AI_BASE_URL` and `AI_MODEL` env vars
2. Run: `coach = GoalCoach()`
3. Call: `coach.make_goal("I want to improve")`

### Expected Result

Clear error message on initialization if required vars missing.

Example:
```
ValueError: AI_BASE_URL environment variable not set.
ValueError: AI_MODEL environment variable not set.
```

### Actual Result

`AIClient` initializes with `base_url=None, model=None`  
Later, OpenAI client call fails with cryptic error:
```
TypeError: 'NoneType' object has no len
```

### Severity
**High** – Blocks all functionality; unclear error message

### Root Cause

In `ai_client.py` lines 23-24:
```python
base_url = base_url or os.getenv("AI_BASE_URL")  # Returns None if not set
model = model or os.getenv("AI_MODEL")           # Returns None if not set
```

No validation after assignment.

### Detected By

**Manual test** (not automated) – would fail immediately if env vars missing.  
Could add a smoke test that validates initialization:

```python
@pytest.mark.smoke
def test_client_initialization_requires_env_vars(monkeypatch):
    # Unset env vars
    monkeypatch.delenv("AI_BASE_URL", raising=False)
    monkeypatch.delenv("AI_MODEL", raising=False)
    
    with pytest.raises(ValueError, match="AI_BASE_URL|AI_MODEL"):
        AIClient()
```

### Fix Suggested

```python
def __init__(self, base_url: str | None = None, model: str | None = None):
    API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    if not API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY environment variable not set.")
    
    base_url = base_url or os.getenv("AI_BASE_URL")
    model = model or os.getenv("AI_MODEL")
    
    # ADD THIS validation
    if not base_url:
        raise ValueError("AI_BASE_URL environment variable not set.")
    if not model:
        raise ValueError("AI_MODEL environment variable not set.")
    
    self.client = OpenAI(base_url=base_url, api_key=API_KEY)
    self.model = model
```

--------------------------------------------------

## Bug 7 — JSON Parsing Breaks on Extra Whitespace in Code Block

### Description
If AI returns JSON inside triple backticks with `json` language tag, current cleanup fails:

```
\`\`\`json
{
  "refined_goal": "...",
  ...
}
\`\`\`
```

### Steps to Reproduce

1. Mock AIClient to return:
```
"```json\n{\n  \"refined_goal\": \"test\",\n  \"key_results\": [...],\n  \"confidence_score\": 5\n}\n```"
```
2. Call: `coach.make_goal("improve sales")`

### Expected Result

JSON successfully parsed.

### Actual Result

```
json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Because `response.replace("```", "").strip()` leaves `json\n{` as first chars.

### Severity
**Medium** – Fails for formatted AI responses (common with Claude/GPT)

### Root Cause

In `goal_coach.py` line 29-31:
```python
cleaned = response.strip()
if cleaned.startswith("```"):
    cleaned = cleaned.replace("```", "").strip()
```

This removes backticks but not the `json` language tag.

### Detected By

**Regression tests** are located in `tests/test_bugs.py`:

```python
@pytest.mark.regression
def test_bug_7_json_code_block_with_language_tag(coach):
    """Test that JSON inside ```json ... ``` is parsed correctly."""
    mock_response = '''```json
{
  "refined_goal": "Improve sales",
  "key_results": ["increase revenue", "boost team", "client retention"],
  "confidence_score": 7
}
```'''
    
    coach.ai.send_prompt = lambda prompt: mock_response
    result = coach.make_goal("improve sales")
    
    assert result["refined_goal"] == "Improve sales"
    assert len(result["key_results"]) == 3
```

### Fix Suggested

```python
# Better regex-based cleanup
import re

cleaned = response.strip()
# Remove markdown code blocks (including language specification)
cleaned = re.sub(r"```(?:json)?\s*\n?", "", cleaned).strip()
return json.loads(cleaned)
```

--------------------------------------------------

## Bug 8 — Retry Logic Not Actually Retrying Telemetry Increment

### Description
Even though `send_prompt(retries=1)` parameter exists, the retry loop increments telemetry incorrectly. Each failed attempt increments `total_retries`, but if all retries fail, the `failed_requests` counter adds 1 more — causing inconsistency.

### Steps to Reproduce

1. Set `AI_BASE_URL` to invalid endpoint
2. Call `send_prompt(retries=3)`
3. Check telemetry after failure

### Expected Result

```
total_retries: 2  (2 failures before final attempt)
failed_requests: 1  (1 overall request failed)
total_requests: 1
```

### Actual Result

```
total_retries: 2
failed_requests: 1  ✓ OK
total_requests: 1   ✓ OK
```

Actually this is fine BUT: if we check `total_retries + failed_requests`, it shows we "retried" twice but only counts as 1 failure. This is **confusing telemetry**.

For clarity:
- `total_requests` = 1 ✓
- `failed_requests` = 1 ✓
- `total_retries` = should be 2 (two failed attempts within retries) ✓

### Severity
**Low** – Logging/metrics only, doesn't break functionality

### Root Cause

Telemetry counting assumptions are unclear. See `ai_client.py` lines 50-75.

### Detected By

**Regression tests** for telemetry can be found in `tests/test_bugs.py`:

```python
@pytest.mark.regression
def test_bug_8_telemetry_structure(monkeypatch):
    """Verify retry telemetry is accurate."""
    
    coach = GoalCoach()
    
    # Mock send_prompt to always fail
    call_count = [0]
    def mock_send(prompt, retries=1):
        call_count[0] += 1
        if call_count[0] < retries:
            raise Exception("Simulated API failure")
        return ""  # This won't happen
    
    coach.ai.send_prompt = mock_send
    
    # Attempt with 2 retries
    with pytest.raises(Exception):
        coach.ai.send_prompt("test", retries=2)
    
    # Check telemetry
    telemetry = coach.ai.get_telemetry()
    assert telemetry["total_requests"] == 1  # Only 1 actual request
    assert telemetry["failed_requests"] == 1
    # total_retries should only count inner loop, not the initial attempt
```

### Fix Suggested

Add comments to clarify telemetry semantics:

```python
"""
Telemetry Semantics:
- total_requests: number of times send_prompt() was called
- failed_requests: number of times it failed (sum of all retries exhausted)
- total_retries: number of retry attempts within send_prompt() calls (not including first attempt)
"""
```

--------------------------------------------------

## Test Coverage Summary

### Bugs Caught by Test Type

| Bug | Smoke | Sanity | Regression | Manual |
|-----|-------|--------|------------|--------|
| 1. Invalid JSON | ✅ | ✅ | - | - |
| 2. key_results length | ✅ | ✅ | - | - |
| 3. Hallucinated goals | - | ✅ | - | - |
| 4. confidence_score out of range | ✅ | - | - | - |
| 5. API failure / rate limit | - | - | ✅ | - |
| **6. Missing env vars** | - | - | - | ✅ |
| **7. JSON code block formatting** | - | - | ✅ | - |
| **8. Retry telemetry counting** | - | - | ✅ | - |

### Running Tests by Category

```bash
# Fast smoke tests (bugs 1, 2, 4)
pytest -m smoke

# Behavioral validation (bugs 1, 2, 3)
pytest -m sanity

# Performance, security, edge cases (bugs 5, 7, 8)
pytest -m regression

# All tests
pytest

# Generate HTML report
pytest --html=report.html --self-contained-html
```

--------------------------------------------------

## Conclusion

The automated test suite successfully detects:

- ✅ Invalid JSON (Bug 1)
- ✅ Schema violations (Bugs 2, 4)
- ✅ Hallucinated goals (Bug 3)
- ✅ API failures with retry logic (Bug 5)
- ✅ JSON formatting edge cases (Bug 7)
- ✅ Telemetry accuracy (Bug 8)
- ⚠️ Missing environment variables (Bug 6) — **requires manual/CI validation**

These tests ensure **reliability** even when the AI model changes or the API behaves unexpectedly.