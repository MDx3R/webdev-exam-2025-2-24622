from dataclasses import dataclass


@dataclass
class ImageDTO:
    filename: str
    mime_type: str
