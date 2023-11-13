import pandas as pd
import plotly.express as px
from frontend.helpers.api_helpers import return_reviews_db
from plotly.graph_objects import Figure
from rich import print


def create_timeseries_graph(df: pd.DataFrame) -> Figure:
    """
    Function that creates a timeseries graph of monthly reviews
    to display a products popularity.

    Args:
        df: pd.DataFrame - pandas dataframe

    Return:
        Figure - plotly line graph
    """
    df["submissionTime"] = pd.to_datetime(df["submissionTime"])
    df["monthly_reviews"] = df["submissionTime"].dt.strftime("%Y-%m")
    new_df = (
        df["monthly_reviews"]
        .value_counts()
        .reset_index()
        .sort_values(by="monthly_reviews")
    )
    fig = px.line(
        new_df,
        x="monthly_reviews",
        y="count",
        markers=True,
        color_discrete_sequence=["#FF006E"],
    )
    fig.update_traces(textposition="top right")

    fig.add_bar(
        x=new_df["monthly_reviews"],
        y=new_df["count"],
        marker=dict(color="#8338EC"),
        showlegend=False,
        name="Monthly",
    )
    fig.update_layout(
        {
            "title": f"Number of Reviews for Model {df['modelId'][0]}",
            "xaxis": {"title": "Monthly Reviews"},
            "yaxis": {"title": "Total Reviews"},
            "showlegend": False,
        }
    )
    return fig


if __name__ == "__main__":
    model = "KGO51"
    resp = return_reviews_db(model=model)
    data = pd.DataFrame(resp)
    print(data)
    graph = create_timeseries_graph(df=data)
    # print(graph)
    graph.show()
