import streamlit as st
from src.services.databricks_connection import execute_sql_query
from src.components.ui_elements import shared_page_header
import plotly.express as px
from pathlib import Path
from src.components.data_visuals import *
import pandas as pd

# Configure Streamlit page settings
st.set_page_config(page_title="Healthcare in EU", layout="wide")

# Create standard page header
shared_page_header(
    title = "💊 Healthcare in EU countries",
    subtitle =" As per data collected and shared by Eurostat",
    page_image = "src/assets/medical-report.png"
)

# ----------------------------------------------------------------------------------------

# loading and staging data from databricks
query_expenditure = Path('src/services/queries/source_query_expenditure.sql').read_text()
df1_raw  = execute_sql_query(query_expenditure)

query_assesement = Path('src/services/queries/source_query_assesement.sql').read_text()
df2_raw = execute_sql_query(query_assesement)

# creating dat categories for filters
years = df1_raw['Year'].unique()
countries = df1_raw['Country_Code'].unique()
types = list(df1_raw['Financing_type'].unique()) + ['Select All']
genders = ['M','F','Select All']
age_buckets = df2_raw['Age_Group'].unique()

# -----------------------------------------------------------------------------------------

# creating sidebar with filters list
with st.sidebar:
    st.header('Dashboard filters')

    # single selct year dropdown - by default last year available preset
    selected_year = st.selectbox('Year', years, index = 0)

    # multi select country slicer with select all
    container1 = st.container()
    isSelectAllCodes = st.checkbox('Select All', value = True, key='select_all_codes')
    if isSelectAllCodes:
        container1.multiselect('Country_Code', [])
        selected_countires = countries
    else:
        selected_countires = container1.multiselect('Country_Code', countries, default = countries)

    st.write('--------------------')
    st.subheader('Filters only for expenditure') 

    # expenditure types dropdown with select all option - all preset by default
    selected_type = st.selectbox('Expenditure Type', types, index = len(types)-1)
    if selected_type == 'Select All':
        selected_types = types
    else:
        selected_types = [selected_type]

    st.write('--------------------')
    st.subheader('Filters only for health status')

    # genders dropdown with select all option - all preset by default
    selected_sex = st.selectbox('Sex', genders, index = len(genders)-1)
    if selected_sex == 'Select All':
        selected_sexes = genders
    else:
        selected_sexes = [selected_sex]

    # multi select age group slicer with select all
    container2 = st.container()
    isSelectAllAges = st.checkbox('Select All', value = True, key='select_all_ages')
    if isSelectAllAges:
        container2.multiselect('Age_Group', [])
        selected_age_buckets = age_buckets
    else:
        selected_age_buckets= container2.multiselect('Age_Group', age_buckets, default = age_buckets)

# --------------------------------------------------------------------------------------------------

# defining final dataframes to work with after filters are applied
df1_withFilters = df1_raw[
            (df1_raw['Year']==selected_year) & 
            (df1_raw['Country_Code'].isin(selected_countires)) &
            (df1_raw['Financing_type']).isin(selected_types)
    ].copy()

df2_withFilters = df2_raw[
            (df2_raw['Year']==selected_year) & 
            (df2_raw['Country_Code'].isin(selected_countires)) &
            (df2_raw['Sex']).isin(selected_sexes) &
            (df2_raw['Age_Group']).isin(selected_age_buckets)
    ].copy()

# additional switch slicers to determine spending measure
first_slicer, second_slicer = st.columns([1,4])
with first_slicer:
    spend_type = st.radio('Euro value as:', ['Nominal','PPP'], horizontal=True)
with second_slicer:
    spend_unit = st.radio('Spending scope:', ['Total','Per capita'], horizontal=True)

# Conditionally set measure for selected filters
if spend_type == 'Nominal' and spend_unit == 'Total':
    metric = 'Total Spending'
elif spend_type == 'Nominal' and spend_unit == 'Per capita':
    metric = 'Spending per inhabitant'
elif spend_type == 'PPP' and spend_unit == 'Total':
    metric = 'Total Spending (PPS)'
elif spend_type == 'PPP' and spend_unit == 'Per capita':
    metric = 'Spending per inhabitant (PPS)'

# ----------------------------------------------------------------------------------------------------

first_charts_section = st.container()
with first_charts_section:

    # defining page layout as two columns with some separation
    left_split, buffer, right_split = st.columns([5,0.5,4])

    # bar chart
    with left_split:

        df2_viz = df1_withFilters \
            .groupby('Country_Code').agg({metric:'sum'}).reset_index() \
            .sort_values(by=metric, ascending=False)

        df2_viz['Index'] = range(len(df2_viz))

        draw_bar_chart(df=df2_viz, metric=metric)


    # dount chart
    with right_split:

        def create_line_breaks(text):
            words = text.split(' ')
            for i, word in enumerate(words):
                if i != 0 and len(word)>2 :
                    words[i] = '<br>' + word
            return ' '.join(words)

        df1_withFilters['Type'] = df1_withFilters['Financing_type'].map(create_line_breaks)

        df1_viz = df1_withFilters \
            .groupby('Type').agg({metric:'sum'}).reset_index() \
            .sort_values(by=metric, ascending=False)
        
        draw_pie_chart(df=df1_viz, metric=metric)

# ------------------------------------------------------------------------------------------------------

st.write('------------')

second_charts_section = st.container()
with second_charts_section:

    # defining page layout as two columns with some separation
    left_split, buffer, right_split = st.columns([5,0.5,4])

    # histogram
    with left_split:

        def add_sort_id(assesement):
            if assesement == 'Very bad':
                return 1
            elif assesement == 'Bad':    
                return 2
            elif assesement == 'Fair':        
                return 3
            elif assesement == 'Good':
                return 4
            elif assesement == 'Very good':
                return 5
        
        df2_withFilters['Sort_ID'] = df2_withFilters['Health_Assesement'].map(add_sort_id)
        df4_viz = df2_withFilters \
            .groupby(['Age_Group','Health_Assesement','Sort_ID'])['Number_of_People'].sum().reset_index() \
            .sort_values(['Age_Group','Sort_ID'])
        
        draw_histogram(df=df4_viz)

    # scatter plot
    with right_split:

        # Create temporary view for spending as % of GDP by country
        df1_temp = df1_withFilters[['Country_Code', 'Percentage of GDP']] \
            .groupby('Country_Code').agg(perc_of_gdp=('Percentage of GDP','sum')) \
            .reset_index()

        # Create a temporary view for percentage of bad and very bad health people in all polulation
        def only_bad_health(row):
            if row['Health_Assesement'] in ['Bad','Very bad']:
                return row['Number_of_People'] 
            
        df2_withFilters['Number only for bad health'] = df2_withFilters.apply(only_bad_health, axis=1)

        df2_temp = df2_withFilters.groupby('Country_Code').agg(
            num_of_bad_health=('Number only for bad health','sum'),
            num_of_total_health=('Number_of_People','sum')
        ).reset_index()

        df2_temp['perc_of_bad_health'] = df2_temp['num_of_bad_health']*100/df2_temp['num_of_total_health']

        # Merge both temp dataframes
        df3_viz = pd.merge(df1_temp, df2_temp, on='Country_Code')

        draw_scatter_plot(df=df3_viz)