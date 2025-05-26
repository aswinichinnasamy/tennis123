import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
#Function to connect to MySql:
def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "AKsk1705@",
        database = "ma37"
    )
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    cursor.close()
    #conn.close()
    return pd.DataFrame(rows,columns=col_names)

st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to",["Project Introduction","Competitions and Categories","Complexes and Venues",
                                 "Competitors and Rankings","Creator Info"])


# --------------------------------page:1 Project Introduction ------------------------------------------
if page == "Project Introduction":
    st.title("SPORTS: Tennis Data Analysis")
    st.subheader("Streamlit App for Exploring Tennis data")
    st.image('c:/Users/User/Desktop/guvi project1/Project1/tennis.jpg')
    st.write(""" 
             This project analysis Tennis data and gives information about categories,competitors,venues and competitions
             across different countries.
             It also provides details of competitors and their rankings amongst other competitors.

             ** Features: **
                * Provides information about the competitions and filters based on the countries
                * Run SQL queries to explore the insights.

             ** Database: MySQL **
            """
             )
#--------------------------------page: 2 Competitions and Categories------------------------------------
elif page == "Competitions and Categories":
    st.title("Tennis: Information about Competitions and Categories")

# Fetching the competitions and categories details:
    query_options = {
       "1.Competitons of type doubles": "select competition_name,type from competitions_table where type = 'doubles'",
       "2.Competitions and their category_names": "select competition_name,category_name from competitions_table join categories_table on competitions_table.category_id = categories_table.category_id",
       "3. Parent competitions and their sub-competitions": "SELECT parent_id, GROUP_CONCAT(competition_name) as sub_competitions FROM competitions_table WHERE parent_id IS NOT NULL group by parent_id",
       "4. List of competitions with no parent": "select competition_name,parent_id from competitions_table where parent_id IS NULL",
       "5. Distribution of competition_type by category": "select ct.category_id,group_concat(type) from competitions_table as cot join categories_table as ct on cot.category_id = ct.category_id group by category_id"          
           }
    selected_query = st.selectbox("choose a query",list(query_options.keys()))
    query = query_options[selected_query]
    query_result = run_query(query)
    st.write("query_result:")
    st.dataframe(query_result)

# --------------------------------     page: 3 Complexes and Venues  ------------------------------------
elif page == "Complexes and Venues":
    st.title("Tennis: Information about Complexes and Venues")

# Fetching Complexes and Venues details:
    query_options1 = {
        "1. Venues and their complex names":"select venue_name,complex_name from complexes_table join venues_table on complexes_table.complex_id = venues_table.complex_id",
        "2. venues and their count":"select complex_name,count(venue_id) as count from complexes_table as ct join venues_table as vt on ct.complex_id = vt.complex_id group by complex_name",
        "3. venues and their specific country":"select country_name,venue_id,venue_name as venues from venues_table",
        "4. venues and their timezones":"select venue_id,venue_name,timezone from venues_table",
        "5. complexes having more than one venue counts":"select ct.complex_id, count(venue_id) as count_of_venues from complexes_table as ct join venues_table as vt on ct.complex_id = vt.complex_id group by complex_id having count(venue_id) > 1"
    }
    selected_query1 = st.selectbox("choose a query",list(query_options1.keys()))
    query1 = query_options1[selected_query1]
    query_result1= run_query(query1)
    st.write("query_result:")
    st.dataframe(query_result1)

# --------------------------------     page: 4 Competitors and Rankings  ------------------------------------ 
elif page == "Competitors and Rankings":
    st.title("Tennis: Information about Competitors and their Rankings")

# fetching competitors and venues details:

    query_options2 = {"1.competitors and their ranks and points":"select ct.name, rt.competitor_rank, rt.points from competitors_table as ct join competitor_rankings_table as rt on ct.competitor_id = rt.competitor_id",
                  "2.Top5 Competitors":"select ct.name as competitor_names, rt.competitor_rank from competitors_table as ct join competitor_rankings_table as rt on ct.competitor_id = rt.competitor_id order by competitor_rank limit 5",
                  "3.competitors with no rank movement":"select ct.name as competitor_names, rt.movement from competitors_table as ct join competitor_rankings_table as rt on ct.competitor_id = rt.competitor_id where movement = 0",
                  "4.competitors and their total points based on country":"select ct.country, sum(rt.points) as total_points_of_competitors from competitors_table as ct join competitor_rankings_table as rt on ct.competitor_id = rt.competitor_id group by country",
                  "5.number of competitors per country": "select country,count(competitor_id) as no_of_competitors from competitors_table group by country"
                  }

    selected_query2 = st.selectbox("choose a query",list(query_options2.keys()))
    query2 = query_options2[selected_query2]
    query_result2 = run_query(query2)
    st.write("query_result:")
    st.dataframe(query_result2)

    q1 = "select name,country from competitors_table"
    q2 = "select ct.name, rt.competitor_rank, rt.points from competitors_table as ct join competitor_rankings_table as rt on ct.competitor_id = rt.competitor_id"
    df1 = pd.read_sql(q1,con=get_connection()) 
    df2 = pd.read_sql(q2,con=get_connection()) 


    st.title("Competitors per country")
    #filter1: countries -multi-select
    country_options = st.multiselect("Select countries:", df1['country'].unique())

    if country_options:
        filtered_df = df1[df1['country'].isin(country_options)]
    else:
        filtered_df = df1

    st.dataframe(filtered_df)


    #filter 2:ranks- slider
    min_rank, max_rank= st.slider("select rank range",
                              min_value = int(df2['competitor_rank'].min()),
                              max_value = int(df2['competitor_rank'].max()),
                              value = (int(df2['competitor_rank'].min()),
                                       int(df2['competitor_rank'].max()))
                              )
    #filter 3: points range slider
    min_points, max_points = st.slider("Select points range",
    min_value = int(df2['points'].min()),
    max_value = int(df2['points'].max()),
        value = (
            int(df2['points'].min()),
            int (df2['points'].max())
         ) )
    filtered_df1 = df2[(df2['competitor_rank'] >= min_rank) & 
                   (df2['competitor_rank'] <= max_rank) &
                   (df2['points'] >= min_points) &
                   (df2['points'] <= max_points)]

    #filter 4: search by name
    search_name = st.text_input("Search Competitor_name")

    if search_name:
        filtered_df1 = filtered_df1[filtered_df1['name'].str.contains(search_name,case=False)]


    #display
    st.subheader("filtered results")
    st.dataframe(filtered_df1)

# --------------------------------     page: 5 Creator Info  --------------------------------------------
else:
    st.title("Creator of this project")
    st.write("""
             **Developed by**: Aswini 
             **Skills**: Python,SQL,Streamlit,pandas
             """)
    st.image('c:/Users/User/Desktop/guvi project1/Project1/tennis1.jpg')
