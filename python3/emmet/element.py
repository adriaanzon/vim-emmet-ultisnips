from __future__ import annotations
from typing import List, Optional, Union
from copy import copy


class ElementCollection:
    items: List[Union[Element, Text]]

    def __init__(self, items=None):
        if isinstance(items, self.__class__):
            self.items = items.items
        elif items:
            self.items = items
        else:
            self.items = []

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def append(self, value):
        self.items.append(value)

    # might be made superfluous using a __str__ method
    def flatten(self):
        items = []
        for i in self.items:
            items += [i for _ in range(i.count)]
        return items


class Text:
    body: str
    count = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, body=""):
        self.body = body

    def __str__(self):
        return self.body


class Element:
    name: str
    attributes: List[Attribute]
    content: ElementCollection
    count = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, name="div"):
        self.name = name
        self.attributes = []
        self.content = ElementCollection()

    def __str__(self) -> str:
        indent = self.child_indent_level()
        el = "\t" * (indent - 1)

        el += "<" + self.name
        if self.attributes:
            el += " " + " ".join([str(a) for a in self.attributes])
        el += ">"

        if not self.content:
            el += "{}"
        elif len(self.content) == 1 and not isinstance(self.content[0], Element):
            el += str(self.content[0])
        else:
            for c in self.content:
                el += "\n" + ("\t" * indent) + str(c)
            el += "\n" + ("\t" * (indent - 1))

        return el + "</" + self.name + ">"

    def set_content(self, value):
        self.content = ElementCollection(value)

    def set_name(self, value):
        self.name = value

    def set_attribute(self, name: str, values: list):
        for attr in self.attributes:
            if attr.name == name:
                attr.values = values
                return

        self.attributes.append(Attribute(name, values))

    def add_to_attribute(self, name, value):
        for attr in self.attributes:
            if attr.name == name:
                attr.values.append(value)
                return

        self.attributes.append(Attribute(name, [value]))

    def set_count(self, value):
        self.count = int(value)

    def child_indent_level(self):
        return 1


class Attribute:
    name: str
    values: List[str]

    def __init__(self, name, values=[]):
        self.name = name
        self.values = values

    def __str__(self) -> str:
        attribute = self.name
        value = self.get_value()
        if value:
            attribute += '="' + value + '"'
        return attribute

    def get_value(self) -> Optional[str]:
        return " ".join(self.filter_values())

    def filter_values(self):
        return [v for v in self.values if v and not v.isspace()]
