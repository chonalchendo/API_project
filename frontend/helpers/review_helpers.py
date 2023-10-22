import pandas as pd
import streamlit as st


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
