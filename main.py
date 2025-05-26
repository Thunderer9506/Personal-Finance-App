from flask import Flask,render_template,request,redirect
from datetime import datetime
from db import Database

app = Flask(__name__)

todaysDate = datetime.now().strftime("%Y-%m-%d")
expenseCategory = [None,'Food','Transportation','Bill','Shoping','Education']
incomeCategory = [None,'Salary','Awards','Coupons','Grants','Rental']

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
        
        database.addData(transaction_type,float(amount),category,description,todaysDate)
        return redirect('/')
    return render_template('index.html',
                           category = {'expense': expenseCategory,'income':incomeCategory},
                           history=database.fetchData(),
                           amount = database.getAmount(),
                           error = error)

@app.route('/filter', methods=["POST"])
def filter():
    database = Database()
    error = None
    filter_type = request.form.get("filterType")
    filter_category = request.form.get("filterCategories")
    filter_date = request.form.get("date")
    print(filter_type,filter_category,filter_date)
    # Only pass non-empty filters
    filters = {}
    if filter_type:
        filters['type'] = filter_type
    else:
        filters['type'] = None
    if filter_category != "None":
        filters['category'] = filter_category
    else:
        filters['category'] = None
    if filter_date:
        filters['date'] = filter_date
    else:
        filters['date'] = None

    # print(database.filterData())
    filtered_history = database.filterData(filters['type'],filters['category'],filters['date'])
    # print(filtered_history)
    return render_template(
        'index.html',
        category={'expense': expenseCategory, 'income': incomeCategory},
        history=filtered_history,
        amount=database.getAmount(),
        error=error
    )
