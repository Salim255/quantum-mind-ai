from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseDTO(BaseModel, Generic[T]):
    """
    Standard API response wrapper.

    Example:

        {
            "status": "success",
            "data": {
                "id": "...",
                "title": "Quantum Entanglement"
            }
        }
    """

    status: str = "success"
    data: Optional[T] = None


    @classmethod
    def success(
        cls,
        data: T,
    ) -> "ResponseDTO[T]":
        """
        Create a successful API response.
        """

        return cls(
            status="success",
            data=data,
        )