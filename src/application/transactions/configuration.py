from .transaction_manager import ITransactionManager


class CurrentTransactionManager:
    _manager: ITransactionManager | None = None

    @classmethod
    def set(cls, manager: ITransactionManager):
        cls._manager = manager

    @classmethod
    def get(cls) -> ITransactionManager | None:
        return cls._manager

    @classmethod
    def reset(cls):
        cls._manager = None
