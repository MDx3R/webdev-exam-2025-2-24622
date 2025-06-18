from abc import ABC, abstractmethod


class IMarkdownSanitizer(ABC):
    @abstractmethod
    def sanitize(self, text: str) -> str: ...
