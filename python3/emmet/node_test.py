import unittest

from emmet.node import Attribute, AttributeCollection, Element, NodeCollection, Text


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

    def test_nested_elements_with_repeated_child(self):
        div = Element("div")
        p = Element("p")
        p.repeat = 2
        div.content.append(p)
        collection = NodeCollection([div])
        self.assertEqual("<div>\n\t<p>{}</p>\n\t<p>{}</p>\n</div>", str(collection))

    def test_nested_elements_with_repeated_parent(self):
        div = Element("div")
        div.repeat = 2
        div.content.append(Element("p"))
        collection = NodeCollection([div])
        self.assertEqual(
            "<div>\n\t<p>{}</p>\n</div>\n<div>\n\t<p>{}</p>\n</div>", str(collection)
        )

    def test_indentation_is_applied_for_each_level(self):
        div = Element("div")
        p = Element("p")
        p.content.append(Element("span"))
        div.content.append(p)
        self.assertEqual(
            "<div>\n\t<p>\n\t\t<span>{}</span>\n\t</p>\n</div>",
            str(NodeCollection([div])),
        )


class TestNodeCollection(unittest.TestCase):
    def test_length(self):
        self.assertEqual(2, len(NodeCollection([Element(), Element()])))


class TestAttributeCollection(unittest.TestCase):
    def test_length(self):
        collection = AttributeCollection(
            [Attribute("id", "some-id"), Attribute("class", "some-class")]
        )
        self.assertEqual(2, len(collection))

    def test_getitem(self):
        id_attr = Attribute("id", "some-id")
        class_attr = Attribute("class", "some-class")
        collection = AttributeCollection([id_attr, class_attr])

        self.assertEqual(id_attr, collection["id"])
        self.assertEqual(class_attr, collection["class"])

    def test_setitem(self):
        collection = AttributeCollection()
        collection["id"] = "some-id"

        self.assertEqual(1, len(collection))
        self.assertEqual(["some-id"], collection["id"].values)

    def test_overwrite(self):
        collection = AttributeCollection([Attribute("id", "some-id")])
        collection["id"] = "some-other-id"
        self.assertEqual(1, len(collection))
        self.assertEqual(["some-other-id"], collection["id"].values)


if __name__ == "__main__":
    unittest.main()
