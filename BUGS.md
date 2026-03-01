# BUGS — AI Goal Coach System

This document lists simulated bugs used to verify that the automated test suite can detect incorrect AI responses.

The bug tests do not call the real AI.
Instead, fake responses are generated in:

Validators/fake_response.py

These responses intentionally break the expected format.

The responses are validated using reusable validation functions in:

Validators/goal_validator.py

The bug tests are located in:

tests/test_bugs.py

This design proves that the same validation logic used in normal tests will fail if the AI returns invalid data.

---

## Bug 1 — Wrong data type in response

### Description

AI returns fields with incorrect data types.

### Fake Response

{
"refined_goal": 123,
"key_results": "not a list",
"confidence_score": "high"
}

### Expected Result

* refined_goal → string
* key_results → list
* confidence_score → integer (1–10)

### Actual Result

Wrong types returned.

### Severity

High

### Detected By

tests/test_bugs.py::test_bug_wrong_type

Validation used:

assert_valid_goal_schema()

---

## Bug 2 — Missing required field

### Description

AI response is missing required field.

### Fake Response

{
"refined_goal": "test",
"confidence_score": 5
}

Missing:

key_results

### Expected Result

All required fields must exist.

### Actual Result

Field missing.

### Severity

High

### Detected By

tests/test_bugs.py::test_bug_missing_field

Validation used:

assert_valid_goal_schema()

---

## Bug 3 — Too many key_results

### Description

AI returns more than allowed number of key results.

### Fake Response

{
"refined_goal": "test",
"key_results": ["a","b","c","d","e","f"],
"confidence_score": 5
}

### Expected Result

key_results must contain 3–5 items.

### Actual Result

6 items returned.

### Severity

Medium

### Detected By

tests/test_bugs.py::test_bug_too_many_results

Validation used:

validate_goal_response()

---

## Bug 4 — Too few key_results

### Description

AI returns less than required key results.

### Fake Response

{
"refined_goal": "test",
"key_results": ["a"],
"confidence_score": 5
}

### Expected Result

3–5 items required.

### Actual Result

Only 1 item returned.

### Severity

Medium

### Detected By

tests/test_bugs.py::test_bug_too_few_results

Validation used:

validate_goal_response()

---

## Bug 5 — confidence_score out of range

### Description

AI returns score outside allowed range.

### Fake Response

{
"refined_goal": "test",
"key_results": ["a","b","c"],
"confidence_score": 50
}

### Expected Result

1 <= confidence_score <= 10

### Actual Result

50 returned.

### Severity

Medium

### Detected By

tests/test_bugs.py::test_bug_invalid_confidence

Validation used:

validate_goal_response()

---

## Bug 6 — Gibberish input returns valid goal

### Description

AI generates valid goal for nonsense input.

### Fake Response

{
"refined_goal": "Improve typing",
"key_results": ["practice","speed","accuracy"],
"confidence_score": 9
}

### Expected Result

For invalid input:

* refined_goal = "NA"
* key_results = "NA"
* confidence_score <= 3

### Actual Result

Valid goal returned.

### Severity

High

### Detected By

tests/test_bugs.py::test_gibberish_response

Validation used:

validate_na_response()

---

## How Bugs Are Simulated

Fake responses are created in:

Validators/fake_response.py

Example functions:

wrong_type_response()
missing_field_response()
too_many_key_results()
too_few_key_results()
invalid_confidence()
gibberish_response()

These responses are passed to validators:

Validators/goal_validator.py

Validator functions used:

validate_goal_response()
assert_valid_goal_schema()
validate_na_response()

This proves that if the AI returns incorrect data, the tests will fail.

---

## Test Coverage Summary

| Bug                | Schema | Validator | Bug Test |
| ------------------ | ------ | --------- | -------- |
| Wrong type         | ✅      | ✅         | ✅        |
| Missing field      | ✅      | ✅         | ✅        |
| Too many results   | -      | ✅         | ✅        |
| Too few results    | -      | ✅         | ✅        |
| Confidence range   | -      | ✅         | ✅        |
| Gibberish response | -      | ✅         | ✅        |

---

## Conclusion

The automated test suite correctly detects invalid AI responses using:

* Schema validation
* Custom validators
* Fake response simulation
* Bug-specific tests

This ensures the system remains reliable even if the AI returns incorrect or malformed output.
