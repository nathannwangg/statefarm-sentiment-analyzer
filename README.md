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
| LLM | Google Gemini |
| Backend API | FastAPI |
| Deployment | Local |

---

## Features

- Reddit API integration via PRAW
- Sentiment analysis using VADER
- In-memory or simple SQLite storage
- Streamlit dashboard:
  - Pie chart of sentiment distribution
  - Line chart of sentiment trend
  - Top positive/negative posts with LLM generated summaries of post and comments
- Fully deployable with minimal setup

---

## Architecture

```
[Data Ingest] -> [Database] <- [Summarization Worker]
       |                         |
       v                         v
   [Sentiment]             [API Backend] -> [Frontend]
```

* **Data Ingest Service**: Python script (`ingest.py`)
* **Summarization Worker**: Triggers LLM calls when needed
* **API Backend**: FastAPI application (`app/`)
* **Frontend**: React app consuming `/api` endpoints

## Tech Stack

* **Backend**: Python 3.11, FastAPI, PRAW, VADER
* **Database**: SQLite 3
* **LLM**: Google Gemini API
* **Frontend**: Streamlit
  
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


### Environment Variables

Create a `.env` file in the project root with the following keys:

```ini
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_app_user_agent
GOOGLE_GEMINI_API_KEY=your_api_key
```

## Database Schema

**Table: posts**

| Column            | Type    | Description                         |
| ----------------- | ------- | ----------------------------------- |
| `id`              | TEXT    | Reddit post ID (primary key)        |
| `title`           | TEXT    | Post title                          |
| `body`            | TEXT    | Post body                           |
| `comments`        | TEXT    | List of comments                    |
| `created_utc`     | INTEGER | Unix timestamp of creation          |
| `permalink`       | TEXT    | Reddit post URL suffix              |
| `sentiment`       | REAL    | Sentiment score \[-1.0, 1.0]        |
| `label`           | TEXT    | `Positive` / `Neutral` / `Negative` |
| `text_summary`    | TEXT    | LLM-generated summary of the post   |
| `comment_summary` | TEXT    | LLM-generated summary of comments   |

## API Endpoints

| Method | Path                                | Description                               |
| ------ | ----------------------------------- | ----------------------------------------- |
| GET    | `/api/sentiment-summary`            | Returns a summary of all sentiments       |
| GET    | `/api/get_top_positive`             | Top 5 positive posts                      |
| GET    | `/api/get_top_positive`             | Top 5 negative posts                      |
| GET    | `/api/summarize{post_id}`           | Retrieves summaries of post and comments  |

When running app in container, visit
http://127.0.0.1:8000/docs/
for API docs

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/XYZ`)
3. Commit your changes (`git commit -m 'Add XYZ'`)
4. Push to the branch (`git push origin feat/XYZ`)
5. Open a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

