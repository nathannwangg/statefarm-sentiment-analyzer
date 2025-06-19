import os
import csv
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "sentiment.csv"

class Storage:
    def __init__(self):
        # If file doesn’t exist, write header
        if not CSV_PATH.exists():
            with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "id",
                    "timestamp",
                    "title",
                    "body",
                    "compound_score",
                    "label"
                ])

    def save(self, records: list[dict]):
        """Append a batch of records to the CSV."""
        with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for r in records:
                # use UTC timestamp or human‐readable
                ts = datetime.utcfromtimestamp(r["created_utc"]).isoformat()
                writer.writerow([
                    r["id"],
                    ts,
                    r["title"],
                    r["body"],
                    r["sentiment"]["compound"],
                    r["label"]
                ])
