#NOTE: Add following things in this project

# Password encryption (bcrypt, argon2)

# Sessions + cookies

# JWT tokens

# Role-based access control: This simplifies access management by ensuring users only have the permissions they need for their specific job function

# Modular Flask architecture

# Microservice split (auth service, finance service)

# Pagination & filtering

from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime
from sqlalchemy import select, and_
from extensions import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    # import models AFTER initializing db
    from models import User, Transaction
    db.create_all()

todaysDate = datetime.now().strftime("%Y-%m-%d")
expenseCategory = [None,'Food','Transportation','Bill','Shopping','Education', 'Rent', 'Entertainment', 'Investment']
incomeCategory = [None,'Salary','Awards','Coupons','Grants','Rental', 'Freelance']

# ---- Util Functions ----
@app.context_processor
def inject_global():
    return {'date': todaysDate,'expense': expenseCategory, 'income': incomeCategory}

def getAmount(history):
    sum = 0
    for i in history:
        if i.type == "Expense":
            sum -= i.amount
        elif i.type == "Income":
            sum += i.amount
    return sum

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get('name')
        
        stmt = select(User).where(
            and_(
                User.fullName == name,
                User.phoneNumber == phone
                ))
        user = db.session.execute(stmt).scalar()
        return redirect(url_for('home',userId = user.id))
    return render_template('login.html')  

@app.route("/signup", methods=['GET', 'POST'])  
def signup():
    if request.method == "POST":
        phone = request.form.get("phone")
        name = request.form.get('name')
        stmt = User(fullName= name,phoneNumber= phone)
        db.session.add(stmt)
        db.session.flush()
        uId = stmt.id
        db.session.commit()
        return redirect(url_for('home',userId = uId))
    return render_template('signup.html')


@app.route("/home/<int:userId>", methods=["GET", "POST"])
def home(userId):
    user = db.get_or_404(User,userId,description=f"No user named '{userId}'.")
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        transaction_type = request.form.get("transactionType")
        category = request.form.get("categories")
        description = request.form.get("description")
        transac = Transaction(type=transaction_type,amount=amount,category=category,
                              description = [None if not description else description.capitalize()][0],
                              userId = userId)
        user.transactions.append(transac)
        db.session.commit()
    transacHistory = user.transactions
    return render_template(
        'index.html',
        history=transacHistory,    
        amount=getAmount(transacHistory),     
        userId = userId
    )

@app.route('/filter/<int:userId>', methods=["POST"])
def filter(userId):
    user = db.get_or_404(User,userId,description=f"No user named '{userId}'.")
    filter_type = request.form.get("filterType") or None
    filter_category = request.form.get("filterCategories")
    filter_date = request.form.get("date") or None

    if filter_category == "None":
        filter_category = None

    query = Transaction.query.filter_by(userId=user.id)

    if filter_type:
        query = query.filter_by(type=filter_type)

    if filter_category:
        query = query.filter_by(category=filter_category)

    if filter_date:
        query = query.filter_by(date=datetime.strptime(filter_date,"%Y-%m-%d"))

    filtered_history = query.all()

    return render_template(
        "index.html",
        history=filtered_history,
        amount=getAmount(user.transactions),
        userId=userId
    )

@app.route('/delete/<int:uId>/<int:fid>')
def delete(uId,fid):
    transac = db.get_or_404(Transaction,fid)
    db.session.delete(transac)
    db.session.commit()
    return redirect(url_for('home',userId=uId))

if __name__ == "__main__":
    app.run(debug=True)