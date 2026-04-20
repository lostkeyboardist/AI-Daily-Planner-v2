import os
from dotenv import load_dotenv

def get_api_key():
    """Loads environment configuration and returns the Gemini API Key."""
    load_dotenv()
    return os.getenv('GEMINI_API_KEY')
