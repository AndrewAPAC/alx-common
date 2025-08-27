# Copyright © 2019-2025 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
# String utility functions including normalization, trimming, and
# conversion between naming styles (e.g., space to underscore).

import re
from datetime import datetime, timezone
from unidecode import unidecode


def date_subst(fmt: str, when: datetime = None,
               tz: timezone = timezone.utc) -> str:
    """
    Return a formatted string of the date passed date according to
    `strftime`.

    :param fmt: date format as for strftime()
    :param when: the date to convert - default is now.
    :param tz: the timezone of the date.  default is UTC
    :return: the date as a formatted string
    """
    if not when:
        when = datetime.now(tz).astimezone()

    return when.strftime(fmt)


def normalize(s: str) -> str:
    """
    Normalize a string: trim, lowercase, collapse internal whitespace.

    :param s: The input string
    :return: The normalized string
    """
    return " ".join(s.strip().lower().split())


def replace_accents(s: str) -> str:
    """
    Convert accented characters to ASCII equivalents.

    E.g., é → e, ñ → n, ü → u

    :param s: Input string
    :return: ASCII-only version of string
    """
    return unidecode(s)


def replace_spaces(s: str, c: str = ".") -> str:
    """
    Replace spaces in a string with another character. Default is '.'

    :param s: The input string
    :param c: The character to use in the substitution., Default is '.'

    :return: The new string
    """
    return s.replace(" ", c)


def sanitize_filename(s: str, c: str = ".") -> str:
    """
    Remove all characters that are not suitable for Unix filenames.
    Essentially, all characters not in the set  [^a-zA-Z0-9._-] but
    also:
    ```
    * accents are removed: é becomes e
    * "word - word" -> "word-word"
    * `c ` -> `c`
    * & -> and
    ```

    :param s: The input string
    :param c: The character to use for the replacement. Default is '.'
    :return: The new string
    """
    s = s.strip()
    s = replace_accents(s)                                          # ✅ Normalize accents
    s = re.sub(r'\s*-\s*', '-', s)                 # "word - word" -> "word-word"
    s = re.sub(r'[()[\]\'{}]', '', s)               # Remove brackets, parens, quotes, braces
    s = re.sub(r'&', 'and', s)                      # & -> and
    s = replace_spaces(s, c)                                    # Replace spaces with `c`
    s = re.sub(rf'[^{re.escape(c)}a-zA-Z0-9._-]', c, s)   # Replace everything else

    return s
