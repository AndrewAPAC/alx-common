# Copyright © 2019 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
#
# Parses and handles ITRS Geneos alerts, creating am html
# table suitable for sending via email or other alert mechanism
#

from alx.html import ALXhtml
from alx.strings import date_subst
from alx.itrs.environment import Environment
from alx.app import ALXapp
import json


class HtmlAlert:
    def __init__(self, environment: Environment):
        """
        Create an HTML table of information suitable for an alert.
        This alert can be sent using the ALXmail module.  Currently,
        it is used for email alerts and user assignment events

        :param environment: The environment created in alx.itrs.environment.Environment
        """
        self.environment = environment
        """Stores the environment passed"""
        self.config = ALXapp.read_lib_config(self)
        """The module configuration read from `alx.ini`"""
        self.colours = json.loads(self.config.get("alert", "colours"))
        """The alert colours read from `alx.ini`"""
        self.date_format = self.config.get("alert", "date_format")
        """The alert date format read from `alx.ini`"""
        self.style = "background-color: %s;" % self.colours[environment.severity]
        """The additional styles for the cells coloured with the severity from colours"""

    def create(self) -> str:
        """
        Populate the HTML table with the values in the environment created
        in a call to alx.itrs.environment.Environment
        :return: the formatted HTML table
        """
        e = self.environment
        html = ALXhtml()

        html.add_table()
        html.add_headings(["Variable", "Value"])
        html.start_row()
        html.add_cell("Severity")
        html.add_cell(e.severity.title(), style=self.style)
        html.end_row()
        html.add_row(["Gateway", e.gateway])
        html.add_row(["Application", e.application])
        html.add_row(["Location", e.location])
        html.add_row(["Host", e.host])
        html.add_row(["Date", date_subst(self.date_format)])
        html.add_row(["Managed Entity", e.managed_entity])
        html.add_row(["Sampler", e.sampler])
        html.add_headings(["Dataview", e.dataview])
        html.start_row()
        html.add_cell("Value")
        html.add_cell("%s %s is %s" % (e.rowname, e.column, e.value),
                      style=self.style)
        html.end_row()

        if len(e.dataview_columns) > 0:
            html.add_headings(["Dataview Columns", ""])

            for c in e.dataview_columns:
                if e.dataview_columns[c]:
                    html.add_row([c, e.dataview_columns[c]])

        html.end_table()

        return html.body + "</body>\n"

    