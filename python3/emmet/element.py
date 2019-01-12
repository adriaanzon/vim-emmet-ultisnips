from __future__ import annotations
from typing import List, Optional, Union
from collections.abc import Sequence


class ElementCollection:
    items: List[Union[Element, Text]]

    def __init__(self, items=None):
        if isinstance(items, self.__class__):
            self.items = items.items
        elif isinstance(items, Sequence):
            self.items = list(items)
        elif items is not None:
            self.items = [items]
        else:
            self.items = []

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def append(self, value):
        self.items.append(value)

    def __str__(self):
        return "\n".join([str(item) for item in self.items])


class Text:
    body: str
    repeat = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, body=""):
        self.body = body

    def to_string_lines(self):
        return [self.body] * self.repeat

    def __str__(self):
        return "\n".join(self.to_string_lines())


class Element:
    name: str
    attributes: List[Attribute]
    content: ElementCollection
    repeat = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, name="div"):
        self.name = name
        self.attributes = []
        self.content = ElementCollection()

    def to_string_lines(self):
        lines = []
        tag_start = "<" + self.name
        if self.attributes:
            tag_start += " " + " ".join([str(a) for a in self.attributes])
        tag_start += ">"
        tag_end = "</" + self.name + ">"

        lines.append(tag_start)

        if not self.content:
            lines[-1] += "{}" + tag_end
        elif len(self.content) == 1 and not isinstance(self.content[0], Element):
            lines[-1] += str(self.content[0]) + tag_end
        else:
            for c in self.content:
                lines += c.to_string_lines()
            lines.append(tag_end)

        lines[1:-1] = map(lambda intermediate: "\t" + intermediate, lines[1:-1])

        return lines * self.repeat

    def __str__(self) -> str:
        return "\n".join(self.to_string_lines())

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

    def set_repeat(self, value):
        self.repeat = int(value)


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
