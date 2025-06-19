# VADER logic

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

def analyze_sentiments(posts: list[dict]) -> list[dict]:
    out = []
    for p in posts:
        text = f"{p['title']} {p['body']}"
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
