import unittest
from emmet import Attribute, Element, Parser


class TestEmmetStringRepresentations(unittest.TestCase):
    def test_attribute_filters_empty_values(self):
        attr = Attribute("class", ["foo", "", "bar", " ", "  "])
        self.assertEqual('class="foo bar"', str(attr))

    def test_empty_element_has_placeholder(self):
        el = Element()
        el.name = "div"
        self.assertEqual("<div>{}</div>", str(el))

    def test_non_empty_element_has_no_placeholder(self):
        pass


class TestEmmetParser(unittest.TestCase):
    def test_tag(self):
        self.assertEqual("<p>$0</p>", Parser.expand_abbreviation("p"))

    def test_tag_with_class(self):
        self.assertEqual('<p class="foo">$0</p>', Parser.expand_abbreviation("p.foo"))

    def test_delimited_keywords(self):
        self.assertEqual("<my-tag>$0</my-tag>", Parser.expand_abbreviation("my-tag"))
        self.assertEqual(
            '<p class="text-center">$0</p>', Parser.expand_abbreviation("p.text-center")
        )
        self.assertEqual(
            '<p id="my-paragraph">$0</p>', Parser.expand_abbreviation("p#my-paragraph")
        )
        self.assertEqual(
            '<p id="myParagraph">$0</p>', Parser.expand_abbreviation("p#myParagraph")
        )
        self.assertEqual(
            '<p class="text-center sm:text-left sm:flex-grow">$0</p>',
            Parser.expand_abbreviation("p.text-center.sm:text-left.sm:flex-grow"),
        )

    def test_class(self):
        self.assertEqual(
            '<div class="foo">$0</div>', Parser.expand_abbreviation(".foo")
        )

    def test_classes(self):
        self.assertEqual(
            '<div class="foo bar">$0</div>', Parser.expand_abbreviation(".foo.bar")
        )

    def test_id(self):
        self.assertEqual('<div id="foo">$0</div>', Parser.expand_abbreviation("#foo"))

    def test_ids(self):
        self.assertEqual(
            '<div id="bar">$0</div>', Parser.expand_abbreviation("#foo#bar")
        )

    def test_tabstops(self):
        self.assertEqual("<div>$0</div>", Parser.add_tabstops("<div>{}</div>"))
        self.assertEqual(
            "<div>$1</div><div>$0</div>",
            Parser.add_tabstops("<div>{}</div><div>{}</div>"),
        )
        self.assertEqual(
            "<div>$1</div><div>$2</div><div>$0</div>",
            Parser.add_tabstops("<div>{}</div><div>{}</div><div>{}</div>"),
        )


if __name__ == "__main__":
    unittest.main()
