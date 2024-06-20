from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, ForeignKey
from marshmallow import fields, validate
from init import db, ma
from models.book import BookSchema
from models.user import UserSchema


class Review(db.Model):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column()
    review: Mapped[str] = mapped_column(String(1000))
    date: Mapped[date]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped["User"] = relationship(back_populates="reviews", cascade="all")
    book: Mapped["Book"] = relationship(back_populates="reviews", cascade="all")


class ReviewSchema(ma.Schema):
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5, error="Rating must be between 1 and 5"))
    review = fields.String(required=True)
    user = fields.Nested(UserSchema, only=["name"])
    book = fields.Nested(BookSchema, only=["title","author"])

    class Meta:
        fields = ("id", "rating", "review", "date", "user", "book")


class UpdateReviewSchema(ma.Schema):
    rating = fields.Integer(validate=validate.Range(min=1, max=5, error="Rating must be between 1 and 5"))
    review = fields.String()
    user = fields.Nested(UserSchema, only=["name"])
    book = fields.Nested(BookSchema, only=["title","author"])

    class Meta:
        fields = ("id", "rating", "review", "date", "user", "book")