from databricks import sql
from databricks.sql.types import Row
import pandas as pd
import streamlit as st

# Initialize connection with databricks client using credentials

@st.cache_resource(ttl=3600)
def get_databricks_client():
    try:
        server_hostname = st.secrets['DATABRICKS_WORKSPACE']
        http_path = st.secrets['DATABRICKS_SQL_WAREHOUSE']
        access_token = st.secrets['DATABRICKS_PAT']

        bricks_client = sql.connect(
            server_hostname = server_hostname,
            http_path = http_path,
            access_token = access_token
        )
        return bricks_client
    
    except Exception as e:
        st.error(f"Underlying connection error with Databricks: {e}")
        return None

# Execute SQL query using established connection to Datbricks Warehouse

@st.cache_data(ttl=600) 
def execute_sql_query(pushdown_query):
    client = get_databricks_client()
    if client:
        try:
            with client.cursor() as cursor:
                result = []
                cursor.execute(pushdown_query)
                for row in cursor.fetchall():
                    result.append(row.asDict())

            df = pd.DataFrame(result)
            return df

        except Exception as e:
            st.error(f"Error while fetching data: {e}")
            return pd.DataFrame()
