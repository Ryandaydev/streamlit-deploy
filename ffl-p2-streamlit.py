#p129
from re import sub
import pandas as pd
import streamlit as st
import datetime as dt
#import seaborn as sns
#import matplotlib.pyplot as plt

#configure the streamlit page
st.set_page_config(layout='wide')

st.title('FFL Performance Power Rating (P2)')




#p2_df = pd.read_csv('data/p2_weekly_with_rank.csv', index_col = 0)
p2_df = pd.read_csv('data/p2_with_rank.csv')

#special df for week1
p2_week1_df = p2_df[p2_df.Week == 1]
p2_week1_df = p2_week1_df[["Franchise","Rank","Win %","Points","H2H","P2"]]

#p2_week1_df = p2_df.query("p2_df.Week == 1")

p2_df["Previous_Rank"] = p2_df["Previous_Rank"].astype('Int64')



#add filter on sidebar
week_filter = st.sidebar.selectbox('FFL_week', p2_df['Week'].unique())
if week_filter:
    p2_df = p2_df[p2_df['Week'] == week_filter]
    p2_df = p2_df[["Franchise","Rank","Previous_Rank","Win %","Points","H2H","P2"]]
    st.subheader('Week: ' + str(week_filter))


#st.table(p2_df.iloc[:, : 5].style.hide_index())
#st.write(p2_df.iloc[:, : 6].style.hide_index())

#todo: make fancy style
#https://pandas.pydata.org/docs/user_guide/style.html

def p2_formatting(row):    

    moving_up = 'background-color: lightgreen;'
    heading_down = 'background-color: lightcoral;'
    default = ''

    # must return one string per cell in this row
    if row['Rank'] > row['Previous_Rank']:
        return [heading_down, default, heading_down]
    elif row['Previous_Rank'] > row['Rank']:
        return [moving_up, default, moving_up]
    else:
        return [default, default, default]


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

#decide how to format
if week_filter == 1:
    st.table(p2_week1_df.style.hide_index())
else:
    st.table(p2_df.style.apply(p2_formatting, subset=['Rank', 'Previous_Rank','Franchise'], axis=1))
