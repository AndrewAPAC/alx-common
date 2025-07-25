# Copyright © 2019 Andrew Lister
# License: GNU General Public License v3.0 (see LICENSE file)
#
# Description:
# Provides utilities for querying the environment when an alert
# or user assignemnt event is generated. Each environment variable
# is placed in a member of the class allowing for consistent
# retrieval and parsing
#
# Dataview columns are also placed in a dict:
#    self.dataview_columns["cpu"]
# to allow alert enrichment

import os


class Environment:
    def __init__(self):
        """
        Populate the `Environment` object with commonly found
        environment variables from [ITRS geneos actions](https://docs.itrsgroup.com/docs/geneos/7.2.0/processing/monitoring-and-alerts/geneos_rulesactionsalerts_tr/index.html#script-actions).
        Useful when writing actions and triggers.  Please refer to the
        source code to see what is set.
        """

        self.location = os.getenv("location")
        """The value of the environment variable `location` - the `location` attribute"""
        self.application = os.getenv("application")
        """The value of the environment variable `application` - the `application` attribute"""
        self.environment = os.getenv("environment")
        """The value of the environment variable `environment` - the `environment` attribute"""
        self.variable = os.getenv("_VARIABLE")
        """The value of the environment variable `_VARIABLE` - Short name of the data-item
        if it is a managed variable, in the form <!>name for headlines or row.col for table
         ells. This value is provided for backwards compatibility."""
        self.action = os.getenv("_ACTION")
        """The value of the environment variable `_ACTION` - The name of the action being triggered"""
        self.value = os.getenv("_VALUE")
        """The value of the environment variable `_VALUE` -
        The value of the dataview cell the data-item belongs to (if any)."""
        self.managed_entity = os.getenv("_MANAGED_ENTITY")
        """The value of the environment variable `_MANAGED_ENTITY` -
        The name of the managed entity the data-item belongs to (if any)."""
        self.sampler = os.getenv("_SAMPLER")
        """The value of the environment variable `_SAMPLER` -
        The name of the sampler the data-item belongs to (if any)."""
        self.sampler_type = os.getenv("_SAMPLER_TYPE")
        """The value of the environment variable `_SAMPLER_TYPE` -
        The type of the sampler the data-item belongs to (if any)."""
        self.sampler_group = os.getenv("_SAMPLER_GROUP")
        """The value of the environment variable `_SAMPLER_GROUP` -
        The group of the sampler the data-item belongs to (if any)."""
        self.gateway = os.getenv("_GATEWAY")
        """The value of the environment variable `_GATEWAY` - 
        The name of the gateway firing the action."""
        self.rowname = os.getenv("_ROWNAME")
        """The value of the environment variable `_ROWNAME` - 
        The row name of the dataview cell the data-item belongs to (if any).  
        If it is a headline variable, then it is set to `_HEADLINE`"""
        if not self.rowname:
            self.rowname = os.getenv("_HEADLINE")
        self.column = os.getenv("_COLUMN")
        """The value of the environment variable `_COLUMN` -
        The column name of the dataview cell the data-item belongs to (if any)."""
        self.first_column = os.getenv("_FIRSTCOLUMN")
        """The value of the environment variable `_FIRSTCOLUMN` - 
        The name of the first column of the dataview the data-item belongs to (if any)."""
        self.dataview = os.getenv("_DATAVIEW")
        """The value of the environment variable `_DATAVIEW` - 
        The name of the dataview the data-item belongs to (if any)."""
        self.plugin_name = os.getenv("_PLUGINNAME")
        """The value of the environment variable `_PLUGINNAME` -
        The plugin name of the sampler the data-item belongs to (if any)."""
        self.rule = os.getenv("_RULE")
        """The value of the environment variable `_RULE` -
        The rule that triggered this action. This is the full path 
        to the rule including the rule groups i.e. group1 > group 2 > rulename"""
        self.host = os.getenv("_NETPROBE_HOST")
        """The value of the environment variable `_NETPROBE_HOST` -
        The hostname of the probe the data-item belongs to (if any). """
        self.probe = os.getenv("_PROBE")
        """The value of the environment variable `_PROBE` -
        The name of the probe the data-item belongs to (if any)."""
        self.kba_urls = os.getenv("_KBA_URLS")
        """The value of the environment variable `_KBA_URLS` -
        A list of application knowledge base article URLs, separated by newlines."""
        self.severity = os.getenv("_SEVERITY") or "critical"
        """The value of the environment variable `_SEVERITY` -
        The data-item severity. One of UNDEFINED, OK, WARNING, CRITICAL or USER.
        Converted to lower case"""
        self.severity = self.severity.lower()
        self.path = os.getenv("_VARIABLEPATH")
        """The value of the environment variable `_VARIABLEPATH` - The full gateway path 
        to the data-item."""
        self.assignee_email = os.getenv("_ASSIGNEE_EMAIL")
        """The value of the environment variable `_ASSIGNEE_EMAIL` -
        Name of the Geneos user assigned this item. The name is taken 
        from the user definition in the authentication section."""
        self.assignee_name = os.getenv("_ASSIGNEE_USERNAME")
        """The value of the environment variable `_ASSIGNEE_USERNAME` -
        Email address of the Geneos user assigned this item. The address is taken from
        the user definition in the authentication section."""
        self.assigner_name = os.getenv("_ASSIGNER_USERNAME")
        """The value of the environment variable `_ASSIGNER_USERNAME` -
        Name of the Geneos user assigning this item to another. The name is taken from
        the user definition in the authentication section."""
        self.comment = os.getenv("_COMMENT")
        """The value of the environment variable `_COMMENT` -
        Comment entered by the assigner or the user who unassigned the item. If no 
        comment is provided, this variable is set to a blank string ("")."""
        self.previous_comment = os.getenv("_PREVIOUS_COMMENT")
        """The value of the environment variable `_PREVIOUS_COMMENT` -
        Contents of the _COMMENT environment variable from the previous 
        assign/unassign event. """
        self.period_type = os.getenv("_PERIOD_TYPE")
        """The value of the environment variable `_PERIOD_TYPE` - 
        Period for which the item is assigned:
        * **Manual** — Assigned to the user until unassigned.
        * **UntilOk** — Assigned until severity is OK.
        * **Until severity changes to specified** — Assigned until severity changed to one specified by assigner.
        * **Until severity changes from specified** — Assigned until severity changed from specified by assigner.
        * **Until a specific date / time** — Assigned until a specific date / time.
        * **Until severity changes to specified or until a specific date / time** — Assigned until severity changed to one specified by assigner or a specific date / time.
"""

        self.dataview_columns = {}
        """A dictionary of all the columns found on the current dataview. These are
        environment variables starting with `_` and followed by a lowercase
        letter"""
        # Pull out all the columns from the dataview (only works if starts
        # with '_' and contains a lowercase letter
        for e in sorted(os.environ):
            if not e.startswith("_"):
                continue
            if e[1:] == self.first_column:
                continue
            if any(c for c in e if c.islower()):
                self.dataview_columns[e[1:]] = os.environ[e]
