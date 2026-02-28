# goal_coach/goal_coach.py

import json
from utils.ai_client import AIClient


class GoalCoach:

    def __init__(self):
        self.ai = AIClient()

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
            return json.loads(response)
        except Exception:
            raise Exception("Invalid JSON returned from AI")