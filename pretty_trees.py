import pandas as pd
import streamlit as st
import numpy as np

#configure the streamlit page
st.set_page_config(layout='wide')

st.title('SF Trees')
trees_df = pd.read_csv('trees.csv')

col1, col2, col3 = st.columns((1, 1, 1))

#code copied from trees.py
#group by dbh
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['tree_count']
#create a line chart



with col1:
    st.line_chart(df_dbh_grouped)

with col2:
    #create a bar chart
    st.bar_chart(df_dbh_grouped)

with col3:
    #create an area chart
    st.area_chart(df_dbh_grouped)
    


