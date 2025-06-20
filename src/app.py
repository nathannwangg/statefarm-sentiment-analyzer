import streamlit as st
from ingestion import fetch_posts
from analysis import analyze_sentiments, plot_sentiment_distribution, sentiment_summary, get_top_sentiment_posts, plot_emotion_bar, plot_wordcloud
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import re
from collections import Counter

st.set_page_config(
    page_title="Reddit Sentiment Analyzer",
    page_icon="💬",
    layout="wide",
)

# Dummy function to fetch posts
def fetch_posts(subreddit):
    return [
        {
            "title": f"Post {i} from {subreddit}",
            "body": f"This is a summary of post {i} from the subreddit {subreddit}.",
        }
        for i in range(1, 11)
    ]

def display_single_post(post, col):
    scaled_score = int((post["score"] + 1) * 50)  # Convert [-1,1] → [0,100]
    score_color = "#4CAF50" if scaled_score >= 50 else "#FF5252"

    with col.container():
        st.markdown(f"""
        <div style='position: relative; padding: 15px; border-radius: 10px; background-color: #F5F5F5; margin-bottom: 15px;'>
            <div style='position: absolute; top: 10px; right: 10px; width: 60px; height: 60px; border-radius: 50%; background-color: {score_color}; display: flex; justify-content: center; align-items: center; color: white; font-size: 18px; font-weight: bold;'>
                {scaled_score}
            </div>
            <h4 style='color: #333333; margin-bottom: 10px;'>{post['title']}</h4>
            <p style='color: #666666; font-size: 14px; margin-bottom: 10px;'>{post['body']}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💬 Open Comments"):
            st.markdown(f"**📝 Post Summary:** {post['body']}")
            st.markdown("**💡 Comment Summary:** Mixed, leaning positive.")

# Main UI
def main():
    st.markdown(
        """
        <div style="text-align: center; background-color: #FF6961; padding: 20px; border-radius: 10px;">
            <h1 style="font-size: 60px; color: white;">Reddit Sentiment Analyzer</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Home", "Dashboard"])

    # Replace with: posts = fetch_posts(sub) when connected
    example_posts = [
        {"title": "I love the new update!", "body": "It's amazing and super smooth.", "score": 85},
        {"title": "Why is it so buggy?", "body": "The app crashes all the time now.", "score": 20},
        {"title": "It’s okay I guess", "body": "Nothing special, but not bad either.", "score": 50}
    ]

    # Analyze sentiment
    analyzed = analyze_sentiments(example_posts)
    positive_posts, negative_posts = get_top_sentiment_posts(analyzed)

    with tab1:
        st.markdown("<h3 style='text-align: center; color: #FF6961;'>Top 5 Posts</h3>", unsafe_allow_html=True)

        posts = fetch_posts("dummy_subreddit")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='text-align: center; color: #4CAF50;'>Positive Posts</h4>", unsafe_allow_html=True)
            for post in positive_posts:
                display_single_post(post, col1)

        with col2:
            st.markdown("<h4 style='text-align: center; color: #FF5252;'>Negative Posts</h4>", unsafe_allow_html=True)
            for post in negative_posts:
                display_single_post(post, col2)

    with tab2: 
        summary = sentiment_summary(analyzed)
        compound_pct = (summary["Average Compound"] + 1) / 2 * 100

        total_posts = summary["Count"]
        positive_pct = summary["Positive (%)"]
        neutral_pct = summary["Neutral (%)"]
        negative_pct = summary["Negative (%)"]

        # Pie chart data
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [positive_pct, neutral_pct, negative_pct]
        colors = ['#2ecc71', '#95a5a6', '#e74c3c']

        # Layout: Summary + Word Chart (Left), Donut Chart (Right)
        col1, col2 = st.columns([1, 1])

        with col1:
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

            # Word frequency bar chart
            st.markdown("<h4 style='margin-top: 25px;'>📊 Top Words</h4>", unsafe_allow_html=True)
            all_text = " ".join([post["title"] + " " + post["body"] for post in analyzed])
            words = re.findall(r'\b\w+\b', all_text.lower())
            stopwords = set([
                "the", "is", "it", "and", "a", "to", "of", "i", "in", "that", "on", "for", "this", "with", "so",
                "now", "but", "all", "was", "its", "not"
            ])
            filtered_words = [w for w in words if w not in stopwords]
            word_freq = Counter(filtered_words)
            top_words = word_freq.most_common(10)

            if top_words:
                words_df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
                st.bar_chart(words_df.set_index("Word"))
            else:
                st.info("Not enough data to display top words.")

        with col2:
            st.markdown("<h4>📈 Sentiment Distribution</h4>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1}
            )
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)
            ax.axis('equal')
            st.pyplot(fig)

    

if __name__ == "__main__":
    main()
