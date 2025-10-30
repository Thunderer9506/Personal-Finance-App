import sqlite3
import sqlitecloud
from dotenv import load_dotenv
import os
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None  # Placeholder for the connection
        self.cursor = None      # Placeholder for the cursor
        try:
            self.connection = sqlitecloud.connect(os.getenv('SQLITE_URI'))
            self.cursor = self.connection.cursor()
            print("Successfully connected to the database!")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def createTable(self):
        transaction = '''
                CREATE TABLE IF NOT EXISTS Finances (
                    ID INTEGER PRIMARY KEY NOT NULL,
                    USER_ID INTEGER NOT NULL,
                    TYPE TEXT NOT NULL,
                    AMOUNT REAL NOT NULL,
                    CATEGORY TEXT NOT NULL,
                    DESCRIPTION TEXT,
                    DATE TEXT,
                    FOREIGN KEY (USER_ID) REFERENCES Users(ID)
                )
                '''
        users = '''
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY NOT NULL,
                    FULL_NAME TEXT NOT NULL,
                    PHONE_NUMBER INTEGER NOT NULL UNIQUE
                )
                '''
        self.cursor.execute(transaction)
        self.connection.commit()
        self.cursor.execute(users)
        self.connection.commit()
        print("Tables Created Successfully")
        return
    def insert_newUser(self,name:str, phone:int):
        query = "INSERT INTO Users (ID, FULL_NAME, PHONE_NUMBER) VALUES (?, ?, ?)"
        maxId = self.getMaxId_Users() + 1
        self.cursor.execute(query,(maxId, name.title(), phone,))
        self.connection.commit()
        fakeData = [
            ('Income', 75000.00, 'Salary', 'Monthly salary credited', '2025-10-01'),
            ('Expense', 1200.00, 'Food', 'Dinner at restaurant', '2025-10-03'),
            ('Expense', 5000.00, 'Rent', 'Shared apartment rent', '2025-10-05'),
            ('Expense', 800.00, 'Transport', 'Cab rides and metro', '2025-10-07'),
            ('Income', 1500.00, 'Freelance', 'Website design project', '2025-10-10'),
        ]
        for i in fakeData:
            self.insert_newFinance(maxId,i[0],i[1],i[2],i[3],i[4])
        print("New User Added Successfully of Id {}".format(maxId))
        return maxId
    
    def find_user(self,name,phone):
        query = "SELECT * FROM Users WHERE FULL_NAME = ? AND PHONE_NUMBER = ?"
        self.cursor.execute(query,(name.title(),phone))
        print("Finded user {}".format(name))
        return self.cursor.fetchone()[0]

    def insert_newFinance(self,userId:int,type:str,amount:float,category:str,description:str,date:str):
        query = "INSERT INTO Finances (ID, USER_ID, TYPE, AMOUNT, CATEGORY, DESCRIPTION, DATE) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (self.getMaxId_Finances() + 1, userId, type, amount, category, description, date))
        self.connection.commit()
        print("New row added Successfully")
        return

    def deleteFinance(self,userId,financeId):
        self.cursor.execute("DELETE FROM Finances WHERE USER_ID = ? AND ID = ?",(userId,financeId,))
        self.connection.commit()
        print(f"Deleted rows with ID = {financeId} of User_Id = {userId}")
        return
    
    def getAmount(self,userId:int):
        self.cursor.execute("SELECT AMOUNT, TYPE FROM Finances WHERE USER_ID = ?",(userId,))
        data = self.cursor.fetchall()
        sum = 0
        for amt,type in data:
            if type == "Expense":
                sum -= amt
            elif type == "Income":
                sum += amt
        return sum
    
    def filterData(self, userId, type=None, category=None, date=None):
        query = "SELECT * FROM Finances WHERE 1=1 AND USER_ID = ?"
        params = [userId]
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
    
    def fetchData_finance(self,userId):
        self.cursor.execute("SELECT * FROM Finances WHERE USER_ID = ?",(userId,))
        return self.cursor.fetchall()
    
    def fetchData_user(self):
        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()
    
    def getMaxId_Finances(self):
        self.cursor.execute("SELECT MAX(ID) FROM Finances")
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else 0
    
    def getMaxId_Users(self):
        self.cursor.execute("SELECT MAX(ID) FROM Users")
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else 0
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Connection Closed")


# if __name__ == "__main__":
    # db = Database()
    # db.createTable()
    # data = [(1, 'Aarav Mehta', 9876543210),
    #         (2, 'Priya Sharma', 9123456789),
    #         (3, 'Rohan Iyer', 9988776655)]
    # for i in data:
    #     db.insert_newUser(i[1],i[2])

    # data = [
    #         (1, 1, 'Income', 75000.00, 'Salary', 'Monthly salary credited', '2025-10-01'),
    #         (2, 1, 'Expense', 1200.00, 'Food', 'Dinner at restaurant', '2025-10-03'),
    #         (3, 1, 'Expense', 5000.00, 'Rent', 'Shared apartment rent', '2025-10-05'),
    #         (4, 1, 'Expense', 800.00, 'Transport', 'Cab rides and metro', '2025-10-07'),
    #         (5, 1, 'Income', 1500.00, 'Freelance', 'Website design project', '2025-10-10'),
    #         (6, 2, 'Income', 68000.00, 'Salary', 'Monthly salary', '2025-10-02'),
    #         (7, 2, 'Expense', 2200.00, 'Food', 'Groceries and snacks', '2025-10-04'),
    #         (8, 2, 'Expense', 4500.00, 'Shopping', 'Clothes and cosmetics', '2025-10-06'),
    #         (9, 2, 'Expense', 600.00, 'Transport', 'Office commute', '2025-10-09'),
    #         (10, 2, 'Income', 3000.00, 'Bonus', 'Quarterly performance bonus', '2025-10-12'),
    #         (11, 3, 'Income', 82000.00, 'Salary', 'Monthly salary payment', '2025-10-01'),
    #         (12, 3, 'Expense', 3000.00, 'Food', 'Dining out and groceries', '2025-10-03'),
    #         (13, 3, 'Expense', 7000.00, 'Rent', 'Apartment rent', '2025-10-05'),
    #         (14, 3, 'Expense', 1500.00, 'Entertainment', 'Concert tickets', '2025-10-08'),
    #         (15, 3, 'Income', 2000.00, 'Investment', 'Stock dividend payout', '2025-10-10')
    #     ]
    
    # for i in data:
    #     db.insert_newFinance(i[1],i[2],i[3],i[4],i[5],i[6])
    
    # db.close()