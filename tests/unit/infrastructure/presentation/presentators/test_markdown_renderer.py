from infrastrcuture.presentation.presentators.markdown_renderer import (
    MarkdownRenderer,
)


class TestMarkdownRenderer:
    def test_render_basic_markdown(self):
        renderer = MarkdownRenderer()
        md = "# Title\n\n**bold** _italic_"
        html = renderer.render(md)
        assert "<h1>Title</h1>" in html
        assert "<strong>bold</strong>" in html or "<b>bold</b>" in html
        assert "<em>italic</em>" in html or "<i>italic</i>" in html

    def test_render_empty_string(self):
        renderer = MarkdownRenderer()
        html = renderer.render("")
        assert html == "<p></p>\n"  # default markdown2 behaviour
