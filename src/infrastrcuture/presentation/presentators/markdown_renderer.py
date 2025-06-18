from markdown2 import markdown  # type: ignore

from presentation.presentators.markdown_renderer import IMarkdownRenderer


class MarkdownRenderer(IMarkdownRenderer):
    def render(self, text: str) -> str:
        return markdown(text)
