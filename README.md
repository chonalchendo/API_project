## Sports Product Comparison App

## Why build this app?

Coming from a sporting background, I have always found purchasing sporting goods difficult. From running shoes to football boots it's always hard to know which product is best for you. That's why I created this app!

## App Features

This app allows users to review crucial product information including price, materials, and product dimensions so a customer can get the best
product tailored to their needs!

The app also displays visualisations of customer reviews including how 
customers have rated a shoe's comfort and sizing as well as what the customers have bought the product for such as long-distance running or for the gym.

Finally, customers can dig even deeper into a product through our
custom chatbot which uses the latest GPT-4 from OpenAI!


## App technologies

The app has exclusively been built with Python, taking advantage of the rich ecosystem the language offers. 

- **MongoDB**: NoSql database used to store product information
- **FastAPI**: asynchronous backend framework used to connect the Streamlit frontend with MongoDB
- **Streamlit**: used as frontend because of its built-in features making it a good option for rapid prototyping
- **Langchain**: used as the framework for the OpenAI large language model (LLM) used for the chatbot, dealing with prompt templating, text splitting, embeddings, vectorstores and the Q&A retrival chain to return the LLM response to a user's question.
- **Plotly**: For frontend data visualisations
- **Pandas**: For manipulating data retrieved from MongoDB
- **Httpx**: used for making calls to product API
- **Pydantic**: used to validate ingested from external sources
- **Rich**: colourful debugging package used in conjunction with the logger library

## Page examples
The app is currently not available for use but here are some screenshots below demonstrate some of its capabilities.

### Home 
![EFE3A5D4-E5A6-428C-94BE-D83F14739378_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/49bf24b3-1f23-4c20-8576-3fbc485e5366)


### Products

![2ACD0A5D-1CD7-4D49-BF10-F4ADF1A9F8EC_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/e3ac01ed-cbcd-4f56-b276-d2705318acf6)

![0ADD8B64-ACFA-4793-AB5B-D3448B226CD5_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/3f31bb4f-75e5-43a3-a59b-220e14c216f0)

![18A948C4-BA11-4844-A569-F027EAD351D0_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/47a99492-2354-40a7-b351-087370757b51)

## Reviews
![4801D498-7D4D-454C-8E1D-02C5FC61618B_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/da1a7afc-fd8a-4d30-b46b-a84b4f585164)
![398D6A21-3198-47B6-B2D2-1BCC4E46B6C4_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/f16ee6f0-25de-4ecd-94c0-a76ced7c3a92)
![CC893999-3EE7-4FF6-8BA9-D86AD22E869C_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/bd5b773a-4955-4d7f-be2c-a080ba9efeb7)
![458C7159-6AFF-408A-8EA4-3CBE27E66427_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/bdf6df39-ee18-4e3f-85dc-98ee25bf57b3)

## Chatbot
![A434C1B3-1889-40E0-BDE2-BA8F4C0C6147_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/274a85b2-76a5-43a5-9ec6-c2b8b5c776ae)
![EA37F9D0-DF00-4216-B3F9-40C23BC0F911_1_201_a](https://github.com/chonalchendo/API_project/assets/110059232/5d45ef3e-c81f-499e-adfe-3b1ffea575c5)


## Usage

I am in the process of setting up a beta version of the app so that users
will be able to use it. This will likely be hosted through Streamlit's cloud services which the MongoDB database hosted through Mongo Atlas.

