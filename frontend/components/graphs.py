import pandas as pd
import plotly.express as px
from frontend.helpers.api_helpers import reviews_api_query
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


def ratings_figure(df: pd.DataFrame) -> Figure:
    """Creates a bar chart of the ratings of the products

    Args:
        df (pd.DataFrame): dataframe of the ratings

    Returns:
        Figure: plotly bar chart
    """
    ratings_fig = px.bar(
        df,
        x="type",
        y="rating",
        color="product",
        barmode="group",
        text="rating",
        title="Detailed ratings of products",
    )
    ratings_fig.update_layout(
        legend=dict(
            font=dict(color="black", size=12),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        )
    )
    ratings_fig.update_traces(textposition="outside", texttemplate="%{text}")
    return ratings_fig


def distribution_figure(df: pd.DataFrame) -> Figure:
    """Creates a bar chart of the distribution of the ratings

    Args:
        df (pd.DataFrame): dataframe of the ratings

    Returns:
        Figure: plotly bar chart
    """
    dist_fig = px.bar(
        df,
        x="value",
        y="count",
        color="product",
        barmode="group",
        text="count",
        title="Ratings distribution",
    )
    dist_fig.update_layout(
        legend=dict(
            font=dict(color="#000000", size=12),
            bgcolor="lightSteelBlue",
            bordercolor="Black",
            borderwidth=2,
        )
    )
    dist_fig.update_traces(textposition="outside", texttemplate="%{text}")
    return dist_fig


if __name__ == "__main__":
    model = "DLQ15"
    resp = reviews_api_query(model=model)
    data = pd.DataFrame(resp)
    print(data)
    graph = create_timeseries_graph(df=data)
    # print(graph)
    graph.show()
