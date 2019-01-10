from __future__ import annotations
from typing import List, Optional, Union


class ElementCollection:
    pass


class Element:
    name: str
    attributes: List[Attribute]
    content: List[Union[Element, str]]

    def __init__(self, name="div"):
        self.name = name
        self.attributes = []
        self.content = []

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
