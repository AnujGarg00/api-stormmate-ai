import streamlit as st
import google.generativeai as genai

st.title("🌩️ StormMate AI")
st.write("Your teen-friendly AI buddy!")

# Configure Gemini
genai.configure(api_key=st.secrets["google"]["api_key"])

# System prompt
SYSTEM_INSTRUCTION = """You are StormMate AI ⚡ – a teen-friendly chatbot. 
Talk casual, supportive, and a bit playful. Use slang like 'bruh', 'fr', 'lowkey'. 
Give advice on mental health, school, and career. 
Always sound like a friend, never lecture. 
Always give simple and short replies unless it's an important long reply."""

# Initialize Gemini model
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_INSTRUCTION
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# Initialize chat history for display
if "chat_history" not in st.session_state:
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
    # Display user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text
                st.markdown(reply)
                
                # Save assistant message
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                error_msg = f"Yo, something went wrong bruh 😅\n\nError: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
