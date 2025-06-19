import os
import shutil
from src.storage import Storage

def test_storage_roundtrip(tmp_path):
    os.environ["DB_PATH"] = str(tmp_path / "test.db")
    store = Storage()
    records = [{
        "id": "x1", "created_utc": 0, "title": "t", 
        "body": "b", "sentiment": {"compound": 0.5}, "label": "Positive"
    }]
    store.save(records)
    # simple check: table exists and row was inserted
    conn = store.conn
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM posts")
    assert cur.fetchone()[0] == 1
