# src/storage.py
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("reddit_data.db")


class Storage:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        self._init_db()

    # ---------- writer ----------
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

    # ---------- readers ----------
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

    def get_top_posts(self, label: str, n: int = 5):
        """Return the `n` most-upvoted posts for a given sentiment label."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            """
            SELECT title, body, permalink, sentiment
            FROM posts
            WHERE label = ?
            ORDER BY sentiment DESC
            LIMIT ?
            """,
            (label, n),
        )
        rows = cur.fetchall()
        con.close()
        return rows

    # ---------- private ----------
    def _init_db(self):
        """Create the DB + table if needed, and add summary columns if missing."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        # 1) Create table with new columns (for fresh installs)
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