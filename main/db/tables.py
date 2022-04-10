from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from main.db.base import Base
from main.services.security import get_password_hash


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    done = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")

    def __init__(self, title: str, owner_id: int) -> None:
        self.title = title
        self.owner_id = owner_id


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="owner")

    def __init__(
        self, username: str, email: str, full_name: str, password: str
    ) -> None:
        self.username = username
        self.email = email
        self.full_name = full_name
        self.hashed_password = get_password_hash(password=password)

    @property
    def is_active(self) -> bool:
        return not self.disabled
