from fastapi import APIRouter, Depends

from main.core.dependencies import get_current_user
from main.models.user import User
from main.schemas.response import Response
from main.schemas.user import UserInCreate, UserInDB, UserLogin, UserToken
from main.services.user import UserService

router = APIRouter()


@router.get("", response_model=Response[UserInDB])
def get_user(user: User = Depends(get_current_user)) -> Response:
    """
    Get current user by provided credentials.
    """
    return Response(data=user)


@router.post("", response_model=Response[UserInDB])
def register_user(
    user: UserInCreate, user_service: UserService = Depends()
) -> Response:
    """
    Process user registration.
    """
    user = user_service.register_user(user_create=user)
    return Response(data=user, message="The user was register successfully")


@router.post("/login", response_model=Response[UserToken])
def login_user(user: UserLogin, user_service: UserService = Depends()) -> Response:
    """
    Process user login.
    """
    token = user_service.login_user(user=user)
    return Response(data=token, message="The user authenticated successfully")
