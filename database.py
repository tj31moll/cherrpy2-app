import sqlite3

class AllowanceTrackerDB:
    def __init__(self):
        self.conn = sqlite3.connect('allowancetracker.db')
        self.conn.execute('PRAGMA foreign_keys = ON')  # enable foreign key constraints
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                cost REAL NOT NULL
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (activity_id) REFERENCES activities (id)
            )
        ''')

        self.conn.commit()

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()

    def add_user(self, name, balance):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users (name, balance) VALUES (?, ?)', (name, balance))
        self.conn.commit()
        return cursor.lastrowid

    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

    def update_user_balance(self, user_id, amount):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))
        self.conn.commit()

    def get_all_activities(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM activities')
        return cursor.fetchall()

    def add_activity(self, name, cost):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO activities (name, cost) VALUES (?, ?)', (name, cost))
        self.conn.commit()
        return cursor.lastrowid

    def get_activity(self, activity_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
        return cursor.fetchone()

    def add_transaction(self, user_id, activity_id, amount):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO transactions (user_id, activity_id, amount) VALUES (?, ?, ?)', (user_id, activity_id, amount))
        self.update_user_balance(user_id, -amount)  # deduct amount from user's balance
        self.conn.commit()
        return cursor.lastrowid

    def get_transactions_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT transactions.id, activities.name, transactions.amount
            FROM transactions
            JOIN activities ON transactions.activity_id = activities.id
            WHERE transactions.user_id = ?
        ''', (user_id,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
