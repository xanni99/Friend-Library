from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from init import db, ma


class Group(db.Model):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)

    user: Mapped[List["User"]] = relationship(back_populates='group')


class GroupSchema(ma.Schema):
    class Meta:
        fields = ["code"]