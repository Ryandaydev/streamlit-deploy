#from email.policy import default
import streamlit as st
#from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
#from  PIL import Image
import numpy as np
import pandas as pd
from raceplotly.plots import barplot
from collections import deque
#p2 stuff
from re import sub
import datetime as dt

 





class WinsRace():
    def get_chart(self, *args, **kwargs):

        reduce_header_height_style = """
            <style>
                div.block-container {padding-top:1rem;}
            </style>
        """
        st.markdown(reduce_header_height_style, unsafe_allow_html=True)
        
        
        ffl_df=pd.read_csv('data/final_clean_data_manual.csv')  
        st.subheader('\U0001f3ce FFL History Chart Race \U0001f3cd')
        st.write('Click the play button to watch the teams race to the highest win totals.')

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
            #paper_bgcolor="lightgray",
            paper_bgcolor="blue",
            margin_t=25 #top margin of chart -         #https://plotly.com/python/reference/#layout-margin
            )
            st.plotly_chart(fig, use_container_width=True)
    

    

