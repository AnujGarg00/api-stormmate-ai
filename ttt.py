import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=st.secrets["openai"]["api_key"],
)

st.title("🌩️ StormMate AI")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are StormMate AI ⚡ – a teen-friendly chatbot. "
         "Talk casual, supportive, and a bit playful. Use slang like 'bruh', 'fr', 'lowkey'. "
         "Give advice on mental health, school, and career. "
         "Always sound like a friend, never lecture. "
         "Always give simple and short replies unless it's an important long reply."},
    ]
    st.session_state.chat_history = []

# Display welcome message once
if len(st.session_state.chat_history) == 0:
    with st.chat_message("assistant", avatar="🐼"):
        st.markdown("""**Team Dystopian Pandas - Demo Representation!**
- Saves chat history inside every session (deleted on close)
- Talks in teen-ish slang
- Chat about school, mental health, career or anything!""")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
