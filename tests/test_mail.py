# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# pytest routines for alx.itrs.mail

import pytest
import os
import platform
from unittest.mock import patch, MagicMock
from alx.mail import ALXmail
from email.message import EmailMessage


def test_plain_email_body():
    mail = ALXmail(mail_type="plain")
    mail.set_from("sender@example.com")
    mail.add_recipient("recipient@example.com")
    mail.set_subject("Test Email")
    mail.add_paragraph("This is a test email.")

    msg = mail._get_mime_message()

    assert msg.get_content_type() == "text/plain"
    assert "This is a test email." in msg.get_payload()

def test_html_body_rendering():
    mail = ALXmail()
    mail.set_from("sender@example.com")
    mail.add_recipient("recipient@example.com")
    mail.set_subject("HTML Test")
    mail.add_html("<h1>This is HTML</h1>")

    msg = mail._get_mime_message()
    html_found = False
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_found = True
            assert "<h1>This is HTML</h1>" in part.get_payload()
    assert html_found, "HTML part not found"


@pytest.mark.skipif(platform.system() == "Windows", reason="File path differs on Windows")
def test_attachment_addition_unix(tmp_path):
    mail = ALXmail()
    mail.set_from("a@b.com")
    mail.add_recipient("b@c.com")
    mail.set_subject("Attachment Test")

    test_file = "/etc/resolv.conf"
    if not os.path.exists(test_file):
        pytest.skip("/etc/resolv.conf not found")

    mail.add_attachment(test_file)
    msg = mail._get_mime_message()

    filenames = [part.get_filename() for part in msg.walk() if part.get_filename()]
    assert "resolv.conf" in filenames


def test_binary_attachment(tmp_path):
    mail = ALXmail()
    mail.set_from("a@b.com")
    mail.add_recipient("b@c.com")
    mail.set_subject("Binary Attachment Test")

    binary_path = tmp_path / "test.png"
    binary_path.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00")  # Fake PNG header

    mail.add_attachment(str(binary_path))
    msg = mail._get_mime_message()

    found = any(part.get_filename() == "test.png" for part in msg.walk())
    assert found, "Binary attachment not found"


def test_send_plain_email(monkeypatch):
    """Ensure plain text emails use set_content and do not create multipart payloads."""
    mail = ALXmail(mail_type="plain")
    mail.set_from("sender@example.com")
    mail.add_recipient("recipient@example.com")
    mail.set_subject("Send Plain Test")
    mail.add_paragraph("Plain body line 1")
    mail.add_paragraph("Plain body line 2")

    sent_messages = {}

    class DummySMTP:
        def __init__(self, host, port=25, timeout: int = None):
            self.host = host
            self.port = port
        def send_message(self, msg):
            # Capture the outgoing message
            sent_messages["msg"] = msg
        def quit(self):
            pass

    monkeypatch.setattr("smtplib.SMTP", DummySMTP)

    mail.send()

    # Check that the message was captured
    msg: EmailMessage = sent_messages["msg"]
    assert msg.get_content_type() == "text/plain"
    payload = msg.get_payload()
    assert "Plain body line 1" in payload
    assert "Plain body line 2" in payload
    # Make sure it wasn't turned into multipart
    assert not msg.is_multipart()


# ---------------------------------------------------------------------------
# test_connection() — validates connect/STARTTLS/login sequencing without
# sending a message. smtplib.SMTP is mocked throughout; no real network I/O.
# ---------------------------------------------------------------------------

def _mailer(mail_type="html", tls=False, user="", password=""):
    mail = ALXmail(mail_type=mail_type)
    mail.set_smtp_server("smtp.example.com")
    mail.set_smtp_port(587)
    mail.set_tls(tls)
    mail.set_smtp_credentials(user, password)
    return mail


def test_connection_uses_configured_host_and_port(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)

    mail = _mailer()
    mail.set_smtp_server("mail.internal")
    mail.set_smtp_port(2525)

    assert mail.test_connection() is True
    mock_smtp.assert_called_once_with("mail.internal", 2525, timeout=10)


def test_connection_no_tls_no_auth_skips_starttls_and_login(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value

    _mailer(tls=False, user="").test_connection()

    server.ehlo.assert_called_once()
    server.starttls.assert_not_called()
    server.login.assert_not_called()
    server.quit.assert_called_once()


def test_connection_tls_triggers_starttls_and_second_ehlo(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value

    _mailer(tls=True).test_connection()

    server.starttls.assert_called_once()
    assert server.ehlo.call_count == 2
    server.quit.assert_called_once()


def test_connection_credentials_trigger_login(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value

    _mailer(user="bob", password="s3cret").test_connection()

    server.login.assert_called_once_with("bob", "s3cret")
    server.quit.assert_called_once()


def test_connection_blank_user_never_calls_login(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value

    _mailer(user="", password="irrelevant").test_connection()

    server.login.assert_not_called()


def test_connection_auth_failure_propagates_and_still_quits(monkeypatch):
    from smtplib import SMTPAuthenticationError

    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value
    server.login.side_effect = SMTPAuthenticationError(535, b"Auth failed")

    mail = _mailer(user="bob", password="wrong-password")

    with pytest.raises(SMTPAuthenticationError):
        mail.test_connection()

    # quit() must still run (it's in a finally block) even though login failed
    server.quit.assert_called_once()


def test_connection_connect_failure_propagates(monkeypatch):
    from smtplib import SMTPConnectError

    mock_smtp = MagicMock(side_effect=SMTPConnectError(421, b"Cannot connect"))
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)

    with pytest.raises(SMTPConnectError):
        _mailer().test_connection()


def test_connection_starttls_failure_propagates_and_still_quits(monkeypatch):
    mock_smtp = MagicMock()
    monkeypatch.setattr("smtplib.SMTP", mock_smtp)
    server = mock_smtp.return_value
    server.starttls.side_effect = RuntimeError("STARTTLS not supported")

    mail = _mailer(tls=True)

    with pytest.raises(RuntimeError):
        mail.test_connection()

    server.quit.assert_called_once()
    server.login.assert_not_called()
