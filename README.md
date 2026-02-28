# AI Goal Coach — Automated Test Suite

This repository contains automated tests for the **AI Goal Coach System** challenge.

The AI Goal Coach converts vague goals into structured SMART goals using an AI model and returns a JSON response.

This project tests the system for correctness, schema validation, adversarial inputs, and reliability.


--------------------------------------------------

## Project Structure

goal_coach/
utils/
tests/
TEST_STRATEGY.md
BUGS.md
README.md


goal_coach/
System under test

utils/
AI client for API calls

tests/
PyTest test suite


--------------------------------------------------

## Requirements

Python 3.10+

Install dependencies:

pip install -r requirements.txt

If requirements.txt not present:

pip install pytest openai jsonschema


--------------------------------------------------

## AI Endpoint Used

This project uses a public AI endpoint via HuggingFace router.

Model:

openai/gpt-oss-20b

Base URL:

https://router.huggingface.co/v1


API key is configured inside ai_client.py.


--------------------------------------------------

## Running Tests

Run all tests:

pytest -v


Run specific test file:

pytest tests/test_goal_coach.py

pytest tests/test_schema.py

pytest tests/test_adversarial.py


--------------------------------------------------

## What is Tested

✔ Functional goal conversion  
✔ JSON schema validation  
✔ Key result count (3–5)  
✔ Confidence score range  
✔ Nonsense / adversarial input  
✔ Retry on API failure  
✔ Regression stability  


--------------------------------------------------

## Notes on AI Testing

AI responses may vary slightly.

Tests validate:

- Structure
- Field types
- Ranges
- Safety rules

instead of exact text.


--------------------------------------------------

## CI/CD Plan

In CI pipeline:

pip install -r requirements.txt
pytest -v

Future improvements:

- GitHub Actions
- Docker container
- Parallel tests
- Mock AI server


--------------------------------------------------

## How to Extend

Possible improvements:

- Add mock AI server
- Add load testing
- Add snapshot testing
- Add contract tests
- Add telemetry logs


--------------------------------------------------

## Author

Ranit Mondal  
Senior SDET Candidate — AI Accelerator Challenge