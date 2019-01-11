import unittest
from emmet.element import Attribute, Element, ElementCollection, Text


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
        el.set_content([Text("some text")])
        self.assertEqual("<div>some text</div>", str(el))

    def test_element_with_multiple_text_content(self):
        el = Element()
        el.name = "div"

        el.set_content([Text("some text"), Text("and some more")])
        self.assertEqual("<div>\n\tsome text\n\tand some more\n</div>", str(el))

        el.set_content([Text("some text"), Text("and some more"), Text("third")])
        self.assertEqual(
            "<div>\n\tsome text\n\tand some more\n\tthird\n</div>", str(el)
        )

    def test_nested_elements(self):
        el = Element("div")
        el.set_content([Element("i")])
        self.assertEqual("<div>\n\t<i>{}</i>\n</div>", str(el))

    def test_nested_elements_with_siblings(self):
        el = Element("div")
        el.set_content([Element("em"), Element("strong")])
        self.assertEqual("<div>\n\t<em>{}</em>\n\t<strong>{}</strong>\n</div>", str(el))


class TestElementCollection(unittest.TestCase):
    def test_length(self):
        self.assertEqual(2, len(ElementCollection([Element(), Element()])))

    def test_flatten(self):
        el = Element()
        el.repeat = 3
        flattened = ElementCollection([el]).flatten()
        self.assertIsInstance(flattened, list)
        self.assertEqual(3, len(flattened))


if __name__ == "__main__":
    unittest.main()
