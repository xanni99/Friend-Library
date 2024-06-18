from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List
from init import db, ma


class Group(db.Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100))

    user: Mapped[List["User"]] = relationship(back_populates='group')


class GroupSchema(ma.Schema):
    class Meta:
        fields = ["id", "name"]