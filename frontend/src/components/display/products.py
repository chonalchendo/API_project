import streamlit as st


def product_details(data: dict) -> st.markdown:
    """Display product details in a streamlit markdown widget

    Args:
        data (dict): product api response

    Returns:
        st.markdown: markdown widget
    """
    details = data["product_description"]["usps"]
    s = " "
    for i in details:
        s += "- " + i + "\n"
    return st.markdown(s)


def details_comp(data_1: dict, data_2: dict) -> None:
    """Display product details side by side

    Args:
        data_1 (dict): data for first product
        data_2 (dict): data for second product
    """
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write(data_1["name"])
        product_details(data=data_1)
    with col_2:
        st.write(data_2["name"])
        product_details(data=data_2)


def product_metrics(data: dict) -> None:
    """Display product metrics in a streamlit metric widget

    Args:
        data (dict): product api response
    """
    pricing = data["pricing_information"]
    c1, c2, c3 = st.columns(3)
    with st.container():
        c1.metric("Current price", f"£{pricing['currentPrice']}")
        c2.metric("Standard price", f"£{pricing['standard_price']}")
        with c3:
            product_details(data)


def calculate_price_diff(data_1: dict, data_2: dict, price: str) -> tuple[int, int]:
    """Calculate the difference in price between two products

    Args:
        data_1 (dict): api response for first product
        data_2 (dict): api response for second product
        price (str): price variable to compare

    Returns:
        tuple[int, int]: difference in price between products
    """
    pricing_1 = data_1["pricing_information"]
    pricing_2 = data_2["pricing_information"]

    price_1_diff = pricing_1[price] - pricing_2[price]
    price_2_diff = pricing_2[price] - pricing_1[price]

    return price_1_diff, price_2_diff


def price_comp(data_1: dict, data_2: dict) -> None:
    """Display product prices side by side

    Args:
        data_1 (dict): api response for first product
        data_2 (dict): api response for second product
    """
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


def create_image_grid(n: int, images: list[str]) -> None:
    """Create a grid of images

    Args:
        n (int): number of columns
        images (list[str]): list of image URLs
    """
    groups = [images[i : i + n] for i in range(0, len(images), n)]
    for group in groups:
        image_cols = st.columns(n)
        for i, image in enumerate(group):
            image_cols[i].image(image, use_column_width=True)

