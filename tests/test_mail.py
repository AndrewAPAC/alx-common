import pytest
import os
import platform
from unittest.mock import patch
from alx.mail import ALXmail


def test_plain_email_body():
    mail = ALXmail(mail_type="plain")
    mail.set_from("sender@example.com")
    mail.add_recipient("recipient@example.com")
    mail.set_subject("Test Email")
    mail.add_paragraph("This is a test email.")

    msg = mail.get_mime_message()

    assert msg.get_content_type() == "text/plain"
    assert "This is a test email." in msg.get_payload()

def test_html_body_rendering():
    mail = ALXmail()
    mail.set_from("sender@example.com")
    mail.add_recipient("recipient@example.com")
    mail.set_subject("HTML Test")
    mail.add_html("<h1>This is HTML</h1>")

    msg = mail.get_mime_message()
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
    msg = mail.get_mime_message()

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
    msg = mail.get_mime_message()

    found = any(part.get_filename() == "test.png" for part in msg.walk())
    assert found, "Binary attachment not found"
