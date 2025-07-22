import re
import arrow
import time
from alx.date_util import date_subst


def test_basic_date_format():
    result = date_subst("%Y-%m-%d")
    assert re.match(r"\d{4}-\d{2}-\d{2}", result)


def test_readable_date_format():
    result = date_subst("%a, %b %d %Y")
    assert "," in result and len(result.split()) == 4


def test_time_with_timezone():
    result = date_subst("%H:%M:%S%z")
    assert re.match(r"\d{2}:\d{2}:\d{2}[+-]\d{4}", result)


def test_time_with_zone_label():
    result = date_subst("%H:%M:%S %Z")
    assert re.match(r"\d{2}:\d{2}:\d{2} \w+", result)


def test_time_only():
    result = date_subst("%H:%M:%S")
    assert re.match(r"\d{2}:\d{2}:\d{2}", result)


def test_custom_arrow_input():
    a = arrow.get(2013, 5, 5)
    result = date_subst("%a, %b %d %Y", a)
    assert result == "Sun, May 05 2013"
