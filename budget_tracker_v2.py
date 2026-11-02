import sqlite3
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QTextEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import sys
import os

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        #Setting up main layout
        layout = QVBoxLayout(self)

        #Setting up main text in the main window
        #if budget_left > 0:
        #    x = f"You can spend this month {left_to_spend}"
        #eles:
        #    x = f"You are out of budget this month"
        self.text_on_main_page = QLabel("EDIT LATER")
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
       
class History(QWidget): #Class for history window
    def __init__(self):
        super().__init__()
        #Layout
        layout = QVBoxLayout(self)
        #Adding button for returninh to the home screen
        self.back_button = QPushButton("Back")

        #Adding componets to the layout
        layout.addWidget(self.back_button)
class Transaction(QWidget):
    def __init__(self):
        super().__init__()
        #Layout
        layout = QVBoxLayout(self)

        #Adding editing text bar for amount
        amount_text_box = QTextEdit()
        amount_text_box.setPlaceholderText("Enter amount (for income +; for withdraw -)")
        

        #Adding text bar for date
        date_text_box = QTextEdit()
        date_text_box.setPlaceholderText("Enter todays date in format M/D/Y")

        #Adding text bar for description
        descrition_text_box = QTextEdit()
        descrition_text_box.setPlaceholderText("Enter a description")

        #Adding button for submiting the form
        send_button = QPushButton("Add transaction")

        #Button back to the home screen
        self.back_button = QPushButton("Back")

        #Adding componets to the layout
        layout.addWidget(amount_text_box)
        layout.addWidget(date_text_box)
        layout.addWidget(descrition_text_box)
        layout.addWidget(send_button)
        layout.addWidget(self.back_button)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget tracker") #Title of the window

        #Setting uo the icon of the window
        basedir = os.path.dirname(os.path.abspath(__file__)) #getting ABS icon path
        i_path = os.path.join(basedir, "money.png")
        self.setWindowIcon(QIcon(i_path)) #showing icon of the app

        #Setting up main page on start
        self.main_page = MainPage()
        self.history = History()
        self.transaction = Transaction()

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

        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()