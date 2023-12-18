from typing import Any

import pandas as pd
import pycountry


def create_review_questions_df(api: Any) -> pd.DataFrame:
    data = api["insightsFilters"]
    # Flatten the data
    flat_data = []
    for entry in data:
        for value in entry["values"]:
            flat_data.append(
                {
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
    loc_names = get_country_names(loc_codes)
    return pd.DataFrame(loc_names, columns=["locations"]).value_counts().reset_index()


def create_review_timeseries_df(api: list[dict[str, Any]]):
    data = [
        {"submissionTime": key["submissionTime"], "modelId": key["modelId"]}
        for key in api
    ]
    return pd.DataFrame(data)
