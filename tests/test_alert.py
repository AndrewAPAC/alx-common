import pytest
from alx.itrs.alert import HtmlAlert
from alx.itrs.environment import Environment


@pytest.fixture
def populated_environment():
    env = Environment()
    env.severity = "warning"
    env.gateway = "Demo Gateway"
    env.application = "OMS"
    env.location = "Hong Kong"
    env.host = "host01"
    env.managed_entity = "OMS 1"
    env.sampler = "Order Monitor"
    env.dataview = "Orders"
    env.rowname = "orderCount"
    env.column = "Value"
    env.value = "999"
    env.dataview_columns = {
        "threshold": "1000",
        "units": "orders",
        "timestamp": "2025-07-24T15:32:01Z"
    }
    return env


def test_html_alert_create_generates_expected_html(populated_environment):
    alert = HtmlAlert(populated_environment)
    html = alert.create()

    # Check basic structure
    assert html.startswith("<body>\n<table>")
    assert html.endswith("</table>\n</body>\n")
    assert html.count("<tr>") >= 1
    assert html.count("<td>") >= 10

    # Check standard fields
    assert "Severity" in html
    assert "Warning" in html  # capitalised by .title()
    assert "Gateway" in html
    assert "Demo Gateway" in html
    assert "Application" in html
    assert "OMS" in html
    assert "Location" in html
    assert "Hong Kong" in html
    assert "Host" in html
    assert "host01" in html
    assert "Managed Entity" in html
    assert "OMS 1" in html
    assert "Sampler" in html
    assert "Order Monitor" in html
    assert "Dataview" in html
    assert "Orders" in html

    # Check alert content
    assert "orderCount Value is 999" in html

    # Check dataview_columns keys and values
    assert "threshold" in html
    assert "1000" in html
    assert "units" in html
    assert "orders" in html
    assert "timestamp" in html
    assert "2025-07-24T15:32:01Z" in html

    # Check style is applied for coloured cells
    assert "style=" in html

    # Optional: check absence of debug tags
    assert "<script" not in html
    assert "<style" not in html
