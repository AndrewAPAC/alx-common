from datetime import datetime
import arrow


def date_subst(format, when=datetime.now()):
    """
    Return a formatted string of the date.

    :param format: date format as for strftime()
    :param when: the date to convert - default is now
    :return: the date as a formatted string
    """
    if type(when) == arrow.Arrow:
        when = when.datetime

    return when.strftime(format)


if __name__ == "__main__":
    print(date_subst("%Y-%m-%d"))
    print(date_subst("%a, %b %d %Y"))
    print(date_subst("%H:%M:%S"))
    a = arrow.get(2013, 5, 5)
    print(date_subst("%a, %b %d %Y", a))
