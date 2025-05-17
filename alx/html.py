#
# html.py - implements an easy to use html creator making code more
# readable
#
# Author: Andrew Lister
# Date: September 2019
from alx.app import ALXapp


class ALXhtml:
    end_html = "</html>\n"
    end_head = "</head>\n"
    end_body = "</body>\n"

    def __init__(self, title=None):
        """
        An HTML module to simplify the creation of HTML through the use of
        methods.  This makes the code calling the library much more readable

        :param title: The title to use in the head section of the html
        """
        self.config = ALXapp.read_lib_config()
        """Adds the configuration read from `alx.ini`"""
        self.css = "<style>\n" + self.config.get('html', 'css') + "\n</style>\n"
        """Stores the css read from the ini file.  More styles can be added with `set_css`"""
        self.head = "<head>\n"
        """Initialise the `head` with `title` if specified"""
        if title:
            self.head += "<title>" + title + "</title>\n"
        self.html = "<html>\n"
        """Initialise the `html` text"""
        self.body = "<body>\n"
        """Initialise the `body` text"""

    def set_css(self, css):
        """
        Allow the default css to be overridden if necessary

        :param css: A block of css. The `style` tags should not be included
        """

        self.css = "<style>\n" + css + "\n</style>\n"

    def add_heading(self, number, heading):
        """
        adds a heading of level 'number'.  This method should likely
        be accessed by the helper functions - `add_h1`, `add_h2`, etc.

        :param number: The heading level
        :param heading: The text for the heading
        """
        self.body += "<h%d>" % number + heading + "</h%d>\n" % number

    def add_h1(self, heading):
        """
        Adds a level 1 heading

        :param heading: The text for the header
        """
        self.add_heading(1, heading)

    def add_h2(self, heading):
        """
        Adds a level 2 heading

        :param heading: The text for the header
        """
        self.add_heading(2, heading)

    def add_h3(self, heading):
        """
        Adds a level 3 heading

        :param heading: The text for the header
        """
        self.add_heading(3, heading)

    def add_h4(self, heading):
        """
        Adds a level 4 heading

        :param heading: The text for the header
        """
        self.add_heading(4, heading)

    def add_h5(self, heading):
        """
        Adds a level 5 heading

        :param heading: The text for the header
        """
        self.add_heading(5, heading)

    def add_horizontal_line(self):
        """
        Adds a horizontal line
        """
        self.body += "<hr>\n"

    def add_paragraph(self, paragraph):
        """
        Adds a paragraph of text

        :param paragraph: The text for the paragraph
        """
        self.body += "<p>\n" + paragraph

    def add_bold_text(self, text):
        """
        Add some text in bold

        :param text: The text to add
        """
        self.body += "<b>" + text + "</b>"

    def add_italic_text(self, text):
        """
        Add some text in italics

        :param text: The text to add
        """
        self.body += "<i>" + text + "</i>"

    def add_bold_italic_text(self, text):
        """
        Add some text in bold italics

        :param text: The text to add
        """
        self.body += "<b><i>" + text + "</i></b>"

    def add_ul(self):
        """
        Adds an unordered list.  Finish with `end_ul`
        """
        self.body += "<ul>\n"

    def add_ol(self, tag='1'):
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

    def add_item(self, item):
        """
        Adds an item to the ordered or unordered list

        :param item: The line item
        """
        self.body += "  <li>" + item + "</li>\n"

    def end_ol(self):
        """
        Ends the ordered list
        """
        self.body += "</ol>\n"

    def end_ul(self):
        """
        Ends the unordered list
        """
        self.body += "</ul>\n"

    def add_table(self, style=None):
        """
        Adds a table

        :param style: adds an optional style to the table.  Do not include the `style` tags
        """
        self.body += "<table"
        if style:
            self.body += " style='%s'" % style
        self.body += ">\n"

    def start_row(self):
        """
        Start a new row in the current table
        """
        self.body += "  <tr>\n"

    def add_cell(self, value, style=None):
        """
        Add a single cell to the current table

        :param value: This can be of any type, it will be converted to a
        string
        :param style: A css style for the cell.  Do not include the `style` tags
        """
        if not style:
            self.body += "    <td>" + str(value) + "</td>\n"
        else:
            self.body += "    <td style='%s'>" % style
            self.body += str(value) + "</td>\n"

    def end_row(self):
        """
        End the current row in the current table
        """
        self.body += "  </tr>\n"

    def add_row(self, values, tag="d", style=None):
        """
        Add a whole row to a table.  The values passed in should be a
        list of values that make up the complete row

        :param values: A list of values
        :param tag: The tag for the row - 'h' or 'd'
        :param style: a css style for the row (do not include tags) like
        * `padding: 5px; font-size: 14px; text-align: left;`
        """
        if not style:
            self.body += "  <tr>\n"
        else:
            self.body += "  <tr style='%s'>\n" % style
        for td in values:
            self.body += "    <t%s>" % tag + str(td) + "</t%s>\n" % tag
        self.body += "  </tr>\n"

    def add_headings(self, values):
        """
        Calls `add_row` with a tag of `h` and passes `values` to
        :param values: a list of values to be used as headings
        """
        self.add_row(values, "h")

    def end_table(self):
        """
        End the current table with a `/table` tag.  Not ending the table can lead
        unexpected results!
        """
        self.body += "</table>\n"

    def add_html(self, html):
        """
        Add raw html to the class

        :param html: The raw html
        """
        self.body += html + "\n"

    def add_url(self, target, text):
        """
        Add a url to the object that will be displayed as a clickable link
        :param target: The target address or URL
        :param text: The text to display for the link
        """
        self.body += "<a href='%s'>%s</a>\n" % (target, text)

    def get_html(self):
        """
        Put all the elements together and return a formatted html document

        :return: The html value in the object
        """
        html = self.html
        html += self.head
        html += self.css
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
    html.add_headings(['heading 1', 'heading 2', 'heading 3', 'heading 4'])
    for r in range(1, 5):
        row = []
        for c in range(1, 5):
            row.append('column %d' % c)
        html.add_row(row)
    html.end_table()

    doc = html.get_html()

    print(doc)

