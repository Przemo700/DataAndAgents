import streamlit as st
from src.services.langchain_agent import ask_agent
from src.components.ui_elements import shared_page_header

# Configure Streamlit page settings
st.set_page_config(page_title="Chat with Gemini-Flash!", layout="wide")
st.sidebar.header('ChatBot Interaction')

# Create standard page header
shared_page_header(
    title = "🤖 Chat with Data Agent",
    subtitle = "In the chat you can talk to AI agent that has full access to our database",
    page_image = "src/assets/artifical-intelligence.png"
)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []
    opening_message = "Hello, I'm a helpful chatbot that can help you to explain the data displayed in this dashabord. Please, feel free to ask!"
    st.session_state.chat_session.append({"role": "assistant", "content": opening_message})

# Display the chat history
for msg in st.session_state.chat_session:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field for user's message
user_input = st.chat_input("Ask AI assistant...")
if user_input:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_input)

    # Send user's message to Gemini and get the response
    gemini_response = ask_agent(user_input, st.session_state.chat_session)

    # Display Gemini's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.append({"role": "user", "content": user_input})
    st.session_state.chat_session.append({"role": "assistant", "content": gemini_response})