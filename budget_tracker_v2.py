import sqlite3
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QTextEdit, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys
import os
import datetime

class Database(): #Database for tracker
    def __init__(self):
        #Setting up datetime library in DB
        self.datetime = datetime

        self.con = sqlite3.connect("budget_tracker.db")
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS budget_tracker (date TEXT, category TEXT, amount REAL)""")
        self.con.commit()

    def add_transaction(self, date, category, amount):
        self.cur.execute("INSERT INTO budget_tracker (date, category, amount) VALUES (?, ?, ?)", (date,category,amount))
        self.con.commit()

    def month_budget_left(self, month_budget = 500):
        #Getting current finance term
        today_date = str(self.datetime.date.today())
        year, month, day = map(int, today_date.split("-"))
        #decision progress using datetime library - reflecting swtiching years and month - starting finance term is 15 every month
        if day >= 15:
            self.start_date = f"{year}-{month:02d}-15"
            if month == 12:
                month = 1
                year = year + 1
            else:
                month += 1
            self.end_date = f"{year}-{month:02d}-15"
        else:
            self.end_date = f"{year}-{month:02d}-15"
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1
            self.start_date = f"{year}-{month:02d}-15"
                    
        
        #Getting deposits/withdraws form DB
        self.cur.execute("SELECT SUM(amount) FROM budget_tracker WHERE date BETWEEN ? AND ?", (self.start_date, self.end_date))
        spend = self.cur.fetchone()[0]
        if spend is None:
            spend = 0
        final_month_budget = month_budget + spend
        return final_month_budget

    def count_of_results_in_term(self):
        self.cur.execute("SELECT rowid, date, category, amount FROM budget_tracker WHERE date >= ? AND date < ?", (self.start_date, self.end_date))
        result = self.cur.fetchall()
        return result

    def delete_transaction(self, rowid):
        self.cur.execute("DELETE FROM budget_tracker WHERE rowid = ?", (rowid,))
        self.con.commit()




class MainPage(QWidget):
    def __init__(self, db):
        super().__init__()
        #Setting up main layout
        layout = QVBoxLayout(self)

        #Setting up DB
        self.db = db

        #Setting up QLabel on main page + putting there one of the text varants
        self.text_on_main_page = QLabel()
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

        self.text_refresh()
    def text_refresh(self): #Setting up two diffrents variants of text on main page
        #Getting amount money to spend in this month from month_bud
        budget_left = self.db.month_budget_left()
        if budget_left < 0:
            self.text_on_main_page.setText("You are out of budget this month...")
        else:
            self.text_on_main_page.setText(f"You can spend this month {budget_left:,.2f}Kč")
       
class History_window(QWidget): #Class for history window
    def __init__(self, db):
        super().__init__()
        #Setting up DB for History window
        self.db = db
        #Layout
        layout = QVBoxLayout(self)
        #Adding button for returninh to the home screen
        self.back_button = QPushButton("Back")

        #Creating table - numbers of rows is made by function in DB and stored to varibale named "rows"
        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Amount", "Category", "Date", "Delete button"])



        #Adding componets to the layout
        layout.addWidget(self.table)
        layout.addWidget(self.back_button)

    def refresh_table(self):
        #Getting data from the DB
        results = self.db.count_of_results_in_term()
        rows = len(results) # counting numbers of records in current term

        #Setting numbers of rows in the table
        self.table.setRowCount(rows)

        #Filling in the informatin form DB to the table
        self.counter = 0

        #For loop for get each record alone + putting in data to the table
        for data in results:
            #Creating varable rowid - getted from DB
            rowid = data[0]
            print(rowid)
            self.table.setItem(self.counter, 0, QTableWidgetItem(str(data[3]))) #Adding amount to the table (row, collum, date,del_button)
            self.table.setItem(self.counter, 1, QTableWidgetItem(data[2]))
            self.table.setItem(self.counter, 2, QTableWidgetItem(data[1]))

            #Creating delete button
            self.delete_button_history = QPushButton("Delete")
            self.delete_button_history.clicked.connect(lambda checked, rid = rowid: self.delete_row(rid)) #Connecting each delete button in with specific rowid
            self.table.setCellWidget(self.counter, 3, self.delete_button_history) #Putting del_button in to the cell
            self.counter += 1

    def delete_row(self, rowid):
        self.db.delete_transaction(rowid)
        self.refresh_table()

                

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
        self.date_text_box.setPlaceholderText("Enter todays date in format YY-MM-DD")

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
        self.history = History_window(db)
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
            #Going back to home screen after adding the transaction
        self.transaction.send_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            #Refreshing budget left text on main page
        self.transaction.send_button.clicked.connect(self.main_page.text_refresh)
            #Refreshing table in History window after each reopen the History of transaction
        self.main_page.history_button.clicked.connect(self.history.refresh_table)
            # Refreshing text on main page after getting back from History window 
        self.history.back_button.clicked.connect(self.main_page.text_refresh)            
        

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