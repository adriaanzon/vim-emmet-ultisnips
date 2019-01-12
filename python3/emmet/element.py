from __future__ import annotations
from typing import List, Optional
from collections.abc import Sequence
from collections import UserList
from abc import ABC, abstractmethod


class ElementCollection(UserList):
    data: List[Node]

    def __init__(self, data=None):
        if isinstance(data, self.__class__):
            self.data = data.data[:]
        elif isinstance(data, Sequence):
            self.data = list(data)
        elif data is not None:
            self.data = [data]
        else:
            self.data = []

    def __str__(self):
        return "\n".join([str(node) for node in self.data])


class Node(ABC):
    @abstractmethod
    def to_list(self):
        """Get each line of the node's string representation."""
        pass

    def __str__(self):
        return "\n".join(self.to_list())


class Text(Node):
    body: str
    repeat = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, body=""):
        self.body = body

    def to_list(self):
        return [self.body] * self.repeat


class Element(Node):
    name: str
    attributes: List[Attribute]
    content: ElementCollection
    repeat = 1
    # an "nth" property may be needed when supporting the ($) operator

    def __init__(self, name="div"):
        self.name = name
        self.attributes = []
        self.content = ElementCollection()

    def to_list(self):
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
                lines += c.to_list()
            lines.append(tag_end)

        lines[1:-1] = map(lambda intermediate: "\t" + intermediate, lines[1:-1])

        return lines * self.repeat

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
        return " ".join(self.filtered_values())

    def filtered_values(self):
        return [v for v in self.values if v and not v.isspace()]
