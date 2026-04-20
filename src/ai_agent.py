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
            if "429" in str(e):
                raise Exception("System busy (Rate limit reached). Please wait 60 seconds and try again.")
            else:
                raise Exception(f"API Error: {e}")
