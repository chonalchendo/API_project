from typing import Any

import pandas as pd
import streamlit as st

from helpers.api_helpers import review_stats_query


def review_metrics(data: dict) -> None:
    c1, c2, c3 = st.columns(3)
    with st.container():
        c1.metric("Overall Rating", f"{data['overallRating']}")
        c2.metric("Review Count", f"{data['reviewCount']}")
        c3.metric("Recommendation Percentage", f"{data['recommendationPercentage']}%")


def create_ratings_df(data: dict, product_name: str) -> pd.DataFrame:
    # plot detailed ratings
    ratings = [round(rating["averageRating"], 2) for rating in data["secondaryRatings"]]
    names = [rating["name"] for rating in data["secondaryRatings"]]
    return pd.DataFrame({"product": product_name, "type": names, "rating": ratings})


def create_dist_df(data: dict, product_name: str) -> pd.DataFrame:
    # plot rating distribution
    rating_counts = [rating["count"] for rating in data["ratingDistribution"]]
    rating_values = [rating["rating"] for rating in data["ratingDistribution"]]
    return pd.DataFrame(
        {"product": product_name, "value": rating_values, "count": rating_counts}
    )


def flatten_review_stats(model: str, product_name: str) -> pd.DataFrame:
    data = review_stats_query(model=model)
    extracted_data = {
        "Product": product_name,
        # "Model ID": data["modelId"],
        "Overall Rating": data["overallRating"],
        "Review Count": data["reviewCount"],
        "Recommended": data["recommendationPercentage"],
    }

    for rating in data["secondaryRatings"]:
        extracted_data[rating["name"]] = round(rating["averageRating"], 2)

    for rating in data["ratingDistribution"]:
        extracted_data[f"{rating['rating']} Star Rating"] = rating["count"]

    return pd.DataFrame([extracted_data])


def display_review_stats(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df = (
        pd.concat([df1, df2])
        .set_index("Product")
        .T.reset_index()
        .rename(columns={"index": "Product"})
        .set_index("Product")
    )
    df.columns.name = None
    return df


def format_review_info(
    df1: list[dict[str, Any]], df2: list[dict[str, Any]]
) -> pd.DataFrame:
    """
    Function to take review data from two products and merge both into a dataframe

    args:
        df1: list[dict[str, Any]] - product review data
        df2: list[dict[str, Any]] - product review data
    returns: pd.DataFrame - pandas dataframe
    """
    data = [*df1, *df2]
    return pd.DataFrame(data)


def create_timeseries_graph(df: pd.DataFrame):
    df["submissionTime"] = df["submissionTime"].dt.strftime("%Y-%m-%d")
