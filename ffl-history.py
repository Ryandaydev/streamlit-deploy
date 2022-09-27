from email.policy import default
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
from raceplotly.plots import barplot
from collections import deque
#p2 stuff
from re import sub
import datetime as dt

#page formatting
st.set_page_config(layout='wide')  

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

#create the sidebar
# with st.sidebar:
#     #uses bootstrap icons: https://icons.getbootstrap.com/
#     choose = option_menu("Menu", ["FFL History in Motion", "P2 Ratings"],
#                          icons=['arrow-right-square', 'clipboard-data'],
#                          menu_icon="list", default_index=0,
#                          styles={
#         "container": {"padding": "5!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"}, 
#         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#02ab21"},
#     }
#     )

#if choose == "P2 Ratings":
# st.title('FFL Performance Power Rating (P2)')

# p2_df = pd.read_csv('data/p2_with_rank.csv')



# #special df for week1
# p2_week1_df = p2_df[p2_df.Week == 1]
# p2_week1_df = p2_week1_df[["Franchise","Rank","Win %","Points","H2H","P2"]]

# #p2_week1_df = p2_df.query("p2_df.Week == 1")

# p2_df["Previous_Rank"] = p2_df["Previous_Rank"].astype('Int64')


# st.sidebar.subheader('Select week for P2')
# #add filter on sidebar, select the largest number
# week_filter = st.sidebar.selectbox('FFL Week', p2_df['Week'].unique(),index = p2_df['Week'].nunique() - 1)
# if week_filter:
#     p2_df = p2_df[p2_df['Week'] == week_filter]
#     p2_df = p2_df[["Franchise","Rank","Previous_Rank","Win %","Points","H2H","P2"]]
#     st.subheader('Week: ' + str(week_filter))




# def p2_formatting(row):    

#     moving_up = 'background-color: lightgreen;'
#     heading_down = 'background-color: lightcoral;'
#     default = ''

#     # must return one string per cell in this row
#     if row['Rank'] > row['Previous_Rank']:
#         return [heading_down, default, heading_down]
#     elif row['Previous_Rank'] > row['Rank']:
#         return [moving_up, default, moving_up]
#     else:
#         return [default, default, default]


# # CSS to inject contained in a string
# hide_table_row_index = """
#             <style>
#             thead tr th:first-child {display:none}
#             tbody th {display:none}
#             </style>
#             """

# # Inject CSS with Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)

# #decide how to format
# if week_filter == 1:
#     st.table(p2_week1_df.style.hide_index())
# else:
#     st.table(p2_df.style.apply(p2_formatting, subset=['Rank', 'Previous_Rank','Franchise'], axis=1))

# heading_up_moving_down = """
# <span style="background-color: lightgreen">Movin' Up</span>
# <br />
# <span style="background-color: lightcoral">Heading Down</span>
    
# """
# st.markdown(heading_up_moving_down, unsafe_allow_html=True)





#elif choose == "FFL History in Motion":

ffl_df=pd.read_csv('data/final_clean_data_manual.csv')  
st.subheader('FFL History in Motion')

#select box for wins/losses/ties
st.sidebar.subheader('Select category for history chart')
metric_selected = st.sidebar.selectbox('Wins/Losses/Ties', ['Career Wins','Career Losses','Career Ties'], index=0)
# value_column = 'h2hw_sum'
# value_label = 'Career wins'

#create multiselect in sidebar for owners
st.sidebar.subheader('Select owners to include')
owners_selected = st.sidebar.multiselect('Owners', ffl_df['owner_name'].unique())

#filter data based on multiselect
if owners_selected:
    ffl_df = ffl_df[ffl_df['owner_name'].isin(owners_selected)]

#todo:create start & end year ranges

#filter data based on multiselect
if owners_selected:
    ffl_df = ffl_df[ffl_df['owner_name'].isin(owners_selected)]


if metric_selected:
    #st.write(metric_selected)
    if metric_selected == 'Career Wins':
        value_column = 'h2hw_sum'
        value_label = 'Career Wins'
    # st.subheader('Wins')
    elif metric_selected == 'Career Losses':
        value_column = 'h2hl_sum'
        value_label = 'Career losses'
        #st.subheader('Losses')
    elif metric_selected == 'Career Ties':
        value_column = 'h2ht_sum'
        value_label = 'Career ties'
        #st.subheader('Losses')


    #ffl_df['item_column'] = ffl_df['owner_name']
    #ffl_df['time_column'] = pd.to_datetime(ffl_df['year'])
    #ffl_df['value_column'] = ffl_df['h2hw_sum'].astype(float)

    item_column = 'owner_name'
    #value_column = 'h2hw_sum'
    time_column = 'year'
    num_items = 15 #20 owners 
    item_label = 'Owners'
    #value_label = 'Career wins'
    frame_duration = 1000
    date_format = 'yearly'
    orientation = 'horizontal'
    chart_title =  'FFL history'
    chart_width = 700
    chart_height = 570


    #https://support.sisense.com/kb/en/article/remove-whitespace-margins-from-plotly-charts

    raceplot = barplot(ffl_df,  item_column=item_column, value_column=value_column, time_column=time_column,top_entries=num_items)
    fig=raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format=date_format,orientation=orientation)
    fig.update_layout(
    #title=chart_title,
    autosize=True,
    width=chart_width,
    height=chart_height,
    paper_bgcolor="lightgray",
    margin_t=25 #top margin of chart -         #https://plotly.com/python/reference/#layout-margin
    )
    st.plotly_chart(fig, use_container_width=True)
    

    

