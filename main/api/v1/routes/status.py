from fastapi import APIRouter

from main.schemas.status import Status
from version import response

router = APIRouter()


@router.get("", response_model=Status)
def status() -> Status:
    """
    Health check for API.
    """
    return Status(**response)
