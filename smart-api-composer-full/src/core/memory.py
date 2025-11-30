import sqlite3
from pathlib import Path
from typing import List, Tuple

DB_PATH = Path("memory.db")

class MemoryBank:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS workflows (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          goal TEXT,
          plan_summary TEXT,
          apis_used TEXT,
          status TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        conn.close()

    def save_workflow_summary(
        self, goal: str, plan_summary: str, apis_used: str, status: str
    ):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO workflows (goal, plan_summary, apis_used, status)
        VALUES (?, ?, ?, ?)
        """, (goal, plan_summary, apis_used, status))
        conn.commit()
        conn.close()

    def fetch_recent(self, limit: int = 5) -> List[Tuple]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        SELECT goal, plan_summary, apis_used, status, created_at
        FROM workflows
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        conn.close()
        return rows

memory_bank = MemoryBank()
