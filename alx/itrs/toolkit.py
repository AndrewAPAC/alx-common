from collections import OrderedDict
import sys


class Toolkit:
    def __init__(self, filename=None):
        self.end = None
        self.headlines = OrderedDict()
        self.rows = []
        self.num_rows = 0
        self.headings = []
        self.num_columns = 0
        self.filename = filename

    def add_headline(self, label, value):
        self.headlines[label] = value

    def add_headings(self, headings, delimiter=','):
        for h in headings.split(delimiter):
            self.add_heading(h)

    def add_heading(self, heading):
        heading = str(heading).strip()
        heading.replace(",", "\\,")
        self.headings.append(heading)
        self.num_columns += 1

    def add_row(self, values, delimiter=','):
        if isinstance(values, str):
            values = values.split(delimiter)

        for i, v in enumerate(values):
            v = str(v)
            values[i] = v.replace(",", "\\,")

        self.rows.append(values)
        self.num_rows += 1

    def error(self, message=''):
        self.add_headline("samplingStatus", "FAIL " + message)
        self._display()
        sys.exit(1)

    def warning(self, message=''):
        self.add_headline("samplingStatus", "WARN " + message)
        self._display()

    def ok(self, message=''):
        self.add_headline("samplingStatus", "OK " + message)
        self._display()

    def _display(self):
        if self.filename:
            fp = open(self.filename, "w")
        else:
            fp = sys.stdout

        print(",".join(self.headings), file=fp)
        for h in self.headlines:
            print("<!>{},{}".format(h, self.headlines[h]), file=fp)
        for r in self.rows:
            print(",".join(r), file=fp)

