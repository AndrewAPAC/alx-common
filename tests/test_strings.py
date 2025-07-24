import re
import pytest
import datetime
from alx.strings import (
    date_subst,
    normalize,
    replace_spaces,
    sanitize_filename
)


def test_date_subst_now():
    result = date_subst("%Y-%m-%d")
    assert re.match(r"\d{4}-\d{2}-\d{2}", result)


def test_date_subst_fixed_date():
    dt = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
    assert date_subst("%Y-%m-%d", when=dt) == "2000-01-01"


def test_normalize_basic():
    assert normalize("   Hello   World  ") == "hello world"


def test_normalize_empty():
    assert normalize("   ") == ""


def test_substitute_spaces_default():
    assert replace_spaces("a b c") == "a.b.c"


def test_substitute_spaces_custom_char():
    assert replace_spaces("a b c", "_") == "a_b_c"


def test_substitute_non_printables_removes_symbols():
    assert sanitize_filename("hello@world!") == "hello.world."


def test_substitute_non_printables_and_logic():
    assert sanitize_filename("fish & chips") == "fish.and.chips"


def test_substitute_non_printables_brackets():
    assert sanitize_filename("some (thing) [weird]") == "some.thing.weird"


def test_substitute_non_printables_dashes():
    assert sanitize_filename("word - word") == "word-word"


def test_substitute_non_printables_leading_trailing():
    assert sanitize_filename(" test & run ") == "test.and.run"


def test_substitute_non_printables_unicode():
    # Should replace all non-matching unicode characters
    assert sanitize_filename("sømé šträngę ñâmë") == "some.strange.name"


def test_substitute_non_printables_custom_char():
    assert sanitize_filename("bad@chars!", c="_") == "bad_chars_"

