from sqlalchemy import String, Integer, Text,create_engine, Date, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker
from datetime import date,datetime
from extensions import db
from typing import List

# ---------- Engine ----------
engine = create_engine("sqlite:///./instance/finance.db")

# ---------- Base ----------
# class Base(DeclarativeBase):
#     pass

# ---------- Session Factory ----------
# SessionLocal = sessionmaker(bind=engine, autoflush=False)

# ---------- Models ----------
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String,nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User: Id:{self.id}, Full Name:{self.fullName}, Phone Number:{self.phoneNumber}>"

class Transaction(db.Model):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String,nullable=False)
    amount: Mapped[int] = mapped_column(Integer,nullable=False)
    category: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(Text, default="No Description")
    date: Mapped[date] = mapped_column(Date,nullable=False, default=date.today())
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"<Transaction: Id:{self.id}, Type:{self.type}, Amount:{self.amount}, Category:{self.category}, Description:{self.description},  Date:{self.date},  User_Id:{self.userId}> "
    

# if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    # print("--- Tables has been created ---")

    # --- Reading data from user and transaction ---
    # Session = sessionmaker(bind=engine)
    # with Session() as session:
    #     stmt = select(User).where(User.id == 1)
    #     user = session.scalars(stmt).first()
    #     transactions = user.transactions
    #     first_transactions = transactions[0]
    #     print(first_transactions.user)

    # --- Create Users ---
    # with Session() as session:
    #     user1 = User(fullName = 'Aarav Mehta', phoneNumber = 9876543210)
    #     user2 = User(fullName = 'Priya Sharma', phoneNumber = 9123456789)
    #     user3 = User(fullName = 'Rohan Iyer', phoneNumber = 9988776655)
    #     session.add_all([user1,user2,user3])
    #     session.commit()

    # --- Create Transactions ---
    # with Session() as session:
    #     data = [
    #             (1, 1, 'Income', 75000.00, 'Salary', 'Monthly salary credited', '2025-10-01'),
    #             (2, 1, 'Expense', 1200.00, 'Food', 'Dinner at restaurant', '2025-10-03'),
    #             (3, 1, 'Expense', 5000.00, 'Rent', 'Shared apartment rent', '2025-10-05'),
    #             (4, 1, 'Expense', 800.00, 'Transport', 'Cab rides and metro', '2025-10-07'),
    #             (5, 1, 'Income', 1500.00, 'Freelance', 'Website design project', '2025-10-10'),
    #             (6, 2, 'Income', 68000.00, 'Salary', 'Monthly salary', '2025-10-02'),
    #             (7, 2, 'Expense', 2200.00, 'Food', 'Groceries and snacks', '2025-10-04'),
    #             (8, 2, 'Expense', 4500.00, 'Shopping', 'Clothes and cosmetics', '2025-10-06'),
    #             (9, 2, 'Expense', 600.00, 'Transport', 'Office commute', '2025-10-09'),
    #             (10, 2, 'Income', 3000.00, 'Bonus', 'Quarterly performance bonus', '2025-10-12'),
    #             (11, 3, 'Income', 82000.00, 'Salary', 'Monthly salary payment', '2025-10-01'),
    #             (12, 3, 'Expense', 3000.00, 'Food', 'Dining out and groceries', '2025-10-03'),
    #             (13, 3, 'Expense', 7000.00, 'Rent', 'Apartment rent', '2025-10-05'),
    #             (14, 3, 'Expense', 1500.00, 'Entertainment', 'Concert tickets', '2025-10-08'),
    #             (15, 3, 'Income', 2000.00, 'Investment', 'Stock dividend payout', '2025-10-10')
    #         ]
        
    #     for i in data:
    #         transaction1 = Transaction(type=i[2],amount=i[3],category=i[4],description=i[5],date=datetime.strptime(i[6],"%Y-%m-%d"),userId=i[1])
    #         session.add(transaction1)
    #         session.commit()
    