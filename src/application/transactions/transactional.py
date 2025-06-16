import functools
from collections.abc import Callable
from typing import Any, TypeVar

from .configuration import CurrentITransactionManager


F = TypeVar("F", bound=Callable[..., Any])


def transactional(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        manager = CurrentITransactionManager.get_transaction_manager()
        if not manager:
            raise ValueError("Transaction manager is not set.")
        with manager:
            return func(*args, **kwargs)

    return wrapper  # type: ignore
