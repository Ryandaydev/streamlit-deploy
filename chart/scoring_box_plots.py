import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# from chart.helpers.charter import Charter
from chart.helpers import constants


class ScoringBoxPlots():
    def get_chart(self, *args, **kwargs):

        st.title ('\U0001f3c8 Regular Season Scoring Chart \U0001f4c8')
        st.subheader('Regular Season Games: 2017-2021')
        st.write('The chart below shows which owners scored consistently highest over the last 5 regular seasons, along with the highs and lows. (See below for more details on reading the chart.)')



        df = pd.read_csv('data/regular_season_scoring.csv')
        #columns: manager, points


        manager_medians = (
            df.groupby("manager")["points"].median().sort_values()
        )
        managers = manager_medians.index
        normalized_medians = mcolors.Normalize(
            vmin=manager_medians.min(),
            vmax=manager_medians.max(),
        )
        color_map = plt.cm.get_cmap("RdYlGn")
        fig = go.Figure()
        for manager, median in zip(managers, manager_medians):
            fig.add_trace(
                go.Box(
                    x=df[df["manager"] == manager]["points"],
                    name=manager,
                    orientation=kwargs.get("orientation", "h"),
                    line_color=f"rgba{str(color_map(normalized_medians(median)))}",
                    boxpoints=False,
                    fillcolor="rgba(0, 0, 0, 0)",
                )
            )
        fig.update_layout(
            **constants.PLOTLY_DEFAULT_LAYOUT_KWARGS,
            title_text="Regular Season Scoring: 2017 - 2021",
            xaxis_title_text="Weekly Points Scored",
            xaxis_showgrid=True,
            xaxis_tickvals=list(range(0, 250, 20)),
            xaxis_zeroline=False,
            yaxis_title_text="Manager",
            yaxis_showgrid=False,
            showlegend=False,
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )
        st.write(
            "Explanation:"
            "\n\nEach manager has a boxplot consisting of 5 values."
            "\n - The leftmost tick represents the manager's least number of"
            " points ever scored in a week."
            "\n - The left side of the box represents the manager's 25th"
            " percentile score. Roughly 25% of the manager's all time scores"
            " fall below this score (meaning roughly 75% are greater than this"
            " score)."
            "\n - The line within the box represents the manager's median"
            " score. Roughly 50% of the manager's all time scores fall on"
            " either side of this score."
            "\n - The right side of the box represents the manager's 75th"
            " percentile score. Roughly 75% of the manager's all time scores"
            " fall below this score (meaning roughly 25% are greater than this"
            " score)."
            "\n - The rightmost tick represents the manager's greatest number"
            " of points ever scored in a week."
        )
