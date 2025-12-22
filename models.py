import sqlite3

DATABASE_NAME = 'bookshelf.db'

# models.py の修正箇所

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            rating INTEGER,
            memo TEXT,
            date_read TEXT,
            source TEXT  -- ← これを追加！
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, rating, memo, date_read, source): # ← sourceを追加
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, rating, memo, date_read, source) VALUES (?, ?, ?, ?, ?, ?)",
        (title, author, rating, memo, date_read, source) # ← sourceを追加
    )
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_book(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
