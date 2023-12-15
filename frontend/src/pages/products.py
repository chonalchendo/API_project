import streamlit as st
from src.helpers.product_helpers import (
    create_image_grid,
    details_comp,
    get_product_images,
    price_comp,
    prod_info_dataframe,
    transpose_dataframes,
)


def product_page(data_1: dict, data_2: dict) -> None:
    """
    Function that creates the product page.

    args:
        product_1 (str): First product to compare
        product_2 (str): Second product to compare

    return: None
    """
    # display product info
    st.title(f"{data_1['name']} Vs {data_2['name']}")

    images_1 = get_product_images(data_1)
    images_2 = get_product_images(data_2)

    col_1, col_2 = st.columns(2)

    with col_1:
        create_image_grid(n=3, images=images_1)
        st.write(f"{data_1['product_description']['text']}")
        st.write(
            f"Go to the product website here: [{data_1['name']}](%s)"
            % data_1["meta_data"]["canonical"]
        )

    with col_2:
        create_image_grid(n=3, images=images_2)
        st.write(f"{data_2['product_description']['text']}")
        st.write(
            f"Go to the product website here: [{data_2['name']}](%s)"
            % data_2["meta_data"]["canonical"]
        )

    st.divider()

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Price")
            price_comp(data_1=data_1, data_2=data_2)

        with c2:
            st.subheader("Product Details")
            details_comp(data_1=data_1, data_2=data_2)

    features = [
        "meta_data",
        "attribute_list",
        "pricing_information",
        "product_description",
        "wash_care_instructions",
    ]

    meta_table, attrs_table, pricing_table, desc_table, wash_table = [
        prod_info_dataframe(data=[data_1, data_2], feature=feature)
        for feature in features
    ]

    attrs_list, attrs_bool, attrs_string, attrs_int = transpose_dataframes(attrs_table)
    price_list, price_bool, price_string, price_int = transpose_dataframes(
        pricing_table
    )

    meta_list, meta_bool, meta_string, meta_int = transpose_dataframes(meta_table)

    desc_list, desc_bool, desc_string, desc_int = transpose_dataframes(desc_table)

    with st.expander("Product Website Information"):
        st.dataframe(meta_string, hide_index=True, use_container_width=True)

    with st.expander("Product Descriptions"):
        st.dataframe(desc_string, hide_index=True, use_container_width=True)
        st.dataframe(desc_list, hide_index=True, use_container_width=True)

    with st.expander("Product Pricing Comparison"):
        st.dataframe(price_int, hide_index=True, use_container_width=True)

    with st.expander("Product Attribute Comparison"):
        st.dataframe(attrs_list, hide_index=True, use_container_width=True)
        st.dataframe(attrs_bool, hide_index=True, use_container_width=True)
        st.dataframe(attrs_string, hide_index=True, use_container_width=True)

    with st.expander("Product Washing Instructions"):
        st.dataframe(wash_table, hide_index=True, use_container_width=True)
