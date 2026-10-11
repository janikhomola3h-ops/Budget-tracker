import PyQt6
import os
import sys
import sqlite3

class Database:
    def __init__(self,conn):
        self.conn = conn
        self.create_table()

    def create_table(self): #creating table
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS budget_tracker (
    date text,
    amount real,
    category text,
    description text)""")
        self.conn.commit()
        c.close()

    def add_transaction(self, date, amount, category, description): #adding new transaction
        c = self.conn.cursor()
        c.execute("INSERT INTO budget_tracker (date, amount, category, description) VALUES(?, ?, ?, ?)", (date, amount, category, description))
        self.conn.commit()
        c.close()

    def withdraw(self):
        ...
    def budget_left(self):
        ...
    def passive_income(self):
        ...

def main():
    conn = sqlite3.connect("budget_tracker.db")
    db = Database(conn)

if __name__ == "__main__":
    main()