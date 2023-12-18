from io import BytesIO

import httpx
import pandas as pd
from PIL import Image


def open_image(image_url: str) -> Image.open:
    """Open an image from a URL.

    Args:
        image_url (str): image URL

    Returns:
        Image.open: Image object
    """
    get_image = httpx.get(image_url)
    image = Image.open(BytesIO(get_image.content))
    return image


def get_product_images(data: dict) -> list[str]:
    """Get product images from api response

    Args:
        data (dict): api response

    Returns:
        list[str]: list of image URLs
    """
    view_list = data["view_list"]
    images = [
        image["image_url"]
        for image in view_list
        if "standard" in image["type"] or "detail" in image["type"]
    ]
    return images


def prod_info_dataframe(data: list[dict[str, str]], feature: str) -> pd.DataFrame:
    """Create a dataframe from a product api response

    Args:
        data (list[dict[str, str]]): api response
        feature (str): product feature to extract

    Returns:
        pd.DataFrame: dataframe of product info
    """
    if "wash" not in feature:
        prod_info = [{**product[feature], "name": product["name"]} for product in data]
    else:
        prod_info = [
            {**product["product_description"][feature], "name": product["name"]}
            for product in data
        ]

    return pd.DataFrame(prod_info)


def validate_columns(data: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Separate dataframe into separate dataframes by data type

    Args:
        data (pd.DataFrame): initial dataframe

    Returns:
        tuple[pd.DataFrame]: boolean, integer, string, and list dataframes
    """
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
    """Separate dataframe into separate dataframes by data type and transpose

    Args:
        data (pd.DataFrame): initial dataframe

    Returns:
        pd.DataFrame: transposed dataframes
    """
    val_dfs = validate_columns(data)
    list_df, bool_df, string_df, int_df = tuple(
        [df.set_index("name").T.reset_index() for df in val_dfs]
    )
    return list_df, bool_df, string_df, int_df
