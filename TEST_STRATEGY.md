# TEST STRATEGY — AI Goal Coach System

## 1. Overview

The AI Goal Coach system converts vague user goals into structured SMART goals using an AI model.

The system returns a JSON response with the following schema:

```json
{
  "refined_goal": "string",
  "key_results": ["string"],
  "confidence_score": 1-10
}
```

The objective of this test strategy is to ensure correctness, reliability, safety, and stability of the AI response across normal, edge, and adversarial inputs.

Tests are implemented using Python + PyTest with schema validation, retry logic testing, and adversarial input testing.

---

## 2. Scope of Testing

We test the following areas:

### Functional Testing

* Valid goal input returns valid JSON
* refined_goal must exist
* key_results must contain 3–5 items
* confidence_score must be between 1–10

### Schema Validation

* JSON must follow strict schema
* No missing fields
* No null values
* No invalid types

### Edge Cases

* Empty input
* Very long input
* Special characters
* Numbers only
* Multiple sentences

### Adversarial Inputs

* Gibberish text
* SQL injection strings
* Unsafe / malicious goals
* Profanity / nonsense input

Expected behavior:

* confidence_score must be low (<=3)
* AI must not hallucinate valid goals

### Regression Testing

* Ensure same inputs return valid structure after model change
* Ensure API changes do not break schema
* Ensure key_results count remains valid

### Reliability Testing

* Retry on API failure
* Handle invalid JSON
* Handle rate limit errors

### Performance

* Response should return within acceptable time
* Multiple calls should not crash test suite

### Observability / Logging

* Log requests
* Log responses
* Log errors
* Log retries

Logs help detect model drift or API changes.

---

## 3. Test Levels

### Unit Tests

* Schema validation
* GoalCoach logic
* Confidence score validation

### Integration Tests

* AIClient + API
* Retry logic
* JSON parsing

### System Tests

* End-to-end goal generation
* Full response validation

### Negative Tests

* Invalid input
* Malicious input
* Broken JSON

### Regression Tests

* Ensure model change does not break schema
* Ensure API updates do not break tests

---

## 4. Non-Functional Testing

### Security

* Prevent prompt injection
* Prevent unsafe outputs
* Validate response structure

### Stability

* Multiple calls should not crash
* API failures should retry

### Maintainability

* Tests must be readable
* Tests must be independent
* Tests must be deterministic

### Reproducibility

* Same input should always return valid schema
* Confidence score must stay in range

---

## 5. JSON Schema Enforcement

Schema validation is done using jsonschema library.

Required fields:

* refined_goal → string
* key_results → array (3–5 strings)
* confidence_score → integer (1–10)

Tests fail if:

* field missing
* wrong type
* invalid range
* invalid array length

---

## 6. Test Architecture

Project structure:

goal_coach/
utils/
tests/
TEST_STRATEGY.md
BUGS.md

Components:

AIClient
Handles API calls with retry logic

GoalCoach
System under test

tests/
PyTest test suite

---

## 7. CI/CD Strategy

In CI pipeline:

1. Checkout code
2. Setup Python
3. Install dependencies
4. Run pytest
5. Generate report
6. Fail build if tests fail

 **Example of command used in the script:**

pip install -r requirements.txt
pytest -v -m smoke --html=report.html --self-contained-html --junitxml=report.xml 


---

## 8. Test Reporting

Test results are generated using pytest-html.

Reports include:

* Passed tests
* Failed tests
* Execution time
* Logs

Reports help detect regression after model change.

---

## 9. Handling Model / API Changes

AI systems may change behavior over time.

Mitigation:

* Schema validation tests
* Confidence score checks
* Regression tests
* Retry logic
* Logging

If model changes, tests should detect schema break.

---

## 10. Major Risks

Risk 1 — AI returns invalid JSON
Mitigation: Strict JSON parsing + schema validation

Risk 2 — AI hallucinates goal for nonsense input
Mitigation: Confidence score validation tests

Risk 3 — API rate limit / failure
Mitigation: Retry logic

Risk 4 — Model output changes over time
Mitigation: Regression tests

Risk 5 — Missing fields in response
Mitigation: Schema validation

---

## 11. Telemetry / Monitoring

Logs should capture:

* Input goal
* Raw response
* Parsed response
* Errors
* Retry attempts

This helps detect:

* Model drift
* API failures
* Invalid outputs

---

## 12. Traceability

Requirement → Test

Valid schema → test_schema_validation
Low confidence for nonsense → test_confidence_for_nonsense
Retry logic → test_retry_logic
Invalid JSON → test_invalid_json
Key results length → test_key_results_count

---


## 13. Conclusion

This strategy ensures that the AI Goal Coach system is tested for:

✔ correctness
✔ schema validity
✔ safety
✔ reliability
✔ regression stability
✔ adversarial resistance

The approach is designed to work even if the AI model evolves over time.
