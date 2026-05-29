import streamlit as st
import google.generativeai as genai
from config import MODEL_NAME, SYSTEM_PROMPT
from dotenv import load_dotenv
import os

# LOAD ENV VARIABLES
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# LOAD MODEL
model = genai.GenerativeModel(MODEL_NAME)

# PAGE SETTINGS
st.set_page_config(
    page_title="Study Chatbot",
    page_icon="📚",
    layout="centered"
)

# CUSTOM BLUE GLOW THEME
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #0F172A, #1E3A8A);
}

.stChatMessage {
    background-color: rgba(30, 41, 59, 0.8);
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
}

.stButton > button {
    background-color: #38BDF8;
    color: white;
    border-radius: 10px;
    border: none;
    box-shadow: 0 0 12px #38BDF8;
}

</style>
""", unsafe_allow_html=True)

# DAILY LIMIT
DAILY_LIMIT = 20

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

remaining = DAILY_LIMIT - st.session_state.chat_count

# CHAT MEMORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR
with st.sidebar:

    st.title("📚 Study Chatbot")
    st.write("Your AI study assistant")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()

    st.markdown("---")

    st.markdown("## 🌟 Plan")
    st.write("Free Plan")

    st.progress(remaining / DAILY_LIMIT)

    st.write(f"💬 Remaining chats: {remaining}")

# MAIN PAGE
st.title("📚 Study AI Assistant")

st.write("""
Ask questions about:
- Programming
- Math
- Science
- Exams
- Homework
""")

# DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT
user_input = st.chat_input("Ask your question...")

# CHAT LOGIC
if user_input:

    # DAILY LIMIT CHECK
    if st.session_state.chat_count >= DAILY_LIMIT:
        st.error("Daily chat limit reached.")
        st.stop()

    st.session_state.chat_count += 1

    # SAVE USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # DISPLAY USER MESSAGE
    with st.chat_message("user"):
        st.markdown(user_input)

    # GENERATE RESPONSE
    with st.spinner("Thinking..."):

        response = model.generate_content(
            SYSTEM_PROMPT + "\n\nUser: " + user_input
        )

        bot_reply = response.text

    # SAVE BOT MESSAGE
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # DISPLAY BOT MESSAGE
    with st.chat_message("assistant"):
        st.markdown(bot_reply)