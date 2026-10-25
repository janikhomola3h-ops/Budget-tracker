import os
import sys
import sqlite3
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
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
        if self.spend is None:
            self.spend = 0
        self.diff = def_month_budget - self.spend
        return self.diff

    def limit_check(self, def_month_budget = 500): #This functin returns you you are or not out of budget
        if int(self.spend) > int(def_month_budget):
            self.limit_result = "You are out of foundings in this term..."
        else:
            self.limit_result = "You have some money lefts in this term..."

    def today_date(self): #Getting today date and sending it in to Database class
        self.full_date = str(date.today())
        self.year, self.month, self.day = self.full_date.split("-")
    def passive_income(self, start_d, end_d, def_month_budget = 500): #Adding automaticaly income every month
        self.today_date()
        c = self.conn.cursor()
        c.execute("""SELECT COUNT (*) FROM budget_tracker WHERE date >= ? AND date <= ?""", (start_d, end_d))
        count = c.fetchone()[0]

        if count == 0:
            c.execute("""INSERT INTO budget_tracker (date, amount, category, description) VALUES(?,?,?,?)""", (self.full_date, 500, "System", "Automatic income"))
            self.conn.commit()

class UI(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.db = database
        self.diff = self.db.month_budget("2026-10-01", "2026-10-31")
        central = QWidget() # creating layout
        self.pages = QStackedWidget() # Creating space for pages
        self.main_layout = QVBoxLayout(central)
        self.pages.addWidget(central) # Adding main page to the stack of pages
        self.setCentralWidget(self.pages)
        self.left_budg_label()#Calling label function
        self.Trancaction_button = QPushButton("Add transaction") #Creating transaction button
        self.b_transaction()#Calling transaction button function
        self.History_button = QPushButton("Show history of transaction")#Creating transaction history button
        self.b_history() #Calling history button function

        #CONNECTING BUTTONS
        self.History_button.clicked.connect(lambda: self.pages.setCurrentIndex(1))

    def build_history(self):
        self.history = QWidget()
        self.history_layout = QVBoxLayout(self.history)
        self.pages.addWidget(self.history)


        


        

    def left_budg_label(self): #Creating and conf. label to show if you are in budget or not
        if self.diff > 500:
            self.l_budg_left = QLabel(f"You are out of budget... {self.diff}Kč ")
        else:
            self.l_budg_left = QLabel(f"You can spend this month {self.diff}Kč ")
        self.l_budg_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_budg_left.setStyleSheet("font-size: 18px;")
        self.main_layout.addWidget(self.l_budg_left)

    def b_transaction(self): #Setting up transaction button
        self.main_layout.addWidget(self.Trancaction_button)

    def b_history(self):
        self.main_layout.addWidget(self.History_button)
    

def main():
    conn = sqlite3.connect("budget_tracker.db")
    db = Database(conn)
    app = QApplication(sys.argv)
    window = UI(db)
    window.setWindowTitle("Budget tracker v1")
    basedir = os.path.dirname(os.path.abspath(__file__)) #getting ABS icon path
    i_path = os.path.join(basedir, "money.png")
    window.setWindowIcon(QIcon(i_path)) #showing icon of the app
    window.show() #show the window
    app.exec()

if __name__ == "__main__":
    main()