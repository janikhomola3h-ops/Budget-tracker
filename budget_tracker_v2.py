import sqlite3
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QTextEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys
import os

class Database(): #Database for tracker
    def __init__(self):
        self.con = sqlite3.connect("budget_tracker.db")
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS budget_tracker (date TEXT, category TEXT, amount REAL)""")
        self.con.commit()

    def add_transaction(self, date, category, amount):
        self.cur.execute("INSERT INTO budget_tracker (date, category, amount) VALUES (?, ?, ?)", (date,category,amount))
        self.con.commit()

    def month_budget_left(self, start_date, end_date, month_budget = 500):
        self.cur.execute("SELECT SUM(amount) FROM budget_tracker WHERE date BETWEEN ? AND ?", (start_date, end_date))
        spend = self.cur.fetchone()[0]
        if spend is None:
            spend = 0
        final_month_budget = month_budget + spend
        return final_month_budget




class MainPage(QWidget):
    def __init__(self, db):
        super().__init__()
        #Setting up main layout
        layout = QVBoxLayout(self)

        #Setting up DB
        self.db = db

        #Getting amont money to spend in this month from month_bud
        budget_left = self.db.month_budget_left("2026/11/01", "2026/14/12")

        #Setting up two diffrents variants of text on main page
        if budget_left < 0:
            text_text_main_page = "You are out of budget this month..."
        else:
            text_text_main_page = f"You can spend this month {budget_left}Kč"

        #Setting up QLabel on main page + putting there one of the text varants
        self.text_on_main_page = QLabel(text_text_main_page)
        self.text_on_main_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_on_main_page.setStyleSheet("font-size: 18px")

        #Creating buttnon for add transaction + connecting it to the action
        self.add_transaction_button = QPushButton("Add transaction")
        #Creating buttnon for history of transactions + connecting it to the action
        self.history_button = QPushButton("Show history of transaction")

        #Adding components to the layout
        layout.addWidget(self.text_on_main_page)
        layout.addWidget(self.add_transaction_button)
        layout.addWidget(self.history_button)
       
class History_window(QWidget): #Class for history window
    def __init__(self):
        super().__init__()
        #Layout
        layout = QVBoxLayout(self)
        #Adding button for returninh to the home screen
        self.back_button = QPushButton("Back")

        #Adding componets to the layout
        layout.addWidget(self.back_button)

class Transaction_window(QWidget):
    def __init__(self):
        super().__init__()
        #Layout
        layout = QVBoxLayout(self)

        #Adding editing text bar for amount
        self.amount_text_box = QTextEdit()
        self.amount_text_box.setPlaceholderText("Enter amount (for income +; for withdraw -)")
        

        #Adding text bar for date
        self.date_text_box = QTextEdit()
        self.date_text_box.setPlaceholderText("Enter todays date in format M/D/Y")

        #Adding text bar for description
        self.descrition_text_box = QTextEdit()
        self.descrition_text_box.setPlaceholderText("Enter a description")

        #Adding button for submiting the form
        self.send_button = QPushButton("Add transaction")

        #Button back to the home screen
        self.back_button = QPushButton("Back")

        #Adding componets to the layout
        layout.addWidget(self.amount_text_box)
        layout.addWidget(self.date_text_box)
        layout.addWidget(self.descrition_text_box)
        layout.addWidget(self.send_button)
        layout.addWidget(self.back_button)
class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        #Setting up DB for MainWindow
        self.db = db

        #Title of the window
        self.setWindowTitle("Budget tracker") 

        #Setting up the icon of the window
        basedir = os.path.dirname(os.path.abspath(__file__)) #getting ABS icon path
        i_path = os.path.join(basedir, "money.png")
        self.setWindowIcon(QIcon(i_path)) #showing icon of the app

        #Setting up main page on start
        self.main_page = MainPage(db)
        self.history = History_window()
        self.transaction = Transaction_window()

        #Creating stack of the pages + adding pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.history)
        self.stack.addWidget(self.transaction)
        self.setCentralWidget(self.stack)



        #Connecting pages
            #Home screen
        self.main_page.history_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.main_page.add_transaction_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
            #Add transaction - screen
        self.transaction.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            #History - screen
        self.history.back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        #connecting buttons
            #Add transaction - Transaction window
        self.transaction.send_button.clicked.connect(self.save_transaction)

    def save_transaction(self):
        date = self.transaction.date_text_box.toPlainText().strip()
        description = self.transaction.descrition_text_box.toPlainText().strip()
        amount = self.transaction.amount_text_box.toPlainText().strip()
        self.db.add_transaction(date, description, amount)
        

def main():
    app = QApplication(sys.argv)
    db = Database()
    window = MainWindow(db)
    window.show()
    app.exec()
    


if __name__ == "__main__":
    main()