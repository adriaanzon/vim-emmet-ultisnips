from abc import ABC, abstractmethod
from collections import UserList
from collections.abc import MutableMapping, Sequence


class NodeCollection(UserList):
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
        return "\n".join([line for node in self.data for line in node.to_list()])


class Node(ABC):
    repeat = 1
    # an "nth" property may be needed when supporting the ($) operator

    def set_repeat(self, value):
        self.repeat = int(value)

    @abstractmethod
    def to_list(self):
        """Get each line of the node's string representation."""
        pass

    def __str__(self):
        return "\n".join(self.to_list())


class Text(Node):
    def __init__(self, body=""):
        self.body = body

    def to_list(self):
        return [self.body] * self.repeat


class Element(Node):
    def __init__(self, name="div"):
        self.name = name
        self.attributes = []  # type: List[Attribute]
        self.content = NodeCollection()

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
        self.content = NodeCollection(value)

    def set_name(self, value):
        self.name = value

    def set_attribute(self, name, values):
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

    def replace_or_add_attribute(self, new_attribute):
        for index, a in enumerate(self.attributes):
            if a.name == new_attribute.name:
                self.attributes[index] = new_attribute
                return

        self.attributes.append(new_attribute)


class AttributeCollection(MutableMapping):
    """List of attributes. Attributes are accessed by their name."""

    def __init__(self, data=None):
        if data is None:
            self.data = []
        elif isinstance(data, list):
            self.data = data
        else:
            raise TypeError("Underlying data must be a list of Attributes")

    def __getitem__(self, name):
        for attribute in self.data:
            if attribute.name == name:
                return attribute
        raise KeyError("'{}' object has no attribute '{}'".format(self.__class__, name))

    def __setitem__(self, name, value):
        if isinstance(value, Attribute):
            if name != value.name:
                raise TypeError("Key name doesn't match with Attribute name")
        else:
            value = Attribute(name, value)

        for index, attribute in enumerate(self.data):
            if attribute.name == name:
                self.data[index] = value
                return
        self.data.append(value)

    def __delitem__(self, name):
        for index, attribute in enumerate(self.data):
            if attribute.name == name:
                del self.data[index]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


class Attribute:
    def __init__(self, name, values=[]):
        self.name = name
        self.values = [values] if isinstance(values, str) else values

    def __str__(self):
        attribute = self.name
        value = self.get_value()
        if value:
            attribute += '="' + value + '"'
        return attribute

    def get_value(self):
        return " ".join(self.filtered_values())

    def filtered_values(self):
        return [v for v in self.values if v and not v.isspace()]
