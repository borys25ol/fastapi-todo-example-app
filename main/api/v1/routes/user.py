from fastapi import APIRouter, Depends

from main.core.dependencies import get_current_user
from main.db.tables import User
from main.schemas.auth import UserInCreate, UserInDB, UserLogin, UserToken
from main.schemas.response import Response
from main.services.auth import BasicAuthService

router = APIRouter()


@router.get("", response_model=Response[UserInDB])
def get_user(user: User = Depends(get_current_user)) -> Response:
    """
    Get current user by provided credentials.
    """
    return Response(data=user)


@router.post("", response_model=Response[UserInDB])
def register_user(
    user: UserInCreate, service: BasicAuthService = Depends()
) -> Response:
    """
    Process user registration.
    """
    user = service.register_user(user_create=user)
    return Response(data=user, message="The user was register successfully")


@router.post("/login", response_model=Response[UserToken])
def login_user(user: UserLogin, service: BasicAuthService = Depends()) -> Response:
    """
    Process user login.
    """
    token = service.login_user(user=user)
    return Response(data=token, message="The user authenticated successfully")
