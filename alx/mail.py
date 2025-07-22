import os.path
import socket
from time import sleep
import re
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPDataError, SMTPHeloError, \
    SMTPNotSupportedError, SMTPRecipientsRefused, SMTPResponseException, SMTPSenderRefused, SMTPServerDisconnected
import mimetypes
from alx.html import ALXhtml
import smtplib
from email.message import EmailMessage, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Optional


class ALXmail(ALXhtml):
    def __init__(self, mail_type: str = "html") -> None:
        """
        Class to send itrs_email - both text and html (default). It is a subclass
        of `ALXhtml` to allow simple html mail composition. Configuration
        is stored in `alx.ini`

        :param type: Either 'text' or 'html' (default)
        :return: None
        """
        super().__init__()

        self.mail_type = mail_type
        """The type of the email - 'text' or 'html'. Default is html"""

        if mail_type == "plain":
            self.body = ""
            self.message = EmailMessage()
            """The message as a plain or MIME multipart instance"""
        elif mail_type == "html":
            self.message = MIMEMultipart()
        else:
            raise TypeError("Only 'plain' and 'html' are supported")

        self.sender = self.config.get("mail", "from")
        """The email sender"""
        self.subject = "No subject"
        """The email subject"""
        self.server = None
        """The smtp server object"""
        self.images = 0
        """Used for naming multiple image attachments"""
        self.mailhost = self.config.get("mail", "server")
        """The hostname of the smtp server. Configured in alx.ini"""
        self.recipients = []
        """A list of recipients"""
        self.cc = []
        """A list of those on the cc list"""
        self.bcc = []
        """A list of those on the bcc list"""
        self.attachments = []
        """A list of attachments"""

    def set_from(self, sender: str) -> None:
        """
        Set the address and name of sender
        :param sender: The name and email address of the sender: 'First Last <sender@example.com>'
        """
        self.sender = sender

    def set_subject(self, subject: str) -> None:
        """
        Sets the subject of the message
        :param subject: The subject
        """
        self.subject = subject

    def add_recipient(self, to: str, recipient_type: str = "to") -> None:
        """
        Adds a recipient of the message to the list of recipients
        :param to: a single email address
        :param recipient_type: The recipent type: 'to', 'cc', or 'bcc'
        """
        if recipient_type == "to":
            self.recipients.append(to)
        elif recipient_type == "cc":
            self.cc.append(to)
        elif recipient_type == "bcc":
            self.bcc.append(to)

    def set_recipients(self, to: Union[str, list], recipient_type = "to") -> None:
        """
        Sets the list of recipients for the email
        :param to: A list or string of recipients, separated by ' ', ',' or ';'
        :param recipient_type: The recipent type: 'to', 'cc', or 'bcc'. This
         parameter is generally not needed as the helper functions should be used
        """

        if type(to) is list:
            recipients = to
        else:
            recipients = re.split(r"[,\s;]+", to)

        for to in recipients:
            self.add_recipient(to, recipient_type)

    def add_cc(self, cc: str) -> None:
        """
        Adds a cc recipient or list of recipients

        :param cc: A list or string of recipients, separated by ' ', ',' or ';'
        """
        self.set_recipients(cc, "cc")

    def add_bcc(self, bcc: str) -> None:
        """
        Adds a bcc recipient or list of recipients

        :param bcc: A list or string of recipients, separated by ' ', ',' or ';'
        """
        self.set_recipients(bcc, "bcc")

    def set_body(self, body: str) -> None:
        self.body = body

    def add_paragraph(self, p: str) -> None:
        if self.mail_type == "html":
            super().add_paragraph(p)
        else:
            self.body += "\n" + p + "\n"

    def add_text(self, t: str) -> None:
        if self.mail_type == "html":
            super().add_paragraph(t)
        else:
            self.body += t + "\n"

    def add_attachment(self, filename: str) -> str:
        """
        Adds a file as an attachment

        :param filename: the full path to the file to attach
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        cd = 'attachment'   # Content-Disposition
        content_id = ""
        fn = os.path.basename(filename)
        with open(filename, "rb") as fp:
            data = fp.read()

        maintype, subtype = mimetypes.guess_type(filename)
        if maintype and maintype.startswith('image'):
            attachment = MIMEImage(data)
            if self.mail_type == 'html':
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

    def send(self) -> None:
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

        if self.mail_type == 'html':
            body = self.get_html()
        else:
            body = self.body + "\n"

        part = MIMEText(body, self.mail_type)
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

    def get_mime_message(self) -> Message:
        """
        Builds and returns the MIME message without sending it.
        Used for testing and inspection.
        """
        if self.mail_type == "plain":
            from email.message import EmailMessage
            msg = EmailMessage()
            msg.set_content(self.body)
        else:
            msg = MIMEMultipart()
            for a in self.attachments:
                msg.attach(a)
            msg.attach(MIMEText(self.get_html(), "html"))

        msg["From"] = self.sender
        msg["To"] = ", ".join(self.recipients)
        msg["Subject"] = self.subject
        if self.cc:
            msg["Cc"] = ", ".join(self.cc)
        if self.bcc:
            msg["Bcc"] = ", ".join(self.bcc)

        return msg