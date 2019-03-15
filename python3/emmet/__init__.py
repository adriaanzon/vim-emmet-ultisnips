import string

from emmet.node import NodeCollection
from emmet.parser import Parser


def expand_abbreviation(input):
    """Transform an emmet abbreviation into a snippet"""
    c = NodeCollection()
    root = c
    parser = Parser(input)

    parser.extract_element(c.append)

    while parser.input:
        if (
            parser.extract_class_name(c[-1].attributes.add_class)
            or parser.extract_id(c[-1].attributes.put)
            or parser.extract_attributes(c[-1].attributes.put)
            or parser.extract_text(c[-1].content.append)
            or parser.extract_repeat(c[-1].set_repeat)
            or parser.extract_sibling(c.append)
        ):
            continue

        if parser.extract_child(c[-1].content.append):
            c = c[-1].content
            continue

        # stop parsing when unrecognized content was found
        break

    return add_tabstops(str(root))


def add_tabstops(html):
    placeholder_count = sum(
        1 for x in string.Formatter().parse(html) if x[1] is not None
    )
    tabstops = ["$" + str(i) for i in range(1, placeholder_count)] + ["$0"]
    return html.format(*tabstops)
