import streamlit as st
from src.services.databricks_connection import execute_sql_query
from src.components.ui_elements import shared_page_header
import plotly.express as px
from pathlib import Path

# Configure Streamlit page settings
st.set_page_config(page_title="Healthcare in EU", layout="wide")

# Create standard page header
shared_page_header(
    title = "💊 Healthcare in EU countries",
    subtitle =" As per data collected and shared by Eurostat",
    page_image = "src/assets/medical-report.png"
)

# loading and staging data from databricks
query = Path('src/services/queries/db_pushdown_query.sql').read_text()
df = execute_sql_query(query)

# creating dat categories for filters
years = df['Year'].unique()
countries = df['Country_Code'].unique()
types = list(df['Type'].unique()) + ['Select All']

# creating sidebar with filters list
with st.sidebar:
    st.header('Dashboard filters')

    # single selct year dropdown - by default last year available preset
    selected_year = st.selectbox('Year', years, index = 0)

    # expenditure types dropdown with select all option - all preset by default
    selected_type = st.selectbox('Expenditure Type', types, index = len(types)-1)
    if selected_type == 'Select All':
        selected_types = types
    else:
        selected_types = [selected_type]

    # multi select country slicer with select all
    container = st.container()
    isSelectAllCodes = st.checkbox('Select All', value = True)
    if isSelectAllCodes:
        container.multiselect('Country_Code', [])
        selected_countires = countries
    else:
        selected_countires = container.multiselect('Country_Code', countries, default = countries)

# defining final dataframe to work with after filters are applied
df_withFilters = df[
            (df['Year']==selected_year) & 
            (df['Country_Code'].isin(selected_countires)) &
            (df['Type']).isin(selected_types)
        ]

# defining page layout as two columns with some separation
left_split, buffer, right_split = st.columns([4,0.5,4])

# pie chart showing total expenditure split by public/private schemas
with left_split:

    # prepare data
    df1 = df_withFilters[['Type','Spending']] \
            .groupby('Type').agg(Spending=('Spending','sum')).reset_index()
    
    # define color templates for pie pieces
    color_mapping = {
        'Out-of-pocket payments': "#D1504A",  # red
        'Government and compulsory schemes': "#d7c539",   # blue
        'Voluntary schemes': '#2ECC40',    # green
        'Rest of world': '#AAAAAA'   # gray
    }
    
    # define chart in plotly
    fig1 = px.pie(
        df1, 
        names = 'Type', values = 'Spending', 
        title=  'Type of expenditure',
        color = 'Type', color_discrete_map = color_mapping
    )

    # execute chart in streamlit
    st.plotly_chart(fig1)

# bar chart showing spending per inhabitant in million euros per country - sorted descending
with right_split:

    # prepare data
    df2 = df_withFilters[['Country_Code','Spending_per_inhabitant']] \
            .groupby('Country_Code').agg(Spending_per_inhabitant=('Spending_per_inhabitant','sum')).reset_index() \
            .sort_values(by='Spending_per_inhabitant', ascending=False)
    
    # define chart in plotly
    fig2 = px.bar(
        df2, 
        x ='Country_Code', y ='Spending_per_inhabitant', 
        title = 'Countries expenditure per inhabitant', 
        text = 'Spending_per_inhabitant',
        color_discrete_sequence = ['#D1504A']
    )

    # execute chart in streamlit
    st.plotly_chart(fig2)