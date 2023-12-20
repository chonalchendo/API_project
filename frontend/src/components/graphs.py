import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from src.helpers.api_helpers import review_stats_query


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
        df.groupby("modelId")["monthly_reviews"]
        .value_counts()
        .reset_index()
        .sort_values(by="monthly_reviews")
    )

    models = new_df["modelId"].unique().tolist()
    model_1 = new_df.loc[new_df["modelId"] == models[0]]
    model_2 = new_df.loc[new_df["modelId"] == models[1]]

    fig = px.line(
        new_df,
        x="monthly_reviews",
        y="count",
        color="modelId",
        markers=True,
        # color_discrete_sequence=["#FF006E"],
    )
    fig.update_traces(textposition="top right")

    fig.add_bar(
        x=model_1["monthly_reviews"],
        y=model_1["count"],
        # offsetgroup=new_df["modelId"],
        marker=dict(color="#8338EC"),
        showlegend=False,
        name="Monthly",
    )
    fig.add_bar(
        x=model_2["monthly_reviews"],
        y=model_2["count"],
        marker=dict(color="#F72585"),
        showlegend=False,
        name="Monthly",
    )
    fig.update_layout(
        {
            "title": f"Time series comparison between {models[0]} and {models[1]}",
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


def review_locations_graph(df: pd.DataFrame) -> Figure:
    """Create a bar chart of the locations of reviewers.

    Args:
        df (pd.DataFrame): dataframe of the locations of reviewers

    Returns:
        Figure: plotly bar chart
    """
    dff = df.groupby("modelId")["locations"].value_counts().reset_index()
    graph = px.bar(
        dff,
        x="locations",
        y="count",
        color="modelId",
        barmode="group",
        title="Location of Reviewers",
    )
    return graph


def review_questions_graph(df: pd.DataFrame, question: str) -> Figure:
    """Create a bar chart of the locations of reviewers.

    Args:
        df (pd.DataFrame): dataframe of the locations of reviewers
        question (str): review question

    Returns:
        Figure: plotly bar chart
    """
    dff = df.loc[df["label"] == question].sort_values("reviewCount", ascending=False)
    return px.bar(
        dff,
        x="answerLabel",
        y="reviewCount",
        color="modelId",
        barmode="group",
        title=f"Customer use of product: {question}",
    )


if __name__ == "__main__":
    model = "MBU20"
    stats = review_stats_query(model=model)
