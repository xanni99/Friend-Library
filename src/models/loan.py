from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from marshmallow import fields, validate
from sqlalchemy import ForeignKey, Boolean
from models.book import BookSchema
from models.user import UserSchema
from init import db, ma


class Loan(db.Model):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    borrow_length: Mapped[int]
    borrow_date: Mapped[date]
    returned_date: Mapped[date] = mapped_column(nullable=True)
    due_date: Mapped[date]
    returned_status: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped["User"] = relationship(back_populates="loans")
    book: Mapped["Book"] = relationship(back_populates="loans")


class LoanSchema(ma.Schema):
    user = fields.Nested(UserSchema, only=["name"])
    book = fields.Nested(BookSchema, only=["title"])
    borrow_length = fields.Integer(required=True, validate=validate.Range(min=1, max=21, error="Borrow length must be between 1 and 21 days"))
    returned_date = fields.Date(allow_none=True)

    class Meta:
        fields = ("id", "borrow_length", "borrow_date", "due_date", "returned_date", "user", "book", "returned_status")