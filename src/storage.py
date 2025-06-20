import os
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "data/reddit_data.db"))

class Storage:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        # ensure parent dir exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def save(self, records: list[dict]):
        """Insert or ignore a batch of Reddit posts/comments."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.executemany(
            """
            INSERT OR IGNORE INTO posts
            (id, title, body, comments, created_utc, permalink,
             sentiment, label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    r["id"],
                    r["title"],
                    r["body"],
                    "\n".join(r["comments"]),
                    int(r["created_utc"]),
                    r["permalink"],
                    float(r["sentiment"]["compound"]),
                    r["label"],
                )
                for r in records
            ],
        )
        con.commit()
        con.close()

    def get_daily_counts(self, days: int = 7):
        """Return sentiment counts per day (last `days`)."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            f"""
            SELECT date(created_utc, 'unixepoch')  AS day,
                   SUM(label='Positive') AS pos,
                   SUM(label='Neutral')  AS neu,
                   SUM(label='Negative') AS neg
            FROM posts
            WHERE created_utc >= strftime('%s','now','-{days} days')
            GROUP BY day
            ORDER BY day DESC
            """
        )
        rows = cur.fetchall()
        con.close()
        return rows

    def get_sentiment_summary(self):
        """Return overall sentiment counts."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            """
            SELECT
                   SUM(CASE WHEN label = 'Positive' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN label = 'Neutral' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN label = 'Negative' THEN 1 ELSE 0 END),
                   COUNT(*),
                   AVG(sentiment)
            FROM posts
            """
        )
        row = cur.fetchone()
        con.close()
        
        if not row or row[3] == 0:
            return {
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "total_count": 0,
                "average_sentiment": 0,
            }
        
        pos, neu, neg, total, avg_sentiment = row
        return {
            "positive_count": pos,
            "neutral_count": neu,
            "negative_count": neg,
            "total_count": total,
            "average_sentiment": avg_sentiment,
        }

    def get_top_posts(self, label: str, n: int = 5, days: int = 7):
        """Return the `n` posts with the most extreme sentiment scores for a given label within the last `days`."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        order = "DESC" if label == "Positive" else "ASC"

        query = f"""
            SELECT id, title, body, permalink, sentiment
            FROM posts
            WHERE label = ? AND created_utc >= strftime('%s', 'now', ?)
            ORDER BY sentiment {order}
            LIMIT ?
        """

        cur.execute(
            query,
            (label, f"-{days} days", n),
        )
        rows = cur.fetchall()
        con.close()
        return rows

    def get_post_by_id(self, post_id: str):
        """Return a single post by its ID."""
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, title, body, comments, text_summary, comment_summary
            FROM posts
            WHERE id = ?
            """,
            (post_id,),
        )
        row = cur.fetchone()
        con.close()
        return row

    def update_summaries(self, post_id: str, text_summary: str, comment_summary: str):
        """Update the text and comment summaries for a post."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            """
            UPDATE posts
            SET text_summary = ?, comment_summary = ?
            WHERE id = ?
            """,
            (text_summary, comment_summary, post_id),
        )
        con.commit()
        con.close()

    def _init_db(self):
        """Create the DB + table if needed, and add summary columns if missing."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id               TEXT PRIMARY KEY,
                title            TEXT,
                body             TEXT,
                comments         TEXT,
                created_utc      INTEGER,
                permalink        TEXT,
                sentiment        REAL,
                label            TEXT,
                text_summary     TEXT,
                comment_summary  TEXT
            )
            """
        )

        cur.execute("CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_utc)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_posts_label   ON posts(label)")
        
        con.commit()
        con.close()