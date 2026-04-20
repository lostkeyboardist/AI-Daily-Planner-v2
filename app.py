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
            {"role": "assistant", "content": "Hey! Ready when you are. Where are we headed today?"}
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
                assistant_reply = agent.generate_schedule(system_prompt, st.session_state.messages)
            except Exception as e:
                if str(e) == "SERVER_OVERWHELMED":
                    st.warning("Google's servers are a bit overwhelmed right now. Give it a minute and try again!")
                else:
                    st.error(str(e))
                st.stop()
        
        with st.chat_message("assistant"):
            st.write(assistant_reply)
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: grey;'>© 2026 Priyanshu Jha. All rights reserved.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
