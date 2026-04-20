import streamlit as st
from src.config import get_api_key
from src.prompts import get_system_prompt
from src.ai_agent import AIAgent

def init_app():
    """Initializes configurations and returns the AI Agent instance."""
    api_key = get_api_key()
    if not api_key:
        st.error('GEMINI_API_KEY not found in Streamlit Secrets. Please check your configuration.')
        st.stop()
    return AIAgent(api_key)

def main():
    st.set_page_config(page_title="AI Daily Planner", page_icon="📅")
    st.title("Your Personal AI Assistant")
    
    # Initialize components
    agent = init_app()
    system_prompt = get_system_prompt()
    
    # Session State Strategy: Initialize with a friendly human greeting
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey! Ready when you are. Where are we headed today?"}
        ]
        
    # Display the conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Capture and Process User Input
    if prompt := st.chat_input("Type your tasks here..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Assistant generation loop
        with st.chat_message("assistant"):
            with st.spinner('Checking local gems...'):
                try:
                    assistant_reply = agent.generate_schedule(system_prompt, st.session_state.messages)
                    st.markdown(assistant_reply)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                except Exception as e:
                    if str(e) == "SERVER_OVERWHELMED":
                        st.warning("Google's servers are a bit overwhelmed right now. Give it a minute and try again!")
                    else:
                        st.error(str(e))
        
    # Footer UI
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: grey;
            text-align: center;
            padding: 10px 0;
            font-size: 12px;
            z-index: 999;
        }
        </style>
        <div class="footer">
            © 2026 Priyanshu Jha. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
