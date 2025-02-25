import sqlite3

DB_NAME = "data/referrals.db"

def init_db():
    """Create the database tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create users table (WITH referrer_id column)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referrer_id INTEGER  -- This column was missing!
        )
    """)
    
    # Create referrals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_id INTEGER
        )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, username, referrer_id=None):
    """Add a new user to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("INSERT INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)",
                       (user_id, username, referrer_id))
        
        # If user has a referrer, add to referrals table
        if referrer_id:
            cursor.execute("INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)", (referrer_id, user_id))

        conn.commit()
    
    conn.close()

def get_referrals(user_id):
    """Get the number of referrals for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_leaderboard():
    """Get the top 10 users with the most referrals."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, COUNT(referrals.referred_id) AS referral_count
        FROM users
        LEFT JOIN referrals ON users.user_id = referrals.referrer_id
        GROUP BY users.user_id
        ORDER BY referral_count DESC
        LIMIT 10
    """)
    
    leaderboard = cursor.fetchall()
    conn.close()
    return leaderboard

# Initialize database
init_db()
