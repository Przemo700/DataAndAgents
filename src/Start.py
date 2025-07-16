import streamlit as st
from src.components.ui_elements import shared_page_header

st.set_page_config(page_title="Healthcare in EU", layout="wide")

shared_page_header(
    title = "🚀 Welcome in HealthCare test app!",
    subtitle = "Learning project created by Przemysław Kazimierski",
    page_image = "src/assets/support.png"
)

intro =  (
    "Following app consists of two pages showing two ways of data consumption: "
    "classical interactive data dashboard and chat with AI agent, showing two ways of data exploration. "
    "Both pages are live connected to the same database in Databricks (Free Edition)."
)

databricks_line = (
    "App's database was built in Databricks, from data downloaded from Eurostat via official API. "
    "Some ETL processing was performed in PySpark and data was saved as unity catalog tables"
)

dashboard_line = (
    "Dashboard page is fetching data from source connecting to provided SQL warehouse. "
    "Then the visuals are created using PyPlot framework embedded in Streamlit frontend."
)

agent_line = (
    "For chatbot part I'm using standard Streamlit's chat elements "
    "and agent himself was developed in LangChain framweork and Gemini 2.5 Flash LLM."
)

left_col, right_col = st.columns([4,2])

with left_col:
    st.markdown(f"""
        <h1 style='
            font-size: 16px;
            color: #000000;
            padding: 20px;
        '>{intro}
        </h1>
        <ul style='margin-top: 10px; padding-left: 10px;list-style-type: none;'>
            <li style='font-size: 14px; margin-bottom: 8px;'>{databricks_line}</li>
            <li style='font-size: 14px; margin-bottom: 8px;'>{dashboard_line}</li>
            <li style='font-size: 14px; margin-bottom: 8px;'>{agent_line}</li>
        </ul>
        <style>
        li::before {{
            content: '★';
            position: absolute;
            left: 0;
            color: #ababab;
        }}
        </style>
    """, unsafe_allow_html=True
    )