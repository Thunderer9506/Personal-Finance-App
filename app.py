#NOTE: Add following things in this project
# SQLAlchemy ORM

# Relational database schema design

# Password encryption (bcrypt, argon2)

# Sessions + cookies

# JWT tokens

# Role-based access control: This simplifies access management by ensuring users only have the permissions they need for their specific job function

# Modular Flask architecture

# Microservice split (auth service, finance service)

# Pagination & filtering

from flask import Flask,render_template,request,redirect,url_for,g
from datetime import datetime
from db import Database

app = Flask(__name__)

todaysDate = datetime.now().strftime("%Y-%m-%d")
expenseCategory = [None,'Food','Transportation','Bill','Shopping','Education', 'Rent', 'Entertainment', 'Investment']
incomeCategory = [None,'Salary','Awards','Coupons','Grants','Rental', 'Freelance']

@app.context_processor
def inject_global():
    return {'date': todaysDate}

def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    db = get_db()
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get('name')
        userId = db.find_user(name,phone)
        return redirect(url_for('home',userId = userId)) 
    return render_template('login.html')  

@app.route("/signup", methods=['GET', 'POST'])  
def signup():
    db = get_db()
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get('name')
        uId = db.insert_newUser(name,phone)
        return redirect(url_for('home',userId = uId)) 
    return render_template('signup.html')  


@app.route("/home/<int:userId>", methods=["GET", "POST"])
def home(userId):        
    db = get_db()                        
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        transaction_type = request.form.get("transactionType")
        category = request.form.get("categories")
        description = request.form.get("description")
        if not description:
            description = "No Description"
        db.insert_newFinance(userId, transaction_type, amount, category, description.capitalize(), todaysDate)

    return render_template(
        'index.html',
        category={'expense': expenseCategory, 'income': incomeCategory},
        history=db.fetchData_finance(userId),    
        amount=db.getAmount(userId),     
        userId = userId
    )

@app.route('/filter/<int:userId>', methods=["POST"])
def filter(userId):
    db = get_db()
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

    filtered_history = db.filterData(userId,filters['type'],filters['category'],filters['date'])
    
    return render_template(
        'index.html',
        category={'expense':expenseCategory, 'income':incomeCategory},
        history=filtered_history,
        amount=db.getAmount(userId),
        userId = userId
    )

@app.route('/delete/<int:uId>/<int:fid>')
def delete(uId,fid):
    db = get_db()
    db.deleteFinance(uId,fid)
    return redirect(url_for('home',userId=uId))

if __name__ == "__main__":
    app.run(debug=False)