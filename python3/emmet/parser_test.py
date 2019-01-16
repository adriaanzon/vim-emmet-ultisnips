import unittest

from emmet import add_tabstops, expand_abbreviation


class TestExpandAbbreviation(unittest.TestCase):
    def test_tag(self):
        self.assertEqual("<p>$0</p>", expand_abbreviation("p"))

    def test_tag_with_class(self):
        self.assertEqual('<p class="foo">$0</p>', expand_abbreviation("p.foo"))

    def test_delimited_keywords(self):
        self.assertEqual("<my-tag>$0</my-tag>", expand_abbreviation("my-tag"))
        self.assertEqual(
            '<p class="text-center">$0</p>', expand_abbreviation("p.text-center")
        )
        self.assertEqual(
            '<p id="my-paragraph">$0</p>', expand_abbreviation("p#my-paragraph")
        )
        self.assertEqual(
            '<p id="myParagraph">$0</p>', expand_abbreviation("p#myParagraph")
        )
        self.assertEqual(
            '<p class="text-center sm:text-left sm:flex-grow">$0</p>',
            expand_abbreviation("p.text-center.sm:text-left.sm:flex-grow"),
        )

    def test_class(self):
        self.assertEqual('<div class="foo">$0</div>', expand_abbreviation(".foo"))

    def test_classes(self):
        self.assertEqual(
            '<div class="foo bar">$0</div>', expand_abbreviation(".foo.bar")
        )

    def test_id(self):
        self.assertEqual('<div id="foo">$0</div>', expand_abbreviation("#foo"))

    def test_ids(self):
        self.assertEqual('<div id="bar">$0</div>', expand_abbreviation("#foo#bar"))

    def test_tabstops(self):
        self.assertEqual("<div>$0</div>", add_tabstops("<div>{}</div>"))
        self.assertEqual(
            "<div>$1</div><div>$0</div>", add_tabstops("<div>{}</div><div>{}</div>")
        )
        self.assertEqual(
            "<div>$1</div><div>$2</div><div>$0</div>",
            add_tabstops("<div>{}</div><div>{}</div><div>{}</div>"),
        )

    def test_repeat(self):
        self.assertEqual("<div>$1</div>\n<div>$0</div>", expand_abbreviation("div*2"))
        self.assertEqual(
            '<div class="foo" id="bar">$1</div>\n<div class="foo" id="bar">$0</div>',
            expand_abbreviation(".foo#bar*2"),
        )

    def test_child(self):
        self.assertEqual(
            "<div>\n\t<div>$0</div>\n</div>", expand_abbreviation("div>div")
        )
        self.assertEqual(
            "<div>\n\t<div>\n\t\t<div>$0</div>\n\t</div>\n</div>",
            expand_abbreviation("div>div>div"),
        )

    def test_child_with_repeated_parent(self):
        self.assertEqual(
            '<div>\n\t<p>\n\t\t<span class="center">$1</span>\n\t</p>\n\t<p>\n\t\t<span class="center">$2</span>\n\t</p>\n\t<p>\n\t\t<span class="center">$0</span>\n\t</p>\n</div>',
            expand_abbreviation("div>p*3>span.center"),
        )

    def test_text(self):
        self.assertEqual(
            "<p>I'm a paragraph</p>", expand_abbreviation("p{I'm a paragraph}")
        )

    def text_text_and_child_element(self):
        self.assertEqual(
            "<p>\n\tI'm a paragraph\n\t<div></div>\n</p>",
            expand_abbreviation("p{I'm a paragraph}>div"),
        )


if __name__ == "__main__":
    unittest.main()
