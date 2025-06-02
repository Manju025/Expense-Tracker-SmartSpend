import sqlite3
def create_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, 
                 date TEXT, 
                 category TEXT,
                 amount REAL,
                 description TEXT)''')
    conn.commit()
    conn.close()
    
def insert_expense(date, category, amount, description):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''INSERT INTO expenses (date, category, amount, description)
                 VALUES (?, ?, ?, ?)''', (date, category, amount, description))
    conn.commit()
    conn.close()

def fetch_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM expenses''')
    data = c.fetchall()
    conn.close()
    return data

