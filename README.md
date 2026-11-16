# Budget tracker v1
## Description:
- Budget tracker is a desktop application built in Python using several different libraries
- This application should help you with tracking your expenses
### How it works:
#### UI
    - PySide6 with its widgets is used for the user interface
    - PySide creates 3 different layouts and switches between them when the user clicks one of the buttons (these layouts are stored in a stack)
    - Every layout has its own class - History_window, Main_page and Transaction_window
    - The whole UI is controlled by Main_window (which also has its own class)
##### Main_page
    - After the user starts the program, the main page is the first layout that is shown
    - On the main page there are 2 buttons for getting to the history of expenses and creating a new transaction
    - In the middle of the main page is a QLabel that shows how much the user can spend in this term (the term is counted from the 15th to the 15th of the next month)
    - The text is automatically refreshed after the user clicks on any button
##### New_transaction
    - The user gets here after clicking on "New transaction"
    - There are 3 QTextEdits with placeholders (each placeholder guides the user to type the correct input)
    - When all QTextEdits are filled in, the user can click on the "Add transaction" button and the data will be stored in the database
    - At the bottom is a back button which takes the user back to the Main_page
##### History_window
    - The user gets here after clicking on "Show history of transactions"
    - The user will see a table made by PySide6 with all their previously entered transactions
    - On each line there is a delete button, and if the user clicks on it, the current entry will be deleted from the database and also from the table
    - At the bottom is a back button which takes the user back to the Main_page
### Database
    - The database (DB) is created and managed by a library named sqlite3
    - When the user opens the application for the first time, the DB creates its own database in the current folder named "budget_tracker.db"
    - The database has several functions:
        - Add transaction - gets the values from the UI and stores them in the DB
        - Month budget left - gets entries from the DB, makes a SUM of them and compares it with the pre-defined monthly budget (500 Kč). If the amount is bigger than the limit, the function returns "You are out of budget this month...", otherwise it returns an f-string with text saying how much you can spend this month
        - Count results in term - a function which counts the number of entries and gives that number to the table (how many rows must be created)
        - Delete transaction - a function for deleting a specific record in the DB

#### Error Handling
    - will be added
#### How to Run
    - Firstly you have to download libraies form "requierements.txt"
    - Then you just simply run python interpreter like in other python scripts("python budget_tracker.py")
    - After this step you can use app like as you want