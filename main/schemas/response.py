from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

ResponseData = TypeVar("ResponseData")


class Response(GenericModel, Generic[ResponseData]):
    success: bool = True
    data: Optional[ResponseData] = None
    message: str = ""
    errors: Optional[list] = None
