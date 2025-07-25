
from alx.html import ALXhtml

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