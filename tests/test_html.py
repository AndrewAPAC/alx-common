import pytest
import requests
from alx.html import ALXhtml


def generate_sample_html():
    html = ALXhtml("XHTML Test")
    html.add_h1("W3C Test Heading")
    html.add_paragraph("Lorem ipsum dolor sit amet.")
    html.add_ul()
    html.add_item("One")
    html.add_item("Two")
    html.end_ul()
    return html.get_html()


def test_html_is_valid_according_to_w3c():
    html = generate_sample_html()
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "User-Agent": "ALX-Common HTML Validator Test"
    }
    params = {"out": "json"}

    resp = requests.post(
        "https://validator.w3.org/nu/",
        headers=headers,
        params=params,
        data=html.encode("utf-8"),
    )

    assert resp.status_code == 200, "W3C validator did not return OK"
    result = resp.json()

    errors = [m for m in result.get("messages", []) if m.get("type") == "error"]
    warnings = [
        m for m in result.get("messages", [])
        if m.get("type") == "info" and m.get("subtype") == "warning"
    ]
    assert not errors, f"HTML failed validation with {len(errors)} error(s): {[e['message'] for e in errors]}"
    assert len(warnings) == 0
