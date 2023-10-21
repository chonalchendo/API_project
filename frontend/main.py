import json
import time
from io import BytesIO

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from rich import print

# User is prompted to ask a question about product reviews
# Spinner to indicate the question is being processed
# The response is returned in a text box
# A link to the product and a photo of the product is displayed with the AI response

# need to create a post request to take in the users query from streamlit
# question is then posted into one of the functions detailed in the reviews_utils file
# return the response of the post request via st.text


class Config:
    REVIEWS = ("helpful", "relevant", "newest")


def create_bar_graph(df: pd.DataFrame, x_axis: str, y_axis: str, title: str) -> px.bar:
    return px.bar(data_frame=df, x=x_axis, y=y_axis, title=title)


def response_handler(response: httpx.get) -> json:
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Error: {response.status_code} - {response.text}")


def vis_metrics(data: dict) -> None:
    c1, c2, c3 = st.columns(3)
    with st.container():
        c1.metric("Overall Rating", f"{data['overallRating']}")
        c2.metric("Review Count", f"{data['reviewCount']}")
        c3.metric("Recommendation Percentage", f"{data['recommendationPercentage']}%")


def create_ratings_df(data: dict, product_name: str) -> pd.DataFrame:
    # plot detailed ratings
    ratings = [rating["averageRating"] for rating in data["secondaryRatings"]]
    names = [rating["name"] for rating in data["secondaryRatings"]]
    return pd.DataFrame({"product": product_name, "type": names, "rating": ratings})


def create_dist_df(data: dict, product_name: str) -> pd.DataFrame:
    # plot rating distribution
    rating_counts = [rating["count"] for rating in data["ratingDistribution"]]
    rating_values = [rating["rating"] for rating in data["ratingDistribution"]]
    return pd.DataFrame(
        {"product": product_name, "value": rating_values, "count": rating_counts}
    )


def return_product_info(product: str | None = None, model: str | None = None):
    if product:
        api = f"http://localhost:8000/api/v1/product/{product}"
    if model:
        api = f"http://localhost:8000/api/v1/reviews/stats/{model}/"
    response = httpx.get(api, timeout=100)
    data = response_handler(response).pop(0)
    return data


def open_image(image_url: str):
    get_image = httpx.get(image_url)
    image = Image.open(BytesIO(get_image.content))
    return image


def main() -> None:
    st.title("Blue Ribbon II")

    ### PRODUCT INFO ###
    with st.sidebar:
        st.write("What products would you like to compare?")
        product = st.text_input("Product 1", key="product_1")
        st.write("Vs")
        product_2 = st.text_input("Product 2", key="product_2")

    if product and product_2:
        data = return_product_info(product=product)
        time.sleep(5)
        data_2 = return_product_info(product=product_2)

        # display product info
        st.title(f"{data['name']} Vs {data_2['name']}")

        c6, c7 = st.columns(2)
        with st.container():
            c6.write(f"About: {data['product_description']['text']}")
            c7.write(f"About: {data_2['product_description']['text']}")

            c6.image(
                data["view_list"][0]["image_url"],
                caption=data["product_description"]["subtitle"],
            )
            c7.image(
                data_2["view_list"][0]["image_url"],
                caption=data_2["product_description"]["subtitle"],
            )
            ### STATS ####
            reviews = return_product_info(model=data["model_number"])
            reviews_2 = return_product_info(model=data_2["model_number"])

            # visualise the metric data
            vis_metrics(reviews)
            vis_metrics(reviews_2)

        # create ratings and dist dataframes
        ratings_df_1 = create_ratings_df(data=reviews, product_name=data["name"])
        dist_df_1 = create_dist_df(data=reviews, product_name=data["name"])

        ratings_df_2 = create_ratings_df(data=reviews_2, product_name=data_2["name"])
        dist_df_2 = create_dist_df(data=reviews_2, product_name=data_2["name"])

        # concatenate the two dataframes
        ratings_df = pd.concat([ratings_df_1, ratings_df_2])
        dist_df = pd.concat([dist_df_1, dist_df_2])

        # create visualisations with the new data
        ratings_fig = px.bar(
            ratings_df, x="type", y="rating", color="product", barmode="group"
        )
        ratings_fig.update_layout(showlegend=False)

        dist_fig = px.bar(
            dist_df, x="value", y="count", color="product", barmode="group"
        )
        dist_fig.update_layout(showlegend=False)

        st.plotly_chart(ratings_fig)
        st.plotly_chart(dist_fig)
        # plot the visualisations
        # c4, c5 = st.columns(2)
        # with st.container():
        # c4.plotly_chart(ratings_fig, use_container_width=True)
        # c5.plotly_chart(dist_fig, use_container_width=True)

    ### AI REVIEW QUERY ###

    sort = st.selectbox(
        "What type of reviews would you like to know about?", (Config.REVIEWS)
    )

    question = st.text_input(
        "What would you like to know about a product?", key="question"
    )
    URL = (
        f"http://localhost:8000/api/v1/reviews/sports/customer_query/{question}/{sort}"
    )

    if st.button("Submit"):
        with st.spinner("Processing AI response..."):
            response = httpx.post(URL, timeout=100)
            if response.status_code == 200:
                data = response.json()
                st.write(data["response"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    main()
