import time

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers.api_helpers import (
    handle_llm_response,
    return_model_info,
    return_product_info,
)
from helpers.product_helpers import (
    create_image_grid,
    get_product_images,
    product_details,
    product_metrics,
)
from helpers.review_helpers import create_dist_df, create_ratings_df, review_metrics

# User is prompted to ask a question about product reviews
# Spinner to indicate the question is being processed
# The response is returned in a text box
# A link to the product and a photo of the product is displayed with the AI response

# need to create a post request to take in the users query from streamlit
# question is then posted into one of the functions detailed in the reviews_utils file
# return the response of the post request via st.text


class Config:
    REVIEWS = ("helpful", "relevant", "newest")


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

    product_tab, review_tab, llm_tab = st.tabs(
        ["Product Info", "Review Info", "Review Chat"]
    )
    if product and product_2:
        with product_tab:
            data = return_product_info(product=product)
            time.sleep(5)
            data_2 = return_product_info(product=product_2)

            # display product info
            st.title(f"{data['name']} Vs {data_2['name']}")

            images_1 = get_product_images(data)
            images_2 = get_product_images(data_2)

            col_1, col_2 = st.columns(2)

            with col_1:
                create_image_grid(n=3, images=images_1)
                st.write(f"{data['product_description']['text']}")
                st.write(
                    f"Go to the product website here: [{data['name']}](%s)"
                    % data["meta_data"]["canonical"]
                )

            with col_2:
                create_image_grid(n=3, images=images_2)
                st.write(f"{data_2['product_description']['text']}")
                st.write(
                    f"Go to the product website here: [{data_2['name']}](%s)"
                    % data_2["meta_data"]["canonical"]
                )

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
                ratings_fig.update_traces(
                    textposition="outside", texttemplate="%{text}"
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
                dist_fig.update_traces(textposition="outside", texttemplate="%{text}")

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
            with llm_tab:
                # default LLM response
                default_sort = "helpful"
                default_question = "Can you succinctly summarise what customers said about this product? List what they liked and what they didn't like about the product"

                data_llm_1 = handle_llm_response(
                    sort=default_sort,
                    question=default_question,
                    model_id=data["model_number"],
                )
                # time.sleep(70)
                data_llm_2 = handle_llm_response(
                    sort=default_sort,
                    question=default_question,
                    model_id=data_2["model_number"],
                )

                column_1, column_2 = st.columns(2)
                with column_1:
                    with st.expander(f"What customers said about {data['name']}"):
                        st.write(data_llm_1)
                with column_2:
                    with st.expander(f"What customers said about {data_2['name']}"):
                        st.write(data_llm_2)
                        st.empty()

                st.header("Have any questions? Ask below!!")

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
