from datetime import datetime, timezone
import arrow


def date_subst(fmt: str, when: datetime | arrow.Arrow = None,
               tz: timezone = timezone.utc) -> str:
    """
    Return a formatted string of the date.

    :param fmt: date format as for strftime()
    :param when: the date to convert - default is now
    :param tz: the timezone of the date.  default is UTC
    :return: the date as a formatted string
    """
    if not when:
        when = datetime.now(tz).astimezone()

    if isinstance(when, arrow.Arrow):
        when = when.datetime

    return when.strftime(fmt)
