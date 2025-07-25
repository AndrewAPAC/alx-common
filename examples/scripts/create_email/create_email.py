
from alx.mail import ALXmail

mail = ALXmail("html")
mail.set_subject("test html email")
mail.add_recipient("mickey.mouse@disney.com")
mail.add_h1("Here is a heading 1")

p = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt....
"""
mail.add_paragraph(p)
mail.add_h2("Here is a heading 2")
mail.add_paragraph(p)

mail.add_ul()
mail.add_item("Item 1")
mail.add_item("Item 2")
mail.add_item("Item 3")
mail.add_item("Item 4")
mail.end_ul()

mail.add_attachment("/etc/resolv.conf")

mail.add_url("https://www.google.com", "Open google search")

mail.add_ol()
mail.add_item("Item 1")
mail.add_item("Item 2")
mail.add_item("Item 3")
mail.add_item("Item 4")
mail.end_ol()

mail.add_table()
mail.add_headings(['heading 1', 'heading 2', 'heading 3', 'heading 4'])
for r in range(1, 5):
    row = []
    for c in range(1, 5):
        row.append('column %d' % c)
    mail.add_row(row)
mail.end_table()

print(mail._get_mime_message())

mail = ALXmail("plain")
mail.set_subject("test plain email")
mail.add_recipient("mickey.mouse@disney.com")
mail.add_paragraph("A boring plain text email")
mail.add_paragraph("--\nMickey Mouse\nPh: (555) 123 4567")

print(mail._get_mime_message())
