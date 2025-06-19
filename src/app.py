#streamlit entrypoint

import streamlit as st
from ingestion import fetch_posts
from analysis import analyze_sentiments

def main():
    st.title("Reddit Sentiment Analyzer")
    sub = st.text_input("Subreddit", "technology")
    if st.button("Analyze"):
        posts = fetch_posts(sub)
        sentiments = analyze_sentiments(posts)
        st.write(sentiments)  # replace with charts/tables

if __name__ == "__main__":
    main()
