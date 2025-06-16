from .transaction_manager import ITransactionManager


class CurrentITransactionManager:
    _manager: ITransactionManager | None = None

    @classmethod
    def set_transaction_manager(cls, manager: ITransactionManager):
        cls._manager = manager

    @classmethod
    def get_transaction_manager(cls) -> ITransactionManager | None:
        return cls._manager

    @classmethod
    def reset_transaction_manager(cls):
        cls._manager = None
