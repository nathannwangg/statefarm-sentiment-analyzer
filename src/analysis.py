import matplotlib.pyplot as plt
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import nltk

# Ensure VADER lexicon is downloaded
nltk.download('vader_lexicon')

# Initialize VADER
sid = SentimentIntensityAnalyzer()

# Analyze sentiment of posts
def analyze_sentiments(posts: list[dict]) -> list[dict]:
    out = []
    for p in posts:
        text = f"{p['title']} {p.get('body', '')}"
        scores = sid.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        out.append({**p, "score": compound, "label": label}) 
    return out

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


def sentiment_summary(sentiments):
    total = len(sentiments)
    if total == 0:
        return {
            "Positive (%)": 0,
            "Neutral (%)": 0,
            "Negative (%)": 0,
            "Average Compound": 0,
            "Count": 0
        }

    pos_count = sum(1 for p in sentiments if p['label'] == "Positive")
    neu_count = sum(1 for p in sentiments if p['label'] == "Neutral")
    neg_count = sum(1 for p in sentiments if p['label'] == "Negative")
    avg_compound = sum(p['score'] for p in sentiments) / total

    return {
        "Positive (%)": round(pos_count / total * 100, 2),
        "Neutral (%)": round(neu_count / total * 100, 2),
        "Negative (%)": round(neg_count / total * 100, 2),
        "Average Compound": round(avg_compound, 4),
        "Count": total
    }

def get_top_sentiment_posts(analyzed_posts: list[dict]) -> tuple[list[dict], list[dict]]:
    # Separate posts by sentiment label
    positives = [post for post in analyzed_posts if post["label"] == "Positive"]
    negatives = [post for post in analyzed_posts if post["label"] == "Negative"]

    # Sort each list by compound score
    top_positive = sorted(positives, key=lambda x: x["score"], reverse=True)[:5]
    top_negative = sorted(negatives, key=lambda x: x["score"])[:5]

    return top_positive, top_negative

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
