from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# this fnc helps us to load env variables from .env
load_dotenv()


class AIClient:

    def __init__(self, base_url: str | None = None, model: str | None = None):

        API_KEY = os.getenv("HUGGINGFACE_API_KEY")
        if not API_KEY:
            raise ValueError("HUGGINGFACE_API_KEY environment variable not set.")

        # base_url = base_url or os.getenv("AI_BASE_URL", "https://router.huggingface.co/v1")
        # # model = model or os.getenv("AI_MODEL", "openai/gpt-oss-20b")
        # model = model or os.getenv("AI_MODEL", "Qwen/Qwen3.5-397B-A17B:novita")

        base_url = base_url or os.getenv("AI_BASE_URL")
        model = model or os.getenv("AI_MODEL")
        # model = model or os.getenv("AI_MODEL", "Qwen/Qwen3.5-397B-A17B:novita")

        

        self.client = OpenAI(
            base_url=base_url,
            api_key=API_KEY
        )

        self.model = model
        self.telemetry = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_retries": 0,
            "total_latency_ms": 0,
        }

    def send_prompt(self, prompt, retries=1):

        self.telemetry["total_requests"] += 1
        request_start = time.time()

        for attempt in range(retries):
            try:
                attempt_start = time.time()

                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a strict JSON API. Always return valid JSON only. DO not add any other extra items in the response. "
                                       "Only RETURN the JSON"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2
                )

                latency_ms = (time.time() - attempt_start) * 1000
                self.telemetry["total_latency_ms"] += latency_ms
                self.telemetry["successful_requests"] += 1
                BRIGHT_MAGENTA = '\033[95m'
                RESET = '\033[0m'


                print(BRIGHT_MAGENTA + f"\n\n[Telemetry] Request succeeded on attempt  : {attempt + 1}" +RESET)
                print(BRIGHT_MAGENTA + f"[Telemetry] Latency : {latency_ms:.2f}ms" + RESET)
                print(BRIGHT_MAGENTA + f"[Telemetry] Stats so far : {self.get_telemetry()}" + RESET)

                return completion.choices[0].message.content.strip()

            except Exception as e:
                self.telemetry["total_retries"] += 1
                print(f"[Telemetry] Retry {attempt + 1} failed: {e}")
                time.sleep(2)

        self.telemetry["failed_requests"] += 1
        total_latency_ms = (time.time() - request_start) * 1000
        self.telemetry["total_latency_ms"] += total_latency_ms

        print(f"[Telemetry] Request fully failed after {retries} retries")
        print(f"[Telemetry] Stats so far: {self.get_telemetry()}")

        raise Exception("AI request failed after retries")

    def get_telemetry(self):
        stats = self.telemetry.copy()
        if stats["successful_requests"] > 0:
            stats["avg_latency_ms"] = round(
                stats["total_latency_ms"] / stats["successful_requests"], 2
            )
        else:
            stats["avg_latency_ms"] = 0
        return stats