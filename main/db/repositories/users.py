from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from main.core.config import get_app_settings
from main.db.repositories.base import BaseRepository
from main.db.session import get_db
from main.models.user import User
from main.schemas.user import UserInCreate, UserInUpdate

settings = get_app_settings()


class UsersRepository(BaseRepository[User, UserInCreate, UserInUpdate]):
    """
    Repository to manipulate with the task.
    """

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by `username` field.
        """
        return self.db.query(User).filter(User.username == username).first()

    @staticmethod
    def is_active(user: User) -> bool:
        """
        Check if user is active.
        """
        return not user.disabled


def get_users_repository(session: Session = Depends(get_db)) -> UsersRepository:
    return UsersRepository(db=session, model=User)
