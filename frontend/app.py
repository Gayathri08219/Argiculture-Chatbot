import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Agro Chatbot", page_icon="🌱", layout="centered")

# 🌱 Header
st.markdown("<h2 style='text-align: center;'>🌱 Agro Chatbot</h2>", unsafe_allow_html=True)
st.write("---")

# 🧠 Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 📥 Chat input (fixed at bottom)
user_input = st.chat_input("Ask your agriculture question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from backend
    try:
        response = requests.post(API_URL, json={"question": user_input})

        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get("answer", "⚠️ No response received")
        else:
            bot_reply = "⚠️ Server error"

    except Exception as e:
        bot_reply = f"⚠️ Connection error: {str(e)}"

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)