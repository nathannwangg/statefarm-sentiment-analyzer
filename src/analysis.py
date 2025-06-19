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
        text = f"{p['title']} {p.get('body', '')}"  # Use .get for safety
        scores = sid.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        out.append({**p, "sentiment": scores, "label": label})
    return out

# Create pie chart from sentiment analysis
def plot_sentiment_distribution(sentiments):                        
    # Adapt your existing plot function but bigger figsize
    from collections import Counter

    labels = [p['label'] for p in sentiments]
    counts = Counter(labels)
    sizes = [counts.get(label, 0) for label in ["Positive", "Neutral", "Negative"]]
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']

    fig, ax = plt.subplots(figsize=(7,7))  # Bigger figure
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=["Positive", "Neutral", "Negative"],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 14}
    )
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
    avg_compound = sum(p['sentiment']['compound'] for p in sentiments) / total

    return {
        "Positive (%)": round(pos_count / total * 100, 2),
        "Neutral (%)": round(neu_count / total * 100, 2),
        "Negative (%)": round(neg_count / total * 100, 2),
        "Average Compound": round(avg_compound, 4),
        "Count": total
    }