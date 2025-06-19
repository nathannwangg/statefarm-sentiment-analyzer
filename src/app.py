import streamlit as st
from ingestion import fetch_posts
from analysis import analyze_sentiments, plot_sentiment_distribution, sentiment_summary
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
            "score": random.randint(1, 100)
        }
        for i in range(1, 11)
    ]

def display_single_post(post, col):
    dummy_comments = [
        {"user": "user123", "comment": "This is super helpful!", "score": 15},
        {"user": "dev_guru", "comment": "I disagree with this take.", "score": -2},
        {"user": "ai_enthusiast", "comment": "Great explanation, thanks!", "score": 7}
    ]

    comment_summary = (
        "Overall, the community response is mixed with a slight positive lean. "
        "Several users appreciated the post's clarity, while others raised counterpoints."
    )

    score_color = "#4CAF50" if post['score'] >= 50 else "#FF5252"

    with col.container():
        # Display the post box
        st.markdown(f"""
        <div style='position: relative; padding: 15px; border-radius: 10px; background-color: #F5F5F5; margin-bottom: 15px;'>
            <div style='position: absolute; top: 10px; right: 10px; width: 60px; height: 60px; border-radius: 50%; background-color: {score_color}; display: flex; justify-content: center; align-items: center; color: white; font-size: 18px; font-weight: bold;'>
                {post['score']}
            </div>
            <h4 style='color: #333333; margin-bottom: 10px;'>{post['title']}</h4>
            <p style='color: #666666; font-size: 14px; margin-bottom: 10px;'>{post['body']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Expandable comment section with post + comment summary
        with st.expander("💬 Open Comments"):
            st.markdown(f"**📝 Post Summary:** {post['body']}")
            st.markdown(f"**💡 Comment Summary:** {comment_summary}")

            # st.divider()

            # st.markdown("**🗨️ Top Comments:**")
            # for comment in dummy_comments:
            #     comment_color = "#d4edda" if comment["score"] > 0 else "#f8d7da"
            #     st.markdown(f"""
            #     <div style='padding: 10px; border-radius: 8px; background-color: {comment_color}; margin-bottom: 10px;'>
            #         <strong>{comment['user']}</strong>: {comment['comment']}
            #         <span style='float: right; color: #555;'>Score: {comment['score']}</span>
            #     </div>
            #     """, unsafe_allow_html=True)

# Function to display multiple posts in a column
def display_posts(posts, col):
    for post in posts[:5]:  # Limit to top 5
        display_single_post(post, col)


# Dummy sentiment analysis output
def analyze_sentiments(posts):
    result = []
    for post in posts:
        polarity = random.uniform(-1, 1)
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        result.append({
            "title": post["title"],
            "body": post["body"],
            "compound": polarity,
            "sentiment": sentiment
        })
    return result

# Create a sentiment summary
def sentiment_summary(data):
    total = len(data)
    pos = sum(1 for d in data if d["sentiment"] == "Positive")
    neu = sum(1 for d in data if d["sentiment"] == "Neutral")
    neg = sum(1 for d in data if d["sentiment"] == "Negative")
    avg_compound = sum(d["compound"] for d in data) / total
    return {
        "Count": total,
        "Positive (%)": round(pos / total * 100),
        "Neutral (%)": round(neu / total * 100),
        "Negative (%)": round(neg / total * 100),
        "Average Compound": avg_compound
    }

# Plot sentiment pie chart
def plot_sentiment_distribution(data):
    labels = ["Positive", "Neutral", "Negative"]
    sizes = [
        sum(1 for d in data if d["sentiment"] == "Positive"),
        sum(1 for d in data if d["sentiment"] == "Neutral"),
        sum(1 for d in data if d["sentiment"] == "Negative"),
    ]
    colors = ["#A3E4D7", "#F9E79F", "#F5B7B1"]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

# Bonus: Emotion bar chart
def plot_emotion_bar(summary):
    fig, ax = plt.subplots()
    categories = ["Positive", "Neutral", "Negative"]
    values = [
        summary["Positive (%)"],
        summary["Neutral (%)"],
        summary["Negative (%)"]
    ]
    bars = ax.barh(categories, values, color=["#2ECC71", "#F4D03F", "#E74C3C"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentage")
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f"{int(width)}%", va='center')
    st.pyplot(fig)

# Bonus: Word cloud
def plot_wordcloud(posts):
    all_text = " ".join(post["body"] for post in posts)
    wc = WordCloud(width=600, height=300, background_color="white").generate(all_text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

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

    with tab1:
        st.markdown("<h3 style='text-align: center; color: #FF6961;'>Top 5 Posts</h3>", unsafe_allow_html=True)

        posts = fetch_posts("dummy_subreddit")

        positive_posts = [p for p in posts if p['score'] >= 50]
        negative_posts = [p for p in posts if p['score'] < 50]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='text-align: center; color: #4CAF50;'>Positive Posts</h4>", unsafe_allow_html=True)
            display_posts(positive_posts, col1)

        with col2:
            st.markdown("<h4 style='text-align: center; color: #FF5252;'>Negative Posts</h4>", unsafe_allow_html=True)
            display_posts(negative_posts, col2)

    with tab2: 
        # Replace with: posts = fetch_posts(sub) when connected
        example_posts = [
            {"title": "I love the new update!", "body": "It's amazing and super smooth."},
            {"title": "Why is it so buggy?", "body": "The app crashes all the time now."},
            {"title": "It’s okay I guess", "body": "Nothing special, but not bad either."}
        ]

        # Analyze sentiment
        analyzed = analyze_sentiments(example_posts)
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
