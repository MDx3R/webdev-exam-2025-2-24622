import io
import os
import tempfile

import pytest

from infrastructure.store.image.local_image_store import LocalImageStore


class TestLocalImageStore:
    @pytest.fixture(autouse=True)
    def sutup(self):
        with tempfile.TemporaryDirectory() as dir:
            self.dir = dir
            self.store = LocalImageStore(self.dir)
            self.filename = "image1.jpg"
            self.data = "some image data"
            self.create_file(self.filename, self.data)
            yield

    def create_file(self, filename: str, data: str):
        f = open(self.build_path(filename), "wb")
        f.write(data.encode())
        f.close()

    def read_file(self, filename: str) -> str:
        f = open(self.build_path(filename), "rb")
        data = f.read().decode()
        f.close()
        return data

    def build_path(self, filename: str) -> str:
        return os.path.join(self.dir, filename)

    def test_store_creates_dir_when_not_exists(self):
        dir = f"{self.dir}/testdir"
        assert not os.path.exists(dir)
        LocalImageStore(dir)
        assert os.path.exists(dir)

    def test_get_retrieves_image_successfully(self):
        with self.store.get(self.filename) as file:
            retrieved = file
            assert file.read() == self.data.encode()
        assert retrieved.closed

    def test_get_raises_when_not_found(self):

        with pytest.raises(FileNotFoundError):
            with self.store.get("random filename"):
                pass

    def test_update_saves_file(self):
        filename = "image2.jpg"
        data = "some image2 data"

        self.store.upload(filename, io.BytesIO(data.encode()))

        file = self.read_file(filename)
        assert file == data

    def test_update_raises_when_exists(self):
        filename = "image3.jpg"
        data = "some image3 data"
        self.create_file(filename, data)

        with pytest.raises(FileExistsError):
            self.store.upload(filename, io.BytesIO(data.encode()))
