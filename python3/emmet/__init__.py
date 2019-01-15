import string
from emmet.node import Element, NodeCollection, Text
from emmet.parser import Parser


def expand_abbreviation(input):
    """Transform an emmet abbreviation into a snippet"""
    c = NodeCollection(Element())
    root = c
    parser = Parser(input)

    parser.extract_element_name(lambda name: c[-1].set_name(name))

    while parser.input:
        if parser.extract_class(lambda name: c[-1].add_to_attribute("class", name)):
            continue

        if parser.extract_id(lambda name: c[-1].set_attribute("id", [name])):
            continue

        # extract custom attributes...

        if parser.extract_text(lambda body: c[-1].content.append(Text(body))):
            continue

        if parser.extract_repeat(lambda times: c[-1].set_repeat(times)):
            continue

        if parser.extract_child(lambda name: c[-1].content.append(Element(name))):
            c = c[-1].content
            continue

        # stop parsing when unrecognized content was found
        break

    return add_tabstops(str(root))


def add_tabstops(html):
    placeholder_count = sum(
        1 for x in string.Formatter().parse(html) if x[1] is not None
    )
    return html.format(*["$" + str(i) for i in range(1, placeholder_count)] + ["$0"])
