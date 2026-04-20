import streamlit as st

def get_api_key():
    """Returns the Gemini API Key from Streamlit Secrets."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except KeyError:
        return None
