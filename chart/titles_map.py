import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



class TitlesMap():
    def get_chart(self, *args, **kwargs):


        st.title ('\U0001F3C6 FFL Trophy Map \U0001f5fa')
        st.write('Where do the FFL titles reside? The heatmap below shows which states have the most (darker is better). The table below the map shows the individual titles. The state drop-down on the left allows you to filter by specific states.')
        #st.subheader('Plotly chart')




        #trees_df   = pd.read_csv('trees.csv')
        #data = [['2021','Kevin Wells','Franklin','TN'],['2020','Kirk Hollis','Ponca City','OK']]
        championship_df = pd.read_csv('data/ffl-history.csv')
        championship_df.columns = ['year','owner','city','state']
        #championship_df = pd.DataFrame(data, columns = ['year','owner','city','state'])
        trophy_count_df = championship_df.groupby('state', as_index = False)['year'].count()
        trophy_count_df.columns = ['state_code','trophy_count']
        #trophy_count_df.head()

       #select box for wins/losses/ties
        st.sidebar.subheader('Filter by US state')
        state_selected = st.sidebar.multiselect('State', championship_df['state'].unique())    

        #filter data based on multiselect
        if state_selected:
            championship_df = championship_df[championship_df['state'].isin(state_selected)]
            trophy_count_df = trophy_count_df[trophy_count_df['state_code'].isin(state_selected)]


        # fig = px.choropleth(trophy_count_df,
        #                     locations='state_code', 
        #                     locationmode="USA-states", 
        #                     scope="usa",
        #                     color='trophy_count',
        #                     color_continuous_scale="Viridis_r", 
        #                     )
        # #st.plotly_chart(fig)

        fig2 = go.Figure(data=go.Choropleth(
            locations=trophy_count_df['state_code'], # Spatial coordinates
            z = trophy_count_df['trophy_count'].astype(int), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Reds',
            colorbar_title = "Trophies",
        ))

        fig2.update_layout(
            # title_text = 'FFL Trophies',
            geo_scope='usa', # limite map scope to USA
        )

        st.plotly_chart(fig2)

        championship_df.set_index('year', inplace=True)
        championship_df = championship_df.sort_values(by="year",ascending=False)
        st.table(championship_df)
    



