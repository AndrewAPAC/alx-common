# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# pytest routines for alx.itrs.toolkit

import pytest
from io import StringIO
from unittest.mock import patch
from alx.itrs.toolkit import Toolkit
import tempfile
import os
from io import StringIO


def test_add_headline_escapes_commas():
    t = Toolkit()
    t.add_headline("key", "value,with,commas")
    assert t.headlines["key"] == "value\\,with\\,commas"


def test_add_headings_from_string():
    t = Toolkit()
    t.add_headings("a,b,c")
    assert t.headings == ["a", "b", "c"]
    assert t._num_columns == 3


def test_add_heading_strips_whitespace_and_escapes():
    t = Toolkit()
    t.add_heading(" heading , ")
    assert t.headings == ["heading ,"]
    assert t._num_columns == 1


def test_add_row_from_list():
    t = Toolkit()
    t.add_row(["a", "b", "c,d"])
    assert t.rows == [["a", "b", "c\\,d"]]
    assert t.num_rows == 1


def test_add_row_from_string():
    t = Toolkit()
    t.add_row("a,b,c,d")
    assert t.rows == [["a", "b", "c", "d"]]
    assert t.num_rows == 1


def test_toolkit_writes_to_file():
    with tempfile.NamedTemporaryFile(mode='r+', delete=False) as tmp:
        tmp_name = tmp.name

    try:
        t = Toolkit(filename=tmp_name)
        t.add_headings("Col1,Col2")
        t.add_row(["val1", "val2"])
        t.ok("All good")

        with open(tmp_name) as f:
            lines = f.read().splitlines()

        assert lines[0] == "Col1,Col2"
        assert "<!>samplingStatus,OK All good" in lines[1]
        assert "val1,val2" in lines[2]
    finally:
        os.remove(tmp_name)


def test_ok_outputs_csv():
    t = Toolkit(display_on_exit=True)
    t.add_headings("name,value")
    t.add_headline("status", "OK")
    t.add_row(["foo", 42])

    output = StringIO()
    with patch("sys.stdout", output):
        # Patch stdout *before* calling .ok()
        t.ok("everything fine")

    result = output.getvalue().splitlines()
    assert result[0] == "name,value"
    assert result[1] == "<!>status,OK"
    assert result[2] == "<!>samplingStatus,OK everything fine"
    assert result[3] == "foo,42"


def test_warning_includes_status():
    t = Toolkit()
    t.add_headings("name")
    output = StringIO()
    with patch("sys.stdout", output):
        t.warning("check this")
    assert "<!>samplingStatus,WARN check this" in output.getvalue()


def test_error_exits_with_status_1():
    t = Toolkit()
    t.add_headings("col1")

    output = StringIO()
    with patch("sys.stdout", output):
        with pytest.raises(SystemExit) as exc:
            t.error("something broke")
    assert exc.value.code == 1
    assert "<!>samplingStatus,ERROR something broke" in output.getvalue()


def test_display_disabled_on_exit():
    t = Toolkit(display_on_exit=False)
    t.add_headings("a")
    output = StringIO()
    with patch("sys.stdout", output):
        t.ok("nothing printed")
    assert output.getvalue() == ""
