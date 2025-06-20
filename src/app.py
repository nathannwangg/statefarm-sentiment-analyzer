import streamlit as st
from analysis import analyze_sentiments, plot_sentiment_distribution, sentiment_summary, get_top_sentiment_posts, plot_emotion_bar, plot_wordcloud
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import re
from collections import Counter
import requests

st.set_page_config(
    page_title="SF-SENTI",
    page_icon="💬",
    layout="wide",
)


def display_single_post(post, col):
    sentiment_score = post.get("sentiment", post.get("score", 0))
    scaled_score = int((sentiment_score + 1) * 50)
    score_color = "#4CAF50" if scaled_score >= 50 else "#FF5252"
    post_id = post.get("id", "No ID")
    title = post.get("title", "No Title")
    body = post.get("body", "No Content Available")
    text_summary = post.get("text_summary", "No Summary Available")
    comment_summary = post.get("comment_summary", "No Comment Summary Available")
    if text_summary == "No Summary Available":
        summary_requests = requests.get(f"http://api:8000//summarize/{post_id}").json()
        text_summary = summary_requests.get("text_summary")
        comment_summary = summary_requests.get("comment_summary")
    
    with col.container():
        st.markdown(f"""
        <div style='position: relative; padding: 15px; border-radius: 10px; background-color: #F5F5F5; margin-bottom: 15px;'>
            <div style='position: absolute; top: 10px; right: 10px; width: 60px; height: 60px; border-radius: 50%; background-color: {score_color}; display: flex; justify-content: center; align-items: center; color: white; font-size: 18px; font-weight: bold;'>{scaled_score}</div>
            <h4 style='color: #333333; margin-bottom: 10px;'>{title}</h4>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💬 Open Summary"):
            st.markdown(f"**📝 Post Summary:** {text_summary}")
            st.markdown(f"**💡 Comment Summary:** {comment_summary}")

# Main UI
def main():
    st.markdown(
        """
        <div style="text-align: center; background-color: #FF6961; padding: 20px; border-radius: 10px;">
            <h1 style="font-size: 60px; color: white;">SF-SENTI</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Home", "Dashboard"])

    # Analyze sentiment
    positive_posts = requests.get("http://api:8000/top-positive").json()
    negative_posts = requests.get("http://api:8000/top-negative").json()
    
    summary = requests.get("http://api:8000/sentiment-summary").json()

    with tab1:
        st.markdown("<h3 style='text-align: center; color: #FF6961;'>Top 5 Posts</h3>", unsafe_allow_html=True)
        col_pos, col_neg = st.columns(2)

        with col_pos:
            st.markdown("<h4 style='text-align: center; color: #4CAF50;'>Positive Posts</h4>", unsafe_allow_html=True)
            for post in positive_posts:
                display_single_post(post, col_pos)

        with col_neg:
            st.markdown("<h4 style='text-align: center; color: #FF5252;'>Negative Posts</h4>", unsafe_allow_html=True)
            for post in negative_posts:
                display_single_post(post, col_neg)
    
    with tab2:
        compound_pct = (summary.get("average_sentiment",0) + 1) / 2 * 100
        total_posts = summary.get("total_count",0)
        positive_pct = summary.get("positive_count", 0)
        neutral_pct = summary.get("neutral_count",0)
        negative_pct = summary.get("negative_count",0)

        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [positive_pct, neutral_pct, negative_pct]
        colors = ['#2ecc71', '#95a5a6', '#e74c3c']

        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.markdown("""
                <div style='
                    padding: 25px;
                    border-radius: 12px;
                    background: #fff7f7;
                    border: 1px solid #ffe0e0;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                    font-size: 17px;
                    line-height: 1.8;
                '>
                <h4>Summary</h4>
                <b>Total Posts:</b> {total}<br>
                <b>Positive:</b> {pos}%<br>
                <b>Neutral:</b> {neu}%<br>
                <b>Negative:</b> {neg}%<br>
                <b>Avg Sentiment:</b> {avg:.1f}%
                </div>
            """.format(
                total=total_posts,
                pos=positive_pct,
                neu=neutral_pct,
                neg=negative_pct,
                avg=compound_pct
            ), unsafe_allow_html=True)
            
            with col_right:
                st.markdown("<h4>📈 Sentiment Distribution</h4>", unsafe_allow_html=True)
                fig1, ax1 = plt.subplots()
                wedges, texts, autotexts = ax1.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
                )
                centre_circle = plt.Circle((0, 0), 0.70, fc='white')
                fig1.gca().add_artist(centre_circle)
                ax1.axis('equal')
                st.pyplot(fig1)


if __name__ == "__main__":
    main()
