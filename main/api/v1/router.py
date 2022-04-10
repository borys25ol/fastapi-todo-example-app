from fastapi import APIRouter

from main.api.v1.routes import status, tasks, user

router = APIRouter()

router.include_router(router=status.router, tags=["Status"], prefix="/status")
router.include_router(router=user.router, tags=["User"], prefix="/user")
router.include_router(router=tasks.router, tags=["Tasks"], prefix="/tasks")
