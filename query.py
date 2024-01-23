#import mysql.connector
#import streamlit as st

#connection

#conn=mysql.connector.connect(
#    host="localhost",
 #   port="3306",
 #   user="root",
  ##  passwd="",
 #   db="myDb"
#)
#c=conn.cursor()

#fetch

#def view_all_data():
# c.execute('select * from insurance order by id asc')
# data=c.fetchall()
# return data
import pandas as pd
import pyodbc
import toml

secrets = toml.load("C:/Users/montassar.benarfia/Desktop/school/BI/.streamlit/secrets.toml")

def run_mdx_query(mdx_query, connection_string):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    
    cursor.execute(mdx_query)
    
    # Fetch the results into a DataFrame
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    df = pd.DataFrame.from_records(results, columns=columns)
    
    connection.close()
    
    return df

# Example usage:
mdx_query = '''select 
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
From TcommsCube'''
connection_string = 'DRIVER={SQL Server};SERVER=PRIMA229;DATABASE=Tcomms_Cube;UID=PRIMATEC\\montassar.benarfia;authentication = "Windows"'

result_df = run_mdx_query(mdx_query, connection_string)
print('MDX Query Result:')
print(result_df)

