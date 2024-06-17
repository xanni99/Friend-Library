from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import ForeignKey
from typing import List
from init import db, ma


class Loan(db.Model):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    borrow_date: Mapped[date]
    return_date: Mapped[date]

    borrower_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    borrower: Mapped[List["User"]] = relationship(back_populates="loans")
    book: Mapped[List["Book"]] = relationship(back_populates="loans")


class LoanSchema(ma.Schema):
    class Meta:
        fields = ("id", "borrow_date", "return_date", "borrower_id", "book_id")