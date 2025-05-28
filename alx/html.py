#
# html.py - implements an easy to use html creator making code more
# readable
#
# Author: Andrew Lister
# Date: September 2019
from alx.app import ALXapp
from typing import Any


class ALXhtml:
    end_html = "</html>\n"
    end_head = "</head>\n"
    end_body = "</body>\n"

    def __init__(self, title: str = None) -> None:
        """
        An HTML module to simplify the creation of HTML through the use of
        methods.  This makes the code calling the library much more readable

        :param title: The title to use in the head section of the html
        """
        self.config = ALXapp.read_lib_config()
        """Adds the configuration read from `alx.ini`"""
        self.logger = ALXapp.logger
        """The default logger from the alx.app.ALXapp.logger"""
        self.css = "\n" + self.config.get('html', 'css') + "\n"
        """Stores the css read from the ini file.  More styles can be added with `set_css`"""
        self.head = "<head>\n"
        """Initialise the `head` with `title` if specified"""
        if title:
            self.head += "<title>" + title + "</title>\n"
        self.html = "<html>\n"
        """Initialise the `html` text"""
        self.body = "<body>\n"
        """Initialise the `body` text"""
        self.column_headings = []
        """Holds column indexes that should be treated as headings.
        For example, to mark the first column as a heading, set to 
        [True] through `html.set_column_headings`"""
        self._current_row = 0
        """Internal variable to hold current row number"""
        self._current_column = 0
        """Internal variable to hold current column number"""
        self.column_alignments = []
        """Holds column index alignments to treat alignments
        differently to `self.css`. For example, to set the
         alignemnt of the first column to left call 
         `html.set_column_alignments(["left"])`"""


    def set_css(self, css: str) -> None:
        """
        Allow the default css to be overridden if necessary

        :param css: A block of css. The `style` tags should not be included
        """

        self.css = "\n" + css + "\n"

    def add_heading(self, number: int, heading: str) -> None:
        """
        adds a heading of level 'number'.  This method should likely
        be accessed by the helper functions - `add_h1`, `add_h2`, etc.

        :param number: The heading level
        :param heading: The text for the heading
        """
        self.body += "<h%d>" % number + heading + "</h%d>\n" % number

    def add_h1(self, heading: str) -> None:
        """
        Adds level 1 heading

        :param heading: The text for the header
        """
        self.add_heading(1, heading)

    def add_h2(self, heading: str) -> None:
        """
        Adds level 2 heading

        :param heading: The text for the header
        """
        self.add_heading(2, heading)

    def add_h3(self, heading: str) -> None:
        """
        Adds level 3 heading

        :param heading: The text for the header
        """
        self.add_heading(3, heading)

    def add_h4(self, heading: str) -> None:
        """
        Adds level 4 heading

        :param heading: The text for the header
        """
        self.add_heading(4, heading)

    def add_h5(self, heading: str) -> None:
        """
        Adds level 5 heading

        :param heading: The text for the header
        """
        self.add_heading(5, heading)

    def add_horizontal_line(self) -> None:
        """
        Adds a horizontal line
        """
        self.body += "<hr>\n"

    def add_paragraph(self, paragraph: str) -> None:
        """
        Adds a paragraph of text

        :param paragraph: The text for the paragraph
        """
        self.body += "<p>\n" + paragraph

    def add_bold_text(self, text: str) -> None:
        """
        Add some text in bold

        :param text: The text to add
        """
        self.body += "<b>" + text + "</b>"

    def add_italic_text(self, text: str) -> None:
        """
        Add some text in italics

        :param text: The text to add
        """
        self.body += "<i>" + text + "</i>"

    def add_bold_italic_text(self, text: str) -> None:
        """
        Add some text in bold italics

        :param text: The text to add
        """
        self.body += "<b><i>" + text + "</i></b>"

    def add_ul(self) -> None:
        """
        Adds an unordered list.  Finish with `end_ul`
        """
        self.body += "<ul>\n"

    def add_ol(self, tag: str = '1') -> None:
        """
        Adds an ordered list.  Finish with `end_ol`
        :param tag: The tag type:
        * "1": The list items will be numbered with numbers (default)
        * "A": The list items will be numbered with uppercase letters
        * "a": The list items will be numbered with lowercase letters
        * "I": The list items will be numbered with uppercase Roman numerals
        * "i": The list items will be numbered with lowercase Roman numerals
        """
        self.body += "<ol type='%s'>\n" % tag

    def add_item(self, item: str) -> None:
        """
        Adds an item to the ordered or unordered list

        :param item: The line item
        """
        self.body += "  <li>" + item + "</li>\n"

    def end_ol(self) -> None:
        """
        Ends the ordered list
        """
        self.body += "</ol>\n"

    def end_ul(self) -> None:
        """
        Ends the unordered list
        """
        self.body += "</ul>\n"

    def add_table(self, style: str = None) -> None:
        """
        Adds a table to the html

        :param style: Adds an optional style to the table.  Do not include the `style` tags
        """
        self.body += "<table"
        if style:
            self.body += " style='%s'" % style
        self.body += ">\n"
        self._current_row = self._current_column = 0

    def set_column_headings(self, headings: list = [True]) -> None:
        """
        Set columns to be headings (bold / different background) for each
        column where the list element is True

        :param headings: A list of boolean values marking a column as a
            heading.  By default, the first column is set
        :return: None
        """
        self.column_headings = headings

    def set_column_alignments(self, alignments: list = ["left"]) -> None:
        """
        Set column alignments to the values in `alignments`

        :param alignments: A list of str values marking the justification of a
        column: "left", "center" or "right".  If a list element is not set
        then the `self.css` rules are followed. By default, the first column is
         set to left justified
        :return: None
        """
        self.column_alignments = alignments

    def start_row(self, style: str = None) -> None:
        """
        Start a new row in the current table

        :param style: The css style to use.
        :return: None
        """
        if not style:
            self.body += "  <tr>\n"
        else:
            self.body += "  <tr style='%s'>\n" % style

    def add_cell(self, value: Any, tag: str = 'd', style: str = "") -> None:
        """
        Add a single cell to the current table

        :param value: This can be of any type, it will be converted to a string
        :param tag: Can be set to 'h' to create a heading
        :param style: A css style for the cell.  Do not include the `style` tags
        """
        if (self._current_column < len(self.column_headings) and
                self.column_headings[self._current_column]):
            tag = 'h'
        if (self._current_column < len(self.column_alignments) and
                self.column_alignments[self._current_column]):
            style += ("text-align: %s; " %
                      self.column_alignments[self._current_column].lower())

        if not style:
            self.body += "    <t%s>%s</t%s>\n" % (tag, str(value), tag)
        else:
            self.body += "    <t%s style='%s'>%s</t%s>\n" % (tag, style, str(value), tag)
        self.logger.debug("Row: %d, Column: %d (%s)", self._current_row,
                          self._current_column, str(value))
        self._current_column += 1

    def add_cells(self, values: list, tag: str = 'd', style: str = "") -> None:
        """
        Add a list of cells, possibly to a partial row
        :param values: A list of values to add.  Elements can be of any type
        :param tag: The tag: either 'd' or 'h'. Default is 'd'
        :param style: A css style for the cells
        :return: None
        """
        for v in values:
            self.add_cell(v, tag, style)

    def end_row(self) -> None:
        """
        End the current row in the current table
        """
        self.body += "  </tr>\n"
        self._current_row += 1
        self._current_column = 0

    def add_row(self, values: list, tag: str = "d", style: str = ""):
        """
        Add a whole row to a table.  The values passed in should be a
        list of values that make up the complete row

        :param values: A list of values
        :param tag: The tag for the row - 'h' or 'd'
        :param style: a css style for the row (do not include `style` tags)
        """

        self.start_row(style)
        for value in values:
            self.add_cell(value, tag, style)
            # self.body += "    <t%s>" % tag + str(td) + "</t%s>\n" % tag
        self.end_row()

    def add_headings(self, values: list) -> None:
        """
        Calls `add_row` with a tag of `h` and passes `values` to
        :param values: a list of values to be used as headings
        """
        self.add_row(values, "h")

    def end_table(self) -> None:
        """
        End the current table with a `/table` tag.  Not ending the table can
        lead to unexpected results!
        """
        self.body += "</table>\n"

    def add_html(self, html: str) -> None:
        """
        Add raw html to the class

        :param html: The raw html
        """
        self.body += html + "\n"

    def add_url(self, target: str, text: str = None) -> None:
        """
        Add a url to the object that will be displayed as a clickable link
        :param target: The target address or URL
        :param text: The text to display for the link. If ommitted, the target
            name is used
        """
        if not text:
            text = target
        self.body += "<a href='%s'>%s</a>\n" % (target, text)

    def get_html(self) -> str:
        """
        Put all the elements together and return a formatted html document

        :return: The html value in the object
        """
        html = self.html
        html += self.head
        html += "<style>" + self.css + "\n</style>\n"
        html += self.end_head
        html += self.body
        html += self.end_body
        html += self.end_html

        return html


if __name__ == "__main__":
    html = ALXhtml("HTML test")

    html.add_h1("Here is a heading 1")

    p = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
    html.add_paragraph(p)
    html.add_h2("Here is a heading 2")
    html.add_paragraph(p)

    html.add_ul()
    html.add_item("Item 1")
    html.add_item("Item 2")
    html.add_item("Item 3")
    html.add_item("Item 4")
    html.end_ul()

    html.add_ol()
    html.add_item("Item 1")
    html.add_item("Item 2")
    html.add_item("Item 3")
    html.add_item("Item 4")
    html.end_ol()

    html.add_table()
    html.set_column_headings()
    html.set_column_alignments(["left", "center", "right"])
    html.add_headings(['heading 1', 'heading 2', 'heading 3', 'heading 4'])
    for r in range(1, 5):
        row = []
        for c in range(1, 5):
            row.append('column %d' % c)
        html.add_row(row)
    html.end_table()

    doc = html.get_html()

    print(doc)
