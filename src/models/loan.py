from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, Boolean, ForeignKey
from typing import List
from marshmallow import fields
from marshmallow.validate import Length
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


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(
        validate=Length(min=8, error="Password must be at least 8 characters long"),
        required=True,
    )
    name = fields.String(required=True)

    class Meta:
        fields = ("id", "email", "name", "password", "is_admin", "group")