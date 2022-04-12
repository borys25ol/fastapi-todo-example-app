from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from main.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa


class Task(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    done = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="tasks")

    def __init__(self, title: str, owner_id: int) -> None:
        self.title = title
        self.owner_id = owner_id
