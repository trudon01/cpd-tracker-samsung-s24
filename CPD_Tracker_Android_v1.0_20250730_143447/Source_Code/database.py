import sqlite3
import os
from datetime import datetime
from kivy.logger import Logger

# Database configuration
DB_DIR = "cpd_tracker"
DB_PATH = os.path.join(DB_DIR, "cpd.db")

def ensure_directory():
    """Ensure the database directory exists"""
    os.makedirs(DB_DIR, exist_ok=True)

def init_db():
    """Initialize the database with proper schema"""
    ensure_directory()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create the main table
        c.execute("""CREATE TABLE IF NOT EXISTS cpd_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_created TEXT NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            photo TEXT,
            points INTEGER DEFAULT 0,
            created_timestamp REAL DEFAULT (julianday('now'))
        )""")
        
        # Add points column if it doesn't exist (for existing databases)
        try:
            c.execute("ALTER TABLE cpd_entries ADD COLUMN points INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
        # Create backup tracking table
        c.execute("""CREATE TABLE IF NOT EXISTS backup_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backup_date TEXT NOT NULL,
            backup_path TEXT NOT NULL,
            entries_count INTEGER,
            status TEXT DEFAULT 'completed'
        )""")
        
        # Create index for better performance
        c.execute("""CREATE INDEX IF NOT EXISTS idx_date_start 
                     ON cpd_entries(date_start)""")
        c.execute("""CREATE INDEX IF NOT EXISTS idx_type 
                     ON cpd_entries(type)""")
        
        conn.commit()
        Logger.info("CPD: Database initialized successfully")
        
    except Exception as e:
        Logger.error(f"CPD: Database initialization error: {e}")
        raise
    finally:
        conn.close()

def insert_entry(data):
    """Insert a new CPD entry"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""INSERT INTO cpd_entries 
                     (date_created, date_start, date_end, name, type, description, photo, points) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (data["date"], data["date_start"], data["date_end"], 
                   data["name"], data["type"], data["description"], data["photo"], data["points"]))
        
        entry_id = c.lastrowid
        conn.commit()
        
        Logger.info(f"CPD: Entry {entry_id} inserted successfully")
        return entry_id
        
    except Exception as e:
        Logger.error(f"CPD: Error inserting entry: {e}")
        raise
    finally:
        conn.close()

def get_all_entries():
    """Retrieve all CPD entries"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""SELECT id, date_created, date_start, date_end, name, type, description, photo 
                     FROM cpd_entries ORDER BY date_start DESC""")
        
        entries = c.fetchall()
        return entries
        
    except Exception as e:
        Logger.error(f"CPD: Error retrieving entries: {e}")
        return []
    finally:
        conn.close()

def get_entries_count():
    """Get total number of entries"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM cpd_entries")
        count = c.fetchone()[0]
        return count
        
    except Exception as e:
        Logger.error(f"CPD: Error getting entries count: {e}")
        return 0
    finally:
        conn.close()

def log_backup(backup_path, entries_count, status="completed"):
    """Log backup information"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""INSERT INTO backup_log (backup_date, backup_path, entries_count, status) 
                     VALUES (?, ?, ?, ?)""",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                   backup_path, entries_count, status))
        
        conn.commit()
        Logger.info(f"CPD: Backup logged: {backup_path}")
        
    except Exception as e:
        Logger.error(f"CPD: Error logging backup: {e}")
    finally:
        conn.close()

def get_last_backup_date():
    """Get the date of the last successful backup"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""SELECT backup_date FROM backup_log 
                     WHERE status = 'completed' 
                     ORDER BY backup_date DESC LIMIT 1""")
        
        result = c.fetchone()
        return result[0] if result else None
        
    except Exception as e:
        Logger.error(f"CPD: Error getting last backup date: {e}")
        return None
    finally:
        conn.close()

# Initialize database when module is imported
init_db()
