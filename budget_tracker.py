import PyQt6
import os
import sys
import sqlite3
from datetime import date

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
        c.execute("INSERT INTO budget_tracker (date, amount, category, description) VALUES (?, ?, ?, ?)", (date, amount, category, description))
        self.conn.commit()
        c.close()

    def month_budget(self, start_d, end_d, def_month_budget = 500): #Get data from DB and make difference between def. set money - you spending in your term
        c = self.conn.cursor()
        c.execute("SELECT SUM(amount) FROM budget_tracker WHERE date >= ? AND date <= ?", (start_d, end_d))
        self.spend = c.fetchone()[0]
        self.diff = def_month_budget - self.spend

    def limit_check(self, def_month_budget = 500): #This functin returns you you are or not out of budget
        if int(self.spend) > int(def_month_budget):
            self.limit_result = "You are out of foundings in this term..."
        else:
            self.limit_result = "You have some money lefts in this term..."
    def today_date(self): #Getting today date and sending it in to Database class
        full_date = str(date.today())
        year, month, self.day = full_date.split("-")
    def passive_income(self):
        ...

def main():
    conn = sqlite3.connect("budget_tracker.db")
    db = Database(conn)

if __name__ == "__main__":
    main()
