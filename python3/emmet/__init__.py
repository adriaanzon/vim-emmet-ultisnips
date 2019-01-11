from __future__ import annotations
import string
from emmet.element import Element, ElementCollection
from emmet.parser import Parser


def expand_abbreviation(input: str) -> str:
    elements = ElementCollection()
    el = Element()
    elements.append(el)
    parser = Parser(input)

    parser.extract_element_name(lambda name: el.set_name(name))

    while parser.input:
        if parser.extract_class(lambda name: el.add_to_attribute("class", name)):
            continue

        if parser.extract_id(lambda name: el.set_attribute("id", [name])):
            continue

        # extract custom attributes...
        # extract content...

        if parser.extract_repeat(lambda times: el.set_count(times)):
            continue

        # stop parsing when unrecognized content was found
        break

    # TODO: add __str__ method on ElementCollection
    return add_tabstops("\n".join([str(el) for el in elements]))


def add_tabstops(html: str):
    placeholder_count = sum(
        1 for x in string.Formatter().parse(html) if x[1] is not None
    )
    tabstops = map(lambda i: "$" + str(i), range(1, placeholder_count))
    return html.format(*tabstops, "$0")
