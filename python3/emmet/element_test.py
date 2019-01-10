import unittest
from emmet.element import Attribute, Element


class TestElementStringRepresentations(unittest.TestCase):
    def test_attribute_filters_empty_values(self):
        attr = Attribute("class", ["foo", "", "bar", " ", "  "])
        self.assertEqual('class="foo bar"', str(attr))

    def test_empty_element_has_placeholder(self):
        el = Element()
        el.name = "div"
        self.assertEqual("<div>{}</div>", str(el))

    def test_element_with_text_content(self):
        el = Element()
        el.name = "div"
        el.content = ["some text"]
        self.assertEqual("<div>some text</div>", str(el))

    def test_element_with_multiple_text_content(self):
        el = Element()
        el.name = "div"

        el.content = ["some text", "and some more"]
        self.assertEqual("<div>\n\tsome text\n\tand some more\n</div>", str(el))

        el.content = ["some text", "and some more", "third"]
        self.assertEqual(
            "<div>\n\tsome text\n\tand some more\n\tthird\n</div>", str(el)
        )

    def test_nested_elements(self):
        el = Element("div")
        el.content = [Element("i")]
        self.assertEqual("<div>\n\t<i>{}</i>\n</div>", str(el))

    def test_nested_elements_with_siblings(self):
        el = Element("div")
        el.content = [Element("em"), Element("strong")]
        self.assertEqual("<div>\n\t<em>{}</em>\n\t<strong>{}</strong>\n</div>", str(el))

    def test_element_with_repeated_child(self):
        # TODO: Still need to decide if I'm going to implement a count attribute.
        # I think it's needed when combining nesting (>) with repeating (*).
        self.skipTest("not implemented")
        el = Element("div")
        el.content = [Element("p")]
        el.content[0].count = 3
        self.assertEqual(
            "<div>\n\t<p>{}</p>\n\t<p>{}</p>\n\t<p>{}</p>\n</div>", str(el)
        )


if __name__ == "__main__":
    unittest.main()
