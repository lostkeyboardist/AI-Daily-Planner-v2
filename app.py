import streamlit as st
from src.config import get_api_key
from src.prompts import get_system_prompt
from src.ai_agent import AIAgent

def init_app():
    """Initializes configurations and the AI Agent."""
    api_key = get_api_key()
    if not api_key:
        st.error('API Key not found. Please check your .env file.')
        st.stop()
    return AIAgent(api_key)

def main():
    st.set_page_config(page_title="Your New Personal AI Assistant")
    st.title("Your New Personal AI Assistant")
    
    # Initialize components
    agent = init_app()
    system_prompt = get_system_prompt()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I am your Context-Aware AI Planner. To save time and get a perfectly tuned schedule, please tell me your tasks, your current location, and any specific preferences (e.g., cravings for lunch, meeting types) all in one message!"}
        ]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if prompt := st.chat_input("Type your tasks here..."):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner('Optimizing your schedule...'):
            try:
                assistant_reply = agent.generate_schedule(system_prompt, prompt)
            except Exception as e:
                st.error(str(e))
                st.stop()
        
        with st.chat_message("assistant"):
            st.write(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

if __name__ == "__main__":
    main()
