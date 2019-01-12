from __future__ import annotations
import string
from emmet.element import Element, ElementCollection
from emmet.parser import Parser


def expand_abbreviation(input: str) -> str:
    e = ElementCollection(Element())
    parser = Parser(input)

    parser.extract_element_name(lambda name: e[-1].set_name(name))

    while parser.input:
        if parser.extract_class(lambda name: e[-1].add_to_attribute("class", name)):
            continue

        if parser.extract_id(lambda name: e[-1].set_attribute("id", [name])):
            continue

        # extract custom attributes...
        # extract content...

        if parser.extract_repeat(lambda times: e[-1].set_repeat(times)):
            continue

        # if parser.extract_nest(lambda name: e.append(Element(name))):
        #     pass

        # stop parsing when unrecognized content was found
        break

    return add_tabstops(str(e))


def add_tabstops(html: str):
    placeholder_count = sum(
        1 for x in string.Formatter().parse(html) if x[1] is not None
    )
    tabstops = map(lambda i: "$" + str(i), range(1, placeholder_count))
    return html.format(*tabstops, "$0")
