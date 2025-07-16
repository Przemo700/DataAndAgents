import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_sql_agent, AgentExecutor
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

def get_gemini_llm(gemini_version="gemini-2.5-flash"):
    try:
        os.environ["GOOGLE_API_KEY"] = st.secrets['GOOGLE_API_KEY']
        llm = ChatGoogleGenerativeAI(model=gemini_version)
        return llm
    
    except Exception as e:
        st.error(f"Error while calling Gemini API: {e}")
        return None
    
def get_database_connection(bricks_catalog = "workspace", bricks_schema = "eurostat"):
    try:
        host_url = st.secrets['DATABRICKS_WORKSPACE']
        warehouse_id = st.secrets['DATABRICKS_SQL_WAREHOUSE'].split('/')[-1]
        access_token = st.secrets['DATABRICKS_PAT']

        # initializing Langchain's SQL database class based on databricks connection
        db = SQLDatabase.from_databricks(
            catalog = bricks_catalog,
            schema = bricks_schema,
            host = host_url,
            api_token = access_token,
            warehouse_id = warehouse_id,
            engine_args = {"pool_pre_ping": True}
        )
        return db
    
    except Exception as e:
        st.error(f"Error while connecting to Databricks: {e}")
        return None
    
def create_ai_agent(llm = get_gemini_llm(), db = get_database_connection()):

    if llm and db:
        try:
            # tools avaialble to agent: sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            # initializng Langchain agent
            my_agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=False
            )
            return my_agent
        except Exception as e:
            st.error(f"Not able to create SQL agent: {e}")
            return None
        
class AgentWrapper:
    
    def __init__(self, agent):
        self.agent = agent
    
    def run(self, query):
        try:
            result = self.agent.invoke(query)
            return result['output']
        except Exception as e:
            # For parsing errors only - extract llm output that should be placed between first and last bactick
            if "Could not parse LLM output" in str(e):
                error_str = str(e).split("Could not parse LLM output")[1]
                response_start, response_end = error_str.find("`"), error_str.rfind("`")
                llm_response = error_str[response_start+1:response_end]
                return llm_response
            raise e
    
    def __getattr__(self, name):
        # Delegate other methods to the wrapped agent
        return getattr(self.agent, name)
        
def ask_agent(user_input, history, my_agent=create_ai_agent()):

    if my_agent:

        # handling frequent errors of original SQL agent realated to parsing orginial LLM response
        enhanced_agent = AgentWrapper(my_agent)

        # injecting full conversation history into prompt
        formatted_history = ""

        for msg in history:
            if msg["role"] == 'user':
                formatted_history += f"Human: {msg['content']}\n"
            elif msg['role'] == 'assistant':
                formatted_history += f"AI: {msg['content']}\n"

        if formatted_history:
            combined_input = f"Previous conversation:\n{formatted_history}\nNew question: {user_input}"
        else:
            combined_input = user_input

        # calling enhanced agent with prompt augemented with history context
        try:
            response = enhanced_agent.run(combined_input)
            return response
        
        except Exception as e:
            return f"Sorry, but there was an error while preparing answer: {e}"
