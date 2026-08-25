import contextlib
import io
import os
import tempfile
import unittest

from Renderer import Renderer
from Token import Token


class TokenTests(unittest.TestCase):
    def test_block_tokens(self):
        cases = {
            "# Heading": ("h1", "Heading"),
            "> quote": ("blockquote", "quote"),
            "**bold**": ("strong", "bold"),
            "*italic*": ("em", "italic"),
            "`code`": ("code", "code"),
            "---": ("hr", ""),
        }

        for source, expected in cases.items():
            with self.subTest(source=source):
                token = Token(source)
                self.assertEqual((token.type, token.val), expected)

    def test_heading_levels(self):
        for level in range(1, 7):
            source = "#" * level + " Heading"
            with self.subTest(level=level):
                token = Token(source)
                self.assertEqual(token.type, f"h{level}")
                self.assertEqual(token.val, "Heading")

    def test_plain_text_is_untyped_and_trimmed(self):
        token = Token("   plain text   ")

        self.assertEqual(token.type, "")
        self.assertEqual(token.val, "plain text")

    def test_link_and_image_tokens(self):
        link = Token('[site](https://example.com "Example")')
        image = Token('![Logo](logo.png "Company logo")')

        self.assertEqual(link.type, "a")
        self.assertEqual(
            link.val,
            {
                "href": "https://example.com",
                "val": "site",
                "title": "Example",
            },
        )
        self.assertEqual(image.type, "img")
        self.assertEqual(
            image.val,
            {"href": "logo.png", "val": "Logo", "title": "Company logo"},
        )

    def test_list_tokens(self):
        self.assertEqual((Token("- item").type, Token("- item").val), ("ul", "item"))
        self.assertEqual((Token("1. item").type, Token("1. item").val), ("ol", "item"))

    def test_alternate_unordered_list_marker(self):
        token = Token("+ item")

        self.assertEqual((token.type, token.val), ("ul", "item"))

    def test_alternate_emphasis_and_strong_markers(self):
        cases = {
            "_italic_": ("em", "italic"),
            "__bold__": ("strong", "bold"),
        }

        for source, expected in cases.items():
            with self.subTest(source=source):
                token = Token(source)
                self.assertEqual((token.type, token.val), expected)

    def test_all_horizontal_rule_markers(self):
        for source in ("___", "***", "---"):
            with self.subTest(source=source):
                token = Token(source)
                self.assertEqual((token.type, token.val), ("hr", ""))


class RendererTests(unittest.TestCase):
    def render_markdown(self, markdown):
        with tempfile.TemporaryDirectory() as directory:
            old_directory = os.getcwd()
            try:
                os.chdir(directory)
                with open("test.md", "w", encoding="utf-8") as markdown_file:
                    markdown_file.write(markdown)

                renderer = Renderer()
                renderer.read()
                with contextlib.redirect_stdout(io.StringIO()):
                    renderer.render()
                return renderer
            finally:
                os.chdir(old_directory)

    def test_renders_blocks_and_specials(self):
        renderer = self.render_markdown(
            '# Title\n\nBody\n\n[site](https://example.com)\n\n'
            '![Logo](logo.png)\n'
        )

        self.assertIn("<h1>Title</h1>", renderer.renderData)
        self.assertIn("<p>Body</p>", renderer.renderData)
        self.assertIn('<a href="https://example.com">site</a>', renderer.renderData)
        self.assertIn('<img src="logo.png" alt="Logo">', renderer.renderData)

    def test_groups_unordered_list_items(self):
        renderer = self.render_markdown("- One\n- Two\n")

        self.assertIn("<ul>", renderer.renderData)
        self.assertIn("<li>One</li>", renderer.renderData)
        self.assertIn("<li>Two</li>", renderer.renderData)

    def test_renders_list_without_trailing_newline(self):
        renderer = self.render_markdown("+ One\n+ Two")

        self.assertIn("<ul>", renderer.renderData)
        self.assertIn("<li>One</li>", renderer.renderData)
        self.assertIn("<li>Two</li>", renderer.renderData)

    def test_preserves_order_of_mixed_blocks(self):
        renderer = self.render_markdown(
            "# First\n\n- Item\n\nFinal paragraph\n"
        )

        heading_position = renderer.renderData.index("<h1>First</h1>")
        list_position = renderer.renderData.index("<ul>")
        paragraph_position = renderer.renderData.index("<p>Final paragraph</p>")

        self.assertLess(heading_position, list_position)
        self.assertLess(list_position, paragraph_position)

    def test_renders_ordered_lists_and_flushes_between_list_types(self):
        renderer = self.render_markdown("1. First\n2. Second\n\n- Third\n")

        self.assertIn("<ol>", renderer.renderData)
        self.assertIn("<li>First</li>", renderer.renderData)
        self.assertIn("<li>Second</li>", renderer.renderData)
        self.assertIn("<ul>", renderer.renderData)
        self.assertIn("<li>Third</li>", renderer.renderData)
        self.assertLess(renderer.renderData.index("</ol>"), renderer.renderData.index("<ul>"))

    def test_renders_titles_on_links_and_images(self):
        renderer = self.render_markdown(
            '[site](https://example.com "Example")\n\n'
            '![Logo](logo.png "Company logo")\n'
        )

        self.assertIn(
            '<a href="https://example.com" title="Example">site</a>',
            renderer.renderData,
        )
        self.assertIn(
            '<img src="logo.png" alt="Logo" title="Company logo">',
            renderer.renderData,
        )

    def test_empty_markdown_renders_nothing(self):
        renderer = self.render_markdown("")

        self.assertEqual(renderer.renderData, "")

    def test_whitespace_only_markdown_renders_nothing(self):
        renderer = self.render_markdown(" \n\n  \n")

        self.assertEqual(renderer.renderData, "")

    def test_save_writes_html_document(self):
        with tempfile.TemporaryDirectory() as directory:
            old_directory = os.getcwd()
            try:
                os.chdir(directory)
                renderer = Renderer()
                renderer.renderData = "<p>Hello</p>"
                renderer.save()

                with open("result.html", encoding="utf-8") as html_file:
                    result = html_file.read()
                self.assertIn("<!DOCTYPE html>", result)
                self.assertIn("<p>Hello</p>", result)
            finally:
                os.chdir(old_directory)


if __name__ == "__main__":
    unittest.main()