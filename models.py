from sqlalchemy import String, Integer, Text,create_engine, Date, ForeignKey, select, insert, and_
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker
from datetime import date,datetime
from extensions import db
from typing import List
import uuid
from argon2 import PasswordHasher

# ---------- Engine ----------
# engine = create_engine("sqlite:///./instance/finance.db")

# ---------- Base ----------
# class Base(DeclarativeBase):
#     pass

# ---------- Session Factory ----------
# SessionLocal = sessionmaker(bind=engine, autoflush=False)

# ---------- Models ----------
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String,nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User: Id:{self.id}, Email:{self.email}, Password:{self.password}>"

class Transaction(db.Model):
    __tablename__ = "transactions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String,nullable=False)
    amount: Mapped[int] = mapped_column(Integer,nullable=False)
    category: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(Text, default="No Description")
    date: Mapped[date] = mapped_column(Date,nullable=False, default=date.today())
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"<Transaction: Id:{self.id}, Type:{self.type}, Amount:{self.amount}, Category:{self.category}, Description:{self.description},  Date:{self.date},  User_Id:{self.userId}> "
    

# if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    # print("--- Tables has been created ---")
    # ph = PasswordHasher()
    # Session = sessionmaker(bind=engine)

    # --- Reading data from user and transaction ---
    # with Session() as session:
    #     stmt = select(User).where(and_(User.email == , User.password ==))
    #     user = session.scalars(stmt).first()
    #     transactions = user.transactions
    #     first_transactions = transactions[0]
    #     print(first_transactions.user)

    # --- Create Users ---
    # fake_users = [
    #     {"id":uuid.uuid4(),"email": "aarav.mehta@example.com", "password": ph.hash(password="Pass@123")},
    #     {"id":uuid.uuid4(),"email": "isha.kapoor@example.com", "password": ph.hash(password="Qwerty!45")},
    #     {"id":uuid.uuid4(),"email": "rohan.desai@example.com", "password": ph.hash(password="Secret#908")},
    # ]
    # with Session() as session:
        # session.execute(insert(User),fake_users)
        # session.commit()

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
        
    # for i in data:
    #     if i[1] == 1:
    #         stmt = select(User).where(User.email == "aarav.mehta@example.com")
    #     elif i[1] == 2:
    #         stmt = select(User).where(User.email == "isha.kapoor@example.com")
    #     elif i[1] == 3:
    #         stmt = select(User).where(User.email == "rohan.desai@example.com")

    #     user = session.scalar(stmt)
    #     transac = Transaction(id = uuid.uuid4(),type=i[2],amount=i[3],category=i[4],description=i[5],date=datetime.strptime(i[6],"%Y-%m-%d"),userId=user.id)
    #     session.add(transac)
    #     session.commit()

        