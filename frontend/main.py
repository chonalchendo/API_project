import time

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st
from helpers.api_helpers import return_product_info
from helpers.product_helpers import (get_product_images, product_details,
                                     product_metrics)
from helpers.review_helpers import (create_dist_df, create_ratings_df,
                                    review_metrics)

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


def main() -> None:
    st.set_page_config(
        page_title="Blue Ribbon II - sports product comparison app",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.title("Blue Ribbon II - the sports comparison app")
    st.markdown("_Prototype v0.0.1_")

    ### PRODUCT INFO ###
    with st.sidebar:
        st.write("What products would you like to compare?")
        product = st.text_input("Product 1", key="product_1")
        st.write("Vs")
        product_2 = st.text_input("Product 2", key="product_2")

    product_tab, review_tab = st.tabs(["Product Info", "Review Info"])

    if product and product_2:
        with product_tab:
            data = return_product_info(product=product)
            data_2 = return_product_info(product=product_2)

            # display product info
            st.title(f"{data['name']} Vs {data_2['name']}")

            images_1 = get_product_images(data)
            images_2 = get_product_images(data_2)

            index = 0

            if st.button("Next"):
                index += 1

            if st.button("Prev"):
                if index > 0:
                    index = index - 1

            c6, c7 = st.columns(2)
            with st.container():
                c6.image(
                    images_1[int(index)],
                    caption=data["product_description"]["subtitle"],
                    use_column_width=True,
                )
                c7.image(
                    images_2[int(index)],
                    caption=data_2["product_description"]["subtitle"],
                    use_column_width=True,
                )
                c6.write(f"About: {data['product_description']['text']}")
                c7.write(f"About: {data_2['product_description']['text']}")

                st.header(f"{data['name']} information", divider="rainbow")
                product_metrics(data=data)
                product_details(data=data)

                st.header(f"{data_2['name']} information", divider="rainbow")
                product_metrics(data=data_2)
                product_details(data=data_2)

            ### REVIEWS ####
            with review_tab:
                reviews = return_product_info(model=data["model_number"])
                reviews_2 = return_product_info(model=data_2["model_number"])

                st.header("Review comparison", divider="rainbow")
                # visualise the metric data
                review_metrics(reviews)
                review_metrics(reviews_2)

                # create ratings and dist dataframes
                ratings_df_1 = create_ratings_df(
                    data=reviews, product_name=data["name"]
                )
                dist_df_1 = create_dist_df(data=reviews, product_name=data["name"])

                ratings_df_2 = create_ratings_df(
                    data=reviews_2, product_name=data_2["name"]
                )
                dist_df_2 = create_dist_df(data=reviews_2, product_name=data_2["name"])

                # concatenate the two dataframes
                ratings_df = pd.concat([ratings_df_1, ratings_df_2])
                dist_df = pd.concat([dist_df_1, dist_df_2])

                # create visualisations with the new data
                ratings_fig = px.bar(
                    ratings_df,
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

                dist_fig = px.bar(
                    dist_df,
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

                col_1, col_2 = st.columns(2)

                with col_1:
                    st.plotly_chart(ratings_fig, use_container_width=True)
                    with st.expander("Ratings insights"):
                        st.write(
                            "This is what people have rated this product for width etc."
                        )
                with col_2:
                    st.plotly_chart(dist_fig, use_container_width=True)
                    with st.expander("Distribution insights"):
                        st.write("This is how people have voted")

                ### AI REVIEW QUERY ###

                sort = st.selectbox(
                    "What type of reviews would you like to know about?",
                    (Config.REVIEWS),
                )

                question = st.text_input(
                    "What would you like to know about a product?", key="question"
                )
                URL = f"http://localhost:8000/api/v1/reviews/sports/customer_query/{question}/{sort}"

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
