import streamlit as st

from settings import settings
from src.helpers.api_helpers import get_all_products, product_api_query

# Create the app
st.set_page_config(
    page_title="Blue Ribbon II - the sports product comparison app",
    page_icon=settings.PAGE_ICON,
    layout=settings.LAYOUT,
    menu_items={
        "Get help": "https://github.com/chonalchendo/API_project",
        "About": "# An app designed to help athletes decide what product is best for them.",
    },
)

st.title("Blue Ribbon II")

st.markdown(settings.MARKDOWN)


st.write("What products would you like to compare?")

products = get_all_products()
product_names = [product["name"] for product in products]

product_1 = st.selectbox("Product 1", product_names, index=None)
product_2 = st.selectbox("Product 2", product_names, index=None)


# Return data on both products
if product_1 and product_2:
    for product in products:
        if product_1 == product["name"]:
            prod_1 = product["product_id"]
        if product_2 == product["name"]:
            prod_2 = product["product_id"]

    data_1 = product_api_query(product=prod_1)
    data_2 = product_api_query(product=prod_2)
