import time

import streamlit as st

from settings import settings
from src.helpers.api_helpers import product_api_query
from src.pages.chatbot import chatbot_page
from src.pages.products import product_page
from src.pages.reviews import reviews_page


def main() -> None:
    # Create the app
    st.set_page_config(
        page_title=settings.TITLE,
        page_icon=settings.PAGE_ICON,
        layout=settings.LAYOUT,
    )

    st.markdown(settings.MARKDOWN)

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
        data = product_api_query(product=product)
        time.sleep(5)
        data_2 = product_api_query(product=product_2)

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
