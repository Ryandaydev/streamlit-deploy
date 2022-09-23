import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
#from st_aggrid import AgGrid
from raceplotly.plots import barplot
from collections import deque
#import bar_chart_race as bcr

#p2 stuff
from re import sub
import datetime as dt

st.set_page_config(layout='wide')  

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

with st.sidebar:
    #uses bootstrap icons: https://icons.getbootstrap.com/
    choose = option_menu("Menu", ["P2 Ratings", "FFL History"],
                         icons=['clipboard-data', 'arrow-right-square'],
                         menu_icon="list", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

    # choose = option_menu("Main Menu", ["2-square-fill", "Demo","App", "FFL History"],
    #                      icons=['house', 'file-slides','app-indicator','trophy'],
    #                      menu_icon="list", default_index=0,
    #                      styles={
    #     "container": {"padding": "5!important", "background-color": "#fafafa"},
    #     "icon": {"color": "orange", "font-size": "25px"}, 
    #     "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
    #     "nav-link-selected": {"background-color": "#02ab21"},
    # }
    # )


#logo = Image.open(r'https://data.worldbank.org/assets/images/logo-wb-header-en.svg')
#profile = Image.open(r'https://data.worldbank.org/assets/images/logo-wb-header-en.svg')
if choose == "P2 Ratings":
    #configure the streamlit page
 

    st.title('FFL Performance Power Rating (P2)')
    # col1, col2 = st.columns( [0.8, 0.2])
    # with col1:               # To display the header text using css style
    #     st.markdown(""" <style> .font {
    #     font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    #     </style> """, unsafe_allow_html=True)
    #     st.markdown('<p class="font">About the Creator</p>', unsafe_allow_html=True)    
    # with col2:               # To display brand log
    #     #st.image(logo, width=130 )
    #     print("")
    
    # st.write("Sharone Li is a data science practitioner, enthusiast, and blogger. She writes data science articles and tutorials about Python, data visualization, Streamlit, etc. She is also an amateur violinist who loves classical music.\n\nTo read Sharone's data science posts, please visit her Medium blog at: https://medium.com/@insightsbees")    
    # #st.image(profile, width=700 )
    

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

# elif choose=='Demo':
#     st.markdown(""" <style> .font {
#     font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
#     </style> """, unsafe_allow_html=True)
#     st.markdown('<p class="font">Watch a short demo of the app...</p>', unsafe_allow_html=True)
#     video_file = open('Demo.mp4', 'rb')
#     video_bytes = video_file.read()
#     st.video(video_bytes)


# elif choose=='App':
#     #Add a file uploader to allow users to upload their csv file
#     st.markdown(""" <style> .font {
#     font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
#     </style> """, unsafe_allow_html=True)
#     st.markdown('<p class="font">Upload your data...</p>', unsafe_allow_html=True) #use st.markdown() with CSS style to create a nice-formatted header/text

#     uploaded_file = st.file_uploader('',type=['csv']) #Only accepts csv file format
#     if uploaded_file is not None:     
#         df=pd.read_csv(uploaded_file)  #use AgGrid to create a aggrid table that's more visually appealing than plain pandas datafame
#         grid_response = AgGrid(            
#             df,
#             editable=False, 
#             height=300, 
#             fit_columns_on_grid_load=True,
#             #theme='ALPINE',
#             width=100,
#             allow_unsafe_jscode=True,
#             )
#         updated = grid_response['data']  
#         df = pd.DataFrame(updated) 

#     st.write('---')
#     st.markdown('<p class="font">Set Parameters...</p>', unsafe_allow_html=True)
#     column_list=list(df)
#     column_list = deque(column_list)
#     column_list.appendleft('-')
#     with st.form(key='columns_in_form'):
#         text_style = '<p style="font-family:sans-serif; color:red; font-size: 15px;">***These input fields are required***</p>'
#         st.markdown(text_style, unsafe_allow_html=True)
#         col1, col2, col3 = st.columns( [1, 1, 1])
#         with col1:
#             item_column=st.selectbox('Bar column:',column_list, index=0, help='Choose the column in your data that represents the bars, e.g., countries, teams, etc.') 
#         with col2:    
#             value_column=st.selectbox('Metric column:',column_list, index=0, help='Choose the column in your data that represents the value/metric of each bar, e.g., population, gdp, etc.') 
#         with col3:    
#             time_column=st.selectbox('Time column:',column_list, index=0, help='Choose the column in your data that represents the time series, e.g., year, month, etc.')   

#         text_style = '<p style="font-family:sans-serif; color:blue; font-size: 15px;">***Customize and fine-tune your plot (optional)***</p>'
#         st.markdown(text_style, unsafe_allow_html=True)
#         col4, col5, col6 = st.columns( [1, 1, 1])
#         with col4:
#             direction=st.selectbox('Choose plot orientation:',['-','Horizontal','Vertical'], index=0, help='Specify whether you want the bar chart race to be plotted horizontally or vertically. The default is horizontal' ) 
#             if direction=='Horizontal'or direction=='-':
#                 orientation='horizontal'
#             elif  direction=='Vertical':   
#                 orientation='vertical'
#         with col5:
#             item_label=st.text_input('Add a label for bar column:', help='For example: Top 10 countries in the world by 2020 GDP')  
#         with col6:
#             value_label=st.text_input('add a label for metric column', help='For example: GDP from 1965 - 2020') 

#         col7, col8, col9 = st.columns( [1, 1, 1])
#         with col7:
#             num_items=st.number_input('Choose how many bars to show:', min_value=5, max_value=50, value=10, step=1,help='Enter a number to choose how many bars ranked by the metric column. The default is top 10 items.')
#         with col8:
#             format=st.selectbox('Show by Year or Month:',['-','By Year','By Month'], index=0, help='Choose to show the time series by year or month')
#             if format=='By Year' or format=='-':
#                 date_format='%Y'
#             elif format=='By Month':
#                 date_format='%x'   
#         with col9:
#             chart_title=st.text_input('Add a chart title', help='Add a chart title to your plot')    
        
#         col10, col11, col12 = st.columns( [1, 1, 1])
#         with col10:
#             speed=st.slider('Animation Speed',10,500,100, step=10, help='Adjust the speed of animation')
#             frame_duration=500-speed  
#         with col11:
#             chart_width=st.slider('Chart Width',500,1000,500, step=20, help='Adjust the width of the chart')
#         with col12:    
#             chart_height=st.slider('Chart Height',500,1000,600, step=20, help='Adjust the height of the chart')

#         submitted = st.form_submit_button('Submit')



#         st.write('---')
#         if submitted:        
#             if item_column=='-'or value_column=='-'or time_column=='-':
#                 st.warning("You must complete the required fields")
#             else: 
#                 st.markdown('<p class="font">Generating your bar chart race plot... And Done!</p>', unsafe_allow_html=True)   
#                 df['time_column'] = pd.to_datetime(df[time_column])
#                 df['value_column'] = df[value_column].astype(float)
     
#                 raceplot = barplot(df,  item_column=item_column, value_column=value_column, time_column=time_column,top_entries=num_items)
#                 fig=raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format=date_format,orientation=orientation)
#                 fig.update_layout(
#                 title=chart_title,
#                 autosize=False,
#                 width=chart_width,
#                 height=chart_height,
#                 paper_bgcolor="lightgray",
#                 )
#                 st.plotly_chart(fig, use_container_width=True)


elif choose == "FFL History":
    # st.markdown(""" <style> .font {
    # font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    # </style> """, unsafe_allow_html=True)
    # st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    # with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    #     #st.write('Please help us improve!')
    #     Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
    #     Email=st.text_input(label='Please Enter Email') #Collect user feedback
    #     Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
    #     submitted = st.form_submit_button('Submit')
    #     if submitted:
    #         st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')
    #st.markdown('<p class="font">Generating your bar chart race plot... And Done!</p>', unsafe_allow_html=True)   
    ffl_df=pd.read_csv('data/final_clean_data_manual.csv')  #use AgGrid to create a aggrid table that's more visually appealing than plain pandas datafame
    # grid_response = AgGrid(            
    #     ffl_df,
    #     editable=False, 
    #     height=300, 
    #     fit_columns_on_grid_load=True,
    #     #theme='ALPINE',
    #     width=100,
    #     allow_unsafe_jscode=True,
    #     )
    # updated = grid_response['data']  
    #ffl_df = pd.DataFrame(updated) 

    #add filter
    st.subheader('FFL History in Motion')
    metric_selected = st.sidebar.selectbox('Select Wins/Losses/Ties', ['Career Wins','Career Losses','Career Ties'], index=0)
    # value_column = 'h2hw_sum'
    # value_label = 'Career wins'


    #col1, col2, col3 = st.columns((1, 1, 1))

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


        #st.subheader('Wins')

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
    
    # st.subheader('Losses')

    # value_column = 'h2hl_sum'
    # value_label = 'Career losses'

    # raceplot = barplot(ffl_df,  item_column=item_column, value_column=value_column, time_column=time_column,top_entries=num_items)
    # fig=raceplot.plot(item_label = item_label, value_label = value_label, frame_duration = frame_duration, date_format=date_format,orientation=orientation)
    # fig.update_layout(
    # title=chart_title,
    # autosize=False,
    # width=chart_width,
    # height=chart_height,
    # paper_bgcolor="lightgray",
    # )
    # st.plotly_chart(fig, use_container_width=True)
    

