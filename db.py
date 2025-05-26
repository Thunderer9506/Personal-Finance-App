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

    def addData(self,id:int,type:str,amount:float,category:str,description:str,date:str):
        query = "INSERT INTO finance (ID, TYPE, AMOUNT, CATEGORY, DESCRIPTION, DATE) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (id, type, amount, category, description, date))
        self.connection.commit()
        print("New row added Successfully")
    def deleteData(self):
        pass
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

dbs1 = Database()

# dbs1.createTable()
# print(dbs1.fetchData())
# dbs1.createTable()
# dbs1.addData(1, "Expense", 1200.00, "Food", "Lunch at restaurant", "20-05-2025")
# dbs1.addData(2, "Income", 5000.00, "Salary", "Monthly salary", "21-05-2025")
# dbs1.addData(3, "Expense", 300.00, "Transportation", "Bus fare", "22-05-2025")
# dbs1.addData(4, "Expense", 800.00, "Bill", "Electricity bill", "23-05-2025")
# dbs1.addData(5, "Income", 200.00, "Awards", "Quiz competition", "24-05-2025")
# dbs1.addData(6, "Expense", 150.00, "Shoping", "Bought a book", "24-05-2025")
# dbs1.addData(7, "Income", 1000.00, "Rental", "House rent received", "25-05-2025")
# dbs1.addData(8, "Expense", 400.00, "Education", "Online course", "25-05-2025")
# print(dbs1.getAmount())
# Get all expenses
expenses = dbs1.filterData(type="Expense")
print(expenses)

# Get all income in "Salary" category
salary_income = dbs1.filterData(type="Income", category="Salary")
print(salary_income)

# Get all transactions on a specific date
on_date = dbs1.filterData(date="21-05-2025")
print(on_date)