import streamlit as st
# from chart.p2 import P2
from chart.titles_map import TitlesMap
from chart.wins_race import WinsRace
from chart.scoring_box_plots import ScoringBoxPlots


PAGE_TITLE = "\U0001F3C6 FFL History \U0001F3C8"
CHARTS = {
    "Welcome": {},
    # "P2": {
    #     "class": P2,
    #     "args": [],
    #     "kwargs": {},
    # },
    "FFL Titles Map": {
        "class": TitlesMap,
        "args": [],
        "kwargs": {},
    },

    # "All Time Standings": {
    #     "class": AllTimeStandings,
    #     "args": [],
    #     "kwargs": {},
    # },  
    "Regular Season Scoring Chart": {
        "class": ScoringBoxPlots,
        "args": [],
        "kwargs": {},
    },    
    "Career Wins Chart": {
        "class": WinsRace,
        "args": [],
        "kwargs": {},
    },    

}

def run():
    st.set_page_config(
            page_title=PAGE_TITLE,
            layout="wide",
            initial_sidebar_state="expanded",
        )
    #st.title(PAGE_TITLE)
    st.sidebar.header(PAGE_TITLE)
    chart_name = st.sidebar.radio("Select a page:", CHARTS, 0)
    if chart_name == "Welcome":
        #PAGE_TITLE = "\U0001F3C6 FFL History \U0001F3C8"
        st.title ('\U0001F3C6 History and Statistics of the Illustrious FFL \U0001F3C8')
        st.write(
            """Welcome to the extended statistics site of the FFL!"""
            """\n\n<---- Choose a page in the left sidebar."""
            # """\n\nUse the ">" symbol in the upper left corner to expand the"""
            # """ sidebar if it is not visible."""
            """\n\nThanks to Robert Astel for the example site: https://github.com/robastel/fantasy_football_app"""
        )

    else:
        chart_dict = CHARTS[chart_name]
        #class_instance = chart_dict["class"](chart_dict["sql"])
        class_instance = chart_dict["class"]()
        #df = class_instance.get_df()
        class_instance.get_chart(
            *chart_dict["args"], **chart_dict["kwargs"]
        )


if __name__ == "__main__":
    run()
