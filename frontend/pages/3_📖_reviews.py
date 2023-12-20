import pandas as pd
import streamlit as st
from src.components.display.reviews import review_metrics
from src.components.graphs import (
    create_timeseries_graph,
    distribution_figure,
    ratings_figure,
    review_locations_graph,
    review_questions_graph,
)
from src.data.adidas.reviews import (
    create_dist_df,
    create_ratings_df,
    create_review_location_df,
    create_review_questions_df,
    create_review_timeseries_df,
    display_review_stats,
    flatten_review_stats,
)
from src.helpers.api_helpers import (
    get_all_products,
    product_api_query,
    review_stats_query,
    reviews_api_query,
)

st.set_page_config(
    page_title="Reviews",
    page_icon="📖",
    layout="wide",
    menu_items={
        "Get help": "https://github.com/chonalchendo/API_project",
        "About": "# An app designed to help athletes decide what product is best for them.",
    },
)


st.title("Compare review information")

products = get_all_products()
product_names = [product["name"] for product in products]

col1, col2 = st.columns(2)

with col1:
    product_1 = st.selectbox("Product 1", product_names, index=None)
    if not product_1:
        st.info("Please select a product.", icon="ℹ️")
    else:
        st.success(f"You have selected product {product_1}!", icon="✅")

with col2:
    product_2 = st.selectbox("Product 2", product_names, index=None)
    if not product_2:
        st.info("Please select a product.", icon="ℹ️")
    else:
        st.success(f"You have selected product {product_2}!", icon="✅")


# Return data on both products
if product_1 and product_2:
    for product in products:
        if product_1 == product["name"]:
            prod_1 = product["product_id"]
        if product_2 == product["name"]:
            prod_2 = product["product_id"]

    data_1 = product_api_query(product=prod_1)
    data_2 = product_api_query(product=prod_2)

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

    # TODO: CREATE DATAFRAME FOR TIMESERIES GRAPHS
    time_df_1 = create_review_timeseries_df(api=total_reviews)
    time_df_2 = create_review_timeseries_df(api=total_reviews_2)

    # concatenate timeseries dataframes
    ts_df = pd.concat([time_df_1, time_df_2])
    reviews_time = create_timeseries_graph(ts_df)

    # review locations graphs
    loc_df_1 = create_review_location_df(api=total_reviews)
    loc_df_2 = create_review_location_df(api=total_reviews_2)

    loc_df = pd.concat([loc_df_1, loc_df_2])
    loc_graph = review_locations_graph(df=loc_df)

    # review questions graphs
    qs_df_1 = create_review_questions_df(api=reviews)
    qs_df_2 = create_review_questions_df(api=reviews_2)

    qs_df = pd.concat([qs_df_1, qs_df_2])

    questions = tuple(qs_df_1["label"].unique())

    col_1, col_2 = st.columns(2)

    with col_1:
        st.plotly_chart(ratings_fig, use_container_width=True)
        st.plotly_chart(reviews_time, use_container_width=True)
        selector = st.selectbox("Select graph metric", questions)
        qs_graph_1 = review_questions_graph(df=qs_df, question=selector)
        st.plotly_chart(qs_graph_1, use_container_width=True)
        # with st.expander("Ratings insights"):
        #     st.write("This is what people have rated this product for width etc.")

    with col_2:
        st.plotly_chart(dist_fig, use_container_width=True)
        st.plotly_chart(loc_graph, use_container_width=True)
        # with st.expander("Distribution insights"):
        #     st.write("This is how people have voted")
        #

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
