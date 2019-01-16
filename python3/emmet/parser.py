import re

from emmet.node import Attribute, Element, Text


class Parser:
    """
    Parser which extracts patterns from emmet abbreviations.

    Each "extract" method accepts a "tap" callback as a parameter, which will be called
    with the result of the parse, only if there was a match. The type of the parse
    result varies per "extract" method.
    """

    def __init__(self, input):
        self.input = input

    def extract_element(self, tap):
        """Extract the element name if it comes first, otherwise use 'div' as name"""
        regex = re.compile(r"^([A-Za-z0-9-]+)")
        match = regex.match(self.input)
        self.input = regex.sub("", self.input)

        tap(Element(match.group(1) if match else "div"))
        return match

    def extract_pattern(self, pattern, tap=lambda: None):
        regex = re.compile(pattern)
        match = regex.match(self.input)
        if match:
            self.input = regex.sub("", self.input)
            tap(*match.groups())
        return match

    def extract_class_name(self, tap):
        """Extract a class name from the input if it comes first"""
        return self.extract_pattern(r"^\.([A-Za-z0-9-_:]+)", tap)

    def extract_id(self, tap):
        """Extract the id attribute from the input if it comes first"""
        return self.extract_pattern(
            r"^#([A-Za-z0-9-_:]+)", lambda value: tap(Attribute("id", value))
        )

    def extract_text(self, tap):
        return self.extract_pattern(r"^{([^}]+)}", lambda body: tap(Text(body)))

    def extract_repeat(self, tap):
        return self.extract_pattern(r"^\*(\d+)", tap)

    def extract_child(self, tap):
        return self.extract_pattern(r"^>", lambda: self.extract_element(tap))
