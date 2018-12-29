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
    def expand_abbreviation(input: str) -> str:
        el = Element()

        # extract name
        regex = re.compile(r"^([A-Za-z0-9-]+)")
        name_match = regex.match(input)
        input = regex.sub("", input)

        if name_match:
            el.name = name_match.group(1)
        else:
            el.name = "div"

        while input:
            # extract classes...
            regex = re.compile(r"^\.([A-Za-z0-9-_:]+)")
            match = regex.match(input)
            input = regex.sub("", input)
            if match:
                el.add_to_attribute("class", match.group(1))
                continue

            # extract ids...
            regex = re.compile(r"^#([A-Za-z0-9-_:]+)")
            match = regex.match(input)
            input = regex.sub("", input)
            if match:
                el.set_attribute("id", [match.group(1)])
                continue

            # extract custom attributes...
            # extract content...

            # stop parsing when unrecognized content was found
            break

        return Parser.add_tabstops(str(el))

    def add_tabstops(html: str):
        placeholder_count = sum(
            1 for x in string.Formatter().parse(html) if x[1] is not None
        )
        tabstops = map(lambda i: "$" + str(i), range(1, placeholder_count))
        return html.format(*tabstops, "$0")
