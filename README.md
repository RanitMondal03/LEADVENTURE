# AI Goal Coach — Automated Test Suite

This repository contains automated tests for the **AI Goal Coach System** challenge.

The AI Goal Coach converts vague goals into structured SMART goals using an AI model and returns a JSON response.

This project tests the system for correctness, schema validation, adversarial inputs, and reliability.


--------------------------------------------------

## Project Structure
```

└── 📁tests
    ├── test_bug.py
    ├── test_goal_coach.py
    ├── test_negative.py
    ├── test_performance.py
    └── test_schema.py
└── 📁utils
    ├── ai_client.py
    └── goal_coach.py    
└── 📁Validators
    ├── fake_response.py
    └── goal_validator.py
```
coach/
utils/
tests/
Validators/goal_
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

This project uses a public AI endpoint via HuggingFace router by default.

Model and endpoint are configurable via environment variables or `AIClient` constructor.

Default values:

- Model: `openai/gpt-oss-20b`
- Base URL: `https://router.huggingface.co/v1`

To switch models or providers, set the following environment variables before running tests or instantiating the client:

```bash
export AI_MODEL="other-model-name"
export AI_BASE_URL="https://api.otherprovider.com/v1"
```

or pass arguments directly:

```python
from utils.ai_client import AIClient
client = AIClient(base_url="https://api.other.com", model="my-model")
```

API key is still read from `HUGGINGFACE_API_KEY` (see `.env.example`).


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




--------------------------------------------------

## Author

Ranit Mondal  
