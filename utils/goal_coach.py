# goal_coach/goal_coach.py

import json
from utils.ai_client import AIClient


class GoalCoach:

    def __init__(self, ai_client: AIClient | None = None):
        """GoalCoach wraps an AIClient to make goals.

        By default it creates a fresh AIClient, but a custom instance can be
        provided (useful for tests or swapping providers).
        """
        self.ai = ai_client or AIClient()

    def make_goal(self, goal: str):

        prompt = f"""
        You are an AI Goal Coach.

        Convert the input goal into JSON.

        Return ONLY JSON in this format:

        {{
          "refined_goal": "",
          "key_results": [],
          "confidence_score": 1
        }}

        Rules:
        - key_results must be 3 to 5 items
        - confidence_score must be 1-10
        - if input is nonsense, confidence_score must be <=3

        Goal: {goal}
        """

        response = self.ai.send_prompt(prompt)

        try:
            print(f"THE GOAL RECEIVED: \n{response}")

            # remove markdown ``` if present
            cleaned = response.strip()

            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```", "").strip()

            return json.loads(cleaned)

        except Exception:
            raise Exception("Invalid JSON returned from AI")