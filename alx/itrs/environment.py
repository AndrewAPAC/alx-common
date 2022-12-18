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
            self.dataview = os.getenv("_DATAVIEW")
            self.plugin_name = os.getenv("_PLUGINNAME")
            self.rule = os.getenv("_RULE")
            self.host = os.getenv("_NETPROBE_HOST")
            self.severity = os.getenv("_SEVERITY")
            self.path = os.getenv("_VARIABLEPATH")
            self.assignee_email = os.getenv("_ASSIGNEE_EMAIL")
            self.assignee_name = os.getenv("_ASSIGNEE_USERNAME")
            self.assigner_name = os.getenv("_ASSIGNER_USERNAME")
            self.comment = os.getenv("_COMMENT")
            self.period_type = os.getenv("_PERIOD_TYPE")
        except Exception as e:
            raise("Environment error: %s", format(e))
