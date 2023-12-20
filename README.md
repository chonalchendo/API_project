## Sports Product Comparison App

## Why build this app?

Coming from a sporting background I have always found it difficult when purchasing sporting goods. From running shoes to football boots it's always hard to know which product is best for you. That's why I created this app!

## App Features

This app allows users to review crucial product information including price, materials, and product dimensions so a customer can get the best
product tailored to their needs!

The app also displays visualisations on customer reviews including how 
customers have rated a shoes comfort and sizing as well as what the customers have bought the product for such as long distance running or for the gym.

Finally, customers are able to dig even deeper about a product through our
custom chatbot which uses the latest GPT-4 from OpenAI!


# App technologies

The app has exclusively been built with Python, taking advantage of the rich ecosystem the language has to offer. 

- MongoDB: NoSql database used to store product information
- FastAPI: asynchronous backend framework used to connect the streamlit frontend with MongoDB
- Streamlit: used as frontend because of its built in features making it a good option for rapid prototyping
- Langchain: used as the framework for the OpenAI large language model (LLM) used for the chatbot. Dealt with prompt templating, text splitting, embeddings, vectorstores and the Q&A retrival chain to return the LLM response to a user's question.
- Plotly: For frontend data visualisations
- Pandas: For manipulating data retrieved from MongoDB
- Httpx: used for making calls to product API
- Pydantic: used to validate ingested from external sources
- Rich: colorful debugging package used in conjunction with the logger library


# Home Page



# Useage

I am in the process of setting up a beta version of the app so that users
will be able to use it. This will likely be hosted through Streamlit's cloud services which the MongoDB database hosted through Mongo Atlas.




Personal project that aims to aggregate sports product information from numerous sporting manufacturers to produce novel product insights for app users