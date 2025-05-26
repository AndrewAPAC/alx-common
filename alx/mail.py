import os.path
import socket
import time
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPHeloError, \
    SMTPNotSupportedError, SMTPRecipientsRefused, SMTPResponseException, SMTPSenderRefused, SMTPServerDisconnected
import mimetypes
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
        self.server = None
        self.images = 0
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
        """
        Adds a file as an attachment

        :param filename: the full path to the file to attach
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        cd = 'attachment'   # Content-Disposition
        fn = os.path.basename(filename)
        with open(filename, "rb") as fp:
            data = fp.read()

        maintype, subtype = mimetypes.guess_type(filename)
        image_ref = None
        if maintype and maintype.startswith('image'):
            attachment = MIMEImage(data)
            if self.type == 'html':
                cd = 'inline'
                image = 'image%02d' % self.images
                # The content_id is returned so the application
                # can put it where it wants
                content_id = '<img src="cid:%s" width="100%%">' % image
                self.images += 1
                attachment.add_header('Content-ID', '<%s>' % image)
        elif maintype and maintype.startswith('application'):
            attachment = MIMEApplication(data)
        elif maintype and maintype.startswith('audio'):
            attachment = MIMEAudio(data)
        else:
            data = data.decode()
            attachment = MIMEText(data)

        attachment.add_header('Content-Disposition', cd,
                              filename=fn)

        self.attachments.append(attachment)

        return content_id

    def send(self):
        self.message["From"] = self.sender
        self.message["Subject"] = self.subject
        # Remove duplicate names
        self.recipients = list(set(self.recipients))
        self.message["To"] = ", ".join(self.recipients)
        if len(self.cc) > 0:
            self.cc = list(set(self.cc))
            self.message["Cc"] = ", ".join(self.cc)
        if len(self.bcc) > 0:
            self.bcc = list(set(self.bcc))
            self.message["Bcc"] = ", ".join(self.bcc)

        for a in self.attachments:
            self.message.attach(a)

        if self.type == 'html':
            body = self.get_html()
        else:
            body = self.body + "\n"

        part = MIMEText(body, self.type)
        self.message.attach(part)

        count = 0
        loop = 20

        while count < 20:
            try:
                self.server = smtplib.SMTP(self.mailhost)
                self.server.send_message(self.message)
                self.server.quit()
                return
            except (socket.error, SMTPException, SMTPAuthenticationError,
                    SMTPConnectError, SMTPDataError, SMTPHeloError,
                    SMTPNotSupportedError, SMTPRecipientsRefused,
                    SMTPResponseException, SMTPSenderRefused,
                    SMTPServerDisconnected) as ex:
                count += 1
                if count == loop:
                    raise type(ex).__name__(format(ex))
                else:
                    sleep(5)


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

    mail.add_attachment("/etc/resolv.conf")
    mail.add_attachment("/home/andrew/GoogleDrive/FilingCabinet/Andrew/Home/Lovina/20240912.land.agreement.pdf")
    mail.add_attachment("/home/andrew/dev/alx/data/account_info/monthly_pnl.png")

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
