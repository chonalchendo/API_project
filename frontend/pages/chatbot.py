import httpx
import streamlit as st
from helpers.api_helpers import handle_llm_response

# User is prompted to ask a question about product reviews
# Spinner to indicate the question is being processed
# The response is returned in a text box
# A link to the product and a photo of the product is displayed with the AI response

# need to create a post request to take in the users query from streamlit
# question is then posted into one of the functions detailed in the reviews_utils file
# return the response of the post request via st.text


class Config:
    REVIEWS = ("helpful", "relevant", "newest")


def chatbot_page(data_1: dict, data_2: dict) -> None:
    """
    Function to create the LLM/Chatbot page.

    args:
        data_1 (dict): Data dictionary of the first product
        data_2 (dict): Data dictionary of the second product

    return (None): Streamlit tab
    """
    # default LLM response
    default_question = "Can you succinctly summarise what customers said about this product? List what they liked and what they didn't like about the product"

    data_llm_1 = handle_llm_response(
        question=default_question,
        model=data_1["model_number"],
    )
    # time.sleep(70)
    data_llm_2 = handle_llm_response(
        question=default_question,
        model=data_2["model_number"],
    )

    column_1, column_2 = st.columns(2)
    with column_1:
        with st.expander(f"What customers said about {data_1['name']}"):
            st.write(data_llm_1)
    with column_2:
        with st.expander(f"What customers said about {data_2['name']}"):
            st.write(data_llm_2)
            st.empty()

    st.header("Have any questions? Ask below!!")

    sort = st.selectbox(
        "What type of reviews would you like to know about?",
        (Config.REVIEWS),
    )

    question = st.text_input(
        "What would you like to know about a product?", key="question"
    )
    URL = (
        f"http://localhost:8000/api/v1/reviews/sports/customer_query/{question}/{sort}"
    )

    if st.button("Submit"):
        with st.spinner("Processing AI response..."):
            response = httpx.post(URL, timeout=100)
            if response.status_code == 200:
                data = response.json()
                st.write(data["response"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
