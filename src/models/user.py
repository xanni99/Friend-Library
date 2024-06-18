from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import List
from marshmallow import fields
from marshmallow.validate import Length
from init import db, ma


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[List["Group"]] = relationship(back_populates="user")
    books: Mapped[List["Book"]] = relationship(back_populates="user")
    loans: Mapped[List["Loan"]] = relationship(back_populates="user")
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(
        validate=Length(min=8, error="Password must be at least 8 characters long"),
        required=True,
    )
    name = fields.String(required=True)
    # group = fields.Nested("GroupSchema")
    is_admin = fields.Boolean(required=False)

    class Meta:
        fields = ("id", "email", "name", "password", "is_admin", "group_id")
