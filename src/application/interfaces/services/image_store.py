from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import BinaryIO


class IImageStore(ABC):
    @abstractmethod
    @contextmanager
    def get(self, filename: str) -> Iterator[BinaryIO]: ...
    @abstractmethod
    def upload(self, filename: str, content: BinaryIO) -> None: ...
