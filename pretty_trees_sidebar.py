from re import sub
import pandas as pd
import streamlit as st
import numpy as np

#configure the streamlit page
#st.set_page_config(layout='wide')

st.title('SF Trees')
trees_df = pd.read_csv('trees.csv')
#add filter on sidebar
owners = st.sidebar.multiselect('Tree owner filter', trees_df['caretaker'].unique())


#col1, col2, col3 = st.columns((1, 1, 1))

if owners:
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]

#code copied from trees.py
#group by dbh
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['tree_count']
#create a line chart
st.line_chart(df_dbh_grouped)

#add map of trees
trees_df = trees_df.dropna(subset=['longitude','latitude'])
trees_df = trees_df.sample(n= 1000, replace=True)
st.map(trees_df)

# with col1:

# with col2:
#     #create a bar chart
#     st.bar_chart(df_dbh_grouped)

# with col3:
#     #create an area chart
#     st.area_chart(df_dbh_grouped)
  


