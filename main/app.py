from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from main.api.v1.router import router as api_router
from main.core.config import get_app_settings
from main.core.exceptions import add_exceptions_handlers


def create_app() -> FastAPI:
    """
    Application factory, used to create application.
    """
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api/v1")

    add_exceptions_handlers(app=application)

    return application


app = create_app()
