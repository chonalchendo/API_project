from io import BytesIO

import httpx
import pandas as pd
import streamlit as st
from PIL import Image


def product_details(data: dict) -> st.markdown:
    details = data["product_description"]["usps"]
    s = " "
    for i in details:
        s += "- " + i + "\n"
    return st.markdown(s)


def details_comp(data_1: dict, data_2: dict) -> None:
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(data_1["name"])
        product_details(data=data_1)
    with col_2:
        st.write(data_2["name"])
        product_details(data=data_2)


def product_metrics(data: dict) -> None:
    pricing = data["pricing_information"]
    attrs = data["attribute_list"]
    c1, c2, c3 = st.columns(3)
    with st.container():
        c1.metric("Current price", f"£{pricing['currentPrice']}")
        c2.metric("Standard price", f"£{pricing['standard_price']}")
        with c3:
            product_details(data)


def calculate_price_diff(data_1: dict, data_2: dict, price: str) -> tuple[int, int]:
    pricing_1 = data_1["pricing_information"]
    pricing_2 = data_2["pricing_information"]

    price_1_diff = pricing_1[price] - pricing_2[price]
    price_2_diff = pricing_2[price] - pricing_1[price]

    return price_1_diff, price_2_diff


def price_comp(data_1: dict, data_2: dict) -> None:
    pricing_1 = data_1["pricing_information"]
    pricing_2 = data_2["pricing_information"]

    price_1_diff_cp, price_2_diff_cp = calculate_price_diff(
        data_1, data_2, "currentPrice"
    )
    price_1_diff_sp, price_2_diff_sp = calculate_price_diff(
        data_1, data_2, "standard_price"
    )

    c1, c2 = st.columns(2)
    with st.container():
        c1.metric(
            f"{data_1['name']} Current Price",
            f"£{pricing_1['currentPrice']}",
            f"£{price_1_diff_cp}",
        )
        c2.metric(
            f"{data_2['name']} Current Price",
            f"£{pricing_2['currentPrice']}",
            f"£{price_2_diff_cp}",
        )
        c1.metric(
            f"{data_1['name']} Standard Price",
            f"£{pricing_1['standard_price']}",
            f"£{price_1_diff_sp}",
        )
        c2.metric(
            f"{data_2['name']} Standard Price",
            f"£{pricing_2['standard_price']}",
            f"£{price_2_diff_sp}",
        )


def get_product_images(data: dict) -> list[str]:
    view_list = data["view_list"]
    images = [
        image["image_url"]
        for image in view_list
        if "standard" in image["type"] or "detail" in image["type"]
    ]
    return images


def create_image_grid(n: int, images: list[str]) -> None:
    groups = [images[i : i + n] for i in range(0, len(images), n)]
    for group in groups:
        image_cols = st.columns(n)
        for i, image in enumerate(group):
            image_cols[i].image(image, use_column_width=True)


def open_image(image_url: str) -> Image.open:
    get_image = httpx.get(image_url)
    image = Image.open(BytesIO(get_image.content))
    return image


def prod_info_dataframe(data: list[dict], feature: str) -> pd.DataFrame:
    if "wash" not in feature:
        prod_info = [{**product[feature], "name": product["name"]} for product in data]
    else:
        prod_info = [
            {**product["product_description"][feature], "name": product["name"]}
            for product in data
        ]

    return pd.DataFrame(prod_info)


def validate_columns(data: pd.DataFrame) -> pd.DataFrame:
    list_cols = ["name"]
    bool_cols = ["name"]
    string_cols = []
    int_cols = ["name"]
    for col in data.columns.tolist():
        is_list = data[col].apply(lambda x: isinstance(x, list))
        if any(is_list):
            list_cols.append(col)
        if data[col].dtype == "bool":
            bool_cols.append(col)
        if data[col].dtype == "O" and not any(is_list):
            string_cols.append(col)
        if data[col].dtype == "int" or data[col].dtype == "float":
            int_cols.append(col)

    list_df = pd.DataFrame(data[list_cols])
    bool_df = pd.DataFrame(data[bool_cols])
    string_df = pd.DataFrame(data[string_cols])
    int_df = pd.DataFrame(data[int_cols])

    return list_df, bool_df, string_df, int_df


def transpose_dataframes(data: pd.DataFrame) -> pd.DataFrame:
    val_dfs = validate_columns(data)
    list_df, bool_df, string_df, int_df = tuple(
        [df.set_index("name").T.reset_index() for df in val_dfs]
    )
    return list_df, bool_df, string_df, int_df
