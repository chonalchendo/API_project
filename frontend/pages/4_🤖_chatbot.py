import streamlit as st
from src.helpers.api_helpers import (
    get_all_products,
    handle_llm_response,
    product_api_query,
)

st.title("Ask our chatbot for more detailed product information!")

products = get_all_products()
product_names = [product["name"] for product in products]


col1, col2 = st.columns(2)

with col1:
    product_1 = st.selectbox("Product 1", product_names, index=None)
    if not product_1:
        st.info("Please select a product.", icon="ℹ️")
    else:
        st.success(f"You have selected product {product_1}!", icon="✅")

with col2:
    product_2 = st.selectbox("Product 2", product_names, index=None)
    if not product_2:
        st.info("Please select a product.", icon="ℹ️")
    else:
        st.success(f"You have selected product {product_2}!", icon="✅")

# Return data on both products
if product_1 and product_2:
    for product in products:
        if product_1 == product["name"]:
            prod_1 = product["product_id"]
        if product_2 == product["name"]:
            prod_2 = product["product_id"]

    data_1 = product_api_query(product=prod_1)
    data_2 = product_api_query(product=prod_2)

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

    st.title("💬 Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": f"What would you like to know about {data_1['name']}",
            }
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        #     if not openai_api_key:
        #         st.info("Please add your OpenAI API key to continue.")
        #         st.stop()

        # openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        msg = handle_llm_response(
            model=data_1["model_number"], question=st.session_state.messages
        )
        # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        # msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg)
