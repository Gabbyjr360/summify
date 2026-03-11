import sqlite3
from datetime import datetime
import json
import uuid
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "summify.db")

def init_db():
    """Initialize database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summary_packs (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        summary TEXT NOT NULL,
        key_insights TEXT NOT NULL,
        flashcards TEXT NOT NULL,
        questions TEXT NOT NULL,
        action_points TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        views INTEGER DEFAULT 0
    )
    """)
    
    conn.commit()
    conn.close()

def save_summary_pack(filename, summary, key_insights, flashcards, questions, action_points):
    """Save a summary pack to the database and return its ID."""
    pack_id = str(uuid.uuid4())[:12]
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO summary_packs 
    (id, filename, summary, key_insights, flashcards, questions, action_points)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        pack_id,
        filename,
        summary,
        json.dumps(key_insights) if isinstance(key_insights, list) else key_insights,
        json.dumps(flashcards) if isinstance(flashcards, list) else flashcards,
        json.dumps(questions) if isinstance(questions, list) else questions,
        json.dumps(action_points) if isinstance(action_points, list) else action_points
    ))
    
    conn.commit()
    conn.close()
    
    return pack_id

def get_summary_pack(pack_id):
    """Retrieve a summary pack from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, filename, summary, key_insights, flashcards, questions, action_points, created_at, views
    FROM summary_packs WHERE id = ?
    """, (pack_id,))
    
    row = cursor.fetchone()
    
    if row:
        try:
            key_insights = json.loads(row[3]) if isinstance(row[3], str) else row[3]
        except:
            key_insights = row[3] if row[3] else []
        
        try:
            flashcards = json.loads(row[4]) if isinstance(row[4], str) else row[4]
        except:
            flashcards = row[4] if row[4] else []
        
        try:
            questions = json.loads(row[5]) if isinstance(row[5], str) else row[5]
        except:
            questions = row[5] if row[5] else []
        
        try:
            action_points = json.loads(row[6]) if isinstance(row[6], str) else row[6]
        except:
            action_points = row[6] if row[6] else []
        
        pack = {
            "id": row[0],
            "filename": row[1],
            "summary": row[2],
            "key_insights": key_insights,
            "flashcards": flashcards,
            "questions": questions,
            "action_points": action_points,
            "created_at": row[7],
            "views": row[8]
        }
        
        # Increment views
        cursor.execute("UPDATE summary_packs SET views = views + 1 WHERE id = ?", (pack_id,))
        conn.commit()
        conn.close()
        
        return pack
    
    conn.close()
    return None

# Initialize database on import
init_db()
