import streamlit as st
from openai import OpenAI

st.title("🌩️ StormMate AI")
st.write("Your teen-friendly AI buddy!")

# Initialize Gemini using OpenAI client
client = OpenAI(
    api_key=st.secrets["google"]["api_key"],
    base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash"
)

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are StormMate AI ⚡ – a teen-friendly chatbot. "
               "Talk casual, supportive, and a bit playful. Use slang like 'bruh', 'fr', 'lowkey'. "
               "Give advice on mental health, school, and career. "
               "Always sound like a friend, never lecture. "
               "Always give simple and short replies unless it's an important long reply."
}

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

# Display welcome message once
if len(st.session_state.chat_history) == 0:
    with st.chat_message("assistant", avatar="🐼"):
        st.markdown("""**Team Dystopian Pandas - Demo Representation!**
- Saves chat history inside every session (deleted on close)
- Powered by Google Gemini 🧠
- Talks in teen-ish slang
- Chat about school, mental health, career or anything!""")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare messages with system prompt
                api_messages = [SYSTEM_PROMPT] + st.session_state.messages
                
                response = client.chat.completions.create(
                    model="gemini-1.5-flash",
                    messages=api_messages,
                    max_tokens=500,
                    temperature=0.7
                )
                
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                # Save assistant message
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                error_msg = f"Yo, something went wrong bruh 😅\n\nError: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})



