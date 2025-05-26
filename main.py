from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

expenseCategory = ['Food','Transportation','Bill','Shoping','Education']
incomeCategory = ['Salary','Awards','Coupons','Grants','Rental']


@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        print(request.form["amount"])
        print(request.form["transactionType"])
        print(request.form["categories"])
        print(request.form["description"])

    return render_template('index.html',category = {'expense': expenseCategory,'income':incomeCategory})

