# SF-SENTI: Subreddit Emotion Network & Textual Insights

Welcome to **SENTI** — a Reddit sentiment analysis tool built for rapid insights into community mood and engagement. SENTI scrapes posts and comments from any subreddit, performs sentiment analysis, and visualizes the results in an interactive dashboard.

---

## Project Purpose

Reddit communities often reflect evolving public sentiment. SENTI helps users:

- Understand emotional trends within subreddits  
- Visualize positivity, negativity, and neutrality over time  
- Identify top contributing posts to community sentiment  
- Easily monitor community health

---

## Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python 3.11+ |
| Reddit API | PRAW |
| Sentiment Analysis | VADER (NLTK) |
| Visualization | Streamlit |
| (Optional Backend API) | FastAPI |
| Deployment | Local / Replit / Hugging Face Spaces |

---

## Features

- Reddit API integration via PRAW
- Sentiment analysis using VADER
- In-memory or simple SQLite storage
- Streamlit dashboard:
  - Pie chart of sentiment distribution
  - Line chart of sentiment trend
  - Top positive/negative posts
  - Word cloud of common terms
- Fully deployable with minimal setup

---

## Setup Instructions

### 1. Clone this Repository

```bash
git clone https://github.com/nathannwangg/statefarm-sentiment-analyzer.git
```

## Quickstart

```bash
git clone <this-repo>
cd <this-repo>
cp .env.example .env   # fill in your REDDIT_* creds
docker-compose up --build
```
