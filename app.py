from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
from db import Database

app = Flask(__name__)

todaysDate = datetime.now().strftime("%Y-%m-%d")
expenseCategory = [None,'Food','Transportation','Bill','Shoping','Education']
incomeCategory = [None,'Salary','Awards','Coupons','Grants','Rental']

@app.context_processor
def inject_global():
    return {'date': todaysDate}

@app.route("/", methods=["GET", "POST"])
def home():
    database = Database()
    
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        transaction_type = request.form.get("transactionType")
        category = request.form.get("categories")
        description = request.form.get("description") 
        if not description:
            description = "No Description"
        
        database.addFinance(transaction_type, amount, category, description.capitalize(), todaysDate)

    return render_template(
        'index.html',
        category={'expense': expenseCategory, 'income': incomeCategory},
        history=database.fetchData(),
        amount=database.getAmount(),
    )

@app.route('/filter', methods=["POST"])
def filter():
    database = Database()
    filter_type = request.form.get("filterType")
    filter_category = request.form.get("filterCategories")
    filter_date = request.form.get("date")
    
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

    filtered_history = database.filterData(filters['type'],filters['category'],filters['date'])
    
    return render_template(
        'index.html',
        category={'expense':expenseCategory, 'income':incomeCategory},
        history=filtered_history,
        amount=database.getAmount(),
    )

@app.route('/delete/<int:id>')
def delete(id):
    datebase = Database()
    datebase.deleteFinance(id)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)