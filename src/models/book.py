from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from marshmallow import fields
from init import db, ma

class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(1000))
    is_available: Mapped[bool] = mapped_column(Boolean(), server_default="true")

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(back_populates='books', cascade="all")
    loans: Mapped["Loan"] = relationship(back_populates='book', cascade="all")
    reviews: Mapped["Review"] = relationship(back_populates="book", cascade="all")


class BookSchema(ma.Schema):
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=True)
    description = fields.String(required=True)
    is_available = fields.Boolean(missing=True)

    user = fields.Nested("UserSchema", only=["name"])
    reviews = fields.Nested("ReviewSchema", only=["rating", "review"])

    class Meta:
        fields = ("id", "title", "author", "genre", "description", "is_available", "user", "reviews")