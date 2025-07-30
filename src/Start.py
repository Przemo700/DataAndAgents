import sys
import os

# adding additional root directory mapping to walk around the streamlit cloud architecture limitation
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
sys.path.append(repo_root)

import streamlit as st
from src.components.ui_elements import shared_page_header

st.set_page_config(page_title="Healthcare in EU", layout="wide")

shared_page_header(
    title = "🚀 Welcome in HealthCare test app!",
    subtitle = "Learning project created by Przemysław Kazimierski",
    page_image = "src/assets/support.png"
)

intro =  (
    "Hello! Welcome to my Streamlit project. "
    "App you're seeing consists of two pages showing two ways of data consumption: "
    "classical interactive dashboard and chat with AI agent having access to the same database. "
    "Source data was pulled from Eurostat through their official API and then processed and saved "
    "in Databricks platform (Free Edition). Hence please be mindful the loading time"
    " of both pages might be a bit longer due to initializing live connection to Databricks SQL Warehouse."
)

databricks_line = (
    "Source data was produced in Databricks with notebooks and PySpark and results saved as unity catalog tables "
    "in dedicated schema. Additional semantic layer was created adding definitions for all tables and columns."
)

dashboard_line = (
    "All data visualizations are created using python's Plotly Express module being a sub part of general "
    "Plotly library. Data for figures fetched from Databricks is loaded and processed in Pandas dataframes."
)

agent_line = (
    "Data agent used in chatbot is developed within LangChain framework utilizing Gemini 2.5 Flash API "
    "as input LLM. One of the standard sql agent classes was deployed with some additional enhancements."
)

left_col, buffer, right_col = st.columns([4,0.5,1.5])

with left_col:

    st.markdown("")
    st.markdown(intro)

    st.markdown("""
        <h1 style='
            font-family: "Source Sans Pro", sans-serif;
            font-size: 18px;
            color: #4F4F4F;
            margin-top: 6px;
            margin-bottom: 10px;
        '>App components
        </h1>
    """, unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(["SQL database", "Interactive data visuals", "AI chatbot agent"])
    
    with tab1:
        st.write(databricks_line)
        st.image("src/assets/databricks.png", width=175)
    with tab2:
        st.write(dashboard_line)
        st.image("src/assets/plotly-ex.png", width=175)
    with tab3:
        st.write(agent_line)
        st.image("src/assets/langchain.png", width=175)

with right_col:
    st.markdown("### About me:")
    st.markdown("")

    # Inline LinkedIn icon and link
    st.markdown(
        """
        <p style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" style="margin-right: 8px;" />
            <a href="https://www.linkedin.com/in/przemysław-kazimierski-77a1942aa" target="_blank" style="font-size: 16px; text-decoration: none;">
                My LinkedIn Profile
            </a>
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("")

    # Inline GitHub icon and link
    st.markdown(
        """
        <p style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" style="margin-right: 8px;" />
            <a href="https://github.com/Przemo700?tab=repositories" target="_blank" style="font-size: 16px; text-decoration: none;">
                My GitHub Projects
            </a>
        </p>
        """,
        unsafe_allow_html=True
    )