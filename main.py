from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime

app = Flask(__name__)

todaysDate = datetime.now().strftime("%d-%m-%Y")
expenseCategory = ['Food','Transportation','Bill','Shoping','Education']
incomeCategory = ['Salary','Awards','Coupons','Grants','Rental']
transactionHistory = [1,'Income', 2500.00,'Food','Food and Dining','25-05-2025']


@app.context_processor
def inject_global():
    return {'date': todaysDate}

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        print(request.form["amount"])
        print(request.form["transactionType"])
        print(request.form["categories"])
        print(request.form["description"])

    return render_template('index.html',category = {'expense': expenseCategory,'income':incomeCategory})

