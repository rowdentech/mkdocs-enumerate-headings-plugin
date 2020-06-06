class Heading:
    def __init__(self, element, soup) -> None:
        """
        Args:
            element (bs4.element.Tag): BeautifulSoup Tag
            soup: BeautifulSoup class instance 
        """
        self.heading = element
        self.soup = soup

        # Placeholder for h1-h6 section numbers that will be filled later
        self.section_numbering = [0, 0, 0, 0, 0, 0]

    @property
    def depth(self):
        """
        Translates h1-h6 strings to integer
        """
        assert self.heading.name in ["h1", "h2", "h3", "h4", "h5", "h6"]
        return int(self.heading.name[1])

    def set_section_number(self, section_number: int, depth: int):
        self.section_numbering[depth - 1] = section_number

    def get_section_number(self, depth: int):
        return self.section_numbering[depth - 1]

    def set_chapter(self, chapter):
        # Chapter is the h1 section number.
        # Note that chapter numbers should always start at either 0 or 1
        # And then increment.
        line_chapter = self.section_numbering[0]
        if line_chapter == 0:
            new_chapter = chapter
        else:
            new_chapter = line_chapter - 1 + chapter

        self.section_numbering[0] = new_chapter

    def section_number_string(self):
        """
        Translate section numbering to a string
        
        Examples:
            # Basic heading
            [1, 0, 0, 0, 0, 0]
            #> "1."
            # Subheading
            [2, 1, 0, 0, 0, 0]
        """
        numbers = self.section_numbering

        # Remove any trailing zeros
        while numbers[-1] == 0:
            del numbers[-1]

        # Join to string
        heading_string = [str(x) for x in numbers]
        heading_string = ".".join(heading_string)

        # Add a trailing dot to level 1 headings
        # For example "1" should be "1."
        if "." not in heading_string:
            heading_string += "."

        return heading_string

    def enumerate(self, add_span_element=False):

        self.heading.string.replace_with(" " + self.heading.string)
        if add_span_element:
            span = self.soup.new_tag("span", **{"class": "enumerate-heading-plugin"})
            span.string = self.section_number_string()
            self.heading.string.insert_before(span)
        else:
            self.heading.string.insert_before(self.section_number_string())
