import sqlite3
from config import DATABASE_FILE

def connect_db():
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referred_by INTEGER,
            points INTEGER DEFAULT 0,
            wallet TEXT DEFAULT NULL
        )
    ''')
    
    conn.commit()
    return conn, cursor

conn, cursor = connect_db()

def add_user(user_id, referred_by=None):
    """Adds a new user with optional referrer ID."""
    cursor.execute("INSERT OR IGNORE INTO users (user_id, referred_by, points) VALUES (?, ?, 0)", (user_id, referred_by))
    conn.commit()

def get_user(user_id):
    """Gets user details."""
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

def add_wallet(user_id, wallet_address):
    """Stores user wallet address."""
    cursor.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (wallet_address, user_id))
    conn.commit()

def get_wallets():
    """Fetch all users with a wallet address."""
    cursor.execute("SELECT user_id, wallet FROM users WHERE wallet IS NOT NULL")
    return cursor.fetchall()

def add_points(user_id, points=1):
    """Increments user referral points."""
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()

def get_leaderboard():
    """Fetches top 100 users based on points."""
    cursor.execute("SELECT user_id, points FROM users ORDER BY points DESC LIMIT 100")
    return cursor.fetchall()
