#NOTE: Add following things in this project

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
from argon2 import PasswordHasher
import uuid

app = Flask(__name__)
ph = PasswordHasher()

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
        email = request.form.get("email")
        password = request.form.get("password")
        
        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar()
        if user.email == email:
            try:
                pass_verify = ph.verify(user.password,password)
                print(pass_verify)
                
                if pass_verify:
                    return redirect(url_for('home',userId = user.id))
                else:
                    return redirect(url_for('login'))
            except Exception as e:
                print(e)
                return redirect(url_for('login'))
    return render_template('login.html')  

@app.route("/signup", methods=['GET', 'POST'])  
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        userId = uuid.uuid4()
        stmt = User(id = userId,password= ph.hash(password),email= email)
        db.session.add(stmt)
        db.session.commit()

        return redirect(url_for('home',userId = userId))
    return render_template('signup.html')

@app.route("/home/<uuid:userId>", methods=["GET", "POST"])
def home(userId):
    user = db.get_or_404(User,userId,description=f"No user with id '{userId}'.")
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        transaction_type = request.form.get("transactionType")
        category = request.form.get("categories")
        description = request.form.get("description")
        transac = Transaction(id=uuid.uuid4(),type=transaction_type,amount=amount,category=category,
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

@app.route('/filter/<uuid:userId>', methods=["POST"])
def filter(userId):
    user = db.get_or_404(User,userId,description=f"No user with id '{userId}'.")
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

@app.route('/delete/<uuid:userId>/<uuid:transacId>')
def delete(userId,transacId):
    transac = db.get_or_404(Transaction,transacId)
    db.session.delete(transac)
    db.session.commit()
    return redirect(url_for('home',userId=userId))

if __name__ == "__main__":
    app.run(debug=True)