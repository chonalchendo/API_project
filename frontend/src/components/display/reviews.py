import streamlit as st


def review_metrics(data: dict) -> None:
    c1, c2, c3 = st.columns(3)
    with st.container():
        c1.metric("Overall Rating", f"{data['overallRating']}")
        c2.metric("Review Count", f"{data['reviewCount']}")
        c3.metric("Recommendation Percentage", f"{data['recommendationPercentage']}%")
