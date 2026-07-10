# visualization.py

import plotly.express as px

def sales_chart(df):

    fig = px.bar(
        df,
        x="Category",
        y="Sales"
    )

    return fig