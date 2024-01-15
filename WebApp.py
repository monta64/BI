import streamlit as st
import toml
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
# Load secrets
secrets = toml.load("C:/Users/montassar.benarfia/Desktop/school/BI/.streamlit/secrets.toml")

# Create connection string with Windows authentication
conn_str = f"Driver=SQL Server;Server={secrets['sql_server']['server']};Database={secrets['sql_server']['database']};Trusted_Connection=yes;"

# Connect to SQL Server
try:
    conn = pyodbc.connect(conn_str)
    st.success("Connected to SQL Server using Windows authentication.")
    # Perform SQL operations here
except Exception as e:
    st.error(f"Error connecting to SQL Server: {e}")

# Function to fetch data from SQL Server
def fetch_data_from_sql(query):
    # Set up your SQL Server connection
    conn = pyodbc.connect(conn_str)

    # Execute the query and fetch the results into a Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    return df

# # Define SQL queries for each table
# agebands_query = "SELECT * FROM AgeBands;"
# calendar_query = "SELECT * FROM Calendar;"
# campaigns_query = "SELECT * FROM Campaigns;"
# genders_query = "SELECT * FROM Genders;"
# prjmkgtype_query = "SELECT * FROM PrjmkgType;"
# segments_query = "SELECT * FROM Segments;"
# tcomms_trends_query = "SELECT * FROM tcomms_Trends;"

# # Fetch data for each table
# agebands_data = fetch_data_from_sql(agebands_query)
# calendar_data = fetch_data_from_sql(calendar_query)
# campaigns_data = fetch_data_from_sql(campaigns_query)
# genders_data = fetch_data_from_sql(genders_query)
# prjmkgtype_data = fetch_data_from_sql(prjmkgtype_query)
# segments_data = fetch_data_from_sql(segments_query)
# tcomms_trends_data = fetch_data_from_sql(tcomms_trends_query)

# # Display the data in Streamlit
# st.title("Data from SQL Server Tables")

# st.subheader("AgeBands Table")
# st.write(agebands_data)

# st.subheader("Calendar Table")
# st.write(calendar_data)

# st.subheader("Campaigns Table")
# st.write(campaigns_data)

# st.subheader("Genders Table")
# st.write(genders_data)

# st.subheader("PrjmkgType Table")
# st.write(prjmkgtype_data)

# st.subheader("Segments Table")
# st.write(segments_data)

# st.subheader("tcomms_Trends Table")
# st.write(tcomms_trends_data)
tcomms_trends_query = """
SELECT
    [PrjMkgID],
    [OpCode],
    [EcastItemID],
    [NbSent],
    [NbDispatched],
    [NbDeliv],
    [NbViews],
    [NbClicks],
    [UniqueViews],
    [UniqueClicks],
    [GenderID],
    [AgeBandID],
    [SegID],
    [Visited],
    [DirectSpent],
    [IndirectSpent],
    [TotalSpent],
    [VisitedWithoutOverLap],
    [DirectSpentWithoutOverlap],
    [IndirectSpentWithoutOverlap],
    [TotalSpentWithoutOverlap],
    [SendDate]
FROM
    tcomms_Trends
"""

tcomms_trends_data = fetch_data_from_sql(tcomms_trends_query)

# Display the data in Streamlit
st.title("Analysis of tcomms_Trends Data")

# Display the raw data
st.subheader("Raw Data:")
st.write(tcomms_trends_data)

# Example: Bar chart for Number of Views by Age Band
st.subheader("Number of Views by Age Band:")
views_by_age_band = tcomms_trends_data.groupby('AgeBandID')['NbViews'].sum()
st.bar_chart(views_by_age_band)

# Example: Pie chart for Gender Distribution
st.subheader("Gender Distribution:")
gender_distribution = tcomms_trends_data['GenderID'].value_counts()
plt.pie(gender_distribution, labels=gender_distribution.index, autopct='%1.1f%%', startangle=140)

# Example: Scatter plot for NbClicks vs NbViews
st.subheader("Scatter plot: NbClicks vs NbViews:")
sns.scatterplot(x='NbViews', y='NbClicks', data=tcomms_trends_data)
st.pyplot()