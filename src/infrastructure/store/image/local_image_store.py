import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import BinaryIO

from application.interfaces.services.image_store import IImageStore


class LocalImageStore(IImageStore):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _full_path(self, filename: str) -> str:
        return os.path.join(self.base_path, filename)

    @contextmanager
    def get(self, filename: str) -> Iterator[BinaryIO]:
        full_path = self._full_path(filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image '{filename}' not found.")
        f = open(full_path, "rb")
        try:
            yield f
        finally:
            f.close()

    def upload(self, filename: str, content: BinaryIO) -> None:
        full_path = self._full_path(filename)
        if os.path.exists(full_path):
            raise FileExistsError(f"Image '{filename}' already exists.")
        full_path = self._full_path(filename)
        with open(full_path, "wb") as f:
            f.write(content.read())
