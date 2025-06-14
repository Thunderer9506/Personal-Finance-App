import sqlite3

class Database:
    def __init__(self):
        self.connection = None  # Placeholder for the connection
        self.cursor = None      # Placeholder for the cursor

        try:
            self.connection = sqlite3.connect('finance.db')
            self.cursor = self.connection.cursor()
            print("Successfully connected to the database!")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def createTable(self):
        query = '''
                CREATE TABLE IF NOT EXISTS finance (
                    ID INTEGER PRIMARY KEY NOT NULL,
                    TYPE TEXT NOT NULL,
                    AMOUNT REAL NOT NULL,
                    CATEGORY TEXT NOT NULL,
                    DESCRIPTION TEXT,
                    DATE TEXT
                )
                '''
        self.cursor.execute(query)
        self.connection.commit()
        print("Table Created Successfully")
        return

    def addData(self,type:str,amount:float,category:str,description:str,date:str):
        query = "INSERT INTO finance (ID, TYPE, AMOUNT, CATEGORY, DESCRIPTION, DATE) VALUES (?, ?, ?, ?, ?, ?)"
        
        self.cursor.execute(query, (self.getMaxId() + 1, type, amount, category, description, date))
        self.connection.commit()
        print("New row added Successfully")
        return

    def deleteData(self,id):
        self.cursor.execute("DELETE FROM finance WHERE ID = ?",(id,))
        self.connection.commit()
        print(f"Deleted rows with ID = {id}")
        return
    
    def getAmount(self):
        self.cursor.execute("SELECT * FROM finance")
        data = self.cursor.fetchall()
        sum = 0
        for i in data:
            if i[1] == "Expense":
                sum -= i[2]
            elif i[1] == "Income":
                sum += i[2]

        return sum
    
    def filterData(self, type=None, category=None, date=None):
        query = "SELECT * FROM finance WHERE 1=1"
        params = []
        if type:
            query += " AND TYPE = ?"
            params.append(type)
        if category:
            query += " AND CATEGORY = ?"
            params.append(category)
        if date:
            query += " AND DATE = ?"
            params.append(date)
        self.cursor.execute(query, params)

        return self.cursor.fetchall()
    
    def fetchData(self):
        self.cursor.execute("SELECT * FROM finance")
        data = self.cursor.fetchall()
        return data
    
    def getMaxId(self):
        self.cursor.execute("SELECT MAX(ID) FROM finance")
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else 0

# dbs1 = Database()

# dbs1.createTable()
# print(dbs1.fetchData())
# dbs1.createTable()
# dbs1.addData("Expense", 1200.00, "Food", "Lunch at restaurant", "2025-05-20")
# dbs1.addData("Income", 5000.00, "Salary", "Monthly salary", "2025-05-21")
# dbs1.addData("Expense", 300.00, "Transportation", "Bus fare", "2025-05-22")
# dbs1.addData("Expense", 800.00, "Bill", "Electricity bill", "2025-05-23")
# dbs1.addData("Income", 200.00, "Awards", "Quiz competition", "2025-05-24")
# dbs1.addData("Expense", 150.00, "Shoping", "Bought a book", "2025-05-24")
# dbs1.addData("Income", 1000.00, "Rental", "House rent received", "2025-05-25")
# dbs1.addData("Expense", 400.00, "Education", "Online course", "2025-05-25")
# print(dbs1.getAmount())
# # Get all expenses
# expenses = dbs1.filterData(type="Expense")
# print(expenses)

# # Get all income in "Salary" category
# salary_income = dbs1.filterData(type="Income", category="Salary")
# print(salary_income)

# # Get all transactions on a specific date
# on_date = dbs1.filterData(date="21-05-2025")
# print(on_date)

# dbs1.deleteData(3)