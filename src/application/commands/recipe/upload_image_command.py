from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class UploadImageCommand:
    mime_type: str
    content: BinaryIO
