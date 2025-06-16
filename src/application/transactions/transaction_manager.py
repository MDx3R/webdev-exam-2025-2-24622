from abc import ABC, abstractmethod


class ITransactionManager(ABC):
    @abstractmethod
    def __enter__(self): ...
    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ): ...
