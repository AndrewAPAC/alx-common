# Copyright © 2019 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
# Provides a consistent framework for creating itrs toolkit samplers
# without the need to know internal details

from collections import OrderedDict
import sys


class Toolkit:
    def __init__(self, filename: str = None, display_on_exit: bool = True):
        """
        Populate and output an [ITRS geneos toolkit sampler](https://docs.itrsgroup.com/docs/geneos/7.2.0/collection/toolkit-plugin).

        :param filename: If a filename is set then the output goes to
        this file rather than the default of `sys.stdout`
        :param display_on_exit: When exiting the sampler with a call to
        `ok`, `warning` or `error` should the contents
        of the sampler be displayed?  Default is True
        """
        self.headlines = OrderedDict()
        """The headlines of the toolkit sampler, added using
        `add_headline`"""
        self.rows = []
        """A list of each row"""
        self.num_rows = 0
        """The number of rows - incremented as each row is added"""
        self.headings = []
        """A list of headings for the sampler"""
        self._num_columns = 0
        self._filename = filename
        self._display_on_exit = display_on_exit

    def add_headline(self, label: str, value):
        """
        Add a headline to the toolkit
        :param label: The label for the headline
        :param value: the value for the headline
        """
        self.headlines[label] = str(value).replace(",", "\\,")

    def add_headings(self, headings: str, delimiter: str = ','):
        """
        Add a list of headings to the sampler.  Each heading in the list
        is added with a call to `self.add_heading`

        :param headings: delimited string of headings
        :param delimiter: the delimiter (default ',')
        """
        for h in headings.split(delimiter):
            self.add_heading(h)

    def add_heading(self, heading: str):
        """
        Add a single column heading to the sampler
        :param heading: The heading string
        """
        heading = str(heading).strip()
        heading.replace(",", "\\,")
        self.headings.append(heading)
        self._num_columns += 1

    def add_row(self, values, delimiter=','):
        """
        Add a row to the sampler.  A list of values or a delimited string
        can be passed.  Handles quoting of values to ensure correct display

        :param values: A list of values or a delimited string
        :param delimiter: If a string is passed then each column is delimited
        by this character.  Default is ','
        """
        if isinstance(values, str):
            values = values.split(delimiter)

        for i, v in enumerate(values):
            v = str(v)
            values[i] = v.replace(",", "\\,")

        self.rows.append(values)
        self.num_rows += 1

    def error(self, message=''):
        """
        Exit the sampler with an error status and display the message parameter.
        **ERROR** *message*.  If `display_on_exit` is True then also
        output the contents of the sampler.  The script will
        exit with a status of 1

        :param message: The message to display after *ERROR*
        """
        self.add_headline("samplingStatus", "ERROR " + message)
        self._display()
        sys.exit(1)

    def warning(self, message=''):
        """
        Display the message parameter after a
        **WARN** status.  If `display_on_exit` is True then also
        output the contents of the sampler.

        :param message: The message to display after *WARN*
        """
        self.add_headline("samplingStatus", "WARN " + message)
        self._display()

    def ok(self, message=''):
        """
        Display the message parameter after an
        **OK** status.  If `display_on_exit` is True then also
        output the contents of the sampler.

        :param message: The message to display after *OK*
        """
        self.add_headline("samplingStatus", "OK " + message)
        self._display()

    def _display(self):
        if not self._display_on_exit:
            return

        if self._filename:
            fp = open(self._filename, "w")
        else:
            fp = sys.stdout

        print(",".join(self.headings), file=fp)
        for h in self.headlines:
            print("<!>{},{}".format(h, self.headlines[h]), file=fp)
        for r in self.rows:
            print(",".join(r), file=fp)

