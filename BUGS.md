# BUGS — AI Goal Coach System

This document lists simulated and potential bugs found while testing the AI Goal Coach system.

Each bug includes reproduction steps, expected result, actual result, severity, and how automated tests detect it.


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

test_schema_validation  
test_valid_goal  

JSON parsing fails → test fails


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

test_schema_validation  
test_key_results_count  

Schema validation fails.


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

test_gibberish  
test_empty  
test_sql_injection  

Confidence validation fails.


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

test_schema_validation

Schema rule fails.


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

Retry logic in AIClient

Test fails if retry not implemented.


--------------------------------------------------

## Conclusion

The automated test suite successfully detects:

- Invalid JSON
- Schema violations
- Hallucinated goals
- Confidence errors
- API failures

These tests help ensure reliability even if the AI model changes.