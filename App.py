import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
#from os import system
from sys import path
path.append("C:\\Program Files\\Microsoft.NET\\ADOMD.NET\\160\\")
from pyadomd import Pyadomd


st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

st.sidebar.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            background-color: #ffffff; /* White color */
        }
    </style>
    """,
    unsafe_allow_html=True
)


CONNECTION_STRING = (
    "Provider=MSOLAP;Data Source=PRIMA229;Integrated Security=SSPI;Catalog=Tcomms_Cube;"
)

QUERY_STRING = """
select 
{
[Measures].[Sent],
[Measures].[Dispatched],
[Measures].[Deliv],
[Measures].[Delivery Rate]
} on columns, 
NonEmpty
(([Campaigns].[Prj Mkg].[Prj Mkg],
[Age Bands].[Age].[Age],
[Genders].[Gender].[Gender]
))on Rows
From TcommsCube
"""

with Pyadomd(CONNECTION_STRING) as conn:
    with conn.cursor().execute(QUERY_STRING) as cur:
        DataSet = cur.fetchall()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(DataSet)
print(df)
df.rename(columns={0:"campaigns", 1:"age_bands", 2:"genders",3:"sent", 4:"dispatched", 5:"deliv",6:"delivRate"}, inplace=True)
print(df.head())
# Main content

st.header("ANALYTICS WEB DASHBOARD | INSURANCE KPI & TRENDS ")
fig2 = px.bar(df, x='campaigns', y='sent', color='age_bands', barmode='group', title='Anaysis results')
st.plotly_chart(fig2, use_container_width=True)
st.sidebar.image("data/logo1.png")
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

