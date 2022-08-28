#p129
from re import sub
import pandas as pd
import streamlit as st
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

#configure the streamlit page
#st.set_page_config(layout='wide')

st.title('SF Trees On The Web')
st.write("Data from SF DPW")
trees_df = pd.read_csv('trees.csv')
#add filter on sidebar
owners = st.sidebar.multiselect('Tree owner filter', trees_df['caretaker'].unique())

trees_df['age'] = (pd.to_datetime('today') - pd.to_datetime(trees_df['date'])).dt.days


if owners:
    trees_df = trees_df[trees_df['caretaker'].isin(owners)]

#code copied from trees.py
#group by dbh
df_dbh_grouped = pd.DataFrame(trees_df.groupby(['dbh']).count()['tree_id'])
df_dbh_grouped.columns = ['tree_count']

#layout section
col1, col2 = st.columns(2)

with col1:
    st.write('Trees by Width')
    fig_1, ax_1 = plt.subplots()
    ax_1 = sns.histplot(trees_df['dbh'])
    plt.xlabel('Tree width')
    st.pyplot(fig_1)


with col2:
    st.write('Trees by Age')
    fig_2, ax_2 = plt.subplots()
    ax_2 = sns.histplot(trees_df['age'])
    plt.xlabel('Age (days)')
    st.pyplot(fig_2)

#add map of trees
trees_df = trees_df.dropna(subset=['longitude','latitude'])
trees_df = trees_df.sample(n= 1000, replace=True)
st.map(trees_df)
