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
from main.db.repositories.users import UsersRepository, get_users_repository
from main.db.tables import User
from main.schemas.auth import UserInCreate, UserLogin, UserToken
from main.services.security import get_basic_auth_token, verify_password


class BasicAuthService:
    """
    Basic Auth service.
    """

    def __init__(self, db: UsersRepository = Depends(get_users_repository)) -> None:
        self.db = db

    def get_user(self, credentials: HTTPBasicCredentials) -> Optional[User]:
        """
        Retrieve current user info by login credentials.
        """
        logger.info(f"Getting user: {credentials.username}")
        return self.db.get_by_username(username=credentials.username)

    def login_user(self, user: UserLogin) -> UserToken:
        """
        Authenticate user with provided credentials.
        """
        logger.info(f"Authenticating user: {user.username}")
        self.authenticate(username=user.username, password=user.password)
        return UserToken(
            token=get_basic_auth_token(username=user.username, password=user.password)
        )

    def register_user(self, user_create: UserInCreate) -> User:
        """
        Register user in application.
        """
        logger.info(f"Try to find user: {user_create.username}")
        db_user = self.db.get_by_username(username=user_create.username)
        if db_user:
            raise UserAlreadyExistException(
                message=f"User with username: `{user_create.username}` already exists",
                status_code=HTTP_401_UNAUTHORIZED,
            )
        logger.info(f"Creating user: {user_create.username}")
        user = self.db.create(obj_create=user_create)
        return user

    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticate user.
        """
        user = self.db.get_by_username(username=username)
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
