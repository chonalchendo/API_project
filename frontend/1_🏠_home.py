import streamlit as st

from settings import settings

# Create the app
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    menu_items={
        "Get help": "https://github.com/chonalchendo/API_project",
        "About": "# An app designed to help athletes decide what product is best for them.",
    },
)

st.title("Blue Ribbon II 🎗️🏃- Elevating your Sports Gear Experience")


about = """
### About
Welcome to Blue Ribbon II, an innovative sports comparison app designed to 
empower users with comprehensive insights into sports products, allowing them 
to effortlessly contrast and compare offerings from various manufacturers. 
The name "Blue Ribbon II" pays homage to Phil Knight's original company which
disrupted the sports industry with its innovative products and marketing.

### Unleash the Power of Informed Choices
Blue Ribbon II is your go-to destination for diving deep into the world of 
sports products. Whether you're a seasoned athlete or a casual fitness enthusiast, 
our app equips you with the knowledge needed to make informed decisions about 
your gear. We believe that your sports equipment should be as exceptional as 
your performance, and Blue Ribbon II is here to make that happen.

### Adidas Running Shoes: Just the Beginning
Currently, Blue Ribbon II focuses on Adidas running shoes, offering a curated 
selection that embodies the perfect fusion of style, technology, and performance. 
We are working hard to expand our product offering to include more sportswear brands.

### What we offer
- High level comparison of general product information including a price comparison 
and detailed product specifications
- In-depth review analysis including stats on how customers rate products based on 
comfort, width, size and quality. As well as, how popular a product is, and how 
customers intend to use their purchased product.
- We use the latest **Large Languaga Model (LLM) technology from OpenAI** to
allow users to ask more in depth questions about each product so they can really 
understand if this product is right for them.
\n**👈 Select a page from the sidebar**
"""

st.markdown(settings.MARKDOWN)

st.markdown(about)
