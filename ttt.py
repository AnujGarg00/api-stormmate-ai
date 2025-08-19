import streamlit as st
from openai import OpenAI

# Replace YOUR_API_KEY_HERE with your free OpenRouter API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

st.title("🌩️ StormMate AI")
st.write("Your teen-friendly AI buddy! Type 'quit' to exit.")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are StormMate AI ⚡ – a teen-friendly chatbot. "
         "Talk casual, supportive, and a bit playful. Use slang like 'bruh', 'fr', 'lowkey'. "
         "Give advice on mental health, school, and career. "
         "Always sound like a friend, never lecture. "
         "Always give simple and short replies unless it’s an important long reply."},
    ]

if "chat" not in st.session_state:
    st.session_state.chat = []  # keeps user-visible chat log
    st.session_state.chat.append((
    "Team Dystopian Pandas",
    """**This is Just a Demo Representation!**

- Still what it can do?  
- Saves chat history inside every session (deleted on close).  
- Talks in teen-ish slang.  
- Chat about school, mental health, career or Literally anything you want to! 
"""))

# Handle user input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.chat.append(("You", prompt))
    st.session_state.chat.append(("StormMate AI", reply))

# Display chat
for sender, msg in st.session_state.chat:
    if sender == "You":
        st.markdown(f"**{sender}:** {msg}")
        
    elif sender == "Team Dystopian Pandas":
        st.markdown(f"<span style='color:#FFD700'>**{sender}:** {msg}</span>", unsafe_allow_html=True)
        
    else:
        st.markdown(
            f"<span style='color:#00d4ff'>**{sender}:** {msg}</span>",
            unsafe_allow_html=True
        )
