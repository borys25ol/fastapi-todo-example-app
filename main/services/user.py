from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from main.core.exceptions import (
    InvalidUserCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from main.core.logging import logger
from main.core.security import get_basic_auth_token, verify_password
from main.db.repositories.users import UsersRepository, get_users_repository
from main.models.user import User
from main.schemas.user import UserInCreate, UserLogin, UserToken


class UserService:
    def __init__(
        self, user_repo: UsersRepository = Depends(get_users_repository)
    ) -> None:
        self.user_repo = user_repo

    def login_user(self, user: UserLogin) -> UserToken:
        """
        Authenticate user with provided credentials.
        """
        logger.info(f"Try to login user: {user.username}")
        self.authenticate(username=user.username, password=user.password)
        return UserToken(
            token=get_basic_auth_token(username=user.username, password=user.password)
        )

    def register_user(self, user_create: UserInCreate) -> User:
        """
        Register user in application.
        """
        logger.info(f"Try to find user: {user_create.username}")
        db_user = self.user_repo.get_by_username(username=user_create.username)
        if db_user:
            raise UserAlreadyExistException(
                message=f"User with username: `{user_create.username}` already exists",
                status_code=HTTP_401_UNAUTHORIZED,
            )
        logger.info(f"Creating user: {user_create.username}")
        user = self.user_repo.create(obj_create=user_create)
        return user

    def get_user(self, credentials: HTTPBasicCredentials) -> Optional[User]:
        """
        Retrieve current user info by login credentials.
        """
        logger.info(f"Getting user: {credentials.username}")
        return self.user_repo.get_by_username(username=credentials.username)

    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticate user.
        """
        logger.info(f"Try to authenticate user: {username}")
        user = self.user_repo.get_by_username(username=username)
        if not user:
            raise UserNotFoundException(
                message=f"User with username: `{username}` not found",
                status_code=HTTP_401_UNAUTHORIZED,
            )
        if not verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            raise InvalidUserCredentialsException(
                message="Invalid credentials", status_code=HTTP_401_UNAUTHORIZED
            )
        return user

    def check_is_active(self, user: User) -> bool:
        """
        Check if user account is active.
        """
        return self.user_repo.is_active(user=user)
