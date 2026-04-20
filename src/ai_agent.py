from google import genai
from google.genai import types
from google.genai.errors import APIError

class AIAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_schedule(self, system_prompt: str, user_input: str) -> str:
        """Generates a schedule based on the user input and the system prompt."""
        full_prompt = f"{system_prompt}\n\nUser Input: {user_input}"
        
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}]
                    )
                )
                return response.text
            except APIError as e:
                if "503" in str(e) or "429" in str(e):
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("SERVER_OVERWHELMED")
                else:
                    raise Exception(f"API Error: {e}")
