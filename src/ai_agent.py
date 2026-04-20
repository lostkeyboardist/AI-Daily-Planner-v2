from google import genai
from google.genai import types
from google.genai.errors import APIError

class AIAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def generate_schedule(self, system_prompt: str, chat_history: list) -> str:
        """Generates a schedule based on the full chat history, injected with memory."""
        
        formatted_contents = []
        for msg in chat_history:
            # Skip the placeholder intro to avoid confusing the model's history flow
            if msg["role"] == "assistant" and "Ready when you are" in msg["content"]:
                continue
                
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(role=role, parts=[types.Part.from_text(msg["content"])])
            )
            
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=[{"google_search": {}}],
                        stop_sequences=["###", "\n\nUser Input:"]
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
