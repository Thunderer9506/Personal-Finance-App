from flask import Flask,render_template,request,redirect
from datetime import datetime
from db import Database

app = Flask(__name__)

todaysDate = datetime.now().strftime("%d-%m-%Y")
expenseCategory = ['Food','Transportation','Bill','Shoping','Education']
incomeCategory = ['Salary','Awards','Coupons','Grants','Rental']


@app.context_processor
def inject_global():
    return {'date': todaysDate}

@app.route("/", methods=["GET","POST"])
def home():
    database = Database()
    error = None
    if request.method == "POST":
        amount = request.form.get("amount")
        transaction_type = request.form.get("transactionType")
        category = request.form.get("categories")
        description = request.form.get("description")
        if not amount or not transaction_type:
            error = "All fields are required."
        else:
            database.addData(transaction_type,float(amount),category,description,todaysDate)
            return redirect('/')
    return render_template('index.html',
                           category = {'expense': expenseCategory,'income':incomeCategory},
                           history=database.fetchData(),
                           amount = database.getAmount(),
                           error = error)

