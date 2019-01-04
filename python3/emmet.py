from __future__ import annotations
from typing import List, Optional, Union
import re
import string


class Element:
    name: str
    attributes: List[Attribute]
    content: List[Union[Element, str]]

    def __init__(self):
        self.attributes = []
        self.content = []

    def __str__(self) -> str:
        el = "<" + self.name

        if self.attributes:
            el += " " + " ".join([str(a) for a in self.attributes])

        el += ">"

        if self.content:
            pass
        else:
            el += "{}"

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


class Parser:
    input: str
    # elements: List[Element]

    def __init__(self, input):
        self.input = input
        # self.elements = []

    def extract_element_name(self, tap):
        """Extract the element name if it comes first, otherwise use 'div' as name"""
        regex = re.compile(r"^([A-Za-z0-9-]+)")
        match = regex.match(self.input)
        self.input = regex.sub("", self.input)

        tap(match.group(1)) if match else tap("div")
        return True

    def extract_pattern(self, pattern, tap):
        regex = re.compile(pattern)
        match = regex.match(self.input)
        if match:
            self.input = regex.sub("", self.input)
            tap(match.group(1))
        return bool(match)

    def extract_class(self, tap):
        """Extract a class name from the input if it comes first"""
        return self.extract_pattern(r"^\.([A-Za-z0-9-_:]+)", tap)

    def extract_id(self, tap):
        """Extract the id from the input if it comes first"""
        return self.extract_pattern(r"^#([A-Za-z0-9-_:]+)", tap)


def expand_abbreviation(input: str) -> str:
    el = Element()
    parser = Parser(input)

    parser.extract_element_name(lambda name: el.set_name(name))

    while parser.input:
        if parser.extract_class(lambda name: el.add_to_attribute("class", name)):
            continue

        if parser.extract_id(lambda name: el.set_attribute("id", [name])):
            continue

        # extract custom attributes...
        # extract content...

        # stop parsing when unrecognized content was found
        break

    return add_tabstops(str(el))


def add_tabstops(html: str):
    placeholder_count = sum(
        1 for x in string.Formatter().parse(html) if x[1] is not None
    )
    tabstops = map(lambda i: "$" + str(i), range(1, placeholder_count))
    return html.format(*tabstops, "$0")
