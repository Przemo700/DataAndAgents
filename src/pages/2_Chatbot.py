import streamlit as st
import sqlparse
from src.services.langchain_agent import ask_agent
from src.components.ui_elements import shared_page_header

# Configure Streamlit page settings
st.set_page_config(page_title="Chat with Gemini-Flash!", layout="wide")

# Create standard page header
shared_page_header(
    title = "🤖 Chat with Data Agent",
    subtitle = "In the chat you can talk to AI agent that has full access to our database",
    page_image = "src/assets/artifical-intelligence.png"
)

# Initialize queries log
if "queries_log" not in st.session_state:
    st.session_state.queries_log =[]

# Create sidebar
with st.sidebar:
    st.header('ChatBot Interaction')
    st.write('Below you can see what actual sql queries were generted for processing you questions')
    popover = st.popover("SQL Logs")
    for i, answer_log in enumerate(st.session_state.queries_log):
        answer_expander = popover.expander(f"Answer {i+1} logs")
        answer_expander.code(answer_log, language='sql')

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
    with st.chat_message("assistant"):
        with st.spinner("Wait a sec! I'm exploring data and analyzing results."):
            gemini_response = ask_agent(user_input, st.session_state.chat_session)
        
        # Display Gemini's response
        st.markdown(gemini_response['text'])

    # Add user and assistant messages to the chat history
    st.session_state.chat_session.append({"role": "user", "content": user_input})
    st.session_state.chat_session.append({"role": "assistant", "content": gemini_response['text']})

    # Add sql queries log returned from processing single answer
    consolidated_sql_log = ''
    for log in gemini_response['logs']:
    
        formatted_sql = sqlparse.format(log, reindent=True, keyword_case='upper')
        sql_with_header = '-- agent query:\n' + formatted_sql + '\n'
        consolidated_sql_log = consolidated_sql_log + sql_with_header

    if consolidated_sql_log != '':
        st.session_state.queries_log.append(consolidated_sql_log)
        log_len = len(st.session_state.queries_log)
        answer_expander = popover.expander(f"Answer {log_len} logs")
        answer_expander.code(consolidated_sql_log, language='sql')