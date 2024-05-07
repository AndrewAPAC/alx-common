import time

from alx.app import ALXApp
from alx.html import ALXhtml
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ALXmail(ALXhtml):
    def __init__(self, type="html"):
        """
        class to send itrs_email - both text and html (default).  It is a subclass
        of `ALXhtml` to allow simple html mail composition.  configuration
        is stored in `alx.ini`

        :param type: either 'plain' or 'html' (default)
        :return: None
        """
        super().__init__()

        self.type = type

        if type == "plain":
            self.body = ""
        elif type != "html":
            raise TypeError("Only 'plain' and 'html' are supported")

        self.sender = self.config.get("mail", "from")
        self.mailhost = self.config.get("mail", "server")
        self.recipients = []
        self.cc = []
        self.bcc = []
        self.attachments = []
        self.message = MIMEMultipart()

    def set_from(self, sender):
        self.sender = sender

    def set_subject(self, subject):
        self.subject = subject

    def add_recipient(self, to):
        self.recipients.append(to)

    def add_cc(self, to):
        self.cc.append(to)

    def add_bcc(self, to):
        self.bcc.append(to)

    def set_body(self, body):
        self.body = body

    def add_paragraph(self, p):
        if self.type == "html":
            super().add_paragraph(p)
        else:
            self.body += "\n" + p + "\n"

    def add_text(self, t):
        if self.type == "html":
            super().add_paragraph(t)
        else:
            self.body += t + "\n"

    def add_attachment(self, filename):
        raise NotImplementedError

    def send(self):
        self.message["From"] = self.sender
        self.message["Subject"] = self.subject
        self.message["To"] = ", ".join(self.recipients)
        if len(self.cc) > 0:
            self.message["Cc"] = ", ".join(self.cc)
        if len(self.bcc) > 0:
            self.message["Bcc"] = ", ".join(self.bcc)

        for a in self.attachments:
            pass

        all = self.recipients + self.cc + self.bcc

        if self.type == 'html':
            body = self.get_html()
        else:
            body = self.body + "\n"

        part = MIMEText(body, self.type)
        self.message.attach(part)
        self.server = smtplib.SMTP(self.mailhost)
        self.server.sendmail(self.sender, all, self.message.as_string())
        self.server.quit()


if __name__ == "__main__":
    mail = ALXmail("html")
    mail.set_subject("test html itrs_email")
    mail.add_recipient("a.lister.hk@gmail.com")
    mail.add_bcc("andrew.lister@outlook.co.id")
    mail.add_h1("Here is a heading 1")

    p = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
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

    mail.send()
