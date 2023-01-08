import os


class Environment:
    def __init__(self):
        try:
            self.location = os.getenv("location")
            self.application = os.getenv("application")
            self.environment = os.getenv("environment")
            self.variable = os.getenv("_VARIABLE")
            self.value = os.getenv("_VALUE")
            self.managed_entity = os.getenv("_MANAGED_ENTITY")
            self.sampler = os.getenv("_SAMPLER")
            self.gateway = os.getenv("_GATEWAY")
            self.rowname = os.getenv("_ROWNAME")
            self.column = os.getenv("_COLUMN")
            self.first_column = os.getenv("_FIRSTCOLUMN")
            self.dataview = os.getenv("_DATAVIEW")
            self.plugin_name = os.getenv("_PLUGINNAME")
            self.rule = os.getenv("_RULE")
            self.host = os.getenv("_NETPROBE_HOST")
            self.severity = os.getenv("_SEVERITY") or "critical"
            self.severity = self.severity.lower()
            self.path = os.getenv("_VARIABLEPATH")
            self.assignee_email = os.getenv("_ASSIGNEE_EMAIL")
            self.assignee_name = os.getenv("_ASSIGNEE_USERNAME")
            self.assigner_name = os.getenv("_ASSIGNER_USERNAME")
            self.comment = os.getenv("_COMMENT")
            self.period_type = os.getenv("_PERIOD_TYPE")
            self.clear = os.getenv("_CLEAR")
        except Exception as e:
            raise("Environment error: %s", format(e))

        self.dataview_columns = {}

        # Pull out all the columns from the dataview (only works if starts
        # with '_' and contains a lowercase letter
        for e in sorted(os.environ):
            if not e.startswith("_"):
                continue
            if e[1:] == self.first_column:
                continue
            if any(c for c in e if c.islower()):
                self.dataview_columns[e[1:]] = os.environ[e]
