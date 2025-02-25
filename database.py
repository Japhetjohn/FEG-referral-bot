import sqlite3

DB_PATH = "data/referrals.db"  # Ensure this path is correct

def create_tables():
    """Creates the database tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referral_link TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            referrer_id INTEGER,
            referred_id INTEGER,
            FOREIGN KEY (referrer_id) REFERENCES users (user_id),
            FOREIGN KEY (referred_id) REFERENCES users (user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS points (
            user_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)

    conn.commit()
    conn.close()

def get_referral_link(user_id):
    """Fetches the referral link for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT referral_link FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result[0] if result else None

def get_referrals(user_id):
    """Fetches referrals for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT referred_id FROM referrals WHERE referrer_id = ?", (user_id,))
    referrals = cursor.fetchall()
    
    conn.close()
    
    return [r[0] for r in referrals]

def get_leaderboard():
    """Fetches the top 10 users with the highest points."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, points FROM points ORDER BY points DESC LIMIT 10")
    leaderboard = cursor.fetchall()
    
    conn.close()
    
    return leaderboard

# Ensure tables exist on script import
create_tables()
