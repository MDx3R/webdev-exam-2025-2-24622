from abc import ABC, abstractmethod
from typing import BinaryIO


class IImageStore(ABC):
    @abstractmethod
    def get(self, filename: str) -> BinaryIO: ...
    @abstractmethod
    def upload(self, filename: str, content: BinaryIO) -> None: ...
