import pandas as pd
import streamlit as st
from components.graphs import (
    create_timeseries_graph,
    distribution_figure,
    ratings_figure,
)
from helpers.api_helpers import review_stats_query, reviews_api_query
from helpers.review_helpers import (
    create_dist_df,
    create_ratings_df,
    display_review_stats,
    flatten_review_stats,
    review_metrics,
)


def reviews_page(data_1: dict, data_2: dict) -> None:
    """
    Function to create the reviews page.

    args:
        data_1 (dict): Data dictionary of first product
        data_2 (dict): Data dictionary of second product

    return (None): Streamlit tab
    """
    reviews = review_stats_query(model=data_1["model_number"])
    reviews_2 = review_stats_query(model=data_2["model_number"])

    total_reviews = reviews_api_query(model=data_1["model_number"])
    total_reviews_2 = reviews_api_query(model=data_2["model_number"])

    st.header("Review comparison", divider="rainbow")
    # visualise the metric data

    col_1, col_2 = st.columns(2)

    with col_1:
        st.subheader(f":blue[{data_1['name']}]")
        review_metrics(reviews)
    with col_2:
        st.subheader(f":red[{data_2['name']}]")
        review_metrics(reviews_2)

    # create ratings and dist dataframes
    ratings_df_1 = create_ratings_df(data=reviews, product_name=data_1["name"])
    dist_df_1 = create_dist_df(data=reviews, product_name=data_1["name"])

    ratings_df_2 = create_ratings_df(data=reviews_2, product_name=data_2["name"])
    dist_df_2 = create_dist_df(data=reviews_2, product_name=data_2["name"])

    # concatenate the two dataframes
    ratings_df = pd.concat([ratings_df_1, ratings_df_2])
    dist_df = pd.concat([dist_df_1, dist_df_2])

    # create visualisations with the new data
    ratings_fig = ratings_figure(df=ratings_df)
    dist_fig = distribution_figure(df=dist_df)

    reviews_time = create_timeseries_graph(df=total_reviews)
    reviews_time_2 = create_timeseries_graph(df=total_reviews_2)

    col_1, col_2 = st.columns(2)

    with col_1:
        st.plotly_chart(ratings_fig, use_container_width=True)
        st.plotly_chart(reviews_time, use_container_width=True)
        with st.expander("Ratings insights"):
            st.write("This is what people have rated this product for width etc.")
    with col_2:
        st.plotly_chart(dist_fig, use_container_width=True)
        st.plotly_chart(reviews_time_2, use_container_width=True)
        with st.expander("Distribution insights"):
            st.write("This is how people have voted")

    df_1 = flatten_review_stats(
        model=data_1["model_number"], product_name=data_1["name"]
    )
    df_2 = flatten_review_stats(
        model=data_2["model_number"], product_name=data_2["name"]
    )
    df = display_review_stats(df_1, df_2)
    product_df = df.iloc[:3]
    second_ratings = df.iloc[3:7]
    rating_dist = df.iloc[7:]

    col_1, col_2, col_3 = st.columns(3)

    with col_1:
        with st.expander("General Review Stats"):
            st.dataframe(
                data=(
                    product_df.style.format("{:.1f}")
                    .highlight_max(axis=1, color="green")
                    .highlight_min(axis=1, color="red")
                ),
                use_container_width=True,
            )

    with col_2:
        with st.expander("Detailed Ratings"):
            st.dataframe(
                data=(
                    second_ratings.style.format("{:.2f}")
                    .highlight_max(axis=1, color="green")
                    .highlight_min(axis=1, color="red")
                ),
                use_container_width=True,
            )

    with col_3:
        with st.expander("Ratings Distribution"):
            st.dataframe(
                data=(
                    rating_dist.style.format("{:.0f}")
                    .highlight_max(axis=1, color="green")
                    .highlight_min(axis=1, color="red")
                ),
                use_container_width=True,
            )
