from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from marshmallow import fields
from sqlalchemy import ForeignKey
from typing import List
from init import db, ma


class Loan(db.Model):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    borrow_date: Mapped[date]
    return_date: Mapped[date]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped["User"] = relationship(back_populates="loans", cascade="all")
    book: Mapped["Book"] = relationship(back_populates="loans", cascade="all")


class LoanSchema(ma.Schema):
    user = fields.Nested("UserSchema")
    book = fields.Nested("BookSchema")

    class Meta:
        fields = ("id", "borrow_date", "return_date", "user", "book")