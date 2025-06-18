from unittest.mock import patch

from infrastrcuture.presentation.sanitizer.bleach_markdown_sanitizer import (
    BleachMarkdownSanitizer,
)


class TestBleachMarkdownSanitizer:
    def test_sanitize_removes_disallowed_tags(self):
        sanitizer = BleachMarkdownSanitizer(allowed_tags=["b", "i"])
        dirty = "<b>bold</b> <script>alert(1)</script> <i>italic</i>"
        clean = sanitizer.sanitize(dirty)
        assert "<script>" not in clean
        assert "<b>bold</b>" in clean
        assert "<i>italic</i>" in clean

    def test_sanitize_with_default_tags(self):
        with patch(
            "infrastrcuture.presentation.sanitizer.bleach_markdown_sanitizer.ALLOWED_TAGS",
            ["b"],
        ):
            sanitizer = BleachMarkdownSanitizer(allowed_tags=None)
            dirty = "<b>ok</b> <i>no</i>"
            clean = sanitizer.sanitize(dirty)
            assert "<b>ok</b>" in clean
            assert "<i>no</i>" not in clean
