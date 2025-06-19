import streamlit as st
from ingestion import fetch_posts
from analysis import analyze_sentiments, plot_sentiment_distribution, sentiment_summary
import pandas as pd

st.set_page_config(
    page_title="Reddit Sentiment Analyzer",
    page_icon="💬",
    layout="wide",
)

def main():
    st.markdown("<h1 style='text-align: center;'>💬 Reddit Sentiment Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("---")

    sub = st.text_input("Subreddit", "technology")
    if st.button("Analyze"):
        # posts = fetch_posts(sub)
        example_posts = [
            {"title": "I love the new update!", "body": "It's amazing and super smooth."},
            {"title": "Why is it so buggy?", "body": "The app crashes all the time now."},
            {"title": "It’s okay I guess", "body": "Nothing special, but not bad either."}
        ]

        analyzed = analyze_sentiments(example_posts)
        summary = sentiment_summary(analyzed)
        compound_pct = (summary["Average Compound"] + 1) / 2 * 100

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📊 Summary")
            st.markdown(
                f"""
                <div style='padding: 15px; border-radius: 10px; background-color: #FDEDEC; font-size: 16px; line-height: 1.8'>
                <b>Total Posts:</b> {summary['Count']}<br>
                <b>Positive:</b> {summary['Positive (%)']}%<br>
                <b>Neutral:</b> {summary['Neutral (%)']}%<br>
                <b>Negative:</b> {summary['Negative (%)']}%<br>
                <b>Avg Sentiment:</b> {compound_pct:.1f}%
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.subheader("Sentiment Distribution")
            plot_sentiment_distribution(analyzed)

if __name__ == "__main__":
    main()
