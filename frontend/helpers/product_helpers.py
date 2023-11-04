from io import BytesIO

import httpx
import pandas as pd
import streamlit as st
from PIL import Image


def product_metrics(data: dict) -> None:
    pricing = data["pricing_information"]
    attrs = data["attribute_list"]
    c1, c2, c3, c4 = st.columns(4)
    with st.container():
        c1.metric("Current price", f"£{pricing['currentPrice']}")
        c2.metric("Standard price", f"£{pricing['standard_price']}")
        c3.metric("Weight", f"{attrs['weight']}")
        c4.metric("Closure", f"{attrs['closure']}")
    with st.container():
        c1.metric("Surface", f"{attrs['surface']}")
        c2.metric("Product fit", f"{attrs['productfit']}")
        c3.metric("Toe height", f"{attrs['toe_stack_height']}")
        c4.metric("Heel height", f"{attrs['heel_stack_height']}")


def product_details(data: dict) -> st.markdown:
    details = data["product_description"]["usps"]
    s = " "
    for i in details:
        s += "- " + i + "\n"
    return st.markdown(s)


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

    # return df.set_index("name").T.reset_index()


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
