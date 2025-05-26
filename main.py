from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from datetime import datetime

app = Flask(__name__)
id = 1
todaysDate = datetime.now().strftime("%d-%m-%Y")
expenseCategory = ['Food','Transportation','Bill','Shoping','Education']
incomeCategory = ['Salary','Awards','Coupons','Grants','Rental']
transactionHistory = [{'id':1,'type':'Expense','amount': 2500.00,'category':'Food','description':'Food and Dining','date':'25-05-2025'}]

def getAmount():
    sum = 0
    for i in transactionHistory:
        if i['type'] == 'Income':
            sum += i['amount']
        elif i['type'] == 'Expense':
            sum -= i['amount']
    return sum

@app.context_processor
def inject_global():
    return {'date': todaysDate}

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        global id
        id += 1
        data = {'id':id,'type':request.form["transactionType"],'amount': float(request.form["amount"]),'category':request.form["categories"],'description':request.form["description"],'date':todaysDate}
        transactionHistory.append(data)
        return redirect('/')
    return render_template('index.html',
                           category = {'expense': expenseCategory,'income':incomeCategory},
                           history=transactionHistory,
                           amount = getAmount())

