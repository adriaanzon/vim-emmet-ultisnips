import re


class Parser:
    def __init__(self, input):
        self.input = input

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

    def extract_text(self, tap):
        return self.extract_pattern(r"^{([^}]+)}", tap)

    def extract_repeat(self, tap):
        return self.extract_pattern(r"^\*(\d+)", tap)

    def extract_child(self, tap):
        return self.extract_pattern(r"^(>)", lambda _: self.extract_element_name(tap))
