from abc import ABC, abstractmethod


class ITransactionManager(ABC):
    @abstractmethod
    def rollback(self): ...
    @abstractmethod
    def commit(self): ...
    @abstractmethod
    def __enter__(self) -> "ITransactionManager": ...
    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ): ...
