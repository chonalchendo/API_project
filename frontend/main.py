import time

import streamlit as st

from helpers.api_helpers import return_product_info
from pages.chatbot import chatbot_page
from pages.products import product_page
from pages.reviews import reviews_page


def main() -> None:
    # Create the app
    st.set_page_config(
        page_title="Blue Ribbon II - sports product comparison app",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.title("Blue Ribbon II - the sports comparison app")
    st.markdown("_Prototype v0.0.1_")

    ### SIDEBAR ###
    with st.sidebar:
        st.write("What products would you like to compare?")

        product = st.text_input("Product 1", key="product_1")
        st.write("Vs")
        product_2 = st.text_input("Product 2", key="product_2")

    # create the app tabs
    product_tab, review_tab, llm_tab = st.tabs(
        ["Product Info", "Review Info", "Review Chat"]
    )

    # Return data on both products
    if product and product_2:
        data = return_product_info(product=product)
        time.sleep(5)
        data_2 = return_product_info(product=product_2)

        ### PRODUCTS TAB ###
        with product_tab:
            product_page(data_1=data, data_2=data_2)

        ### REVIEWS TAB ####
        with review_tab:
            reviews_page(data_1=data, data_2=data_2)

        ### AI REVIEW TAB ###
        with llm_tab:
            chatbot_page(data_1=data, data_2=data_2)


if __name__ == "__main__":
    main()
