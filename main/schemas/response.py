from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic.generics import GenericModel

ResponseData = TypeVar("ResponseData")


class Response(GenericModel, Generic[ResponseData]):
    success: bool = True
    data: Optional[ResponseData] = None
    message: Optional[str] = None
    errors: Optional[list] = None

    def dict(self, *args, **kwargs) -> Dict[str, Any]:  # type: ignore
        """Exclude `null` values from the response."""
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)
