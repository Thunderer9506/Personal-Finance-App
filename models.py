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