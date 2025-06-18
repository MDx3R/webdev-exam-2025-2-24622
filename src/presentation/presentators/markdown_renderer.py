from abc import ABC, abstractmethod


class IMarkdownRenderer(ABC):
    @abstractmethod
    def render(self, text: str) -> str: ...
