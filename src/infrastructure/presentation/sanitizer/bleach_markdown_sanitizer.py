import bleach

from infrastructure.config.config import ALLOWED_TAGS
from presentation.sanitizer.markdown_sanitizer import IMarkdownSanitizer


class BleachMarkdownSanitizer(IMarkdownSanitizer):
    def __init__(self, allowed_tags: list[str] | None) -> None:
        self.allowed_tags = allowed_tags or ALLOWED_TAGS

    def sanitize(self, text: str) -> str:
        return bleach.clean(text, tags=self.allowed_tags, strip=True)
