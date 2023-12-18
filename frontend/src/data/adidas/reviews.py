from typing import Any

import pandas as pd
import pycountry
from src.helpers.api_helpers import review_stats_query


def create_review_questions_df(api: Any) -> pd.DataFrame:
    """Create a dataframe of review questions.

    Args:
        api (Any): api response containing product review data

    Returns:
        pd.DataFrame: pandas dataframe of review questions
    """
    data = api["insightsFilters"]
    # Flatten the data
    flat_data = []
    for entry in data:
        for value in entry["values"]:
            flat_data.append(
                {
                    "modelId": api["modelId"],
                    "label": entry["label"],
                    "reviewCount": value["reviewCount"],
                    "answerLabel": value["answerLabel"],
                }
            )
    return pd.DataFrame(flat_data)


def get_country_names(data: list[str]) -> list[str]:
    """Get country names from country codes.

    Args:
        data (list[str]): list of country codes

    Returns:
        list[str]: list of country names
    """
    alpha_2 = [country.split("_")[1] for country in data]
    return [pycountry.countries.get(alpha_2=code).name for code in alpha_2]


def create_review_location_df(api: list[dict[str, Any]]) -> pd.DataFrame:
    """Create a dataframe of customer review locations.

    Args:
        api (list[dict[str, Any]]): api response containing product review data

    Returns:
        pd.DataFrame: pandas data of review locations
    """
    loc_codes = [loc["locale"] for loc in api]
    model_ids = [model["modelId"] for model in api]
    loc_names = get_country_names(loc_codes)

    data = {"modelId": model_ids, "locations": loc_names}
    return pd.DataFrame(data)


def create_review_timeseries_df(api: list[dict[str, Any]]) -> pd.DataFrame:
    """Create a dataframe of review timeseries data.

    Args:
        api (list[dict[str, Any]]): api response containing product review data

    Returns:
        pd.DataFrame: pandas dataframe of review timeseries data
    """
    data = [
        {"submissionTime": key["submissionTime"], "modelId": key["modelId"]}
        for key in api
    ]
    return pd.DataFrame(data)


def create_ratings_df(data: dict, product_name: str) -> pd.DataFrame:
    """Create a dataframe of detailed ratings data.

    Args:
        data (dict): api response containing product review data
        product_name (str): product name

    Returns:
        pd.DataFrame: pandas dataframe of detailed ratings data
    """
    # plot detailed ratings
    ratings = [round(rating["averageRating"], 2) for rating in data["secondaryRatings"]]
    names = [rating["name"] for rating in data["secondaryRatings"]]
    return pd.DataFrame({"product": product_name, "type": names, "rating": ratings})


def create_dist_df(data: dict, product_name: str) -> pd.DataFrame:
    """Create a dataframe of rating distribution data.

    Args:
        data (dict): api response containing product review data
        product_name (str): product name

    Returns:
        pd.DataFrame: pandas dataframe of rating distribution data
    """
    # plot rating distribution
    rating_counts = [rating["count"] for rating in data["ratingDistribution"]]
    rating_values = [rating["rating"] for rating in data["ratingDistribution"]]
    return pd.DataFrame(
        {"product": product_name, "value": rating_values, "count": rating_counts}
    )


def flatten_review_stats(model: str, product_name: str) -> pd.DataFrame:
    """Flatten review stats data.

    Args:
        model (str): model id
        product_name (str): product name

    Returns:
        pd.DataFrame: pandas dataframe of review stats
    """
    data = review_stats_query(model=model)
    extracted_data = {
        "Product": product_name,
        # "Model ID": data["modelId"],
        "Overall Rating": data["overallRating"],
        "Review Count": data["reviewCount"],
        "Recommended": data["recommendationPercentage"],
    }

    for rating in data["secondaryRatings"]:
        extracted_data[rating["name"]] = round(rating["averageRating"], 2)

    for rating in data["ratingDistribution"]:
        extracted_data[f"{rating['rating']} Star Rating"] = rating["count"]

    return pd.DataFrame([extracted_data])


def display_review_stats(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Combine review stats for two products into one dataframe.

    Args:
        df1 (pd.DataFrame): review stats dataframe
        df2 (pd.DataFrame): review stats dataframe

    Returns:
        pd.DataFrame: pandas dataframe of review stats
    """
    df = (
        pd.concat([df1, df2])
        .set_index("Product")
        .T.reset_index()
        .rename(columns={"index": "Product"})
        .set_index("Product")
    )
    df.columns.name = None
    return df


def format_review_info(
    df1: list[dict[str, Any]], df2: list[dict[str, Any]]
) -> pd.DataFrame:
    """
    Function to take review data from two products and merge both into a dataframe

    args:
        df1: list[dict[str, Any]] - product review data
        df2: list[dict[str, Any]] - product review data
    returns: pd.DataFrame - pandas dataframe
    """
    data = [*df1, *df2]
    return pd.DataFrame(data)
