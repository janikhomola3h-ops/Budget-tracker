import sqlite3
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
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
        self.add_transaction = QPushButton("Add transaction")
        #Creating buttnon for history of transactions + connecting it to the action
        self.history_button = QPushButton("Show history of transaction")

        #Adding components to the layout
        layout.addWidget(self.text_on_main_page)
        layout.addWidget(self.add_transaction)
        layout.addWidget(self.history_button)
       
class History(QWidget): #Class for history window
    def __init__(self):
        super().__init__()
        #Layout
        layout = QVBoxLayout(self)

        self.test_text = QLabel("TEST")

        #Adding componets to the layout
        layout.addWidget(self.test_text)

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

        #Creating stack of the pages + adding pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.history)
        self.setCentralWidget(self.stack)



            #Connecting pages
        self.main_page.history_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()